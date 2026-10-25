'use strict';
// Prove automatiche del servizio con l'agente finto, in una cartella temporanea.
// Non toccano tasks/ e projects/ veri e non chiamano nessun modello.
// Uso: node server/test.js
const { spawn } = require('child_process');
const fs = require('fs');
const os = require('os');
const path = require('path');
const http = require('http');
const assert = require('assert');

const SRC = path.join(__dirname, '..');
const ROOT = fs.mkdtempSync(path.join(os.tmpdir(), 'beluga-test-'));
for (const d of ['modelli.json', 'roles', 'projects/mezzeuro/CONTESTO.md', 'projects/mezzeuro/libreria.json', 'app']) {
  fs.cpSync(path.join(SRC, d), path.join(ROOT, d), { recursive: true });
}
fs.mkdirSync(path.join(ROOT, 'tasks'));
const PORT = 4199;
let srv;

function start(mode, ms) {
  return new Promise((resolve, reject) => {
    srv = spawn(process.execPath, [path.join(__dirname, 'server.js')], { env: { ...process.env, BELUGA_ROOT: ROOT, BELUGA_PORT: PORT, BELUGA_AGENTE_FINTO: mode, BELUGA_FINTO_MS: ms || 100 } });
    srv.stdout.on('data', d => { if (/acceso/.test(d)) resolve(); });
    srv.stderr.on('data', d => process.stderr.write(d));
    srv.on('exit', c => reject(new Error('server uscito ' + c)));
  });
}
const stop = () => new Promise(r => { srv.removeAllListeners('exit'); srv.on('exit', r); srv.kill('SIGTERM'); });
const kill = () => new Promise(r => { srv.removeAllListeners('exit'); srv.on('exit', r); srv.kill('SIGKILL'); });

function req(method, p, body, headers = {}) {
  return new Promise((resolve, reject) => {
    const data = body ? JSON.stringify(body) : null;
    const h = { Host: `127.0.0.1:${PORT}`, ...(data ? { 'Content-Type': 'application/json', 'X-Niko': '1' } : {}), ...headers };
    const r = http.request({ host: '127.0.0.1', port: PORT, method, path: p, headers: h }, res => {
      let s = ''; res.on('data', c => s += c); res.on('end', () => { let j = null; try { j = JSON.parse(s); } catch {} resolve({ code: res.statusCode, body: j, text: s }); });
    });
    r.on('error', reject);
    if (data) r.write(data);
    r.end();
  });
}
const post = (p, b, h) => req('POST', p, b, h);
const get = p => req('GET', p);
const wait = ms => new Promise(r => setTimeout(r, ms));
async function until(id, states, ms = 5000) {
  const end = Date.now() + ms;
  while (Date.now() < end) {
    const t = (await get('/api/lavori')).body.find(x => x.id === id);
    if (t && states.includes(t.stato)) return t;
    await wait(100);
  }
  throw new Error(`timeout aspettando ${states} per ${id}`);
}

const results = [];
async function test(name, fn) {
  try { await fn(); results.push(['OK  ', name]); } catch (e) { results.push(['FAIL', name + ' → ' + e.message]); }
}

