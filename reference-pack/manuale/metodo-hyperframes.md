# Metodo HyperFrames (test del 2026-10-22)

HyperFrames (HeyGen, Apache-2.0) trasforma una pagina HTML con timeline GSAP in un MP4. Il render è deterministico: ogni fotogramma dipende solo dal tempo. Lo usiamo al posto dei vecchi canvas fatti a mano.

## Installazione
- Container cloud: `npm i -g hyperframes@0.8.185`, poi `hyperframes browser ensure`. Il CDN jsdelivr è bloccato: GSAP va copiato in `assets/js/gsap.min.js` (da `npm pack gsap@3.14.2`).
- Mac di fede: installato con Node 22 via nvm. Prima di usarlo: `nvm use 22`.
- Telemetria spenta: `export HYPERFRAMES_NO_TELEMETRY=1`.
- Skill copiate: hyperframes, hyperframes-cli, hyperframes-registry, media-use.

## Ciclo di lavoro
1. Scrivere `index.html` (meglio generarlo con uno script `genera.py`, come nei test).
2. `hyperframes lint`, poi `hyperframes check` (layout, contrasto, testo leggibile, durata delle righe).
3. `hyperframes snapshot --at 0,1.5,3,...` e guardare il contact sheet. Controllare sempre il fotogramma 0: è la miniatura e l'aggancio.
4. `hyperframes render --quality looks --output x.mp4` (circa 1 minuto per 7 s a 1080×1920 nel container).

## Cosa rende "professionale" (dal test)
- Motion blur vero: `filter: blur()` che sale e scende con il movimento, picco nel fotogramma più veloce (15–20 px a pieno schermo).
- Tagli sul picco del blur: così 3 immagini ferme sembrano una rotazione.
- Ease per ruolo: arrivo `expo.out`, uscita `power3.in`, movimenti di camera `power2.inOut`.
- Grana e vignetta sempre accese, leggere (opacità 0.10–0.13).
- Suono su ogni azione visibile: libreria gratuita di 21 effetti inclusa in HyperFrames (whoosh, pop, impact, glitch, key-press, ping...).
- Testo: almeno 28 px, righe tenute 0.5 s + 0.3 s a parola, l'ultima riga almeno 2 s.

## Asset: cosa serve davvero
- Immagini Kling bastano per: rivelazioni (foto → raggi X), esplosi in 2.5D con strati ritagliati, finte rotazioni con 3 angoli, riflessi, glitch, push-in.
- Serve un video Kling (o 3D vero) per: rotazione continua che mostra lati nuovi, dissolvenze in particelle, stoffa o liquidi fisici, personaggi che recitano (stop-motion stile Telstra).

## Errori incontrati
- `svgOrigin` su un gruppo con clip-path sposta il gruppo: usare `transformOrigin` in px sull'elemento svg.
- `gsap.set` dopo le tween può annullare uno stato iniziale (le gocce erano invisibili).
- Un elemento con `filter` appiattisce il 3D dei figli: il blur va sul contenitore esterno, non su quello con `preserve-3d`.

## Test di riferimento
`reference-pack/test-hyperframes/`: clip1-xray (3D raggi X, stile FutureDeluxe/Nothing), clip2-flat (2D stile BUCK), clip1-v2-immagini (stessa idea con immagini Kling), clip3-spot (mascotte stop-motion stile Telstra, serve il video Kling).
