# Agent skills, MCP servers and open-source tools for a Claude-based motion designer / video producer (as of 22 Oct 2026)

Method: README and metadata reading only. Nothing was installed or executed. GitHub repo metadata (stars, licence SPDX, last push) came from the GitHub search API on 2026-10-22. READMEs were downloaded as plain text from raw.githubusercontent.com and read, not run. I did NOT audit every script line by line; the safety notes rely on the READMEs plus visible repo structure. A code-level audit before install is still needed (see Gaps).

URLs opened / fetched:
- https://raw.githubusercontent.com/heygen-com/hyperframes/main/README.md and .../packages/cli/README.md
- https://raw.githubusercontent.com/calesthio/OpenMontage/main/README.md
- https://raw.githubusercontent.com/remotion-dev/skills/main/README.md
- https://raw.githubusercontent.com/remotion-dev/remotion/main/LICENSE.md
- https://raw.githubusercontent.com/greensock/gsap-skills/main/README.md
- https://raw.githubusercontent.com/LottieFiles/motion-design-skill/main/README.md
- https://raw.githubusercontent.com/CloudAI-X/threejs-skills/main/README.md
- https://raw.githubusercontent.com/ahujasid/mcp-for-blender/main/README.md
- https://raw.githubusercontent.com/Dakkshin/after-effects-mcp/main/README.md
- https://raw.githubusercontent.com/abhiemj/manim-mcp-server/main/README.md
- https://raw.githubusercontent.com/anthropics/skills/main/README.md
- https://raw.githubusercontent.com/redotvideo/revideo/main/README.md (redirects to midrender/revideo)
- https://raw.githubusercontent.com/motion-canvas/motion-canvas/main/README.md
- https://raw.githubusercontent.com/hellokaton/unsplash-mcp-server/main/README.md
- https://raw.githubusercontent.com/JosiahSiegel/claude-plugin-marketplace/main/README.md
- https://raw.githubusercontent.com/danielgatis/rembg/main/README.md
- https://raw.githubusercontent.com/ComposioHQ/awesome-claude-skills/master/README.md
- https://raw.githubusercontent.com/travisvn/awesome-claude-skills/main/README.md
- https://docs.lottiefiles.com/en/platform/mcp/security
- Firecrawl developer search (skills:"only") for "motion graphics animation video GSAP Lottie ffmpeg skill"
- Web searches: HyperFrames, OpenMontage, Remotion skills, LottieFiles MCP, Freesound MCP, Pexels/Pixabay MCP, Spline MCP

---

## Q1. Which skills/tools are actively maintained, and what are their licences (permissive vs copyleft vs unclear)?

### Takeaway
Most of the core stack is permissive and was active within the last 1-4 months: HyperFrames (Apache-2.0), GSAP skills, LottieFiles motion-design-skill, Three.js skills, Manim, rembg, whisper.cpp and faster-whisper (MIT), WhisperX (BSD-2). The exceptions: OpenMontage is AGPL-3.0 (copyleft). Remotion is source-available, and companies with more than 3 employees need a paid licence. The remotion-dev/skills and anthropics/skills repos have no repo-level licence that GitHub can detect. The community stock-media MCPs (Pexels, Pixabay, Freesound) are tiny, with 1-19 stars.

### Cited Findings

**Shortlist table** (stars, SPDX and last push from the GitHub API, 2026-10-22):

