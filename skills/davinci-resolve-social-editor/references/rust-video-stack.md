# Rust Video Stack

Use Rust as the reliable planning/orchestration layer, not as a replacement for proven media engines.

## Practical Stack

- Rust CLI: project scanning, manifests, scoring, edit decision graph, reproducible plans.
- FFmpeg/libav: decode, trim, concat, filters, loudness, render, mux.
- GStreamer/GStreamer Editing Services: real timeline model, transitions, preview pipelines.
- Whisper/whisper.cpp/Candle Whisper: timestamps and rough transcript.
- PySceneDetect or scene detection stage: visual boundaries.
- OpenCV Rust / CV models: face/subject tracking, crop safety, motion quality.
- Symphonia/Rubato/dasp/hound: native Rust audio decode/resample/DSP analysis.
- Resolve Python/Lua scripting: project/timeline setup and review handoff.

## Planner Model

The missing piece is the edit planner:

```text
raw media
-> media manifest
-> transcript with timestamps
-> semantic segments
-> story beat candidates
-> visual continuity scoring
-> subject framing scoring
-> audio/music scoring
-> edit decision list
-> Resolve/FCPXML/EDL timeline
-> preview render
-> verification artifacts
```

## Cut Eligibility

No cut unless:

1. The idea/sentence boundary is complete.
2. The visual scene is stable or intentionally covered.
3. Speaker face/body remains trackable, or B-roll/graphics cover it.
4. The edit has a transition strategy: angle change, punch-in, B-roll, crossfade, title card, or motivated hard cut.
5. Audio remains continuous or the cut is intentionally masked.

## Suggested Rust Data Types

```rust
struct FrameSafetyScore {
    subject_visible: bool,
    face_centered: f32,
    headroom_ok: bool,
    body_cutoff_risk: f32,
    motion_blur: f32,
}

struct EditDecision {
    source_path: String,
    source_in: f64,
    source_out: f64,
    camera_angle: String,
    story_beat: String,
    transition: String,
    crop: Option<CropWindow>,
    audio_source: String,
    rationale: String,
}
```

## Crate Candidates

- `ffmpeg-next`, `rsmpeg`, `rusty_ffmpeg`, `ez-ffmpeg`: FFmpeg bindings.
- `gstreamer`, `gstreamer-editing-services`: timeline/preview pipeline.
- `symphonia`: safe Rust demux/decode and metadata.
- `rubato`, `dasp`, `hound`: resampling, DSP, WAV.
- `opencv`: face/body/crop analysis.
- `candle`: local ML inference.

Keep the Rust planner deterministic and artifact-heavy. Let humans review EDL/FCPXML/Resolve timelines before final export.
