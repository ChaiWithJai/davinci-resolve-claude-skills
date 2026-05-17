# Editing QA Gates

Use these gates before delivering a social edit.

## Story Coherence

The cut must have a visible structure:

1. Hook/agenda: the viewer knows what the event/video is about.
2. Body: complete ideas in an order that can be followed without external context.
3. Recap/CTA: the viewer remembers the promise and knows what to do.

Reject cuts that:

- Start after necessary context.
- Stitch unrelated transcript snippets together.
- Cut out the setup needed to understand a later claim.
- End without repeating the main value proposition.

## Jump-Cut Prevention

Each cut must satisfy at least one:

- new camera angle,
- new crop scale,
- B-roll/graphic/brand card covers the seam,
- crossfade or dip for a section boundary,
- motivated hard cut on emphasis,
- natural pause or sentence boundary.

Avoid same-camera hard cuts across removed words or pauses. If unavoidable, create a punch-in/punch-out or cover with B-roll.

For Instagram Reels, treat same-camera, same-scale consecutive cuts as a benchmark failure. Alternate crop scale, X/Y position, or use B-roll/graphics so the viewer reads the seam as intentional.

## Frame Safety

For speaker-led social video:

- Speaker visible during spoken sections.
- Blank/black camera angles are removed from the selectable angle pool.
- Face not hidden by large logos, captions, or overlays.
- Eyes close to upper third when possible.
- Captions do not cover mouth/face.
- Bottom caption area stays clear of Instagram UI where practical.

Review stills at opening, every major beat, and closing.

## Caption QA

- Proper names must be verified manually.
- Captions should summarize cleanly when the transcript is messy.
- Do not burn in captions from an unreviewed transcript.
- If speeding up a burned-in render, captions remain visually baked; regenerate from source when text changes.
- A caption deliverable is not complete until there is a burned-in review render or visible Resolve caption layer.
- Netflix-style social captions should use large white bold sans text, black outline or translucent black box, bottom-safe placement, and two lines maximum.
- Run `scripts/caption_burnin_pipeline.py` for review renders when Resolve subtitle burn-in is not being exported directly.

## Audio QA

Voice is primary.

- Music should be ducked or mixed low enough that speech remains intelligible.
- Use `loudnorm`, `acompressor`, and/or `sidechaincompress`.
- Check LUFS and true peak. General social dialogue should land around `-16` to `-14 LUFS`; Instagram Reels candidates should target about `-14 LUFS`, with an acceptable gate of `-15` to `-13 LUFS`.
- Listen to dense speech sections, not only intro/outro.
- Run `scripts/audio_quality_audit.py` on HQ audio, embedded camera audio, and any cleaned stems before committing to a source.
- Keep a ranked source report with the edit artifacts; if the chosen source is not the top-ranked source, explain why.
- Treat LUFS as a gate, not a full answer. A pass still needs a human listen check for room tone, pumping, music masking, clipping, and noise-reduction artifacts.

## Render Runtime QA

- Still-image overlays and looped audio must not control final duration.
- Use an explicit duration cap or shortest-stream behavior when a render graph contains looped logos, brand cards, or beds.
- Verify output duration against the edit decision list before importing to Resolve.

## Color QA

For broadcast/documentary style:

- Neutral skin tones.
- Moderate contrast.
- Lifted mids if the set is dark.
- Restrained saturation.
- No heavy vignette or crunchy 90s LUT unless explicitly requested.
