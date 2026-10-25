# Test A "La spunta che viaggia" (11 s)

Test per PRATICA (brand inventato), fatto solo in HyperFrames nel cloud: il Mac di fede non è stato usato. 1920×1080, 60 fps, render in 36 s.

## Da quali reference (analisi in `focus/3d-motion/analisi/`)
- **Housing.com "Look Up"**: un solo simbolo del logo che viaggia per tutto il film, senza tagli netti.
- **Intel**: il quadratino del logo fa da cursore dentro l'interfaccia.
- **Burger King**: parole enormi a tempo, una ogni 0,6 s.
- **Google Gemini**: zoom dentro l'elemento della UI per cambiare mondo.

## Scaletta
| s | Cosa succede | Transizione |
|---|---|---|
| 0–2,6 | modulo "Dichiarazione 730": la spunta arancione fa da cursore, scende riga per riga, ogni riga si riempie e lascia una spunta, contatore 0/5 → 5/5 | — |
| 2,6–3,5 | la spunta va al centro e ci si entra dentro: lo schermo diventa arancione | zoom attraverso l'oggetto |
| 3,6–6 | "730." "BOLLETTE." "RICORSI." "FATTO." a 0,6 s l'una | colpi a tempo |
| 6–7,6 | l'arancione si richiude nella spunta, che diventa l'icona della notifica "Pratica inviata · 730 · in 3 minuti" | iris al contrario |
| 7,6–11 | la spunta scivola e diventa il logo, "PRATICA" si scrive lettera per lettera, poi il claim | carry across |

## Suono
Effetti già nel progetto (`assets/sfx`, crediti in `CREDITS.md`): pop su ogni spunta, whoosh sugli spostamenti, colpo basso su "730." e "FATTO.". Mix normalizzato a −14 LUFS, picco −1,5 dBTP. Niente musica.

## Cosa migliorare
- Serve una musica con melodia sotto (Lemon), non solo effetti.
- Le parole arancioni sono tutte uguali: una variazione (una parola in nero, o una che entra in modo diverso) darebbe più ritmo.
- La notifica resta a schermo 1,1 s: per leggerla tutta servirebbero circa 1,7 s.
