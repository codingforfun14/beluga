# App di Niko

La finestra di BELUGA: chat con Niko, incarichi, anteprime, calendario e squadra.

Per ora è un'**anteprima della UI con dati di esempio** (`data.js`): non avvia agenti né render. Si apre facendo doppio clic su `index.html`, senza installare niente.

## File

- `index.html`: struttura della pagina.
- `app.css`: stile (palette e font del prototipo approvato, Space Grotesk incluso in `fonts/`).
- `data.js`: dati di esempio. Più avanti verrà sostituito dalle letture del worker sul Mac (`tasks/`, `projects/`).
- `app.js`: comportamento della pagina.
- `assets/niko-buddy.webp`: Niko.

## Prossimo passo, dopo l'ok di Fede

Collegare la chat al worker locale, così le richieste di **Idee** e **Video Blender** diventano incarichi veri eseguiti con Claude Code e Codex sugli abbonamenti di Fede.
