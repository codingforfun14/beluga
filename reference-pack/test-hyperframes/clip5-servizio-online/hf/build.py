# Inserisce card_track.json (angoli della card esportati da spot_peso.py) in index.html.
import json, os
here = os.path.dirname(os.path.abspath(__file__))
track = json.load(open(os.path.join(here, '..', 'card_track.json')))
src = open(os.path.join(here, 'index.src.txt')).read()
open(os.path.join(here, 'index.html'), 'w').write(src.replace('/*TRACK*/', json.dumps(track, separators=(',', ':'))))
