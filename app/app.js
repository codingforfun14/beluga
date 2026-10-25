'use strict';
const $ = s => document.querySelector(s);
const $$ = s => [...document.querySelectorAll(s)];
const esc = s => String(s).replace(/[&<>"']/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' })[c]);
const icon = n => `<svg aria-hidden="true"><use href="#${n}"/></svg>`;
const now = () => new Date().toLocaleTimeString('it-IT', { hour: '2-digit', minute: '2-digit' });
const calm = matchMedia('(prefers-reduced-motion: reduce)').matches;
const vnum = n => 'versione ' + String(n).padStart(2, '0');
const vtag = n => 'v' + String(n).padStart(2, '0');

// Modalità reale quando l'app è aperta dal servizio locale (http://127.0.0.1:4170).
// Con il doppio clic sul file resta la demo con i dati di esempio: le due cose non si mescolano.
const REAL = /^https?:$/.test(location.protocol);
const db = REAL ? { tasks: [], deliveries: [], messages: [], links: [], library: [], events: demo.events } : structuredClone(demo);
const task = id => db.tasks.find(t => t.id === id);
const delivery = id => db.deliveries.find(d => d.id === id);
let kind = null;
let filter = 'all';
let revising = null;

function toast(text) {
  const el = $('#toast');
  el.textContent = text;
  el.classList.add('show');
  clearTimeout(toast.t);
  toast.t = setTimeout(() => el.classList.remove('show'), 2800);
}

// In quale reparto si trova adesso un lavoro
function where(t) {
  if (t.state === 'done') return null;
  if (t.state === 'you') return 'you';
  const s = STEPS[t.kind][t.step];
  return s ? s[1] : 'consegne';
}

const needYou = () => db.tasks.filter(t => ['you', 'stuck'].includes(t.state));
const toPublish = () => db.deliveries.filter(d => !d.published);

/* ---------- schede dei lavori ---------- */

function tracker(t) {
  const steps = STEPS[t.kind];
  return `<ol class="tracker">${steps.map(([s], i) => {
    const cls = i < t.step || t.state === 'done' ? 'done' : i === t.step ? (t.state === 'stuck' ? 'stuck' : t.state === 'queue' ? 'todo' : 'now') : 'todo';
    return `<li class="${cls}"><span class="dot">${cls === 'done' ? icon('i-check') : ''}</span>${s}</li>`;
  }).join('')}</ol>`;
}

function history(t) {
  return t.history && t.history.length ? `<details class="history"><summary>Versioni precedenti (${t.history.length})</summary><ul>${t.history.map(h => `<li>${esc(h)}</li>`).join('')}</ul></details>` : '';
}

function body(t) {
  const changes = `<button class="soft" data-changes="${t.id}">Chiedi modifiche</button>`;
  if (t.state === 'you' && t.ideas) {
    return `<div class="ideas">${t.ideas.map((i, n) => `<label class="idea">
        <input type="radio" name="pick-${t.id}" value="${n}" ${i.tip ? 'checked' : ''}>
        <span><strong>${esc(i.name)}${i.tip ? '<em>consigliata</em>' : ''}</strong>${esc(i.line)}</span>
      </label>`).join('')}</div>
      <div class="buttons"><button class="primary" data-approve="${t.id}">${icon('i-check')}Approva l'idea scelta</button>${changes}</div>`;
  }
  if (t.state === 'you' && t.preview) {
    return `<div class="preview" aria-label="Anteprima del video">
        <div class="screen"><span class="spinlogo">€</span><span class="play">${icon('i-play')}</span></div>
        <p>Anteprima ${vnum(t.version)} · ${esc(t.preview.length)} · ${esc(t.preview.size)}</p>
      </div>
      ${history(t)}
      <div class="buttons"><button class="primary" data-approve="${t.id}">${icon('i-check')}Approva la ${vnum(t.version)}</button>${changes}</div>`;
  }
  if (t.state === 'stuck') {
    return `<div class="planb">
      <p class="planbtitle">Fallo a mano in 3 passi</p>
      <ol>
        <li><span>Copia le istruzioni per ChatGPT</span><button class="soft small" data-copy="${t.id}">${icon('i-copy')}Copia</button></li>
        <li><span>Incollale nella chat di ChatGPT e invia</span></li>
        <li><span>Incolla qui sotto la risposta</span></li>
      </ol>
      <details><summary>Vedi le istruzioni</summary><pre>${esc(t.prompt)}</pre></details>
      <label class="sr" for="answer-${t.id}">Risposta di ChatGPT</label>
      <textarea id="answer-${t.id}" rows="3" placeholder="Incolla qui la risposta di ChatGPT"></textarea>
      <div class="buttons"><button class="primary" data-resume="${t.id}">Continua</button><button class="soft" data-wait="${t.id}">Aspetto che si liberi</button></div>
    </div>`;
  }
  if (t.progress != null && t.state === 'work') {
    return `<div class="bar"><i style="width:${Math.max(4, Math.round(t.progress * 100))}%"></i></div><p class="detail">${esc(t.detail)}</p>${history(t)}`;
  }
  return history(t);
}

function card(t) {
  return `<article class="card s-${t.state}" data-task="${t.id}">
    <div class="cardtop"><span class="kind">${icon(KIND[t.kind].icon)}${KIND[t.kind].label} · ${esc(PROJECT[t.project])}${t.version ? `<b class="ver">${vtag(t.version)}</b>` : ''}</span><span class="state">${t.stateLabel || STATE[t.state]}</span></div>
    <h3>${esc(t.title)}</h3>
    <p class="status">${esc(t.status)}</p>
    ${tracker(t)}
    ${body(t)}
  </article>`;
}

/* ---------- chat ---------- */

let seen = 0;
function message(m, i) {
  const t = m.task ? task(m.task) : null;
  const enter = i >= seen ? ` enter" style="--d:${(i - seen) * 90}ms` : '';
  if (m.from === 'fede') {
    return `<div class="msg me${enter}"><div class="bubble">${esc(m.text)}</div><time>${m.time}</time></div>`;
  }
  return `<div class="msg bot${enter}">
    <img class="face" src="assets/niko-buddy.webp" alt="" width="40" height="40">
    <div class="msgcol"><div class="bubble">${esc(m.text)}</div>${t ? card(t) : ''}<time>Niko · ${m.time}</time></div>
  </div>`;
}

function renderChat() {
  const intro = `<div class="intro"><strong>Questa è la tua chat con Niko.</strong> Puoi scrivergli dalla barra in basso anche dalle altre pagine: le risposte arrivano sempre qui.</div>`;
  $('#messages').innerHTML = intro + db.messages.map(message).join('');
  seen = db.messages.length;
  $('#feed').scrollTop = $('#feed').scrollHeight;
}

/* ---------- centrale: Niko al centro, i reparti intorno ---------- */

// Dove ogni cavo è agganciato, in percentuale dentro la scena. L'ultimo valore dice dove va l'etichetta:
// sul computer sta all'esterno del cavo, sul telefono sotto o sopra l'aggancio.
const anchors = () => innerWidth <= 760
  ? { libreria: [50, 2, 'top'], ideatore: [6, 18, 'tl'], revisore: [94, 18, 'tr'], produzione: [94, 95, 'br'], consegne: [6, 95, 'bl'] }
  : { libreria: [50, 3, 'top'], ideatore: [22, 10, 'ol'], revisore: [78, 10, 'or'], produzione: [78, 94, 'or'], consegne: [22, 94, 'ol'] };

function deptState(id) {
  if (id === 'consegne') {
    const list = toPublish();
    const wait = list.filter(d => !d.captionOk).length;
    if (wait) return { state: 'you', text: `${wait === 1 ? 'Una didascalia' : wait + ' didascalie'} da approvare`, n: list.length };
    return list.length ? { state: 'ready', text: `${list.length} pront${list.length === 1 ? 'o' : 'i'} da pubblicare`, n: list.length } : { state: 'idle', text: 'Niente da pubblicare', n: 0 };
  }
  if (id === 'libreria') {
    const n = db.library.length;
    return { state: 'idle', text: n < 3 ? 'Quasi vuota, aggiungi il tuo gusto' : `${n} cose salvate`, n: 0 };
  }
  const list = db.tasks.filter(t => where(t) === id);
  const stuck = list.find(t => t.state === 'stuck');
  if (stuck) return { state: 'stuck', text: 'Fermo: ' + (/ChatGPT/.test(stuck.status) ? 'limite di ChatGPT' : 'serve una mano'), n: list.length };
  const busy = list.find(t => t.state === 'work');
  if (busy) return { state: 'work', text: busy.progress != null ? `${busy.title.split(',')[0]} · ${Math.round(busy.progress * 100)}%` : busy.title, n: list.length };
  if (list.length) return { state: 'queue', text: `${list.length} in attesa`, n: list.length };
  return { state: 'idle', text: 'Libero', n: 0 };
}

function renderHome() {
  const need = needYou().length;
  holo.states = {};
  const labels = Object.entries(anchors()).map(([id, [x, y, side]]) => {
    const d = DEPTS[id], st = deptState(id);
    holo.states[id] = st.state;
    return `<button class="tag t-${st.state} at-${side}" style="--x:${x}%;--y:${y}%" data-dept="${id}">
      <span class="tagname">${d.name}${st.n ? ` <b>${String(st.n).padStart(2, '0')}</b>` : ''}</span>
      <span class="tagstate">${esc(st.text)}</span>
      <small>${esc(d.uses)}</small>
    </button>`;
  }).join('');
  $('#stage').innerHTML = `<canvas class="holo" aria-hidden="true"></canvas>
    <button class="core${need ? ' alert' : ''}" data-view="${need ? 'work' : 'chat'}">
      <strong>NIKO</strong>
      <span>${need ? `${need === 1 ? 'Una cosa aspetta' : need + ' cose aspettano'} te` : 'Tutto tranquillo'}</span>
    </button>
    ${labels}`;
  holo.mount($('#stage canvas'));

  const next = db.events.filter(e => e.type === 'out' && e.date >= dkey(new Date())).sort((a, b) => a.date.localeCompare(b.date))[0];
  const nd = next && db.deliveries.find(d => d.date === next.date && !d.published);
  $('#glance').innerHTML = `
    <article class="tile"><h2>Serve te<b>${need}</b></h2>${need ? `<ul>${needYou().map(t => `<li><span class="led ${t.state === 'stuck' ? 'warn' : 'you'}"></span>${esc(t.title)}</li>`).join('')}</ul><button class="soft small" data-view="work">Vai ai lavori ${icon('i-arrow')}</button>` : '<p>Niente, puoi creare.</p>'}</article>
    <article class="tile"><h2>Prossima uscita</h2>${next ? `<p class="big">${esc(next.title)}</p><p>${esc(longDate(next.date))}${nd ? ` · ${nd.captionOk ? 'pacchetto pronto' : 'manca il tuo ok sulla didascalia'}` : ''}</p><button class="soft small" data-view="${nd ? 'consegne' : 'calendar'}">${nd ? 'Apri la consegna' : 'Apri il calendario'} ${icon('i-arrow')}</button>` : '<p>Nessuna uscita in programma.</p>'}</article>
    <article class="tile"><h2>Collegamenti</h2><ul>${db.links.map(l => `<li><span class="led ${l.ok ? 'ok' : 'warn'}"></span><span><strong>${esc(l.name)}</strong> ${esc(l.note)}</span></li>`).join('')}</ul></article>`;
}

/* ---------- lavori, divisi per reparto ---------- */

function renderWork() {
  const depts = ['ideatore', 'revisore', 'produzione'];
  $('#filters').innerHTML = [['all', 'Tutti'], ...depts.map(d => [d, DEPTS[d].name])]
    .map(([id, name]) => `<button data-filter="${id}" aria-pressed="${filter === id}">${name}</button>`).join('');
  const group = (name, list, sub) => `<section class="group"><h2>${name}<span>${list.length}</span>${sub ? `<small>${sub}</small>` : ''}</h2>${list.length ? `<div class="cards">${list.map(card).join('')}</div>` : '<p class="empty">Niente qui.</p>'}</section>`;
  let html = group('Serve te', needYou());
  for (const d of depts) {
    if (filter !== 'all' && filter !== d) continue;
    html += group(DEPTS[d].name, db.tasks.filter(t => where(t) === d && ['work', 'queue'].includes(t.state)), DEPTS[d].does);
  }
  if (filter === 'all') html += group('Finiti', db.tasks.filter(t => t.state === 'done'));
  $('#worklist').innerHTML = html;
}

/* ---------- consegne ---------- */

function deliveryCard(d) {
  const st = d.published ? 'done' : d.captionOk ? 'ready' : 'you';
  const label = { you: 'Manca il tuo ok', ready: 'Pronto da pubblicare', done: 'Pubblicato' }[st];
  return `<article class="card delivery s-${st}" data-delivery="${d.id}">
    <div class="cardtop"><span class="kind">${icon('i-box')}${esc(d.where)}<b class="ver">${vtag(d.version)}</b></span><span class="state">${label}</span></div>
    <h3>${esc(d.title)}</h3>
    <p class="status">Esce ${esc(longDate(d.date))}</p>
    <ul class="pack">
      <li class="ok"><span class="dot">${icon('i-check')}</span><div><strong>Video finale</strong><span>${esc(d.file)} · ${esc(d.length)} · ${vnum(d.version)} approvata da te</span></div></li>
      <li class="${d.captionOk ? 'ok' : 'wait'}"><span class="dot">${d.captionOk ? icon('i-check') : ''}</span><div><strong>Didascalia</strong>
        ${d.captionOk || d.published ? `<p class="caption">${esc(d.caption)}</p>` : `<label class="sr" for="cap-${d.id}">Didascalia</label><textarea id="cap-${d.id}" rows="5">${esc(d.caption)}</textarea>`}
      </div></li>
      <li class="ok"><span class="dot">${icon('i-check')}</span><div><strong>Dove e quando</strong><span>${esc(d.where)} · ${esc(longDate(d.date))}</span></div></li>
    </ul>
    <div class="buttons">${d.published ? '' : d.captionOk
      ? `<button class="primary" data-published="${d.id}">${icon('i-check')}L'ho pubblicato</button><button class="soft" data-copycap="${d.id}">${icon('i-copy')}Copia didascalia</button><button class="soft" data-editcap="${d.id}">Modifica didascalia</button>`
      : `<button class="primary" data-capok="${d.id}">${icon('i-check')}Approva la didascalia</button>`}</div>
  </article>`;
}

function renderConsegne() {
  const open = toPublish().sort((a, b) => a.date.localeCompare(b.date));
  const done = db.deliveries.filter(d => d.published);
  $('#deliveries').innerHTML = `<section class="group"><h2>Da pubblicare<span>${open.length}</span></h2>${open.length ? `<div class="cards">${open.map(deliveryCard).join('')}</div>` : '<p class="empty">Niente da pubblicare. Quando approvi un video finale, il pacchetto arriva qui.</p>'}</section>
    <section class="group"><h2>Pubblicati<span>${done.length}</span></h2>${done.length ? `<div class="cards">${done.map(deliveryCard).join('')}</div>` : '<p class="empty">Ancora niente.</p>'}</section>`;
}

/* ---------- libreria ---------- */

const SAVE = 'niko-libreria-v1';
if (!REAL) { try { const saved = JSON.parse(localStorage.getItem(SAVE)); if (Array.isArray(saved)) db.library = saved; } catch {} }
const saveLibrary = () => { try { localStorage.setItem(SAVE, JSON.stringify(db.library)); } catch {} };

function libItem(it, i) {
  let text = esc(it.text);
  if (/^https?:\/\/\S+$/.test(it.text)) {
    try { const u = new URL(it.text); text = `<a href="${esc(u.href)}" target="_blank" rel="noopener">${esc(u.hostname.replace(/^www\./, '') + (u.pathname.length > 1 ? u.pathname : ''))}</a>`; } catch {}
  }
  return `<li><span>${text}</span><button class="close" data-unlib="${i}" aria-label="Togli">✕</button></li>`;
}

function renderLibrary() {
  $('#addshelf').innerHTML = SHELVES.map(s => `<option value="${s.id}">${s.name}</option>`).join('');
  $('#shelves').innerHTML = SHELVES.map(s => {
    const items = db.library.map((it, i) => [it, i]).filter(([it]) => it.shelf === s.id);
    return `<section class="shelf"><h2>${s.name}<span>${items.length}</span></h2><p>${s.hint}</p>
      ${items.length ? `<ul>${items.map(([it, i]) => libItem(it, i)).join('')}</ul>` : '<p class="empty">Vuoto per ora.</p>'}</section>`;
  }).join('');
}

/* ---------- Niko, calendario ---------- */

function renderNiko() {
  const need = needYou().length, pub = toPublish().length;
  const busy = db.tasks.find(t => t.state === 'work');
  $('.nikosays').textContent = need
    ? `Ho ${need === 1 ? 'una cosa' : need + ' cose'} da farti vedere.${busy ? ' Intanto ' + busy.status.charAt(0).toLowerCase() + busy.status.slice(1) : ''}`
    : pub ? `Niente da approvare. In Consegne ${pub === 1 ? 'c\'è un pacchetto' : 'ci sono ' + pub + ' pacchetti'} da pubblicare.`
      : busy ? busy.status : 'Tutto tranquillo. Cosa creiamo?';
  const cta = $('.nikocta');
  cta.hidden = !need && !pub;
  cta.dataset.view = need ? 'work' : 'consegne';
  cta.innerHTML = need ? `Guarda ${need === 1 ? 'ora' : 'le ' + need} ${icon('i-arrow')}` : `Apri Consegne ${icon('i-arrow')}`;
  $$('[data-badge=work]').forEach(b => { b.textContent = need || ''; });
  $$('[data-badge=consegne]').forEach(b => { b.textContent = pub || ''; });
}

let month = new Date();
month = new Date(month.getFullYear(), month.getMonth(), 1);
const dkey = d => `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}-${String(d.getDate()).padStart(2, '0')}`;
const longDate = k => new Date(k + 'T12:00').toLocaleDateString('it-IT', { weekday: 'long', day: 'numeric', month: 'long' });
function renderCalendar() {
  $('#monthlabel').textContent = month.toLocaleDateString('it-IT', { month: 'long', year: 'numeric' });
  const offset = (month.getDay() + 6) % 7;
  const days = new Date(month.getFullYear(), month.getMonth() + 1, 0).getDate();
  const today = dkey(new Date());
  let html = ['Lun', 'Mar', 'Mer', 'Gio', 'Ven', 'Sab', 'Dom'].map(d => `<div class="wd">${d}</div>`).join('');
  for (let i = 0; i < Math.ceil((offset + days) / 7) * 7; i++) {
    const d = i - offset + 1;
    if (d < 1 || d > days) { html += '<div class="day out"></div>'; continue; }
    const key = dkey(new Date(month.getFullYear(), month.getMonth(), d));
    html += `<div class="day${key === today ? ' today' : ''}"><b>${d}</b>${db.events.filter(e => e.date === key).map(e => `<span class="ev ${e.type}">${esc(e.title)}</span>`).join('')}</div>`;
  }
  $('#calendar').innerHTML = html;
}

function renderAll() { renderChat(); renderHome(); renderWork(); renderConsegne(); renderNiko(); }

/* ---------- navigazione ---------- */

const views = ['home', 'chat', 'work', 'consegne', 'libreria', 'calendar'];
function show(name) {
  $$('.view').forEach(v => v.classList.toggle('active', v.id === 'view-' + name));
  $$('.nav [data-view], .tabs [data-view]').forEach(b => {
    b.classList.toggle('active', b.dataset.view === name);
    if (b.dataset.view === name) b.setAttribute('aria-current', 'page'); else b.removeAttribute('aria-current');
  });
  document.body.dataset.view = name;
  if (name === 'chat') { $('#feed').scrollTop = $('#feed').scrollHeight; $('#peek').hidden = true; }
  if (name === 'home') { holo.size(); holo.draw(performance.now()); }
  const v = $('#view-' + name);
  if (v.classList.contains('page')) v.scrollTop = 0;
}

/* ---------- la barra per parlare con Niko ---------- */

function guess(text) {
  if (kind) return kind;
  if (/blender|3d|scena/i.test(text)) return 'blender';
  if (/hyperframes|animat|titolo|video/i.test(text)) return 'hyperframes';
  return 'idee';
}

// Quando scrivi da un'altra pagina resti dove sei: la risposta compare sopra la barra
function peek(text) {
  if (document.body.dataset.view === 'chat') return;
  $('#peektext').textContent = text;
  $('#peek').hidden = false;
  clearTimeout(peek.t);
  peek.t = setTimeout(() => { $('#peek').hidden = true; }, 9000);
}

function setRevising(id) {
  revising = id;
  const t = id && task(id);
  $('#revising').hidden = !t;
  if (t) $('#revising span').textContent = `Modifiche per "${t.title}", ${vnum(t.version)}`;
  $('#prompt').placeholder = t ? 'Scrivi cosa vuoi cambiare…' : 'Scrivi a Niko cosa ti serve…';
}

function grow() {
  const p = $('#prompt');
  p.style.height = 'auto';
  p.style.height = Math.min(p.scrollHeight, 140) + 'px';
}

function reply(text, taskId) {
  setTimeout(() => {
    db.messages.push({ from: 'niko', time: now(), text, task: taskId });
    renderAll();
    peek(text);
  }, calm ? 0 : 700);
}

function send(text) {
  text = text.trim();
  if (!text) { $('#prompt').focus(); return; }
  db.messages.push({ from: 'fede', time: now(), text });
  $('#prompt').value = '';
  grow();
  if (revising) {
    const t = task(revising);
    t.history = [...(t.history || []), `${vnum(t.version).replace('v', 'V')}: ${text}`];
    t.version += 1;
    t.state = 'work'; t.step = 0; t.progress = 0.04; t.detail = 'Appena partita';
    t.status = `Preparo la ${vnum(t.version)} con le tue modifiche.`;
    setRevising(null);
    renderAll();
    reply(`Ok, preparo la ${vnum(t.version)}. Te la mostro appena il Revisore la controlla.`, t.id);
    return;
  }
  const k = guess(text);
  const t = {
    id: 'n' + Date.now(), kind: k, project: $('#project').value, state: 'queue', step: 0, version: 1,
    title: text.length > 60 ? text.slice(0, 57) + '…' : text,
    status: 'In questa anteprima non parte niente. Con il sistema collegato, qui vedresti il lavoro avanzare.',
  };
  db.tasks.unshift(t);
  renderAll();
  reply(`Ricevuto! Lo passo ${k === 'idee' ? 'all\'Ideatore' : 'a Produzione'}. Ti scrivo appena c'è qualcosa da vedere.`, t.id);
}

