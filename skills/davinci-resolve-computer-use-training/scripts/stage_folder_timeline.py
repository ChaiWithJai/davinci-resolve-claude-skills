#!/usr/bin/env python3
"""Stage a local media folder into an editable Resolve timeline."""

from __future__ import annotations

import argparse
from pathlib import Path

from resolve_common import (
    DEFAULT_FPS,
    classify_media,
    ffprobe_duration,
    get_or_create_bin,
    get_resolve,
    json_dump,
    media_files,
    project_by_name,
    seconds,
    timeline_by_name,
    timeline_summary,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("folder", type=Path)
    parser.add_argument("--project", default="Codex Resolve Autocut")
    parser.add_argument("--timeline", default=None)
    parser.add_argument("--output", type=Path, default=None)
    parser.add_argument("--fps", type=int, default=DEFAULT_FPS)
    parser.add_argument("--max-seconds", type=float, default=180.0)
    parser.add_argument("--replace", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    folder = args.folder.expanduser().resolve()
    if not folder.exists():
        raise FileNotFoundError(folder)

    timeline_name = args.timeline or f"{folder.name} - Layered Rough Cut"
    output = args.output or folder / "work" / "resolve_stage_report.json"

    paths = media_files(folder)
    classified = classify_media(paths)
    if not classified["video"]:
        raise RuntimeError(f"No video files found in {folder}")

    resolve = get_resolve()
    project_manager = resolve.GetProjectManager()
    project = project_by_name(project_manager, args.project)
    if not project:
        raise RuntimeError(f"Could not load/create project {args.project!r}")

    project.SetSetting("timelineFrameRate", str(args.fps))
    media_storage = resolve.GetMediaStorage()
    media_pool = project.GetMediaPool()
    root = media_pool.GetRootFolder()
    source_bin = get_or_create_bin(media_pool, root, f"{folder.name} Source")
    media_pool.SetCurrentFolder(source_bin)

    imported = {}
    existing = {item.GetName(): item for item in source_bin.GetClipList()}
    for path in classified["video"] + classified["audio"]:
        item = existing.get(path.name)
        if not item:
            added = media_storage.AddItemListToMediaPool([str(path)])
            if not added:
                continue
            item = added[0]
        imported[str(path)] = item

    old = timeline_by_name(project, timeline_name)
    if old and args.replace:
        media_pool.DeleteTimelines([old])
        old = None

    timeline = old or media_pool.CreateEmptyTimeline(timeline_name)
    if not timeline:
        raise RuntimeError(f"Could not create timeline {timeline_name!r}")
    project.SetCurrentTimeline(timeline)
    resolve.OpenPage("edit")

    while int(timeline.GetTrackCount("video") or 0) < 4:
        timeline.AddTrack("video")
    while int(timeline.GetTrackCount("audio") or 0) < 4:
        timeline.AddTrack("audio")

    track_names = [
        ("video", 1, "V1 Primary A-roll"),
        ("video", 2, "V2 B-roll / Whiteboard / Cutaways"),
        ("video", 3, "V3 Alternate Angle"),
        ("video", 4, "V4 Captions / Titles / Graphics"),
        ("audio", 1, "A1 Clean Dialogue"),
        ("audio", 2, "A2 Scratch / Camera Audio"),
        ("audio", 3, "A3 Music / Ambience"),
        ("audio", 4, "A4 SFX / Bumpers"),
    ]
    for media_type, index, name in track_names:
        timeline.SetTrackName(media_type, index, name)

    if old and not args.replace:
        report = timeline_summary(project, timeline)
        report["status"] = "existing timeline left unchanged; pass --replace to rebuild"
        json_dump(output, report)
        print(output)
        return 0

    videos = classified["video"]
    audios = classified["audio"]
    primary_video = next((p for p in videos if "cam 2" in p.name.lower()), videos[0])
    broll_video = next((p for p in videos if "cam 1" in p.name.lower()), videos[min(1, len(videos) - 1)])
    alt_video = next((p for p in videos if "cam 3" in p.name.lower()), videos[min(2, len(videos) - 1)])
    clean_audio = next((p for p in audios if "mic 1" in p.name.lower()), audios[0] if audios else None)

    duration = ffprobe_duration(primary_video) or args.max_seconds
    total = min(duration, args.max_seconds)
    beat_count = 6
    beat_len = max(8.0, total / beat_count)
    start_frame = int(timeline.GetStartFrame())
    record = 0
    beats = []

    for idx in range(beat_count):
        src_in = idx * beat_len
        src_out = min(src_in + beat_len - 1.0, duration)
        if src_out <= src_in:
            break
        duration_frames = seconds(src_out - src_in, args.fps)
        rec = start_frame + record
        clip_infos = [
            {
                "mediaPoolItem": imported[str(primary_video)],
                "startFrame": seconds(src_in, args.fps),
                "endFrame": seconds(src_out, args.fps),
                "recordFrame": rec,
                "mediaType": 1,
                "trackIndex": 1,
            }
        ]
        if clean_audio:
            clip_infos.append(
                {
                    "mediaPoolItem": imported[str(clean_audio)],
                    "startFrame": seconds(src_in, args.fps),
                    "endFrame": seconds(src_out, args.fps),
                    "recordFrame": rec,
                    "mediaType": 2,
                    "trackIndex": 1,
                }
            )
        media_pool.AppendToTimeline(clip_infos)

        overlay = broll_video if idx % 2 == 0 else alt_video
        overlay_track = 2 if idx % 2 == 0 else 3
        overlay_offset = seconds(4.0, args.fps)
        overlay_len = min(seconds(8.0, args.fps), max(0, duration_frames - overlay_offset))
        if overlay_len:
            media_pool.AppendToTimeline(
                [
                    {
                        "mediaPoolItem": imported[str(overlay)],
                        "startFrame": seconds(src_in + 4.0, args.fps),
                        "endFrame": seconds(src_in + 4.0, args.fps) + overlay_len,
                        "recordFrame": rec + overlay_offset,
                        "mediaType": 1,
                        "trackIndex": overlay_track,
                    }
                ]
            )

        marker_name = f"{idx + 1}. Story beat {idx + 1}"
        note = "Rough-cut beat. Replace with transcript-confirmed semantic section during hillclimb."
        timeline.AddMarker(rec, "Blue", marker_name, note, duration_frames, f"story_beat_{idx + 1}")
        beats.append({"name": marker_name, "source_seconds": [src_in, src_out], "record_frame": rec})
        record += duration_frames + seconds(0.5, args.fps)

    project_manager.SaveProject()

    report = timeline_summary(project, timeline)
    report.update(
        {
            "status": "staged",
            "folder": str(folder),
            "primary_video": str(primary_video),
            "broll_video": str(broll_video),
            "alt_video": str(alt_video),
            "clean_audio": str(clean_audio) if clean_audio else None,
            "beats": beats,
        }
    )
    json_dump(output, report)
    print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
