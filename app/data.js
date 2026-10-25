'use strict';
// Dati di esempio per l'anteprima della UI.
// Quando il worker sul Mac sarà pronto, queste informazioni arriveranno
// dai file in tasks/ e projects/ invece che da qui.

// Ogni tappa dice anche quale reparto ci sta lavorando
const STEPS = {
  idee: [['Idee', 'ideatore'], ['Controllo', 'revisore'], ['Il tuo ok', 'you']],
  blender: [['Anteprima', 'produzione'], ['Controllo', 'revisore'], ['Il tuo ok', 'you'], ['Video finale', 'produzione'], ['Consegna', 'consegne']],
  hyperframes: [['Anteprima', 'produzione'], ['Controllo', 'revisore'], ['Il tuo ok', 'you'], ['Video finale', 'produzione'], ['Consegna', 'consegne']],
};

const KIND = {
  idee: { label: 'Idee', icon: 'i-spark' },
  blender: { label: 'Blender', icon: 'i-cube' },
  hyperframes: { label: 'HyperFrames', icon: 'i-film' },
};

const STATE = {
  you: 'Serve il tuo ok',
  work: 'In corso',
  stuck: 'Fermo',
  queue: 'In attesa',
  done: 'Finito',
};

const PROJECT = { mezzeuro: 'mezzeuro', motion: 'Libreria motion' };

// I reparti della mappa in Centrale. Niko sta al centro.
const DEPTS = {
  ideatore: { name: 'Ideatore', does: 'Trova idee, scrive testi e storyboard.', uses: 'ChatGPT', icon: 'i-spark' },
  revisore: { name: 'Revisore', does: 'Controlla che sia chiaro, fattibile e in regola.', uses: 'L\'altro modello', icon: 'i-eye' },
  produzione: { name: 'Produzione', does: 'Costruisce il video in Blender o HyperFrames e fa il render.', uses: 'Claude', icon: 'i-cube' },
  consegne: { name: 'Consegne', does: 'Prepara il pacchetto da pubblicare: video, didascalia, data.', uses: 'Niko', icon: 'i-box' },
  libreria: { name: 'Libreria', does: 'Il tuo gusto e i pezzi pronti. L\'Ideatore la legge prima di proporre.', uses: 'Tu', icon: 'i-book' },
};

const SHELVES = [
  { id: 'gusto', name: 'Mi piace', hint: 'Video, post e stili che ti piacciono. L\'Ideatore li usa come riferimento.' },
  { id: 'evita', name: 'Da evitare', hint: 'Cose che non vuoi vedere nelle idee.' },
  { id: 'stile', name: 'Stile mezzeuro', hint: 'Tono, colori, font e regole del canale.' },
  { id: 'pezzi', name: 'Pezzi pronti', hint: 'Modelli Blender, animazioni e suoni da riusare.' },
];

