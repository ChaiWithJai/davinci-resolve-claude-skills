---
name: davinci-resolve-export-multi-platform
description: Use when a user needs to export the same DaVinci Resolve edit for multiple platforms — YouTube (16:9), LinkedIn (square 1:1), Reels/Shorts/TikTok (9:16) — with correct dimensions, loudness, and optionally batch automation. Triggering symptoms include phrases like "export for YouTube and LinkedIn", "make a vertical version", "9:16 from my 16:9 edit", "render the same edit three times", "batch render", "generate captions", or any DaVinci Resolve Deliver/render question.
---

# DaVinci Resolve — export the same edit for YouTube, LinkedIn, and Shorts

## Overview

One source edit, three platform-specific exports, optionally automated with Python. The core principle: **let Resolve's AI Smart Reframe do the reframing for you** — do not manually keyframe Position for every clip when you change aspect ratio. Then save custom render presets so the next video is a one-click affair.

This skill also covers two merged JTBDs: **auto-generating subtitles** and **batch-rendering with the Python API**.

## When to use

Symptoms:
- Need to ship the same video to YouTube + LinkedIn + Reels/Shorts/TikTok
- Need a vertical version of an existing 16:9 edit
- Need to add captions/subtitles to your video
- Want to automate "render this and that and the other" with a script
- Have multiple timelines to render in series and do not want to babysit Resolve

When NOT to use:
- One-off rendering of a single platform — use Quick Export (Edit page top-right cloud icon).
- DCP (digital cinema) export — separate Colorist Guide workflow (pp. 431-447).

## Quick reference

| Target | Resolution | Audio standard | Codec |
|---|---|---|---|
| YouTube (long-form) | 1920x1080 (or 3840x2160) | YouTube (-14 LUFS) | H.264 or H.265 |
| LinkedIn (feed) | 1080x1080 (square) | Streaming (-16 LUFS) | H.264 |
| Reels / Shorts / TikTok | 1080x1920 (vertical) | Streaming (-16 LUFS) | H.264 |

For HITL Resolve handoffs, create separate timelines before rendering:

- `Instagram Semantic Cut` or equivalent for vertical social.
- `YouTube Semantic Cut` or equivalent for horizontal long form.
- V1/V2/V3 for source picture layers.
- V4 for burned-caption/title graphics.
- A1/A2 for source and processed dialogue.
- A3/A4 for music, SFX, bumpers.

Do not treat an SRT file as enough when the user asked for burned-in Netflix-style captions. Captions must be visible in the video frame and editable as a layer or template until final render.

## Steps

### Phase 1 — Reframe your 16:9 source for vertical and square versions

Editor's Guide pp. 569-575 covers AI Smart Reframe.

1. Press **Shift-4** to go to the Edit page.
2. Right-click your master timeline in the Media Pool > **Duplicate Timeline**. Name the duplicate `MASTER_TIMELINE_VERTICAL`.
3. Open the duplicate. In the timeline, click the **Timeline Resolution** dropdown (top of the viewer) > custom > set to `1080x1920` (vertical).
4. Resolve will warn that clips will be cropped. Click OK.
5. Select all clips. Right-click > **Smart Reframe** (Studio only — for free Resolve, use manual keyframes via the **Position** parameter in the Inspector).
6. In the Smart Reframe dialog, choose **Object of Interest: Auto** and click **Reframe**. Resolve adds keyframes that keep the main subject in frame even as the aspect ratio crops the edges.
7. Scrub through and check — if a clip drifted (e.g. the AI followed the wrong person), select that clip and either:
   - Reset Position keyframes and use the **Reference Point** mode to manually click the subject
   - Or set Position X manually via the Inspector
8. Repeat for `MASTER_TIMELINE_SQUARE` at `1080x1080`.

Editor's Guide pp. 572-575 covers the Reference Point fallback when AI Smart Reframe picks the wrong subject.

### Phase 2 — Add captions with AI-generated subtitles

Editor's Guide pp. 586-590 covers Create Subtitles from Audio.

1. With your timeline open, choose **Timeline menu > AI Tools > Create Subtitles from Audio**.
2. In the dialog:
   - **Language**: Auto (or specific language)
   - **Caption Preset**: Subtitle Default
   - **Maximum**: 42 characters per line
   - **Lines**: Single (or Double if you have very long sentences)
   - **Gap Between Subtitles**: 0 frames
3. Click **Create**. Resolve transcribes and adds a Subtitle track to your timeline.
4. **Fix the inevitable errors** — playback the timeline, double-click any subtitle clip in the Subtitle track to edit the text. The AI gets technical terms, brand names, and acronyms wrong constantly.
5. To export subtitles as an SRT file, right-click the Subtitle track > **Export Subtitles** > choose SRT format.

### Phase 3 — Build the three render presets

Editor's Guide pp. 577-580 covers Save As New Preset.

