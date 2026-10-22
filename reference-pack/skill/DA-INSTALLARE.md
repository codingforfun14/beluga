# Skill e strumenti da installare

Verificati il 22 ottobre 2026 leggendo README e metadati, senza installare né eseguire niente. Prima dell'installazione va fatto un controllo dei file (`grep -rE "curl|wget|eval|base64|fetch\(" skills/`).

## Da installare subito

| Nome | Cosa aggiunge | Licenza | Come si installa |
| --- | --- | --- | --- |
| [HyperFrames](https://github.com/heygen-com/hyperframes) (HeyGen) | motore HTML/GSAP → MP4 deterministico, circa 450 blocchi pronti (transizioni, kinetic type, sottotitoli, grafici, 3D) e 7 skill | Apache-2.0 | `claude plugin marketplace add heygen-com/hyperframes` |
| [GSAP skills](https://github.com/greensock/gsap-skills) (ufficiali) | timeline corrette, SplitText, MorphSVG, DrawSVG, MotionPath; tutti i plugin GSAP ora sono gratis anche per uso commerciale | MIT | copia delle cartelle SKILL.md, fissata a un commit |
| [LottieFiles motion-design-skill](https://github.com/LottieFiles/motion-design-skill) | gusto: 12 principi, tabelle di timing ed easing, coreografia, checklist | MIT | copia delle cartelle SKILL.md |
| [Three.js skills](https://github.com/CloudAI-X/threejs-skills) | 3D corretto per three.js r186, con gli errori comuni | MIT | copia delle cartelle SKILL.md |
| [rembg](https://github.com/danielgatis/rembg) | scontorno locale di persone e oggetti | MIT | `pip install rembg` |
| [faster-whisper](https://github.com/SYSTRAN/faster-whisper) o [WhisperX](https://github.com/m-bain/whisperX) | trascrizione con tempi per parola, base dei sottotitoli animati | MIT / BSD-2 | `pip install faster-whisper` |

## Con condizioni

- [Remotion skills](https://github.com/remotion-dev/skills): ottime, ma Remotion è gratis solo per privati e aziende fino a 3 dipendenti. Si sovrappone a HyperFrames: ne serve uno solo come motore principale.
- [LottieFiles MCP](https://docs.lottiefiles.com/en/platform/mcp) (connettore ufficiale): ricerca di animazioni Lottie, ma dà accesso completo all'account, anche per cancellare.
- [Blender MCP](https://github.com/ahujasid/mcp-for-blender): scene 3D vere; da usare con `DISABLE_TELEMETRY=true`, mai con lo script `curl | sh`.
- [After Effects MCP](https://github.com/Dakkshin/after-effects-mcp): solo se hai After Effects.
- [Spline MCP](https://docs.spline.design/generate/spline-mcp-server): oggetti 3D eroici, meglio la modalità desktop.
- [Manim](https://github.com/ManimCommunity/manim): solo per spiegazioni matematiche.

## Solo idee, niente installazione

- [OpenMontage](https://github.com/calesthio/OpenMontage): AGPL-3.0, quindi prendiamo solo le idee (scelta del motore, controlli di qualità dopo il render), non il codice.
- I connettori Pexels, Pixabay e Freesound della community hanno 1-19 stelle: meglio un piccolo script nostro con le chiavi API gratuite.

## Cosa cambia per noi

Il motore attuale (`tools/render.mjs`, canvas disegnato a mano) resta per le clip della libreria. Per i video veri il passo più grande è HyperFrames più le skill GSAP e LottieFiles: blocchi già pronti e timeline più ricche invece di scrivere ogni animazione da zero.
