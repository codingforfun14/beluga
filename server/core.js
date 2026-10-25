'use strict';
// Incarichi, chat e worker. Gli incarichi sono file JSON in tasks/, con un log degli eventi accanto.
const fs = require('fs');
const path = require('path');
const L = require('./lib');
const ideas = require('./ideas');
const agents = require('./agents');

const STATI = ['in_coda', 'in_corso', 'attesa_fede', 'completato', 'fallito', 'annullato', 'da_verificare'];
const file = id => path.join(L.TASKS, `${id}.json`);
const logFile = id => path.join(L.TASKS, `${id}.log`);
const runLock = id => path.join(L.TASKS, `${id}.lock`);
const CHAT = path.join(L.TASKS, 'chat.jsonl');
const AGENTI = path.join(L.TASKS, 'agenti.json');
const v2 = n => String(n).padStart(2, '0');

const modelli = () => L.readJSON(path.join(L.ROOT, 'modelli.json'), { ruoli: {} });
const projects = () => {
  try { return fs.readdirSync(L.PROJECTS).filter(p => L.safeName(p) && fs.existsSync(path.join(L.PROJECTS, p, 'CONTESTO.md'))); } catch { return []; }
};

/* ---------- incarichi ---------- */

function list() {
  let names = [];
  try { names = fs.readdirSync(L.TASKS).filter(n => /^t-[a-z0-9-]+\.json$/.test(n)); } catch {}
  return names.map(n => L.readJSON(path.join(L.TASKS, n), null)).filter(Boolean).sort((a, b) => b.creato.localeCompare(a.creato));
}
const get = id => (typeof id === 'string' && /^t-[a-z0-9-]+$/.test(id) ? L.readJSON(file(id), null) : null);

function save(task, evento, extra = {}) {
  task.aggiornato = L.now();
  L.writeJSON(file(task.id), task);
  if (evento) L.appendLine(logFile(task.id), { evento, stato: task.stato, versione: task.versione, ...extra });
  return task;
}

const workDir = t => path.join(L.PROJECTS, t.progetto, 'work', t.id, `v${v2(t.versione)}`);
const rel = f => path.relative(L.ROOT, f);

function create({ progetto, ruolo, tipo, richiesta }) {
  const norm = richiesta.trim().toLowerCase().replace(/\s+/g, ' ');
  const impronta = L.hash(`${progetto}|${ruolo}|${tipo}|${norm}`).slice(0, 16);
  // Stessa richiesta ancora aperta: niente secondo incarico.
  const same = list().find(t => t.impronta === impronta && !['annullato', 'completato'].includes(t.stato));
  if (same) return { task: same, doppio: true };
  const d = new Date();
  const id = `t-${d.toISOString().slice(0, 10).replace(/-/g, '')}-${d.toISOString().slice(11, 19).replace(/:/g, '')}-${impronta.slice(0, 6)}`;
  const conf = modelli().ruoli[ruolo] || {};
  const task = {
    id, progetto, ruolo, tipo, richiesta: richiesta.trim(),
    titolo: (t => t.charAt(0).toUpperCase() + t.slice(1))(richiesta.trim().replace(/^niko[,:]?\s*/i, '').slice(0, 80)),
    versione: 1, input: [], output_attesi: [], stato: 'in_coda',
    agente: { programma: conf.programma || null, temporaneo: !!conf.temporaneo },
    creato: L.now(), aggiornato: L.now(), errore: null, risultato: null, revisioni: [], impronta,
  };
  task.output_attesi = [rel(path.join(workDir(task), 'idee.json'))];
  // il lucchetto sul file evita due incarichi creati nello stesso istante
  if (!L.lock(file(id) + '.new')) return { task: get(id), doppio: true };
  try { save(task, 'creato'); } finally { L.unlock(file(id) + '.new'); }
  return { task, doppio: false };
}

/* ---------- chat ---------- */

const chat = () => L.readLines(CHAT);
const say = (da, testo, task) => L.appendLine(CHAT, { da, testo, task: task || undefined });

