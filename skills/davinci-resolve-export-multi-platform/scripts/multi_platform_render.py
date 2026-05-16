#!/usr/bin/env python3
"""
multi_platform_render.py — Queue and render every timeline in the current
DaVinci Resolve project against a matching platform preset, based on the
timeline's aspect ratio.

This script:
  1. Walks every timeline in the current project.
  2. Determines each timeline's aspect ratio (16:9, 1:1, or 9:16).
  3. Loads the matching render preset by name.
  4. Adds a render job to the Render Queue.
  5. Asks for stdin confirmation before starting the actual render.
  6. Calls StartRendering() and reports progress.

Required preset names (rename in PRESET_BY_ASPECT below if yours differ):
  - "DEVREL_YOUTUBE_1080"   for 16:9 (1920x1080)
  - "DEVREL_LINKEDIN_1080"  for 1:1  (1080x1080)
  - "DEVREL_SHORTS_1080"    for 9:16 (1080x1920)

Requirements:
  - DaVinci Resolve 20 (free or Studio) running with a project open.
  - The three render presets above must already exist. Create them by
    following the steps in SKILL.md (Phase 3 — Build the three render
    presets).
  - External scripting enabled: Preferences > System > General >
    External scripting using = Local.
  - Python 3.9+.

Run from terminal (macOS example):
  export RESOLVE_SCRIPT_API="/Library/Application Support/Blackmagic Design/DaVinci Resolve/Developer/Scripting"
  export RESOLVE_SCRIPT_LIB="/Applications/DaVinci Resolve/DaVinci Resolve.app/Contents/Libraries/Fusion/fusionscript.so"
  export PYTHONPATH="$PYTHONPATH:$RESOLVE_SCRIPT_API/Modules/"
  python3 multi_platform_render.py

API surface used (all documented in Reference Manual and Developer/Scripting/README.txt):
  Resolve.GetProjectManager()
  ProjectManager.GetCurrentProject()
  Project.GetTimelineCount()
  Project.GetTimelineByIndex(idx)
  Project.SetCurrentTimeline(timeline)
  Project.LoadRenderPreset(presetName)
  Project.SetRenderSettings(settings_dict)
  Project.AddRenderJob()
  Project.StartRendering()
  Project.IsRenderingInProgress()
  Project.GetRenderJobStatus(jobId)
  Timeline.GetName()
  Timeline.GetSetting(setting_name)
"""

import os
import sys
import time


# Map aspect ratio (width:height ratio rounded to 2 decimals) to preset name.
PRESET_BY_ASPECT = {
    1.78: "DEVREL_YOUTUBE_1080",   # 1920x1080 = 16:9
    1.00: "DEVREL_LINKEDIN_1080",  # 1080x1080 = 1:1
    0.56: "DEVREL_SHORTS_1080",    # 1080x1920 = 9:16
}


def get_resolve():
    try:
        import DaVinciResolveScript as dvr_script
    except ImportError:
        print(
            "ERROR: Could not import DaVinciResolveScript.\n"
            "  - DaVinci Resolve must be running.\n"
            "  - External scripting must be set to Local.\n"
            "  - RESOLVE_SCRIPT_API, RESOLVE_SCRIPT_LIB, and PYTHONPATH\n"
            "    must be set. See README.md.\n"
        )
        sys.exit(1)

    resolve = dvr_script.scriptapp("Resolve")
    if resolve is None:
        print("ERROR: Could not connect to Resolve. Is a project open?")
        sys.exit(1)
    return resolve


def get_timeline_aspect(timeline):
    """
    Return (width, height, aspect) for a timeline. Aspect is rounded to
    2 decimal places so we can dict-lookup the preset.
    """
    try:
        width = int(timeline.GetSetting("timelineResolutionWidth"))
        height = int(timeline.GetSetting("timelineResolutionHeight"))
    except (TypeError, ValueError):
        return None, None, None
    if height == 0:
        return width, height, None
    return width, height, round(width / height, 2)


