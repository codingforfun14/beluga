#!/bin/zsh
# Analisi leggera di un video di reference: scarica 720p, misura i tagli, estrae fotogrammi, cancella il video.
# Uso: ana.sh <url> <slug>
URL=$1; SLUG=$2
T=${TMPDIR:-/tmp}/ana-reference
OUT=$HOME/Desktop/DIGITALIZA/beluga/reference-pack/test-hyperframes/frames/$SLUG
FONT=/System/Library/Fonts/HelveticaNeue.ttc
mkdir -p $T $OUT; rm -f $T/v.*(N)
nice -n 19 yt-dlp -q --js-runtimes node --no-playlist -f "bv*[height<=720][ext=mp4]+ba[ext=m4a]/b[height<=720]" --merge-output-format mp4 \
  --write-info-json --no-write-comments -o "$T/v.%(ext)s" "$URL" || exit 1
V=$T/v.mp4
python3 - "$T/v.info.json" > $OUT/info.txt <<'EOF'
import json,sys; d=json.load(open(sys.argv[1]))
print('source:', d.get('webpage_url')); print('title:', d.get('title')); print('channel:', d.get('channel') or d.get('uploader'))
print('upload_date:', d.get('upload_date')); print('views:', d.get('view_count'))
print('description:', (d.get('description') or '').replace('\n',' | ')[:700])
EOF
ffprobe -v error -select_streams v:0 -show_entries stream=width,height,r_frame_rate -show_entries format=duration -of default=nw=1 $V >> $OUT/info.txt
DUR=$(ffprobe -v error -show_entries format=duration -of csv=p=0 $V)
nice -n 19 ffmpeg -nostdin -threads 2 -hide_banner -i $V -vf "select='gt(scene,0.3)',showinfo" -an -f null - 2>&1 | grep -o "pts_time:[0-9.]*" | cut -d: -f2 | awk '{printf "%.2f\n",$1}' > $OUT/cuts.txt
nice -n 19 ffmpeg -nostdin -threads 2 -hide_banner -i $V -vf "select='gt(scene,0.12)',showinfo" -an -f null - 2>&1 | grep -c pts_time | xargs -I{} echo 'scene_changes_soft (soglia 0.12): {}' > $T/soft.txt
N=$(wc -l < $OUT/cuts.txt | tr -d ' ')
python3 - $DUR $N >> $OUT/info.txt <<'EOF'
import sys; d=float(sys.argv[1]); n=int(sys.argv[2])
print(f'scene_cuts: {n} (ffmpeg scene threshold 0.3)'); print(f'average_shot_length_s: {d/(n+1):.2f}')
EOF
# fotogrammi chiave: primo + uno 0.15 s dopo ogni taglio, ridotti a 10 al massimo
python3 - $OUT/cuts.txt $DUR > $T/times.txt <<'EOF'
import sys; c=[float(x) for x in open(sys.argv[1]) if x.strip()]; d=float(sys.argv[2])
t=[0.3]+[x+0.15 for x in c if x+0.15<d-0.1]
if len(t)>10: t=[t[round(i*(len(t)-1)/9)] for i in range(10)]
if len(t)<6: t=[0.3+i*(d-0.6)/7 for i in range(8)]  # piano unico: 8 fotogrammi equidistanti
for x in t: print(f'{x:.2f}')
EOF
rm -f $OUT/scene_*.jpg(N); i=1; : > $OUT/frames_time.txt
for t in $(cat $T/times.txt); do
  f=$(printf "scene_%03d" $i)
  nice -n 19 ffmpeg -nostdin -threads 2 -loglevel error -ss $t -i $V -frames:v 1 -vf scale=960:-2 -q:v 3 $OUT/$f.jpg
  echo "$f $t" >> $OUT/frames_time.txt; i=$((i+1))
done
nice -n 19 ffmpeg -nostdin -threads 2 -loglevel error -i $V -vf "fps=20/$DUR,scale=384:-2,drawtext=fontfile=${FONT}:text='%{pts\:hms}':x=6:y=6:fontsize=18:fontcolor=white:box=1:boxcolor=black@0.6,tile=5x4:padding=3" -frames:v 1 -q:v 3 $OUT/sheet.jpg
cat $T/soft.txt >> $OUT/info.txt
echo "scene frames: frames_time.txt; sheet.jpg: 20 fotogrammi equidistanti con il tempo" >> $OUT/info.txt
rm -f $T/v.*(N)
cat $OUT/info.txt
