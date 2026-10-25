#!/bin/zsh
# Render leggero e riprendibile: nice 19, 2 thread, blocchi da 100 fotogrammi con pausa.
# I fotogrammi gia' presenti non vengono rifatti (use_overwrite=False nello script).
# Uso: ./render_light.sh <cartella_fotogrammi> [da] [a] [pausa_s]
OUT=${1:-$HOME/Desktop/DIGITALIZA/render-clip5/frames}; FROM=${2:-1}; TO=${3:-930}; PAUSE=${4:-150}
B=$HOME/Applications/Blender.app/Contents/MacOS/Blender
HERE=${0:A:h}
for ((s=FROM; s<=TO; s+=100)); do
  e=$((s+99)); ((e>TO)) && e=$TO
  echo "$(date +%T) blocco $s-$e"
  nice -n 19 $B -b --factory-startup -t 2 -P $HERE/spot_peso.py -- $OUT/f_ final 60 $s-$e > /dev/null 2>&1
  echo "$(date +%T) fatti: $(ls $OUT | wc -l)"
  ((e<TO)) && sleep $PAUSE
done
