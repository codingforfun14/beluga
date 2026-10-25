# Housing.com, "Look Up – Housing Brand Story"

## Scheda
Housing.com (portale immobiliare indiano), marzo 2015, film di rebrand (canale Housing.com, 2,1 milioni di visualizzazioni). 60 s, 1280×720 a 25 fps. Link: https://youtu.be/KyYyKRiJR4M. Fotogrammi in `test-hyperframes/frames/housing-look-up/`.

## L'idea in una riga
Un solo simbolo, la freccia "^" del logo (un tetto che indica "guarda in alto"), viaggia senza stacchi da una barra di ricerca allo spazio, alle persone, fino al logo.

## Stile visivo (misurato sui fotogrammi)
- **Palette:** bianco iniziale con magenta (#E6007E circa); poi un lungo viaggio su viola profondo (#2A0A6B circa) con accenti magenta, giallo, verde lime; finale giallo pieno (#FFF200 circa) con scritta magenta "LOOK UP".
- **Luce:** glow e bagliori (un sole magenta-bianco a 15 s e 48 s), particelle luminose.
- **Materiali:** forme piatte con un po' di profondità; particelle che formano scie, un infinito e la parola "positivity" scritta in luce.
- **Camera:** un unico viaggio continuo, la camera segue la freccia.

## Ritmo (misurato)
**0 tagli** sia a soglia 0.3 sia a 0.12: è un **piano unico di 60 s**, con le scene che si trasformano una nell'altra. I cambi di "capitolo" sono passaggi di colore (bianco → viola a circa 8 s, viola → crema → giallo a circa 50 s).

## Beat
| s | Cosa succede |
|---|---|
| 0–6 | barra di ricerca bianca: si scrive "how?", "where?", il tasto SEARCH si gonfia e si rompe in forme |
| 6–14 | la freccia magenta vola nel viola |
| 14–20 | esplosione di luce: un sole, pianeti collegati da raggi (le persone, la rete) |
| 20–33 | scie di particelle disegnano un infinito, poi la parola "positivity" |
| 33–47 | la freccia diventa verde, un fiore di loto magenta si apre, piccoli fiori/case all'orizzonte |
| 47–60 | ultimo bagliore, flash crema, fondo giallo, "LOOK UP" e la freccia che diventa logo |

## Tipografia
Poca: la barra di ricerca, la parola "positivity" scritta con le particelle, il claim finale in un bold geometrico magenta. Il racconto lo fa il simbolo.

## Transizioni
Nessun taglio: morph del simbolo, flash di luce, passaggi di colore pieno.

## Suono
Non ascoltato in questa analisi. Il testo della descrizione fa pensare a una voce narrante ispirazionale: da verificare.

## Tecnica probabile
Motion 2D/2.5D in After Effects con particelle (Trapcode Particular/Form) e glow. Nessun 3D fotorealistico.

## Come lo replichiamo
- **HyperFrames + Three.js:** tutto. Il simbolo è un SVG che si trasforma (morph di path con GSAP), le particelle sono un `Points` di Three.js che segue una curva (infinito, parola), i bagliori sono sprite additivi. Un piano unico in una sola composizione.
- **Blender:** facoltativo, solo per il fiore di loto se lo vogliamo in 3D (Geometry Nodes con petali istanziati).
- **Kling:** no.
- **Asset CC0:** nessuno; font Google Fonts.
- **Difficoltà:** media, perché il piano unico obbliga a pianificare ogni passaggio.
- **Render sul Mac:** HyperFrames con WebGL, 10 s a 60 fps in 2–3 minuti a un worker.

## Cosa rubare
- **Un simbolo che viaggia** tiene insieme 60 s senza un solo taglio: per PRATICA può essere la spunta ✓.
- La barra di ricerca come gancio: chiunque la riconosce in un fotogramma.
- Capitoli fatti con il colore pieno invece che con i tagli.
