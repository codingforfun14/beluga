'use strict';
// Modalità reale: l'app parla con il servizio locale di Niko. Niente dati finti, niente percentuali inventate.
// Aperta con il doppio clic sul file (demo) questo script non fa niente.
(function () {
  if (!REAL) return;
  document.body.classList.add('real');

  /* ---------- chiamate al servizio ---------- */

  async function call(method, url, body) {
    const r = await fetch(url, { method, headers: body ? { 'Content-Type': 'application/json', 'X-Niko': '1' } : {}, body: body ? JSON.stringify(body) : undefined });
    let j = null;
    try { j = await r.json(); } catch {}
    if (!r.ok) throw new Error((j && j.errore) || `Errore ${r.status}`);
    return j;
  }
  const api = { get: u => call('GET', u), post: (u, b) => call('POST', u, b || {}) };

  /* ---------- dal formato del servizio a quello dell'app ---------- */

  STEPS.idee = [['Idee', 'ideatore'], ['Controllo', 'ideatore'], ['Il tuo ok', 'you']];
  const MAP = { in_coda: 'queue', in_corso: 'work', attesa_fede: 'you', completato: 'done', fallito: 'stuck', da_verificare: 'stuck', annullato: 'done' };
  const PROG = { claude: 'Claude', codex: 'ChatGPT (Codex)' };
  let status = null;
  const prompts = {};

  const hhmm = iso => new Date(iso).toLocaleTimeString('it-IT', { hour: '2-digit', minute: '2-digit' });
  const ago = iso => { const s = Math.max(0, Math.round((Date.now() - Date.parse(iso)) / 1000)); return s < 60 ? `${s} secondi` : `${Math.round(s / 60)} min`; };
  function agentLabel(a) {
    if (status && status.modalita === 'test') return 'agente finto di test';
    return a && a.programma ? `${PROG[a.programma] || a.programma}${a.temporaneo ? ', temporaneo' : ''}` : 'nessun programma';
  }

  function toUI(s) {
    const state = MAP[s.stato] || 'queue';
    const t = { id: s.id, kind: 'idee', project: s.progetto, state, version: s.versione, title: s.titolo, real: s };
    t.stateLabel = { fallito: 'Fermo', da_verificare: 'Da verificare', annullato: 'Annullato', completato: 'Approvato' }[s.stato];
    t.step = { queue: 0, work: 0, you: 2, done: 3, stuck: s.errore && s.errore.tipo === 'risposta_non_valida' ? 1 : 0 }[state];
    const who = `Ideatore: ${agentLabel(s.agente)}`;
    t.status = {
      in_coda: `In coda. ${who}.`,
      in_corso: `${who}. Ci lavora da ${ago(s.iniziato || s.aggiornato)}.`,
      attesa_fede: 'Le 3 idee sono pronte e hanno passato il controllo. Scegline una.',
      completato: s.scelta ? `Hai scelto "${s.scelta.titolo}".` : 'Approvato.',
      fallito: s.errore ? (s.errore.tipo === 'altro' ? `Errore: ${s.errore.messaggio}` : s.errore.messaggio) : 'Fermo.',
      da_verificare: s.errore ? s.errore.messaggio : 'Da verificare.',
      annullato: 'Annullato da te.',
    }[s.stato];
    if (s.risultato) t.ideas = s.risultato.idee.map(i => ({ name: i.titolo, line: i.hook, more: i.sviluppo, visual: i.direzione_visiva }));
    return t;
  }

  /* ---------- schede ---------- */

  function planB(t) {
    const p = prompts[t.id];
    if (p == null) loadPrompt(t.id);
    return `<div class="planb">
      <p class="planbtitle">Piano B: fallo a mano in 3 passi</p>
      <ol>
        <li><span>Copia le istruzioni</span><button class="soft small" data-copy="${t.id}">${icon('i-copy')}Copia</button></li>
        <li><span>Incollale nella chat di Claude o di ChatGPT e invia</span></li>
        <li><span>Incolla qui sotto la risposta: la controllo come quella dell'agente</span></li>
      </ol>
      <details><summary>Vedi le istruzioni</summary><pre data-prompt="${t.id}">${esc(p == null ? 'Carico…' : p)}</pre></details>
      <label class="sr" for="answer-${t.id}">Risposta incollata</label>
      <textarea id="answer-${t.id}" rows="3" placeholder="Incolla qui la risposta"></textarea>
      <div class="buttons"><button class="primary" data-resume="${t.id}">Controlla e salva</button><button class="soft" data-retry="${t.id}">Riprova con l'agente</button><button class="soft" data-cancel="${t.id}">Annulla</button></div>
    </div>`;
  }

  const oldBody = body;
  body = function (t) {
    if (!t.real) return oldBody(t);
    const s = t.real;
    const saved = s.risultato ? `<p class="detail">Salvato in ${esc(s.risultato.markdown)}${s.risultato.origine === 'manuale' ? ' · risposta incollata a mano' : ''}</p>` : '';
    const temp = s.agente && s.agente.temporaneo ? '<p class="detail">Claude fa l\'Ideatore solo per provare il collegamento. Non è ancora il flusso definitivo a due modelli.</p>' : '';
    if (s.stato === 'attesa_fede') {
      return `<div class="ideas">${t.ideas.map((i, n) => `<label class="idea">
          <input type="radio" name="pick-${t.id}" value="${n}" ${n === 0 ? 'checked' : ''}>
          <span><strong>${esc(i.name)}</strong>${esc(i.line)}<small class="more">${esc(i.more)}</small><small class="more"><b>Visivo:</b> ${esc(i.visual)}</small></span>
        </label>`).join('')}</div>${saved}
        <div class="buttons"><button class="primary" data-approve="${t.id}">${icon('i-check')}Approva l'idea scelta</button><button class="soft" data-changes="${t.id}">Chiedi modifiche</button></div>`;
    }
    if (s.stato === 'completato') return `${saved}<div class="buttons"><button class="soft" data-changes="${t.id}">Chiedi una nuova versione</button></div>`;
    if (s.stato === 'in_corso') return `<div class="bar indet" aria-label="In corso"><i></i></div>${temp}`;
    if (s.stato === 'in_coda') return `${temp}<div class="buttons"><button class="soft" data-cancel="${t.id}">Annulla</button></div>`;
    if (s.stato === 'da_verificare') return `<div class="buttons"><button class="primary" data-retry="${t.id}">Rilancia</button><button class="soft" data-cancel="${t.id}">Annulla</button></div>`;
    if (s.stato === 'fallito') return planB(t);
    return '';
  };

  async function loadPrompt(id) {
    if (prompts[id] != null || loadPrompt[id]) return;
    loadPrompt[id] = true;
    try { prompts[id] = (await api.get(`/api/lavori/${id}/piano-b`)).prompt; } catch { prompts[id] = 'Non riesco a caricare le istruzioni.'; }
    $$(`[data-prompt="${id}"]`).forEach(p => { p.textContent = prompts[id]; });
  }

  /* ---------- aggiornamento leggero ---------- */

  let sig = '', timer = null, offline = false, heard = -1;
  // Rifare le schede non deve cancellare quello che Fede sta scrivendo o la scelta fatta.
  function keep(fn) {
    const texts = $$('textarea[id^="answer-"]').map(t => [t.id, t.value]);
    const picks = $$('.idea input:checked').map(i => [i.name, i.value]);
    fn();
    texts.forEach(([id, v]) => $$(`#${CSS.escape(id)}`).forEach(t => { t.value = v; }));
    picks.forEach(([n, v]) => $$(`input[name="${CSS.escape(n)}"][value="${CSS.escape(v)}"]`).forEach(i => { i.checked = true; }));
  }

  async function refresh(force) {
    clearTimeout(timer);
    try {
      const [tasks, chat] = await Promise.all([api.get('/api/lavori'), api.get('/api/chat')]);
      if (offline) { offline = false; await loadStatus(); }
      const busy = tasks.some(t => ['in_coda', 'in_corso'].includes(t.stato));
      const next = JSON.stringify([tasks, chat.length]);
      if (force || next !== sig || busy) {
        sig = next;
        db.tasks.splice(0, db.tasks.length, ...tasks.map(toUI));
        db.messages.splice(0, db.messages.length, ...chat.map(m => ({ from: m.da === 'fede' ? 'fede' : 'niko', time: hhmm(m.ora), text: m.testo, task: m.task })));
        keep(renderAll);
        // Una risposta nuova di Niko mentre sei su un'altra pagina: compare sopra la barra.
        const last = chat.length - 1;
        if (heard >= 0 && last > heard && chat[last].da === 'niko') peek(chat[last].testo);
        heard = last;
      }
      timer = setTimeout(refresh, busy ? 1500 : 5000);
    } catch {
      if (!offline) {
        offline = true;
        db.links.splice(0, db.links.length, { name: 'Servizio locale', ok: false, note: 'Non risponde. Riaccendi Niko dal Terminale.' });
        renderHome();
        toast('Il servizio di Niko non risponde');
      }
      timer = setTimeout(refresh, 5000);
    }
  }

  async function loadStatus() {
    try { status = await api.get('/api/stato'); } catch { return; }
    const r = status.ruoli || {};
    const uses = k => (r[k] && r[k].programma ? `${PROG[r[k].programma] || r[k].programma}${r[k].temporaneo ? ', temporaneo' : ''}` : 'Non attivo in questa fase');
    DEPTS.ideatore.uses = status.modalita === 'test' ? 'Agente finto di test' : uses('ideatore');
    DEPTS.revisore.uses = uses('revisore');
    DEPTS.produzione.uses = uses('produzione');
    const links = [{ name: 'Servizio locale', ok: true, note: status.worker ? 'Acceso, worker attivo' : 'Acceso, ma il worker è occupato da un altro servizio' }];
    for (const [p, i] of Object.entries(status.programmi || {})) {
      const name = status.modalita === 'test' ? 'Agente finto' : PROG[p] || p;
      const note = status.modalita === 'test' ? 'Modalità test: i risultati non sono reali'
        : !i.installato ? 'Non trovato sul Mac'
          : i.ultimo_successo ? `Ha risposto davvero alle ${hhmm(i.ultimo_successo)} (${i.versione})`
            : `Installato (${i.versione}). Accesso non ancora verificato`;
      links.push({ name, ok: !!i.ultimo_successo && status.modalita !== 'test', note });
    }
    db.links.splice(0, db.links.length, ...links);
    $('.demo').textContent = status.modalita === 'test' ? 'Modalità test: agente finto, i risultati non sono reali.' : 'Modalità reale: collegata al servizio sul tuo Mac.';
    renderHome();
  }

  /* ---------- chi lavora ---------- */

  // In Centrale Fede sceglie quale programma fa partire ogni ruolo. Si possono scegliere solo programmi trovati sul Mac.
  const baseHome = renderHome;
  renderHome = function () {
    baseHome();
    if (!status) return;
    const r = status.ruoli || {}, ass = status.assegnabili || {}, pr = status.programmi || {};
    const row = (k, name) => {
      const cur = r[k] && r[k].programma;
      if (!ass[k]) return `<li><span class="led ${cur ? 'ok' : 'warn'}"></span><span><strong>${name}</strong> ${cur ? esc(PROG[cur] || cur) : 'Non attivo in questa fase'}</span></li>`;
      const opts = ass[k].map(p => {
        const i = pr[p] || {}, ok = status.modalita === 'test' || i.installato;
        return `<option value="${p}"${p === cur ? ' selected' : ''}${ok ? '' : ' disabled'}>${esc(PROG[p] || p)}${ok ? '' : ' (non installato)'}</option>`;
      }).join('');
      const note = r[k].temporaneo ? 'temporaneo' : r[k].definitivo === cur ? 'definitivo' : '';
      return `<li class="assign"><span class="led ok"></span><label><strong>${name}</strong><select data-assign="${k}" aria-label="Chi fa ${name}">${opts}</select>${note ? `<small>${note}</small>` : ''}</label></li>`;
    };
    const tile = document.createElement('article');
    tile.className = 'tile who';
    tile.innerHTML = `<h2>Chi lavora</h2><ul>${row('ideatore', 'Ideatore')}${row('revisore', 'Revisore')}${row('produzione', 'Produzione')}</ul>`;
    $('#glance').appendChild(tile);
  };

  document.addEventListener('change', async e => {
    const s = e.target.closest('select[data-assign]');
    if (!s) return;
    const k = s.dataset.assign, before = status.ruoli[k].programma;
    s.disabled = true;
    try {
      await api.post('/api/ruoli', { ruolo: k, programma: s.value });
      toast(`Da ora l'${k} è ${PROG[s.value] || s.value}`);
    } catch (err) { toast(err.message); s.value = before; }
    await loadStatus();
  });

  /* ---------- azioni ---------- */

  send = async function (text) {
    text = text.trim();
    if (!text) { $('#prompt').focus(); return; }
    $('#prompt').value = '';
    grow();
    try {
      let r;
      if (revising) { const id = revising; setRevising(null); r = await api.post(`/api/lavori/${id}/modifica`, { testo: text }); peek('Ok, preparo la nuova versione.'); }
      else { r = await api.post('/api/messaggi', { testo: text, progetto: $('#project').value }); if (r.risposta) peek(r.risposta); }
    } catch (e) { toast(e.message); $('#prompt').value = text; grow(); }
    refresh(true);
  };

  approve = function (t, b) {
    if (!t.real || !t.ideas) return;
    const pick = b.closest('.card').querySelector('input:checked');
    const n = pick ? Number(pick.value) : 0;
    ask(`Idee · ${vnum(t.version)}`, `Approvi "${t.ideas[n].name}"?`, 'Segno questa idea come scelta per questa versione. Lo script arriva in una fase successiva.', async () => {
      try { await api.post(`/api/lavori/${t.id}/approva`, { scelta: n }); toast('Approvato'); } catch (e) { toast(e.message); }
      refresh(true);
    });
  };

  // I pulsanti che in demo cambiano solo dati finti, qui parlano con il servizio.
  document.addEventListener('click', async e => {
    const b = e.target.closest('button');
    if (!b) return;
    const d = b.dataset;
    if (!(d.resume || d.copy || d.retry || d.cancel || d.unlib != null || d.importlib)) return;
    e.stopPropagation();
    try {
      if (d.copy) {
        if (prompts[d.copy] == null) await loadPrompt(d.copy);
        copy(prompts[d.copy], b, 'Istruzioni copiate');
      }
      if (d.resume) {
        const box = b.closest('.planb').querySelector('textarea');
        if (!box.value.trim()) { toast('Incolla prima la risposta'); box.focus(); return; }
        await api.post(`/api/lavori/${d.resume}/manuale`, { testo: box.value });
        box.value = '';
        toast('Risposta controllata e salvata');
      }
      if (d.retry) { await api.post(`/api/lavori/${d.retry}/riprova`); toast('Rilanciato'); }
      if (d.cancel) { await api.post(`/api/lavori/${d.cancel}/annulla`); toast('Annullato'); }
      if (d.unlib != null) { await api.post('/api/libreria/togli', { indice: Number(d.unlib) }); await loadLibrary(); }
      if (d.importlib) {
        const r = await api.post('/api/libreria/importa', { voci: localLibrary() });
        toast(r.aggiunte ? `Importate ${r.aggiunte} note nel progetto` : 'Erano già tutte nel progetto');
        await loadLibrary();
      }
    } catch (err) { toast(err.message); }
    refresh(true);
  }, true);

  /* ---------- libreria del progetto ---------- */

  function localLibrary() {
    try { const v = JSON.parse(localStorage.getItem('niko-libreria-v1')); return Array.isArray(v) ? v : []; } catch { return []; }
  }

  async function loadLibrary() {
    try {
      const lib = await api.get('/api/libreria?progetto=mezzeuro');
      db.library.splice(0, db.library.length, ...lib.voci.map(v => ({ shelf: v.scaffale, text: v.testo })));
    } catch { return; }
    renderLibrary();
    renderHome();
    // Le note salvate prima solo nel browser: si portano nel progetto solo se Fede lo chiede.
    const have = new Set(db.library.map(v => `${v.shelf}|${v.text}`));
    const missing = localLibrary().filter(v => v && !have.has(`${v.shelf}|${v.text}`));
    let box = $('#importbox');
    if (!box) { box = document.createElement('div'); box.id = 'importbox'; box.className = 'importbox'; $('#shelves').before(box); }
    box.hidden = !missing.length;
    box.innerHTML = missing.length ? `<span>In questo browser ci sono ${missing.length} note della Libreria che il progetto non ha ancora.</span><button class="soft small" data-importlib="1">Importale nel progetto</button>` : '';
  }

  document.addEventListener('submit', async e => {
    if (e.target.id !== 'addform') return;
    e.preventDefault();
    e.stopPropagation();
    const text = $('#addtext').value.trim();
    if (!text) { $('#addtext').focus(); return; }
    try {
      await api.post('/api/libreria', { progetto: 'mezzeuro', scaffale: $('#addshelf').value, testo: text });
      $('#addtext').value = '';
      toast('Aggiunto alla libreria del progetto');
    } catch (err) { toast(err.message); }
    loadLibrary();
  }, true);

  /* ---------- partenza ---------- */

  const sel = $('#project');
  sel.insertAdjacentHTML('afterbegin', '<option value="">Dal testo</option>');
  sel.value = '';
  $('#tries [data-try="idee"]').dataset.text = 'Niko, proponi tre idee per un reel di mezzeuro sul fondo emergenze';
  kind = 'idee';
  $$('[data-kind]').forEach(x => x.setAttribute('aria-pressed', String(x.dataset.kind === 'idee')));
  renderAll();
  loadStatus().then(() => refresh(true));
  loadLibrary();
  setInterval(loadStatus, 30000);
})();
