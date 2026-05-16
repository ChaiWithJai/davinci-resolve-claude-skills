#!/usr/bin/env python3
"""
auto_silence_cut.py — Inspect the active DaVinci Resolve timeline and print
clip-level start/end timecodes so you can spot silent gaps and long clips
that may need trimming.

This script is intentionally read-only. It does NOT delete clips. Use it to
audit a timeline before you do destructive ripple-deletes by hand.

Requirements:
  - DaVinci Resolve 20 (free or Studio) running, with a project open
  - External scripting enabled (Preferences > System > General > External
    scripting using = Local)
  - Python 3.9+

Run from terminal (macOS example):
  export RESOLVE_SCRIPT_API="/Library/Application Support/Blackmagic Design/DaVinci Resolve/Developer/Scripting"
  export RESOLVE_SCRIPT_LIB="/Applications/DaVinci Resolve/DaVinci Resolve.app/Contents/Libraries/Fusion/fusionscript.so"
  export PYTHONPATH="$PYTHONPATH:$RESOLVE_SCRIPT_API/Modules/"
  python3 auto_silence_cut.py

Or from inside Resolve:
  Workspace > Console > Py3, then File > Open and select this script.

API surface used (all documented in the Reference Manual / Developer/Scripting/README.txt):
  Resolve.GetProjectManager()
  ProjectManager.GetCurrentProject()
  Project.GetCurrentTimeline()
  Timeline.GetItemListInTrack(trackType, trackIndex)
  TimelineItem.GetName()
  TimelineItem.GetStart()
  TimelineItem.GetEnd()
  TimelineItem.GetDuration()
  Timeline.GetTrackCount(trackType)
  Project.GetSetting("timelineFrameRate")
"""

import sys


def get_resolve():
    """Attach to the running Resolve instance via the scripting bridge."""
    try:
        import DaVinciResolveScript as dvr_script
    except ImportError:
        print(
            "ERROR: Could not import DaVinciResolveScript.\n"
            "  - Make sure DaVinci Resolve is running.\n"
            "  - Make sure External scripting is set to Local in\n"
            "    Preferences > System > General.\n"
            "  - Make sure RESOLVE_SCRIPT_API, RESOLVE_SCRIPT_LIB, and\n"
            "    PYTHONPATH environment variables are set.\n"
            "  - See README.md in the repo root for the exact paths.\n"
        )
        sys.exit(1)

    resolve = dvr_script.scriptapp("Resolve")
    if resolve is None:
        print("ERROR: Could not connect to Resolve. Is a project open?")
        sys.exit(1)
    return resolve


def frames_to_timecode(frames, fps):
    """Convert frame count to HH:MM:SS:FF timecode string."""
    fps_int = int(round(fps))
    if fps_int < 1:
        fps_int = 24
    total_seconds = frames // fps_int
    frame_remainder = frames % fps_int
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    seconds = total_seconds % 60
    return f"{hours:02d}:{minutes:02d}:{seconds:02d}:{frame_remainder:02d}"


def audit_timeline():
    resolve = get_resolve()
    pm = resolve.GetProjectManager()
    project = pm.GetCurrentProject()
    if project is None:
        print("ERROR: No project is currently open.")
        sys.exit(1)

    timeline = project.GetCurrentTimeline()
    if timeline is None:
        print("ERROR: No timeline is currently active.")
        sys.exit(1)

    timeline_name = timeline.GetName()
    fps_str = project.GetSetting("timelineFrameRate")
    try:
        fps = float(fps_str)
    except (TypeError, ValueError):
        fps = 24.0

    print(f"\nTimeline: {timeline_name}  ({fps} fps)\n")
    print(f"{'#':>3}  {'Track':>5}  {'Clip':<40}  {'Start TC':>12}  {'End TC':>12}  {'Duration':>10}")
    print("-" * 100)

    audio_track_count = timeline.GetTrackCount("audio")
    if audio_track_count == 0:
        print("WARNING: Timeline has no audio tracks. Are you on the right timeline?")
        return

    silence_warnings = []

    for track_index in range(1, audio_track_count + 1):
        clips = timeline.GetItemListInTrack("audio", track_index)
        if not clips:
            continue
        # Sort by start frame so the report is timecode-ordered.
        clips_sorted = sorted(clips, key=lambda c: c.GetStart())

        last_end = None
        for i, clip in enumerate(clips_sorted, start=1):
            name = clip.GetName() or "(unnamed)"
            start = clip.GetStart()
            end = clip.GetEnd()
            duration = clip.GetDuration()

            print(
                f"{i:>3}  A{track_index:>3}  {name[:40]:<40}"
                f"  {frames_to_timecode(start, fps):>12}"
                f"  {frames_to_timecode(end, fps):>12}"
                f"  {frames_to_timecode(duration, fps):>10}"
            )

            # Flag gaps longer than 2 seconds between consecutive clips.
            if last_end is not None:
                gap_frames = start - last_end
                if gap_frames > fps * 2:
                    silence_warnings.append(
                        (track_index, last_end, start, gap_frames)
                    )
            last_end = end

    if silence_warnings:
        print(
            f"\nFound {len(silence_warnings)} silent gaps longer than 2 seconds:\n"
        )
        for track, gap_start, gap_end, gap_frames in silence_warnings:
            print(
                f"  A{track}  {frames_to_timecode(gap_start, fps)}"
                f"  -> {frames_to_timecode(gap_end, fps)}"
                f"  ({frames_to_timecode(gap_frames, fps)} duration)"
            )
        print(
            "\nTo remove these, jump to each timecode in the timeline, mark"
            " In/Out around the silent range, and press Shift-Delete to"
            " ripple-delete. Or use the AI Transcription's Remove Silent"
            " Portions feature on the entire timeline at once."
        )
    else:
        print("\nNo silent gaps longer than 2 seconds detected on audio tracks.")

    print()


if __name__ == "__main__":
    audit_timeline()
