# 16 · Hook per short

I primi 3 secondi di un video verticale (TikTok, Reels, Shorts). Lo scopo è uno solo: fermare il pollice. Tutto il resto del video vale solo se l'hook funziona.

## Le regole, con i numeri

| Regola | Valore | Fonte |
| --- | --- | --- |
| Primo movimento e primo suono | frame 0 | tutti gli outlier vidIQ ott. 2025 - ott. 2026 |
| Hook risolto | entro 2 s | TikTok: il 50% dell'impatto di un annuncio arriva nei primi 2 s |
| Proposta di valore | entro 3 s | TikTok Ads, Creative best practices |
| Brand e messaggio | entro 5 s, presenza del brand al massimo 25% della durata | Meta × Toluna |
| Logo in apertura | no | Vidmob × TikTok: il logo subito abbassa del 14% la visione a 6 s |
| Testo a schermo | 5-10 parole al secondo per i lampi, circa 3 al secondo per frasi da leggere | TikTok Ads |
| Volto in camera | aumenta la visione a 2 s del 14% | Vidmob × TikTok |
| Musica o voce | fino al 13% di conversioni in più; oltre l'80% dei Reels è ascoltato con l'audio | Meta |
| Video sotto 15 s | finale che si ricollega all'inizio (loop) | pattern degli outlier |

## Safe zone a 1080 × 1920

Il testo sta tra y 270 e y 1250, e tra x 80 e x 940. Sotto y 1250 ci sono didascalia e nome dell'account, a destra i bottoni like e commenti. Gli oggetti grafici possono uscire dalla zona, il testo no. Con `"safe": true` nella config le clip mostrano la zona in rosso.

## Le 12 tecniche ricostruite in codice

Ogni clip dura 3 s. Il sorgente è `categoria16.html`, le clip singole sono in `clip/`.

| Clip | Tecnica | Quando usarla | Timing chiave | Reference |
| --- | --- | --- | --- | --- |
| 16.01 | Text slam: parole enormi che entrano sul beat | claim forti, feed senza audio | colpi a 0 / 0,45 / 0,9 s, ingresso in 5 frame da 145% a 100% | 24, 26, 16 |
| 16.02 | Risultato subito: si mostra il finale al frame 0 | tutorial, SaaS, prima e dopo | risultato a f0, CTA a 1,1 s, punch-in a 2,35 s | 12, 15, 18, 20 |
| 16.03 | Tipografia che cade: le lettere fanno quello che dice la parola | showcase di brand, loop | lettere sfalsate di 0,09 s, rimbalzo con schiacciamento | 13, 14 |
| 16.04 | Oggetto che si assembla: pezzi già in volo che formano il logo | lanci di prodotto, chiusure di logo | in volo da f0, forma completa a 1,5 s | 21, 25 |
| 16.05 | Interruzione: scena banale spezzata da un taglio netto | qualsiasi feed dove l'attenzione cala | taglio a 0,6 s con flash, scossa e separazione RGB | 19, 23, 24 |
| 16.06 | Split screen: demo sopra, volto sotto, sottotitoli a parola | recensioni, formazione, reaction | entrambe le metà attive da f0, 6 parole in 2,6 s | 16, 17, 20 |
| 16.07 | Aspetta e guarda: si fa indovinare il risultato | intrattenimento, commenti | domanda leggibile sotto 1 s, risultato a 2,55 s | 22 |
| 16.08 | Domanda aperta: domanda parola per parola | explainer | 0,14 s per parola, punto di domanda a 1,1 s | 18, 23 |
| 16.09 | Numero che esplode: un dato grande che sale | recap, fintech, risultati | conteggio in 1,1 s con sfocatura che sparisce, coriandoli all'arrivo | 5 |
| 16.10 | Prima e dopo: tendina che rivela la versione nuova | trasformazioni, design, grading | "prima" leggibile a f0, tendina da 0,9 a 1,7 s | 28, 29 |
| 16.11 | Swipe nativo: il gesto del telefono come transizione | app, prodotti con interfaccia | dito a 0,2 s, swipe da 0,8 a 1,5 s | 6, 7, 12 |
| 16.12 | Barra di progresso con punch-in | liste, "3 errori che" | un passo al secondo, zoom da 112% a 100% in 0,25 s | nessuna reference citata: tecnica comune ma non verificata |

I numeri nell'ultima colonna rimandano a `reference.csv`.

## Palette e font

- 3-5 colori: un fondo scuro, un bianco, un accento forte e uno secondario. Nella config di default: `#0D0D10`, `#FFFFFF`, `#FF3B2F`, `#FFD23F`.
- Titoli in Anton (condensato, alto impatto), testi in Inter 600-800. Alternative già nel pack: Bebas Neue, Archivo Black, Unbounded.

## Suono (da aggiungere in montaggio)

- Il primo suono parte al frame 0, sullo stesso frame del primo movimento.
- Uno slam vuole un hit sul frame d'impatto, un whoosh che parte 2-4 frame prima.
- A 120 BPM un beat dura 15 frame a 30 fps: i colpi dello slam a 0,45 s sono quasi un beat a 133 BPM.
- Mix a -14 LUFS integrati, picco a -1 dBTP.

## Errori da evitare

- Aprire con il logo o con una schermata lenta di introduzione.
- Testo sotto y 1250 o sopra y 270.
- Movimenti lineari: ogni movimento ha la sua curva di easing.
- Far arrivare tutti gli elementi nello stesso frame.
- Un hook che promette qualcosa che il video non mantiene.

## Come usarle

```
cd reference-pack
node tools/render.mjs categorie/16-hook-per-short/categoria16.html out.mp4 30 categorie/16-hook-per-short/esempio-config.json
node tools/render.mjs categorie/16-hook-per-short/categoria16.html slam.mp4 30 mia-config.json --scene 1
```

In `esempio-config.json` si cambiano colori, brand e testi senza toccare il codice. Le chiavi dei testi sono in cima a `categoria16.html`, nell'oggetto `t`.

## Limiti di questa scheda

- I tempi delle reference sono stime a 30 fps ricavate dalle descrizioni, non misure frame per frame.
- Molti link Instagram sono costruiti dall'ID e non aperti: nel CSV hanno `stato_url = da verificare`.
- Non ci sono studi ufficiali recenti su Reels e Shorts per i primi 1-3 secondi: i dati più solidi sono TikTok 2023 e Meta 2025.
