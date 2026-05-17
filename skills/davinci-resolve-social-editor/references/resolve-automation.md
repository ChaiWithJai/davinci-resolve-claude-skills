# Resolve Automation Notes

## Resolve Connection

Python scripting normally uses:

```python
sys.path.append('/Library/Application Support/Blackmagic Design/DaVinci Resolve/Developer/Scripting/Modules')
import DaVinciResolveScript as dvr
resolve = dvr.scriptapp('Resolve')
```

If `resolve` is false, launch Resolve and retry. If `dvr.scriptapp('Resolve')` hangs instead of returning, kill the attempt after a short timeout and switch to an in-Resolve script-menu handoff:

1. Copy the automation script into `~/Library/Application Support/Blackmagic Design/DaVinci Resolve/Fusion/Scripts/Edit/`.
2. Run it from Resolve's `Workspace > Scripts` menu after saving the current project.
3. Report that the script was installed but do not claim the timeline import succeeded until Resolve visibly creates the project/timeline or the script returns a project/timeline.

Do not claim a Resolve timeline was created unless the API call returns a project/timeline or the GUI has been verified.

## Project Setup

For social vertical edits:

- Timeline resolution: `1080x1920`
- Frame rate: match source unless user requests otherwise.
- Bins:
  - `Video ISO`
  - `HQ Audio`
  - `Brand`
  - `Renders`
  - `Review`

Import original media and rendered masters. Keep the original `.drp` untouched; create versioned projects/timelines.

## Multicam and Sync

Preferred Resolve-native workflow:

1. Import camera ISOs and HQ audio.
2. Use waveform sync / multicam clip / sync bin when audio tracks are usable.
3. Build an editable timeline with multicam angle switches.
4. Use proxies for speed if camera files are heavy.

If Resolve scripting cannot create the full multicam setup reliably, generate:

- `edit_decisions.csv`
- rough preview render
- optional FCPXML/EDL
- imported rendered-master timeline

## FCPXML/EDL Handoff

Use interchange files when the final creative work should be adjusted manually in Resolve. The planner should output source paths, in/out timestamps, track placement, transitions, and markers.

## Timeline Markers

Add markers or a companion CSV for:

- story beats,
- known weak cuts,
- B-roll needs,
- caption/name verification,
- audio/music check points.

## Layered Social Timeline Standard

Do not stop at an imported rendered master when the user expects to keep editing in Resolve. Build a layered timeline with named tracks:

- `V1 ORIGINAL CAMERA CUTS`
- `V2 BUMPER / B-ROLL COVER`
- `V3 GRAPHICS / TITLE CARDS`
- `V4 CAPTIONS / LOGO`
- `V5 MASTER REFERENCE` disabled by default
- `A1 CLEAN DIALOGUE MIX`
- `A2 ORIGINAL DIALOGUE CUTS` disabled or muted by default for repair
- `A3 MUSIC BED`
- `A4 BUMPER / SFX`

Use `AppendToTimeline([{clipInfo}])` with `mediaType`, `trackIndex`, and `recordFrame` to place original media on the intended tracks. Verify with `GetTrackCount()` and `GetItemListInTrack()` after script execution; the GUI can be zoomed or collapsed and may not visibly show all tracks.

## Visible Start Frame Audit

Resolve timelines commonly start at `01:00:00:00`, which is frame `86400` at 24 fps. When using `AppendToTimeline` with `recordFrame`, the value is an absolute timeline frame, not a zero-based offset from the edit start. Insertions at frame `0` can exist before the visible timeline start, causing the API to report clips while the Edit page appears empty or black.

Always compute:

```python
record_frame = timeline.GetStartFrame() + edit_offset_frames
```

After building a timeline, run `scripts/resolve_timeline_audit.py` and reject timelines where any clip starts before `timeline.GetStartFrame()`.
