'use strict';
const $ = s => document.querySelector(s);
const $$ = s => [...document.querySelectorAll(s)];
const esc = s => String(s).replace(/[&<>"']/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' })[c]);
const icon = n => `<svg aria-hidden="true"><use href="#${n}"/></svg>`;
const now = () => new Date().toLocaleTimeString('it-IT', { hour: '2-digit', minute: '2-digit' });
const calm = matchMedia('(prefers-reduced-motion: reduce)').matches;

const db = structuredClone(demo);
const task = id => db.tasks.find(t => t.id === id);
let kind = null;

function toast(text) {
  const el = $('#toast');
  el.textContent = text;
  el.classList.add('show');
  clearTimeout(toast.t);
  toast.t = setTimeout(() => el.classList.remove('show'), 2800);
}

/* ---------- schede dei lavori ---------- */

function tracker(t) {
  const steps = STEPS[t.kind];
  return `<ol class="tracker">${steps.map((s, i) => {
    const cls = i < t.step || t.state === 'done' ? 'done' : i === t.step ? (t.state === 'stuck' ? 'stuck' : t.state === 'queue' ? 'todo' : 'now') : 'todo';
    return `<li class="${cls}"><span class="dot">${cls === 'done' ? icon('i-check') : ''}</span>${s}</li>`;
  }).join('')}</ol>`;
}

function body(t) {
  if (t.state === 'you' && t.ideas) {
    return `<div class="ideas">${t.ideas.map((i, n) => `<label class="idea">
        <input type="radio" name="pick-${t.id}" value="${n}" ${i.tip ? 'checked' : ''}>
        <span><strong>${esc(i.name)}${i.tip ? '<em>consigliata</em>' : ''}</strong>${esc(i.line)}</span>
      </label>`).join('')}</div>
      <div class="buttons"><button class="primary" data-approve="${t.id}">${icon('i-check')}Approva l'idea scelta</button><button class="soft" data-changes="${t.id}">Chiedi modifiche</button></div>`;
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
  if (t.progress != null) {
    return `<div class="bar"><i style="width:${Math.round(t.progress * 100)}%"></i></div><p class="detail">${esc(t.detail)}</p>`;
  }
  return '';
}

function card(t) {
  return `<article class="card s-${t.state}" data-task="${t.id}">
    <div class="cardtop"><span class="kind">${icon(KIND[t.kind].icon)}${KIND[t.kind].label} · ${esc(PROJECT[t.project])}</span><span class="state">${STATE[t.state]}</span></div>
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
  const intro = `<div class="intro"><strong>Questa è la tua chat con Niko.</strong> Scrivi cosa ti serve: Niko lo passa all'agente giusto e ti porta qui il risultato da approvare.</div>`;
  $('#messages').innerHTML = intro + db.messages.map(message).join('');
  seen = db.messages.length;
  $('#feed').scrollTop = $('#feed').scrollHeight;
}

/* ---------- lavori ---------- */

function renderWork() {
  const groups = [
    ['Serve te', ['you', 'stuck']],
    ['In corso', ['work', 'queue']],
    ['Finiti', ['done']],
  ];
  $('#worklist').innerHTML = groups.map(([name, states]) => {
    const list = db.tasks.filter(t => states.includes(t.state));
    return `<section class="group"><h2>${name}<span>${list.length}</span></h2>${list.length ? `<div class="cards">${list.map(card).join('')}</div>` : '<p class="empty">Niente qui.</p>'}</section>`;
  }).join('');
}

/* ---------- Niko, squadra, calendario ---------- */

function renderNiko() {
  const need = db.tasks.filter(t => ['you', 'stuck'].includes(t.state)).length;
  const busy = db.tasks.find(t => t.state === 'work');
  $('#nikosays').textContent = need
    ? `Ho ${need === 1 ? 'una cosa' : need + ' cose'} da farti vedere.${busy ? ' Intanto ' + busy.status.charAt(0).toLowerCase() + busy.status.slice(1) : ''}`
    : busy ? busy.status : 'Tutto tranquillo. Cosa creiamo?';
  $('#nikocta').hidden = !need;
  $('#nikocta').innerHTML = `Guarda ${need === 1 ? 'ora' : 'le ' + need} ${icon('i-arrow')}`;
  for (const b of ['#badge-side', '#badge-tab']) $(b).textContent = need || '';
}

function renderTeam() {
  $('#team').innerHTML = db.team.map(a => `<article class="member"><span class="micon">${icon(a.icon)}</span><div><h3>${esc(a.name)}</h3><p>${esc(a.does)}</p><small>Usa ${esc(a.uses)}</small></div></article>`).join('');
  $('#links').innerHTML = db.links.map(l => `<li><span class="led ${l.ok ? 'ok' : 'warn'}"></span><strong>${esc(l.name)}</strong><span>${esc(l.note)}</span></li>`).join('');
}

let month = new Date();
month = new Date(month.getFullYear(), month.getMonth(), 1);
const dkey = d => `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}-${String(d.getDate()).padStart(2, '0')}`;
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

function renderAll() { renderChat(); renderWork(); renderNiko(); }

/* ---------- navigazione ---------- */

const views = ['chat', 'work', 'calendar', 'team'];
function show(name) {
  $$('.view').forEach(v => v.classList.toggle('active', v.id === 'view-' + name));
  $$('.nav [data-view], .tabs [data-view]').forEach(b => {
    b.classList.toggle('active', b.dataset.view === name);
    if (b.dataset.view === name) b.setAttribute('aria-current', 'page'); else b.removeAttribute('aria-current');
  });
  document.body.dataset.view = name;
  if (name === 'chat') $('#feed').scrollTop = $('#feed').scrollHeight;
}

/* ---------- azioni ---------- */

function guess(text) {
  if (kind) return kind;
  if (/blender|3d|scena/i.test(text)) return 'blender';
  if (/hyperframes|animat|titolo|video/i.test(text)) return 'hyperframes';
  return 'idee';
}

function send(text) {
  text = text.trim();
  if (!text) { $('#prompt').focus(); return; }
  show('chat');
  db.messages.push({ from: 'fede', time: now(), text });
  $('#prompt').value = '';
  const k = guess(text);
  const t = {
    id: 'n' + Date.now(), kind: k, project: $('#project').value, state: 'queue', step: 0,
    title: text.length > 60 ? text.slice(0, 57) + '…' : text,
    status: 'In questa anteprima non parte niente. Con il sistema collegato, qui vedresti il lavoro avanzare.',
  };
  db.tasks.unshift(t);
  renderAll();
  setTimeout(() => {
    const who = k === 'idee' ? 'all\'Ideatore' : 'a Produzione';
    db.messages.push({ from: 'niko', time: now(), text: `Ricevuto! Lo passo ${who}. Ti scrivo appena c'è qualcosa da vedere.`, task: t.id });
    renderAll();
  }, calm ? 0 : 700);
}

document.addEventListener('click', e => {
  const b = e.target.closest('button');
  if (!b) return;
  if (b.dataset.view) show(b.dataset.view);
  if (b.dataset.kind) {
    kind = kind === b.dataset.kind ? null : b.dataset.kind;
    $$('[data-kind]').forEach(x => x.setAttribute('aria-pressed', String(x.dataset.kind === kind)));
  }
  if (b.dataset.try) {
    kind = b.dataset.try;
    $$('[data-kind]').forEach(x => x.setAttribute('aria-pressed', String(x.dataset.kind === kind)));
    $('#prompt').value = b.dataset.text;
    $('#prompt').focus();
  }
  if (b.dataset.approve) {
    const t = task(b.dataset.approve);
    const pick = document.querySelector(`#view-${document.body.dataset.view} [data-task="${t.id}"] input:checked`);
    t.state = 'done'; t.step = STEPS[t.kind].length;
    t.status = pick ? `Hai scelto "${t.ideas[pick.value].name}".` : 'Approvato da te.';
    db.messages.push({ from: 'niko', time: now(), text: pick ? `Perfetto, teniamo "${t.ideas[pick.value].name}". Preparo lo script.` : 'Perfetto, approvato.' });
    renderAll();
    toast('Approvato');
  }
  if (b.dataset.changes) {
    const t = task(b.dataset.changes);
    show('chat');
    $('#prompt').value = `Per "${t.title}" vorrei cambiare: `;
    $('#prompt').focus();
  }
  if (b.dataset.copy) {
    const text = task(b.dataset.copy).prompt;
    const fallback = () => { const d = b.closest('.planb').querySelector('details'); d.open = true; getSelection().selectAllChildren(d.querySelector('pre')); toast('Selezionate: premi Cmd+C'); };
    navigator.clipboard ? navigator.clipboard.writeText(text).then(() => toast('Istruzioni copiate'), fallback) : fallback();
  }
  if (b.dataset.resume) {
    const t = task(b.dataset.resume);
    const box = b.closest('.planb').querySelector('textarea');
    if (!box.value.trim()) { toast('Incolla prima la risposta di ChatGPT'); box.focus(); return; }
    t.state = 'work'; t.step = 1; t.status = 'Risposta ricevuta. Ora il Revisore la controlla.';
    db.messages.push({ from: 'niko', time: now(), text: 'Grazie! Ho la risposta, la faccio controllare.' });
    renderAll();
  }
  if (b.dataset.wait) toast('Ok, riprovo da solo quando ChatGPT si libera');
});

$('#composer').addEventListener('submit', e => { e.preventDefault(); send($('#prompt').value); });
$('#prompt').addEventListener('keydown', e => {
  if (e.key === 'Enter' && !e.shiftKey && !e.isComposing) { e.preventDefault(); send($('#prompt').value); }
});
$('#prevmonth').onclick = () => { month.setMonth(month.getMonth() - 1); renderCalendar(); };
$('#nextmonth').onclick = () => { month.setMonth(month.getMonth() + 1); renderCalendar(); };
$('#thismonth').onclick = () => { const d = new Date(); month = new Date(d.getFullYear(), d.getMonth(), 1); renderCalendar(); };
window.addEventListener('hashchange', () => { const v = location.hash.slice(1); if (views.includes(v)) show(v); });

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
renderTeam();
renderCalendar();
show(views.includes(location.hash.slice(1)) ? location.hash.slice(1) : 'chat');
space();
