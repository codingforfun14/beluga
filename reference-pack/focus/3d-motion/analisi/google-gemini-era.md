# Google, "Welcome to the Gemini era"

## Scheda
Google, maggio 2024, film di apertura del Google I/O 2024 (canale Google, 55,6 milioni di visualizzazioni). 60 s, 1280×720 a 29,97 fps nella copia analizzata. Link: https://www.youtube.com/watch?v=_fuimO6ErKI. Fotogrammi in `test-hyperframes/frames/google-gemini-era/`.

## L'idea in una riga
La homepage di Google si trasforma davanti a noi: dalla barra di ricerca escono i "chip" di Gemini, e l'AI entra nelle vite vere delle persone.

## Stile visivo (misurato sui fotogrammi)
- **Palette:** bianco Google e i quattro colori del logo nella prima parte; poi il gradiente Gemini blu → viola → rosa (stella a quattro punte) e una sezione scura (nero con gradienti sfocati) per la parte "creativa".
- **Luce:** UI piatta e luminosa; nelle parti live action, luce naturale calda.
- **Materiali:** superfici della UI che diventano tessuto iridescente (6 s), vetro sfocato, glow.
- **Camera:** zoom e pan dentro la UI (spazio 2.5D), poi live action a mano con primi piani.

## Ritmo (misurato)
23 tagli a soglia 0.3, **inquadratura media 2.5 s**; 66 cambi a soglia 0.12 (la UI si trasforma di continuo anche senza taglio). Raffica di tagli a 5.4–6.5 s (6 in 1.1 s) quando la UI "esplode" nei chip; poi tagli ogni 1–7 s nella parte live action.

## Beat
| s | Cosa succede |
|---|---|
| 0–5.4 | homepage Google classica; i chip ("Break it down", "Generate", "Help me write") escono dal logo e dalla barra |
| 5.4–6.5 | raffica: la UI diventa materia (tessuto iridescente), stella Gemini enorme |
| 6.5–15 | parole che si scrivono ("Help me write", "Generate"), barra Search con la stella |
| 15–30 | live action: persone che usano Gemini (lavagna, podcast, shopping, sport) alternate a schermi |
| 30–50 | UI in primo piano (riassunto email, "Simpler / Break it down"), video in 3D di una città |
| 50–60 | "Welcome to the Gemini era" su nero, logo G |

## Tipografia
Google Sans, grande e arrotondata; il testo appare come se fosse scritto in tempo reale (effetto streaming dell'AI) con un cursore o un gradiente che avanza.

## Transizioni
Morph della UI (un elemento diventa il successivo), zoom attraverso uno schermo dentro la scena live action, glow che copre il taglio.

## Suono
Non ascoltato in questa analisi. È un film d'apertura di keynote: probabile musica epica con crescendo, da verificare.

## Tecnica probabile
Motion 2D/2.5D della UI (After Effects) + live action girato apposta + alcuni passaggi 3D (città in fotogrammetria/Google Earth, materiali iridescenti). L'"AI" è raccontata con la tipografia che si scrive da sola.

## Come lo replichiamo
- **HyperFrames/GSAP:** quasi tutta la parte UI: chip che escono da una barra (stagger con `back.out`), testo che si scrive a pezzi con un gradiente che avanza, stella a quattro punte in SVG con gradiente. È il punto di forza di HyperFrames.
- **Blender:** solo il momento "materia" (la UI che diventa tessuto o vetro iridescente): un piano con la texture della UI, displacement animato e materiale thin-film. È un breve inserto di 1–2 s.
- **Kling:** le scene live action di persone (circa 4–6 clip da 5 s). Stima indicativa 4–6 generazioni a qualità standard, da verificare sul listino attuale. Va usato solo se fede lo approva, oppure le scene si sostituiscono con stock CC0 di Pexels.
- **Asset CC0:** clip live action da Pexels (con ok per il download), font Google Fonts (Google Sans non è libera, si usa Plus Jakarta o Inter).
- **Difficoltà:** bassa per la UI, media per l'inserto materico.
- **Render sul Mac:** HyperFrames 10 s a 60 fps in 1–2 minuti a un worker; l'inserto Blender di 2 s in circa 5 minuti.

## Cosa rubare
- **La UI che si trasforma è già una storia**: barra di ricerca → chip → risultato, senza bisogno di metafore.
- Testo che si scrive da solo come firma del "servizio intelligente".
- Una raffica di 6 tagli in un secondo come detonatore, poi ritmo regolare.
