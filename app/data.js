'use strict';
// Dati di esempio per l'anteprima della UI.
// Quando il worker sul Mac sarà pronto, queste funzioni leggeranno i file
// in tasks/ e projects/ tramite il worker locale invece di questi oggetti.

const STATES = {
  coda: { label: 'In coda', tone: 'idle' },
  corso: { label: 'In corso', tone: 'work' },
  revisione: { label: 'In revisione', tone: 'work' },
  attesa: { label: 'Aspetta te', tone: 'you' },
  pianob: { label: 'Piano B', tone: 'warn' },
  fatto: { label: 'Fatto', tone: 'done' },
  fallito: { label: 'Fallito', tone: 'bad' },
};

const KINDS = {
  idee: { label: 'Idee', icon: 'i-spark' },
  blender: { label: 'Video Blender', icon: 'i-cube' },
  hyperframes: { label: 'Video HyperFrames', icon: 'i-film' },
};

const PROJECTS = { mezzeuro: 'mezzeuro', motion: 'Libreria motion', ferrari: 'Ferrari 488' };

const demo = {
  connections: [
    { name: 'Worker sul Mac', state: 'ok', note: 'attivo' },
    { name: 'Claude Code', state: 'ok', note: 'pronto' },
    { name: 'Codex (ChatGPT)', state: 'warn', note: 'tetto del piano' },
  ],

  tasks: [
    {
      id: 't-0412', kind: 'idee', project: 'mezzeuro', state: 'attesa',
      title: 'Tre idee per il reel ep. 4, Lordo e netto',
      steps: [
        { agent: 'Ideatore', runner: 'Codex', state: 'fatto' },
        { agent: 'Revisore', runner: 'Claude Code', state: 'fatto' },
      ],
      preview: 'p-0412', updated: '14:31',
    },
    {
      id: 't-0413', kind: 'blender', project: 'mezzeuro', state: 'corso',
      title: 'La moneta di mezzeuro cade sul tavolo, 5 s',
      steps: [{ agent: 'Produzione', runner: 'Claude Code', state: 'corso' }],
      progress: { done: 48, total: 150, unit: 'fotogrammi' },
      note: 'Anteprima 720p con Eevee. Il render finale aspetta il tuo ok.',
      updated: '14:40',
    },
    {
      id: 't-0414', kind: 'idee', project: 'mezzeuro', state: 'pianob',
      title: 'Cinque hook per il carosello ep. 5',
      steps: [{ agent: 'Ideatore', runner: 'Codex', state: 'pianob' }],
      note: 'Codex ha raggiunto il tetto del piano. Prompt pronto da incollare.',
      prompt: 'Sei l\'Ideatore di BELUGA per mezzeuro, canale Instagram di educazione finanziaria per ragazzi italiani 18-30 anni. Tono da fratello maggiore, niente promesse di guadagno.\n\nScrivi 5 hook (massimo 10 parole) per la prima slide del carosello ep. 5 "Quanto costa il tuo conto". Per ognuno aggiungi una riga sul perché funziona.\n\nRispondi solo con una lista numerata.',
      updated: '14:42',
    },
    {
      id: 't-0408', kind: 'hyperframes', project: 'mezzeuro', state: 'fatto',
      title: 'Animatic del reel ep. 3, Fondo emergenze',
      steps: [{ agent: 'Produzione', runner: 'Claude Code', state: 'fatto' }],
      preview: 'p-0408', note: 'Approvato da te alle 11:05.', updated: '11:05',
    },
    {
      id: 't-0415', kind: 'hyperframes', project: 'motion', state: 'coda',
      title: 'Pratica: titolo che si costruisce lettera per lettera',
      steps: [{ agent: 'Produzione', runner: 'Claude Code', state: 'coda' }],
      note: 'Parte dopo la moneta: un lavoro alla volta sul Mac.', updated: '14:44',
    },
  ],

  previews: [
    {
      id: 'p-0412', task: 't-0412', kind: 'idee', state: 'attesa',
      title: 'Tre idee per il reel ep. 4',
      review: 'Il Revisore consiglia la 2: è la più chiara in 30 secondi.',
      ideas: [
        { name: 'La busta che si sbuccia', line: 'La RAL è un frutto: ogni voce toglie una buccia fino al netto.' },
        { name: 'Dove spariscono 7.000 €', line: 'Un contatore scende in tempo reale mentre passano INPS e IRPEF.' },
        { name: 'Due colleghi, due stipendi', line: 'Stessa RAL, netti diversi: le detrazioni spiegate con due personaggi.' },
      ],
    },
    {
      id: 'p-0413', task: 't-0413', kind: 'blender', state: 'corso',
      title: 'Moneta sul tavolo, anteprima 720p',
      frame: '48 / 150', note: 'Primi fotogrammi del blockout, luci provvisorie.',
    },
    {
      id: 'p-0408', task: 't-0408', kind: 'hyperframes', state: 'fatto',
      title: 'Animatic reel ep. 3', frame: '35 s', note: 'Approvato. Il render finale è in archivio.',
    },
  ],

  messages: [
    { role: 'niko', time: '14:30', text: 'Ciao Fede. Ho due lavori in corso e uno che aspetta te.' },
    { role: 'user', time: '14:30', mode: 'idee', text: 'Tre idee per il reel di mezzeuro ep. 4, lordo e netto.' },
    { role: 'niko', time: '14:30', text: 'Ci pensa l\'Ideatore su Codex, poi il Revisore controlla con Claude.', task: 't-0412' },
    { role: 'niko', time: '14:31', text: 'Le tre idee sono pronte e revisionate. Quale tieni?', preview: 'p-0412' },
    { role: 'user', time: '14:39', mode: 'blender', text: 'Fammi in Blender la moneta di mezzeuro che cade sul tavolo, 5 secondi.' },
    { role: 'niko', time: '14:40', text: 'Passo a Produzione: Claude Code segue la skill Blender e ti mostra prima un\'anteprima leggera. Il render finale parte solo dopo il tuo ok.', task: 't-0413' },
    { role: 'niko', time: '14:42', text: 'Codex non risponde per gli hook dell\'ep. 5: il piano ha raggiunto il tetto. Puoi usare il piano B, oppure aspetto che si liberi.', planB: 't-0414' },
  ],

  team: [
    { name: 'Niko', role: 'Coordina e ti mostra le anteprime', runner: 'Claude Code', icon: 'i-chat', skills: ['smistamento', 'anteprime e feedback', 'calendario'] },
    { name: 'Ideatore', role: 'Concept, testi, storyboard e reference', runner: 'Codex (ChatGPT)', icon: 'i-spark', skills: ['concept-reel', 'storyboard', 'hook-social'] },
    { name: 'Revisore', role: 'Coerenza, fattibilità e licenze', runner: 'Il modello che non ha scritto', icon: 'i-check', skills: ['controllo-coerenza', 'licenze-asset', 'regole-mezzeuro'] },
    { name: 'Produzione', role: 'Costruisce, renderizza, verifica e pulisce', runner: 'Claude Code', icon: 'i-cube', skills: ['blender-scena', 'hyperframes-reel', 'render-e-pulizia'] },
  ],

  events: [
    { date: '2026-10-26', title: 'Carosello ep. 3', type: 'out' },
    { date: '2026-10-29', title: 'Reel ep. 3', type: 'out' },
    { date: '2026-11-02', title: 'Carosello ep. 4', type: 'out' },
    { date: '2026-11-05', title: 'Reel ep. 4', type: 'out' },
    { date: '2026-11-08', title: 'Controllo: 5 prove', type: 'check' },
    { date: '2026-11-09', title: 'Carosello ep. 5', type: 'out' },
    { date: '2026-11-12', title: 'Reel ep. 5', type: 'out' },
    { date: '2026-11-16', title: 'Carosello ep. 6', type: 'out' },
    { date: '2026-11-19', title: 'Reel ep. 6', type: 'out' },
    { date: '2026-11-22', title: 'Controllo: primo reel', type: 'check' },
    { date: '2026-11-23', title: 'Carosello ep. 7', type: 'out' },
    { date: '2026-11-26', title: 'Reel ep. 7', type: 'out' },
  ],
};
