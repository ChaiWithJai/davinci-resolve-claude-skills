# Instagram Reels Evaluation Benchmark

Use this benchmark when producing speaker-led Instagram Reels, Shorts, or TikTok-style cuts from interview/podcast/event footage.

## Four Evaluators

1. **Video editing craft**
   - Checks semantic beat integrity, cut smoothness, motivated transitions, visual variety, punch-ins, B-roll coverage, J-cuts, L-cuts, and whether the edit respects complete phrases.
   - Blocking failures: same-camera jump cuts without crop/angle change, clipped words, mid-thought cuts, absent split edits on dense A-roll, and unmotivated visual discontinuities.

2. **Creative direction**
   - Checks hook, audience clarity, value proposition, narrative arc, CTA, brand tone, social-native pacing, retention design, and whether on-screen text is public-facing.
   - Blocking failures: internal labels such as `THE HOOK`, weak first three seconds, no clear event promise, no CTA, and draft-looking graphics.

3. **Visual multimodal**
   - Checks native 9:16 framing, speaker frame safety, caption readability, caption safe zone, color/vibrance, graphic design, phone readability, and visual continuity.
   - Blocking failures: speaker out of frame during speech, captions under Instagram UI, dark grade, face covered by logo/graphic, black frames, or unreadable text.

4. **Audio multimodal**
   - Checks dialogue intelligibility, loudness, true peak, edit smoothness, room-tone continuity, noise/reverb control, music masking, and phone competitiveness.
   - Blocking failures: audible pops/clicks, room-tone jumps at cuts, music above dialogue, integrated loudness outside the target range, or clipped/peaked dialogue.

## Targets

- Instagram Reels dialogue loudness: approximately `-14 LUFS integrated`, acceptable range `-15` to `-13 LUFS`.
- True peak: below `-1 dBTP`.
- Audio edit smoothing: 2-4 frame constant-power fades or equivalent room-tone bridge at every dialogue edit.
- Captions: Netflix-style, two-line maximum, above the bottom social UI danger zone.
- Talking speed: 1.1x for speaker-led short-form when intelligibility remains strong.

## HITL Resolve Artifact Requirements

The Resolve timeline is the product, not just the preview render. A usable HITL artifact should include:

- enabled source-layer picture edit,
- enabled clean dialogue/master mix,
- disabled original repair audio,
- optional disabled music/SFX tracks,
- editable captions or caption reference,
- disabled master/reference render,
- track names that explain intent,
- visible timeline start-frame audit,
- markers at every benchmark failure and every human decision point.

## Failure-To-Tool Mapping

- Jump cuts: punch-in/punch-out, angle change, B-roll, J-cut/L-cut, or deliberate transition.
- Clipped words: expand source range, remove partial word, or rebuild the sentence selection.
- Room-tone jumps: constant-power crossfades, continuous room tone bed, denoise, and compression.
- Too quiet for social: loudness normalize to `-14 LUFS`, limit below `-1 dBTP`.
- Draft graphics: remove internal labels; use viewer-facing event promise, CTA, date/time, and brand elements.
- Good visual but failing craft/audio: do not publish; create a repair timeline with exact markers.
