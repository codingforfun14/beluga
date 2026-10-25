# PayPal, "How PayPal Works"

## Scheda
PayPal, marzo 2015, video esplicativo (canale PayPal, circa 509 mila visualizzazioni). 74 s, 1280×720 a 23,976 fps. Link: https://youtu.be/WB370ewOklw. Fotogrammi in `test-hyperframes/frames/paypal-how-it-works/`.

## L'idea in una riga
Il servizio spiegato passo per passo con icone a linea su bianco: registrati, aggiungi la carta, paga con un clic su computer, tablet e telefono, e sei protetto.

## Stile visivo (misurato sui fotogrammi)
- **Palette:** bianco come fondo base, con passaggi a colore pieno: azzurro PayPal (#009CDE circa), magenta (#A0007E circa), arancione (#F7941D circa), verde menta. Il blu scuro del logo solo alla fine.
- **Luce:** nessuna, è grafica piatta.
- **Materiali:** icone a linea nera di spessore costante (telefono, monitor, lucchetto, ombrello, pacco), riempimenti piatti.
- **Camera:** ferma; i passaggi sono "wipe" diagonali di colore.

## Ritmo (misurato)
**0 tagli netti** a soglia 0.3 e solo 4 cambi a soglia 0.12: tutto il film è un'animazione continua che passa da una scena all'altra con wipe e morph. I "capitoli" cambiano circa ogni 4–7 s (cambio di colore pieno o di icona).

## Beat
| s | Cosa succede |
|---|---|
| 0–7 | wipe azzurro, un telefono con "Shop", il carrello |
| 7–11 | "ONE" enorme su magenta (un solo account) |
| 11–22 | registrazione: browser con email, carte di debito e credito, lucchetto (sicurezza) |
| 22–29 | "$ You don't need a balance", wipe arancione |
| 29–40 | il checkout con "Check out with PayPal", pattern di browser su verde menta |
| 40–48 | computer, tablet, mobile phone con le spunte |
| 48–70 | account, PayPal Buyer Protection (ombrello sul pacco), "We'll reimburse you for the full amount", "Secure" |
| 70–74 | logo PayPal su bianco |

## Tipografia
Un sans tondo (tipo Gotham Rounded/Avenir), parole chiave in grassetto o in un secondo colore ("don't need a balance", "full amount"); poche parole per schermata, sempre sincronizzate con la voce.

## Transizioni
Wipe diagonali di colore pieno, icone che si disegnano (stroke che si traccia), oggetti che si trasformano l'uno nell'altro (monitor → tablet → telefono).

## Suono
Non ascoltato in questa analisi; un explainer di questo tipo ha sempre voce narrante e musichetta leggera, con piccoli effetti sulle icone. Da verificare.

## Tecnica probabile
Motion 2D in After Effects (shape layers, trim paths), montaggio sulla voce.

## Come lo replichiamo
- **HyperFrames/GSAP:** al 100 %. Icone SVG a linea con `stroke-dashoffset` (come la spunta della card di "Peso"), wipe diagonali con `clip-path: polygon()`, morph tra icone. Il testo segue la voce con i tempi presi dalla trascrizione.
- **Blender:** non serve.
- **Kling:** no. La voce si farebbe con ElevenLabs, che però per ora non usiamo: si può scrivere il testo e lasciare la voce a fede.
- **Asset CC0:** icone da Lucide o Tabler (licenza ISC/MIT, già SVG), font Google Fonts (Nunito o Quicksand).
- **Difficoltà:** bassa.
- **Render sul Mac:** HyperFrames 10 s a 60 fps in meno di un minuto.

## Cosa rubare
- **Spiegare il servizio in passi** (registrati → collega → paga → protetto) con un'icona per passo: è la struttura giusta per un video tutorial di PRATICA.
- Wipe di colore pieno come capitoli: ritmo senza tagli e senza fatica.
- Spessore di linea costante in tutte le icone: dà coerenza con pochissimo lavoro.
