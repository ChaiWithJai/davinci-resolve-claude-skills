---
name: davinci-resolve-computer-use-training
description: Use when the user wants Codex to learn DaVinci Resolve through Blackmagic Design lesson homework, operate the Resolve UI with Computer Use, validate skills against real Resolve behavior, or build a capstone workflow that turns local/T7 media into Instagram and YouTube cuts.
---

# DaVinci Resolve Computer Use Training

Use this skill for lesson-by-lesson Resolve practice and for improving Resolve skills from observed UI behavior.

## Automation Priority

Default to DaVinci Resolve's supported scripting and preset systems before UI automation:

1. Use the official Resolve Python/Lua scripting API for project setup, media import, timeline construction, markers, render queue work, preset import/export, and verification.
2. Use installed Workspace scripts, render presets, burn-in presets, layout presets, Fusion macros/templates, PowerGrades/LUTs, and reusable project templates for batteries-included repeatability.
3. Use Computer Use for UI homework, screenshot evidence, manual HITL validation, and controls the scripting API cannot expose.
4. Use external tools such as `ffprobe`, `ffmpeg`, Whisper/Gemini, Rust/Python edit planners, and audio/video analyzers around Resolve; materialize final decisions back into editable Resolve timelines.

Before any lesson or production edit, run or emulate `scripts/resolve_doctor.py` to confirm process state, scripting paths, Resolve version, current project/timeline, current page, database, and timeline start frame.

Use `bin/resolve-kit` for repeatable local execution:

- `resolve-kit doctor`
- `resolve-kit install`
- `resolve-kit stage-folder <folder>`
- `resolve-kit validate --project <name> --timeline <name>`
- `resolve-kit capstone <folder>`

## Core Loop

For every lesson:

1. Read the lesson map entry and the cited PDF page range.
2. Create a homework card with objective, required media/project, UI pages, expected artifact, and validation checks.
3. Use Resolve scripting for setup, inspection, and repeatable verification. Use Computer Use for the UI steps when the point is specifically to learn Resolve operation or validate HITL controls.
4. Capture evidence: screenshot/state notes, project/timeline name, exported file path, markers, and any logs.
5. Record failure modes: inaccessible control, wrong page, missing media, UI ambiguity, scripting mismatch, render/export failure, or quality failure.
6. Update the relevant production skill if the lesson teaches a durable workflow or catches a bad assumption.

## Computer Use Rules

- Start each UI session with `get_app_state` for DaVinci Resolve.
- Prefer accessibility element clicks. Use coordinates only when the Resolve canvas/tool surface exposes no useful element.
- After each meaningful action, call `get_app_state` or use the action result to verify the UI changed.
- Do not use UI automation for long repeated setup if Resolve scripting can do it more reliably. Use scripts to stage projects, then Computer Use to learn/edit/verify the interaction.
- If `list_apps` or `get_app_state` times out, do not claim the UI lesson is complete. Verify the Resolve process and scripting API, record the bridge failure in the lesson journal, and only use scripting to stage a practice artifact or inspect the project.
- Resolve scripting API availability varies by install. Prefer project timeline lookup by index when name-based lookup is unavailable, save through `ProjectManager.SaveProject`, and always use `timeline.GetStartFrame()` when placing clips so media appears at Resolve's `01:00:00:00` timeline origin.
- Keep a per-lesson journal in `training_runs/<book>/<lesson>/journal.md`.
- Keep screenshots or stills in the same folder when possible.

## Resolve Scripting Rules

- Use the local SDK paths from `references/resolve-automation-stack.md`.
- Always set `RESOLVE_SCRIPT_API`, `RESOLVE_SCRIPT_LIB`, and `PYTHONPATH`/`sys.path` before importing `DaVinciResolveScript`.
- Keep reusable scripts installable under the user's Resolve Scripts folder so they can be invoked from Workspace > Scripts.
- Prefer importing render, burn-in, layout, Fusion macro, and project-template assets over recreating equivalent state through UI clicks.
- Save through `ProjectManager.SaveProject()`.
- Validate by reading the project/timeline back through the API after writing.
- Never flatten the handoff unless the user asks for a flat render only; preserve layered tracks, markers, disabled repair/reference tracks, captions, and B-roll.

## Homework Card Schema

Each lesson should produce a JSON or Markdown card with:

- `book`
- `lesson_number`
- `lesson_title`
- `pdf_pages`
- `target_resolve_pages`
- `homework_objective`
- `source_media_needed`
- `ui_actions_to_learn`
- `automation_candidates`
- `expected_artifact`
- `validation_checks`
- `skill_updates`

## Skill Validation

When validating `davinci-resolve-claude-skills`:

- Check whether a skill cites the correct PDF lesson/page range.
- Check whether it has a verification section.
- Check whether it distinguishes UI-only steps from scripting API steps.
- Check whether Studio-only features are clearly marked.
- Check whether it handles failures discovered by prior video-editing traces: bad audio, missing captions, flattened timelines, frame offsets, stale media pool items, subject out of frame, and transcript-only jump cuts.

## Capstone Contract

The capstone must prove the full workflow:

