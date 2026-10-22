# Clip 3: spot con mascotte, stile Telstra (stop-motion)

Reference: Telstra "Better on a better network" (Revolver, Cannes Lions 2025 Grand Prix Animation). Fotogrammi in `../frames/telstra/`.

Cosa prendiamo: pupazzo di feltro su un paesaggio in miniatura realistico, cielo coperto, camera ferma, personaggio impassibile, battuta secca con sottotitolo bianco, logo che arriva come un adesivo alla fine.

## Prompt Kling (3.0, 9:16, 5 s, text-to-video o image-to-video)

Stop-motion animation. A handmade felt and wool puppet of a small white beluga whale wearing a knitted red-and-cream striped sweater, sitting on a miniature rocky coastline with moss and tiny bushes. Overcast grey sky, soft diffuse daylight, fog over the sea behind. Locked-off static camera, medium shot, the character in the lower half of the frame. The beluga slowly blinks, turns its head to the camera and gives a tiny deadpan nod. Stop-motion feel: animated on twos, slight frame-to-frame jitter in the fabric fibres, visible felt texture, miniature scale, shallow depth of field, handcrafted like Aardman or Laika. No text, no logos.

Negative: CGI, smooth 3D render, glossy plastic, 2D cartoon, text, watermark, morphing, extra limbs.

## Come si monta

1. Salva il video come `assets/mascotte.mp4`.
2. Passo due vero (12 fps): `ffmpeg -i kling.mp4 -vf "fps=12,scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920" -r 30 -an assets/mascotte.mp4`
3. `npx hyperframes render --quality looks --output clip3-spot.mp4`

Le battute dei sottotitoli sono segnaposto: si cambiano in `index.html`.
