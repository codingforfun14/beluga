'use strict';
// Adattatori verso i programmi ufficiali da terminale. Nessuna API, nessuna shell:
// ogni programma parte con argomenti separati e il prompt arriva su stdin.
const { spawn } = require('child_process');
const fs = require('fs');
const path = require('path');

const LIMIT = 2 * 1024 * 1024;
const { readModelli } = require('./lib');
// Percorso del programma: da modelli.json ("programmi") se indicato, altrimenti il nome nel PATH.
function conf(name) {
  const c = readModelli(); return (c.programmi && c.programmi[name]) || {};
}
const bin = name => conf(name).percorso || name;
// Modello scelto in modelli.json solo per le chiamate di Niko: il config personale del programma resta com'è.
const model = name => { const m = conf(name).modello; return typeof m === 'string' && /^[A-Za-z0-9._:-]{1,64}$/.test(m) ? m : null; };
const TIMEOUT = Number(process.env.BELUGA_TIMEOUT_MS) || 6 * 60 * 1000;

function run(bin, args, { input = '', cwd, timeout = TIMEOUT } = {}) {
  return new Promise(resolve => {
    let out = '', err = '', done = false, child;
    const finish = r => { if (!done) { done = true; clearTimeout(timer); resolve(r); } };
    try {
      child = spawn(bin, args, { cwd, shell: false, stdio: ['pipe', 'pipe', 'pipe'], env: process.env });
    } catch (e) { return finish({ code: null, out, err, spawnError: e }); }
    const timer = setTimeout(() => { child.kill('SIGTERM'); finish({ code: null, out, err, timedOut: true }); }, timeout);
    child.on('error', e => finish({ code: null, out, err, spawnError: e }));
    child.stdout.on('data', d => { if (out.length < LIMIT) out += d; });
    child.stderr.on('data', d => { if (err.length < LIMIT) err += d; });
    child.on('close', code => finish({ code, out, err }));
    child.stdin.on('error', () => {});
    child.stdin.end(input);
  });
}

// Tipi di errore: programma_assente, autenticazione, limite, tempo_scaduto, altro
function classify(r, text = '') {
  if (r.spawnError && r.spawnError.code === 'ENOENT') return { tipo: 'programma_assente', messaggio: 'Il programma non è installato o non è nel PATH.' };
  if (r.timedOut) return { tipo: 'tempo_scaduto', messaggio: 'L\'agente non ha risposto in tempo.' };
  const all = `${text}\n${r.err}\n${r.out}`;
  if (/usage limit|rate limit|limit reached|quota|too many requests|\b429\b|limite/i.test(all)) return { tipo: 'limite', messaggio: 'Limite del piano raggiunto.' };
  if (/not logged in|log ?in|authenticat|unauthori[sz]ed|invalid api key|\b401\b|credential|oauth/i.test(all)) return { tipo: 'autenticazione', messaggio: 'Accesso all\'account non valido o scaduto.' };
  const tail = (r.err || text || r.out || '').trim().split('\n').slice(-3).join(' ').slice(0, 300);
  return { tipo: 'altro', messaggio: tail || `Il programma è terminato con codice ${r.code}.` };
}

// Le opzioni cambiano tra versioni: leggo l'help una volta e uso solo quelle presenti.
const helpCache = {};
async function help(bin, args) {
  const k = bin + args.join(' ');
  if (!(k in helpCache)) { const r = await run(bin, args, { timeout: 15000 }); helpCache[k] = r.code === 0 ? r.out + r.err : ''; }
  return helpCache[k];
}

const claude = {
  name: 'claude',
  async call(prompt, { cwd }) {
    const h = await help(bin('claude'), ['--help']);
    const args = ['-p', '--output-format', 'json'];
    // Per le idee non servono strumenti: niente file, niente comandi, niente server MCP.
    if (h.includes('--no-session-persistence')) args.push('--no-session-persistence');
    if (/--tools\b/.test(h.replace(/--(allowed|disallowed)Tools|--(allowed|disallowed)-tools/g, ''))) args.push('--tools', '');
    if (h.includes('--strict-mcp-config')) args.push('--strict-mcp-config');
    if (h.includes('--safe-mode')) args.push('--safe-mode');
    if (h.includes('dontAsk')) args.push('--permission-mode', 'dontAsk');
    const r = await run(bin('claude'), args, { input: prompt, cwd });
    if (r.spawnError || r.timedOut) return { ok: false, errore: classify(r) };
    let data = null;
    try { data = JSON.parse(r.out); } catch {}
    if (r.code !== 0 || !data || data.is_error || data.subtype !== 'success') {
      return { ok: false, errore: classify(data ? { ...r, out: '' } : r, data && typeof data.result === 'string' ? data.result : ''), dettagli: { codice: r.code } };
    }
    return { ok: true, testo: data.result, dettagli: { costo_usd: data.total_cost_usd, durata_ms: data.duration_ms, sessione: data.session_id } };
  },
};