| # | Name | URL | Licence | Stars | Last push | Recommendation |
|---|---|---|---|---|---|---|
| 1 | HyperFrames (HeyGen) + 7 skills | https://github.com/heygen-com/hyperframes | Apache-2.0 | 69,627 | 2026-10-22 | **Install** (core set) |
| 2 | Remotion Agent Skills | https://github.com/remotion-dev/skills | none detected (Remotion itself is source-available) | 5,518 | 2026-10-19 | **Install** if the user is eligible for Remotion's free licence |
| 3 | Remotion (engine) | https://github.com/remotion-dev/remotion | NOASSERTION (custom Remotion License) | 66,218 | 2026-10-22 | Install (licence check first) |
| 4 | GSAP official skills | https://github.com/greensock/gsap-skills | MIT | 16,902 | 2026-07-29 | **Install** |
| 5 | LottieFiles motion-design-skill | https://github.com/LottieFiles/motion-design-skill | MIT | 2,421 | 2026-05-18 | **Install** |
| 6 | Three.js skills (CloudAI-X) | https://github.com/CloudAI-X/threejs-skills | MIT | 3,678 | 2026-10-19 | **Install** |
| 7 | OpenMontage | https://github.com/calesthio/OpenMontage | AGPL-3.0 | 70,754 | 2026-10-16 | **Adapt ideas only** |
| 8 | Motion Canvas | https://github.com/motion-canvas/motion-canvas | MIT | 19,427 | 2026-07-02 | Optional install (engine, no official agent skill) |
| 9 | Revideo (now midrender/revideo) | https://github.com/midrender/revideo | MIT | 4,130 | updated 2026-10-22 | Adapt / optional; turn telemetry off |
| 10 | Manim Community | https://github.com/ManimCommunity/manim | MIT | 41,764 | 2026-10-20 | Install for math explainers |
| 11 | manim-mcp-server | https://github.com/abhiemj/manim-mcp-server | MIT | 653 | 2025-05-19 (stale) | Skip; call the manim CLI directly |
| 12 | MCP for Blender (formerly blender-mcp) | https://github.com/ahujasid/mcp-for-blender | MIT | 31,959 | updated 2026-10-22 | Install with care (telemetry off, no curl\|sh) |
| 13 | After Effects MCP | https://github.com/Dakkshin/after-effects-mcp | MIT | 774 | 2026-04-01 | Install only if the user owns AE |
| 14 | LottieFiles official MCP (hosted) | https://docs.lottiefiles.com/en/platform/mcp | MIT source (per docs) | n/a | n/a | Install (OAuth, remote) |
| 15 | dotLottie web player | https://github.com/LottieFiles/dotlottie-web | MIT | 924 | 2026-10-21 | Install as a library |
| 16 | Rive WASM runtime | https://github.com/rive-app/rive-wasm | MIT | 1,011 | 2026-10-22 | Optional (needs .riv authored in Rive editor) |
| 17 | rembg | https://github.com/danielgatis/rembg | MIT | 25,156 | 2026-10-21 | **Install** (local cutouts) |
| 18 | WhisperX / faster-whisper / whisper.cpp | https://github.com/m-bain/whisperX · https://github.com/SYSTRAN/faster-whisper · https://github.com/ggml-org/whisper.cpp | BSD-2 / MIT / MIT | 24,774 / 26,043 / 54,556 | 2026-10-18 / 10-16 / 10-19 | **Install one** (faster-whisper or WhisperX for word timestamps) |
| 19 | ffmpeg skills (JosiahSiegel marketplace, ffmpeg-effects plugin) | https://github.com/JosiahSiegel/claude-plugin-marketplace | MIT | 59 | 2026-06-18 | Adapt ideas only |
| 20 | Unsplash MCP | https://github.com/hellokaton/unsplash-mcp-server | MIT | 237 | 2026-10-12 | Optional |
| 21 | Pexels / Pixabay / Freesound community MCPs | see below | various | 1-19 | 2026 | Skip, or write a thin API wrapper yourself |
| 22 | anthropics/skills (slack-gif-creator etc.) | https://github.com/anthropics/skills | none at repo level; README says many skills are Apache 2.0 | 182,888 | 2026-10-09 | Adapt ideas only (no dedicated video skill) |

Per-item detail:

