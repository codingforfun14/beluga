#!/bin/zsh
# Render leggero a blocchi che occupa poco disco (metodo approvato da fede il 2026-10-25):
# ogni blocco da 100 fotogrammi JPEG viene subito unito in un video H.264 di alta qualita' e i JPEG vengono cancellati.
# Sul disco non restano mai piu' di un blocco di fotogrammi; alla fine i blocchi si uniscono senza ricodifica.
# Riprendibile: i blocchi gia' fatti (blocco_XXXX.mp4) vengono saltati.
# Uso: ./render_blocchi.sh <scena.py> <cartella_lavoro> <da> <a> [fps=30] [pausa_s=150]
#   <scena> puo' essere un .blend (render diretto) oppure uno script che accetta:  -- <cartella/f_> final <fps> <da-a>
SCENE=$1; WORK=$2; FROM=$3; TO=$4; FPS=${5:-30}; PAUSE=${6:-150}
B=$HOME/Applications/Blender.app/Contents/MacOS/Blender
mkdir -p $WORK/frames $WORK/blocchi
for ((s=FROM; s<=TO; s+=100)); do
  e=$((s+99)); ((e>TO)) && e=$TO
  OUTB=$WORK/blocchi/blocco_$(printf %04d $s).mp4
  [[ -s $OUTB ]] && { echo "salto $s-$e (gia' fatto)"; continue; }
  echo "$(date +%T) render $s-$e"
  if [[ $SCENE == *.blend ]]; then
    nice -n 19 $B -b $SCENE -t 2 -o $WORK/frames/f_#### -F JPEG -s $s -e $e -a > $WORK/blender_$s.log 2>&1
  else
    nice -n 19 $B -b --factory-startup -t 2 -P $SCENE -- $WORK/frames/f_ final $FPS $s-$e > $WORK/blender_$s.log 2>&1
  fi
  n=$(ls $WORK/frames/f_*.jpg 2>/dev/null | wc -l | tr -d ' ')
  if (( n != e - s + 1 )); then echo "ERRORE: $n fotogrammi invece di $((e-s+1)), vedi $WORK/blender_$s.log"; exit 1; fi
  nice -n 19 ffmpeg -nostdin -loglevel error -y -threads 2 -framerate $FPS -start_number $s -i $WORK/frames/f_%04d.jpg \
    -c:v libx264 -preset slow -crf 14 -pix_fmt yuv420p -r $FPS $OUTB || { echo "ERRORE ffmpeg"; exit 1; }
  rm -f $WORK/frames/f_*.jpg $WORK/blender_$s.log
  echo "$(date +%T) blocco $s-$e -> $(du -h $OUTB | cut -f1)"
  if [[ -n $PARTIAL ]]; then   # anteprima parziale aggiornata dopo ogni blocco (se la sessione si interrompe resta questa)
    ls $WORK/blocchi/blocco_*.mp4 | sed "s/^/file '/; s/$/'/" > $WORK/blocchi/lista.txt
    ffmpeg -nostdin -loglevel error -y -f concat -safe 0 -i $WORK/blocchi/lista.txt -c copy $PARTIAL
    if [[ -n $PARTIAL_GIT ]]; then
      (cd $(dirname $PARTIAL) && git add $(basename $PARTIAL) && git commit -qm "clip6: animatic parziale fino al fotogramma $e" && \
        { git push -q || { git pull -q --rebase && git push -q; }; }) && echo "$(date +%T) animatic parziale pushato (fino a $e)"
    fi
  fi
  ((e<TO)) && sleep $PAUSE
done
ls $WORK/blocchi/blocco_*.mp4 | sed "s/^/file '/; s/$/'/" > $WORK/blocchi/lista.txt
ffmpeg -nostdin -loglevel error -y -f concat -safe 0 -i $WORK/blocchi/lista.txt -c copy $WORK/render_3d.mp4 && echo "fatto: $WORK/render_3d.mp4 ($(du -h $WORK/render_3d.mp4 | cut -f1))"