def plan_render_jobs(project):
    """
    Walk every timeline in the project and return a list of
    (timeline, preset_name, width, height) tuples that should be rendered.
    """
    plan = []
    count = project.GetTimelineCount()
    if count == 0:
        print("ERROR: Project has no timelines.")
        sys.exit(1)

    for i in range(1, count + 1):
        timeline = project.GetTimelineByIndex(i)
        if timeline is None:
            continue
        name = timeline.GetName()
        width, height, aspect = get_timeline_aspect(timeline)
        if aspect is None:
            print(f"  Skipping '{name}' (could not read resolution)")
            continue
        preset = PRESET_BY_ASPECT.get(aspect)
        if preset is None:
            print(
                f"  Skipping '{name}' ({width}x{height}, aspect {aspect})"
                f" — no preset mapped for this aspect ratio"
            )
            continue
        plan.append((timeline, preset, width, height))
    return plan


def confirm(prompt):
    try:
        answer = input(f"{prompt} [y/N]: ").strip().lower()
    except EOFError:
        return False
    return answer == "y"


def queue_render_jobs(project, plan, output_dir):
    """Add a render job to the queue for each timeline in the plan."""
    queued = []
    for timeline, preset, width, height in plan:
        name = timeline.GetName()
        print(f"\nQueueing: {name} ({width}x{height}) -> preset '{preset}'")

        if not project.SetCurrentTimeline(timeline):
            print(f"  WARNING: Could not set current timeline to '{name}'")
            continue

        if not project.LoadRenderPreset(preset):
            print(
                f"  WARNING: Could not load preset '{preset}'. Does it exist?\n"
                f"           Create it via SKILL.md Phase 3 first."
            )
            continue

        # Override the output location so all renders land in the same folder.
        # The preset's own file-name template (e.g. %timeline_name) is preserved.
        settings = {
            "TargetDir": output_dir,
            # CustomName is optional — only set it if you want to override
            # the preset's filename template:
            # "CustomName": f"{name}_{preset}",
        }
        if not project.SetRenderSettings(settings):
            print(f"  WARNING: Could not set render settings (TargetDir).")
            continue

        job_id = project.AddRenderJob()
        if not job_id:
            print(f"  WARNING: AddRenderJob() returned no id.")
            continue
        print(f"  Queued job id: {job_id}")
        queued.append(job_id)
    return queued


def render_all_and_wait(project):
    """Start rendering and poll until the queue completes."""
    if not project.StartRendering():
        print("ERROR: StartRendering() returned False. Is anything queued?")
        return False

    print("\nRendering started. Polling every 5 seconds...")
    while project.IsRenderingInProgress():
        time.sleep(5)
        print("  ...still rendering")
    print("Rendering complete.")
    return True


def main():
    resolve = get_resolve()
    pm = resolve.GetProjectManager()
    project = pm.GetCurrentProject()
    if project is None:
        print("ERROR: No project is currently open.")
        sys.exit(1)

    print(f"\nProject: {project.GetName()}")
    print("Planning render jobs based on timeline aspect ratios...\n")
    plan = plan_render_jobs(project)
    if not plan:
        print("\nNothing to render. Exiting.")
        return

    print(f"\nPlanned {len(plan)} render jobs:")
    for timeline, preset, width, height in plan:
        print(f"  - {timeline.GetName()} ({width}x{height}) -> {preset}")

    default_dir = os.path.expanduser("~/Movies/DevRel_Renders")
    output_dir = input(
        f"\nOutput directory [default: {default_dir}]: "
    ).strip() or default_dir
    os.makedirs(output_dir, exist_ok=True)

    if not confirm(f"\nProceed to queue {len(plan)} jobs and render now?"):
        print("Cancelled. No jobs queued.")
        return

    queued = queue_render_jobs(project, plan, output_dir)
    if not queued:
        print("\nNo jobs queued successfully. Exiting.")
        return

    if not confirm(f"\n{len(queued)} jobs queued. Start rendering?"):
        print("Jobs are queued in Resolve. You can render them manually from the Deliver page.")
        return

    render_all_and_wait(project)
    print(f"\nOutput files should be in: {output_dir}")


if __name__ == "__main__":
    main()
