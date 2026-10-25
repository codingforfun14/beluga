# Dropbox, "Do more than store with Dropbox"

## Scheda
Dropbox, 2024 (caricato il 2024-03-06 sul canale Dropbox, circa 10 mila visualizzazioni). 60 s, 1280×720 a 30 fps nella copia analizzata. Studio non indicato nella descrizione. Link: https://youtu.be/stVA57Rf4aM. Fotogrammi in `test-hyperframes/frames/dropbox-more-than-store/` (sheet.jpg, keyframes.jpg, scene_*.jpg).

## L'idea in una riga
L'interfaccia di Dropbox diventa un luogo fisico: finestre, cartelle, firme e commenti sono oggetti 3D in una stanza lilla piena di luce, e la camera ci vola dentro.

## Stile visivo (misurato sui fotogrammi)
- **Palette:** lilla e azzurro pervinca (circa #C9CCF5 → #3D5AFE), bianco latte, un solo accento blu Dropbox (#0061FE). Nella parte "creativa" (36–45 s) entrano nero lucido, verde lime, rosso e lilla scuro.
- **Luce:** morbida, da grande finestra fuori campo, con **ombre di veneziane** che attraversano pareti e oggetti (9 s, 12 s, 48 s). Bloom leggero sui bianchi, niente ombre dure.
- **Materiali:** plastica satinata e vetro smerigliato per le card UI; superfici gonfie e lucide (gomma, palloncino) per le icone; un tubo nero laccato che disegna la firma.
- **Camera:** dolly e orbite lente con profondità di campo corta; un unico movimento lungo per scena, con fuoco che passa da un oggetto all'altro.

## Ritmo (misurato)
18 tagli a soglia 0.3 in 60 s, **inquadratura media 3.2 s**; 27 cambi a soglia 0.12 (dissolvenze e zoom dentro la UI). Tagli a 6.4, 8.4, 10.6–10.8 (raffica di 4), 21.2, 23.6, 27.6, 35.7, 37.3, 38.5, 39.5, 42.6, 44.5, 49.0, 56.8 s. Il ritmo accelera solo nella sezione video/creatività (35–45 s, 6 tagli in 9 s).

## Beat
| s | Cosa succede |
|---|---|
| 0–3 | logo Dropbox di vetro luminoso su fondo lilla, si apre in fogli |
| 3–9 | fogli bianchi in controluce, poi la finestra di Dropbox fluttua nella stanza con avatar e icone |
| 9–21 | muro di file che si sincronizzano (icone di sync blu, avatar colorati), molla 3D in bianco e nero |
| 21–35 | la UI in macro: "Create folder", "Edit PDF", un contratto che viene firmato; la firma diventa un tubo nero 3D |
| 35–45 | esplosione creativa: forme gonfie, pesci, stelle, un player video con commenti e annotazioni |
| 45–57 | ritorno alla finestra Dropbox nella stanza, gli oggetti rientrano nelle cartelle |
| 57–60 | logo blu su bianco |

## Tipografia
Quella del prodotto (Sharp Grotesk/Atlas di Dropbox): la UI è il testo. Nessun claim a tutto schermo; il prodotto parla da solo.

## Transizioni
Zoom dentro un elemento della UI che diventa la scena successiva; oggetti che attraversano la camera; un taglio a nero con la scena in finestra (39 s).

## Suono
Non ascoltato in questa analisi (solo fotogrammi). Probabile musica elettronica morbida con effetti UI (click, whoosh): da verificare.

## Tecnica probabile
3D completo (Cinema 4D o Blender con Redshift/Octane), UI ricostruita come geometria con texture, simulazioni morbide per gli oggetti gonfi, compositing con bloom e grana. Nessun live action, nessuna AI visibile.

## Come lo replichiamo
- **Blender (Eevee):** la stanza lilla con le veneziane è quasi identica all'ufficio di `clip5/ufficio_still.py` (stessa luce di sole attraverso le lamelle). Le card UI sono piani con angoli arrotondati e materiale vetro smerigliato o plastica, con lo screenshot dell'interfaccia come texture. Gli oggetti gonfi si fanno con Cloth + pressione o con un Subdivision su forme semplici. Il tubo-firma è una curva con bevel animata con `bevel_factor_end`.
- **HyperFrames/GSAP:** testi UI nitidi sopra il 3D (cursore, menu "Share", commenti), agganciati con la tecnica a omografia già usata per la card di "Peso" (`card_track.json`).
- **Kling:** non serve. Il look dipende da materiali e luce controllati, che in Blender sono ripetibili; con Kling le UI si deformerebbero.
- **Asset CC0:** HDRI interno luminoso da Poly Haven (da scaricare con ok), font di sistema o Google Fonts. Le UI sono nostre (brand inventato).
- **Difficoltà:** media. La parte difficile sono i materiali vetro/plastica puliti senza rumore.
- **Render sul Mac:** circa 2–3 s a fotogramma a 1080p con Eevee (scene semplici e luminose). Un test di 10 s a 30 fps fa 300 fotogrammi, cioè 15 minuti in modalità leggera.

## Cosa rubare
- **La UI come luogo**: per un servizio online è il modo più diretto di "mostrare l'invisibile" senza un prodotto fisico.
- Una sola luce morbida con le ombre delle veneziane basta a dare atmosfera e coerenza a tutto lo spot.
- L'accento colorato arriva solo nel momento "creativo", per contrasto con 30 s di lilla calmo.