- **HyperFrames**: "open-source framework for turning HTML, CSS, media, and seekable animations into deterministic MP4 videos". Apache 2.0, "no per-render fees or commercial-use thresholds". It ships 7 skills: core set `/hyperframes`, `/hyperframes-cli`, `/hyperframes-registry` (about 450 ready-made blocks: transitions, kinetic type, captions, charts, maps, 3D, camera moves) and `/media-use` (music, SFX, images, voiceover, transcripts, cutouts, colour grades "with HeyGen or free local tools"). On demand: `/figma`, `/slideshow`, `/remotion-to-hyperframes`. Install via `claude plugin marketplace add heygen-com/hyperframes` or `npx skills add heygen-com/hyperframes`. — [HyperFrames README](https://raw.githubusercontent.com/heygen-com/hyperframes/main/README.md)
- The HyperFrames animation skill names GSAP as the default runtime "for 95% of motion work" and Lottie for pre-baked After Effects timelines. Lottie players must be `autoplay:false` and registered on `window.__hfLottie` for deterministic seeking. — [hyperframes-animation techniques.md](https://github.com/heygen-com/hyperframes/blob/b306438e8b5e2199db1ed07e6eb4332d53131048/skills/hyperframes-animation/techniques.md); [mirror SKILL.md](https://github.com/freekmurze/dotfiles/blob/fe89482ce432f76e750885c4cdb29f88155c4cb7/config/claude/skills/hyperframes-animation/SKILL.md)
- HyperFrames is also packaged as an official optional skill for Nous Research's Hermes agent (Apache-2.0, author heygen-com). — [hermes-agent docs](https://github.com/nousresearch/hermes-agent/blob/4d04303818b61bf3aa09278af48356315515965b/website/docs/user-guide/skills/optional/creative/creative-hyperframes.md)
- **Remotion skills**: the skills are `/remotion-best-practices`, `-create`, `-markup`, `-studio`, `-render`, `-maps`, `-captions`, `-saas`, `-interactivity`, `-docs` (searches the Remotion docs and fetches pages as Markdown), `-upgrade` and `-multimedia` (Mediabunny). Install with `npx skills add remotion-dev/skills`. — [remotion-dev/skills README](https://raw.githubusercontent.com/remotion-dev/skills/main/README.md); [Remotion skills docs](https://www.remotion.dev/docs/ai/skills)
- **Remotion licence**: free for individuals, for-profit organisations with up to 3 employees, and non-profits. A Company License is required otherwise. Copying the code to sell a derivative is not allowed. — [Remotion LICENSE.md](https://raw.githubusercontent.com/remotion-dev/remotion/main/LICENSE.md)
- **GSAP skills**: 8 skills (gsap-core, timeline, scrolltrigger, plugins, utils, react, performance, frameworks) plus `skills/llms.txt`, examples, and `.claude-plugin` config. The repo self-rates its risk as "LOW". GSAP and all its former Club plugins (SplitText, MorphSVG, etc.) are now free, including for commercial use, after the Webflow acquisition. — [gsap-skills README](https://raw.githubusercontent.com/greensock/gsap-skills/main/README.md)
- **LottieFiles motion-design-skill**: "Universal motion design principles… timing, easing, choreography". Files: SKILL.md plus `director/` (Disney's 12 principles, emotion mapping, choreography, narrative), `patterns/` and `reference/` (timing/easing tables, quality checklist, troubleshooting). MIT. — [motion-design-skill README](https://raw.githubusercontent.com/LottieFiles/motion-design-skill/main/README.md)
- **Three.js skills**: 13 skills targeting three.js r186, R3F 9.8, drei 10.7 and gltf-transform 4.5. Every import path was checked against the published packages, and each skill has a "Common Mistakes" section covering outdated APIs. MIT. — [threejs-skills README](https://raw.githubusercontent.com/CloudAI-X/threejs-skills/main/README.md)
- **OpenMontage**: AGPLv3. Advertises "12 production pipelines, 100+ tools, 700+ agent skill" files, Python tools plus a Remotion composer, and picks Remotion or HyperFrames as the render runtime. Without API keys it uses Piper TTS and free archives (Archive.org, NASA, Wikimedia). With keys it calls FAL, Atlas Cloud, Kling, Pexels, Pixabay, Unsplash, Suno, ElevenLabs, OpenAI, xAI, Google, Volcengine Ark, HeyGen and Runway. It has budget caps and approval gates. — [OpenMontage README](https://raw.githubusercontent.com/calesthio/OpenMontage/main/README.md)
- Its `animation-runtime-selector.md` skill warns: "Never use GSAP with requestAnimationFrame inside Remotion — render will be non-deterministic". — [OpenMontage skill file](https://github.com/calesthio/openmontage/blob/c8066452325cb57c8fc1ba8c2a71b6e8842e6b65/skills/meta/animation-runtime-selector.md)
- Search results also show unofficial copies of OpenMontage at github.com/luotwo/OpenMontage and github.com/badgids/OpenMontage. The canonical repo is calesthio/OpenMontage. — [search result luotwo](https://github.com/luotwo/OpenMontage); [search result badgids](https://github.com/badgids/OpenMontage)
- **Revideo**: moved to midrender/revideo. MIT, a TypeScript generator-scene engine with headless `renderVideo()` and parallel rendering. It counts renders anonymously via PostHog; set `DISABLE_TELEMETRY=true` to stop it. — [Revideo README](https://raw.githubusercontent.com/redotvideo/revideo/main/README.md)
- **Motion Canvas**: MIT monorepo, last push 2026-07-02 (about 3.5 months ago, so slower). — [Motion Canvas README](https://raw.githubusercontent.com/motion-canvas/motion-canvas/main/README.md); GitHub API
- **Manim**: ManimCommunity is MIT, pushed 2026-10-20. The 3b1b/manim original is MIT with 95.5k stars, pushed 2026-09-09. — GitHub API ([ManimCommunity](https://github.com/ManimCommunity/manim), [3b1b](https://github.com/3b1b/manim))
- **manim-mcp-server**: it "executes Manim animation code and returns the generated video". Last push 2025-05-19. — [manim-mcp-server README](https://raw.githubusercontent.com/abhiemj/manim-mcp-server/main/README.md)
- **After Effects MCP**: Node MCP server plus `mcp-bridge-auto.jsx`, an ExtendScript panel that `npm run install-bridge` copies into the AE install. It controls compositions, text, shapes, solids, properties and track mattes. — [after-effects-mcp README](https://raw.githubusercontent.com/Dakkshin/after-effects-mcp/main/README.md)
- **rembg**: MIT. Runs as CLI, Python library, HTTP server or Docker. Models are downloaded on first use, or ahead of time with `rembg d`. — [rembg README](https://raw.githubusercontent.com/danielgatis/rembg/main/README.md)
- **LottieFiles official MCP**: hosted at `https://mcp.lottiefiles.com/mcp`. OAuth 2.1 + PKCE, with "never uses static API keys". Single scope `mcp:full`, which equals full account access, including GraphQL mutations that can modify or delete animations. Source on GitHub under MIT per the docs. Limit 60 req/s. — [LottieFiles MCP security docs](https://docs.lottiefiles.com/en/platform/mcp/security)
- An older community LottieFiles MCP (junmer/mcp-server-lottiefiles) has 19 stars. — [GitHub](https://github.com/junmer/mcp-server-lottiefiles)
- **Stock-media MCPs**: Pixabay (Unlock-MCP/pixabay-mcp-server, 11★, updated 2026-10-17), Pexels (developer-ishan/mcp-pexels 2★, afshinator/mcp-server-pexels 2★), Freesound (timjrobinson/FreesoundMCPServer 2★, last update 2026-02-26; MuShan-bit/freesound-mcp 1★). — GitHub API ([Pixabay](https://github.com/Unlock-MCP/pixabay-mcp-server), [Pexels](https://github.com/developer-ishan/mcp-pexels), [Freesound](https://github.com/timjrobinson/FreesoundMCPServer))
- **Unsplash MCP**: MIT, needs an Unsplash Access Key. The README pushes install through the Smithery CLI (`npx -y @smithery/cli@latest install ... --key ...`). — [unsplash-mcp-server README](https://raw.githubusercontent.com/hellokaton/unsplash-mcp-server/main/README.md)
- **Spline official MCP**: it has two modes.
  - Hosted, at `https://mcp.spline.design/mcp`: OAuth with a Spline account, runs a cloud editor per conversation, and calls count against a daily allowance set by the Spline plan.
  - Desktop: a local server bound to 127.0.0.1 inside the Spline desktop app, gated by an origin allowlist with no tokens.
  - Tools: scene building and editing, a code layer, 3D and image generation, screenshots, publishing, and Hana frame design with HTML/CSS export.
  - AI generation runs in Spline's cloud in both modes.
  - Recommendation: optional install for 3D hero objects, with the desktop mode preferred for privacy. A community alternative is aydinfer/spline-mcp-server; I did not open it. — [Spline MCP docs](https://docs.spline.design/generate/spline-mcp-server); [glama listing](https://glama.ai/mcp/servers/@aydinfer/spline-mcp-server)
- **anthropics/skills**: the only video/animation-adjacent skill listed is `slack-gif-creator` ("animated GIFs optimized for Slack… composable animation primitives"). There is no dedicated video skill. — [travisvn/awesome-claude-skills](https://raw.githubusercontent.com/travisvn/awesome-claude-skills/main/README.md); [anthropics/skills README](https://raw.githubusercontent.com/anthropics/skills/main/README.md)
- **ComposioHQ/awesome-claude-skills** video entries: Slack GIF Creator, Video Downloader, youtube-transcript, Pixelbin media generation (85+ APIs), TikTok/YouTube automation. None are motion-graphics authoring skills. — [ComposioHQ README](https://raw.githubusercontent.com/ComposioHQ/awesome-claude-skills/master/README.md)
- **ffmpeg skills**: JosiahSiegel's marketplace includes an `ffmpeg-effects` plugin with `ffmpeg-shapes-graphics/SKILL.md` (masking, blur, maskedmerge recipes). — [skill file](https://github.com/josiahsiegel/claude-plugin-marketplace/blob/5a1b1123b9e50aa9a66a61005ca6fe012cc7442d/plugins/ffmpeg-effects/skills/ffmpeg-shapes-graphics/SKILL.md)

### Inferences
- Permissive and actively maintained (push within about 3 months): HyperFrames, GSAP skills, Three.js skills, Manim, rembg, faster-whisper, WhisperX, whisper.cpp, dotlottie-web, rive-wasm, Blender MCP, Revideo, Unsplash MCP.
- Permissive but slower: LottieFiles motion-design-skill (May 2026). That is fine for a principles skill, which ages slowly. Motion Canvas (July 2026) and After Effects MCP (April 2026) are also slower.
- Copyleft: OpenMontage (AGPL-3.0). Copying its skill text into a distributed product would put that product under AGPL obligations, so take ideas only.
- Unclear: remotion-dev/skills and anthropics/skills have no repo-level licence detected. Remotion itself is source-available, not OSI open source.
- OpenMontage's 70.7k stars on a fairly young repo, plus third-party copies, are a reason to verify you are on the canonical repo. I did not confirm this is anything more than ordinary forking.

### Gaps
- Exact last-commit dates come from `pushed_at`. Midrender/revideo, mcp-for-blender and the small MCPs only returned `updated_at`, which can change without commits.
- I could not get a file-level licence for remotion-dev/skills. The GitHub API was blocked for this session; only search worked.
- I did not open the Rive MCP or Rive agent tooling. I found no official Rive MCP and only checked the runtime.
- I did not confirm the per-plan call allowances for the Spline hosted MCP; the docs page doesn't list them.

---

## Q2. Which are safe (no obfuscated code, no exfiltration, no curl|bash installers)?

### Takeaway
The pure-Markdown skill packs carry the least risk: GSAP, LottieFiles motion-design, Three.js, the HyperFrames skills, the Remotion skills and Anthropic's skills. Their risk is prompt content, not executables. The tools to watch are: Blender MCP (a curl|sh installer is offered, arbitrary Python execution, and anonymous usage telemetry by default); Revideo (PostHog render telemetry by default); OpenMontage (sends prompts and assets to many cloud APIs when keys are set); the LottieFiles MCP (full-account OAuth scope that can delete animations); and Unsplash MCP (Smithery CLI install path).

### Cited Findings
- **Blender MCP** offers `curl -LsSf https://www.mcp-for-blender.com/install.sh | sh`. Alternatives: `uvx mcp-for-blender setup`, `winget`, or `pipx`. — [mcp-for-blender README](https://raw.githubusercontent.com/ahujasid/mcp-for-blender/main/README.md)
- **Blender MCP** `execute_blender_code` "allows running arbitrary Python code in Blender… potentially dangerous". The addon opens a socket server inside Blender. — same source
- **Blender MCP** telemetry: by default it collects "a minimal anonymous usage record": install ID, session ID, tool name, success, duration, versions and OS. Prompts, code, screenshots and scene data are collected only on opt-in. `DISABLE_TELEMETRY=true` turns all of it off. — same source
- **Blender MCP** downloads assets from Poly Haven, Sketchfab and Poly Pizza, and calls Meshy, Tripo, Hyper3D Rodin and Hunyuan3D for AI models. It upsells a "premium" tier with no user API keys. — same source
- **Revideo** sends anonymous render counts to PostHog by default. `DISABLE_TELEMETRY=true` stops this. — [Revideo README](https://raw.githubusercontent.com/redotvideo/revideo/main/README.md)
- **OpenMontage** with keys set calls FAL, Kling (default Singapore endpoint), Suno, ElevenLabs, OpenAI, xAI, Google, Volcengine Ark, HeyGen, Runway, Pexels, Pixabay and Unsplash. Its setup runs `pip install -r requirements.txt` and `npm install` (a large dependency surface). It also offers `make install-gpu` for local Wan/Hunyuan/LTX models. — [OpenMontage README](https://raw.githubusercontent.com/calesthio/OpenMontage/main/README.md)
- **HyperFrames** `/media-use` can source media "with HeyGen or free local tools". The CLI can "render locally or in the cloud, publish". The CLI README returned no hits for telemetry, PostHog or analytics. — [HyperFrames README](https://raw.githubusercontent.com/heygen-com/hyperframes/main/README.md); [CLI README](https://raw.githubusercontent.com/heygen-com/hyperframes/main/packages/cli/README.md)
- **HyperFrames** recommends `npx hyperframes skills update`, which installs skills from current `main` rather than a pinned release. — [HyperFrames README](https://raw.githubusercontent.com/heygen-com/hyperframes/main/README.md)
- **LottieFiles MCP** sends tool calls and GraphQL operations tied to the account to LottieFiles. It "doesn't train models on your content". The scope `mcp:full` equals full account access. — [LottieFiles MCP security](https://docs.lottiefiles.com/en/platform/mcp/security)
- **GSAP skills** self-describe as "Risk level: LOW". The repo contains only SKILL.md files, llms.txt, examples and plugin config. — [gsap-skills README](https://raw.githubusercontent.com/greensock/gsap-skills/main/README.md)
- **After Effects MCP** `install-bridge` copies a JSX script into the After Effects install folder. That is a local file write; no network calls were documented. — [after-effects-mcp README](https://raw.githubusercontent.com/Dakkshin/after-effects-mcp/main/README.md)
- **Unsplash MCP** suggests installing through `npx -y @smithery/cli@latest` with a key, which is a third-party registry and an unpinned `@latest`. — [unsplash-mcp-server README](https://raw.githubusercontent.com/hellokaton/unsplash-mcp-server/main/README.md)
- **rembg** downloads ONNX models on first run. Processing is local after that. — [rembg README](https://raw.githubusercontent.com/danielgatis/rembg/main/README.md)
- **Remotion `/remotion-docs`** fetches Remotion documentation pages over the network. — [remotion-dev/skills README](https://raw.githubusercontent.com/remotion-dev/skills/main/README.md)

### Inferences
- None of the README-level evidence shows obfuscated code or covert exfiltration. The documented network behaviour is all disclosed: telemetry with an opt-out, and API calls that only happen when you supply keys.
- Safe install recipe:
  - Pin skill packs to a commit, or copy the SKILL.md folders by hand, instead of `@latest` or `main` auto-updates.
  - Run Blender MCP with `DISABLE_TELEMETRY=true` via uvx or pipx, never the curl|sh script.
  - Set `DISABLE_TELEMETRY=true` for Revideo.
  - Give OpenMontage-style pipelines only the API keys you intend to spend on.
- The LottieFiles MCP is the most powerful account-level integration. Use a dedicated LottieFiles account if delete rights are a concern.

### Gaps
- I did not grep skill repos for embedded scripts (`scripts/*.py`, `*.sh`) or base64 blobs. A static scan (e.g. `grep -rE "curl|wget|eval|base64|fetch\(" skills/`) is still required before install.
- I did not verify that the HyperFrames CLI has no telemetry. The CLI README had no hit, but the package code was not inspected.
- I did not inspect the small Pexels, Pixabay and Freesound MCPs' code.

---

## Q3. Which give the biggest jump in quality for motion graphics specifically?

### Takeaway
The biggest quality jump comes from combining:
1. a deterministic render engine with an agent skill: HyperFrames (Apache-2.0, about 450 ready-made blocks), or Remotion skills if the licence fits;
2. GSAP official skills for correct timelines, SplitText, MorphSVG, DrawSVG and MotionPath;
3. LottieFiles motion-design-skill for timing, easing and choreography taste.

Three.js skills (3D), Manim (math), rembg and Whisper (cutouts, word-level captions) are the next tier. OpenMontage is the best source of pipeline and quality-gate ideas, but its AGPL licence and cloud-heavy setup make it adapt-only.

### Cited Findings
- HyperFrames `/hyperframes-registry` provides "about 450 ready-made blocks and components… transitions, overlays, titles, kinetic type, captions, charts, maps, 3D, camera moves". The skill says to use it "before hand-building any named visual". — [HyperFrames README](https://raw.githubusercontent.com/heygen-com/hyperframes/main/README.md)
- The HyperFrames techniques reference maps "video energy" to technique combinations, for example Premium = "variable font animation + Lottie + slow velocity transitions". It also covers the GSAP MotionPathPlugin. — [techniques.md](https://github.com/heygen-com/hyperframes/blob/b306438e8b5e2199db1ed07e6eb4332d53131048/skills/hyperframes-animation/techniques.md)
- OpenMontage routes logo morphs to MorphSVG, stroke reveals to DrawSVG, curved paths to MotionPath, per-word reveals to SplitText, and FLIP flights to the GSAP plugins skill. — [OpenMontage asset-director.md](https://github.com/calesthio/openmontage/blob/c8066452325cb57c8fc1ba8c2a71b6e8842e6b65/skills/pipelines/animation/asset-director.md)
- OpenMontage's "bespoke composition" skill tells agents to apply Disney principles in Remotion `spring()`/`interpolate()`, and to escalate to gsap/threejs/d3/manim "only when the concept demands it". — [bespoke-composition.md](https://github.com/calesthio/openmontage/blob/c8066452325cb57c8fc1ba8c2a71b6e8842e6b65/skills/meta/bespoke-composition.md)
- OpenMontage quality gates include blocking "slideshow-looking renders", pre-compose validation, and mandatory post-render self-review (ffprobe plus frame extraction). — [OpenMontage README](https://raw.githubusercontent.com/calesthio/OpenMontage/main/README.md)
- The LottieFiles skill teaches an "8-step checklist, motion personality archetypes, duration/easing tables" and Disney's 12 principles adapted for UI. — [motion-design-skill README](https://raw.githubusercontent.com/LottieFiles/motion-design-skill/main/README.md)
- A third-party skill audit rates LottieFiles/motion-design-skill "best for framework-agnostic choreography… before code. Strength: strong." — [lazyweb skill](https://github.com/aboul3ata/lazyweb-skill/blob/71e86aaa76b0ae444b191e57de0bd28a2a3b4e78/skills/lazyweb-apply-design-best-practices/SKILL.md)
- The Three.js skills fix concrete API drift between r160 and r186 (`RGBELoader`→`HDRLoader`, `Clock`→`Timer`, `PostProcessing`→`RenderPipeline`). — [threejs-skills README](https://raw.githubusercontent.com/CloudAI-X/threejs-skills/main/README.md)
- WhisperX provides "Automatic Speech Recognition with Word-level Timestamps (& Diarization)", which is the basis for kinetic captions. — GitHub API description for [m-bain/whisperX](https://github.com/m-bain/whisperX)

### Inferences
- **Install, top tier for motion graphics:** HyperFrames core skills, GSAP skills, LottieFiles motion-design-skill. Add Remotion skills only if the Remotion licence fits. HyperFrames and Remotion overlap, so pick one primary engine. HyperFrames' Apache licence and GSAP-native approach suit an HTML/GSAP/headless-Chrome workflow.
- **Install, second tier:** Three.js skills, rembg, faster-whisper or WhisperX, the LottieFiles official MCP (asset sourcing), and dotlottie-web.
- **Conditional:** Blender MCP (3D scenes; telemetry off), After Effects MCP (only with an AE licence), Manim (math explainers), and Motion Canvas or Revideo as an alternative code engine.
- **Adapt ideas only:** OpenMontage (AGPL; mine the runtime selector, quality gates and budget gates), the JosiahSiegel ffmpeg skills, and anthropics/skills slack-gif-creator.
- **Skip:** manim-mcp-server (stale wrapper around a CLI the agent can call directly), and the 1-19★ Pexels, Pixabay and Freesound MCPs. Those APIs are simple REST calls with free keys, so a small self-written helper is safer than an unaudited MCP.

### Gaps
- There is no head-to-head benchmark measuring output-quality uplift from each skill. The ranking above is inferred from scope and content, not from measured evals.
- Tessl publishes evals and security reviews for the Remotion skills (tessl.io/registry/skills/github/remotion-dev/remotion/...). I did not open them.
