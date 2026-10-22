# 09 · Demo UI e prodotto

Per quando il brief dice: app, software, funzione nuova, lancio SaaS, "come si usa", walkthrough.

## Principi (da chi lo fa meglio)
Linear descrive così il lavoro di chi fa i suoi video ([annuncio di lavoro Motion Storyteller](https://linear.app/careers/2cf28db7-821f-44a0-99ee-ee0b7b7581af)): un solo linguaggio visivo dai clip social ai film di brand; l'animazione è al servizio dell'interfaccia; mostrare le interazioni curate; trasformare flussi complessi in racconti visivi chiari; composizione, timing e gerarchia curatissimi. Squarespace "Make the Next" (ManvsMachine, 2022) usa gli oggetti dell'interfaccia (puntatori, contatori di like, bottoni) come elementi grafici del film.

## Le regole, con i numeri (valori di partenza)
| Regola | Valore |
|---|---|
| Schermate | sempre vere (dal prodotto o catturate dal sito), mai disegnate da zero; dati finti ma realistici |
| Cattura | `npx hyperframes capture <url>` per portare un sito dentro il video |
| Zoom sul clic | 1,4-2× sulla zona, 0,4-0,6 s, ease power2.inOut, motion blur leggero durante lo zoom |
| Cursore | si muove ad arco, non in linea retta, 0,4-0,8 s per spostamento; rallenta prima del clic; clic con piccolo cerchio che si espande |
| Schermo nuovo | entra leggermente più grande (102-104%) e si assesta; il taglio cade sul rimbalzo del clic (match cut) |
| Una funzione per scena | 3-5 s ciascuna, con un'etichetta di 2-5 parole |
| Dispositivo | mockup semplice o nessuno; mai dispositivi che distraggono dall'interfaccia |
| Fondo | neutro scuro o il colore del brand, con il prodotto che occupa almeno il 60% del quadro |
| Testo | nella zona sicura e fuori dall'interfaccia, mai sopra i bottoni che si stanno usando |

## Struttura tipo (30-45 s, lancio di una funzione)
1. Il problema in una riga o il risultato finale già sullo schermo (0-3 s)
2. La funzione in azione: 3 interazioni chiave (3-25 s)
3. Il dettaglio che fa la differenza, in zoom (25-35 s)
4. Disponibilità e azione finale (35-45 s)

## Suono
Clic morbidi sincronizzati al fotogramma, whoosh leggeri sugli zoom, una musica elettronica pulita con battito costante (100-120 BPM) su cui tagliare.

## Errori da evitare
- Registrare lo schermo a velocità reale: si accelerano le attese e si rallentano le interazioni importanti.
- Cursore che vaga: ogni movimento va dritto verso un obiettivo.
- Troppe funzioni: oltre 3-4 il pubblico non ne ricorda nessuna.
- Dati veri dei clienti nelle schermate.

## Collegamenti
- Lancio SaaS con estetica a gradienti: categoria 04 nella [mappa](../../MAPPA-STILI.md).
- App bancaria: clip `11-05-app-e-notifica` in [11 Corporate finanza](../11-corporate-finanza/SCHEDA.md).
- Metodo HyperFrames: [manuale](../../manuale/metodo-hyperframes.md).

## Limiti di questa scheda
Nessuna clip ancora ricostruita in codice; le reference sono 3 e vanno ampliate.
