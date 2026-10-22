# 01 · Kinetic typography

Per quando il brief dice: lancio, manifesto, citazione, lyric video, evento, titoli di testa. Il testo è il protagonista: niente illustrazioni a sostegno, la parola fa tutto.

## Le regole, con i numeri
Dalle regole di movimento di HyperFrames (`motion.md`, `film.md`) e dai lavori premiati qui sotto.

| Regola | Valore |
|---|---|
| Parole per scena | 3-7 parole in inglese (in italiano tenersi sul basso: le parole sono più lunghe) |
| Quanto resta una riga | circa 0,5 s + 0,3 s per parola. L'ultima riga del film resta almeno 2 s |
| Dimensione | titolo al 4-9% dell'altezza del quadro; la parola eroe riempie il 60-90% della larghezza |
| Accento | una sola parola accento per scena (colore o peso diverso), mai due |
| Ritmo | in montaggio, tagli ogni 0,13-0,8 s; inquadrature in media 1,8-3 s. Sul beat, non tra un beat e l'altro |
| Blur di movimento | sui movimenti veloci, con il picco nel fotogramma più veloce: 6-12 px sul testo, 15-20 px a tutto quadro |
| Dopo l'arrivo | il titolo arrivato sta fermo. Niente deriva, niente respiro |
| Contatori | un numero che sale dura 1,2-1,6 s |
| Font | 1 display + 1 per il testo, 2 colori più l'accento |

## Sei entrate per i titoli (alternarle dentro lo stesso film)
| Entrata | Come si costruisce |
|---|---|
| Parola per parola, sfocata | ogni parola da blur 6 px a 0 in 0,13 s, 0,067 s tra una parola e l'altra |
| Parola per parola, da grigio | ogni parola passa da grigio chiaro al colore dell'inchiostro |
| Riga intera | tutta la riga entra con un blur unico |
| Lettera per lettera | 0,1 s tra una lettera e l'altra; solo per parole brevi |
| Dietro al soggetto | il testo sta tra lo sfondo e una maschera del soggetto (serve un ritaglio) |
| Slot machine | una sola parola che rotola, circa 0,1 s per giro, e si ferma sulla parola giusta |

## Transizioni che funzionano con il testo
| Transizione | Come si costruisce |
|---|---|
| Colore che allaga | il fondo cambia colore in circa 0,4 s e porta la riga nuova |
| Frusta | una scia di 0,13-0,3 s |
| Morph | un contenitore si allarga nel successivo con blur orizzontale 12→0 |
| Zoom dentro una lettera | la camera entra nel vuoto di una lettera (la O, la A) e il dentro diventa la scena nuova |
| Iride | `clip-path: circle()` che si apre in 0,15 s |
| Dip | il quadro scurisce del 40% per 3 fotogrammi prima del taglio netto |

## Cosa prendere dai premiati
- **Sistemi, non singoli titoli.** I lavori TDC 2024 e D&AD 2025 sono identità in cui la tipografia stessa si deforma, si stira e cambia peso secondo regole fisse (DEMO 2025: globo distorto, sistema di colori RGB, tipografia che evolve). Prima di animare, decidere la regola: cosa fa il testo e perché.
- **Font variabili.** Animare il peso o la larghezza invece di spostare il testo dà movimento senza muovere nulla.
- **Titoli di testa** (Blackwater, Guns and Gulaabs): la tipografia porta il tono del racconto; un solo gesto ripetuto, non dieci effetti.

## Errori da evitare (default che sembrano generati)
- Stessa entrata su ogni scena; tutto che sfuma e sale dal basso.
- Titoli che continuano a scivolare dopo essere arrivati; loop di respiro o galleggiamento.
- Effetto macchina da scrivere su frasi lunghe.
- Testo piccolo al centro con tanto vuoto: se è kinetic type, la parola è enorme.
- Troppe parole in una scena: oltre 7 diventa un sottotitolo.

## Collegamenti
- Primi 2 secondi e gancio: [16 Hook per short](../16-hook-per-short/SCHEDA.md)
- Come costruirlo in codice: [metodo HyperFrames](../../manuale/metodo-hyperframes.md)
- Reference: [reference.csv](reference.csv)
