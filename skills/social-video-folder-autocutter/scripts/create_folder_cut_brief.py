#!/usr/bin/env python3
"""Create a repeatable folder-to-social-cut brief from media and audio audits."""

from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path


DAVINCI_SKILL = Path(__file__).resolve().parents[2] / "davinci-resolve-social-editor"


def run_json(cmd: list[str]) -> dict:
    proc = subprocess.run(cmd, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
    if proc.returncode not in (0, 2):
        raise RuntimeError(proc.stderr.strip() or proc.stdout.strip())
    stdout = proc.stdout.strip()
    try:
        return json.loads(stdout)
    except json.JSONDecodeError:
        path = Path(stdout)
        if path.exists():
            return json.loads(path.read_text())
        raise


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("project_folder")
    parser.add_argument("--out", required=True)
    parser.add_argument(
        "--audio-path",
        action="append",
        help="Audio file/dir to audit. Defaults to source-like folders, not generated exports.",
    )
    parser.add_argument("--full-audio-audit", action="store_true", help="Scan complete audio files instead of a fast intake sample.")
    args = parser.parse_args()

    project = Path(args.project_folder).expanduser().resolve()
    out = Path(args.out).expanduser().resolve()
    out.parent.mkdir(parents=True, exist_ok=True)

    manifest_path = out.parent / "media_manifest.json"
    audio_path = out.parent / "audio_quality_audit.json"

    manifest = run_json([
        "python3",
        str(DAVINCI_SKILL / "scripts" / "probe_media.py"),
        str(project),
        "--out",
        str(manifest_path),
    ])
    default_audio_paths = []
    for rel in ("Audio Source Files", "Video ISO Files"):
        candidate = project / rel
        if candidate.exists():
            default_audio_paths.append(str(candidate))
    clean_stems = sorted((project / "work").glob("**/*dialogue*.wav")) if (project / "work").exists() else []
    default_audio_paths.extend(str(path) for path in clean_stems)
    audio_inputs = args.audio_path or default_audio_paths or [str(project)]

    audio = run_json([
        "python3",
        str(DAVINCI_SKILL / "scripts" / "audio_quality_audit.py"),
        *audio_inputs,
        "--out",
        str(audio_path),
        *(["--sample-seconds", "45"] if not args.full_audio_audit else []),
    ])

    brief = {
        "project_folder": str(project),
        "profiles": {
            "vertical_social": {
                "aspect_ratio": "9:16",
                "resolution": "1080x1920",
                "duration_target_seconds": [45, 180],
                "talking_speed": 1.1,
                "requires_burned_or_visible_captions": True,
            },
            "horizontal_long_form": {
                "aspect_ratio": "16:9",
                "resolution": "1920x1080",
                "duration_target_seconds": [180, 420],
                "talking_speed": 1.0,
                "requires_layered_resolve_timeline": True,
            },
        },
        "artifacts": {
            "media_manifest": str(manifest_path),
            "audio_quality_audit": str(audio_path),
        },
        "best_audio_candidate": audio.get("best_candidate"),
        "media_summary": {
            "video_count": sum(1 for item in manifest.get("files", []) if "video" in item.get("kind", "")),
            "audio_count": sum(1 for item in manifest.get("files", []) if "audio" in item.get("kind", "")),
            "image_count": sum(1 for item in manifest.get("files", []) if item.get("kind") == "brand_or_image"),
            "resolve_project_count": sum(1 for item in manifest.get("files", []) if item.get("kind") == "resolve_project"),
        },
        "next_steps": [
            "Write story_plan.md with hook/body/recap before cutting.",
            "Create edit_decisions.csv with semantic beats and cut rationale.",
            "Create broll_plan.json and broll_asset_manifest.json before placing B-roll.",
            "Source native B-roll first, then Coverr for missing visual evidence with license/source metadata.",
            "Generate low-res critic proxy before final Resolve build.",
            "Build layered Resolve timeline and run resolve_timeline_audit.py.",
            "Generate spoken Netflix-style captions from word-level timing, then inspect phone-safe stills.",
        ],
        "broll_defaults": {
            "source_priority": ["native project footage", "user assets", "Coverr"],
            "coverr_queries": [
                "small business owner",
                "entrepreneur workshop",
                "business planning",
                "whiteboard",
                "team collaboration",
                "laptop work",
                "coffee meeting",
                "Jersey City",
                "AI technology",
                "coding",
                "marketing campaign",
                "community event",
            ],
            "required_artifacts": [
                "broll_plan.json",
                "broll_asset_manifest.json",
            ],
        },
    }
    out.write_text(json.dumps(brief, indent=2) + "\n")
    print(json.dumps(brief, indent=2))


if __name__ == "__main__":
    main()
