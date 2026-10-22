GOAL:    lo spettatore ricorda "il telefono che arriva a mezzanotte con il 31%" e il nome ORMA.
OUTPUT:  HyperFrames, 1920 x 1080, 60 fps
TIME:    22 s x 60 = 1320 fotogrammi
LOOK:    fondi pieni, uno per momento: alba #F3B48B, giorno #A9D3EE, sera #C63F2B, notte #13202B.
         Inchiostro #14202A sui fondi chiari, crema #FBF3E8 sui scuri. Accento #FF5A1F solo sul 31% finale.
         Display Outfit 800, titoli 104 px (9,6% altezza), tracking -2%; numeri 220 px. Testo a sinistra, x = 150 px.
         Telefono 3D (Three.js): corpo alluminio #9AA0A6 roughness 0,45 metalness 1; retro vetro opaco salvia #7E9A86
         roughness 0,55; schermo con texture del blocco schermo; ambiente RoomEnvironment 0,5; chiave calda da alto
         sinistra, controluce freddo da dietro; ombra di contatto morbida su un piano invisibile.
OBJECTS: telefono (rapporto 71 x 147 x 8 mm, angoli arrotondati, modulo fotocamera con due obiettivi, tasti laterali);
         blocco schermo con ora grande, data, batteria in alto a destra, una notifica per mondo, sfondo disegnato del mondo.
MOTION:  entrate testo power4.out 0,13 s per parola, 0,067 s tra le parole, blur 6 -> 0 px; camera power2.inOut;
         rotazioni rapide (frusta) 0,4 s expo.inOut con blur del canvas a 14 px nel fotogramma più veloce.
SHOTS:   0-3,0     alba: dolly-out da macro dello schermo (07:00, 100%) al telefono intero; "Sveglia." "100%"
         3,0-3,45  flood a giorno + frusta di 180 gradi sul retro; whoosh
         3,45-5,3  giorno, retro: orbita lenta sul modulo fotocamera; "Foto."
         5,3-5,7   frusta al fronte; whoosh corto
         5,7-7,4   giorno, fronte: 12:30, 74%; "Mappe. Messaggi." "74%"
         7,4-7,85  flood a sera + giro di 360 gradi; whoosh
         7,85-11,4 sera: push-in lento; 18:45, 52%; "Allenamento. Musica." "52%"
         11,4-11,85 flood a notte + frusta; whoosh cinematico
         11,85-15,4 notte: luce chiave bassa, lo schermo illumina; 23:10 -> 23:24, 34%; "Concerto in 4K." "34%"
         15,4-17,0 ricompensa: 23:59, il telefono si mette frontale, la camera entra nello schermo (riser)
         17,0-18,6 lo schermo diventa il mondo: "31%" enorme in accento (impatto), poi "Più lunga della tua giornata."
         18,6-22,0 finale: fondo alba, wordmark ORMA a tendina, "Orma 2", "Dal 3 novembre", fermo 2,5 s
BANNED:  vuoto scuro con oggetti piccoli; glow, bloom, particelle; gradienti viola o blu; card di vetro; tutto centrato;
         testo che si muove mentre si legge; logo in un angolo; tre card in fila; telefono piccolo al centro.
QA:      0,0 (non vuoto); 2,9; 4,5; 6,8; 9,5; 13,5; 16,6; 17,6; 18,3; 21,5
