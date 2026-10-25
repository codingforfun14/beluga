'use strict';
// Percorsi e scritture sicure su disco. Tutto il resto del servizio passa da qui.
const fs = require('fs');
const path = require('path');
const crypto = require('crypto');

const ROOT = path.resolve(process.env.BELUGA_ROOT || path.join(__dirname, '..'));
const TASKS = path.join(ROOT, 'tasks');
const PROJECTS = path.join(ROOT, 'projects');
const ROLES = path.join(ROOT, 'roles');
const APP = path.join(ROOT, 'app');

const now = () => new Date().toISOString();
const hash = s => crypto.createHash('sha256').update(s).digest('hex');

// Scrittura atomica: file temporaneo nella stessa cartella, poi rename.
function writeAtomic(file, data) {
  fs.mkdirSync(path.dirname(file), { recursive: true });
  const tmp = `${file}.${process.pid}.${crypto.randomBytes(4).toString('hex')}.tmp`;
  fs.writeFileSync(tmp, data);
  fs.renameSync(tmp, file);
}
const writeJSON = (file, obj) => writeAtomic(file, JSON.stringify(obj, null, 2) + '\n');

function readJSON(file, fallback) {
  try { return JSON.parse(fs.readFileSync(file, 'utf8')); } catch { return fallback; }
}

// Log solo in aggiunta: una riga JSON per evento, mai riscritto.
function appendLine(file, obj) {
  fs.mkdirSync(path.dirname(file), { recursive: true });
  fs.appendFileSync(file, JSON.stringify({ ora: now(), ...obj }) + '\n');
}
function readLines(file) {
  try {
    return fs.readFileSync(file, 'utf8').split('\n').filter(Boolean).map(l => { try { return JSON.parse(l); } catch { return null; } }).filter(Boolean);
  } catch { return []; }
}

// Un processo è ancora vivo? (serve per capire se un lucchetto è rimasto orfano)
function alive(pid) {
  try { process.kill(pid, 0); return true; } catch (e) { return e.code === 'EPERM'; }
}

// Lucchetto con open 'wx': fallisce se il file esiste già, quindi un solo proprietario.
function lock(file, info = {}) {
  fs.mkdirSync(path.dirname(file), { recursive: true });
  for (let i = 0; i < 2; i++) {
    try {
      const fd = fs.openSync(file, 'wx');
      fs.writeSync(fd, JSON.stringify({ pid: process.pid, ora: now(), ...info }));
      fs.closeSync(fd);
      return true;
    } catch (e) {
      if (e.code !== 'EEXIST') throw e;
      const owner = readJSON(file, null);
      if (owner && alive(owner.pid)) return false;
      try { fs.unlinkSync(file); } catch {} // lucchetto orfano di un processo morto
    }
  }
  return false;
}
const unlock = file => { try { fs.unlinkSync(file); } catch {} };

// Solo nomi semplici: niente "..", niente barre. Protegge da percorsi inventati.
const safeName = s => typeof s === 'string' && /^[a-z0-9][a-z0-9-]{0,40}$/.test(s);

// modelli.json (su GitHub) + modelli.locale.json (solo su questo Mac: percorsi, modello, chi lavora).
const MODELLI = path.join(ROOT, 'modelli.json');
const MODELLI_LOCALE = path.join(ROOT, 'modelli.locale.json');
const isObj = v => v && typeof v === 'object' && !Array.isArray(v);
function merge(a, b) {
  const out = { ...a };
  for (const [k, v] of Object.entries(b || {})) out[k] = isObj(v) && isObj(a[k]) ? merge(a[k], v) : v;
  return out;
}
const readModelli = () => merge(readJSON(MODELLI, { ruoli: {} }), readJSON(MODELLI_LOCALE, {}));

module.exports = { MODELLI, MODELLI_LOCALE, readModelli, merge, ROOT, TASKS, PROJECTS, ROLES, APP, now, hash, writeAtomic, writeJSON, readJSON, appendLine, readLines, alive, lock, unlock, safeName };
