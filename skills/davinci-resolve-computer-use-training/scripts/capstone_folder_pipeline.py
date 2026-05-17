#!/usr/bin/env python3
"""Create capstone seed timelines and reports for a local media folder."""

from __future__ import annotations

import argparse
import os
import subprocess
from pathlib import Path

from resolve_common import json_dump


SCRIPT_DIR = Path(__file__).resolve().parent


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("folder", type=Path)
    parser.add_argument("--project", default="Codex ChaiWithJai Capstone")
    parser.add_argument("--status-dir", type=Path, default=Path(os.environ.get("RESOLVE_KIT_STATUS_DIR", "resolve_kit/status")))
    parser.add_argument("--replace", action="store_true")
    return parser.parse_args()


def run(args: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(args, check=True, text=True, capture_output=True)


def main() -> int:
    args = parse_args()
    folder = args.folder.expanduser().resolve()
    slug = folder.name.replace(" ", "_").lower()
    args.status_dir.mkdir(parents=True, exist_ok=True)

    outputs = {}
    for label, max_seconds in [("instagram_9x16_seed", 180), ("youtube_16x9_seed", 720)]:
        timeline = f"{folder.name} - {label}"
        report = args.status_dir / f"{slug}_{label}_stage.json"
        cmd = [
            "python3",
            str(SCRIPT_DIR / "stage_folder_timeline.py"),
            str(folder),
            "--project",
            args.project,
            "--timeline",
            timeline,
            "--max-seconds",
            str(max_seconds),
            "--output",
            str(report),
        ]
        if args.replace:
            cmd.append("--replace")
        run(cmd)

        validation = args.status_dir / f"{slug}_{label}_validation.json"
        run(
            [
                "python3",
                str(SCRIPT_DIR / "validate_timeline.py"),
                "--project",
                args.project,
                "--timeline",
                timeline,
                "--output",
                str(validation),
            ]
        )
        outputs[label] = {"timeline": timeline, "stage_report": str(report), "validation_report": str(validation)}

    checklist = {
        "folder": str(folder),
        "project": args.project,
        "outputs": outputs,
        "next_manual_or_agent_steps": [
            "Replace rough time-sliced beats with transcript-aware semantic sections.",
            "Add V4 burned-in captions using the Netflix-style template.",
            "Apply A1 dialogue cleanup, A3 music ducking, and loudness verification.",
            "Apply color grade and visual safety checks for speaker/whiteboard framing.",
            "Render and evaluate Instagram and YouTube outputs.",
            "Write chaiwithjai.com/workshops markdown from final transcript story.",
        ],
    }
    summary_path = args.status_dir / f"{slug}_capstone_pipeline_summary.json"
    json_dump(summary_path, checklist)
    print(summary_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
