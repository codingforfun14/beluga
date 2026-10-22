# 11 · Corporate finanza

Per quando il brief dice: banca, investimenti, assicurazioni, fintech, B2B serio, "affidabile", "trasparente".

## Le regole, con i numeri
| Regola | Valore |
|---|---|
| Movimento | lento e preciso, ease in-out (power2/quart), nessun rimbalzo |
| Durata clip | 4 s ciascuna, formato 16:9 a 1280×720 |
| Numeri | contano fino al valore finale in 1-1,5 s, poi restano fermi |
| Grafici | linee e barre crescono da sinistra a destra, ease in-out, etichetta del valore finale con fonte |
| Spazio | margini ampi (almeno 8% del lato), una sola idea per schermata |
| Contrasto | testo bianco su navy o navy su grigio chiaro, almeno 4,5:1 |

## Le 12 tecniche ricostruite in codice
| # | Clip | Cosa fa | Quando usarla |
|---|---|---|---|
| 01 | claim istituzionale | sopratitolo, claim su due righe, sottotitolo | apertura |
| 02 | KPI che crescono | 3 card con numeri e mini grafici | risultati, report |
| 03 | grafico con cursore | area chart con cursore e valore | andamento di un fondo |
| 04 | carta con riflesso | carta di pagamento che ruota con riflesso | prodotto carta, conto |
| 05 | app e notifica | telefono con saldo e notifica di pagamento | app bancaria |
| 06 | mappa immobili | mappa con prezzi e scheda immobile | real estate |
| 07 | edificio wireframe | edificio in linee con rendimento | investimento immobiliare |
| 08 | sicurezza dati | scudo con spunta ed elenco garanzie | privacy, sicurezza |
| 09 | allocazione portafoglio | ciambella che si compone con legenda | profilo di rischio |
| 10 | confronto costi | barre a confronto con risparmio | prezzo, commissioni |
| 11 | processo tre passi | 3 passi collegati da una linea | onboarding, "come funziona" |
| 12 | chiusura logo e disclaimer | logo, claim, sito, nota legale | chiusura obbligatoria |

File: `clip/11-*.mp4`, sorgente `categoria11.html`, anteprima `contact_sheet_11.jpg`.

## Palette e font
- Navy #0B1F3A e #132C4F, verde acqua #19C2A0 come accento, oro #C9A227 solo per un dettaglio, grigio chiaro #F5F7FA, testo secondario #6B7A90.
- Font (già nel pack, OFL): Inter 300/500/600/700 per tutto, DM Serif Display solo per un titolo istituzionale.

## Stock con licenza commerciale
`stock_commerciale_finanza.csv`: 61 video Pexels e altri, con link di download e licenza, divisi per tema (trading, città, persone, firma).

## Suono
Musica corporate calma (pianoforte e archi leggeri o elettronica pulita, 90-110 BPM). Effetti discreti: tick dei contatori, swoosh morbidi, un chime sul logo. Niente impatti forti.

## Errori da evitare
- Rimbalzi e ease elastici: tolgono serietà.
- Numeri senza fonte o senza data: in finanza sono anche un rischio legale.
- Disclaimer illeggibile: va tenuto abbastanza a lungo e nella zona sicura.
- Troppo verde "denaro": l'accento è uno solo.

## Come usarle
`node ../../tools/render.mjs categoria11.html out.mp4 30 [config.json] [--scene N]`. Per il verticale e per i nuovi progetti conviene rifare la tecnica in HyperFrames ([metodo](../../manuale/metodo-hyperframes.md)).

## Limiti di questa scheda
Mancano ancora le reference esterne (`reference.csv`) e le clip in 9:16. I numeri nelle clip sono esempi, non dati reali.
