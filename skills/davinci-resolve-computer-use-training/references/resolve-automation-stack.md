# Resolve Automation Stack

Use DaVinci Resolve's supported automation surfaces in this order.

## 1. Resolve Scripting API

Default to the official Python/Lua scripting API for repeatable operations:

- project/database inspection
- bin creation and media import
- timeline creation and clip placement
- marker creation
- page switching with `resolve.OpenPage(pageName)`
- layout preset import/export
- render preset import/export
- burn-in preset import/export
- render queue setup and render status polling
- project export/archive

Local SDK paths on macOS:

```bash
RESOLVE_SCRIPT_API="/Library/Application Support/Blackmagic Design/DaVinci Resolve/Developer/Scripting"
RESOLVE_SCRIPT_LIB="/Applications/DaVinci Resolve/DaVinci Resolve.app/Contents/Libraries/Fusion/fusionscript.so"
PYTHONPATH="$PYTHONPATH:$RESOLVE_SCRIPT_API/Modules/"
```

The official SDK README and examples are installed at:

- `/Library/Application Support/Blackmagic Design/DaVinci Resolve/Developer/Scripting/README.txt`
- `/Library/Application Support/Blackmagic Design/DaVinci Resolve/Developer/Scripting/Examples`
- `/Library/Application Support/Blackmagic Design/DaVinci Resolve/Developer/Scripting/Modules/DaVinciResolveScript.py`

Resolve must be running unless deliberately launched in `-nogui` mode. For normal HITL editing, keep the UI running.

## 2. Installed Workspace Scripts

For actions the user may invoke manually, install scripts into Resolve's Workspace > Scripts menu.

macOS locations:

- All users: `/Library/Application Support/Blackmagic Design/DaVinci Resolve/Fusion/Scripts`
- Current user: `~/Library/Application Support/Blackmagic Design/DaVinci Resolve/Fusion/Scripts`

Use subfolders by surface:

- `Utility` for all pages
- `Edit`, `Color`, `Deliver`, etc. for page-specific scripts
- `Deliver` scripts also appear under render jobs

Preferred skill pattern:

1. Generate/edit a script in the skills repo.
2. Copy or symlink it into the user Scripts folder.
3. Verify Resolve sees it after restart or script refresh.
4. Keep a command-line entrypoint for automation and a menu entrypoint for HITL.

## 3. Presets, Templates, and Macros

Use Resolve-native assets for reusable production looks:

- Layout presets for consistent UI state.
- Render presets for Instagram, YouTube, review proxies, and archive outputs.
- Burn-in presets for timecode/debug overlays.
- Fusion macros/templates for lower thirds, caption styles, bumpers, motion graphics, and branded overlays.
- PowerGrade/LUT/still workflows for repeatable color look, while avoiding hard-coded destructive grades when a timeline should stay editable.

Skill outputs should prefer importing/installing these reusable assets over recreating UI state by clicking.

## 4. Computer Use

Use Computer Use only for UI learning, verification, and operations the scripting API cannot expose.

Examples:

- proving that a lesson control exists and can be operated
- validating visible UI state with screenshots
- testing manual HITL workflow
- adjusting plugin panels or modal controls that are not scriptable

If Computer Use fails but scripting succeeds, continue with scripting only and record the UI bridge failure. Do not mark UI homework complete.

## 5. External Analysis and Rendering Helpers

Use external tools around Resolve, not instead of it:

- `ffprobe`/`ffmpeg` for media probing, rough loudness checks, proxy generation, and render verification
- Whisper/Gemini/LLM evaluators for transcript/story/quality review
- Rust/Python planners for edit-decision graphs
- Resolve scripting to materialize the planner output into editable timelines

The production handoff target is always a layered Resolve artifact unless the user explicitly asks for a flat render only.

## Required Preflight

Before any Resolve skill edits a project:

1. Confirm Resolve process is running.
2. Confirm scripting API connection.
3. Capture Resolve version, current page, current project, current timeline, database info, and scripting paths.
4. Confirm timeline start frame before placing clips.
5. Confirm target media paths exist and are not AppleDouble `._*` sidecar files.
6. If using Computer Use, call `get_app_state` once and record success/failure separately from scripting readiness.
