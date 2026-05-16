---
name: davinci-resolve-devrel-project-template
description: Use when a user wants a reusable DaVinci Resolve project structure for shipping DevRel videos repeatedly — sets up bins, timeline, render presets, and a color preset so future videos start with one click instead of one hour. Triggering symptoms include phrases like "set up a Resolve template", "reusable project structure", "every video starts from scratch", "save my Resolve setup as a preset", or "DevRel video workflow."
---

# DaVinci Resolve — reusable DevRel project template

## Overview

A pre-configured Resolve project that you duplicate for every new video. It contains: a sensible bin hierarchy, a 1080p / 23.976 fps timeline, three render presets (YouTube 16:9, LinkedIn 1:1, Shorts 9:16), a starter color node tree, and a 100-track Fairlight timeline preset. Saved once, reused forever.

## When to use

Symptoms:
- You ship a new video every 1-4 weeks for the same channel/audience
- You catch yourself recreating the same bin structure every time
- You want render queue presets that match your platforms' specs
- A teammate keeps asking "what render settings do you use for X"

When NOT to use:
- You only ship one or two videos a year (the setup cost is not worth it).
- You are editing a one-off feature film (different structural needs).

## Quick reference

| Asset | What is in it |
|---|---|
| Bin structure | `01 — Footage`, `02 — Audio`, `03 — Music`, `04 — Graphics`, `05 — SFX`, `06 — VO`, `07 — Timelines`, `08 — Exports` |
| Master timeline | 1920x1080, 23.976 fps, 5-track audio (Dialogue / VO / SFX / Music / Bus) |
| Render presets | YouTube 1080p H.264, LinkedIn Square 1080x1080, Shorts 1080x1920 |
| Color preset | "Webcam Look" PowerGrade — see `davinci-resolve-color-grade-webcam` for what is in it |
| Fairlight preset | Saved 5-track configuration in Presets Library |

## Steps

### 1. Create the empty project that becomes the template

1. In the Project Manager, click **New Project**.
2. Name it `DEVREL_TEMPLATE_v1`.
3. Double-click to open it.

### 2. Build the bin hierarchy in the Media Pool

1. Press Shift-4 to go to the Edit page (or click Edit at the bottom).
2. Open the Media Pool (top-left button).
3. Right-click the **Master** bin > **New Bin**. Name it `01 — Footage`.
4. Repeat for: `02 — Audio`, `03 — Music`, `04 — Graphics`, `05 — SFX`, `06 — VO`, `07 — Timelines`, `08 — Exports`.

The numeric prefixes force the bins to sort in workflow order. See `templates/devrel-bin-structure.txt` in this skill for a copy-pasteable list.

### 3. Build a Power Bin that survives across projects

Standard bins are project-scoped. **Power Bins** are project-library-scoped — perfect for music stings, brand logos, animated graphics you reuse.

1. **View menu > Show Power Bins**.
2. In the Power Bins panel, right-click > **New Bin**. Name it `BRAND ASSETS`.
3. Drag your logo PNG/SVG and any reusable music files in. Future projects in the same library will see this bin.

Editor's Guide p. 317 covers Power Bins in detail.

### 4. Create the master timeline

1. **File > New Timeline** (Cmd-N / Ctrl-N).
2. Uncheck **Use Project Settings**.
3. Set:
   - Timeline name: `MASTER_TIMELINE`
   - Start Timecode: `01:00:00:00` (standard broadcast convention)
   - Video tracks: 3 (V1: main, V2: titles, V3: B-roll/overlays)
   - Audio tracks: 5 (Stereo on all)
   - Resolution: 1920x1080
   - Frame rate: 23.976 (or 29.97 if your audience is North American TV-trained, or 25 if you are in Europe)
4. Create. Move the new timeline to the `07 — Timelines` bin.

### 5. Name and color-code the audio tracks

1. Double-click the **Audio 1** track name and rename to `DIALOGUE`. Right-click the track header > color > Teal.
2. Repeat:
   - Audio 2: `VO` (Violet)
   - Audio 3: `SFX` (Orange)
   - Audio 4: `MUSIC` (Olive)
   - Audio 5: `BUS` (Gray — this is your scratch/safety track)
3. Right-click any track > **Lock Track** if you want to prevent accidental edits later.

This naming is loosely based on the structure shown in Fairlight Audio Post pp. 527-528 for documentary projects.

### 6. Save the Fairlight timeline configuration as a preset

This is the magic: the entire timeline structure (tracks, busses, names) can be saved as a Fairlight Configuration Preset and applied to any future new timeline.

1. Press Shift-7 to switch to the Fairlight page.
2. **Fairlight menu > Presets Library**.
3. Change **Filter by** dropdown to **Fairlight Configuration Presets**.
4. Click **Save New**. In the dialog, click **Create New**.
5. Name it `DEVREL_5_TRACK_TEMPLATE`. Click **OK**.

Now any new timeline created in this project (or any project in the same library) can opt into this preset via the **Use Fairlight Preset** checkbox when creating.

Fairlight Audio Post pp. 530-531 documents this workflow.

