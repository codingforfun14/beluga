# Review: spot telefono ORMA 2

## Scelte creative
- Storyline A, "Una carica, tutta la giornata" (vedi STORYLINES.md). Non costruite: B "Dopo la caduta", C "Zoom infinito nella fotocamera".
- Brand e numeri inventati (ORMA, Orma 2, 100% -> 31%, "Dal 3 novembre"): illustrativi.
- Telefono 3D in Three.js dentro HyperFrames, nessun credito Kling. 60 fps, 23,2 s, 1392 fotogrammi.
- Regole della libreria applicate: un oggetto eroe che riempie circa il 75% dell'altezza; luce calda di chiave e controluce freddo; ombra di contatto; frusta con blur al picco; colour flood che parte dal telefono; un solo accento (il 31%); lo schermo che diventa il mondo (zoom dentro lo schermo, poi taglio sul 31% a tutto quadro); marchio una volta sola, sul finale.

## Cosa ho misurato e cosa no
- `check`: nessun errore. Avvisi tenuti: tracce dense e strutture annidate (file unico per semplicità), avvisi del driver WebGL.
- Guardati i fogli di review e i fotogrammi 6,6 / 9,6 / 13,6 / 15,8-17,05 s.
- Il suono è misurato, non ascoltato. Solo effetti (whoosh, pop, riser, impatto, click), **nessuna musica**: qui non c'è una libreria musicale. Con una musica il film migliora molto.

## Punto più debole
- I mondi sono solo colori pieni con lo sfondo dello schermo disegnato: manca un vero luogo (cucina, metro, palestra, concerto). Con più tempo: clip Kling dei quattro luoghi come lastre dietro al telefono, o un set 3D per ogni momento.
- Il taglio 16,97 -> 17,03 s: il 31% dello schermo e quello a tutto quadro non coincidono al pixel (piccolo salto di posizione).
- La notte: il corpo del telefono si stacca poco dal fondo scuro, anche con il controluce alzato.
- Audio normalizzato dopo il render: da -10,5 a -13,3 LUFS, picco reale -1 dBTP.
