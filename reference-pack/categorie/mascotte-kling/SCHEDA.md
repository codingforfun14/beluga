# Mascotte di brand con Kling

Per quando il brief dice: personaggio, mascotte, serie social con lo stesso protagonista, tono ironico, spot con dialogo.

## Perché funziona (con fonti)
- Le campagne con mascotte hanno il 37% di probabilità in più di legare il messaggio al brand e il 30% in più di catturare l'attenzione (Ipsos 2023, citato da [Frontify](https://www.frontify.com/en/futures/how-mascots-became-the-secret-sauce-for-successful-brands)).
- Duolingo: la "morte" e la resurrezione del gufo Duo su TikTok nel 2025, con un +40% di abbonati paganti anno su anno secondo lo stesso articolo.
- Telstra: 26 spot in stop-motion con animali di feltro, Grand Prix Animation a Cannes Lions 2025. Fotogrammi in `../../test-hyperframes/frames/telstra/`.

## Le regole del personaggio
1. Una sagoma riconoscibile anche nera su bianco (prova: silhouette a 64 px).
2. Al massimo 3 colori propri più un accessorio fisso (es. maglione a righe). L'accessorio è ciò che Kling tiene più stabile.
3. Una personalità in una frase, con un difetto (es. "impassibile, sempre un po' deluso"). L'umorismo nasce dal difetto.
4. Un materiale deciso: feltro e lana (stop-motion), plastilina, vinile da collezione, 2D piatto. Mai "3D generico".
5. Un mondo fisso: stessa luce, stessa scala, stessi set ricorrenti.
6. Voce fissa: una sola voce (Kling voice binding o ElevenLabs), stesso ritmo.

## Come tenerlo coerente in Kling (Element Library)
Fonte: [guida ufficiale Kling Element Library](https://kling.ai/quickstart/klingai-element-library-3-user-guide).
- Crea un **Element** con 2-4 immagini: una frontale come immagine principale, più 1-3 angoli (profilo, 3/4, retro) o dettagli. La frontale dà la coerenza migliore.
- Descrizione dell'Element: tratti fissi, dettagli chiave e cosa ignorare (es. "ignora lo sfondo").
- Nel prompt si richiama con `@NomeElement`. Funziona con Video 3.0, 3.0 Omni, O1 Video, Image 3.0 Omni, Image O1.
- Limiti: fino a 7 immagini o Element per generazione (4 se c'è un video in input). Con primo e ultimo fotogramma, al massimo 3 Element in più, che devono comparire nei fotogrammi.
- Voce: solo 3.0 Omni. Si carica un audio pulito di 5-30 s, oppure si sceglie una voce dalla libreria.
- Costi: creare un Element è gratis. La generazione automatica degli angoli mancanti (multi-view) è gratis 3 volte al giorno per gli abbonati, poi costa 5 crediti.
- Alternativa video: una clip di 3-8 s del personaggio da più angoli. Kling estrae aspetto e voce.

## Flusso di lavoro
1. **Bibbia del personaggio** (modello sotto): nome, frase di personalità, difetto, materiale, colori, accessorio, voce, cose vietate.
2. **Foglio modello in Kling Image**: frontale, profilo, 3/4, retro, 3 espressioni. Stesso sfondo neutro.
3. **Element** con la frontale più i 3 angoli migliori.
4. **Scene**: un'inquadratura per generazione, camera ferma o un solo movimento, 5 s. Per lo stop-motion vero, passo due in ffmpeg (`fps=12`).
5. **Montaggio in HyperFrames**: sottotitoli, logo, suono, tagli. Il testo non va mai generato da Kling.

## Modello di bibbia del personaggio
```
Nome:
Specie / oggetto:
Personalità in una frase:
Difetto (da qui nasce l'umorismo):
Materiale: feltro e lana / plastilina / vinile / 2D piatto
Colori (max 3) e accessorio fisso:
Proporzioni: testa / corpo, occhi
Voce: età, ritmo, accento
Set ricorrenti:
Vietato: (es. niente denti, mai arrabbiato, mai testo sul corpo)
```

## Prompt base (Kling, da adattare)
**Foglio modello (Image 3.0):**
Character turnaround sheet of [@Nome], a [specie] made of [materiale], [colori], wearing [accessorio]. Front view, side profile, three-quarter view and back view in a row, plus three expressions: neutral, surprised, deadpan. Neutral light grey background, even studio light, same scale in every view, no text.

**Scena stop-motion (Video 3.0 con Element):**
Stop-motion animation. [@Nome] [azione semplice] on [set in miniatura]. Locked-off static camera, medium shot. Overcast soft daylight. Animated on twos, slight frame-to-frame jitter in the fabric fibres, visible [materiale] texture, miniature scale, shallow depth of field. No text, no logos.

**Battuta con voce (3.0 Omni con voce legata):**
[@Nome] looks at the camera and says, deadpan: "[battuta breve, max 8 parole]". Static camera, medium close-up, tiny head movements only.

Negative: CGI, glossy plastic, 2D cartoon (se il materiale è fisico), text, watermark, morphing, extra limbs, changing outfit.

## Errori comuni
- Cambiare materiale o luce tra un video e l'altro: il personaggio sembra un altro.
- Troppe azioni in 5 s: Kling deforma il personaggio. Una sola azione per clip.
- Testo o logo generati da Kling: escono sbagliati. Si aggiungono in HyperFrames.
- Mascotte senza difetto: risulta carina ma piatta, nessuno la ricorda.

## Collegamenti
- Test spot stile Telstra: `../../test-hyperframes/clip3-spot/` (prompt e montaggio pronti).
- Beluga 2D piatta (stile BUCK): `../../test-hyperframes/clip2-flat/`.
