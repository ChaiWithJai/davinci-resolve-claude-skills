#!/usr/bin/env python3
"""Create a repeatable B-roll sourcing plan for speaker-led social edits."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


DEFAULT_CHAI_INTENTS = [
    {
        "beat": "event_location",
        "spoken_context": "June 7 / Jersey City / K-Vibe Studios",
        "native_targets": ["venue exterior", "studio sign", "room establishing shot", "mic/table detail"],
        "coverr_queries": ["Jersey City", "studio podcast", "community event"],
        "shot_types": ["wide", "environment", "insert/detail"],
        "reason": "Establish where the workshop happens and make the event feel concrete.",
    },
    {
        "beat": "audience_fit",
        "spoken_context": "personal brands, solo operators, regional businesses",
        "native_targets": ["people at table", "small business owner", "laptop close-up", "notes/forms"],
        "coverr_queries": ["small business owner", "entrepreneur workshop", "coffee meeting"],
        "shot_types": ["medium", "human moment", "insert/detail"],
        "reason": "Give warm traffic a visual mirror for who the workshop is for.",
    },
    {
        "beat": "ai_workflow_gap",
        "spoken_context": "AI falls short on ads, emails, videos, and business tasks",
        "native_targets": ["laptop screen", "keyboard", "phone", "hands typing"],
        "coverr_queries": ["laptop work", "marketing campaign", "AI technology"],
        "shot_types": ["close-up", "screen/product", "insert/detail"],
        "reason": "Visualize the pain point without covering the speaker's trust-building moments.",
    },
    {
        "beat": "business_model_canvas",
        "spoken_context": "Business Model Canvas / business plan in five minutes",
        "native_targets": ["whiteboard", "hand writing", "canvas/framework", "marker close-up"],
        "coverr_queries": ["business planning", "whiteboard", "team collaboration"],
        "shot_types": ["medium", "close-up", "insert/detail"],
        "reason": "Show the actual framework or closest visual evidence for the required pre-work.",
    },
    {
        "beat": "skill_share_room",
        "spoken_context": "small intimate room of entrepreneurs at different stages",
        "native_targets": ["chairs/table", "small group", "discussion", "workshop room"],
        "coverr_queries": ["workshop collaboration", "community event", "entrepreneur meeting"],
        "shot_types": ["wide", "medium", "human moment"],
        "reason": "Make the room feel intimate and worth joining.",
    },
    {
        "beat": "cta",
        "spoken_context": "apply at chaiwithjai.com/workshops / tell a friend",
        "native_targets": ["website page", "form", "phone signup", "logo/brand"],
        "coverr_queries": ["online form", "laptop signup", "business website"],
        "shot_types": ["screen/product", "insert/detail"],
        "reason": "Support the action step without distracting from the final spoken CTA.",
    },
]


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("project_folder")
    parser.add_argument("--out", required=True, help="Path to broll_plan.json")
    parser.add_argument("--profile", default="chai_workshops", help="Preset profile name.")
    args = parser.parse_args()

    project = Path(args.project_folder).expanduser().resolve()
    out = Path(args.out).expanduser().resolve()
    out.parent.mkdir(parents=True, exist_ok=True)

    plan = {
        "project_folder": str(project),
        "profile": args.profile,
        "source_priority": [
            "native project footage that proves the exact claim",
            "user-provided brand/workshop/site assets",
            "Coverr free stock footage with recorded attribution/license metadata",
        ],
        "coverr_policy": {
            "source": "https://coverr.co/",
            "api_docs": "https://coverr.co/api",
            "license_note": "Record Coverr source URL and attribution/license terms per asset before use.",
            "reject_if": [
                "asset is generic atmosphere without proving a spoken claim",
                "asset obscures the speaker during a trust-building beat",
                "asset contains unsafe trademark/brand/signage ambiguity",
                "asset feels unrelated to business education, workshops, AI, planning, or community",
            ],
        },
        "placements": DEFAULT_CHAI_INTENTS,
        "asset_manifest_template": [
            {
                "beat": item["beat"],
                "query": "",
                "source": "native|coverr|user_asset",
                "source_url": "",
                "license_or_attribution": "",
                "local_path": "",
                "selected_in": "",
                "selected_out": "",
                "placement_time": "",
                "duration_seconds": "",
                "used": False,
                "reason": item["reason"],
                "rejection_reason": "",
            }
            for item in DEFAULT_CHAI_INTENTS
        ],
    }

    out.write_text(json.dumps(plan, indent=2) + "\n")
    print(json.dumps(plan, indent=2))


if __name__ == "__main__":
    main()
