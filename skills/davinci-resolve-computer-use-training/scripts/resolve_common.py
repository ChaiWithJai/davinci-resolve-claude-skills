"""Shared helpers for DaVinci Resolve automation scripts."""

from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Any


SCRIPT_API = Path("/Library/Application Support/Blackmagic Design/DaVinci Resolve/Developer/Scripting")
SCRIPT_LIB = Path("/Applications/DaVinci Resolve/DaVinci Resolve.app/Contents/Libraries/Fusion/fusionscript.so")
MODULES = SCRIPT_API / "Modules"
USER_SCRIPTS = Path.home() / "Library/Application Support/Blackmagic Design/DaVinci Resolve/Fusion/Scripts"
DEFAULT_FPS = 24


def configure_env() -> None:
    os.environ.setdefault("RESOLVE_SCRIPT_API", str(SCRIPT_API))
    os.environ.setdefault("RESOLVE_SCRIPT_LIB", str(SCRIPT_LIB))
    if str(MODULES) not in sys.path:
        sys.path.append(str(MODULES))


def get_resolve():
    configure_env()
    import DaVinciResolveScript as dvr  # type: ignore

    resolve = dvr.scriptapp("Resolve")
    if not resolve:
        raise RuntimeError("Could not connect to DaVinci Resolve. Start Resolve and enable local scripting.")
    return resolve


def project_by_name(project_manager, name: str):
    return project_manager.LoadProject(name) or project_manager.CreateProject(name)


def timeline_by_name(project, name: str):
    for index in range(1, int(project.GetTimelineCount() or 0) + 1):
        timeline = project.GetTimelineByIndex(index)
        if timeline and timeline.GetName() == name:
            return timeline
    return None


def get_or_create_bin(media_pool, parent, name: str):
    for folder in parent.GetSubFolderList():
        if folder.GetName() == name:
            return folder
    return media_pool.AddSubFolder(parent, name)


def seconds(value: float, fps: int = DEFAULT_FPS) -> int:
    return int(round(value * fps))


def json_dump(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")


def ffprobe_duration(path: Path) -> float | None:
    try:
        result = subprocess.run(
            [
                "ffprobe",
                "-v",
                "error",
                "-show_entries",
                "format=duration",
                "-of",
                "default=noprint_wrappers=1:nokey=1",
                str(path),
            ],
            check=True,
            capture_output=True,
            text=True,
        )
        return float(result.stdout.strip())
    except Exception:
        return None


def media_files(folder: Path) -> list[Path]:
    exts = {".mp4", ".mov", ".m4v", ".wav", ".aif", ".aiff", ".mp3", ".m4a"}
    return sorted(
        path
        for path in folder.rglob("*")
        if path.is_file() and not path.name.startswith("._") and path.suffix.lower() in exts
    )


def classify_media(paths: list[Path]) -> dict[str, list[Path]]:
    classified = {"video": [], "audio": [], "other": []}
    for path in paths:
        suffix = path.suffix.lower()
        if suffix in {".mp4", ".mov", ".m4v"}:
            classified["video"].append(path)
        elif suffix in {".wav", ".aif", ".aiff", ".mp3", ".m4a"}:
            classified["audio"].append(path)
        else:
            classified["other"].append(path)
    return classified


def timeline_summary(project, timeline) -> dict[str, Any]:
    summary: dict[str, Any] = {
        "project": project.GetName() if project else None,
        "timeline": timeline.GetName() if timeline else None,
        "start_frame": int(timeline.GetStartFrame()) if timeline else None,
        "markers": len(timeline.GetMarkers() or {}) if timeline else None,
        "tracks": {},
    }
    if not timeline:
        return summary
    for media_type in ("video", "audio"):
        tracks = {}
        for index in range(1, int(timeline.GetTrackCount(media_type) or 0) + 1):
            items = timeline.GetItemListInTrack(media_type, index) or []
            tracks[str(index)] = {
                "name": timeline.GetTrackName(media_type, index),
                "clip_count": len(items),
            }
        summary["tracks"][media_type] = tracks
    return summary
