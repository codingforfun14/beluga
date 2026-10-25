# App di Niko

La finestra di BELUGA: chat con Niko, lavori da approvare, calendario e squadra, in una stanza con lo spazio e i pianeti che si muovono dietro.

Per ora è un'**anteprima della UI con dati di esempio** (`data.js`): non avvia agenti né render. Si apre facendo doppio clic su `index.html`, senza installare niente.

## File

- `index.html`: struttura della pagina.
- `app.css`: stile (palette e font del prototipo approvato, Space Grotesk incluso in `fonts/`).
- `data.js`: dati di esempio. Più avanti verrà sostituito dalle letture del worker sul Mac (`tasks/`, `projects/`).
- `app.js`: comportamento della pagina e animazione dello spazio (canvas, circa 30 fotogrammi al secondo, si ferma quando la scheda non è visibile o se il sistema chiede meno movimento).
- `assets/niko-buddy.webp`: Niko.

## Prossimo passo, dopo l'ok di Fede

Collegare la chat al worker locale, così le richieste di **Idee** e **Video Blender** diventano incarichi veri eseguiti con Claude Code e Codex sugli abbonamenti di Fede.