const codex = {
  name: 'codex',
  async call(prompt, { cwd }) {
    const h = await help(bin('codex'), ['exec', '--help']);
    const last = path.join(cwd, 'ultima-risposta.txt');
    const args = ['exec'];
    if (h.includes('--skip-git-repo-check')) args.push('--skip-git-repo-check');
    if (h.includes('--sandbox')) args.push('--sandbox', 'read-only');
    if (h.includes('--color')) args.push('--color', 'never');
    if (model('codex') && h.includes('--model')) args.push('--model', model('codex'));
    const useLast = h.includes('--output-last-message');
    if (useLast) args.push('--output-last-message', last);
    args.push('-'); // il prompt arriva da stdin
    const r = await run(bin('codex'), args, { input: prompt, cwd });
    if (r.spawnError || r.timedOut || r.code !== 0) return { ok: false, errore: classify(r), dettagli: { codice: r.code } };
    const testo = useLast && fs.existsSync(last) ? fs.readFileSync(last, 'utf8') : r.out;
    return { ok: true, testo };
  },
};

// Solo per i test automatici: BELUGA_AGENTE_FINTO=buono|vuoto|rotto|assente|accesso|limite
const fake = {
  name: 'finto',
  async call() {
    const mode = process.env.BELUGA_AGENTE_FINTO;
    await new Promise(r => setTimeout(r, Number(process.env.BELUGA_FINTO_MS) || 150));
    if (mode === 'assente') return { ok: false, errore: { tipo: 'programma_assente', messaggio: 'Il programma non è installato o non è nel PATH.' } };
    if (mode === 'accesso') return { ok: false, errore: { tipo: 'autenticazione', messaggio: 'Accesso all\'account non valido o scaduto.' } };
    if (mode === 'limite') return { ok: false, errore: { tipo: 'limite', messaggio: 'Limite del piano raggiunto.' } };
    if (mode === 'vuoto') return { ok: true, testo: '' };
    if (mode === 'rotto') return { ok: true, testo: 'Ecco tre idee: 1) ... 2) ... 3) ...' };
    const idea = n => ({ titolo: `Idea di prova ${n}`, hook: `Hook di prova ${n}`, sviluppo: `Sviluppo di prova ${n}.`, momento: `Momento di prova ${n}.`, direzione_visiva: `Direzione visiva di prova ${n}.`, scaletta: ['0-2 s: hook', '2-10 s: sviluppo', '10-15 s: chiusura'] });
    const brief = { messaggio: 'Messaggio di prova', insight: 'Insight di prova', prova: 'Prova di prova' };
    return { ok: true, testo: JSON.stringify({ brief, idee: [idea(1), idea(2), idea(3)] }) };
  },
};

function adapter(programma) {
  if (process.env.BELUGA_AGENTE_FINTO) return fake;
  return { claude, codex }[programma] || null;
}

// Controllo leggero, senza consumare messaggi: il programma c'è? che versione?
async function probe(programma) {
  if (process.env.BELUGA_AGENTE_FINTO) return { programma: 'finto', installato: true, versione: 'test' };
  const r = await run(bin(programma), ['--version'], { timeout: 15000 });
  const res = { programma, installato: r.code === 0, versione: r.code === 0 ? r.out.trim().split('\n')[0] : null };
  if (programma === 'codex' && res.installato) {
    const s = await run(bin('codex'), ['login', 'status'], { timeout: 15000 });
    res.accesso = s.code === 0 ? (s.out + s.err).trim().split('\n')[0] : 'non verificato';
  }
  return res;
}

module.exports = { adapter, probe, classify, run };
