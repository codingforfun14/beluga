# I 12 principi dell'animazione, applicati al motion design e al 3D

Fonte: Frank Thomas e Ollie Johnston, *The Illusion of Life: Disney Animation* (1981), cap. 3. Riassunto pubblico: [IBM Design, classic principles](https://www.ibm.com/design/language/animation/classic-principles). I valori in frame sono a 60 fps; a 30 fps si dimezzano.

Nel motion design i principi valgono anche per gli oggetti: un logo, un telefono, una scritta. Un oggetto senza peso e senza intenzione sembra un template.

| # | Principio | Cosa vuol dire | Regola pratica per noi | Errore tipico |
|---|---|---|---|---|
| 1 | Squash and stretch (schiacciamento e allungamento) | Il volume resta costante mentre la forma si deforma | Oggetti morbidi e clay: squash fino al 20-30% all'impatto, volume costante (scaleX × scaleY ≈ 1). Prodotti rigidi (telefono, orologio): niente squash sull'oggetto, si "schiaccia" la camera o l'ombra *(da provare)* | Deformare un prodotto premium: sembra di gomma |
| 2 | Anticipation (anticipazione) | Prima di un'azione grande c'è un piccolo movimento opposto | 6-12 frame di rinculo, ampiezza 5-15% del movimento principale | Oggetti che partono di colpo da fermi |
| 3 | Staging (messa in scena) | Una sola idea leggibile per inquadratura | Un oggetto protagonista, sfondo che non compete, silhouette leggibile anche in nero pieno (test: metti tutto nero e guarda se si capisce) | Tre cose che si muovono insieme al centro |
| 4 | Straight ahead e pose to pose | Animare in sequenza oppure per pose chiave | In codice si lavora sempre pose to pose: keyframe con easing. Lo straight ahead lo fanno le simulazioni (fisica di Blender, particelle) | Tutto in keyframe, anche ciò che dovrebbe essere caotico (fumo, detriti) |
| 5 | Follow through e overlapping action | Le parti non si fermano tutte insieme | Elementi secondari in ritardo di 2-6 frame; code, cavi, etichette continuano 8-20 frame dopo l'arresto | Gruppo di elementi che si ferma nello stesso frame |
| 6 | Slow in e slow out | Accelerare e frenare | Mai lineare, tranne rotazioni continue. Curve in `manuale/principi-motion.md` | Easing di default, movimento "da PowerPoint" |
| 7 | Arcs (archi) | Le cose naturali si muovono su archi | Camera e oggetti su traiettorie curve (bezier o somma di due assi con easing diverse) | Spostamenti in linea retta diagonale |
| 8 | Secondary action (azione secondaria) | Un gesto che arricchisce l'azione principale senza rubarla | Riflesso che scorre sul vetro mentre il telefono ruota, polvere che si alza all'atterraggio | Azione secondaria più forte della principale |
| 9 | Timing | Il numero di frame dà peso e carattere | Pesante = lento ad accelerare, frenata breve. Leggero = veloce, rimbalza. Stesso movimento a 18 o 42 frame racconta due oggetti diversi | Tutti gli oggetti con la stessa durata |
| 10 | Exaggeration (esagerazione) | Spingere oltre il reale per renderlo leggibile | Overshoot 5-10% per brand seri, 10-20% per brand giocosi. Nei 3D di prodotto si esagera la luce, non la forma | Realismo piatto, nessun momento che resta in testa |
| 11 | Solid drawing (forma solida) | Volume, peso, prospettiva credibili | Nel 3D: luce chiave calda, rim freddo, ombra di contatto, roughness ≥0.45 sui metalli (regole HF in `focus/3d-motion/SCHEDA.md`) | Oggetto che "galleggia" senza ombra |
| 12 | Appeal (fascino) | Il pubblico vuole guardarlo | Forme semplici e chiare, proporzioni con un elemento dominante, almeno un dettaglio curato in primo piano | Design corretto ma senza carattere |

## Come entrano nel nostro flusso

- **Storyboard**: per ogni inquadratura si scrive quale principio la regge (di solito staging + timing).
- **Review**: aggiungere alla checklist "c'è anticipazione sui movimenti grandi? gli elementi si fermano sfalsati?".
- **Three.js / HyperFrames**: `renderAt(t)` deve essere funzione pura del tempo, quindi anticipazione e follow through si scrivono come keyframe in più sulla traccia, non come fisica.
- **Blender**: follow through e caos (detriti, tessuti, liquidi) si fanno con le simulazioni e poi si "cuociono" (bake), così il render resta ripetibile.

## Per approfondire

- Richard Williams, *The Animator's Survival Kit* (2001): timing e spaziatura in frame.
- Alan Becker, *12 Principles of Animation* (serie YouTube, un video per principio; link da verificare).
