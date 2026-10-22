# 05 · Disegnato a mano

Per quando il brief dice: tono umano, artigianale, appunti, formazione, piccolo brand locale, "fatto con cura".

## Le regole, con i numeri
| Regola | Valore |
|---|---|
| Tratto che "bolle" (boiling line) | il disegno cambia leggermente 12 volte al secondo (passo due), spostamento 1-2 px |
| Tratto che si disegna | 0,5-0,8 s per un tratto, ease in uscita morbida (ease out cubic) |
| Carta | fondo #FBF7EE con fibre e macchie a opacità 3-6% |
| Inchiostro | #1B1B1B, mai nero puro |
| Accenti | massimo 2 per scena tra arancio #FF6A1A, magenta #E01E6A, blu #2E6BFF, giallo #F2B705, verde acqua #3CC9B0 |
| Testo | rivelato da sinistra a destra come se fosse scritto, poi resta fermo e "bolle" |
| Durata clip | 3,5 s ciascuna, formato 16:9 a 1280×720 |

## Le 12 tecniche ricostruite in codice
| # | Clip | Cosa fa | Quando usarla |
|---|---|---|---|
| 01 | titolo che tremola | titolo a pennarello con stelline e sottolineatura disegnata | apertura, titolo di capitolo |
| 02 | evidenziatore e cerchio | evidenziatore giallo e cerchio a mano su una parola | sottolineare il messaggio chiave |
| 03 | icone a scarabocchio | 4 icone che si disegnano con etichette | elenco di valori o funzioni |
| 04 | riempimento a scarabocchio | stella a punte riempita a tratteggio, "NUOVO!" | lancio, offerta |
| 05 | lavagna e gesso | lavagna verde con testo a gesso | menu, liste, formazione |
| 06 | macchia di inchiostro | l'inchiostro si allarga e rivela il titolo | transizione, claim forte |
| 07 | grafico a pennarello | linea che cresce, cerchio sul risultato +48% | dati in tono informale |
| 08 | note sul prodotto | frecce e annotazioni attorno al prodotto | caratteristiche del prodotto |
| 09 | stop-motion ritagli | lettere di carta che saltano a scatti | saldi, promozioni |
| 10 | personaggio che parla | faccina disegnata con fumetto | storytelling, tono amichevole |
| 11 | lista sul quaderno | spunte su un foglio a righe | "perché sceglierci", checklist |
| 12 | pennellate e chiusura | pennellate di colore e logo finale | chiusura con logo |

File: `clip/05-*.mp4`, sorgente `categoria05.html`, anteprima `contact_sheet_05.jpg`.

## Palette e font
- Fondo carta #FBF7EE, inchiostro #1B1B1B, lavagna verde scuro, accenti sopra.
- Font (già nel pack, licenza OFL): Permanent Marker per i titoli, Caveat Brush per le note, Inter 500/800 per il testo leggibile, Archivo Black per le lettere ritagliate.

## Suono
Matita o pennarello su carta mentre il tratto si disegna, piccoli pop quando compare un'icona, carta che si sposta per lo stop-motion. Musica acustica leggera (ukulele, pianoforte, fischio).

## Errori da evitare
- Tratto perfetto e fermo: sembra un font vettoriale, non un disegno. Il tratto deve bollire.
- Troppi colori nella stessa scena: al massimo 2 accenti.
- Testo lungo scritto a mano: oltre 6-8 parole si passa a Inter.
- Animazione fluida a 30 fps sul disegno: perde il fatto a mano. Passo due (12 fps) sul disegno, 30 fps solo sui movimenti di camera.

## Come usarle
`node ../../tools/render.mjs categoria05.html out.mp4 30 [config.json] [--scene N]`. Per il verticale e per i nuovi progetti conviene rifare la tecnica in HyperFrames ([metodo](../../manuale/metodo-hyperframes.md)).

## Limiti di questa scheda
Le reference esterne sono poche (vedi `reference.csv`) e vanno ampliate; mancano le clip in 9:16.
