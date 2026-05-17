#!/usr/bin/env python3
"""Benchmark a Resolve capstone against the local DeepWiki/book competency gate."""

from __future__ import annotations

import argparse
import datetime as dt
import json
import os
from pathlib import Path

from resolve_common import get_resolve, json_dump, project_by_name, timeline_by_name


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project", default="Codex ChaiWithJai Capstone")
    parser.add_argument("--instagram", default="CAPSTONE Instagram Semantic Cut")
    parser.add_argument("--youtube", default="CAPSTONE YouTube Semantic Cut")
    parser.add_argument("--output-dir", type=Path, default=Path(os.environ.get("RESOLVE_KIT_STATUS_DIR", "resolve_kit/status")))
    return parser.parse_args()


def timeline_state(project, timeline_name: str) -> dict:
    timeline = timeline_by_name(project, timeline_name)
    if not timeline:
        return {"name": timeline_name, "missing": True, "tracks": {"video": {}, "audio": {}}}
    state = {
        "name": timeline.GetName(),
        "start_frame": int(timeline.GetStartFrame()),
        "markers": len(timeline.GetMarkers() or {}),
        "tracks": {"video": {}, "audio": {}, "subtitle": {}},
    }
    for track_type in ("video", "audio", "subtitle"):
        for index in range(1, int(timeline.GetTrackCount(track_type) or 0) + 1):
            items = timeline.GetItemListInTrack(track_type, index) or []
            enabled = None
            if hasattr(timeline, "GetIsTrackEnabled"):
                enabled = timeline.GetIsTrackEnabled(track_type, index)
            state["tracks"][track_type][str(index)] = {
                "name": timeline.GetTrackName(track_type, index),
                "enabled": enabled,
                "clip_count": len(items),
                "sample_items": [item.GetName() for item in items[:8]],
            }
    return state


