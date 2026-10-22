# Indice: dal brief alla categoria

Si parte da qui per ogni nuova idea. Si scelgono 1-3 categorie, si apre la loro `SCHEDA.md` e il `reference.csv`, e si parte dalle clip in `clip/`.

## Da dove parte il creative director

Prima di scegliere una categoria si segue il [metodo di direzione creativa](direzione-creativa/METODO.md): brief, insight, tre territori, direzione artistica, storyboard, review. Modelli pronti in `direzione-creativa/modelli/`.

## Focus attuale (priorità di fede)
| Quando il brief dice | Apri | Cosa c'è |
|---|---|---|
| 3D, prodotto premium, brand film, ident, simulazione | [Motion design 3D](focus/3d-motion/SCHEDA.md) | scheda, 24 reference, catalogo skill |
| spot, campagna, TV, YouTube, social a pagamento | [Spot pubblicitari](focus/spot/SCHEDA.md) | scheda, 35 reference, 7 analisi spot per spot, regole di efficacia, catalogo skill |

## Categorie di stile

| Se il brief dice... | Categoria | Stato |
| --- | --- | --- |
| reel, TikTok, Shorts, "deve fermare lo scroll", lancio social | [16 Hook per short](categorie/16-hook-per-short/SCHEDA.md) | completa: scheda, 29 reference, 12 clip 9:16 con parametri |
| finanza, banca, investimenti, tono serio e affidabile | [11 Corporate finanza](categorie/11-corporate-finanza/SCHEDA.md) | scheda, 4 reference, 12 clip 16:9, 61 stock con licenza |
| fatto a mano, appunti, lavagna, tono umano | [05 Disegnato a mano](categorie/05-disegnato-a-mano/SCHEDA.md) | scheda, 6 reference, 12 clip 16:9 |
| spiegare come funziona, app o servizio nuovo, scienza, formazione | [02 Explainer flat](categorie/02-explainer-flat/SCHEDA.md) | scheda, 5 reference |
| app, software, funzione nuova, lancio SaaS, walkthrough | [09 Demo UI e prodotto](categorie/09-demo-ui-prodotto/SCHEDA.md) | scheda, 3 reference |
| "perché succede", storia, documentario, giornalismo | [06 Collage e carta](categorie/06-collage-carta/SCHEDA.md) | scheda, 7 reference, skill vox-explainer |
| lancio, manifesto, citazione, lyric video, titoli di testa | [01 Kinetic typography](categorie/01-kinetic-typography/SCHEDA.md) | scheda, 9 reference |
| tech amichevole, prodotto simpatico, clay, plastilina, 3D pastello | [03 3D morbido e clay](categorie/03-3d-morbido-clay/SCHEDA.md) | scheda, 6 reference |
| mascotte, personaggio, serie con lo stesso protagonista, spot con dialogo | [Mascotte con Kling](categorie/mascotte-kling/SCHEDA.md) | scheda, 5 reference, prompt base, test spot in `test-hyperframes/clip3-spot` |

Tutti i 20 stili, con firma visiva e quando usarli, sono nella [mappa degli stili](MAPPA-STILI.md). Le schede mancanti arrivano una per sessione.

## Regole valide per tutto

- [Principi di movimento](manuale/principi-motion.md): easing, durate, ritmo.
- [Formati e safe zone](manuale/formati-e-safe-zone.md): 9:16, 4:5, 1:1, 16:9, testo e sottotitoli.
- [Suono](manuale/sound-design.md): livelli e sincronia.
- [Checklist prima della consegna](manuale/checklist-qualita.md).
- [Metodo HyperFrames](manuale/metodo-hyperframes.md): installazione, ciclo di lavoro, cosa rende un clip professionale, quando servono immagini o video Kling.
- [Skill e strumenti da installare](skill/DA-INSTALLARE.md).

## Colonne di ogni reference.csv

`id, titolo, autore, anno, piattaforma, url, stato_url, tecnica, frame_1, timing, suono, cosa_prendere, licenza, fonte`

`stato_url` vale `aperto` quando il link è stato verificato e `da verificare` quando è stato ricostruito. `licenza` dice se è solo ispirazione (opera di terzi) o materiale usabile.

## Render

```
cd reference-pack
node tools/render.mjs <categoria>.html out.mp4 [fps] [config.json] [--scene N]
```

Le clip nuove dichiarano `window.W` e `window.H`, quindi lo stesso script fa 9:16, 16:9 e 1:1. La config JSON cambia colori, testi e brand senza toccare il codice.
