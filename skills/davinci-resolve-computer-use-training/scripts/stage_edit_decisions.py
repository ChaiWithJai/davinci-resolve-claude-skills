#!/usr/bin/env python3
"""Stage transcript/story edit decisions into layered Resolve timelines."""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path

from resolve_common import (
    DEFAULT_FPS,
    get_or_create_bin,
    get_resolve,
    json_dump,
    project_by_name,
    seconds,
    timeline_by_name,
    timeline_summary,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("decisions", type=Path)
    parser.add_argument("--project", default="Codex ChaiWithJai Capstone")
    parser.add_argument("--audio", type=Path, default=None)
    parser.add_argument("--output-dir", type=Path, default=Path(os.environ.get("RESOLVE_KIT_STATUS_DIR", "resolve_kit/status")))
    parser.add_argument("--replace", action="store_true")
    return parser.parse_args()


def ensure_tracks(timeline) -> None:
    while int(timeline.GetTrackCount("video") or 0) < 5:
        timeline.AddTrack("video")
    while int(timeline.GetTrackCount("audio") or 0) < 4:
        timeline.AddTrack("audio")
    names = [
        ("video", 1, "V1 Semantic A-roll"),
        ("video", 2, "V2 B-roll / Whiteboard"),
        ("video", 3, "V3 Alternate Angle"),
        ("video", 4, "V4 Captions / Titles"),
        ("video", 5, "V5 Rendered Segment Reference"),
        ("audio", 1, "A1 Dialogue Source"),
        ("audio", 2, "A2 Dialogue Processed"),
        ("audio", 3, "A3 Music / Ambience"),
        ("audio", 4, "A4 SFX / Bumpers"),
    ]
    for media_type, index, name in names:
        timeline.SetTrackName(media_type, index, name)


def stage_timeline(project, media_pool, media_storage, bin_folder, name: str, segments: list[dict], audio_path: Path | None, replace: bool):
    old = timeline_by_name(project, name)
    if old and replace:
        media_pool.DeleteTimelines([old])
        old = None
    timeline = old or media_pool.CreateEmptyTimeline(name)
    project.SetCurrentTimeline(timeline)
    ensure_tracks(timeline)

    if old and not replace:
        return timeline_summary(project, timeline)

    imported = {item.GetName(): item for item in bin_folder.GetClipList()}

    def import_item(path: Path):
        item = imported.get(path.name)
        if not item:
            added = media_storage.AddItemListToMediaPool([str(path)])
            if not added:
                raise RuntimeError(f"Could not import {path}")
            item = added[0]
            imported[path.name] = item
        return item

    start_frame = int(timeline.GetStartFrame())
    record = 0
    staged = []
    audio_item = import_item(audio_path) if audio_path else None

    for idx, segment in enumerate(segments, start=1):
        src_video = Path(segment["video"])
        video_item = import_item(src_video)
        src_in = float(segment["start"])
        src_out = float(segment["end"])
        duration_frames = seconds(src_out - src_in, DEFAULT_FPS)
        rec = start_frame + record
        mode = segment.get("mode", "")
        track = 1
        if "board" in mode:
            track = 2
        elif "wide" in mode:
            track = 3

        media_pool.AppendToTimeline(
            [
                {
                    "mediaPoolItem": video_item,
                    "startFrame": seconds(src_in, DEFAULT_FPS),
                    "endFrame": seconds(src_out, DEFAULT_FPS),
                    "recordFrame": rec,
                    "mediaType": 1,
                    "trackIndex": track,
                }
            ]
        )
        if audio_item:
            media_pool.AppendToTimeline(
                [
                    {
                        "mediaPoolItem": audio_item,
                        "startFrame": seconds(src_in, DEFAULT_FPS),
                        "endFrame": seconds(src_out, DEFAULT_FPS),
                        "recordFrame": rec,
                        "mediaType": 2,
                        "trackIndex": 1,
                    }
                ]
            )
        processed = segment.get("processed_video")
        if processed and Path(processed).exists():
            ref_item = import_item(Path(processed))
            media_pool.AppendToTimeline(
                [
                    {
                        "mediaPoolItem": ref_item,
                        "startFrame": 0,
                        "endFrame": seconds(float(segment.get("output_duration_seconds", src_out - src_in)), DEFAULT_FPS),
                        "recordFrame": rec,
                        "mediaType": 1,
                        "trackIndex": 5,
                    }
                ]
            )
            media_pool.AppendToTimeline(
                [
                    {
                        "mediaPoolItem": ref_item,
                        "startFrame": 0,
                        "endFrame": seconds(float(segment.get("output_duration_seconds", src_out - src_in)), DEFAULT_FPS),
                        "recordFrame": rec,
                        "mediaType": 2,
                        "trackIndex": 2,
                    }
                ]
            )

        caption_image = segment.get("caption_image")
        if caption_image and Path(caption_image).exists():
            caption_item = import_item(Path(caption_image))
            media_pool.AppendToTimeline(
                [
                    {
                        "mediaPoolItem": caption_item,
                        "startFrame": 0,
                        "endFrame": duration_frames,
                        "recordFrame": rec,
                        "mediaType": 1,
                        "trackIndex": 4,
                    }
                ]
            )

        label = segment.get("label") or segment.get("name") or f"Segment {idx}"
        note = f"{segment.get('name', '')} | {segment.get('reason', '')}".strip()
        timeline.AddMarker(rec, "Blue", f"{idx}. {label}", note, duration_frames, f"semantic_{idx}")
        staged.append(
            {
                "index": idx,
                "label": label,
                "source": str(src_video),
                "source_seconds": [src_in, src_out],
                "record_frame": rec,
                "track": track,
                "caption_text": segment.get("caption_text"),
                "caption_image": caption_image,
            }
        )
        record += duration_frames + seconds(0.25, DEFAULT_FPS)

    timeline.SetTrackEnable("audio", 1, False)
    timeline.SetTrackEnable("audio", 2, True)
    timeline.SetTrackEnable("video", 5, False)

    report = timeline_summary(project, timeline)
    report["segments"] = staged
    return report


def main() -> int:
    args = parse_args()
    data = json.loads(args.decisions.read_text())
    audio_path = args.audio or Path(data.get("audio_source", ""))
    if not audio_path.exists():
        audio_path = None

    resolve = get_resolve()
    project_manager = resolve.GetProjectManager()
    project = project_by_name(project_manager, args.project)
    media_pool = project.GetMediaPool()
    media_storage = resolve.GetMediaStorage()
    root = media_pool.GetRootFolder()
    bin_folder = get_or_create_bin(media_pool, root, "Capstone Semantic Sources")
    media_pool.SetCurrentFolder(bin_folder)

    reports = {}
    for key, timeline_name, segments in [
        ("reel", "CAPSTONE Instagram Semantic Cut", data["reel_segments"]),
        ("youtube", "CAPSTONE YouTube Semantic Cut", data["youtube_segments"]),
    ]:
        reports[key] = stage_timeline(
            project,
            media_pool,
            media_storage,
            bin_folder,
            timeline_name,
            segments,
            audio_path,
            args.replace,
        )

    resolve.OpenPage("edit")
    project_manager.SaveProject()
    args.output_dir.mkdir(parents=True, exist_ok=True)
    out = args.output_dir / "kvibe3_semantic_capstone_resolve_report.json"
    json_dump(out, {"project": args.project, "reports": reports})
    print(out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