1. Press **Shift-8** to switch to the **Deliver** page.
2. In Render Settings, click **H.264 Master**.
3. Configure:
   - **File Name**: type `%timeline_name` then choose the Timeline Name variable from the dropdown
   - **Location**: browse to your `08 — Exports` folder
   - **Render**: Single clip
   - **Video tab**: Format = MP4, Codec = H.264, Resolution = Timeline Resolution (this picks up the current timeline's dimensions)
   - **Audio tab > Export Audio**: ON, Codec AAC, Bit Rate 320 Kb/s
   - **Audio tab > Audio Normalization**: enable **Normalize Audio** > **Optimize to standard** > Standard = **YouTube** (-14 LUFS, -1.0 dBTP)
4. Click the Options menu (`...`) at top of Render Settings > **Save As New Preset**.
5. Name: `DEVREL_YOUTUBE_1080`. Check **Add to quick export**. Save.
6. Repeat for **LinkedIn** (1080x1080, audio standard = Streaming) and **Shorts** (1080x1920, audio standard = Streaming).

### Phase 4 — Queue and render all three

1. Open your **YouTube** timeline > Deliver page > select `DEVREL_YOUTUBE_1080` preset > click **Add to Render Queue**.
2. Switch to your **LinkedIn** timeline > Deliver page > select `DEVREL_LINKEDIN_1080` preset > **Add to Render Queue**.
3. Switch to your **Shorts** timeline > Deliver page > select `DEVREL_SHORTS_1080` preset > **Add to Render Queue**.
4. In the Render Queue panel (right side), click **Render All**.
5. Walk away. Resolve renders all three serially.

## Python automation — batch render multiple timelines

This is the merged "batch render with Python API" JTBD. The script below assumes Resolve is running, a project is open, and you have already saved render presets named `DEVREL_YOUTUBE_1080`, `DEVREL_LINKEDIN_1080`, `DEVREL_SHORTS_1080`. The script walks every timeline in the project and adds a render job for each preset that matches the timeline's aspect ratio.

See `scripts/multi_platform_render.py` for the full script.

The script uses the official DaVinci Resolve scripting API as documented in `DaVinci Resolve/Developer/Scripting/README.txt`:

```python
Resolve.GetProjectManager()
ProjectManager.GetCurrentProject()
Project.GetTimelineByIndex(idx)
Project.GetTimelineCount()
Project.LoadRenderPreset(preset_name)
Project.SetRenderSettings(settings_dict)
Project.AddRenderJob()
Project.StartRendering()
Project.IsRenderingInProgress()
```

These methods are real and documented. The script has been written defensively — it prints what it would do before doing it, and it confirms via stdin before starting the actual render.

## Common mistakes

- **Manually keyframing Position to vertical-frame every clip** -> there is a button for that. Use AI Smart Reframe (Studio) or at minimum the per-clip Reframe button in the Inspector. (Editor's Guide pp. 572-575.) **(This is the misconception this skill addresses head-on.)**
- **Saving the YouTube preset without enabling audio normalization** -> your videos will be inconsistent across uploads. Always enable Optimize to standard.
- **Forgetting that AI Smart Reframe is Studio-only** -> free Resolve has manual Position keyframes only. Either upgrade or accept manual reframing.
- **Trusting AI-generated subtitles without proofreading** -> always playback and fix. They will mangle product names, acronyms, and technical jargon.
- **Rendering all three timelines at once on a single GPU** -> Resolve renders serially anyway. There is no penalty for queueing all three; do not start three Resolve instances.

## Verification

You succeeded if all of the following are true:

1. Your `08 — Exports` folder contains three MP4 files: one 1920x1080, one 1080x1080, one 1080x1920.
2. Each file plays cleanly when dragged into VLC / QuickTime.
3. The vertical version keeps the main subject in frame for the entire duration (no awkward background-only stretches).
4. Subtitles burn in correctly on platforms that auto-display them, or are exported as `.srt` for upload alongside the MP4.
5. Audio loudness measured by a third-party LUFS meter (e.g. YouLean Loudness Meter, free) reads -14 LUFS ±1 for the YouTube file.

## Transfer

Now try this: add a fourth target — Twitter / X video at 1920x1080 but capped at 2:20 duration. Build a Twitter timeline that is a shorter cut of your master (use the trim workflow from `davinci-resolve-cut-screen-recording`). Save a new `DEVREL_TWITTER_1080` render preset. Add it to the Python script. You now have a one-script, four-platform export pipeline.

## Working reference

- `docs/wiki/editors-guide.md#lesson-9--delivering-projects-pp-545-617` (full Deliver chapter — primary)
- `docs/wiki/editors-guide.md#lesson-9--delivering-projects-pp-545-617` (AI Smart Reframe specifics inside the chapter notes)
- `docs/wiki/master.md#shared-glossary-terms-that-appear-across-multiple-pdfs` (LUFS / dBTP / AI Smart Reframe glossary)
- `docs/wiki/master.md#reset-matrix--when-the-user-pushes-back-read-this` (Smart Reframe + render failure rows)

## When the agent's work isn't matching expectations (context-rot reset)

If the user reports Smart Reframe drift, render failures, missing subtitles, or wrong loudness on delivered files, read these PDF page ranges to reset:

- `DaVinci-Resolve-20-Editors-Guide.pdf` pp. 545-617 (Lesson 9 — Delivering Projects, full chapter)
- `DaVinci-Resolve-20-Editors-Guide.pdf` pp. 569-575 (AI Smart Reframe — Object of Interest vs Reference Point modes)
- `DaVinci-Resolve-20-Editors-Guide.pdf` pp. 577-580 (Creating a Custom Render Preset)
- `DaVinci-Resolve-20-Editors-Guide.pdf` pp. 586-590 (Generating Subtitles from Audio)
- `DaVinci-Resolve-20-Editors-Guide.pdf` pp. 597-617 (Customizing Deliver Presets, Verifying the Exported Files)
- DaVinci Resolve Scripting API: `DaVinci Resolve/Developer/Scripting/README.txt` (shipped with installer)
