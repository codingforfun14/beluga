# 03 · 3D morbido e clay

Per quando il brief dice: tech amichevole, prodotto da rendere simpatico, finanza o servizi "noiosi" da scaldare, giocoso ma premium. Il materiale fa il messaggio: tutto sembra toccabile, niente è freddo.

Prova che funziona anche per temi seri: Aardman ha fatto le pensioni Nest (2025) in CG che imita la plastilina, per renderle "calde e avvicinabili", e gli spot hanno testato sopra la media ([Creative Boom](https://www.creativeboom.com/news/aardman-creates-feathery-fun-for-nest/)).

## Due varianti, da scegliere subito
| Variante | Come appare | Movimento | Quando |
|---|---|---|---|
| **Clay** (finta plastilina) | impronte, piccole ammaccature, bordi non perfetti, occhi e bocche "adesivi" alla Aardman | a passo due (12 pose al secondo), con un leggero tremolio della superficie tra una posa e l'altra | racconto, personaggi, umorismo, brand che vogliono sembrare fatti a mano |
| **Soft 3D** (3D morbido) | superfici lisce e opache, forme arrotondate, pastello | fluido a 24-30 fps, rimbalzi elastici | prodotto, app, tech, icone 3D |

Non mischiarle nello stesso film: o tutto a passo due o tutto fluido.

## Le regole, con i numeri
Regole di lavoro della libreria. I valori di partenza vengono dalla mappa stili e dalle reference; quelli segnati *(da provare)* vanno confermati al primo test.

| Regola | Valore |
|---|---|
| Materiale | opaco, nessun riflesso a specchio; ruvidezza alta; un po' di luce che passa sotto la superficie (subsurface) sui bordi sottili |
| Luce | una luce grande e morbida dall'alto o di lato, ombre morbide a contatto, nessuna luce dura; sfondo tinta unita o gradiente leggero |
| Colori | 3-4 pastello + 1 colore pieno per il prodotto o la parola chiave; sfondo e oggetti dello stesso tono, separati dalla luminosità |
| Forme | spigoli tutti arrotondati, proporzioni "giocattolo" (teste grandi, mani tozze); niente dettagli sottili che si perdono in un formato 9:16 |
| Rimbalzi | elastici, con smorzamento 0,6-0,8: 1-2 rimbalzi visibili, poi fermo. In GSAP `elastic.out(1, 0.6)` o `back.out(1.7)` *(da provare)* |
| Squash e stretch | all'atterraggio schiacciare del 10-20% e allargare di pari volume, poi tornare in 0,15-0,25 s *(da provare)* |
| Camera | lenta: una sola mossa per inquadratura (carrellata o orbita breve), mai scatti di camera dentro il 3D; i tagli fanno il ritmo |
| Passo due (solo clay) | ogni posa tenuta 2 fotogrammi a 24 fps; la texture cambia leggermente a ogni posa (in Kling: "animated on twos, slight frame-to-frame jitter") |
| Testo | fuori dal 3D: titoli piatti in HyperFrames sopra il video, sans tondo e pesante; oppure il titolo stesso in clay, ma solo per il logo finale |

## Come lo facciamo noi (asset KI / KV)
1. **Kling Image** per i fotogrammi chiave e il personaggio (foglio modello, poi Element). Prompt base: "soft matte clay material, rounded shapes, pastel palette, soft studio light, soft contact shadows, no glossy reflections".
2. **Kling Video** per il movimento del personaggio o del prodotto, 5 s per clip, una azione per clip.
3. **HyperFrames** per montaggio, titoli, packshot finale e suono. Il 3D resta nel video, la grafica resta in HTML.
4. Per clay vero e proprio: aggiungere al prompt "stop-motion, animated on twos, visible fingerprints in the clay", e nel negativo "smooth CGI, glossy plastic".

Vedi anche la scheda [Mascotte con Kling](../mascotte-kling/SCHEDA.md) per il character bible e l'Element.

## Errori da evitare
- Plastica lucida: appena c'è un riflesso a specchio sembra un giocattolo economico, non clay.
- Clay "troppo perfetto": senza impronte e ammaccature diventa 3D generico.
- Passo due mescolato a camere fluide: la camera deve scattare insieme ai personaggi, o restare ferma.
- Rimbalzi infiniti o oggetti che galleggiano e respirano in loop (default da video generato).
- Troppi colori saturi: il pastello regge solo se c'è un unico colore pieno.
- Testo 3D illeggibile in piccolo: i titoli vanno piatti.

## Collegamenti
- Gancio dei primi 2 secondi: [16 Hook per short](../16-hook-per-short/SCHEDA.md)
- Costruzione in codice: [metodo HyperFrames](../../manuale/metodo-hyperframes.md)
- Reference: [reference.csv](reference.csv)
