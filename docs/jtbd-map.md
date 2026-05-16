# Job → Skill Map

Use this when you want to find the right skill for a specific job. Each row maps a job to be done to the skill that solves it.

## The map

| # | Job to be done | Skill | Notes |
|---|---|---|---|
| 1 | Cut 60-min screen recording into a watchable 8-min demo | `davinci-resolve-cut-screen-recording` | Uses AI Transcription + Remove Silent Portions for the heaviest lift |
| 2 | Make webcam footage look broadcast-quality | `davinci-resolve-color-grade-webcam` | Primary correction + skin-tone refinement |
| 3 | Clean podcast/interview audio | `davinci-resolve-audio-cleanup-podcast` | Clip EQ → De-Hummer → Gate → Noise Reduction → Leveler → Ducker |
| 4 | Branded titles + animated lower-thirds | `davinci-resolve-titles-and-lower-thirds` | Text+ template, save as preset |
| 5 | Animated logo intro from still SVG | `davinci-resolve-titles-and-lower-thirds` (merged) | Same Text+/Fusion tooling; treated as the "transform a still" subcase |
| 6 | Export for YouTube + LinkedIn + Reels | `davinci-resolve-export-multi-platform` | AI Smart Reframe + custom render presets + Python automation |
| 7 | Reusable DevRel project template | `davinci-resolve-devrel-project-template` | Bins, timeline, render queue presets, color preset |
| 8 | Auto-transcribed captions + fix errors | `davinci-resolve-export-multi-platform` (merged) | Subtitle track + Create Subtitles from Audio workflow |
| 9 | Batch-render with Python scripting API | `davinci-resolve-export-multi-platform` (script lives there) | `scripts/multi_platform_render.py` |
| 10 | Troubleshoot "why is X broken" | `davinci-resolve-troubleshooting` | Top 5: red playback indicator, missing media, audio out of sync, GPU crashes, render queue stalls |

Plus one foundational skill — `davinci-resolve-setup` — that the other seven all assume.

## Why some jobs were merged into existing skills

- **Animated logo (job #5)** shares the **Text+** node and Fusion animation modifiers with lower-thirds. The mental model "use Text+, then animate a transform parameter" is identical for both cases.
- **Captions (job #8)** lives entirely in the Deliver workflow and uses the same Subtitle track that the multi-platform export skill already needs.

## Jobs not yet in this repo (and why)

These would be valuable but did not make the first cut:

- **`davinci-resolve-multicam-interview`** — useful for podcast/talkshow setups with 2-3 cameras. Deferred because most content is single-camera. Editor's Guide pp. 197-243 covers the full multicam workflow.
- **`davinci-resolve-green-screen-keying`** — Fusion-based, requires the Delta Keyer (Fusion VFX Guide pp. 111-138). Deferred because most company demo videos are screen recordings, not chroma-key shoots.
- **`davinci-resolve-dolby-atmos-immersive`** — Fairlight Audio Post pp. 643-724. Deferred — overkill for the typical audience.
- **`davinci-resolve-3d-camera-tracking`** — Advanced VFX pp. 129-159. Same reason.

If your job is one of these, the relevant wiki under `docs/wiki/` is your starting point, and the PDF pages cited there are the ground truth.

## When not to use these skills

These skills are not a Resolve tutorial. If you have never opened DaVinci Resolve before, start with the Beginner's Guide PDF (or Blackmagic Design's free 8-hour video course) and then come back here. These skills assume:

- You have Resolve 20 (free or Studio) installed.
- You know what a timeline is.
- You know that the bottom of the Resolve interface has seven pages (Media, Cut, Edit, Fusion, Color, Fairlight, Deliver).
- You have a real project to ship — not a homework exercise.
