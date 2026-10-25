'use strict';
// Dati di esempio per l'anteprima della UI.
// Quando il worker sul Mac sarà pronto, queste informazioni arriveranno
// dai file in tasks/ e projects/ invece che da qui.

const STEPS = {
  idee: ['Idee', 'Controllo', 'Il tuo ok'],
  blender: ['Scena', 'Anteprima', 'Il tuo ok', 'Video finale'],
  hyperframes: ['Animazione', 'Anteprima', 'Il tuo ok', 'Video finale'],
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

const demo = {
  tasks: [
    {
      id: 't1', kind: 'idee', project: 'mezzeuro', state: 'you', step: 2,
      title: 'Idee per il reel ep. 4, Lordo e netto',
      status: 'Le idee sono pronte e controllate. Scegline una.',
      ideas: [
        { name: 'La busta che si sbuccia', line: 'Ogni voce della busta paga toglie uno strato, fino al netto.' },
        { name: 'Dove spariscono 7.000 €', line: 'Un contatore scende mentre passano contributi e tasse.', tip: true },
        { name: 'Due colleghi, due stipendi', line: 'Stesso lordo, netti diversi: le detrazioni con due personaggi.' },
      ],
    },
    {
      id: 't2', kind: 'blender', project: 'mezzeuro', state: 'work', step: 1,
      title: 'Moneta che cade sul tavolo, 5 secondi',
      status: 'Sto preparando l\'anteprima in Blender.',
      progress: 0.32, detail: '48 di 150 fotogrammi',
    },
    {
      id: 't3', kind: 'idee', project: 'mezzeuro', state: 'stuck', step: 0,
      title: 'Hook per il carosello ep. 5',
      status: 'ChatGPT ha raggiunto il limite del tuo piano. Puoi aspettare o farlo a mano.',
      prompt: 'Sei l\'Ideatore di BELUGA per mezzeuro, canale Instagram di educazione finanziaria per ragazzi italiani 18-30 anni. Tono da fratello maggiore, niente promesse di guadagno.\n\nScrivi 5 hook (massimo 10 parole) per la prima slide del carosello ep. 5 "Quanto costa il tuo conto". Per ognuno aggiungi una riga sul perché funziona.\n\nRispondi solo con una lista numerata.',
    },
    {
      id: 't5', kind: 'hyperframes', project: 'motion', state: 'queue', step: 0,
      title: 'Titolo che si scrive lettera per lettera',
      status: 'Parte dopo la moneta: sul Mac faccio un lavoro alla volta.',
    },
    {
      id: 't4', kind: 'hyperframes', project: 'mezzeuro', state: 'done', step: 4,
      title: 'Animatic del reel ep. 3, Fondo emergenze',
      status: 'Approvato da te stamattina alle 11:05.',
    },
  ],

  messages: [
    { from: 'niko', time: '14:30', text: 'Ciao Fede! Le idee per l\'ep. 4 sono pronte, e intanto preparo la moneta in Blender.' },
    { from: 'fede', time: '14:30', text: 'Mi servono idee per il reel di mezzeuro ep. 4, lordo e netto.' },
    { from: 'niko', time: '14:31', text: 'Ecco tre idee, già controllate. Ti consiglio la seconda: è la più chiara in 30 secondi.', task: 't1' },
    { from: 'fede', time: '14:39', text: 'Fammi in Blender la moneta di mezzeuro che cade sul tavolo, 5 secondi.' },
    { from: 'niko', time: '14:40', text: 'Ci lavoro. Prima ti mostro un\'anteprima leggera: il video finale parte solo quando mi dici ok.', task: 't2' },
    { from: 'niko', time: '14:42', text: 'Gli hook per l\'ep. 5 sono fermi.', task: 't3' },
  ],

  team: [
    { name: 'Niko', does: 'Parla con te, passa il lavoro agli altri e ti mostra i risultati.', uses: 'Claude', icon: 'i-chat' },
    { name: 'Ideatore', does: 'Trova idee, scrive testi e storyboard.', uses: 'ChatGPT', icon: 'i-spark' },
    { name: 'Revisore', does: 'Controlla che il lavoro sia chiaro, fattibile e in regola.', uses: 'L\'altro modello rispetto a chi ha scritto', icon: 'i-check' },
    { name: 'Produzione', does: 'Costruisce il video in Blender o HyperFrames, fa il render e pulisce i file.', uses: 'Claude', icon: 'i-cube' },
  ],

  links: [
    { name: 'Il tuo Mac', ok: true, note: 'Acceso e pronto' },
    { name: 'Claude', ok: true, note: 'Collegato con il tuo abbonamento' },
    { name: 'ChatGPT', ok: false, note: 'Limite del piano raggiunto, riprova più tardi' },
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
