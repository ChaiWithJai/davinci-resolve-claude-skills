#!/usr/bin/env python3
"""Score the current capstone/proof bundle against the Resolve 20 workbook map."""

from __future__ import annotations

import json
import os
import re
from datetime import datetime
from pathlib import Path

SKILL_ROOT = Path(__file__).resolve().parents[1]
ROOT = Path(os.environ.get("CAPSTONE_MEDIA_ROOT", ".")).expanduser().resolve()
TRAINING = Path(os.environ.get("RESOLVE_KIT_STATUS_DIR", "resolve_kit/status"))
MAP = Path(os.environ.get("RESOLVE_HOMEWORK_MAP", str(SKILL_ROOT / "references" / "resolve20-homework-map.md")))
V1 = ROOT / "output" / "workbook_proof_v1" / "workbook_proof_v1_report.json"
V2 = ROOT / "output" / "workbook_proof_v2" / "workbook_proof_v2_report.json"
VERIFY = ROOT / "output" / "deepwiki_repair_v1_limited_verify" / "verification_report.json"
REEL = ROOT / "exports" / "kvibe3_instagram_deepwiki_repair_v1_limited.mp4"
YOUTUBE = ROOT / "exports" / "kvibe3_ai_world_cup_youtube_16x9_v1.mp4"
SKILL = Path(os.environ.get("RESOLVE_TRAINING_SKILL_MD", str(SKILL_ROOT / "SKILL.md")))


def load_json(path: Path) -> dict:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def parse_lessons() -> list[dict]:
    lessons = []
    book = None
    for line in MAP.read_text(encoding="utf-8").splitlines():
        if line.startswith("## "):
            book = line[3:].strip()
        m = re.match(r"\|\s*(\d+)\s*\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|", line)
        if not m or not book or m.group(1) == "---":
            continue
        lessons.append({
            "book": book,
            "lesson": int(m.group(1)),
            "title": m.group(2).strip(),
            "pages": m.group(3).strip(),
            "goal": m.group(4).strip(),
        })
    return lessons


def evidence_flags() -> dict[str, bool]:
    v1 = load_json(V1)
    v2 = load_json(V2)
    verify = load_json(VERIFY)
    fair = v2.get("timelines", {}).get("fairlight", {})
    fusion = v2.get("timelines", {}).get("fusion", {})
    color = v2.get("timelines", {}).get("color_delivery", {})
    exports = v2.get("color_delivery", {}).get("exports", {})
    alt_xml = ROOT / "output" / "workbook_proof_v2" / "color_delivery_v2_EXPORT_FCPXML_1_10.xml"
    return {
        "capstone_reel": REEL.exists(),
        "youtube_cut": YOUTUBE.exists(),
        "social_loudness_verified": bool(verify) and not verify.get("warnings"),
        "editing_layered": (ROOT / "output" / "workbook_proof_v1" / "editing_validation.json").exists(),
        "subtitles_netflix": any(op.get("op", "").startswith("CreateSubtitlesFromAudio") and op.get("ok") for op in v1.get("operations", []))
        or bool(fair.get("subtitle_tracks")),
        "take_selector": any(op.get("op") == "AddTake alternate camera to first edit item" and op.get("ok") for op in v1.get("operations", [])),
        "color_group_still": any(op.get("op") == "AddColorGroup" and op.get("ok") for op in v1.get("operations", []))
        and any(op.get("op") == "ExportStill" and op.get("ok") for op in v1.get("operations", [])),
        "color_cdl_versions": color.get("markers", 0) >= 4 and v2.get("color_delivery", {}).get("still_ok", False),
        "conform_exports": (exports.get("fcpxml", {}).get("ok") or alt_xml.exists()) and exports.get("edl_cdl", {}).get("ok"),
        "delivery_exports": exports.get("drt", {}).get("ok") and exports.get("aaf", {}).get("ok") and exports.get("csv", {}).get("ok"),
        "fairlight_lanes": fair.get("markers", 0) >= 5 and len(fair.get("audio_tracks", {})) >= 8,
        "fairlight_bus_assets": all((Path(p).exists() for p in v2.get("audio_assets", {}).values())),
        "fusion_nodes": fusion.get("markers", 0) >= 4 and (ROOT / "output" / "workbook_proof_v2" / "fusion_v2_2d_3d_nodes.setting").exists(),
        "fusion_v1_export": any(op.get("op") == "ExportFusionComp" and op.get("ok") for op in v1.get("operations", [])),
        "skill_updated": "Source Workbook Benchmark Gate" in SKILL.read_text(encoding="utf-8"),
        "project_exports": (ROOT / "output" / "resolve_exports" / "kvibe3_workbook_proof_v2_20260516.drp").exists(),
    }