/* ---------- approvazione: sempre di una versione precisa ---------- */

let pending = null;
function ask(kicker, title, text, then) {
  pending = then;
  $('#sheetkicker').textContent = kicker;
  $('#sheettitle').textContent = title;
  $('#sheettext').textContent = text;
  $('#sheet').hidden = false;
  $('#sheetok').focus();
}
function closeSheet() { $('#sheet').hidden = true; pending = null; }
$('#sheetok').onclick = () => { const f = pending; closeSheet(); if (f) f(); };
$('#sheetno').onclick = closeSheet;
$('#sheet').addEventListener('click', e => { if (e.target.id === 'sheet') closeSheet(); });
document.addEventListener('keydown', e => { if (e.key === 'Escape' && !$('#sheet').hidden) closeSheet(); });

function approve(t, b) {
  if (t.ideas) {
    const pick = b.closest('.card').querySelector('input:checked');
    const idea = pick ? t.ideas[pick.value] : null;
    ask(`${KIND[t.kind].label} · ${vnum(t.version)}`, `Approvi "${idea ? idea.name : t.title}"?`,
      'Dopo il tuo ok l\'Ideatore scrive lo script su questa idea.', () => {
        t.state = 'done'; t.step = STEPS[t.kind].length;
        t.status = idea ? `Hai scelto "${idea.name}".` : 'Approvato da te.';
        db.messages.push({ from: 'niko', time: now(), text: idea ? `Perfetto, teniamo "${idea.name}". Preparo lo script.` : 'Perfetto, approvato.' });
        renderAll();
        toast('Approvato');
      });
    return;
  }
  ask(`${KIND[t.kind].label} · ${vnum(t.version)}`, `Approvi la ${vnum(t.version)}?`,
    `Approvi proprio questa versione. Dopo il tuo ok Produzione fa il video finale in alta qualità e lo porta in Consegne.`, () => {
      t.state = 'work'; t.step = 3; t.progress = 0.04; t.detail = 'Il render parte tra poco';
      t.status = `Faccio il video finale della ${vnum(t.version)}. Poi lo trovi in Consegne.`;
      db.messages.push({ from: 'niko', time: now(), text: `Grazie! ${vnum(t.version).replace('v', 'V')} approvata, parto con il video finale.` });
      renderAll();
      toast(`${vnum(t.version).replace('v', 'V')} approvata`);
    });
}