(async () => {
  await start('buono');
  let firstId;

  await test('1. Richiesta normale: tre idee salvate e visibili', async () => {
    const r = await post('/api/messaggi', { testo: 'Niko, proponi tre idee per un reel di mezzeuro sul fondo emergenze' });
    assert.ok(r.body.task, 'nessun incarico creato');
    firstId = r.body.task;
    const t = await until(firstId, ['attesa_fede']);
    assert.strictEqual(t.risultato.idee.length, 3);
    assert.ok(fs.existsSync(path.join(ROOT, t.risultato.file)), 'file idee.json mancante');
    assert.ok(fs.existsSync(path.join(ROOT, t.risultato.markdown)), 'file idee.md mancante');
    assert.ok(t.risultato.file.includes('/v01/'), 'versione non nel percorso');
    const chat = (await get('/api/chat')).body;
    assert.ok(chat.some(m => m.task === firstId && /Ecco le 3 idee/.test(m.testo)), 'risultato non in chat');
  });

  await test('2. Progetto mancante: Niko chiede quale', async () => {
    const r = await post('/api/messaggi', { testo: 'proponi tre idee per un reel sul conto corrente' });
    assert.ok(r.body.chiarimento && !r.body.task);
  });

  await test('5. Doppio invio: un solo incarico', async () => {
    const a = await post('/api/messaggi', { testo: 'Proponi tre idee per un carosello di mezzeuro sulle carte prepagate' });
    const b = await post('/api/messaggi', { testo: 'proponi  tre idee per un carosello di mezzeuro sulle carte prepagate' });
    assert.strictEqual(a.body.task, b.body.task);
    assert.ok(b.body.doppio);
    const n = (await get('/api/lavori')).body.filter(t => t.id === a.body.task).length;
    assert.strictEqual(n, 1);
    await until(a.body.task, ['attesa_fede']);
  });

  await test('Approvazione e richiesta di modifiche creano la versione 02', async () => {
    const ap = await post(`/api/lavori/${firstId}/approva`, { scelta: 1 });
    assert.strictEqual(ap.body.task.stato, 'completato');
    const md = await post(`/api/lavori/${firstId}/modifica`, { testo: 'Più ironiche' });
    assert.strictEqual(md.body.task.versione, 2);
    const t = await until(firstId, ['attesa_fede']);
    assert.ok(t.risultato.file.includes('/v02/'));
    assert.ok(fs.existsSync(path.join(ROOT, 'projects/mezzeuro/work', firstId, 'v01', 'idee.json')), 'la v01 non deve sparire');
  });

  await test('Sicurezza: scritture da altri siti e host estranei rifiutati', async () => {
    assert.strictEqual((await post('/api/messaggi', { testo: 'idee mezzeuro' }, { 'X-Niko': '' })).code, 403);
    assert.strictEqual((await post('/api/messaggi', { testo: 'idee mezzeuro' }, { Origin: 'https://cattivo.example' })).code, 403);
    assert.strictEqual((await req('GET', '/api/lavori', null, { Host: 'cattivo.example:4199' })).code, 421);
    assert.strictEqual((await get('/../modelli.json')).code, 404);
    assert.strictEqual((await get('/%2e%2e/modelli.json')).code, 404);
  });

  await test('Chi lavora: Fede assegna l\'Ideatore, ruoli e programmi non previsti rifiutati', async () => {
    const st = (await get('/api/stato')).body;
    assert.deepStrictEqual(st.assegnabili.ideatore, ['manuale', 'claude', 'codex']);
    assert.ok(st.programmi.codex, 'codex deve comparire anche se non assegnato');
    const prima = JSON.parse(fs.readFileSync(path.join(ROOT, 'modelli.json'), 'utf8'));
    const a = await post('/api/ruoli', { ruolo: 'ideatore', programma: 'codex' });
    assert.strictEqual(a.code, 200);
    assert.strictEqual(a.body.temporaneo, false);
    assert.deepStrictEqual(JSON.parse(fs.readFileSync(path.join(ROOT, 'modelli.json'), 'utf8')), prima, 'modelli.json (su GitHub) non cambia');
    let loc = JSON.parse(fs.readFileSync(path.join(ROOT, 'modelli.locale.json'), 'utf8'));
    assert.strictEqual(loc.ruoli.ideatore.programma, 'codex');
    assert.strictEqual((await get('/api/stato')).body.ruoli.ideatore.programma, 'codex');
    assert.ok((await get('/api/stato')).body.ruoli.ideatore.definitivo, 'i campi di modelli.json restano');
    assert.strictEqual((await post('/api/ruoli', { ruolo: 'revisore', programma: 'claude' })).code, 422);
    assert.strictEqual((await post('/api/ruoli', { ruolo: 'ideatore', programma: 'bash' })).code, 422);
    assert.strictEqual((await post('/api/ruoli', { ruolo: '__proto__', programma: 'claude' })).code, 422);
    assert.strictEqual((await post('/api/ruoli', { ruolo: 'ideatore', programma: 'claude' }, { 'X-Niko': '' })).code, 403);
    const b = await post('/api/ruoli', { ruolo: 'ideatore', programma: 'claude' });
    assert.strictEqual(b.body.temporaneo, true);
    loc = JSON.parse(fs.readFileSync(path.join(ROOT, 'modelli.locale.json'), 'utf8'));
    assert.strictEqual(loc.ruoli.ideatore.programma, 'claude');
  });

  await test('Solo prompt: Ideatore "a mano", nessun programma avviato, la risposta incollata viene salvata', async () => {
    assert.strictEqual((await post('/api/ruoli', { ruolo: 'ideatore', programma: 'manuale' })).body.temporaneo, false);
    const id = (await post('/api/messaggi', { testo: 'proponi tre idee per un reel di mezzeuro sul budget mensile' })).body.task;
    const t = await until(id, ['attesa_risposta']);
    assert.strictEqual(t.agente.programma, 'manuale');
    assert.ok(fs.existsSync(path.join(ROOT, 'projects/mezzeuro/work', id, 'v01', 'prompt.md')));
    assert.match((await get(`/api/lavori/${id}/piano-b`)).body.prompt, /budget mensile/);
    assert.ok(!fs.existsSync(path.join(ROOT, 'projects/mezzeuro/work', id, 'v01', 'risposta-agente.txt')), 'nessun agente deve aver risposto');
    const idea = n => ({ titolo: `M${n}`, hook: `H${n}`, sviluppo: `S${n}`, direzione_visiva: `V${n}` });
    const ok = await post(`/api/lavori/${id}/manuale`, { testo: JSON.stringify({ idee: [idea(1), idea(2), idea(3)] }) });
    assert.strictEqual(ok.body.task.stato, 'attesa_fede');
    const md = await post(`/api/lavori/${id}/modifica`, { testo: 'Più brevi' });
    assert.strictEqual(md.body.task.versione, 2);
    const t2 = await until(id, ['attesa_risposta']);
    assert.match((await get(`/api/lavori/${id}/piano-b`)).body.prompt, /Più brevi/);
    assert.strictEqual(t2.versione, 2);
    await post('/api/ruoli', { ruolo: 'ideatore', programma: 'claude' });
  });

  // 3. Riavvio: incarico e risultato restano. Poi un incarico interrotto a metà.
  await stop();
  await start('buono', 3000);
  await test('3. Riavvio del servizio: incarico e risultato conservati', async () => {
    const t = (await get('/api/lavori')).body.find(x => x.id === firstId);
    assert.ok(t && t.stato === 'attesa_fede' && t.risultato.idee.length === 3);
  });
  const slow = (await post('/api/messaggi', { testo: 'proponi tre idee per un reel di mezzeuro sul TFR' })).body.task;
  await until(slow, ['in_corso']);
  await kill(); // spengo di colpo mentre l'agente lavora
  await start('buono');
  await test('3b. Interruzione: lo stesso incarico torna "da verificare", senza duplicati', async () => {
    const all = (await get('/api/lavori')).body;
    const t = all.find(x => x.id === slow);
    assert.strictEqual(t.stato, 'da_verificare');
    assert.strictEqual(all.filter(x => x.impronta === t.impronta).length, 1);
    const r = await post(`/api/lavori/${slow}/riprova`, {});
    assert.strictEqual(r.body.task.stato, 'in_coda');
    await until(slow, ['attesa_fede']);
  });
  await stop();

  await start('vuoto');
  await test('4a. Risposta vuota: errore comprensibile', async () => {
    const id = (await post('/api/messaggi', { testo: 'proponi idee mezzeuro sul bollo' })).body.task;
    const t = await until(id, ['fallito']);
    assert.strictEqual(t.errore.tipo, 'risposta_non_valida');
    assert.match(t.errore.messaggio, /vuota/);
  });
  await stop();
  await start('rotto');
  await test('4b. Risposta fuori formato: errore comprensibile', async () => {
    const id = (await post('/api/messaggi', { testo: 'proponi idee mezzeuro sul mutuo' })).body.task;
    const t = await until(id, ['fallito']);
    assert.match(t.errore.messaggio, /formato JSON/);
  });
  await stop();

  for (const [mode, tipo] of [['assente', 'programma_assente'], ['accesso', 'autenticazione'], ['limite', 'limite']]) {
    await start(mode);
    await test(`6. Agente non disponibile (${tipo}): piano B utilizzabile`, async () => {
      const id = (await post('/api/messaggi', { testo: `proponi tre idee mezzeuro caso ${mode}` })).body.task;
      const t = await until(id, ['fallito']);
      assert.strictEqual(t.errore.tipo, tipo);
      const pb = await get(`/api/lavori/${id}/piano-b`);
      assert.match(pb.body.prompt, /Richiesta di Fede/);
      assert.match(pb.body.prompt, /fondo|caso/);
      const bad = await post(`/api/lavori/${id}/manuale`, { testo: 'non è json' });
      assert.strictEqual(bad.code, 422);
      const idea = n => ({ titolo: `T${n}`, hook: `Hook ${n}`, sviluppo: `Sviluppo ${n}`, direzione_visiva: `Visiva ${n}` });
      const ok = await post(`/api/lavori/${id}/manuale`, { testo: '```json\n' + JSON.stringify({ idee: [idea(1), idea(2), idea(3)] }) + '\n```' });
      assert.strictEqual(ok.body.task.stato, 'attesa_fede');
      assert.strictEqual(ok.body.task.risultato.origine, 'manuale');
      // nessun nuovo tentativo automatico: il log ha un solo "avviato"
      const log = fs.readFileSync(path.join(ROOT, 'tasks', id + '.log'), 'utf8');
      assert.strictEqual((log.match(/"avviato"/g) || []).length, 1);
    });
    await stop();
  }

  await start('buono');
  await test('Libreria: importazione dal browser senza duplicati e senza perdere le note', async () => {
    const r = await post('/api/libreria/importa', { voci: [{ shelf: 'gusto', text: 'https://example.com/reel' }, { shelf: 'stile', text: 'Tono da fratello maggiore. Niente promesse di guadagno.' }, { shelf: 'boh', text: 'x' }] });
    assert.strictEqual(r.body.aggiunte, 1);
    assert.strictEqual(r.body.voci.length, 2);
  });
  await stop();

  for (const [s, n] of results) console.log(s, n);
  const failed = results.filter(r => r[0] === 'FAIL').length;
  console.log(failed ? `\n${failed} prove fallite` : `\nTutte le ${results.length} prove superate`);
  fs.rmSync(ROOT, { recursive: true, force: true });
  process.exit(failed ? 1 : 0);
})().catch(async e => { console.error(e); try { srv.kill('SIGKILL'); } catch {} process.exit(1); });
