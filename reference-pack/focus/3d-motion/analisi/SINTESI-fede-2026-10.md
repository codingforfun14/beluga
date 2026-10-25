# Sintesi delle 6 reference di fede (ottobre 2026)

Video mandati da fede il 2026-10-25 come modello per i video in motion graphics di servizi online. Analisi singole in questa cartella; fotogrammi, tagli e contact sheet in `test-hyperframes/frames/<slug>/`. Tutti i numeri sono misurati con ffmpeg (scene detection a soglia 0.3, e 0.12 per i cambi morbidi). Il suono non è stato ascoltato: è da verificare.

| Video | Durata | Tagli (0.3) | Inquadratura media | Tecnica |
|---|---|---|---|---|
| [Google, Gemini era](google-gemini-era.md) (2024) | 60 s | 23 | 2.5 s | UI 2.5D + live action + inserti 3D |
| [Housing.com, Look Up](housing-look-up.md) (2015) | 60 s | 0 | piano unico | 2D/2.5D, particelle |
| [Burger King, rebrand](burger-king-rebrand.md) (2021) | 84 s | 79 | 1.05 s | kinetic type + foto di prodotto |
| [Intel, nuovo brand](intel-transforms-brand.md) (2020) | 60 s | 27 | 2.1 s | testo-maschera + badge 3D + live action |
| [PayPal, How it works](paypal-how-it-works.md) (2015) | 74 s | 0 | piano unico | explainer 2D a icone |
| [Dropbox, Do more than store](dropbox-more-than-store.md) (2024) | 60 s | 18 | 3.2 s | 3D completo, la UI come luogo |

## Cosa hanno in comune
1. **Il servizio non si vede, quindi si mostra l'interfaccia o un suo simbolo.** Barra di ricerca (Google, Housing), finestre e card (Dropbox), icone (PayPal), un pezzo del logo (Intel, Housing).
2. **Fondi pieni e palette di brand strette**: 3–5 colori, uno per capitolo; un solo accento forte.
3. **La tipografia è un personaggio**, non una didascalia: parole enormi, una per volta, che si scrivono, si gonfiano o fanno da finestra.
4. **Continuità più dei tagli**: due su sei sono piani unici, e gli altri usano morph e zoom dentro la UI più che stacchi. I tagli veloci arrivano solo dove c'è un beat.
5. **Un elemento che viaggia** fa da filo: la freccia di Housing, il quadratino di Intel, la stella di Gemini, il blu di Dropbox.
6. **Finale sempre uguale**: logo su fondo pieno, 3–5 s, fermo.

## Le tecniche ricorrenti da imparare (in ordine di utilità per noi)
1. **Interfaccia che si trasforma** (Google, Dropbox, PayPal): elementi UI che escono, si espandono e diventano la scena successiva. → HyperFrames/GSAP con `Flip`, `clip-path` e stagger.
2. **UI in uno spazio 3D con luce morbida** (Dropbox): card di vetro o plastica in una stanza luminosa, ombre di veneziane, profondità di campo. → Blender Eevee + UI agganciata con omografia (già fatto in "Peso").
3. **Kinetic type sul beat** (Burger King, Intel): una parola per inquadratura, montata sui tempi della musica. → HyperFrames con l'array dei beat.
4. **Testo come maschera su immagini** (Intel). → CSS `mask`/`background-clip: text` su `<video>`.
5. **Icone a linea che si disegnano e wipe di colore** (PayPal). → SVG `stroke-dashoffset`, `clip-path: polygon()`.
6. **Un simbolo che viaggia in piano unico** (Housing). → morph di path SVG + particelle Three.js lungo una curva.
7. **Testo che si scrive come un'AI** (Google): gradiente o cursore che avanza, parole a pezzi. → SplitText-like in GSAP.
8. **Inserto "materico" breve** (Google 6 s, Dropbox): la UI che diventa tessuto, vetro o un oggetto gonfio per 1–2 s. → Blender (displacement, cloth con pressione).

## Due test da 10 s proposti (per PRATICA, brand inventato)
**Test A, "La spunta che viaggia"** (tecniche 1, 5, 6, 7; solo HyperFrames, il Mac non si scalda)
- 0–2 s: barra "Cerca: 730, bollette, ricorso…" che si scrive da sola su fondo crema.
- 2–6 s: la spunta arancione ✓ esce dalla barra e viaggia in piano unico: diventa una busta, un modulo che si compila (icone a linea), un timbro.
- 6–8.5 s: wipe arancione a tutto schermo, "Inviata." enorme.
- 8.5–10 s: logo PRATICA fermo.
- Render: 1–2 minuti a un worker. Nessun asset esterno.

**Test B, "La stanza di PRATICA"** (tecniche 2, 3, 8; Blender + HyperFrames)
- Una stanza lilla-crema con le veneziane (la stessa luce dell'ufficio di "Peso"), card della UI di PRATICA di vetro smerigliato che fluttuano e si ordinano.
- 0–3 s: dolly lento tra le card; 3–5 s: una card si gonfia e diventa un modulo 3D che si piega (inserto materico); 5–8 s: tre parole sul beat, "Moduli." "Code." "Fatto."; 8–10 s: logo.
- Render: circa 300 fotogrammi a 30 fps, 2–3 s l'uno in Eevee, cioè circa 15 minuti in modalità leggera (nice 19, 2 thread, blocchi con pausa).

Nessuno dei due richiede Kling o ElevenLabs. Il suono si fa sintetico in ffmpeg come per "Peso".
