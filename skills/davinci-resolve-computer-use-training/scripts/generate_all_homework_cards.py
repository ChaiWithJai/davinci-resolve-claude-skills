#!/usr/bin/env python3
"""Generate homework cards and coverage matrix for every Resolve 20 lesson."""

from __future__ import annotations

import json
import os
from pathlib import Path

from create_homework_card import parse_map, slug


OUT_ROOT = Path(os.environ.get("RESOLVE_TRAINING_RUNS_DIR", "training_runs"))
STATUS_DIR = Path(os.environ.get("RESOLVE_KIT_STATUS_DIR", "resolve_kit/status"))


def main() -> int:
    lessons = parse_map()
    coverage = []
    for item in lessons:
        out_dir = (
            OUT_ROOT
            / slug(item["book"])
            / f"lesson-{item['lesson_number']:02d}-{slug(item['lesson_title'])}"
        )
        out_dir.mkdir(parents=True, exist_ok=True)
        card_path = out_dir / "homework_card.json"
        if not card_path.exists():
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
            card_path.write_text(json.dumps(card, indent=2) + "\n", encoding="utf-8")

        journal_path = out_dir / "journal.md"
        stage_report = out_dir / "resolve_stage_report.json"
        validation_report = out_dir / "validation_report.md"
        status = "not_started"
        if stage_report.exists() or validation_report.exists():
            status = "script_staged_or_validated"
        if journal_path.exists() and "Computer Use timeout" in journal_path.read_text(
            encoding="utf-8", errors="ignore"
        ):
            status = "ui_blocked_script_staged" if status != "not_started" else "ui_blocked"

        coverage.append(
            {
                "book": item["book"],
                "lesson_number": item["lesson_number"],
                "lesson_title": item["lesson_title"],
                "pdf_pages": item["pdf_pages"],
                "homework_goal": item["homework_objective"],
                "run_dir": str(out_dir),
                "card": str(card_path),
                "status": status,
            }
        )

    STATUS_DIR.mkdir(parents=True, exist_ok=True)
    matrix = {
        "total_lessons": len(coverage),
        "status_counts": {
            status: sum(1 for item in coverage if item["status"] == status)
            for status in sorted({item["status"] for item in coverage})
        },
        "coverage": coverage,
    }
    matrix_path = STATUS_DIR / "homework_coverage_matrix.json"
    matrix_path.write_text(json.dumps(matrix, indent=2) + "\n", encoding="utf-8")

    md = ["# Resolve 20 Homework Coverage Matrix", ""]
    md.append(f"Total lessons: {len(coverage)}")
    md.append("")
    md.append("| Book | Lesson | Title | Pages | Status |")
    md.append("| --- | ---: | --- | --- | --- |")
    for item in coverage:
        md.append(
            f"| {item['book']} | {item['lesson_number']} | {item['lesson_title']} | "
            f"{item['pdf_pages']} | {item['status']} |"
        )
    md_path = STATUS_DIR / "homework_coverage_matrix.md"
    md_path.write_text("\n".join(md) + "\n", encoding="utf-8")

    print(matrix_path)
    print(md_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
