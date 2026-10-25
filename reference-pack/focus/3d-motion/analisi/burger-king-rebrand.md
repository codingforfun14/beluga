# Burger King, video di presentazione del rebrand 2021

## Scheda
Burger King, gennaio 2021; identità di Jones Knowles Ritchie (dichiarato nella descrizione). Video caricato dal canale STIR (2 milioni di visualizzazioni). 84 s, 1280×720 a 23,976 fps. Link: https://youtu.be/xwH4oVnuIAs. Fotogrammi in `test-hyperframes/frames/burger-king-rebrand/`.

## L'idea in una riga
Le parole del nuovo carattere tipografico ("NEW", "CRAVEABLE", "DROOL") riempiono lo schermo a tempo di musica e si alternano al packaging, alle insegne e al cibo vero.

## Stile visivo (misurato sui fotogrammi)
- **Palette:** rosso fiamma (#D62300 circa), arancione (#FF8732), crema (#F5EBDC), marrone (#502314), verde lattuga. Fondi pieni, un colore per inquadratura.
- **Luce:** piatta nelle parti grafiche; still life del cibo con luce da studio.
- **Materiali:** grafica piatta, illustrazioni a tratto grosso, foto di packaging e del cibo.
- **Camera:** quasi ferma; il movimento lo fa la tipografia (scala, scorrimento, rimbalzo).

## Ritmo (misurato)
**79 tagli in 84 s, inquadratura media 1.05 s**; 186 cambi a soglia 0.12. È il più veloce dei sei: montaggio sulla musica, con raffiche di 3–4 tagli in mezzo secondo (3.34–3.63 s, 68.57–68.82 s, 80.33–80.71 s).

## Beat
| s | Cosa succede |
|---|---|
| 0–8 | "NEW", "CRAVEABLE", "It's", "more": parole a tutto schermo, una per taglio |
| 8–20 | il logo nuovo nasce (un panino che si chiude), muri di "BURGER KING" ripetuto, "MAKES US GREAT" |
| 20–35 | packaging con le illustrazioni, vassoi, la gamma completa, foto macro del cibo con "and the food" |
| 35–55 | insegne, affissioni, social, "Flame-grilled burgers", "DROOL", "The kind of stuff that makes…" |
| 55–75 | ristoranti, divise dello staff, stories Instagram |
| 75–84 | ingredienti illustrati che si compongono nel logo, logo finale |

## Tipografia
È la protagonista: il carattere custom "Flame" (morbido, rotondo, pesante) usato enorme, con parole tagliate dal bordo, linee ripetute come pattern e scritte che si deformano e rimbalzano. Una parola per volta, a tempo.

## Transizioni
Tagli secchi sul beat; parole che scorrono fuori campo e trascinano la scena successiva; elementi illustrati che entrano a rimbalzo.

## Suono
Non ascoltato in questa analisi; il montaggio a tagli regolari sotto il secondo indica una traccia musicale ritmata con la tipografia montata sul tempo. Da verificare.

## Tecnica probabile
Motion 2D in After Effects (kinetic type), foto e video di prodotto girati in studio, mockup 3D di packaging e insegne.

## Come lo replichiamo
- **HyperFrames/GSAP:** quasi tutto. Kinetic type con un font molto pesante (Google Fonts: "Bowlby One", "Chango" o un display rotondo), fondi pieni e tagli montati sui beat; illustrazioni in SVG che entrano a rimbalzo. Il ritmo si comanda con un array di tempi presi dalla traccia (beat detection con ffmpeg o a mano).
- **Blender:** mockup di packaging o insegne (scatola, sacchetto) con texture del brand, still o brevi rotazioni.
- **Kling:** facoltativo per macro del cibo o del "prodotto" (2–3 clip da 5 s, stima indicativa), meglio stock CC0 da Pexels.
- **Asset CC0:** foto di prodotto da Pexels (con ok), musica CC0 con battito chiaro.
- **Difficoltà:** bassa tecnicamente, alta di design (servono un carattere e una palette forti).
- **Render sul Mac:** HyperFrames 10 s a 60 fps in circa un minuto; Blender per 3–4 still pochi secondi.

## Cosa rubare
- **Il carattere tipografico è il brand**: una parola per inquadratura, enorme, a tempo.
- Ritmo sotto il secondo solo dove c'è un beat musicale da seguire.
- Mescolare grafica piatta e foto vere senza transizioni elaborate: basta che i colori siano gli stessi.
