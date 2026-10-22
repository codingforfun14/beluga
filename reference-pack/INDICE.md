# Indice: dal brief alla categoria

Si parte da qui per ogni nuova idea. Si scelgono 1-3 categorie, si apre la loro `SCHEDA.md` e il `reference.csv`, e si parte dalle clip in `clip/`.

| Se il brief dice... | Categoria | Stato |
| --- | --- | --- |
| reel, TikTok, Shorts, "deve fermare lo scroll", lancio social | [16 Hook per short](categorie/16-hook-per-short/SCHEDA.md) | completa: scheda, 29 reference, 12 clip 9:16 con parametri |
| finanza, banca, investimenti, tono serio e affidabile | [11 Corporate finanza](categorie/11-corporate-finanza/) | 12 clip 16:9, scheda da scrivere |
| fatto a mano, appunti, lavagna, tono umano | [05 Disegnato a mano](categorie/05-disegnato-a-mano/) | 12 clip 16:9, scheda da scrivere |

Le altre 17 categorie del piano arrivano una per sessione.

## Regole valide per tutto

- [Principi di movimento](manuale/principi-motion.md): easing, durate, ritmo.
- [Formati e safe zone](manuale/formati-e-safe-zone.md): 9:16, 4:5, 1:1, 16:9, testo e sottotitoli.
- [Suono](manuale/sound-design.md): livelli e sincronia.
- [Checklist prima della consegna](manuale/checklist-qualita.md).
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
