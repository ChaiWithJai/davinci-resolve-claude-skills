# QEDC Trace Learnings

Use these findings when future video-editing threads resemble the QEDC workstream.

## Repeated Failure Loops

- User feedback around jump cuts, story coherence, framing, music levels, and captions must become explicit acceptance gates immediately.
- A flat render imported into Resolve is not a usable DaVinci deliverable when the user expects source layers.
- Transcript timestamps locate material; they do not define cuts. Cut on complete ideas, pauses, camera continuity, and B-roll coverage.
- Resolve API success is not enough. Audit `timeline.GetStartFrame()` and reject clips placed before the visible start frame.
- Audio source choice needs a ranked artifact. Silent MIC tracks and weak camera WAVs must be detected before cutting.
- Captions need a visible deliverable. SRT/ASS files alone are not enough; there must be a transparent overlay, Resolve subtitle layer, or burned-in review render.

## New Default Gates

- Story plan before render.
- Audio quality audit before source selection.
- Critic/pro-editor review before final Resolve build.
- Layered Resolve timeline audit before claiming handoff complete.
- Burned-in or transparent Netflix-style captions before social review.
- Repair/original camera audio disabled when clean dialogue is present.

## Tooling Implications

- `resolve_timeline_audit.py` catches invisible timeline and layer/handoff issues.
- `audio_quality_audit.py` catches silent/weak sources and creates a ranking artifact.
- `caption_burnin_pipeline.py` creates reviewable caption renders.
- Project-specific caption PNGs must be alpha-transparent, not full-frame black images.
