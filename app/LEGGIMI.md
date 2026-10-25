# App di Niko

La finestra di BELUGA, in una stanza con lo spazio e i pianeti che si muovono dietro. Le pagine:

- **Centrale**: Niko al centro e i reparti intorno (Ideatore, Revisore, Produzione, Consegne, Libreria). Le linee si accendono quando un reparto lavora.
- **Chat**: la conversazione con Niko. La barra per scrivergli resta in basso su ogni pagina.
- **Lavori**: in alto quello che aspetta Fede, sotto i lavori divisi per reparto. Si approva sempre una versione precisa (v01, v02…).
- **Consegne**: il pacchetto pronto da pubblicare (video finale, didascalia, dove e quando). Niko non pubblica da solo.
- **Libreria**: il gusto di Fede e i pezzi pronti, che l'Ideatore legge prima di proporre. Per ora si salva solo nel browser.
- **Calendario**: le uscite di mezzeuro e i controlli del piano.

Per ora è un'**anteprima della UI con dati di esempio** (`data.js`): non avvia agenti né render. Si apre facendo doppio clic su `index.html`, senza installare niente.

## File

- `index.html`: struttura della pagina.
- `app.css`: stile (palette e font del prototipo approvato, Space Grotesk incluso in `fonts/`).
- `data.js`: dati di esempio. Più avanti verrà sostituito dalle letture del worker sul Mac (`tasks/`, `projects/`).
- `app.js`: comportamento della pagina e animazione dello spazio (canvas, circa 30 fotogrammi al secondo, si ferma quando la scheda non è visibile o se il sistema chiede meno movimento).
- `assets/niko-buddy.webp`: Niko.

## Prossimo passo, dopo l'ok di Fede

Collegare la chat al worker locale, così le richieste di **Idee** e **Video Blender** diventano incarichi veri eseguiti con Claude Code e Codex sugli abbonamenti di Fede.
