'use strict';
// Il lavoro "idee": costruisce il prompt con il contesto minimo e controlla la risposta.
const fs = require('fs');
const path = require('path');
const { ROLES, PROJECTS, readJSON } = require('./lib');

const FIELDS = ['titolo', 'hook', 'sviluppo', 'momento', 'direzione_visiva'];
const BRIEF = ['messaggio', 'insight', 'prova'];
const read = f => { try { return fs.readFileSync(f, 'utf8').trim(); } catch { return ''; } };

// Solo ciò che serve: skill del ruolo, contesto del progetto, libreria, file dell'incarico.
function buildPrompt(task) {
  const skill = read(path.join(ROLES, task.ruolo, 'SKILL.md'));
  const ctx = read(path.join(PROJECTS, task.progetto, 'CONTESTO.md'));
  const lib = readJSON(path.join(PROJECTS, task.progetto, 'libreria.json'), { voci: [] }).voci || [];
  const shelves = { gusto: 'Mi piace', evita: 'Da evitare', stile: 'Stile del progetto', pezzi: 'Pezzi pronti' };
  const libText = lib.length ? lib.map(v => `- [${shelves[v.scaffale] || v.scaffale}] ${v.testo}`).join('\n') : '(vuota)';
  const inputs = (task.input || []).map(f => `--- ${f} ---\n${read(path.join(PROJECTS, task.progetto, f))}`).join('\n\n');
  const prev = task.versione > 1 && task.revisioni && task.revisioni.length
    ? `\n# Modifiche chieste da Fede alla versione precedente\n${task.revisioni.map(r => `- v${String(r.da).padStart(2, '0')}: ${r.testo}`).join('\n')}\n` : '';
  return `${skill}

# Contesto del progetto ${task.progetto}
${ctx || '(nessun CONTESTO.md)'}

# Libreria di Fede
${libText}
${inputs ? `\n# File allegati all'incarico\n${inputs}\n` : ''}${prev}
# Richiesta di Fede
${task.richiesta}

# Formato della risposta (obbligatorio)
Rispondi SOLO con un oggetto JSON valido, senza testo prima o dopo e senza blocchi di codice:
{"brief":{"messaggio":"...","insight":"...","prova":"..."},
 "idee":[{"titolo":"...","hook":"...","sviluppo":"...","momento":"...","direzione_visiva":"...","scaletta":["0-2 s: ...","2-6 s: ..."]}]}
Esattamente 3 idee. Tutti i campi pieni, in italiano. La scaletta ha da 3 a 10 beat, ognuno con i secondi.`;
}

// Trova il JSON anche se il modello aggiunge un blocco ```json o due parole attorno.
function extractJSON(text) {
  if (typeof text !== 'string') return null;
  const t = text.trim().replace(/^```(?:json)?\s*/i, '').replace(/```\s*$/, '');
  try { return JSON.parse(t); } catch {}
  const a = t.indexOf('{'), b = t.lastIndexOf('}');
  if (a >= 0 && b > a) { try { return JSON.parse(t.slice(a, b + 1)); } catch {} }
  return null;
}

// Restituisce { ok, idee } oppure { ok:false, errore } con un motivo leggibile.
function validate(text) {
  if (!text || !String(text).trim()) return { ok: false, errore: 'La risposta è vuota.' };
  const data = extractJSON(String(text));
  if (!data) return { ok: false, errore: 'La risposta non è nel formato JSON richiesto.' };
  const list = Array.isArray(data) ? data : data.idee;
  if (!Array.isArray(list)) return { ok: false, errore: 'Nella risposta manca la lista "idee".' };
  if (list.length !== 3) return { ok: false, errore: `Servono 3 idee, ne sono arrivate ${list.length}.` };
  const b = Array.isArray(data) ? null : data.brief;
  for (const f of BRIEF) {
    if (!b || typeof b[f] !== 'string' || !b[f].trim()) return { ok: false, errore: `Nel brief manca il campo "${f}" o è vuoto.` };
  }
  for (const [i, idea] of list.entries()) {
    for (const f of FIELDS) {
      const v = idea && idea[f];
      if (typeof v !== 'string' || !v.trim()) return { ok: false, errore: `Nell'idea ${i + 1} manca il campo "${f}" o è vuoto.` };
    }
    const sc = idea.scaletta;
    if (!Array.isArray(sc) || sc.length < 3 || sc.some(x => typeof x !== 'string' || !x.trim())) return { ok: false, errore: `Nell'idea ${i + 1} la scaletta deve avere almeno 3 beat scritti.` };
  }
  return {
    ok: true,
    brief: Object.fromEntries(BRIEF.map(f => [f, b[f].trim()])),
    idee: list.map(i => ({ ...Object.fromEntries(FIELDS.map(f => [f, i[f].trim()])), scaletta: i.scaletta.slice(0, 10).map(x => x.trim()) })),
  };
}

function toMarkdown(task, idee, origine, brief) {
  return `# ${task.titolo} · versione ${String(task.versione).padStart(2, '0')}

Richiesta: ${task.richiesta}
Fatto da: ${origine}
${brief ? `
## Brief

- **Messaggio:** ${brief.messaggio}
- **Insight:** ${brief.insight}
- **Perché crederci:** ${brief.prova}
` : ''}
${idee.map((i, n) => `## ${n + 1}. ${i.titolo}

**Hook:** ${i.hook}

${i.sviluppo}

**Il momento da raccontare:** ${i.momento}

**Direzione visiva:** ${i.direzione_visiva}

**Scaletta**
${(i.scaletta || []).map(x => `- ${x}`).join('\n')}
`).join('\n')}`;
}

module.exports = { buildPrompt, validate, toMarkdown, FIELDS };
