# Stato del render "Peso"

- Fotogrammi Blender (JPEG 1920×1080, 60 fps, 1–930 = 0–15.5 s): `~/Desktop/DIGITALIZA/render-clip5/frames/f_XXXX.jpg` sul Mac, fuori dal repo.
- Livello HyperFrames già renderizzato (WebM con alfa, 20 s): `~/Desktop/DIGITALIZA/render-clip5/overlay-hf.webm`.
- Il primo render a piena potenza è stato fermato a 168 fotogrammi perché il Mac scaldava troppo. È ripartito in modalità leggera dal 169.

## Riprendere
```
cd reference-pack/test-hyperframes/clip5-servizio-online
./render_light.sh ~/Desktop/DIGITALIZA/render-clip5/frames 1 930 150
```
`nice -n 19`, Blender con `-t 2`, blocchi da 100 fotogrammi e 150 s di pausa tra un blocco e l'altro. I fotogrammi già presenti non vengono rifatti (`use_overwrite=False`, `use_placeholder=True`). Per fermarlo: `pkill -f render_light.sh; pkill -f MacOS/Blender`.
