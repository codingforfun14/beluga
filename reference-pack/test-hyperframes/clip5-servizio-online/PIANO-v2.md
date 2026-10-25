# Spot "Peso", piano v2: finale in ufficio

Richiesta di fede (2026-10-25): cambiare il design della parte che viene dopo il 3D e metterci uno sfondo da ufficio, per far capire subito il mondo della burocrazia. Per ora è solo il piano: non riparto finché fede non lo dice.

## Idea
Il 3D resta il "dopo il disastro" nel buio. Quando la card è pronta, il buio si apre su un **ufficio vero e calmo**: la scrivania è vuota e in ordine, c'è solo un telefono. Il monolite di carta era il peso, l'ufficio ordinato è il risultato. La card arancione è l'unico elemento che passa da un mondo all'altro e finisce sullo schermo del telefono, così "dal telefono" si vede invece di essere solo scritto.

## Scaletta nuova (da 12 s in poi; 0–12 s non cambia)
| s | Cosa si vede | Strumento |
|---|---|---|
| 12–14 | la card arriva in camera nel buio, compare l'interfaccia "730 · Inviata ✓ · 3 min", "tic" sulla spunta | Blender + HyperFrames (già pronto) |
| 14–15.5 | **passaggio**: la card si rimpicciolisce verso il basso, il nero si apre a tendina (luce da finestra con veneziane) e scopre l'ufficio sfocato | HyperFrames su still di Blender |
| 15.5–17.5 | **claim** sull'ufficio: scrivania vuota, luce calda del tardo pomeriggio, strisce d'ombra delle veneziane che scorrono piano. "PESANTE PER NOI." in alto a sinistra, "LEGGERA PER TE." sotto, sottile | HyperFrames, parallasse lenta su 2 piani |
| 17.5–20 | **end card**: piccolo push verso il telefono sulla scrivania; sullo schermo la card arancione con la spunta. A fianco il logo PRATICA e "La burocrazia, dal telefono." | HyperFrames |

## Design dopo il 3D
- **Look:** niente più nero pieno. Fondo ufficio caldo e desaturato (grigi caldi, legno chiaro, luce 3200–4000 K), sfocato quanto basta perché il testo si legga; vignettatura leggera.
- **Tipografia:** stessa famiglia del test Impatto (Helvetica Neue). Claim a 120 px, testo a sinistra a x = 150 px; "PESANTE" in Bold, "LEGGERA" in UltraLight: il contrasto di peso è il messaggio.
- **Colore:** arancione #FF5A1F solo sulla card, sulla spunta e sul marchio, come prima.
- **Movimento:** push e parallasse molto lenti (2–3 % in 2 s), entrate del testo `power4.out`. Il testo resta fermo mentre lo si legge.
- **Suono:** sul passaggio entra un ambiente d'ufficio quasi muto (ronzio di neon, un orologio lontano), sintetico in ffmpeg. Resta il "tic" del brand sulla spunta e sul logo.

## Da dove viene l'ufficio
1. **Consigliata: ufficio costruito in Blender** (scrivania, sedia, scaffale con qualche raccoglitore in ordine, finestra con veneziane, lampada, telefono sulla scrivania). Si renderizzano solo **2–3 still a 1080p** (piano largo, scrivania, schermo del telefono), circa un minuto in tutto, e il movimento lo fa HyperFrames. Il Mac quasi non si scalda, lo stile resta coerente col 3D e non ci sono licenze o download.
2. Alternativa: una foto d'ufficio CC0 (Pexels o Unsplash), più realistica subito ma meno coerente col 3D. Prima di scaricare chiedo l'ok.

## Carico sul Mac quando si riparte (tutto in modalità leggera)
1. Finisco il 3D da 7,8 a 15,5 s: 464 fotogrammi, circa 45 minuti a blocchi con pausa. Se l'ufficio parte già a 14 s, ne bastano circa 370 (circa 35 minuti).
2. Still dell'ufficio in Blender: circa 1 minuto.
3. HyperFrames aggiornato (passaggio, claim, end card sull'ufficio): circa 2 minuti a un worker.
4. Suono e mix a −14 LUFS / −1 dBTP, montaggio ffmpeg: pochi minuti.

## Domande per fede
- Ufficio **solo nel finale** (claim + end card), oppure il passaggio all'ufficio già a 14 s come sopra?
- Ufficio **in Blender** (consigliato) o **foto CC0**?
