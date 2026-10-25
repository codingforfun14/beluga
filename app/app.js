'use strict';
const $ = s => document.querySelector(s);
const $$ = s => [...document.querySelectorAll(s)];
const esc = s => String(s).replace(/[&<>"']/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' })[c]);
const icon = n => `<svg aria-hidden="true"><use href="#${n}"/></svg>`;
const now = () => new Date().toLocaleTimeString('it-IT', { hour: '2-digit', minute: '2-digit' });

const db = structuredClone(demo);
const findTask = id => db.tasks.find(t => t.id === id);
const findPreview = id => db.previews.find(p => p.id === id);
let mode = 'auto';
let taskFilter = 'tutti';

function toast(text) {
  const el = $('#toast');
  el.textContent = text;
  el.classList.add('show');
  clearTimeout(toast.timer);
  toast.timer = setTimeout(() => el.classList.remove('show'), 3200);
}

function badge(state) {
  const s = STATES[state];
  return `<span class="badge ${s.tone}">${s.label}</span>`;
}

function taskCard(t) {
  const k = KINDS[t.kind];
  const steps = t.steps.map(s => `<span class="step ${STATES[s.state].tone}">${esc(s.agent)} <i>${esc(s.runner)}</i></span>`).join('<span class="stepsep">→</span>');
  const bar = t.progress
    ? `<div class="progress"><div style="width:${Math.round(t.progress.done / t.progress.total * 100)}%"></div></div><div class="progresslabel">${t.progress.done} di ${t.progress.total} ${t.progress.unit}</div>`
    : '';
  return `<article class="task" data-task="${t.id}">
    <header>${icon(k.icon)}<span>${k.label} · ${esc(PROJECTS[t.project])}</span>${badge(t.state)}</header>
    <h3>${esc(t.title)}</h3>
    <div class="steps">${steps}</div>
    ${bar}
    ${t.note ? `<p class="note">${esc(t.note)}</p>` : ''}
    <footer><span>${t.id}</span><span>agg. ${t.updated}</span></footer>
  </article>`;
}

function stage(p) {
  // Segnaposto visivo finché il worker non manda il vero fotogramma
  const kind = p.kind === 'blender' ? 'coin' : 'type';
  return `<div class="stage ${kind}"><div class="stageart"></div><span class="framecount">${esc(p.frame)}</span></div>`;
}

function previewActions(p) {
  if (p.state === 'attesa') {
    return `<div class="actions"><button class="primary" data-approve="${p.id}">${icon('i-check')}Approva</button><button class="ghost" data-changes="${p.id}">Chiedi modifiche</button></div>`;
  }
  if (p.state === 'fatto') return `<div class="actions"><span class="approved">${icon('i-check')}Approvato</span></div>`;
  return `<div class="actions"><span class="working"><span class="pulse"></span>In lavorazione</span></div>`;
}

function previewCard(p) {
  let body;
  if (p.kind === 'idee') {
    body = `<ol class="ideas">${p.ideas.map((i, n) => `<li><label><input type="radio" name="pick-${p.id}" value="${n}" ${n === 1 ? 'checked' : ''} ${p.state !== 'attesa' ? 'disabled' : ''}><span><strong>${esc(i.name)}</strong>${esc(i.line)}</span></label></li>`).join('')}</ol>
      <p class="review">${icon('i-check')}${esc(p.review)}</p>`;
  } else {
    body = `${stage(p)}<p class="note">${esc(p.note)}</p>`;
  }
  return `<article class="preview" data-preview="${p.id}">
    <header>${icon(KINDS[p.kind].icon)}<span>${esc(p.title)}</span>${badge(p.state)}</header>
    ${body}
    ${previewActions(p)}
  </article>`;
}

function planBCard(t) {
  return `<article class="planb" data-planb="${t.id}">
    <header>${icon('i-alert')}<span>Piano B · ${esc(t.title)}</span></header>
    <p>Incolla questo prompt in ChatGPT, poi incolla qui sotto la risposta. Il lavoro riprende dallo stesso punto.</p>
    <div class="promptbox"><pre>${esc(t.prompt)}</pre><button class="ghost small" data-copy="${t.id}">${icon('i-copy')}Copia</button></div>
    <label class="sr" for="answer-${t.id}">Risposta di ChatGPT</label>
    <textarea id="answer-${t.id}" rows="3" placeholder="Incolla qui la risposta di ChatGPT"></textarea>
    <div class="actions"><button class="primary" data-resume="${t.id}">Continua</button><button class="ghost" data-wait="${t.id}">Aspetta che si liberi</button></div>
  </article>`;
}

function messageHTML(m) {
  const who = m.role === 'user' ? 'FEDE' : 'NIKO';
  const tag = m.mode && m.mode !== 'auto' ? `<span class="modetag">${KINDS[m.mode].label}</span>` : '';
  let extra = '';
  if (m.task) extra = taskCard(findTask(m.task));
  if (m.preview) extra = previewCard(findPreview(m.preview));
  if (m.planB) extra = planBCard(findTask(m.planB));
  return `<div class="msg ${m.role === 'user' ? 'user' : 'bot'}">
    <span class="avatar">${m.role === 'user' ? 'F' : 'n_'}</span>
    <div class="msgbody"><div class="meta">${who}${tag}<time>${m.time}</time></div>
    <p>${esc(m.text)}</p>${extra}</div>
  </div>`;
}

function renderMessages() {
  $('#messages').innerHTML = db.messages.map(messageHTML).join('');
  $('#feed').scrollTop = $('#feed').scrollHeight;
}

function renderTasks() {
  const filters = { tutti: 'Tutti', attesa: 'Aspetta te', corso: 'In corso', pianob: 'Piano B', coda: 'In coda', fatto: 'Fatti' };
  $('#taskfilters').innerHTML = Object.entries(filters).map(([k, v]) => `<button class="chip ${k === taskFilter ? 'on' : ''}" data-filter="${k}">${v}</button>`).join('');
  const list = db.tasks.filter(t => taskFilter === 'tutti' || t.state === taskFilter || (taskFilter === 'corso' && t.state === 'revisione'));
  $('#tasklist').innerHTML = list.length ? list.map(taskCard).join('') : '<p class="empty">Nessun incarico in questo stato.</p>';
}

function renderPreviews() {
  const order = { attesa: 0, corso: 1, fatto: 2 };
  $('#previewgrid').innerHTML = [...db.previews].sort((a, b) => order[a.state] - order[b.state]).map(previewCard).join('');
}

function renderTeam() {
  $('#teamgrid').innerHTML = db.team.map(a => `<article class="agent">
    <div class="agenticon">${icon(a.icon)}</div>
    <h3>${esc(a.name)}</h3><p>${esc(a.role)}</p>
    <div class="runner">Gira su <b>${esc(a.runner)}</b></div>
    <div class="skills">${a.skills.map(s => `<span>${esc(s)}</span>`).join('')}</div>
  </article>`).join('');
}

let month = new Date();
month = new Date(month.getFullYear(), month.getMonth(), 1);
const dkey = d => `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}-${String(d.getDate()).padStart(2, '0')}`;

function renderCalendar() {
  $('#monthlabel').textContent = month.toLocaleDateString('it-IT', { month: 'long', year: 'numeric' });
  const head = ['Lun', 'Mar', 'Mer', 'Gio', 'Ven', 'Sab', 'Dom'].map(d => `<div class="wd">${d}</div>`).join('');
  const offset = (month.getDay() + 6) % 7;
  const days = new Date(month.getFullYear(), month.getMonth() + 1, 0).getDate();
  const total = Math.ceil((offset + days) / 7) * 7;
  const today = dkey(new Date());
  let cells = '';
  for (let i = 0; i < total; i++) {
    const d = i - offset + 1;
    if (d < 1 || d > days) { cells += '<div class="day out"></div>'; continue; }
    const key = dkey(new Date(month.getFullYear(), month.getMonth(), d));
    const ev = db.events.filter(e => e.date === key).map(e => `<span class="ev ${e.type}">${esc(e.title)}</span>`).join('');
    cells += `<div class="day ${key === today ? 'today' : ''}"><b>${d}</b>${ev}</div>`;
  }
  $('#calendar').innerHTML = head + cells;
}

function renderSide() {
  $('#connections').innerHTML = db.connections.map(c => `<li><span class="led ${c.state}"></span>${esc(c.name)}<small>${esc(c.note)}</small></li>`).join('');
  const open = db.tasks.filter(t => ['coda', 'corso', 'revisione'].includes(t.state));
  const waiting = db.previews.filter(p => p.state === 'attesa').length;
  const planB = db.tasks.filter(t => t.state === 'pianob').length;
  $('#count-tasks').textContent = open.length + planB || '';
  $('#count-previews').textContent = waiting || '';
  const working = db.tasks.filter(t => ['corso', 'revisione'].includes(t.state)).length;
  $('#nikostatus').textContent = working ? `Sto lavorando a ${working} ${working === 1 ? 'incarico' : 'incarichi'}` : 'Pronto, socio';
  const subs = [];
  if (waiting) subs.push(`${waiting} ${waiting === 1 ? 'anteprima aspetta' : 'anteprime aspettano'} il tuo ok`);
  if (planB) subs.push(`${planB} in piano B`);
  $('#nikosub').textContent = subs.join(' · ') || 'Nessuna attesa';
  $('#now').innerHTML = '<div class="eyebrow">ADESSO</div>' + db.tasks.filter(t => t.state !== 'fatto').map(t => `<button class="nowrow" data-goto="${t.id}">${icon(KINDS[t.kind].icon)}<span>${esc(t.title)}${t.progress ? `<i style="--p:${Math.round(t.progress.done / t.progress.total * 100)}%"></i>` : ''}</span>${badge(t.state)}</button>`).join('');
}

function renderAll() {
  renderMessages();
  renderTasks();
  renderPreviews();
  renderSide();
}

const crumbs = { chat: 'chat', tasks: 'incarichi', previews: 'anteprime', calendar: 'calendario', team: 'squadra' };
function showView(name) {
  $$('.view').forEach(v => v.classList.toggle('active', v.id === 'view-' + name));
  $$('[data-view]').forEach(b => {
    const on = b.dataset.view === name;
    b.classList.toggle('active', on);
    if (on) b.setAttribute('aria-current', 'page'); else b.removeAttribute('aria-current');
  });
  $('#crumb').textContent = crumbs[name];
  $('#sidebar').classList.remove('open');
  document.body.dataset.view = name;
}

function guessKind(text) {
  if (mode !== 'auto') return mode;
  if (/blender|3d|scena|modello/i.test(text)) return 'blender';
  if (/hyperframes|animatic|reel|video/i.test(text)) return 'hyperframes';
  return 'idee';
}

function send(text) {
  text = text.trim();
  if (!text) return;
  showView('chat');
  db.messages.push({ role: 'user', time: now(), mode, text });
  $('#prompt').value = '';
  const kind = guessKind(text);
  const project = $('#project').value;
  const agent = kind === 'idee' ? { agent: 'Ideatore', runner: 'Codex' } : { agent: 'Produzione', runner: 'Claude Code' };
  const t = {
    id: 't-' + String(Math.max(...db.tasks.map(x => Number(x.id.slice(2)))) + 1).padStart(4, '0'), kind, project, state: 'coda',
    title: text.length > 70 ? text.slice(0, 67) + '…' : text,
    steps: [{ ...agent, state: 'coda' }],
    note: 'Anteprima UI: l\'incarico è finto e non parte niente.', updated: now(),
  };
  db.tasks.unshift(t);
  renderAll();
  setTimeout(() => {
    db.messages.push({ role: 'niko', time: now(), text: `Ricevuto. Lo passo a ${agent.agent} per ${PROJECTS[project]}. Ti scrivo appena c'è qualcosa da vedere.`, task: t.id });
    renderAll();
  }, 500);
}

document.addEventListener('click', e => {
  const b = e.target.closest('button');
  if (!b) return;
  if (b.dataset.view) showView(b.dataset.view);
  if (b.dataset.mode) {
    mode = b.dataset.mode;
    $$('[data-mode]').forEach(x => x.setAttribute('aria-checked', String(x === b)));
    $('#prompt').placeholder = { auto: 'Parla con Niko. Che cosa creiamo?', idee: 'Che idee ti servono? Per quale episodio o progetto?', blender: 'Descrivi la scena: soggetto, durata, camera, luce.', hyperframes: 'Descrivi il video: testo, durata, stile.' }[mode];
    $('#prompt').focus();
  }
  if (b.dataset.filter) { taskFilter = b.dataset.filter; renderTasks(); }
  if (b.dataset.approve) {
    const p = findPreview(b.dataset.approve);
    const pick = document.querySelector(`[data-preview="${p.id}"] input:checked`);
    p.state = 'fatto';
    findTask(p.task).state = 'fatto';
    const chosen = p.ideas && pick ? ` Tengo "${p.ideas[pick.value].name}".` : '';
    db.messages.push({ role: 'niko', time: now(), text: `Approvato.${chosen} Lo segno nel progetto e preparo il passo successivo.` });
    renderAll();
    toast('Approvato (anteprima UI: nessun lavoro avviato)');
  }
  if (b.dataset.changes) {
    const p = findPreview(b.dataset.changes);
    showView('chat');
    $('#prompt').value = `Modifiche per "${p.title}": `;
    $('#prompt').focus();
  }
  if (b.dataset.copy) {
    navigator.clipboard?.writeText(findTask(b.dataset.copy).prompt).then(() => toast('Prompt copiato'), () => toast('Copia non riuscita: selezionalo a mano'));
  }
  if (b.dataset.resume) {
    const t = findTask(b.dataset.resume);
    const answer = $('#answer-' + t.id).value.trim();
    if (!answer) { toast('Incolla prima la risposta di ChatGPT'); return; }
    t.state = 'revisione';
    t.steps = [{ agent: 'Ideatore', runner: 'manuale', state: 'fatto' }, { agent: 'Revisore', runner: 'Claude Code', state: 'revisione' }];
    t.note = 'Risposta incollata a mano. Ora la controlla il Revisore.';
    t.updated = now();
    db.messages = db.messages.filter(m => m.planB !== t.id);
    db.messages.push({ role: 'niko', time: now(), text: 'Grazie, ho la risposta. La passo al Revisore.', task: t.id });
    renderAll();
  }
  if (b.dataset.wait) toast('Ok, riprovo da solo quando il piano si libera');
  if (b.dataset.goto) { showView('tasks'); taskFilter = 'tutti'; renderTasks(); document.querySelector(`#tasklist [data-task="${b.dataset.goto}"]`)?.scrollIntoView({ block: 'center' }); }
});

$('#composer').addEventListener('submit', e => { e.preventDefault(); send($('#prompt').value); });
$('#prompt').addEventListener('keydown', e => {
  if (e.key === 'Enter' && !e.shiftKey && !e.isComposing) { e.preventDefault(); send($('#prompt').value); }
});
$('#menubtn').onclick = () => $('#sidebar').classList.toggle('open');
document.addEventListener('keydown', e => { if (e.key === 'Escape') $('#sidebar').classList.remove('open'); });
$('#prevmonth').onclick = () => { month.setMonth(month.getMonth() - 1); renderCalendar(); };
$('#nextmonth').onclick = () => { month.setMonth(month.getMonth() + 1); renderCalendar(); };
$('#thismonth').onclick = () => { const d = new Date(); month = new Date(d.getFullYear(), d.getMonth(), 1); renderCalendar(); };

renderAll();
renderTeam();
renderCalendar();
showView(location.hash.slice(1) in crumbs ? location.hash.slice(1) : 'chat');
window.addEventListener('hashchange', () => { const v = location.hash.slice(1); if (v in crumbs) showView(v); });
