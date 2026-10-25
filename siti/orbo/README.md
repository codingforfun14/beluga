# ORBO One: sito 3D di prova

Marchio inventato per uno studio di design. Il sito mostra l'auricolare che si smonta mentre scorri la pagina.

- `blender/orbo_model.py`: modello procedurale e render statici (`--shot hero|pair|macro`).
- `blender/orbo_explode.py`: animazione dell'esploso (120 frame) e `--track` per le posizioni dei pezzi.
- `site/page.html`: la pagina. `site/build.sh` crea `site/index.html` per GitHub Pages.
- `site/frames/`: i fotogrammi WebP. Ora sono quelli di prova a 960x540: per il render finale basta sostituirli con lo stesso nome.

Rigenerare i fotogrammi (serve `pip install bpy`, Python 3.13):

    python blender/orbo_explode.py --out /tmp/f_#### --samples 128 --res 1920 1080
    python blender/orbo_explode.py --out x --track site/track.json