function agentLabel(t) {
  const p = process.env.BELUGA_AGENTE_FINTO ? 'agente finto di test' : t.agente.programma === 'codex' ? 'ChatGPT (Codex)' : t.agente.programma === 'claude' ? 'Claude' : 'nessun programma';
  return `${p}${t.agente.temporaneo ? ', temporaneo' : ''}`;
}

// Capire cosa vuole Fede. Per ora a regole: Niko non chiama un modello per smistare.
function receive(body) {
  const testo = String(body.testo || '').trim().slice(0, 4000);
  if (!testo) return { errore: 'Messaggio vuoto.' };
  say('fede', testo);
  const known = projects();
  let progetto = L.safeName(body.progetto) && known.includes(body.progetto) ? body.progetto : null;
  if (!progetto) progetto = known.find(p => new RegExp(`\\b${p.replace('mezzeuro', 'mezz[o ]?euro')}\\b`, 'i').test(testo)) || null;
  const wantsIdeas = /\bide[ae]\b|propon|hook|spunt|concept/i.test(testo);
  const wantsVideo = /blender|render|hyperframes|anima|video|scena/i.test(testo);
  if (!wantsIdeas) {
    const r = wantsVideo
      ? 'Video e render arrivano nella prossima fase. Per ora so far partire solo l\'Ideatore: chiedimi delle idee.'
      : 'Per ora so fare una cosa sola: chiedere idee all\'Ideatore. Prova con "proponi tre idee per un reel di mezzeuro sul fondo emergenze".';
    say('niko', r);
    return { risposta: r };
  }
  if (!progetto) {
    const r = `Per quale progetto? ${known.length ? 'Ho questi: ' + known.join(', ') + '. ' : ''}Scegli il progetto nella barra o scrivilo nel messaggio.`;
    say('niko', r);
    return { risposta: r, chiarimento: true };
  }
  const { task, doppio } = create({ progetto, ruolo: 'ideatore', tipo: 'idee', richiesta: testo });
  if (doppio) {
    const r = 'Questa richiesta c\'è già, non ne apro una seconda. La trovi in Lavori.';
    say('niko', r, task.id);
    return { risposta: r, task: task.id, doppio: true };
  }
  const r = `Ricevuto. Lo passo all'Ideatore (${agentLabel(task)}). Ti scrivo qui quando c'è il risultato.`;
  say('niko', r, task.id);
  return { risposta: r, task: task.id };
}

/* ---------- piano B ---------- */

function planBPrompt(t) {
  const f = path.join(workDir(t), 'prompt.md');
  if (!fs.existsSync(f)) L.writeAtomic(f, ideas.buildPrompt(t));
  return fs.readFileSync(f, 'utf8');
}

function storeResult(t, testo, origine) {
  const v = ideas.validate(testo);
  const dir = workDir(t);
  L.writeAtomic(path.join(dir, origine === 'manuale' ? 'risposta-manuale.txt' : 'risposta-agente.txt'), String(testo || ''));
  if (!v.ok) return v;
  L.writeJSON(path.join(dir, 'idee.json'), { incarico: t.id, versione: t.versione, origine, creato: L.now(), idee: v.idee });
  L.writeAtomic(path.join(dir, 'idee.md'), ideas.toMarkdown(t, v.idee, origine === 'manuale' ? 'risposta incollata a mano da Fede (piano B)' : agentLabel(t)));
  t.risultato = { file: rel(path.join(dir, 'idee.json')), markdown: rel(path.join(dir, 'idee.md')), origine, idee: v.idee };
  return v;
}

/* ---------- azioni di Fede ---------- */