def status_for(lesson: dict, f: dict[str, bool]) -> tuple[str, list[str]]:
    book, n, title = lesson["book"], lesson["lesson"], lesson["title"]
    reason = []
    status = "FAIL"
    if book == "Beginner's Guide":
        table = {
            1: ("PASS" if f["editing_layered"] and f["capstone_reel"] else "PARTIAL", ["layered soundbite/B-roll/music proof", "published reel render"]),
            2: ("PASS" if f["take_selector"] and f["editing_layered"] else "PARTIAL", ["take selector", "trim/replacement/title/logo timeline evidence"]),
            3: ("PASS" if f["fairlight_lanes"] and f["social_loudness_verified"] else "PARTIAL", ["Fairlight lanes", "verified LUFS/true peak"]),
            4: ("PASS" if f["color_cdl_versions"] else "PARTIAL", ["CDL primary correction", "stills/versions"]),
            5: ("PARTIAL", ["secondary adjustment target is marked; no UI-proven qualifier/window pass"]),
            6: ("PASS" if f["color_group_still"] and f["color_cdl_versions"] else "PARTIAL", ["stills/grades/version/cache evidence"]),
            7: ("PARTIAL", ["project setup/media import verified; Smart Bins/preferences not UI-proven"]),
            8: ("PASS" if f["fairlight_lanes"] and f["fairlight_bus_assets"] else "PARTIAL", ["Fairlight track formats, SFX/VO/music/stems"]),
            9: ("PASS" if f["fusion_nodes"] else "PARTIAL", ["Fusion comp/node export"]),
            10: ("PASS" if f["delivery_exports"] and f["project_exports"] else "PARTIAL", ["vertical deliver, subtitles, DRP/DRT/AAF/CSV exports"]),
        }
        status, reason = table[n]
    elif book == "Editor's Guide":
        table = {
            1: ("PASS" if f["editing_layered"] and f["capstone_reel"] else "PARTIAL", ["rough cut soundbite/B-roll/music capstone"]),
            2: ("PARTIAL", ["timeline refinements/markers exist; manual dynamic trim UI not proven"]),
            3: ("PASS" if f["take_selector"] else "PARTIAL", ["take selector and alternate-camera proof"]),
            4: ("PARTIAL", ["multi-camera media/takes present; live multicam angle-switch UI not proven"]),
            5: ("PARTIAL", ["media import/project organization evidence; Power Bins/People Analyze not proven"]),
            6: ("PASS" if f["subtitles_netflix"] else "PARTIAL", ["AI subtitle generation with Netflix preset"]),
            7: ("PARTIAL", ["effects/Fusion and sizing proof; full effects lesson not recreated"]),
            8: ("PASS" if f["fairlight_lanes"] else "PARTIAL", ["audio lanes, VO/SFX/music/stems"]),
            9: ("PASS" if f["delivery_exports"] and f["subtitles_netflix"] else "PARTIAL", ["AAF/aspect/subtitle/preset handoff evidence"]),
        }
        status, reason = table[n]
    elif book == "Colorist Guide":
        table = {
            1: ("PASS" if f["color_cdl_versions"] else "PARTIAL", ["primary grade and backup/still evidence"]),
            2: ("PASS" if f["color_cdl_versions"] else "PARTIAL", ["shot matching section across CAM1/CAM2"]),
            3: ("PARTIAL", ["isolated-area marker only; manual qualifier/window not UI-proven"]),
            4: ("PASS" if f["conform_exports"] else "PARTIAL", ["FCPXML and EDL/CDL exports for conform handoff"]),
            5: ("PARTIAL", ["node-order evidence captured in markers; complex node tree not UI-proven"]),
            6: ("PASS" if f["color_group_still"] else "PARTIAL", ["versions/stills/grade management"]),
            7: ("PASS" if f["color_group_still"] else "PARTIAL", ["group/still evidence; scene cut/group UI not fully proven"]),
            8: ("PASS" if f["delivery_exports"] else "PARTIAL", ["timeline sizing/cache/delivery handoff"]),
            9: ("FAIL", ["no raw/BRAW/R3D source project evidence"]),
            10: ("PASS" if f["delivery_exports"] else "PARTIAL", ["client/delivery exports and render validation"]),
        }
        status, reason = table[n]
    elif book == "Fairlight Audio Post":
        table = {
            1: ("PASS" if f["fairlight_lanes"] else "PARTIAL", ["audio-only style build with clips/tracks/markers"]),
            2: ("PASS" if f["subtitles_netflix"] and f["fairlight_lanes"] else "PARTIAL", ["dialogue lanes and speech-to-text"]),
            3: ("PASS" if f["fairlight_bus_assets"] else "PARTIAL", ["SFX/music/audio assets and markers"]),
            4: ("PARTIAL", ["ADR/VO/Foley lanes and cue tones; no live recording proof"]),
            5: ("PASS" if f["fairlight_lanes"] else "PARTIAL", ["dialogue balancing/panning track structure"]),
            6: ("PASS" if f["fairlight_bus_assets"] and f["social_loudness_verified"] else "PARTIAL", ["cleanup manifest and loudness verification"]),
            7: ("PARTIAL", ["creative SFX/Foley assets exist; FX UI settings not proven"]),
            8: ("PASS" if f["fairlight_bus_assets"] else "PARTIAL", ["bus/reference/stem assets"]),
            9: ("PASS" if f["fairlight_lanes"] and f["social_loudness_verified"] else "PARTIAL", ["ducked music and loudness verification"]),
            10: ("PASS" if f["delivery_exports"] and f["social_loudness_verified"] else "PARTIAL", ["stems/handoff exports and loudness"]),
            11: ("PARTIAL", ["immersive placeholder lane marks exploration; no Atmos master claimed"]),
        }
        status, reason = table[n]
    elif book == "Fusion Visual Effects":
        table = {
            1: ("PASS" if f["fusion_nodes"] else "PARTIAL", ["Fusion page/node graph proof"]),
            2: ("PASS" if f["fusion_nodes"] else "PARTIAL", ["split screen and tracking node proof"]),
            3: ("PARTIAL", ["key/sky replacement tools staged; no source sky shot"]),
            4: ("PASS" if f["fusion_nodes"] else "PARTIAL", ["PlanarTracker/sign-replacement tool proof"]),
            5: ("PARTIAL", ["DeltaKeyer/green-screen tools staged; no green-screen source comp"]),
            6: ("PASS" if f["fusion_nodes"] and f["fusion_v1_export"] else "PARTIAL", ["Text+/title comp exported"]),
            7: ("PASS" if f["fusion_nodes"] else "PARTIAL", ["keyframe/modifier-ready Fusion graph"]),
        }
        status, reason = table[n]
    elif book == "Advanced Visual Effects":
        table = {
            1: ("PASS" if f["fusion_nodes"] else "PARTIAL", ["3D text/camera/light/renderer node proof"]),
            2: ("PARTIAL", ["DeltaKeyer/VFX color workflow staged; no full green-screen exercise"]),
            3: ("PARTIAL", ["FastNoise/particle-style staging; no full rainy-day comp"]),
            4: ("PARTIAL", ["tracking tools staged; no solved 3D camera track"]),
            5: ("FAIL", ["no USD source/import/render evidence"]),
        }
        status, reason = table[n]
    return status, reason


