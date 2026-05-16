---
name: davinci-resolve-cut-screen-recording
description: Use when a user has a long screen recording, tutorial, conference talk, or demo recording and needs to cut it down to a tight watchable version — removes dead air, mistakes, "ums", and silences. Triggering symptoms include phrases like "raw recording is too long", "edit out the bad takes", "fix the ums", "remove silences", "rough cut my demo", or any DaVinci Resolve cutting question for long-form content.
---

# DaVinci Resolve — cut a long screen recording into a tight demo

## Overview

The fastest way to turn a 60-minute screen recording into an 8-minute watchable demo. Uses Resolve's **AI Transcription** plus **Remove Silent Portions** to do 80% of the work automatically, then refines manually. The core principle: do not waste your time scrubbing a waveform when Resolve can find the dead air for you.

## When to use

Symptoms:
- You recorded a 30-90 minute demo, talk, or tutorial and need to ship a tight version
- You said "um" too many times
- There are long pauses between sentences where you were thinking
- You did 2-3 takes of the same explanation and need to pick the best one
- Phrases like "raw recording is too long", "remove silences", "fix the ums"

When NOT to use:
- Multi-camera interview / talk-show — that needs the Multicam workflow (Editor's Guide ch. 4).
- Tight musical edits to a beat (rhythmic cuts) — use the Cut page manually.
- The recording is already under 10 minutes — manual editing is faster than this skill.

## Quick reference

| Tool | What it does | Where |
|---|---|---|
| **AI Transcription** | Generates word-level transcript with speaker detection | Right-click clip > Audio Transcription > Transcribe With Speaker Detection |
| **Remove Silent Portions** | Auto-deletes silent ranges from the timeline | Transcription window > Options menu (...) > Remove Silent Portions |
| **Editing from transcript** | Click a word, press F12, the clip lands in the timeline at that word | Transcription window > Append (F12) / Insert (Shift-F12) buttons |
| **Subframe audio editing** | Edit audio at sub-frame precision for tight cuts | Cmd-B for Razor, then trim by mouse |

## Steps

### Phase 1 — Set up and transcribe (3 minutes)

1. Switch to the Edit page (Shift-4).
2. In the Media Pool, drag your screen recording into a bin (e.g. `01 — Footage`).
3. Right-click the clip > **Audio Transcription > Transcribe With Speaker Detection**. (This is Studio-only; if you have free Resolve, use the manual Cut workflow below.)
4. Wait — about 1 minute per 10 minutes of audio. The AI Transcription window opens automatically when done.

If you have free Resolve (not Studio), AI Transcription is unavailable. Use the Cut page approach: import the clip, drag to the timeline, use the **mouse-scrub-and-mark-In/Out** workflow on the Cut page (Beginner's Guide pp. 1-67 covers this).

### Phase 2 — Create the rough cut from the transcript (10-15 minutes)

1. Create a new bin called `TIMELINES` and a new timeline inside it called `ROUGH_CUT`. Audio Track Type = Mono if your recording is mono voice.
2. With the Transcription window open, click on any word — the playhead jumps to that timecode in the source viewer.
3. Use **J / K / L** to scrub backward/stop/forward through the transcript.
4. To add a soundbite to the timeline:
   - Click and drag through the words you want to keep — this sets In and Out points automatically.
   - Press **Shift-F12** to **Append** the marked range to the timeline end.
   - Or press **F12** to **Insert** at the playhead.
5. Search the transcript for keywords — type a word in the Search field at the top of the Transcription window to jump to every instance.
6. Build the rough cut by appending each good soundbite one by one. Aim for ~2x your target length (a 16-minute rough cut for an 8-minute final).

Editor's Guide pp. 352-358 covers this workflow in depth.

### Phase 3 — Auto-remove silent portions (1 minute)

1. In the Transcription window, click the **Timeline** button (top-left of the Transcription window) to switch from clip-mode to timeline-mode. The window now shows the transcript for everything on the timeline, with silent gaps marked as `(...)`.
2. Click the Options menu (three dots `...`) > **Remove Silent Portions**.
3. The silent ranges are ripple-deleted from the timeline. Your 16-minute rough cut is suddenly 12 minutes.

Editor's Guide p. 358 shows this exact step.

### Phase 4 — Refine the edits manually (10-20 minutes)

The AI cuts are crude — they leave breaths cut off or pauses that feel unnatural. Walk the playhead through each edit point.

1. Press **N** to disable snapping (so you can trim by mouse at sub-frame precision).
2. Press **Shift-S** to enable audio scrubbing (you can hear what you are passing over).
3. At each cut: hover the cut point, click and drag the edge to extend or pull in by a few frames.
4. Use **Shift-,** / **Shift-.** to nudge an edit by 5 frames forward/back.

The audio subframe editing tip is on Editor's Guide p. 496.

### Phase 5 — Cut the obvious mistakes (5 minutes)

1. Play through end-to-end at 1.5x speed.
2. When you hear a mistake / dead air / re-take, press **I** for In-point.
3. Find the end of the mistake, press **O** for Out-point.
4. Press **Shift-Delete** to ripple-delete the marked region.
5. Continue. This pass should remove 1-3 minutes more.

You should be at or near your target length. Save the project.

## Python automation (rough silence detection on existing timeline)

For a long talk you have already imported, this script walks the active timeline, finds audio clips, and prints their durations so you can quickly identify long silent gaps to manually remove. It is **not** a substitute for AI Transcription's Remove Silent Portions — it is a helper for when you need to script a multi-clip operation.

The script uses the official DaVinci Resolve scripting API documented in `DaVinci Resolve/Developer/Scripting/README.txt` and the public Reference Manual.

```python
# scripts/auto_silence_cut.py
# Marks silent regions on the active timeline by inspecting clip start/end frames.
# Run from inside Resolve via Workspace > Console > Py3, or from terminal after
# setting RESOLVE_SCRIPT_API / RESOLVE_SCRIPT_LIB / PYTHONPATH (see README.md).
```

See `scripts/auto_silence_cut.py` for the full script. The script is conservative — it does not actually delete anything. It prints clip-level timecode reports so you can verify before running destructive edits.

## Common mistakes

- **Trusting the AI Transcription's accuracy** -> it gets technical terms, brand names, and acronyms wrong. Always proofread before treating it as a script. Editor's Guide pp. 346-348 documents the Search + Replace workflow for fixing systematic errors (e.g. "Oregon" -> "Organ" misrecognition).
- **Cutting on the Cut page when this is a single long clip** -> the Cut page is optimized for fast assembly from many small clips. For one long recording, the transcript-driven workflow on the Edit page is faster.
- **Forgetting to disable snapping when fine-trimming** -> snapping forces your cuts to align with existing edits and frame boundaries. Press N to toggle it off for fine work, on for assembly.
- **Doing the entire pass at 1x playback speed** -> 1.5x or 2x is faster and your ear can still spot rough cuts. Use the L key twice to enable 2x playback.

## Verification

You succeeded if all of the following are true:

1. The timeline duration matches your target (or is within 30 seconds of it).
2. Playing back the timeline end-to-end, you cannot hear any cut edits — the audio flows smoothly.
3. Every "um" / "uh" / long pause has been removed or trimmed.
4. The audio levels look broadly even on the meters (no clip is much louder than another — though the next skill, `davinci-resolve-audio-cleanup-podcast`, handles the actual leveling).
5. You can hand the timeline to a teammate and they cannot tell which cuts were AI-driven vs manual.

## Transfer

Now try this on a 20-minute conference talk recording. Watch the silence-detection threshold — large auditoriums often have ambient room noise above -30 dB, so Resolve's Remove Silent Portions might not detect actual pauses. In that case, you may need to manually search for the "(silent)" markers in the transcript and remove them by hand, or apply a quick noise-reduction pass first (see `davinci-resolve-audio-cleanup-podcast`) so the noise floor drops below the silence-detection threshold.

## Working reference

- `docs/wiki/editors-guide.md#lesson-6--ai-workflows-pp-323-387` (AI Transcription, Remove Silent Portions — primary)
- `docs/wiki/beginners-guide.md#lesson-1--editing-a-rough-cut-pp-1-67` (Cut/Edit page basics for free Resolve users)
- `docs/wiki/master.md#reset-matrix--when-the-user-pushes-back-read-this` (transcription pitfall rows)

## When the agent's work isn't matching expectations (context-rot reset)

If the user reports that transcription edits land on the wrong word, breaths are cut weirdly, or Remove Silent Portions misses pauses, read these PDF page ranges to reset:

- `DaVinci-Resolve-20-Editors-Guide.pdf` pp. 341-361 (Lesson 6 — full AI Transcription workflow)
- `DaVinci-Resolve-20-Editors-Guide.pdf` pp. 352-358 (Editing Using Transcription — append/insert/F12 semantics)
- `DaVinci-Resolve-20-Editors-Guide.pdf` pp. 358-360 (Editing Transcribed Clips in the Timeline — Remove Silent Portions)
- `DaVinci-Resolve-20-Editors-Guide.pdf` p. 496 (Subframe Audio Editing)
- `DaVinci-Resolve-20_Beginners-Guide.pdf` pp. 1-67 (Cut/Edit page basics — fallback workflow for free Resolve, no AI Transcription)
