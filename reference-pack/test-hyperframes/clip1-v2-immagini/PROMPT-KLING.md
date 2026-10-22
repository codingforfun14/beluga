# Clip 1 v2: immagini Kling (niente video)

Il montaggio è pronto in `index.html` e gira con immagini segnaposto (scritta rossa SEGNAPOSTO). Basta sostituire i file in `assets/k/` con quelli di Kling, stessi nomi, e rifare il render.

Regole per tutte: Kling Image, 9:16, 2K. Genera prima `foto.png`, poi usala come immagine di riferimento (subject reference) per tutte le altre, così il prodotto resta identico. Niente testo nelle immagini: il titolo lo aggiungo io.

| File | Prompt |
|---|---|
| `foto.png` | Hyperreal studio product photograph of a minimalist smartphone seen from the back, transparent glass back revealing neatly arranged internal components, matte white aluminium frame, two round camera lenses top left, a thin red LED strip, centred in the frame, light grey seamless background, hard top light, soft contact shadow, crisp reflections, commercial packshot, no text |
| `ang1.png` | Same smartphone as the reference, three-quarter view from the left, same studio, same light, dark charcoal seamless background, centred, no text |
| `ang2.png` | Same smartphone, pure side profile showing the thin frame and buttons, same studio light, dark charcoal background, centred, no text |
| `ang3.png` | Same smartphone, three-quarter view from the right, slightly from above, dark charcoal background, centred, no text |
| `xray.png` | X-ray scan of the same smartphone from the back, same framing as ang1, black background, internal parts glowing white and pale blue: chip, wireless charging coil, battery, screws and flex cables, monochrome, fine film grain, medical scan look, no text |
| `strato1.png` | Exploded-view component only: the transparent back glass panel with the camera ring, isolated on pure black, top-down orthographic, glowing white edges, no text |
| `strato2.png` | Component only: the wireless charging copper coil with flex cable, isolated on pure black, top-down orthographic, no text |
| `strato3.png` | Component only: the motherboard with the main chip and screws, isolated on pure black, top-down orthographic, no text |
| `strato4.png` | Component only: the flat battery pack, isolated on pure black, top-down orthographic, no text |

Negative per tutte: text, logo, watermark, hands, extra phones, blurry, low detail.

Strati: se lo sfondo nero non basta, ritaglio con rembg (`rembg i strato1.png strato1.png`).

## Cosa fa il montaggio
- 0–1.7 s: angolo 1, la linea di scansione rivela la versione a raggi X sopra la foto, glitch.
- 1.7–2.2 s: finta rotazione: whip con motion blur tra ang1, ang2, ang3, taglio sul picco del blur.
- 2.2–3.7 s: esploso: i 4 strati si aprono in 2.5D con etichette.
- 3.7 s: flash bianco, poi packshot `foto.png` con riflesso che scorre, titolo a matrice di punti e "Vedi attraverso."

Render: `npx hyperframes render --quality looks --output clip1-v2.mp4` (sul Mac prima `nvm use 22`).