/* ---------- clic ---------- */

document.addEventListener('click', e => {
  const b = e.target.closest('button');
  if (!b) return;
  if (b.dataset.view) show(b.dataset.view);
  if (b.dataset.dept) {
    const d = b.dataset.dept;
    if (d === 'consegne' || d === 'libreria') show(d);
    else { filter = d; renderWork(); show('work'); }
  }
  if (b.dataset.filter) { filter = b.dataset.filter; renderWork(); }
  if (b.dataset.kind) {
    kind = kind === b.dataset.kind ? null : b.dataset.kind;
    $$('[data-kind]').forEach(x => x.setAttribute('aria-pressed', String(x.dataset.kind === kind)));
  }
  if (b.dataset.try) {
    kind = b.dataset.try;
    $$('[data-kind]').forEach(x => x.setAttribute('aria-pressed', String(x.dataset.kind === kind)));
    $('#prompt').value = b.dataset.text;
    grow();
    $('#prompt').focus();
  }
  if (b.dataset.approve) approve(task(b.dataset.approve), b);
  if (b.dataset.changes) {
    setRevising(b.dataset.changes);
    $('#prompt').focus();
  }
  if (b.dataset.copy) copy(task(b.dataset.copy).prompt, b, 'Istruzioni copiate');
  if (b.dataset.resume) {
    const t = task(b.dataset.resume);
    const box = b.closest('.planb').querySelector('textarea');
    if (!box.value.trim()) { toast('Incolla prima la risposta di ChatGPT'); box.focus(); return; }
    t.state = 'work'; t.step = 1; t.status = 'Risposta ricevuta. Ora il Revisore la controlla.';
    db.messages.push({ from: 'niko', time: now(), text: 'Grazie! Ho la risposta, la faccio controllare.' });
    renderAll();
  }
  if (b.dataset.wait) toast('Ok, riprovo da solo quando ChatGPT si libera');
  if (b.dataset.capok) {
    const d = delivery(b.dataset.capok);
    d.caption = $(`#cap-${d.id}`).value.trim() || d.caption;
    d.captionOk = true;
    renderAll();
    toast('Didascalia approvata');
  }
  if (b.dataset.editcap) { delivery(b.dataset.editcap).captionOk = false; renderAll(); $(`#cap-${b.dataset.editcap}`).focus(); }
  if (b.dataset.copycap) copy(delivery(b.dataset.copycap).caption, b, 'Didascalia copiata');
  if (b.dataset.published) {
    const d = delivery(b.dataset.published);
    ask(d.where, `Hai pubblicato "${d.title}"?`, 'Lo sposto tra i pubblicati. Niko non pubblica niente da solo: questo serve solo a tenere il conto.', () => {
      d.published = true;
      renderAll();
      toast('Segnato come pubblicato');
    });
  }
  if (b.dataset.unlib) { db.library.splice(Number(b.dataset.unlib), 1); saveLibrary(); renderLibrary(); renderHome(); }
});

