'use strict';
// Servizio locale di Niko: serve l'app, riceve i messaggi, registra gli incarichi e fa girare il worker.
// Ascolta solo su 127.0.0.1. Avvio: node server/server.js   Stop: Ctrl+C
const http = require('http');
const fs = require('fs');
const path = require('path');
const L = require('./lib');
const core = require('./core');

const PORT = Number(process.env.BELUGA_PORT) || 4170;
const HOST = '127.0.0.1';
const HOSTS = [`127.0.0.1:${PORT}`, `localhost:${PORT}`];
const TYPES = { '.html': 'text/html; charset=utf-8', '.css': 'text/css; charset=utf-8', '.js': 'text/javascript; charset=utf-8', '.webp': 'image/webp', '.woff2': 'font/woff2', '.png': 'image/png', '.svg': 'image/svg+xml' };

function send(res, code, body, type = 'application/json; charset=utf-8') {
  res.writeHead(code, {
    'Content-Type': type,
    'Cache-Control': 'no-store',
    'X-Content-Type-Options': 'nosniff',
    'Referrer-Policy': 'no-referrer',
    'Content-Security-Policy': "default-src 'self'; img-src 'self' data:; style-src 'self' 'unsafe-inline'; frame-ancestors 'none'",
  });
  res.end(type.startsWith('application/json') ? JSON.stringify(body) : body);
}

// Solo i file dell'app, niente lettura libera del disco.
function serveStatic(req, res) {
  let p = decodeURIComponent(new URL(req.url, 'http://x').pathname);
  if (p === '/') p = '/index.html';
  const f = path.normalize(path.join(L.APP, p));
  if (!f.startsWith(L.APP + path.sep) || !TYPES[path.extname(f)] || !fs.existsSync(f) || !fs.statSync(f).isFile()) return send(res, 404, 'Non trovato', 'text/plain; charset=utf-8');
  send(res, 200, fs.readFileSync(f), TYPES[path.extname(f)]);
}

function readBody(req) {
  return new Promise((resolve, reject) => {
    let data = '';
    req.on('data', c => { data += c; if (data.length > 300000) { reject(new Error('troppo grande')); req.destroy(); } });
    req.on('end', () => { try { resolve(data ? JSON.parse(data) : {}); } catch { reject(new Error('JSON non valido')); } });
  });
}

/* ---------- libreria del progetto ---------- */

const SHELVES = ['gusto', 'evita', 'stile', 'pezzi'];
const libFile = p => path.join(L.PROJECTS, p, 'libreria.json');
const libRead = p => L.readJSON(libFile(p), { voci: [] });
function libAdd(p, voci, origine) {
  const lib = libRead(p);
  const seen = new Set(lib.voci.map(v => `${v.scaffale}|${v.testo}`));
  let n = 0;
  for (const v of voci) {
    const scaffale = SHELVES.includes(v.scaffale || v.shelf) ? (v.scaffale || v.shelf) : null;
    const testo = String(v.testo || v.text || '').trim().slice(0, 500);
    if (!scaffale || !testo || seen.has(`${scaffale}|${testo}`)) continue;
    lib.voci.push({ scaffale, testo, origine, aggiunto: L.now() });
    seen.add(`${scaffale}|${testo}`); n++;
  }
  if (n) L.writeJSON(libFile(p), lib);
  return { aggiunte: n, voci: lib.voci };
}

/* ---------- API ---------- */