def main() -> int:
    args = parse_args()
    resolve = get_resolve()
    project = project_by_name(resolve.GetProjectManager(), args.project)
    instagram = timeline_state(project, args.instagram)
    youtube = timeline_state(project, args.youtube)

    checks: list[dict] = []

    def add(domain: str, requirement: str, status: str, evidence: str, fix: str) -> None:
        checks.append(
            {
                "domain": domain,
                "requirement": requirement,
                "status": status,
                "evidence": evidence,
                "fix": fix,
            }
        )

    iv = instagram["tracks"]["video"]
    ia = instagram["tracks"]["audio"]
    sub = instagram["tracks"].get("subtitle", {})

    add(
        "Beginner/Edit",
        "Soundbite-driven A-roll spine with B-roll layered over it",
        "PASS" if iv.get("1", {}).get("clip_count", 0) and iv.get("2", {}).get("clip_count", 0) else "FAIL",
        f"V1={iv.get('1')}; V2={iv.get('2')}",
        "Build V1 semantic spine and cover hard cuts with V2/V3 B-roll.",
    )
    add(
        "Editor/Multicam",
        "Real multicam workflow or preserved multi-angle edit lanes",
        "PARTIAL" if iv.get("3", {}).get("clip_count", 0) else "FAIL",
        f"V3={iv.get('3')}",
        "Create a true multicam source clip or angle-select timeline with all camera ISOs synced.",
    )
    add(
        "Editor/Smart Reframe",
        "Vertical timeline with subject-safe reframing/keyframes",
        "PARTIAL",
        "Vertical render exists, but Resolve timeline lacks per-segment subject-safety/reframe proof.",
        "Add per-segment crop/framing metadata, safe-zone stills, and Resolve transform/keyframe evidence.",
    )
    add(
        "Editor/Subtitles",
        "Proofread captions/subtitles with editable Resolve layer",
        "PASS" if sub and sum(t.get("clip_count", 0) for t in sub.values()) else "PARTIAL",
        f"subtitle_tracks={sub}; V4={iv.get('4')}",
        "Create native subtitle/Text+ captions, or keep PNG plates only as render fallback with editable source.",
    )
    add(
        "Fairlight/Track layout",
        "Dialogue source, processed dialogue, music, SFX/bumpers separated",
        "PASS"
        if ia.get("1", {}).get("clip_count", 0)
        and ia.get("2", {}).get("clip_count", 0)
        and ia.get("3", {}).get("clip_count", 0)
        and ia.get("4", {}).get("clip_count", 0)
        else "PARTIAL",
        f"audio_tracks={ia}",
        "Populate A3 music/ambience and A4 bumper/SFX; keep source/processed dialogue separated.",
    )
    add(
        "Fairlight/Speed sync",
        "Processed audio/video speed matches editable picture",
        "FAIL" if ia.get("2", {}).get("clip_count", 0) else "PARTIAL",
        "A2 uses 1.1x rendered segment audio while V1/V2/V3 source clips remain original speed.",
        "Retimed source clips to 1.1x in Resolve or make processed segment clips the active picture/audio layer.",
    )
    add(
        "Fairlight/Cleanup chain",
        "Clip EQ -> De-Hummer -> Gate -> Noise Reduction -> Leveler order proven",
        "FAIL",
        "No exported Resolve FX chain or stem processing manifest proves the class sequence.",
        "Create processed stems and a manifest with the exact filter chain, or set/capture Fairlight FX state.",
    )
    add(
        "Fairlight/Ducker",
        "Music ducks under dialogue and stays subtle",
        "FAIL" if not ia.get("3", {}).get("clip_count", 0) else "PARTIAL",
        f"A3={ia.get('3')}",
        "Add music/ambience and duck it under dialogue using Ducker, sidechain, or documented automation.",
    )
    add(
        "Color/Primary grade",
        "Normalize -> balance -> enhance order using scopes",
        "FAIL",
        "No named color nodes or scope/primary correction audit.",
        "Create named nodes: 01 Normalize, 02 Balance, 03 Contrast/Sat, 04 Skin/Face, 05 Look.",
    )
    add(
        "Color/Shot matching",
        "Hero clip/stills/continuity matching across cameras",
        "FAIL",
        "No stills, hero clip, PowerGrade, or per-camera match report.",
        "Pick hero camera, save still, match other cameras with waveform and still comparison.",
    )
    add(
        "Fusion/Text+ titles",
        "Captions/lower thirds use Text+ or Fusion template, not flat overlay only",
        "FAIL",
        "V4 PNG plates exist; no Text+ macro/template proof.",
        "Create reusable Text+/Fusion caption/lower-third template and use it in the timeline.",
    )
    add(
        "Fusion/Motion design",
        "Animated title/bumper/macro reusable across projects",
        "FAIL" if not ia.get("4", {}).get("clip_count", 0) else "PARTIAL",
        f"A4={ia.get('4')}",
        "Place outro/bumper assets on dedicated V/A tracks and save reusable macro/template metadata.",
    )
    add(
        "Project/Organization",
        "Bins, timeline names, markers, layered handoff",
        "PASS" if instagram.get("markers", 0) else "FAIL",
        f"markers={instagram.get('markers')}; tracks={instagram.get('tracks')}",
        "Keep layered handoff and HITL markers.",
    )
    add(
        "Delivery/Multi-platform",
        "Instagram and YouTube timelines/renders created",
        "PASS" if instagram.get("markers", 0) and youtube.get("markers", 0) else "FAIL",
        f"instagram_markers={instagram.get('markers')}; youtube_markers={youtube.get('markers')}",
        "Keep separate deliver presets and validation reports.",
    )

    score = round(sum({"PASS": 1, "PARTIAL": 0.5, "FAIL": 0}[c["status"]] for c in checks) / len(checks) * 100, 1)
    payload = {
        "generated_at": dt.datetime.now().isoformat(timespec="seconds"),
        "project": project.GetName(),
        "score": score,
        "checks": checks,
        "timeline_state": {"instagram": instagram, "youtube": youtube},
    }
    args.output_dir.mkdir(parents=True, exist_ok=True)
    stamp = dt.datetime.now().strftime("%Y%m%d-%H%M%S")
    json_path = args.output_dir / f"deepwiki_capstone_benchmark_{stamp}.json"
    md_path = args.output_dir / f"deepwiki_capstone_benchmark_{stamp}.md"
    json_dump(json_path, payload)
    rows = [
        "# DeepWiki Capstone Benchmark",
        "",
        f"Generated: {payload['generated_at']}",
        f"Score: **{score}/100**",
        "",
        "| Domain | Requirement | Status | Evidence | Fix |",
        "|---|---|---|---|---|",
    ]
    for check in checks:
        rows.append(
            f"| {check['domain']} | {check['requirement']} | `{check['status']}` | {check['evidence']} | {check['fix']} |"
        )
    md_path.write_text("\n".join(rows) + "\n")
    print(md_path)
    print(json_path)
    print(f"score={score}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