function copy(text, b, ok) {
  const fallback = () => {
    const pre = b.closest('.card').querySelector('pre, .caption, textarea');
    const d = pre && pre.closest('details'); if (d) d.open = true;
    if (pre) { if (pre.select) pre.select(); else getSelection().selectAllChildren(pre); }
    toast('Selezionato: premi Cmd+C');
  };
  navigator.clipboard ? navigator.clipboard.writeText(text).then(() => toast(ok), fallback) : fallback();
}

$('#composer').addEventListener('submit', e => { e.preventDefault(); send($('#prompt').value); });
$('#prompt').addEventListener('keydown', e => {
  if (e.key === 'Enter' && !e.shiftKey && !e.isComposing) { e.preventDefault(); send($('#prompt').value); }
});
$('#prompt').addEventListener('input', grow);
$('#revcancel').onclick = () => setRevising(null);
$('#peekclose').onclick = () => { $('#peek').hidden = true; };
$('#addform').addEventListener('submit', e => {
  e.preventDefault();
  const text = $('#addtext').value.trim();
  if (!text) { $('#addtext').focus(); return; }
  db.library.push({ shelf: $('#addshelf').value, text });
  saveLibrary();
  $('#addtext').value = '';
  renderLibrary(); renderHome();
  toast('Aggiunto alla libreria');
});
$('#prevmonth').onclick = () => { month.setMonth(month.getMonth() - 1); renderCalendar(); };
$('#nextmonth').onclick = () => { month.setMonth(month.getMonth() + 1); renderCalendar(); };
$('#thismonth').onclick = () => { const d = new Date(); month = new Date(d.getFullYear(), d.getMonth(), 1); renderCalendar(); };
window.addEventListener('hashchange', () => { const v = location.hash.slice(1); if (views.includes(v)) show(v); });

