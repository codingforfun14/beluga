# Servizio locale di Niko

Prima fase: dalla chat parte un agente vero (l'Ideatore), il risultato viene controllato, salvato per versione e mostrato nella chat e in Lavori.

## Accendere e spegnere

```
cd ~/Desktop/DIGITALIZA/beluga
npm start
```

Poi apri **http://127.0.0.1:4170** nel browser. Per spegnere: `Ctrl+C` nel Terminale.

Se apri `app/index.html` con il doppio clic vedi la **demo** con i dati di esempio: lì non parte niente.

## Prove automatiche

```
npm test
```

Usano un agente finto in una cartella temporanea: non toccano i tuoi incarichi e non consumano messaggi.

## Dove finiscono le cose

- `tasks/<id>.json`: l'incarico (stato, versione, errore, risultato).
- `tasks/<id>.log`: gli eventi dell'incarico, solo in aggiunta.
- `tasks/chat.jsonl`: la chat con Niko.
- `projects/<progetto>/work/<id>/v01/`: `prompt.md` (cosa ha ricevuto l'agente), `risposta-agente.txt` o `risposta-manuale.txt`, `idee.json` e `idee.md`.
- `projects/<progetto>/libreria.json`: la Libreria del progetto.

## Chi fa cosa

È deciso in `modelli.json`. Per ora l'Ideatore è **Claude, temporaneo**: serve a provare il collegamento. Il definitivo sarà Codex, quando sarà verificato con l'account della scuola: basta cambiare `"programma": "claude"` in `"codex"`. Se `claude` o `codex` non sono nel PATH, scrivi il percorso completo in `programmi.<nome>.percorso`.

## Sicurezza

- Il servizio ascolta solo su 127.0.0.1.
- Le scritture accettano solo richieste della pagina stessa: serve un header apposito, il corpo deve essere JSON e l'Origin deve essere il nostro. Gli host diversi da 127.0.0.1 e localhost vengono rifiutati.
- Il browser non può mandare comandi né leggere file a piacere. Vengono serviti solo i file di `app/`.
- I programmi partono con argomenti separati, senza shell, e il prompt passa su stdin. Claude gira senza strumenti (`--tools ""`) dentro una cartella temporanea dell'incarico, che poi viene cancellata.

## Limiti di questa fase

- Niko smista le richieste con regole semplici: capisce solo le richieste di idee. Video, Blender e render arrivano dopo.
- Il Revisore non è ancora attivo. Il "Controllo" che vedi nelle schede è il controllo automatico del formato: 3 idee, ognuna con titolo, hook, sviluppo e direzione visiva.
- L'adattatore di Codex è scritto ma non è provato, perché Codex non è installato.
- Un incarico alla volta. Non ci sono tentativi automatici: se un agente non risponde, l'incarico si ferma e puoi usare il piano B o "Riprova".

## Modello di Codex
Se Codex risponde che il modello "non è supportato con un account ChatGPT", in `modelli.json` aggiungi
`"modello": "<nome>"` sotto `programmi.codex`. Niko lo passa con `--model` solo per le sue chiamate,
senza cambiare il tuo `~/.codex/config.toml`. I modelli disponibili per il tuo account si vedono con `codex debug models`.