def main() -> int:
    TRAINING.mkdir(parents=True, exist_ok=True)
    flags = evidence_flags()
    rows = []
    points = 0
    for lesson in parse_lessons():
        status, reasons = status_for(lesson, flags)
        score = {"PASS": 2, "PARTIAL": 1, "FAIL": 0}[status]
        points += score
        rows.append({**lesson, "status": status, "points": score, "evidence": reasons})
    total = len(rows) * 2
    pct = round(points / total * 100, 1) if total else 0
    counts = {s: sum(1 for r in rows if r["status"] == s) for s in ["PASS", "PARTIAL", "FAIL"]}
    ts = datetime.now().strftime("%Y%m%d-%H%M%S")
    payload = {
        "score": pct,
        "points": points,
        "total": total,
        "counts": counts,
        "target": 70,
        "passed_target": pct >= 70,
        "flags": flags,
        "rows": rows,
        "evidence_bundle": {
            "workbook_proof_v1": str(V1),
            "workbook_proof_v2": str(V2),
            "publish_reel": str(REEL),
            "youtube_cut": str(YOUTUBE),
            "verification": str(VERIFY),
        },
    }
    json_path = TRAINING / f"source_workbook_capstone_benchmark_{ts}.json"
    md_path = TRAINING / f"source_workbook_capstone_benchmark_{ts}.md"
    json_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    lines = [
        f"# Source Workbook Capstone Benchmark {ts}",
        "",
        f"Score: **{pct}/100** ({points}/{total})",
        f"Target 70: **{'PASS' if pct >= 70 else 'FAIL'}**",
        f"Counts: PASS={counts['PASS']} PARTIAL={counts['PARTIAL']} FAIL={counts['FAIL']}",
        "",
        "This is a source-workbook benchmark, not a claim that every homework exercise is 100% complete.",
        "PASS requires native Resolve/project evidence; PARTIAL means applied or staged but not fully UI-proven.",
        "",
        "| Book | Lesson | Status | Evidence |",
        "|---|---:|---|---|",
    ]
    for r in rows:
        ev = "; ".join(r["evidence"])
        lines.append(f"| {r['book']} | {r['lesson']} {r['title']} | {r['status']} | {ev} |")
    md_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(json.dumps({"score": pct, "points": points, "total": total, "counts": counts, "json": str(json_path), "md": str(md_path)}, indent=2))
    return 0 if pct >= 70 else 2


if __name__ == "__main__":
    raise SystemExit(main())