/* ---------- l'ologramma della Centrale, tenuto su dai cavi dei reparti ---------- */

const holo = {
  states: {},
  cv: null,
  mount(cv) { this.cv = cv; this.ctx = cv.getContext('2d'); this.size(); this.draw(performance.now()); },
  size() {
    if (!this.cv) return;
    const r = this.cv.getBoundingClientRect(), dpr = Math.min(devicePixelRatio || 1, 2);
    this.w = r.width; this.h = r.height;
    this.cv.width = r.width * dpr; this.cv.height = r.height * dpr;
    this.ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
  },
  draw(t) {
    const { ctx, w, h } = this;
    if (!ctx || !w) return;
    ctx.clearRect(0, 0, w, h);
    const cx = w / 2, cy = h * 0.47, R = Math.min(w, h) * (w < 600 ? 0.2 : 0.17);
    if (this.below !== cy + R) { this.below = cy + R; this.cv.parentElement.style.setProperty('--below', Math.round(cy + R + 18) + 'px'); }
    const flick = 0.9 + 0.1 * Math.sin(t * 0.03) * Math.sin(t * 0.011);
    const glitch = (t % 4200) < 110 ? Math.sin(t) * 6 : 0;

    // cavi: da ogni aggancio all'anello dell'ologramma
    const COL = { work: [142, 248, 255], you: [243, 155, 227], ready: [143, 240, 189], stuck: [255, 197, 138], queue: [190, 160, 255], idle: [150, 135, 190] };
    for (const [id, [px, py]] of Object.entries(anchors())) {
      const st = this.states[id] || 'idle', c = COL[st];
      const ax = w * px / 100, ay = h * py / 100;
      const th = Math.atan2(ay - cy, ax - cx);
      const bx = cx + Math.cos(th) * R * 1.45, by = cy + Math.sin(th) * R * 0.42;
      const sway = Math.sin(t * 0.0009 + px) * 6;
      const mx = (ax + bx) / 2 + sway, my = (ay + by) / 2 + Math.hypot(ax - bx, ay - by) * 0.12;
      const path = () => { ctx.beginPath(); ctx.moveTo(ax, ay); ctx.quadraticCurveTo(mx, my, bx, by); };
      // guaina scura e anima luminosa
      path(); ctx.strokeStyle = 'rgba(8,6,18,.9)'; ctx.lineWidth = 5; ctx.stroke();
      const live = st === 'work' || st === 'you' || st === 'ready';
      const a = st === 'idle' ? 0.25 : st === 'stuck' ? 0.35 + 0.5 * (Math.sin(t * 0.02) > 0.6 ? 1 : 0.2) : live ? 0.85 : 0.45;
      path(); ctx.strokeStyle = `rgba(${c},${a})`; ctx.lineWidth = live ? 1.6 : 1.1;
      ctx.shadowColor = `rgba(${c},.9)`; ctx.shadowBlur = live ? 10 : 0; ctx.stroke(); ctx.shadowBlur = 0;
      // impulsi di energia lungo il cavo
      if (live) {
        for (let k = 0; k < 3; k++) {
          let u = ((t * 0.00035 + k / 3 + px * 0.01) % 1);
          if (st === 'you') u = 1 - u; // verso di te
          const qx = (1 - u) ** 2 * ax + 2 * (1 - u) * u * mx + u * u * bx, qy = (1 - u) ** 2 * ay + 2 * (1 - u) * u * my + u * u * by;
          ctx.fillStyle = `rgba(${c},.95)`; ctx.shadowColor = `rgb(${c})`; ctx.shadowBlur = 12;
          ctx.beginPath(); ctx.arc(qx, qy, 2.4, 0, 6.283); ctx.fill(); ctx.shadowBlur = 0;
        }
      }
      // morsetti alle due estremità
      ctx.fillStyle = '#0b0818'; ctx.strokeStyle = `rgba(${c},${Math.max(a, 0.4)})`; ctx.lineWidth = 1.2;
      for (const [x, y, s] of [[ax, ay, 5], [bx, by, 3.5]]) { ctx.beginPath(); ctx.rect(x - s, y - s, s * 2, s * 2); ctx.fill(); ctx.stroke(); }
    }

    // l'ologramma
    ctx.save();
    ctx.translate(glitch, 0);
    const halo = ctx.createRadialGradient(cx, cy, R * 0.2, cx, cy, R * 2.2);
    halo.addColorStop(0, 'rgba(142,248,255,.16)'); halo.addColorStop(1, 'rgba(142,248,255,0)');
    ctx.fillStyle = halo; ctx.fillRect(cx - R * 2.2, cy - R * 2.2, R * 4.4, R * 4.4);
    ctx.globalAlpha = flick;
    ctx.strokeStyle = 'rgba(142,248,255,.55)'; ctx.lineWidth = 1;
    const spin = t * 0.00035;
    // meridiani
    for (let k = 0; k < 9; k++) {
      const ph = spin + k * Math.PI / 9, rx = Math.abs(Math.cos(ph)) * R;
      ctx.globalAlpha = flick * (Math.sin(ph) > 0 ? 0.75 : 0.25);
      ctx.beginPath(); ctx.ellipse(cx, cy, rx, R, 0, 0, 6.283); ctx.stroke();
    }
    // paralleli
    ctx.globalAlpha = flick * 0.5;
    for (let j = -3; j <= 3; j++) {
      const la = j * Math.PI / 8, y = cy + Math.sin(la) * R, rx = Math.cos(la) * R;
      ctx.beginPath(); ctx.ellipse(cx, y, rx, rx * 0.16, 0, 0, 6.283); ctx.stroke();
    }
    // nucleo che respira
    const pulse = 0.5 + 0.5 * Math.sin(t * 0.002);
    const core = ctx.createRadialGradient(cx, cy, 0, cx, cy, R * 0.5);
    core.addColorStop(0, `rgba(230,250,255,${0.75 + 0.25 * pulse})`); core.addColorStop(0.35, 'rgba(142,248,255,.45)'); core.addColorStop(1, 'rgba(184,146,255,0)');
    ctx.globalAlpha = flick; ctx.fillStyle = core; ctx.beginPath(); ctx.arc(cx, cy, R * 0.5, 0, 6.283); ctx.fill();
    // poliedro interno che gira al contrario
    ctx.strokeStyle = 'rgba(200,175,255,.7)'; ctx.globalAlpha = flick * 0.8;
    const pts = Array.from({ length: 6 }, (_, i) => { const an = -spin * 2 + i * Math.PI / 3; return [cx + Math.cos(an) * R * 0.38, cy + Math.sin(an) * R * 0.38 * 0.9]; });
    ctx.beginPath(); pts.forEach(([x, y], i) => i ? ctx.lineTo(x, y) : ctx.moveTo(x, y)); ctx.closePath();
    pts.forEach(([x, y], i) => { if (i % 2 === 0) { ctx.moveTo(x, y); ctx.lineTo(...pts[(i + 3) % 6]); } });
    ctx.stroke();
    // anello dove si agganciano i cavi
    ctx.globalAlpha = 0.9; ctx.strokeStyle = 'rgba(190,160,255,.75)'; ctx.lineWidth = 1.4;
    ctx.beginPath(); ctx.ellipse(cx, cy, R * 1.45, R * 0.42, 0, 0, 6.283); ctx.stroke();
    ctx.setLineDash([2, 6]); ctx.lineDashOffset = -t * 0.02; ctx.strokeStyle = 'rgba(142,248,255,.6)';
    ctx.beginPath(); ctx.ellipse(cx, cy, R * 1.6, R * 0.47, 0, 0, 6.283); ctx.stroke(); ctx.setLineDash([]);
    // linee di scansione
    ctx.globalAlpha = 0.07; ctx.fillStyle = '#8ef8ff';
    for (let y = cy - R + ((t * 0.03) % 4); y < cy + R; y += 4) ctx.fillRect(cx - R, y, R * 2, 1);
    ctx.restore();
  },
};