function act(id, azione, body = {}) {
  const t = get(id);
  if (!t) return { errore: 'Incarico non trovato.', codice: 404 };
  const no = msg => ({ errore: msg, codice: 409 });
  if (azione === 'manuale') {
    if (!['fallito', 'da_verificare', 'in_coda'].includes(t.stato)) return no('Il piano B serve solo per un incarico fermo o in attesa.');
    const v = storeResult(t, String(body.testo || '').slice(0, 100000), 'manuale');
    if (!v.ok) { save(t, 'risposta_manuale_non_valida', { motivo: v.errore }); return { errore: `La risposta incollata non va bene: ${v.errore}`, codice: 422 }; }
    t.stato = 'attesa_fede'; t.errore = null;
    save(t, 'risposta_manuale', { file: t.risultato.file });
    say('niko', `Ho salvato la risposta che hai incollato (versione ${v2(t.versione)}). Scegli l'idea che preferisci.`, t.id);
    return { task: t };
  }
  if (azione === 'riprova') {
    if (!['fallito', 'da_verificare'].includes(t.stato)) return no('Si può rilanciare solo un incarico fallito o da verificare.');
    t.stato = 'in_coda'; t.errore = null;
    save(t, 'rilanciato_da_fede');
    return { task: t };
  }
  if (azione === 'approva') {
    if (t.stato !== 'attesa_fede' || !t.risultato) return no('Non c\'è niente da approvare.');
    const n = Number(body.scelta);
    if (!Number.isInteger(n) || n < 0 || n >= t.risultato.idee.length) return { errore: 'Scelta non valida.', codice: 422 };
    t.stato = 'completato'; t.scelta = { indice: n, titolo: t.risultato.idee[n].titolo, versione: t.versione };
    save(t, 'approvato', { scelta: n });
    say('niko', `Perfetto, teniamo "${t.scelta.titolo}" (versione ${v2(t.versione)}).`, t.id);
    return { task: t };
  }
  if (azione === 'modifica') {
    const testo = String(body.testo || '').trim().slice(0, 2000);
    if (!testo) return { errore: 'Scrivi cosa vuoi cambiare.', codice: 422 };
    if (!['attesa_fede', 'completato'].includes(t.stato)) return no('Si possono chiedere modifiche solo a un risultato pronto.');
    say('fede', testo);
    t.revisioni.push({ da: t.versione, testo, ora: L.now() });
    t.versione += 1; t.stato = 'in_coda'; t.risultato = null; t.errore = null; delete t.scelta;
    t.output_attesi = [rel(path.join(workDir(t), 'idee.json'))];
    save(t, 'modifica_chiesta', { testo });
    say('niko', `Ok, preparo la versione ${v2(t.versione)} con le tue modifiche.`, t.id);
    return { task: t };
  }
  if (azione === 'annulla') {
    if (t.stato === 'in_corso') return no('È in corso: aspetta che finisca, poi annullalo.');
    if (['annullato', 'completato'].includes(t.stato)) return no('È già chiuso.');
    t.stato = 'annullato';
    save(t, 'annullato');
    return { task: t };
  }
  return { errore: 'Azione sconosciuta.', codice: 400 };
}

/* ---------- worker: un incarico alla volta ---------- */

const WORKER_LOCK = path.join(L.TASKS, '.worker.lock');
let busy = false, timer = null;

// Dopo un'interruzione: se il risultato c'è ed è valido lo recupero, altrimenti "da verificare".
function recover() {
  for (const t of list().filter(t => t.stato === 'in_corso')) {
    const owner = L.readJSON(runLock(t.id), null);
    if (owner && L.alive(owner.pid) && owner.pid !== process.pid) continue;
    const out = path.join(workDir(t), 'idee.json');
    const saved = L.readJSON(out, null);
    if (saved && ideas.validate(JSON.stringify({ idee: saved.idee })).ok) {
      t.risultato = { file: rel(out), markdown: rel(path.join(workDir(t), 'idee.md')), origine: saved.origine, idee: saved.idee };
      t.stato = 'attesa_fede';
      save(t, 'recuperato_dopo_interruzione');
    } else {
      t.stato = 'da_verificare';
      t.errore = { tipo: 'interrotto', messaggio: 'Il servizio si è fermato mentre l\'agente lavorava. Non so se ha finito: controlla e rilancia se serve.' };
      save(t, 'interrotto');
    }
    L.unlock(runLock(t.id));
  }
}

