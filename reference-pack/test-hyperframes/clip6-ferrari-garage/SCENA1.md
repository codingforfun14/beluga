# Scena 1 (0-6 s): pronta da lanciare, NON ancora partita

Cosa c'è: garage buio, la saracinesca sale con la lama di luce sul cemento, il drone entra controluce e rasoterra, l'auto coperta dal telo in primo piano. Camera `C1_saracinesca` (24 mm, f/2.8), lento push in avanti. 180 fotogrammi a 30 fps, 1080p, Eevee qualità finale, motion blur.

Quando fede dice ok, sul Mac in modalità leggera:

```zsh
cd ~/Desktop/DIGITALIZA/beluga/reference-pack/test-hyperframes/clip6-ferrari-garage
W=~/Desktop/DIGITALIZA/render-clip6/scena1
nice -n 19 ~/Applications/Blender.app/Contents/MacOS/Blender -b --factory-startup -t 2 -P spot_garage.py -- $W final 6
PARTIAL=$PWD/progress/scena1.mp4 PARTIAL_GIT=1 ./render_blocchi.sh $W/spot_garage.blend $W 1 180 30 150
```

Il primo comando prepara la scena e calcola il telo solo fino al fotogramma 180. Il secondo renderizza 2 blocchi (1-100, 101-180) e aggiorna `progress/scena1.mp4` dopo ogni blocco. Spazio: meno di 100 MB.