async function api(req, res, url) {
  const p = url.pathname;
  const isWrite = req.method === 'POST';
  if (isWrite) {
    // Protezione da richieste di altri siti: header personalizzato (forza il preflight CORS, che non
    // concediamo), JSON obbligatorio e Origin, se presente, uguale al nostro.
    const origin = req.headers.origin;
    if (req.headers['x-niko'] !== '1' || !String(req.headers['content-type'] || '').startsWith('application/json') || (origin && !HOSTS.some(h => origin === `http://${h}`))) {
      return send(res, 403, { errore: 'Richiesta non permessa.' });
    }
  } else if (req.method !== 'GET') return send(res, 405, { errore: 'Metodo non permesso.' });

  const body = isWrite ? await readBody(req) : {};
  const project = url.searchParams.get('progetto') || body.progetto || 'mezzeuro';
  let m;

  if (p === '/api/stato' && !isWrite) return send(res, 200, await core.status());
  if (p === '/api/lavori' && !isWrite) return send(res, 200, core.list());
  if (p === '/api/chat' && !isWrite) return send(res, 200, core.chat());
  if (p === '/api/messaggi' && isWrite) { const r = core.receive(body); return send(res, r.errore ? 422 : 200, r); }
  if ((m = p.match(/^\/api\/lavori\/(t-[a-z0-9-]+)\/piano-b$/)) && !isWrite) {
    const t = core.get(m[1]);
    return t ? send(res, 200, { prompt: core.planBPrompt(t) }) : send(res, 404, { errore: 'Incarico non trovato.' });
  }
  if ((m = p.match(/^\/api\/lavori\/(t-[a-z0-9-]+)\/(manuale|riprova|approva|modifica|annulla)$/)) && isWrite) {
    const r = core.act(m[1], m[2], body);
    return send(res, r.errore ? r.codice || 400 : 200, r);
  }
  if (p.startsWith('/api/libreria')) {
    if (!core.projects().includes(project)) return send(res, 404, { errore: 'Progetto sconosciuto.' });
    if (p === '/api/libreria' && !isWrite) return send(res, 200, libRead(project));
    if (p === '/api/libreria' && isWrite) return send(res, 200, libAdd(project, [body], 'app'));
    if (p === '/api/libreria/importa' && isWrite) return send(res, 200, libAdd(project, Array.isArray(body.voci) ? body.voci.slice(0, 500) : [], 'importata dal browser'));
    if (p === '/api/libreria/togli' && isWrite) {
      const lib = libRead(project), i = Number(body.indice);
      if (!Number.isInteger(i) || !lib.voci[i]) return send(res, 422, { errore: 'Voce non trovata.' });
      lib.voci.splice(i, 1); L.writeJSON(libFile(project), lib);
      return send(res, 200, lib);
    }
  }
  return send(res, 404, { errore: 'Non trovato.' });
}

const server = http.createServer(async (req, res) => {
  // Solo il nostro indirizzo: blocca anche i trucchi di DNS rebinding.
  if (!HOSTS.includes(req.headers.host)) return send(res, 421, 'Host non permesso', 'text/plain; charset=utf-8');
  const url = new URL(req.url, `http://${req.headers.host}`);
  try {
    if (url.pathname.startsWith('/api/')) return await api(req, res, url);
    if (req.method !== 'GET') return send(res, 405, 'Metodo non permesso', 'text/plain; charset=utf-8');
    return serveStatic(req, res);
  } catch (e) {
    return send(res, 400, { errore: String(e.message || e) });
  }
});

server.on('error', e => {
  console.error(e.code === 'EADDRINUSE' ? `La porta ${PORT} è già usata: forse Niko è già acceso.` : e);
  process.exit(1);
});
server.listen(PORT, HOST, () => {
  const w = core.startWorker();
  console.log(`Niko è acceso: http://${HOST}:${PORT}`);
  console.log(w ? 'Worker attivo: un incarico alla volta.' : 'Un altro worker è già attivo: questo servizio non esegue incarichi.');
  if (process.env.BELUGA_AGENTE_FINTO) console.log(`ATTENZIONE: modalità test con agente finto (${process.env.BELUGA_AGENTE_FINTO}).`);
});

function shutdown() {
  core.stopWorker();
  server.close(() => process.exit(0));
  setTimeout(() => process.exit(0), 1500).unref();
}
process.on('SIGINT', shutdown);
process.on('SIGTERM', shutdown);

module.exports = server;
