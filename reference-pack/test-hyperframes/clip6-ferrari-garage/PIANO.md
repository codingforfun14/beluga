# Spot "Sotto il telo": Ferrari 488 in un garage (piano, da discutere)

Richiesta di fede (2026-10-25): un garage buio, un drone che entra, un'auto coperta da un telo che viene sfilato, sotto c'è una Ferrari 488 rossa. Tutto in Blender (auto e scena), HyperFrames per il resto. Voce e musica per ora no: conta solo il render 3D fatto bene. Il garage deve sembrare vero e vivo, non uno sfondo fermo.

> Nota: è un test spec/portfolio. Ferrari, 488 e il cavallino sono marchi registrati: per pubblicarlo come pubblicità vera servono i diritti. Nel render non mettiamo il logo del cavallino finché non c'è un cliente.

## L'idea
Il buio e il silenzio sono la promessa, il rosso è la ricompensa. Per 12 secondi non si vede la macchina: si sente e si intuisce. Il drone è il nostro sguardo curioso. Quando il telo scivola via, il garage si accende con lei.

## Scaletta (25 s, 16:9; versione 9:16 ricavabile)
| s | Cosa si vede | Cosa si muove nel garage |
|---|---|---|
| 0–3 | nero; una lama di luce sotto la saracinesca che si alza di un metro | polvere che entra con l'aria, la luce che corre sul cemento |
| 3–6 | il drone entra rasoterra controluce (camera fissa bassa, lui si avvicina) | eliche che sollevano polvere, LED rosso e verde, riflessi nelle pozze |
| 6–9 | **POV del drone** (FPV): vola tra cassettiera, gomme, scaffali; il faro scivola sugli oggetti | un neon si accende tremolando, un cavo che oscilla, una goccia che cade in una pozza |
| 9–12 | il faro trova la sagoma sotto il telo; orbita lenta attorno alla macchina coperta | il vento delle eliche fa vibrare il telo (simulazione cloth) |
| 12–15 | il drone aggancia il telo e lo tira: il telo scivola dal muso alla coda e cade a terra | simulazione cloth vera; polvere che si alza dal telo |
| 15–19 | **rivelazione**: la 488 rossa; luce che corre sulla carrozzeria; 3 dettagli da 1 s (faro, presa d'aria laterale, cerchio con pinza) | i neon si accendono tutti in sequenza, riflessi che scorrono sulla vernice |
| 19–23 | eroe: camera bassa 3/4 che gira lentamente; il drone si allontana verso la saracinesca | luce del giorno dalla saracinesca, nebbia leggera |
| 23–25 | end card (HyperFrames): claim e spazio per il logo | l'auto resta sullo sfondo, sfocata |

Ritmo: lento fino a 12 s (2 tagli), poi più veloce alla rivelazione (5 tagli in 7 s). È lo schema dei nostri test: tensione lunga, ricompensa rapida.

## Il garage "vero e vivo"
- **Spazio**: officina privata di 8 × 12 m con saracinesca, cemento lucido con macchie e pozze (riflessi), muri a blocchi, plafoniere neon, cassettiera, pile di gomme, scaffali, tubo dell'aria, prolunghe.
- **Cose che si muovono sempre**: polvere nell'aria (particelle), nebbia volumetrica nei raggi, neon che si accendono e tremolano, la saracinesca, gocce, un cavo che oscilla, il telo mosso dal vento delle eliche, riflessi che scorrono, camera con micro-vibrazioni da drone o da steadicam.
- **Luce**: buio con una sola fonte all'inizio (la lama di luce dalla saracinesca), poi il faro del drone, poi i neon freddi e la luce calda del giorno. Il rosso della 488 è l'unico colore saturo.

## La Ferrari 488
Rifarla da zero in Blender con la qualità di uno spot richiederebbe giorni e verrebbe peggio di un modello professionale. Propongo:
1. **Consigliato: un modello 3D già fatto e dettagliato** (carrozzeria, interni, ruote separate, fari), da Sketchfab (controllando la licenza) o comprato su CGTrader/TurboSquid (circa 50–300 €). Lo scarica o lo compra fede; io non creo account e non pago. Poi lo preparo io in Blender: vernice Rosso Corsa a strati (base, metallizzato, trasparente), vetri, gomme, cerchi, pinze, fari con emissione, ruote che girano.
2. Alternativa: lo modello io da blueprint e foto di fede. È più lento (giorni) e meno preciso; va bene solo se il modello pronto non è possibile.

## Strumenti
- **Blender (Eevee)**: tutta la scena, il drone (lo costruisco io), il telo (simulazione cloth già provata nei fotogrammi di prova), la polvere, la nebbia, le luci animate.
- **Cycles**: solo per 2–3 still "poster" della macchina, perché a fotogramma sul Mac sarebbe troppo lento e scalderebbe.
- **HyperFrames**: end card, eventuali scritte e titoli, montaggio finale con ffmpeg.
- **Kling (facoltativo, crediti di fede)**: solo per generare 2–3 immagini di riferimento del look (prompt pronti in `PROMPT-KLING.md`). Il video lo facciamo in Blender, non con Kling.
- **Asset CC0** da scaricare con il tuo ok: HDRI di un interno industriale (Poly Haven), texture di cemento, metallo e gomma (ambientCG / Poly Haven), qualche attrezzo.

## Tempi e carico sul Mac (modalità leggera: nice 19, 2 thread, blocchi con pausa)
- Preparazione scena, modello, materiali e animazione: lavoro mio, render solo di prova.
- Render finale: 25 s a **30 fps = 750 fotogrammi**, circa 6–12 s l'uno in Eevee con nebbia e riflessi, cioè **1,5–2,5 ore** in modalità leggera. A 24 fps (look più cinema) i fotogrammi sono 600, circa 1–2 ore.
- 60 fps qui non lo consiglio: raddoppia il tempo e il calore senza vantaggi per uno spot di questo tipo.

## Tappe con screen
1. Garage completo con luci e polvere (fotogrammi di prova).
2. 488 importata e materiali (still Cycles della macchina).
3. Animazione: drone, telo, camere (animatic a bassa risoluzione).
4. Fotogrammi di prova 1080p, poi render a blocchi con screen a metà e alla fine.
5. End card e montaggio; voce e musica in un secondo momento.

## Cosa mi serve da fede
- **Modello 3D della 488**: lo cerchi tu o vuoi che ti proponga 2–3 link da valutare?
- **Reference**: foto di garage che ti piacciono (officina vissuta o garage privato minimal?), foto della 488 rossa (dettagli, fari, cerchi), e uno o due spot di auto che ti piacciono per il ritmo.
- **Formato**: 25 s vanno bene? Serve anche il 9:16? 24 o 30 fps?
- **Il drone**: lo vogliamo vedere come personaggio (com'è adesso) o solo come camera POV?
- **Ok per scaricare asset CC0** da Poly Haven / ambientCG.

## Fotogrammi di esempio
- `progress/01-mood-drone-entra.jpg`: il drone entra controluce dalla saracinesca, la macchina coperta in primo piano.
- `progress/02-mood-telo.jpg`: il faro del drone scopre la sagoma sotto il telo (simulazione cloth vera sulla sagoma con le proporzioni della 488).
Sono un blockout: materiali, nebbia volumetrica e dettagli del garage vanno ancora fatti.