- Input: any local or T7 folder with camera/audio/media assets.
- Output 1: Instagram vertical cut, target up to 3 minutes, speaker-first, burned-in captions, B-roll, audio in social loudness range.
- Output 2: YouTube/long-form 16:9 cut, up to 12 minutes, coherent story, clean audio, graded visuals.
- Resolve handoff: layered editable timelines, disabled repair/reference tracks, markers, edit decisions, B-roll plan, captions, and render verification.
- Website bridge: markdown or copy block for `chaiwithjai.com/workshops` using the video story.

## Anti-Reward-Hacking Gate

Never count a Loom upload, flat render, generated preview, or seed timeline as the capstone. Those are distribution or scaffolding artifacts only.

Never count shared screenshots across all lessons as lesson completion. Page visibility proves only that the app opened. It does not prove the class/homework concept was performed.

Before calling homework or capstone complete, produce an auditable proof bundle:

- `homework_coverage_matrix.md/json` covering every mapped workbook lesson.
- Per-lesson `homework_card.json`, `journal.md`, and `validation_report.md`.
- A clear status for each lesson:
  - `manual_ui_verified` only when Computer Use or human UI evidence proves the Resolve UI homework was performed.
  - `manual_ui_screenshot_verified` when Resolve's supported scripting/menus navigate the live app and macOS screenshots prove the UI state, because Computer Use is known to time out against Resolve on this machine.
  - `script_api_verified` when Resolve scripting created and read back the artifact.
  - `capstone_applied_script_verified_ui_blocked` when the lesson was applied to the capstone through scripting but Computer Use timed out.
  - `not_started` when there is no proof.
- Capstone acceptance report tying lesson groups to concrete Resolve timelines, source clips, captions, audio checks, color/visual checks, renders, and website copy.

If Computer Use times out, do not say the UI homework is complete. Record the timeout and continue with supported Resolve scripting for practical progress.

## DeepWiki Benchmark Gate

Before saying a capstone follows the classes, benchmark it against the local DeepWiki at the repo DeepWiki under `docs/wiki/` and fail it honestly when the artifact lacks the workbook competency.

Required capstone competency groups:

- Editing: semantic A-roll spine, B-roll over jumps, multicam/synced angle strategy, subject-safe vertical reframing, proofread captions.
- Fairlight: source/processed/music/SFX lanes, cleanup order proof (`Clip EQ -> De-Hummer -> Gate -> Noise Reduction -> Leveler`), music ducking below dialogue, LUFS/dBTP verification.
- Color: scope-based primary correction, named node order (`Normalize -> Balance -> Enhance -> Skin/Secondaries`), shot matching across cameras, vibrant but non-crushed delivery.
- Fusion/graphics: Text+ or Fusion caption/lower-third system, reusable macro/template for titles/bumper, editable graphics on separate tracks.
- Delivery: separate Instagram and YouTube timelines, presets/validation, project export, and human-editable handoff.

Status rules:

- `PASS` only when the Resolve artifact or exported audit proves the competency.
- `PARTIAL` only when the competency exists but lacks workbook-grade proof or editability.
- `FAIL` when the artifact uses a flat/rendered shortcut, screenshot-only proof, or omits the workflow.

Write the benchmark to `resolve_kit/status/deepwiki_capstone_benchmark_*.md/json` and let it drive the next repair pass. A capstone under 85/100 is not publish-ready and must not be described as class-complete.

## Source Workbook Benchmark Gate

The DeepWiki is not enough when the user asks whether the work follows the classes. The source-workbook benchmark must run against all 52 mapped workbook lessons using `references/resolve20-homework-map.md` and local PDF text exported from the Blackmagic workbooks, or the configured `RESOLVE_PDF_TEXT_DIR`.

Rules:

- Score every mapped lesson as `PASS`, `PARTIAL`, or `FAIL`.
- `PASS` requires workbook-grade/native Resolve evidence for that lesson's actual tool or workflow.
- `PARTIAL` is allowed only for adjacent production evidence that does not prove the native workbook workflow.
- `FAIL` is required for omitted lessons, pre-rendered shortcuts, screenshots that only show page visibility, or features represented by assets instead of Resolve workflows.
- If the source-workbook score is under 85/100, do not call the homework or capstone complete.
- If the user asked to do all homework, advanced/irrelevant lessons still fail unless there is a separate lesson artifact proving them; do not mark them N/A just because they are unnecessary for the capstone.

Write the source-workbook benchmark to `resolve_kit/status/source_workbook_capstone_benchmark_*.md/json` and report the score before attempting any further hillclimb.

## Workbook-Derived Quality Bar

Across the 52 mapped lessons, carry these checks into every production capstone:

- Editing: cut on semantic beats, preserve audio continuity, use B-roll to cover jumps, and expose markers for HITL review.
- Audio: select the best source by audit and listening, clean rumble/hum/noise before leveling, duck music under speech, and verify loudness.
- Color: balance and match cameras before stylizing; for Chai With Jai, target vibrant broadcast/documentary color without crushed shadows.
- Fusion/graphics: captions, titles, lower thirds, bumpers, and reference overlays must stay editable on separate tracks.
- Delivery: produce separate Instagram and YouTube timelines, validate aspect ratio, safe zones, captions, audio, and render playback.
- Automation: prefer Resolve API, macros, presets, and templates; use Computer Use for UI proof only.

## References

- `references/resolve20-homework-map.md` for the full book/lesson map.
- `references/computer-use-journal-template.md` for per-lesson journals.
- `references/resolve-automation-stack.md` for the supported Resolve scripting, preset, macro, and Computer Use hierarchy.
