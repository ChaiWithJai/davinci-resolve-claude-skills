#!/usr/bin/env python3
"""Validate the current or named Resolve timeline for editable handoff basics."""

from __future__ import annotations

import argparse
from pathlib import Path

from resolve_common import get_resolve, json_dump, timeline_by_name, timeline_summary


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project", default=None)
    parser.add_argument("--timeline", default=None)
    parser.add_argument("--output", type=Path, default=None)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    resolve = get_resolve()
    project_manager = resolve.GetProjectManager()
    project = project_manager.LoadProject(args.project) if args.project else project_manager.GetCurrentProject()
    if not project:
        raise RuntimeError("No Resolve project is open or loadable.")

    timeline = timeline_by_name(project, args.timeline) if args.timeline else project.GetCurrentTimeline()
    if not timeline:
        raise RuntimeError("No Resolve timeline is current or loadable.")

    summary = timeline_summary(project, timeline)
    issues = []
    video_tracks = summary["tracks"].get("video", {})
    audio_tracks = summary["tracks"].get("audio", {})

    if int(summary["start_frame"]) != int(timeline.GetStartFrame()):
        issues.append("timeline start frame readback mismatch")
    if not video_tracks:
        issues.append("no video tracks")
    if not audio_tracks:
        issues.append("no audio tracks")
    if sum(track["clip_count"] for track in video_tracks.values()) == 0:
        issues.append("no video clips")
    if sum(track["clip_count"] for track in audio_tracks.values()) == 0:
        issues.append("no audio clips")
    if int(summary["markers"] or 0) == 0:
        issues.append("no markers")
    if len(video_tracks) < 2:
        issues.append("less than two video tracks; likely weak B-roll/layer handoff")

    summary["issues"] = issues
    summary["pass"] = not issues

    if args.output:
        json_dump(args.output, summary)
    print("PASS" if summary["pass"] else "FAIL")
    print(summary)
    return 0 if summary["pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
