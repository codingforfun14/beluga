# ORBO One: sito 3D di prova

Marchio inventato per uno studio di design. Il sito mostra l'auricolare che si smonta mentre scorri la pagina, poi lo pesa su una bilancia, mostra i numeri animati, le finiture e la pagina d'acquisto.

- `blender/orbo_model.py`: modello procedurale, materiali, luci e render statici.
- `blender/orbo_explode.py`: esploso (120 frame) e `--track` per le posizioni dei pezzi a schermo.
- `blender/orbo_plan_renders.py`: foto dei pezzi (`--shot part_cap|part_upper|part_battery|part_driver|chip`), finiture, custodia.
- `blender/orbo_sequences.py`: sequenze per lo scroll, bilancia (60 frame + `lcd.json`) e custodia che si apre (40 frame).
- `site/page.html`: la pagina. `site/build.sh` crea `site/index.html` per GitHub Pages.
- `site/frames/`, `site/scale/`, `site/case/`: fotogrammi WebP. `site/img/`: foto dei pezzi e finiture.
- `mockup-v2/`: le prove del piano.

Rigenerare (serve `pip install bpy`, Python 3.13):

    python blender/orbo_explode.py --out /tmp/ex/f_#### --samples 48 --res 1600 900
    python blender/orbo_explode.py --out x --track site/track.json
    python blender/orbo_sequences.py --seq scale --out /tmp/scale --samples 40 --res 1280 800
    python blender/orbo_sequences.py --seq case --out /tmp/case --samples 40 --res 1280 800

Poi converti i PNG in WebP con lo stesso nome (`ffmpeg -i f_0001.png -quality 78 f_0001.webp`).