const demo = {
  tasks: [
    {
      id: 't1', kind: 'idee', project: 'mezzeuro', state: 'you', step: 2, version: 1,
      title: 'Idee per il reel ep. 4, Lordo e netto',
      status: 'Le idee sono pronte e controllate. Scegline una.',
      ideas: [
        { name: 'La busta che si sbuccia', line: 'Ogni voce della busta paga toglie uno strato, fino al netto.' },
        { name: 'Dove spariscono 7.000 €', line: 'Un contatore scende mentre passano contributi e tasse.', tip: true },
        { name: 'Due colleghi, due stipendi', line: 'Stesso lordo, netti diversi: le detrazioni con due personaggi.' },
      ],
    },
    {
      id: 't6', kind: 'blender', project: 'mezzeuro', state: 'you', step: 2, version: 2,
      title: 'Logo di mezzeuro che ruota sul tavolo, 4 secondi',
      status: 'Ho rallentato la rotazione come mi avevi chiesto. Il Revisore dice che ora si legge bene.',
      preview: { length: '0:04', size: '720p, leggera' },
      history: ['Versione 01: girava troppo veloce'],
    },
    {
      id: 't2', kind: 'blender', project: 'mezzeuro', state: 'work', step: 0, version: 1,
      title: 'Moneta che cade sul tavolo, 5 secondi',
      status: 'Sto preparando l\'anteprima in Blender.',
      progress: 0.32, detail: '48 di 150 fotogrammi',
    },
    {
      id: 't3', kind: 'idee', project: 'mezzeuro', state: 'stuck', step: 0, version: 1,
      title: 'Hook per il carosello ep. 5',
      status: 'ChatGPT ha raggiunto il limite del tuo piano. Puoi aspettare o farlo a mano.',
      prompt: 'Sei l\'Ideatore di BELUGA per mezzeuro, canale Instagram di educazione finanziaria per ragazzi italiani 18-30 anni. Tono da fratello maggiore, niente promesse di guadagno.\n\nScrivi 5 hook (massimo 10 parole) per la prima slide del carosello ep. 5 "Quanto costa il tuo conto". Per ognuno aggiungi una riga sul perché funziona.\n\nRispondi solo con una lista numerata.',
    },
    {
      id: 't5', kind: 'hyperframes', project: 'motion', state: 'queue', step: 0, version: 1,
      title: 'Titolo che si scrive lettera per lettera',
      status: 'Parte dopo la moneta: sul Mac faccio un lavoro alla volta.',
    },
    {
      id: 't4', kind: 'hyperframes', project: 'mezzeuro', state: 'done', step: 5, version: 3,
      title: 'Reel ep. 3, Fondo emergenze',
      status: 'Versione 03 approvata da te stamattina alle 11:05. È in Consegne.',
    },
  ],

  // Pacchetti pronti da pubblicare. Niko non pubblica da solo: lo fai tu.
  deliveries: [
    {
      id: 'd1', task: 't4', title: 'Reel ep. 3, Fondo emergenze', date: '2026-10-29', where: 'Instagram, reel',
      file: 'reel-ep3-v03.mp4', length: '0:32', version: 3,
      caption: 'Se domani ti si rompe la macchina, da dove prendi i soldi? 🛟\nIl fondo emergenze è la prima cosa da costruire, prima di investire.\nQuanto mettere da parte e dove tenerlo: te lo spiego in 30 secondi.\n\n#mezzeuro #finanzapersonale #risparmio',
      captionOk: false, published: false,
    },
    {
      id: 'd0', title: 'Carosello ep. 3, Fondo emergenze', date: '2026-10-26', where: 'Instagram, carosello',
      file: 'carosello-ep3-v02.zip', length: '8 slide', version: 2,
      caption: 'Il fondo emergenze in 8 slide. Salvalo per quando ti serve. 💾\n\n#mezzeuro #risparmio',
      captionOk: true, published: false,
    },
  ],

  messages: [
    { from: 'niko', time: '14:30', text: 'Ciao Fede! Le idee per l\'ep. 4 sono pronte, e intanto preparo la moneta in Blender.' },
    { from: 'fede', time: '14:30', text: 'Mi servono idee per il reel di mezzeuro ep. 4, lordo e netto.' },
    { from: 'niko', time: '14:31', text: 'Ecco tre idee, già controllate. Ti consiglio la seconda: è la più chiara in 30 secondi.', task: 't1' },
    { from: 'fede', time: '14:35', text: 'Il logo gira troppo veloce, rallentalo.' },
    { from: 'niko', time: '14:38', text: 'Fatto, ecco la versione 02 del logo.', task: 't6' },
    { from: 'fede', time: '14:39', text: 'Fammi in Blender la moneta di mezzeuro che cade sul tavolo, 5 secondi.' },
    { from: 'niko', time: '14:40', text: 'Ci lavoro. Prima ti mostro un\'anteprima leggera: il video finale parte solo quando mi dici ok.', task: 't2' },
    { from: 'niko', time: '14:42', text: 'Gli hook per l\'ep. 5 sono fermi.', task: 't3' },
  ],

  links: [
    { name: 'Il tuo Mac', ok: true, note: 'Acceso e pronto' },
    { name: 'Claude', ok: true, note: 'Collegato con il tuo abbonamento' },
    { name: 'ChatGPT', ok: false, note: 'Limite del piano raggiunto, riprova più tardi' },
  ],

  // La libreria parte quasi vuota: la riempiamo insieme.
  library: [
    { shelf: 'stile', text: 'Tono da fratello maggiore. Niente promesse di guadagno.' },
  ],

  events: [
    { date: '2026-10-26', title: 'Carosello ep. 3', type: 'out' },
    { date: '2026-10-29', title: 'Reel ep. 3', type: 'out' },
    { date: '2026-11-02', title: 'Carosello ep. 4', type: 'out' },
    { date: '2026-11-05', title: 'Reel ep. 4', type: 'out' },
    { date: '2026-11-08', title: 'Controllo', type: 'check' },
    { date: '2026-11-09', title: 'Carosello ep. 5', type: 'out' },
    { date: '2026-11-12', title: 'Reel ep. 5', type: 'out' },
    { date: '2026-11-16', title: 'Carosello ep. 6', type: 'out' },
    { date: '2026-11-19', title: 'Reel ep. 6', type: 'out' },
    { date: '2026-11-22', title: 'Controllo', type: 'check' },
    { date: '2026-11-23', title: 'Carosello ep. 7', type: 'out' },
    { date: '2026-11-26', title: 'Reel ep. 7', type: 'out' },
  ],
};