(function holoLoop() {
  let last = 0;
  const tick = t => {
    requestAnimationFrame(tick);
    if (document.hidden || document.body.dataset.view !== 'home' || t - last < 33) return;
    last = t;
    holo.draw(t);
  };
  if (!calm) requestAnimationFrame(tick);
  let wide = innerWidth > 760;
  addEventListener('resize', () => {
    if (wide !== innerWidth > 760) { wide = !wide; renderHome(); }
    holo.size(); holo.draw(performance.now());
  });
})();

/* ---------- lo spazio fuori dalla finestra ---------- */

function space() {
  const cv = $('#space');
  const ctx = cv.getContext('2d');
  let w, h, stars;
  const rand = (a, b) => a + Math.random() * (b - a);

  function size() {
    const dpr = Math.min(devicePixelRatio || 1, 1.5);
    w = innerWidth; h = innerHeight;
    cv.width = w * dpr; cv.height = h * dpr;
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    stars = Array.from({ length: Math.round(w * h / 7000) }, () => ({ x: rand(0, w), y: rand(0, h), r: rand(0.3, 1.4), p: rand(0, 6.28), s: rand(0.4, 1.4), z: rand(0.2, 1) }));
  }

  function ring(x, y, r, c, front) {
    ctx.save();
    ctx.translate(x, y); ctx.rotate(-0.32);
    ctx.beginPath();
    if (front) ctx.rect(-r * 2.4, 0, r * 4.8, r * 2); else ctx.rect(-r * 2.4, -r * 2, r * 4.8, r * 2);
    ctx.clip();
    for (const [k, a] of [[1.4, 0.4], [1.6, 0.25], [1.85, 0.14]]) {
      ctx.strokeStyle = c.ring; ctx.globalAlpha = a; ctx.lineWidth = r * 0.1;
      ctx.beginPath(); ctx.ellipse(0, 0, r * k, r * k * 0.22, 0, 0, 6.283); ctx.stroke();
    }
    ctx.restore();
  }

  function planet(x, y, r, t, c) {
    if (c.ring) ring(x, y, r, c, false);
    ctx.save();
    ctx.beginPath(); ctx.arc(x, y, r, 0, 6.283); ctx.clip();
    const base = ctx.createRadialGradient(x - r * 0.35, y - r * 0.35, r * 0.1, x, y, r);
    base.addColorStop(0, c.light); base.addColorStop(1, c.dark);
    ctx.fillStyle = base; ctx.fillRect(x - r, y - r, r * 2, r * 2);
    // bande che scorrono: il pianeta gira piano
    ctx.globalAlpha = 0.18;
    for (let i = 0; i < c.bands; i++) {
      const by = y - r + (i + 0.5) * (2 * r / c.bands);
      ctx.fillStyle = i % 2 ? c.band : c.light;
      ctx.beginPath();
      ctx.ellipse(x + Math.sin(t * c.spin + i * 1.7) * r * 0.3, by, r * 1.4, r / c.bands * 0.5, 0, 0, 6.283);
      ctx.fill();
    }
    ctx.globalAlpha = 1;
    const shade = ctx.createRadialGradient(x - r * 0.45, y - r * 0.45, r * 0.3, x - r * 0.2, y - r * 0.2, r * 1.45);
    shade.addColorStop(0, 'rgba(0,0,0,0)'); shade.addColorStop(1, 'rgba(4,2,12,.9)');
    ctx.fillStyle = shade; ctx.fillRect(x - r, y - r, r * 2, r * 2);
    ctx.restore();
    const glow = ctx.createRadialGradient(x, y, r * 0.95, x, y, r * 1.2);
    glow.addColorStop(0, c.glow); glow.addColorStop(1, 'rgba(0,0,0,0)');
    ctx.fillStyle = glow; ctx.beginPath(); ctx.arc(x, y, r * 1.2, 0, 6.283); ctx.fill();
    if (c.ring) ring(x, y, r, c, true);
  }

  const giant = { light: '#b796ff', dark: '#2a1650', band: '#ef8cdd', glow: 'rgba(170,120,255,.35)', ring: '#9fe9ff', bands: 9, spin: 0.00005 };
  const blue = { light: '#9ef3ff', dark: '#0d2a46', band: '#5fb4ff', glow: 'rgba(110,220,255,.3)', bands: 6, spin: 0.00008 };
  const moon = { light: '#f3c6ff', dark: '#3b1d45', band: '#ffffff', glow: 'rgba(240,160,255,.25)', bands: 3, spin: 0.0001 };

  function frame(t) {
    ctx.clearRect(0, 0, w, h);
    const neb = ctx.createRadialGradient(w * 0.75, h * 0.25, 0, w * 0.75, h * 0.25, Math.max(w, h) * 0.8);
    neb.addColorStop(0, 'rgba(110,50,170,.35)'); neb.addColorStop(0.5, 'rgba(30,20,80,.25)'); neb.addColorStop(1, 'rgba(0,0,0,0)');
    ctx.fillStyle = neb; ctx.fillRect(0, 0, w, h);
    ctx.fillStyle = '#ece6ff';
    for (const s of stars) {
      const x = ((s.x - t * 0.006 * s.z) % w + w) % w;
      ctx.globalAlpha = 0.3 + 0.7 * Math.abs(Math.sin(t * 0.0007 * s.s + s.p));
      ctx.beginPath(); ctx.arc(x, s.y, s.r, 0, 6.283); ctx.fill();
    }
    ctx.globalAlpha = 1;
    const m = Math.min(w, h), drift = Math.sin(t * 0.00006);
    planet(w * 0.3 + drift * 30, h * 0.16, m * 0.05, t, blue);
    const gx = w * 0.6 - drift * 15, gy = h * 0.98, gr = m * 0.46;
    planet(gx, gy, gr, t, giant);
    const a = t * 0.00012;
    const mx = gx + Math.cos(a) * gr * 1.8, my = gy - gr * 0.9 + Math.sin(a) * gr * 0.3;
    if (Math.sin(a) > 0 || Math.hypot(mx - gx, my - gy) > gr) planet(mx, my, m * 0.03, t, moon);
  }

  let last = 0, raf;
  function loop(t) {
    raf = requestAnimationFrame(loop);
    if (t - last < 33) return; // circa 30 fotogrammi al secondo, leggero per il Mac
    last = t;
    frame(t);
  }
  size();
  addEventListener('resize', () => { size(); frame(performance.now()); });
  frame(0);
  if (calm) return;
  document.addEventListener('visibilitychange', () => { cancelAnimationFrame(raf); if (!document.hidden) raf = requestAnimationFrame(loop); });
  raf = requestAnimationFrame(loop);
}

renderAll();
renderLibrary();
renderCalendar();
show(views.includes(location.hash.slice(1)) ? location.hash.slice(1) : 'home');
space();
