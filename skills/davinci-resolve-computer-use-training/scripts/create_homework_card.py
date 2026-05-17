#!/usr/bin/env python3
"""Create a DaVinci Resolve Computer Use homework card from the lesson map."""

from __future__ import annotations

import argparse
import json
import os
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
LESSON_MAP = ROOT / "references" / "resolve20-homework-map.md"


def parse_map() -> list[dict]:
    current_book = None
    lessons: list[dict] = []
    for line in LESSON_MAP.read_text(encoding="utf-8").splitlines():
        if line.startswith("## "):
            current_book = line[3:].strip()
            continue
        m = re.match(r"\|\s*(\d+)\s*\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|", line)
        if not m or not current_book or m.group(1) == "---":
            continue
        lessons.append(
            {
                "book": current_book,
                "lesson_number": int(m.group(1)),
                "lesson_title": m.group(2).strip(),
                "pdf_pages": m.group(3).strip(),
                "homework_objective": m.group(4).strip(),
            }
        )
    return lessons


def slug(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--book", required=True)
    parser.add_argument("--lesson", type=int, required=True)
    parser.add_argument("--out-root", default=os.environ.get("RESOLVE_TRAINING_RUNS_DIR", "training_runs"))
    args = parser.parse_args()

    matches = [
        item
        for item in parse_map()
        if item["lesson_number"] == args.lesson and args.book.lower() in item["book"].lower()
    ]
    if not matches:
        raise SystemExit(f"No lesson found for book={args.book!r} lesson={args.lesson}")
    item = matches[0]
    out_dir = Path(args.out_root) / slug(item["book"]) / f"lesson-{item['lesson_number']:02d}-{slug(item['lesson_title'])}"
    out_dir.mkdir(parents=True, exist_ok=True)
    card = {
        **item,
        "target_resolve_pages": [],
        "source_media_needed": "Blackmagic lesson media or local substitute media with equivalent properties.",
        "ui_actions_to_learn": [],
        "automation_candidates": [],
        "expected_artifact": "",
        "validation_checks": [],
        "skill_updates": [],
    }
    (out_dir / "homework_card.json").write_text(json.dumps(card, indent=2) + "\n", encoding="utf-8")
    journal = ROOT / "references" / "computer-use-journal-template.md"
    (out_dir / "journal.md").write_text(journal.read_text(encoding="utf-8"), encoding="utf-8")
    print(out_dir)


if __name__ == "__main__":
    main()
