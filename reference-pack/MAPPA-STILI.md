# Mappa degli stili

20 stili visivi (asse 1) e 8 famiglie di tecniche (asse 2). Ogni brief prende da 1 a 3 stili e le tecniche che servono. I numeri sono valori di partenza: la spec del progetto li fissa ([modello spec](direzione-creativa/modelli/spec.md)).

Legenda asset: **C** = codice (HyperFrames), **KI** = immagine Kling animata in codice, **KV** = video Kling.

## Asse 1: stili

| N. | Stile | Quando (parole del brief) | Firma visiva | Movimento | Asset | Riferimenti da studiare | Stato |
|---|---|---|---|---|---|---|---|
| 01 | Kinetic typography | lancio, manifesto, citazione, lyric video | 1 font display + 1 testo, 2 colori, testo enorme a tutto schermo | parole a ritmo del beat, tagli ogni 0,3-0,6 s, letter spacing animato | C | titoli di Saul Bass, lyric video, Apple keynote | da fare |
| 02 | Explainer flat vettoriale | spiegare un concetto, app, scienza | forme piatte, 4-5 colori pastello saturi, contorni assenti, ombre a 1 tono | ogni idea 3-5 s, transizioni per trasformazione delle forme | C | Kurzgesagt, BUCK | da fare |
| 03 | 3D morbido e clay | tech amichevole, prodotto, giocoso premium | materiali opachi tipo argilla, luce morbida da studio, colori pastello | rimbalzi elastici (smorzamento 0,6-0,8), camera lenta | KI / KV | spot tech, Apple | da fare |
| 04 | Vetro, gradienti, SaaS | software, startup, lancio funzione | sfondo scuro, gradienti mesh, vetro smerigliato, UI pulita | parallasse lenta, glow, reveal con maschere, ease expo.out | C | lanci prodotto Stripe e Linear | da fare |
| 05 | Disegnato a mano | tono umano, appunti, formazione | tratto irregolare, carta, colori a pennarello | animazione a passo due (12 fps), tratto che si disegna | C | lavagna, sketchnote | clip pronte, [scheda](categorie/05-disegnato-a-mano/SCHEDA.md) |
| 06 | Collage e carta strappata | giornalismo, storia, documentario | foto in bianco e nero ritagliate, carta strappata, mezzatinta, font condensato | passo due, scatti di posizione, zoom lenti | C + KI | Vox | da fare (skill vox-explainer) |
| 07 | Retro, Y2K, VHS | nostalgia, musica, moda giovane | aberrazione cromatica, linee di scansione, cromature, colori acidi | glitch a scatti, zoom digitali, testo che lampeggia | C | spot nostalgici, videoclip | da fare |
| 08 | Data viz e infografiche | numeri, report, risultati | griglia, 1 colore d'accento su grigi, numeri grandi | barre e linee che crescono con ease power2.inOut, contatori | C | giornalismo visivo | da fare |
| 09 | Demo UI e prodotto | app walkthrough, funzione nuova | schermate reali, cursore, mockup del dispositivo | zoom sul clic, match cut, rimbalzo dello schermo nuovo | C + schermate | app walkthrough | da fare |
| 10 | Svizzero e brutalista | agenzie, cultura, architettura | griglia rigida, Helvetica o grotesk, bianco e nero + 1 colore | tagli secchi, testo che scorre a velocità costante | C | identità di agenzie | da fare |
| 11 | Corporate finanza | banca, investimenti, B2B serio | blu scuro e neutri, grafici puliti, foto stock curate | movimenti lenti e precisi, nessun rimbalzo | C + stock | | clip pronte, [scheda](categorie/11-corporate-finanza/SCHEDA.md) |
| 12 | Personaggi 2D e mascotte | brand amichevole, serie social | personaggio con silhouette chiara, max 3 colori | recitazione, anticipazione e squash and stretch | C / KV | Duolingo, Headspace | [scheda mascotte](categorie/mascotte-kling/SCHEDA.md) |
| 13 | Forme liquide e morphing | identità animata, beauty, musica | blob, gradienti, forme che si fondono | morph continui, nessun taglio, ease sine.inOut | C | identity animate, BUCK | da fare |
| 14 | Isometrico | processi, città, logistica | vista isometrica a 30°, colori piatti, ombre a 1 tono | oggetti che salgono dal piano, camera fissa | C | mondi in miniatura | da fare |
| 15 | Titoli cinematografici | trailer, sigla, evento | nero, tipografia elegante, luce volumetrica, grana | reveal lenti 1-2 s, dissolvenze, riser musicale | C + KI | Art of the Title | da fare |
| 16 | Hook per short e reel | TikTok, Reels, Shorts | testo enorme nella zona sicura, contrasto massimo | movimento e suono dal fotogramma 0, promessa entro 3 s | C | | completa, [scheda](categorie/16-hook-per-short/SCHEDA.md) |
| 17 | Foto animata 2.5D e parallasse | documentario, storia, memoria | foto scontornate su più piani, luce cinematografica | camera che si muove tra i piani, 4-8 s per foto | KI | documentari | da fare |
| 18 | Glitch e digitale | musica elettronica, tech, gaming | pixel, RGB separati, rumore, monospace | scatti, ripetizioni, strobo brevi | C | musica e tech | da fare |
| 19 | Lusso ed editoriale | moda, gioielli, hotel | molto spazio vuoto, serif sottile, nero e oro o crema | lentezza, dissolvenze lunghe, macro del prodotto | KI / KV | moda e gioielli | da fare |
| 20 | Giocoso per bambini | app educative, giochi | forme tonde, colori primari, contorni spessi | rimbalzi ampi (smorzamento 0,4-0,6), pop | C | app educative | da fare |

## Asse 2: tecniche

Ogni reference ha tag su entrambi gli assi, così si può cercare "un logo reveal in stile 13" o "un hook in stile 06".

| Tecnica | Dove sono le regole | Tag |
|---|---|---|
| Hook dei primi 3 secondi | [16 Hook per short](categorie/16-hook-per-short/SCHEDA.md) | `hook` |
| Transizioni (match cut, wipe, morph, whip pan) | [principi-motion](manuale/principi-motion.md), [metodo-hyperframes](manuale/metodo-hyperframes.md) | `transizione` |
| Comparsa del testo | [principi-motion](manuale/principi-motion.md) | `testo` |
| Logo reveal | da scrivere | `logo` |
| Lower third e sottotitoli | [formati-e-safe-zone](manuale/formati-e-safe-zone.md) | `lower-third` |
| Call to action finale | da scrivere | `cta` |
| Movimenti di camera (push-in, parallasse, orbit) | [metodo-hyperframes](manuale/metodo-hyperframes.md) | `camera` |
| Sound design e sincronia | [sound-design](manuale/sound-design.md) | `suono` |

## Come scegliere
1. Dal brief si prende il tono (3 aggettivi) e il canale.
2. Si cercano nella colonna "Quando" le parole del brief: di solito escono 2-4 stili.
3. Se ne tengono al massimo 3: uno principale, uno per i momenti di rottura, uno per i dati o il prodotto.
4. Per ogni stile si leggono SCHEDA e reference, poi si scrive la spec.

Combinazioni che funzionano: 16 + 01 (hook tipografico), 02 + 08 (explainer con dati), 09 + 04 (lancio SaaS), 12 + 16 (mascotte social), 06 + 17 (documentario), 15 + 19 (lusso cinematografico).