async function runOne(t) {
  if (!L.lock(runLock(t.id), { incarico: t.id })) return; // un altro worker l'ha preso
  const tmp = path.join(L.PROJECTS, t.progetto, 'tmp', `run-${t.id}-v${v2(t.versione)}`);
  try {
    const fresh = get(t.id);
    if (!fresh || fresh.stato !== 'in_coda') return;
    t = fresh;
    const conf = modelli().ruoli[t.ruolo] || {};
    t.agente = { programma: conf.programma || null, temporaneo: !!conf.temporaneo };
    t.stato = 'in_corso'; t.iniziato = L.now();
    save(t, 'avviato', { programma: t.agente.programma });
    const prompt = ideas.buildPrompt(t);
    L.writeAtomic(path.join(workDir(t), 'prompt.md'), prompt);
    const a = agents.adapter(t.agente.programma);
    fs.mkdirSync(tmp, { recursive: true });
    const r = a ? await a.call(prompt, { cwd: tmp }) : { ok: false, errore: { tipo: 'programma_assente', messaggio: `Nessun programma configurato per il ruolo ${t.ruolo} in modelli.json.` } };
    t = get(t.id);
    if (!r.ok) {
      t.stato = 'fallito'; t.errore = r.errore;
      save(t, 'agente_non_disponibile', { errore: r.errore, dettagli: r.dettagli });
      say('niko', `L'Ideatore non è partito: ${r.errore.messaggio} Puoi usare il piano B dalla scheda.`, t.id);
      return;
    }
    if (!process.env.BELUGA_AGENTE_FINTO) {
      const st = L.readJSON(AGENTI, {});
      st[t.agente.programma] = { verificato: L.now() };
      L.writeJSON(AGENTI, st);
    }
    const v = storeResult(t, r.testo, 'agente');
    if (!v.ok) {
      t.stato = 'fallito'; t.errore = { tipo: 'risposta_non_valida', messaggio: v.errore };
      save(t, 'risposta_non_valida', { motivo: v.errore, dettagli: r.dettagli });
      say('niko', `L'Ideatore ha risposto, ma la risposta non va bene: ${v.errore} Puoi rilanciarlo o usare il piano B.`, t.id);
      return;
    }
    t.stato = 'attesa_fede'; t.errore = null;
    save(t, 'risultato_salvato', { file: t.risultato.file, dettagli: r.dettagli });
    say('niko', `Ecco le 3 idee (versione ${v2(t.versione)}). Le ho salvate in ${t.risultato.markdown}. Scegli quella che preferisci.`, t.id);
  } catch (e) {
    const cur = get(t.id);
    if (cur) { cur.stato = 'fallito'; cur.errore = { tipo: 'altro', messaggio: String(e.message || e) }; save(cur, 'errore_interno'); }
  } finally {
    fs.rmSync(tmp, { recursive: true, force: true }); // solo la cartella temporanea di questo lancio
    L.unlock(runLock(t.id));
  }
}

async function tick() {
  if (busy) return;
  const next = list().filter(t => t.stato === 'in_coda').sort((a, b) => a.aggiornato.localeCompare(b.aggiornato))[0];
  if (!next) return;
  busy = true;
  try { await runOne(next); } finally { busy = false; }
}

function startWorker() {
  if (!L.lock(WORKER_LOCK, { ruolo: 'worker' })) return false;
  recover();
  timer = setInterval(tick, 1000);
  tick();
  return true;
}
function stopWorker() { clearInterval(timer); L.unlock(WORKER_LOCK); }

/* ---------- stato dei collegamenti ---------- */

async function status() {
  const conf = modelli();
  const verified = L.readJSON(AGENTI, {});
  const used = [...new Set(Object.values(conf.ruoli).map(r => r.programma).filter(Boolean))];
  const programmi = {};
  for (const p of used) programmi[p] = { ...(await agents.probe(p)), ultimo_successo: (verified[p] || {}).verificato || null };
  return { modalita: process.env.BELUGA_AGENTE_FINTO ? 'test' : 'reale', ruoli: conf.ruoli, programmi, progetti: projects(), worker: !!timer };
}

module.exports = { STATI, list, get, receive, act, chat, startWorker, stopWorker, status, planBPrompt, projects, workDir };