### 7. Build the three render presets — YouTube, LinkedIn, Shorts

Each preset reuses the same source timeline but with different reframing and dimensions. See the dedicated skill `davinci-resolve-export-multi-platform` for the full workflow including AI Smart Reframe. Here is the short version for getting the presets saved into the template:

1. Press Shift-8 to switch to the Deliver page.
2. In **Render Settings**, click **H.264 Master**.
3. Set **File Name** field to `%timeline_name` (variable). Click the variable dropdown if you want `%timestamp` appended.
4. Set Resolution: 1920x1080, Frame Rate: Timeline Resolution.
5. **Audio tab > Audio Normalization > Optimize to standard > Standard: YouTube**. This bakes in YouTube's -14 LUFS standard.
6. Click the Options menu (`...`) at the top of Render Settings > **Save As New Preset**.
7. Name: `DEVREL_YOUTUBE_1080`. Check **Add to quick export**. Save.
8. Repeat for LinkedIn (1080x1080, audio standard = streaming) and Shorts (1080x1920, audio standard = streaming).

Editor's Guide pp. 577-580 documents this exact workflow including the YouTube audio normalization standard at -14 LKFS / -1.0 dBTP.

### 8. Save the project as a template

Resolve does not have a true "save as template" command — the workflow is to **duplicate** the project for each new edit.

1. Close the project (File > Close Current Project, or just go back to Project Manager).
2. In Project Manager, right-click `DEVREL_TEMPLATE_v1` > **Duplicate**.
3. Rename the duplicate to `2026-05-WhateverVideo`.
4. Open the duplicate, replace media, edit. Your template stays clean.

You can also **Export Project Archive** (right-click in Project Manager) to ship the template as a `.dra` file to teammates.

## Common mistakes

- **Treating Smart Bins like Folder Bins** -> Smart Bins are dynamic queries (e.g. "all clips tagged 'interview'"). They are not folders. Use regular bins for hierarchy and Smart Bins for filtering. Editor's Guide p. 302.
- **Forgetting that Power Bins span projects** -> If you delete a clip from a Power Bin while editing one project, it disappears from every project that uses that Power Bin. Be careful.
- **Picking the wrong frame rate** -> Once a timeline has clips in it, changing the frame rate causes retiming. Decide upfront. 23.976 is the cinematic standard; use 29.97 if your audience watches your videos on a North-American TV; use 25 if you are in Europe.
- **Saving the YouTube render preset without enabling audio normalization** -> your audio will be inconsistent across uploads. Always enable Optimize to standard.

## Verification

You succeeded if all of the following are true:

1. Project Manager shows `DEVREL_TEMPLATE_v1` and you can right-click > Duplicate it.
2. Opening the template shows the eight numbered bins in the Media Pool.
3. The Quick Export menu (Edit page > top-right cloud icon) shows your `DEVREL_YOUTUBE_1080`, `DEVREL_LINKEDIN_1080`, `DEVREL_SHORTS_1080` presets.
4. Creating a new timeline with **Use Fairlight Preset** checked offers `DEVREL_5_TRACK_TEMPLATE` in the dropdown.
5. The duplicate project (your actual working project) has empty bins but identical structure.

## Transfer

Now try this: ship one real video using the duplicated project. After you have shipped, go back to the template and add anything you wished was there (a specific lower-third graphic, an SFX bin you reused, an additional render preset for Twitter/X). Version-bump the template to `DEVREL_TEMPLATE_v2`. Templates compound — each iteration shortens future setup time.

## Working reference

- `docs/wiki/editors-guide.md#lesson-5--project-organization-pp-245-321` (bins, Smart Bins, Power Bins — primary)
- `docs/wiki/editors-guide.md#lesson-9--delivering-projects-pp-545-617` (render presets workflow)
- `docs/wiki/fairlight-audio-post.md#lesson-8--busses-and-nested-timelines-pp-475-533` (Fairlight timeline preset)
- `docs/wiki/master.md#shared-glossary-terms-that-appear-across-multiple-pdfs` (bin vs Smart Bin vs Power Bin definitions)

## When the agent's work isn't matching expectations (context-rot reset)

If the user pushes back on the template structure, bin types, render presets, or Fairlight preset workflow, read these PDF page ranges to reset:

- `DaVinci-Resolve-20-Editors-Guide.pdf` pp. 246-321 (Lesson 5 — Project Organization, full bin/metadata workflow)
- `DaVinci-Resolve-20-Editors-Guide.pdf` pp. 317-321 (Power Bins — specifically the library-scoping behavior)
- `DaVinci-Resolve-20-Editors-Guide.pdf` pp. 577-580 (Creating a Custom Render Preset)
- `DaVinci-Resolve-20-Editors-Guide.pdf` pp. 246-253 (Creating a New Project and Project Settings)
- `DaVinci-Resolve-20-Fairlight-Audio-Post.pdf` pp. 525-532 (Creating a Timeline Template)
- `DaVinci-Resolve-20-Fairlight-Audio-Post.pdf` pp. 530-532 (Saving a Timeline Configuration in the Presets Library)
