# Resolve SDK Notes

These notes are from the locally installed Resolve 20 scripting SDK README dated May 7, 2025.

## Supported Invocation

- Python and Lua scripts are supported.
- Resolve must be running for normal external scripting.
- Scripts can be run from the Fusion console, from the command line, or from Resolve's Workspace > Scripts menu.
- External scripting access is controlled in Resolve Preferences. Use local access for Codex workflows unless a network workflow is explicitly required.

## Local macOS Environment

```bash
export RESOLVE_SCRIPT_API="/Library/Application Support/Blackmagic Design/DaVinci Resolve/Developer/Scripting"
export RESOLVE_SCRIPT_LIB="/Applications/DaVinci Resolve/DaVinci Resolve.app/Contents/Libraries/Fusion/fusionscript.so"
export PYTHONPATH="$PYTHONPATH:$RESOLVE_SCRIPT_API/Modules/"
```

## Script Menu Install Paths

```text
/Library/Application Support/Blackmagic Design/DaVinci Resolve/Fusion/Scripts
~/Library/Application Support/Blackmagic Design/DaVinci Resolve/Fusion/Scripts
```

Place scripts under:

- `Utility` for all pages
- page folders such as `Edit`, `Color`, or `Deliver` for page-specific actions
- `Deliver` when render-job menu availability is useful

## APIs We Should Prefer

- `resolve.OpenPage("media" | "cut" | "edit" | "fusion" | "color" | "fairlight" | "deliver")`
- `resolve.GetCurrentPage()`
- `resolve.LoadLayoutPreset`, `SaveLayoutPreset`, `ImportLayoutPreset`, `ExportLayoutPreset`
- `resolve.ImportRenderPreset`, `ExportRenderPreset`
- `resolve.ImportBurnInPreset`, `ExportBurnInPreset`
- `ProjectManager.CreateProject`, `LoadProject`, `SaveProject`, `ExportProject`, `ArchiveProject`
- `Project.GetCurrentTimeline`, `GetTimelineByIndex`, `SetCurrentTimeline`
- `Project.SetRenderSettings`, `AddRenderJob`, `StartRendering`, `GetRenderJobStatus`
- `MediaStorage.AddItemListToMediaPool`
- `MediaPool.CreateEmptyTimeline`, `AppendToTimeline`, `CreateTimelineFromClips`
- `Timeline.InsertFusionTitleIntoTimeline`, `InsertFusionCompositionIntoTimeline`, `InsertFusionGeneratorIntoTimeline`
- `TimelineItem.ImportFusionComp`, `ExportFusionComp`, `LoadBurnInPreset`

## Practical Implication

Most production work should be script-first. UI automation is for proving manual workflows, catching screenshots, and operating non-scriptable controls.
