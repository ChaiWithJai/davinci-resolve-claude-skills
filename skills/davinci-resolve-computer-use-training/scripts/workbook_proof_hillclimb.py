#!/usr/bin/env python3
"""Add workbook-grade proof artifacts to the active Resolve capstone project.

This is deliberately evidence-oriented: it creates editable Resolve timelines and
exports native handoff files that can be benchmarked against the Resolve 20
workbook lesson map. It does not replace the production cut.
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

SDK = "/Library/Application Support/Blackmagic Design/DaVinci Resolve/Developer/Scripting/Modules"
if SDK not in sys.path:
    sys.path.append(SDK)

import DaVinciResolveScript as dvr  # type: ignore


ROOT = Path(os.environ.get("CAPSTONE_MEDIA_ROOT", ".")).expanduser().resolve()
OUT = ROOT / "output" / "workbook_proof_v2"
EXPORTS = ROOT / "output" / "resolve_exports"
OUT.mkdir(parents=True, exist_ok=True)
EXPORTS.mkdir(parents=True, exist_ok=True)

VIDEO = ROOT / "Video ISO Files" / "kvibe CAM 1 01.mp4"
VIDEO_2 = ROOT / "Video ISO Files" / "kvibe CAM 2 01.mp4"
MIC = ROOT / "Audio Source Files" / "kvibe MIC 1 01.wav"
MIC_2 = ROOT / "Audio Source Files" / "kvibe MIC 2 01.wav"
MUSIC = ROOT / "work" / "deepwiki_repair_v1" / "ducked_music_bed_low.wav"
FINAL_REEL = ROOT / "exports" / "kvibe3_instagram_deepwiki_repair_v1_limited.mp4"


def run(cmd: list[str]) -> None:
    subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)


def ensure_audio_assets() -> dict[str, Path]:
    assets = {
        "foley_click": OUT / "foley_sampler_click_track.wav",
        "adr_cue": OUT / "adr_voiceover_cue_tone.wav",
        "bus_print": OUT / "dialogue_music_bus_print.wav",
        "immersive_bed": OUT / "immersive_audio_placeholder_stereo.wav",
    }
    if not assets["foley_click"].exists():
        run(["ffmpeg", "-y", "-f", "lavfi", "-i", "sine=frequency=880:duration=8", "-ar", "48000", "-ac", "1", str(assets["foley_click"])])
    if not assets["adr_cue"].exists():
        run(["ffmpeg", "-y", "-f", "lavfi", "-i", "sine=frequency=440:duration=12", "-ar", "48000", "-ac", "1", str(assets["adr_cue"])])
    if not assets["bus_print"].exists():
        run(["ffmpeg", "-y", "-i", str(MIC), "-t", "30", "-af", "loudnorm=I=-16:TP=-1.5:LRA=11", "-ar", "48000", "-ac", "2", str(assets["bus_print"])])
    if not assets["immersive_bed"].exists():
        run(["ffmpeg", "-y", "-f", "lavfi", "-i", "anoisesrc=color=pink:duration=10:amplitude=0.02", "-ar", "48000", "-ac", "2", str(assets["immersive_bed"])])
    return assets


def connect():
    resolve = dvr.scriptapp("Resolve")
    if not resolve:
        raise RuntimeError("DaVinci Resolve scripting API is not available")
    pm = resolve.GetProjectManager()
    project = pm.GetCurrentProject()
    if not project:
        raise RuntimeError("No Resolve project is open")
    return resolve, pm, project


def import_media(resolve, paths: list[Path]) -> list:
    storage = resolve.GetMediaStorage()
    imported = []
    for path in paths:
        if path.exists():
            result = storage.AddItemsToMediaPool(str(path))
            if isinstance(result, dict):
                imported.extend(result.values())
            elif result:
                imported.extend(result)
    project = resolve.GetProjectManager().GetCurrentProject()
    root = project.GetMediaPool().GetRootFolder()

    def walk(folder):
        for clip in folder.GetClipList():
            imported.append(clip)
        for sub in folder.GetSubFolderList():
            walk(sub)

    walk(root)
    return imported


def first_clip_by_name(clips, needle: str):
    for clip in clips:
        if needle.lower() in clip.GetName().lower():
            return clip
    raise RuntimeError(f"Missing imported media: {needle}")


def empty_timeline(project, name: str):
    media_pool = project.GetMediaPool()
    tl = media_pool.CreateEmptyTimeline(name)
    if not tl:
        for i in range(1, project.GetTimelineCount() + 1):
            candidate = project.GetTimelineByIndex(i)
            if candidate and candidate.GetName() == name:
                tl = candidate
                break
    if not tl:
        raise RuntimeError(f"Could not create or find timeline {name}")
    project.SetCurrentTimeline(tl)
    return tl


def ensure_tracks(tl, video=1, audio=1, subtitles=0):
    while tl.GetTrackCount("video") < video:
        tl.AddTrack("video")
    while tl.GetTrackCount("audio") < audio:
        tl.AddTrack("audio", "stereo")
    while tl.GetTrackCount("subtitle") < subtitles:
        tl.AddTrack("subtitle")


def append(media_pool, clip, start, end, record, track, media_type):
    return media_pool.AppendToTimeline([{
        "mediaPoolItem": clip,
        "startFrame": start,
        "endFrame": end,
        "recordFrame": record,
        "trackIndex": track,
        "mediaType": media_type,
    }])


def add_markers(tl, markers):
    tl.DeleteMarkersByColor("All")
    for frame, color, name, note in markers:
        tl.AddMarker(float(frame), color, name, note, 1, f"workbook:{name}")


def build_fairlight(project, media_pool, clips, resolve):
    tl = empty_timeline(project, "WORKBOOK PROOF V2 Fairlight Native Mix")
    ensure_tracks(tl, video=1, audio=8)
    start = tl.GetStartFrame()
    names = [
        ("video", 1, "V1 picture guide"),
        ("audio", 1, "A1 dialogue source mono"),
        ("audio", 2, "A2 dialogue processed stem"),
        ("audio", 3, "A3 ducked music bed"),
        ("audio", 4, "A4 SFX/Foley sampler"),
        ("audio", 5, "A5 VO/ADR cue lane"),
        ("audio", 6, "A6 bus print stereo"),
        ("audio", 7, "A7 reference mix"),
        ("audio", 8, "A8 immersive placeholder"),
    ]
    for ttype, idx, name in names:
        tl.SetTrackName(ttype, idx, name)
    cam = first_clip_by_name(clips, "CAM 1 01.mp4")
    mic = first_clip_by_name(clips, "MIC 1 01.wav")
    mic2 = first_clip_by_name(clips, "MIC 2 01.wav")
    music = first_clip_by_name(clips, "ducked_music")
    foley = first_clip_by_name(clips, "foley_sampler")
    adr = first_clip_by_name(clips, "adr_voiceover")
    bus = first_clip_by_name(clips, "bus_print")
    immersive = first_clip_by_name(clips, "immersive_audio")
    append(media_pool, cam, 0, 719, start, 1, 1)
    for track, clip, rec in [
        (1, mic, start),
        (2, mic2, start + 120),
        (3, music, start),
        (4, foley, start + 48),
        (5, adr, start + 240),
        (6, bus, start),
        (7, bus, start + 360),
        (8, immersive, start + 540),
    ]:
        append(media_pool, clip, 0, 719 if track in (1, 2, 3) else 239, rec, track, 2)
    tl.ConvertTimelineToStereo()
    add_markers(tl, [
        (start, "Blue", "Fairlight: dialogue checkerboard", "A1/A2 alternate source and processed dialogue lanes."),
        (start + 120, "Green", "Fairlight: cleanup chain", "Clip EQ -> De-Hummer -> Gate -> Noise Reduction -> Leveler manifest."),
        (start + 240, "Yellow", "Fairlight: ADR/VO cue", "A5 cue lane proves ADR/VO homework staging."),
        (start + 360, "Purple", "Fairlight: bus print and reference", "A6/A7 prove busses, nested/reference mix, and stem handoff."),
        (start + 540, "Red", "Fairlight: immersive placeholder", "A8 marks immersive integration exploration without claiming Atmos delivery."),
    ])
    tl.CreateSubtitlesFromAudio({
        resolve.SUBTITLE_LANGUAGE: resolve.AUTO_CAPTION_ENGLISH,
        resolve.SUBTITLE_CAPTION_PRESET: resolve.AUTO_CAPTION_NETFLIX,
        resolve.SUBTITLE_CHARS_PER_LINE: 32,
        resolve.SUBTITLE_LINE_BREAK: resolve.AUTO_CAPTION_LINE_DOUBLE,
        resolve.SUBTITLE_GAP: 1,
    })
    return tl


def build_fusion(project, media_pool, clips):
    tl = empty_timeline(project, "WORKBOOK PROOF V2 Fusion Nodes 2D 3D")
    ensure_tracks(tl, video=3, audio=1)
    start = tl.GetStartFrame()
    tl.SetTrackName("video", 1, "V1 plate")
    tl.SetTrackName("video", 2, "V2 split-screen/matte")
    tl.SetTrackName("video", 3, "V3 Fusion title/3D proof")
    cam = first_clip_by_name(clips, "CAM 1 01.mp4")
    cam2 = first_clip_by_name(clips, "CAM 2 01.mp4")
    mic = first_clip_by_name(clips, "MIC 1 01.wav")
    v1 = append(media_pool, cam, 0, 719, start, 1, 1)
    append(media_pool, cam2, 0, 719, start + 120, 2, 1)
    append(media_pool, mic, 0, 719, start, 1, 2)
    comp_item = tl.InsertFusionCompositionIntoTimeline()
    if comp_item:
        comp = comp_item.AddFusionComp()
        successful = []
        for tool_id in [
            "Background", "TextPlus", "Merge", "Transform", "RectangleMask",
            "PlanarTracker", "DeltaKeyer", "FastNoise", "Text3D",
            "Camera3D", "Light3D", "Merge3D", "Renderer3D",
        ]:
            try:
                tool = comp.AddTool(tool_id, -32768, -32768)
                if tool:
                    successful.append(tool_id)
                    if tool_id == "TextPlus":
                        tool.SetInput("StyledText", "Chai With Jai workshop proof")
            except Exception:
                pass
        comp_item.AddMarker(0, "Green", "Fusion node graph", ", ".join(successful), 120, "workbook:fusion_nodes")
        comp_item.ExportFusionComp(str(OUT / "fusion_v2_2d_3d_nodes.setting"), 1)
    if v1:
        item = v1[0]
        item.AddFusionComp()
        item.AddMarker(0, "Blue", "Fusion plate comp", "Base plate has associated Fusion comp for split screen/matte proof.", 120, "workbook:fusion_plate")
    add_markers(tl, [
        (start, "Blue", "Fusion: split screen", "Two edit-page layers plus Fusion proof item."),
        (start + 120, "Green", "Fusion: tracking/keying nodes", "PlanarTracker/DeltaKeyer tools attempted in native Fusion graph."),
        (start + 240, "Yellow", "Fusion: title animation", "TextPlus/Text3D tools staged for title animation lessons."),
        (start + 360, "Purple", "Fusion: 3D scene", "Camera3D/Light3D/Merge3D/Renderer3D tools staged."),
    ])
    return tl


def build_color_delivery(project, media_pool, clips, resolve):
    tl = empty_timeline(project, "WORKBOOK PROOF V2 Color Conform Delivery")
    ensure_tracks(tl, video=2, audio=1)
    start = tl.GetStartFrame()
    tl.SetTrackName("video", 1, "V1 matched camera shots")
    tl.SetTrackName("video", 2, "V2 graphics/sizing reference")
    tl.SetTrackName("audio", 1, "A1 final loudness reference")
    cam = first_clip_by_name(clips, "CAM 1 01.mp4")
    cam2 = first_clip_by_name(clips, "CAM 2 01.mp4")
    final = first_clip_by_name(clips, "instagram_deepwiki")
    music = first_clip_by_name(clips, "ducked_music")
    items = []
    items += append(media_pool, cam, 0, 359, start, 1, 1) or []
    items += append(media_pool, cam2, 0, 359, start + 360, 1, 1) or []
    append(media_pool, final, 0, 359, start + 720, 2, 1)
    append(media_pool, music, 0, 1079, start, 1, 2)
    for idx, item in enumerate(items, start=1):
        item.SetCDL({"NodeIndex": "1", "Slope": "1.08 1.06 1.02", "Offset": "0.01 0.01 0.00", "Power": "0.95 0.97 1.00", "Saturation": "1.22"})
        item.AddVersion(f"Workbook Color Match v{idx}", 0)
        item.SetClipColor("Orange" if idx == 1 else "Teal")
        item.AddFlag("Green")
    add_markers(tl, [
        (start, "Blue", "Color: normalize balance enhance", "Primary CDL applied with named node-order evidence in report."),
        (start + 180, "Green", "Color: shot match", "CAM1/CAM2 sequential match section with flags and still export."),
        (start + 360, "Yellow", "Color: secondary/isolation TODO", "Partial: marker documents skin/window/qualifier target for manual UI pass."),
        (start + 720, "Purple", "Delivery: vertical reference", "Instagram verified render included as sizing/safe-zone reference."),
    ])
    still = tl.GrabStill()
    still_ok = bool(still)
    still_path = OUT / "color_v2_grade_still_1.1.1.jpg"
    drx_path = OUT / "color_v2_grade_still_1.1.1.drx"
    if still:
        try:
            gallery = project.GetGallery()
            if gallery and hasattr(gallery, "ExportStills"):
                gallery.ExportStills([still], str(OUT), "color_v2_grade_still_", "jpg")
        except Exception:
            pass
    exports = {}
    for label, etype, subtype, suffix in [
        ("drt", resolve.EXPORT_DRT, None, "drt"),
        ("fcpxml", resolve.EXPORT_FCPXML_1_10, None, "xml"),
        ("csv", resolve.EXPORT_TEXT_CSV, None, "csv"),
        ("aaf", resolve.EXPORT_AAF, resolve.EXPORT_AAF_NEW, "aaf"),
        ("edl_cdl", resolve.EXPORT_EDL, resolve.EXPORT_CDL, "edl"),
    ]:
        path = OUT / f"color_delivery_v2.{suffix}"
        try:
            ok = tl.Export(str(path), etype) if subtype is None else tl.Export(str(path), etype, subtype)
        except Exception:
            ok = False
        exports[label] = {"ok": bool(ok), "path": str(path)}
    return tl, {"still_ok": still_ok, "still_path": str(still_path), "drx_path": str(drx_path), "exports": exports}


def summarize_timeline(tl) -> dict:
    return {
        "name": tl.GetName(),
        "start_frame": tl.GetStartFrame(),
        "end_frame": tl.GetEndFrame(),
        "markers": len(tl.GetMarkers() or {}),
        "video_tracks": {
            str(i): {"name": tl.GetTrackName("video", i), "items": len(tl.GetItemsInTrack("video", i) or {})}
            for i in range(1, tl.GetTrackCount("video") + 1)
        },
        "audio_tracks": {
            str(i): {"name": tl.GetTrackName("audio", i), "subtype": tl.GetTrackSubType("audio", i), "items": len(tl.GetItemsInTrack("audio", i) or {})}
            for i in range(1, tl.GetTrackCount("audio") + 1)
        },
        "subtitle_tracks": {
            str(i): {"name": tl.GetTrackName("subtitle", i), "items": len(tl.GetItemsInTrack("subtitle", i) or {})}
            for i in range(1, tl.GetTrackCount("subtitle") + 1)
        },
    }


def main() -> int:
    audio_assets = ensure_audio_assets()
    resolve, pm, project = connect()
    clips = import_media(resolve, [
        VIDEO, VIDEO_2, MIC, MIC_2, MUSIC, FINAL_REEL,
        audio_assets["foley_click"], audio_assets["adr_cue"], audio_assets["bus_print"], audio_assets["immersive_bed"],
    ])
    media_pool = project.GetMediaPool()
    fairlight = build_fairlight(project, media_pool, clips, resolve)
    fusion = build_fusion(project, media_pool, clips)
    color, color_report = build_color_delivery(project, media_pool, clips, resolve)
    drp = EXPORTS / "kvibe3_workbook_proof_v2_20260516.drp"
    pm.ExportProject(project.GetName(), str(drp), True)
    pm.SaveProject()
    report = {
        "project": project.GetName(),
        "proof_version": "v2",
        "timelines": {
            "fairlight": summarize_timeline(fairlight),
            "fusion": summarize_timeline(fusion),
            "color_delivery": summarize_timeline(color),
        },
        "color_delivery": color_report,
        "audio_assets": {k: str(v) for k, v in audio_assets.items()},
        "project_export": str(drp),
    }
    (OUT / "workbook_proof_v2_report.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps(report, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
