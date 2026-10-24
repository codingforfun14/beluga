# Budget crediti Kling

Prezzi letti il 2026-10-24 da guide terze che riportano la tabella ufficiale di Kling VIDEO 3.0 ([Aiarty](https://www.aiarty.com/ai-video-generator/kling-ai-pricing.htm), [diyai.io](https://diyai.io/ai-tools/video-generation/kling-ai-pricing/), [eesel](https://www.eesel.ai/en/blog/kling-ai-pricing)). I prezzi cambiano spesso: ricontrollare sulla pagina prezzi di Kling prima di comprare.

## Costo per clip (Kling VIDEO 3.0)

| Clip | 720p muto | 1080p muto | 1080p con audio nativo |
|---|---|---|---|
| al secondo | 6 | 8 | 12 |
| 5 s | 30 | 40 | 60 |
| 10 s | 60 | 80 | 120 |

Piani: Standard 10 $/mese con 660 crediti, Pro 37 $ con 3.000, Premier 92 $ con 8.000 (fonte diyai.io, giugno 2026). I crediti dell'abbonamento scadono a fine mese.

## Quanto serve per uno spot

Regole prese dalle misure delle reference: uno spot da 30 s ha 8-15 inquadrature (media 2-5 s, vedi `../test-hyperframes/frames/*/info.txt`). Il suono lo facciamo a parte (ElevenLabs, musica), quindi si genera **muto a 1080p**. Ogni inquadratura si genera da 5 s e se ne usano 2-3; si contano **3 tentativi** per inquadratura buona.

| Lavoro | Inquadrature Kling | Crediti (5 s, 1080p muto, x3 tentativi) | Piano consigliato |
|---|---|---|---|
| Test di stile, 15 s | 4 | 4 x 40 x 3 = 480 | Standard (660) |
| Spot 30 s, metà 3D in Blender e metà Kling | 6 | 6 x 40 x 3 = 720 | Standard + ricarica, o Pro |
| Spot 30 s tutto Kling | 12 | 12 x 40 x 3 = 1.440 | Pro (3.000) |
| Spot 60 s + 3 tagli social da 15 s | 20 | 20 x 40 x 3 = 2.400 | Pro (3.000) |
| Prove a 720p prima del 1080p | qualsiasi | -25% sul costo delle prove | |

Proposta: **piano Pro (3.000 crediti al mese)**. Basta per due spot da 30 s con margine, oppure uno spot da 60 s con i tagli social. Il 3D di prodotto (scarpa, orologio, packshot) lo facciamo in Blender a costo zero; Kling serve solo per persone, personaggi, ambienti reali e azioni difficili da simulare.

## Come lo usiamo

1. Io scrivo i prompt per ogni inquadratura (durata, camera, luce prese dalle reference misurate) con la skill `kling-prompt-master`.
2. Tu generi dal tuo account (i crediti sono tuoi, io non li uso) e metti i file in una cartella.
3. Io scelgo le prese, monto, coloro, aggiungo testi, voce e musica.
