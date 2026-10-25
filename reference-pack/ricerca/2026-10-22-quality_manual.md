# Motion design and edited video: numeric craft rules for a "creative director manual"

Researched 2026-10-22. Labels used below:
- **[VERIFIED]**: checked on the cited page during this session.
- **[3rd-party]**: from a vendor or practitioner blog, not a platform's own docs.
- **[UNVERIFIED, memory]**: from training knowledge, with no page fetched this session. Confirm before printing.

---

## Q1. Exact easing values and durations in Material Design 3, IBM Carbon, Apple HIG and Microsoft Fluent

### Takeaway
Across these systems, UI motion durations run from about 50ms to 1000ms. Most transitions fall between 150ms and 400ms. Every system uses a "fast out, slow in" curve for entrances, which is a strong deceleration. Material 3 and Carbon publish exact cubic-bezier values. Apple now defaults to a critically damped spring (response 0.55s). The Fluent 2 public motion page gives only qualitative guidance.

### Cited Findings

**Material Design 3** (from the Android Material Components docs; the m3.material.io page renders only with JavaScript and could not be scraped)
- Easing [VERIFIED] — [MDC-Android Motion.md](https://github.com/material-components/material-components-android/blob/master/docs/theming/Motion.md)
  - Emphasized (the default for expressive transitions) is not one bezier. It is a path: `M 0,0 C 0.05,0, 0.133333,0.06, 0.166666,0.4 C 0.208333,0.82, 0.25,1, 1,1`
  - Emphasized Decelerate (entering): `cubic-bezier(0.05, 0.7, 0.1, 1)`
  - Emphasized Accelerate (exiting): `cubic-bezier(0.3, 0, 0.8, 0.15)`
  - Standard (small utility moves): `cubic-bezier(0.2, 0, 0, 1)`
  - Standard Decelerate: `cubic-bezier(0, 0, 0, 1)`; Standard Accelerate: `cubic-bezier(0.3, 0, 1, 1)`
  - Linear: `cubic-bezier(0, 0, 1, 1)`
  - Discrepancy: the same doc's container-transform table lists Standard as `cubic-bezier(0.4, 0.0, 0.2, 1)`. That is the older Material 2 "standard" curve.
- Duration tokens [VERIFIED] — [MDC-Android Motion.md](https://github.com/material-components/material-components-android/blob/master/docs/theming/Motion.md)
  - Short 1–4: 50 / 100 / 150 / 200ms
  - Medium 1–4: 250 / 300 / 350 / 400ms
  - Long 1–4: 450 / 500 / 550 / 600ms
  - Extra-long 1–4: 700 / 800 / 900 / 1000ms
- M3 Expressive spring tokens (damping ratio / stiffness) [VERIFIED] — [MDC-Android Motion.md](https://github.com/material-components/material-components-android/blob/master/docs/theming/Motion.md)
  - Fast spatial: 0.9 / 1400; Fast effects: 1 / 3800
  - Default spatial: 0.9 / 700; Default effects: 1 / 1600
  - Slow spatial: 0.9 / 300; Slow effects: 1 / 800
  - "Spatial" springs (position, size) have a damping ratio of 0.9, which gives a slight overshoot. "Effects" springs (colour, opacity) have 1.0, which gives no overshoot.

**IBM Carbon** [VERIFIED] — [Carbon motion overview](https://carbondesignsystem.com/elements/motion/overview/)
- Productive curves: standard `cubic-bezier(0.2, 0, 0.38, 0.9)`, entrance `cubic-bezier(0, 0, 0.38, 0.9)`, exit `cubic-bezier(0.2, 0, 1, 0.9)`
- Expressive curves: standard `cubic-bezier(0.4, 0.14, 0.3, 1)`, entrance `cubic-bezier(0, 0, 0.3, 1)`, exit `cubic-bezier(0.4, 0.14, 1, 1)`
- Durations:
  - fast-01 70ms (button, toggle)
  - fast-02 110ms (fade)
  - moderate-01 150ms (small expansion, short distance)
  - moderate-02 240ms (expansion, toast)
  - slow-01 400ms (large expansion, important notification)
  - slow-02 700ms (background dimming)
- Usage:
  - Productive curves are for task-focused moments. Expressive curves are for occasional important moments, such as opening a page, a primary action or an alert.
  - Use standard easing when an element stays visible the whole time. Use exit easing when an element leaves for good.
  - Scale duration with the distance or size of the change.
- IBM's take on the classic principles [VERIFIED] — [IBM Design Language, classic principles](https://www.ibm.com/design/language/animation/classic-principles)
  - No cartoon squash and stretch.
  - Use as few key poses as possible.
  - Secondary elements follow the parent "with a slight delay".
  - "Speed up quickly and slow down smoothly."
  - Avoid "long exponential easing as elements settle".
  - Move one axis at a time with slight overlap, rather than on organic arcs.

**Apple (SwiftUI / HIG)**
- The SwiftUI `.default` animation is `spring(response: 0.55, dampingFraction: 1.0, blendDuration: 0)`, a critically damped spring with no bounce. It has been the default since iOS 17 / macOS 14; before that, the default was `easeInOut`. [VERIFIED] — [Apple docs: Animation.default](https://developer.apple.com/documentation/swiftui/animation/default.md)
- The presets `.smooth` (bounce 0), `.snappy` (bounce ~0.15) and `.bouncy` (bounce ~0.3), with a base duration of ~0.5s, are [UNVERIFIED, memory]. Check against [Apple docs: Spring](https://developer.apple.com/documentation/swiftui/spring.md).

**Microsoft Fluent 2**
- The public motion page gives no millisecond or bezier values. Its guidance:
  - Scale duration with element size and travel distance.
  - Use linear "only in cases that need a consistent rate, like rotations".
  - Ease-out is for things arriving. [VERIFIED] — [Fluent 2 Motion](https://fluent2.microsoft.design/motion)
- **Windows / WinUI 3 (Fluent)** [VERIFIED] — [Microsoft Learn, Timing and easing](https://learn.microsoft.com/en-us/windows/apps/design/motion/timing-and-easing)
  - Control durations: ControlNormalAnimationDuration 250ms, ControlFastAnimationDuration 167ms, ControlFasterAnimationDuration 83ms. At 60fps these are 15, 10 and 5 frames. At 24fps they are 6, 4 and 2 frames.
  - "Fast Out, Slow In" `cubic-bezier(0, 0, 0, 1)` is for anything entering the scene.
  - "Slow Out, Fast In" `cubic-bezier(1, 0, 1, 1)` is for anything exiting.
- Fluent UI web tokens such as durationUltraFast 50ms, durationFaster 100ms, durationFast 150ms, durationNormal 200ms, durationGentle 250ms, durationSlow 300ms, durationSlower 400ms, durationUltraSlow 500ms, and curveDecelerateMax `cubic-bezier(0.1, 0.9, 0.2, 1)`, are [UNVERIFIED, memory]. Check against the Fluent UI React tokens package.

### Inferences
- **Durations converted to frames.** These are my own calculations (ms × fps / 1000, rounded):

  | ms | 24fps | 30fps | 60fps | Typical use |
  |---|---|---|---|---|
  | 50 | 1 | 1.5 | 3 | Micro feedback |
  | 100 | 2.4 | 3 | 6 | Fade, colour change |
  | 150 | 3.6 | 4.5 | 9 | Small move |
  | 200 | 4.8 | 6 | 12 | Button, chip |
  | 250 | 6 | 7.5 | 15 | Standard UI transition |
  | 300 | 7.2 | 9 | 18 | Panel, card |
  | 400 | 9.6 | 12 | 24 | Large expansion |
  | 500 | 12 | 15 | 30 | Full-screen or page change |
  | 700 | 16.8 | 21 | 42 | Dim, hero reveal |
  | 1000 | 24 | 30 | 60 | Upper ceiling for UI |

- **Applying UI durations to video.** Motion graphics for video can usually run 1.5–2× longer than UI durations. In UI, the user is waiting on the result; in video, the motion is the content. This is an inference and needs practitioner confirmation.
- **Choosing a curve:**
  - Entering elements decelerate: M3 Emphasized Decelerate `(0.05, 0.7, 0.1, 1)` or Carbon entrance `(0, 0, 0.3, 1)`.
  - Exiting elements accelerate: M3 `(0.3, 0, 0.8, 0.15)`.
  - Elements that move on screen use standard `(0.2, 0, 0, 1)`.
  - Linear is only for rotation, scrolling tickers and opacity cross-dissolves.
- **Exit vs. entry duration.** Across systems, exits are shorter than entries; Carbon's exit curves accelerate hard to the end. A common practitioner rule is exit ≈ 70–80% of entry duration. [UNVERIFIED, memory]

### Gaps
- M3's own web page and its motion "duration by distance" guidance could not be scraped because the page needs JavaScript.
- Fluent tokens and the Apple HIG motion page were not fetched.

---

## Q2. What School of Motion, Motion Design School, Ben Marriott, Jake Bartlett, The Animator's Survival Kit and The Illusion of Life recommend

### Takeaway
Practitioner sources agree on one qualitative rule: always ease, and shape the motion in the graph editor rather than relying on "Easy Ease" presets. They give few hard numbers. Most of the numeric rules in this section come from the classic animation books and are drawn from memory.

### Cited Findings
- **Easing always applies.** "You want all motion to always ease." Most other Disney principles transfer poorly to UI, and the article proposes "Transform" as a new principle. [VERIFIED] — [Adobe Blog, Redesigning the 12 Principles for Motion Design](https://blog.adobe.com/en/publish/2016/11/08/redesigning-the-12-principles-of-animation-for-motion-design)
- **Common After Effects mistakes** [VERIFIED, 3rd-party] — [PremiumBeat, 10 After Effects mistakes](https://www.premiumbeat.com/blog/10-after-effects-mistakes-avoid)
  - Skipping motion blur.
  - Using linear keyframes.
  - Leaving masks unfeathered.
  - Grading without scopes.
  - Using the Stroke effect instead of Trim Paths.
  - Animating text through Transform instead of text Animators.
- **Overshoot and bounce technique** [VERIFIED, 3rd-party] — [mtmograph, overshoot trick](https://mtmograph.com/blogs/tools/the-bounce-and-overshoot-animation-trick-every-motion-designer-should-know)
  - The article's keyframe example is scale 50 → 150 → 100 → 75 → 100. Each bounce shrinks.
  - The sample decay expression uses `freq = 3; decay = 5;`.
  - Oscillations should get shorter and smaller over time.
- **Classic animation numbers** [UNVERIFIED, memory: Williams, *The Animator's Survival Kit*; Thomas & Johnston, *The Illusion of Life*]
  - Film runs at 24fps. Animating "on twos" (12 drawings per second) is the standard for most motion. "On ones" is for fast action and camera moves, because twos strobe on pans.
  - Anticipation should be roughly ⅓ or less of the action's length, and should move opposite to the main action.
  - Hold a pose for at least about 6–8 frames at 24fps to register it, and keep "moving holds" alive with slight drift.
  - Spacing, not the number of keyframes, gives the feeling of weight. Bunch drawings at the extremes (slow in / slow out).
- **School of Motion, Ben Marriott, Jake Bartlett, Motion Design School.** I fetched no first-party article from these sources with numbers. Practitioner lore commonly repeated in their tutorials [UNVERIFIED, memory]:
  - Pull bezier influence handles to roughly 70–90% for "snappy" motion, instead of the default Easy Ease 33%.
  - Overshoot about 5–15% of the travel distance for UI-style motion graphics.
  - Stagger offsets of 2–4 frames between items in a list or text block.
  - Use motion blur with a shutter angle of 180°, which is the AE default.
  - Never let every element arrive on the same frame.

### Inferences
- **The 12 principles applied to motion graphics** (my synthesis from the IBM and Adobe sources plus classic practice):
  - Slow in/out: every keyframe gets a custom curve.
  - Anticipation: a 2–4 frame pull-back before a big move.
  - Follow-through / overlapping action: children lag the parent by 1–3 frames.
  - Staging: one focal action at a time.
  - Arcs: use arcs for organic objects and single-axis moves for UI (IBM).
  - Squash and stretch: use sparingly; at most ~10–20% on "bouncy" brands [UNVERIFIED].
  - Secondary action: only in support of the main action.
  - Timing: decisive moves, without long, mushy tails.
  - Exaggeration: in service of function.
  - Solid drawing: consistent light and perspective.
  - Appeal: one "delight" moment per sequence.

### Gaps
- School of Motion, Ben Marriott and Jake Bartlett pages with specific numbers were not retrieved this session. The search results surfaced only low-quality mirrors.
- The book quotes are from memory. Verify page references before using them as citations.

---

## Q3. Platform specs: safe zones, loudness, caption sizing, text on screen, hooks, voiceover pacing

### Takeaway
No platform publishes an official organic-content safe zone or loudness target. The figures in circulation come from ad specs and third-party tools.

The working rule for 9:16 at 1080×1920:
- Keep text inside roughly the central box from y = 270 to y = 1250 px, with a margin of about 65–120 px on each side.
- Keep the right ~120–140 px clear of the action-button rail.
- Master the audio to about −14 LUFS integrated with a true peak of −1 dBTP.

### Cited Findings

**Safe zones**
- **Meta Stories / Reels 9:16 (1080×1920)** [3rd-party, citing Meta's Help Center diagram] — [AdsUploader, Meta safe zones](https://adsuploader.com/blog/meta-ads-safe-zones); Meta source cited: [facebook.com/business/help/980593475366490](https://www.facebook.com/business/help/980593475366490)
  - Keep about 14% clear at the top (269 px), 35% at the bottom (672 px) and 6% on each side (65 px).
  - The usable centre box is about 950×979 px.
  - The bottom-right corner needs 40% clearance.
- **Meta feed sizes** [3rd-party, same source as above]
  - Feed 4:5 (1080×1350): 250 px top and bottom, 100 px on the sides.
  - Feed 1:1: about 100 px on all sides, which is a working figure, not a Meta number.
- **TikTok** [3rd-party] — [Zuuvi, social safe zone guide](https://help.zuuvi.com/en/articles/8907258-social-content-safe-zone-guide)
  - On a 540×960 canvas: top 108, bottom 320, left 60, right 120 px.
  - Doubled for 1080×1920, that is ≈ 216 / 640 / 120 / 240 px. The doubling is my inference.
- **Instagram Story and Snapchat Story (1080×1920)** [3rd-party, same Zuuvi source]
  - Instagram Story: 250 px top and bottom.
  - Snapchat Story: 149 px top and bottom.
- **Cross-platform working margins** for Shorts, Reels and TikTok, explicitly "not official" [3rd-party] — [Reap, short-form safe zones](https://reap.video/blog/short-form-video-safe-zones)
  - Top ~15%, sides 10–15%, bottom 25–35%.
  - Place captions in the lower-middle, above the account/description area and left of the action rail. Use at most 1–2 lines.
  - Keep captions off the mouth, hands and product.
  - YouTube's June 2026 Shorts "Clear Screen" mode exists, but there is no pixel spec for it.

**TikTok's own creative guidance** [VERIFIED, official] — [TikTok Ads, Creative best practices](https://ads.tiktok.com/help/article/creative-best-practices?lang=en)
- Format: 9:16 vertical, at least 720p.
- Introduce the content proposition in the first 3 seconds, and land the hook within the first 6 seconds.
- On-screen text: show 5–10 words per second.
- Testing: run 3–5 creatives per ad group.

**Loudness** [VERIFIED summary of a 3rd-party compilation] — [Fora Soft, LUFS targets per platform 2026](https://www.forasoft.com/learn/audio-for-video/articles-audio/lufs-targets-per-platform-2026)

| Platform | Integrated target | True-peak ceiling | Status |
|---|---|---|---|
| YouTube | −14 LUFS | −1 dBTP | Observed playback normalisation, not a published spec |
| TikTok, Instagram, Facebook | None published | −1 dBTP advised | Adaptive loudness (Meta uses xHE-AAC); the source warns against writing ~−14 into a contract |
| Spotify | −14 LUFS | −1 dBTP (−2 dBTP on upload) | Official |
| Apple Music | −16 LUFS | — | Published value, cited secondhand |
| Netflix | −27 LKFS dialogue-gated (±2 LU) | −2 dBTP | Official |
| EBU R128 (broadcast) | −23 LUFS | −1 dBTP | Official |
| ATSC A/85 (US broadcast) | −24 LKFS | −2 dBTP | Official |

**Subtitles and captions**
- Netflix sets a maximum of 2 lines and holds each event for at least 5/6 s (20 frames at 24fps) and at most 7 s. [VERIFIED] — [Netflix Timed Text, General Requirements](https://partnerhelp.netflixstudios.com/hc/en-us/articles/215758617-Timed-Text-Style-Guide-General-Requirements)
- Netflix recommends about 42 characters per line for most languages. CJK languages are limited to 23 (16 for Originals). [VERIFIED] — [Netflix, max characters per line](https://partnerhelp.netflixstudios.com/hc/en-us/articles/215274938-What-is-the-maximum-number-of-characters-per-line-allowed-in-Timed-Text-assets)
- **Netflix subtitle timing rules** [VERIFIED] — [Netflix Subtitle Timing Guidelines](https://partnerhelp.netflixstudios.com/hc/en-us/articles/360051554394-Timed-Text-Style-Guide-Subtitle-Timing-Guidelines)
  - Gaps between subtitles are either 2 frames or ≥ 0.5 s. That is 12 frames at 24fps, 15 at 30fps and 30 at 60fps. At 24fps, gaps of 3–11 frames are closed to 2 frames.
  - In-time: within 1–2 frames of the start of the audio.
  - Out-time: about 12 frames after the audio ends when no subtitle follows.
  - Snap to shot changes: when an in-time or out-time falls within 12 frames of a cut, move it to the cut and keep a 2-frame gap.
  - The page states the minimum duration as 20 frames ("4/5 s"); the General Requirements page states it as 5/6 s.
  - The page gives no characters-per-second value.
  - These rules carry over directly to burned-in captions and kinetic type: snap text changes to cuts, never leave 3–11 frame "flash" gaps, and add about 0.5 s of tail after speech.
- Netflix English reading speed of 20 characters per second for adult content and 17 cps for children's content is [UNVERIFIED, memory]. See [Netflix Subtitle Timing Guidelines](https://backlothelp.netflix.com/hc/en-us/articles/360051554394-Timed-Text-Style-Guide-Subtitle-Timing-Guidelines).
- No platform source gave a caption font size. A practitioner norm for 1080×1920 is about 48–72 px cap height, bold sans, with an outline, shadow or plate. [UNVERIFIED, memory]

**Voiceover pacing** [3rd-party] — [Bread n Beyond, words in a 60s script](https://breadnbeyond.com/how-many-words-does-a-60-seconds-explainer-video-needs/)
- Voice actors average about 2.5 words per second, or 150 wpm.
- A 60-second explainer runs 140–150 words. A pace of 240 wpm is possible but sounds forced.
- The same source reports retention of 77% for videos ≤ 1 minute, 57% for 1–2 minutes and 47% for > 2 minutes. Methodology is not disclosed.

### Inferences
- **Text-on-screen budget.** TikTok's 5–10 words per second applies to fast caption bursts. For text that must be read in full, a safer hold is about 0.3 s per word plus 0.5–1 s of overhead, which is roughly 3 words per second. That rate is consistent with 150 wpm (2.5 words per second) VO pacing. This is my synthesis.
- **Single 9:16 master for all platforms.** Use the intersection of the published zones:
  - top 270 px (TikTok and Meta)
  - bottom 672 px (Meta, the most conservative)
  - left 65–120 px
  - right 140–240 px (TikTok rail)
- **Sources for 16:9 and 1:1.** Broadcast "action safe" 93% / "title safe" 90% (SMPTE ST 2046-1) is [UNVERIFIED, memory]. The 1:1 figure of 100 px per side comes from the AdsUploader source above.
- **Mastering for adaptive platforms.** For social, master to −14 LUFS and −1 dBTP. Exporting much louder only gets turned down on YouTube and Spotify. On TikTok and Instagram there is no published target, so −14 is a convention, not a rule.

### Gaps
- No official, current TikTok, YouTube Shorts or Instagram organic safe-zone pixel spec was found. All pixel values are from ads guidance or third-party sources.
- No official platform loudness spec exists for TikTok or Instagram.
- No official maximum word count for on-screen text was found beyond TikTok's 5–10 words per second.

---

## Q4. What separates "premium" from "amateur" motion (mistakes list, colour, sound, hooks, QC)

### Takeaway
The main signs of premium motion are custom easing on every move, staggered timing and nothing arriving on the same frame, motion blur, restraint (one focal action at a time, few key poses), a disciplined palette and type system, and sound locked to picture. Amateur work shows linear keys, default Easy Ease, simultaneous moves, no blur, long mushy settles, ungraded footage and inconsistent loudness.

### Cited Findings
- **Amateur tells** (PremiumBeat list in Q2) [VERIFIED, 3rd-party] — [PremiumBeat](https://www.premiumbeat.com/blog/10-after-effects-mistakes-avoid)
  - Linear keyframes
  - No motion blur
  - Hard mask edges
  - Grading without scopes
- **Restraint and decisiveness** [VERIFIED] — [IBM classic principles](https://www.ibm.com/design/language/animation/classic-principles)
  - Avoid competing actions.
  - Use as few poses as possible.
  - No long exponential settles.
  - Exaggerate for function, not decoration.
- **Productive vs. expressive** [VERIFIED] — [Carbon](https://carbondesignsystem.com/elements/motion/overview/)
  - Reserve expressive motion for occasional important moments. Premium work rations its flourishes.

**Colour** [UNVERIFIED, memory; no source fetched]
- Palette: 3–5 colours, split roughly 60/30/10 (dominant / secondary / accent).
- Text contrast: at least 4.5:1, or 3:1 for large text (WCAG 2.x AA).
- Grading: work on scopes, and keep skin tones on the vectorscope skin-tone line.
- Common looks: teal-orange, bleach bypass, filmic low-contrast with lifted blacks.

**Sound design and music sync** [UNVERIFIED, memory]
- Start a whoosh 2–4 frames before the visual move, so its peak lands on the move's fastest frame.
- Put hits and impacts on the frame of contact, or 1 frame early.
- Risers should resolve exactly on the cut or reveal.
- Cut on the beat. At 120 BPM, one beat is 0.5 s, which is 12 frames at 24fps or 15 frames at 30fps.
- Duck music by about 6–12 dB under VO.

**Hook and retention**
- From [TikTok](https://ads.tiktok.com/help/article/creative-best-practices?lang=en): state the proposition within 3 s and land the hook within 6 s.
- Retention falls with length (Bread n Beyond figures in Q3).
- Pattern interrupts every 3–5 s in short-form video are [UNVERIFIED, memory].

### Inferences

**Pre-delivery QC checklist** (synthesis; each number traces to the sections above)
1. Every keyframe has custom easing; no linear moves except rotation or opacity.
2. Entries decelerate and exits accelerate. Exits are shorter than entries.
3. Staggers are 2–4 frames, and no two hero elements land on the same frame.
4. Motion blur is on (180° shutter).
5. Overshoot is at most about 10% for brand UI, and each bounce decays.
6. Text sits inside the platform safe zone; check with an overlay template on a real phone.
7. Every text card stays up long enough to read at about 3 words per second. Captions are at most 2 lines and about 42 characters per line, held at least 20 frames at 24fps.
8. Contrast is at least 4.5:1 [UNVERIFIED], and the palette has at most 5 colours.
9. Grade is checked on scopes; shots match across cuts.
10. VO runs at about 150 wpm, with the proposition within 3 s and the hook within 6 s.
11. Audio is mastered to −14 LUFS integrated and −1 dBTP for social, or −23 / −24 for broadcast. There are no clipping or level jumps at cuts.
12. Sound effects are synced frame-accurately, and music cuts land on beats.
13. Export: 1080×1920 for 9:16, 1920×1080 for 16:9, 1080×1080 for 1:1. Frame rate matches the source, with no frame-rate conversion judder.
14. Watch the full export once with the sound off and once on a phone, checking that captions carry the message.

### Gaps
- No authoritative practitioner source with numbers was found for sound-design sync offsets, colour palette size or grading looks. Those items are marked unverified.
- No published "premium vs. amateur" checklist from School of Motion or Motion Design School was retrieved.
