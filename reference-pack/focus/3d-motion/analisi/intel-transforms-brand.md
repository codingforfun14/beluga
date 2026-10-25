# Intel, "Intel Transforms Its Brand"

## Scheda
Intel, settembre 2020, presentazione del rebrand "Do Something Wonderful" (canale Intel Newsroom, circa 518 mila visualizzazioni). 60 s, 1280×720 a 24 fps. Link: https://youtu.be/qCUAEDvaJsY. Fotogrammi in `test-hyperframes/frames/intel-transforms-brand/`.

## L'idea in una riga
La frase "Do something wonderful" si costruisce parola per parola, e ogni lettera è una finestra che si apre su immagini del mondo reale e sui prodotti Intel.

## Stile visivo (misurato sui fotogrammi)
- **Palette:** blu Intel (#0068B5 circa), azzurro elettrico (#00C7FD), blu notte, bianco; un tocco di giallo alla fine della sezione colori. Fondi pieni.
- **Luce:** piatta nella grafica; nelle parti di prodotto, glow blu sui bordi dei badge in 3D; live action con luce naturale calda (tramonto).
- **Materiali:** carta millimetrata per la storia del logo (1969 → 2006 → nuovo), badge di vetro blu.
- **Camera:** grafica ferma con elementi che scorrono; macro sui chip; live action con droni e camera a mano.

## Ritmo (misurato)
27 tagli in 60 s, **inquadratura media 2.1 s**; 51 cambi a soglia 0.12. Apertura rapida (5 tagli nei primi 3 s), parte centrale lenta (20.6–36.0 s quasi senza tagli: la storia del logo), finale accelerato (10 tagli tra 41.6 e 50.1 s).

## Beat
| s | Cosa succede |
|---|---|
| 0–10 | "Do" "something" scritti enormi in un sans sottile; le lettere fanno da maschera su foto (Terra, chip) |
| 10–20 | "to forge the future" con video in un riquadro; la storia del logo su carta millimetrata |
| 20–30 | griglia di loghi nelle tonalità del blu, "something", "timeless", "Classic Blue" (il sistema colore) |
| 30–40 | icone a linea, il badge CORE in 3D, la famiglia di badge in isometria |
| 40–55 | live action: persone, laptop, natura; "and Intel inside", "to do something wonderful." |
| 55–60 | logo Intel su blu |

## Tipografia
Intel Clear (nuovo carattere del rebrand), sottile e geometrico, usato enorme con le lettere tagliate dal bordo; un **quadratino azzurro** (il "dot" del logo) apre e chiude ogni frase come un cursore.

## Transizioni
Maschere di testo (la parola è una finestra sul video), il quadratino che scorre e "spinge" la scena successiva, riquadri che si espandono fino a tutto schermo.

## Suono
Non ascoltato in questa analisi; da verificare (probabile musica ispirazionale con voce o solo testo).

## Tecnica probabile
Motion 2D (After Effects) con maschere di testo su footage, alcune parti 3D (badge di prodotto), live action di repertorio o girato.

## Come lo replichiamo
- **HyperFrames/GSAP:** maschere di testo su video (`background-clip: text` o `mask-image` con un `<video>`), il quadratino che fa da cursore e da transizione, griglie di colori. Tutto in HTML.
- **Blender:** i badge di vetro blu in isometria (piani con bevel, materiale vetro e un'emissione sul bordo), still o brevi movimenti.
- **Kling:** facoltativo per le scene live action (3–4 clip da 5 s, stima indicativa); in alternativa stock CC0.
- **Asset CC0:** footage di Terra e natura da Pexels o NASA (pubblico dominio), con ok per il download; font sottile da Google Fonts (Manrope Light o Outfit).
- **Difficoltà:** bassa.
- **Render sul Mac:** HyperFrames 10 s in 1–2 minuti; Blender badge circa 2 s a fotogramma.

## Cosa rubare
- **La parola come finestra**: il claim e le immagini sono la stessa cosa.
- Un elemento minimo del logo (il quadratino) che fa da cursore, transizione e firma.
- Mostrare il sistema del brand (colori, griglie) come contenuto, non solo come regola.
