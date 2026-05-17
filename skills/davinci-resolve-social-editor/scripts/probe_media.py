#!/usr/bin/env python3
import argparse
import json
import subprocess
from pathlib import Path

MEDIA_EXTS = {".mp4", ".mov", ".m4v", ".wav", ".mp3", ".m4a", ".aif", ".aiff", ".png", ".jpg", ".jpeg", ".drp"}
PROBE_EXTS = {".mp4", ".mov", ".m4v", ".wav", ".mp3", ".m4a", ".aif", ".aiff"}


def run_json(cmd):
    out = subprocess.check_output(cmd, text=True, stderr=subprocess.STDOUT)
    return json.loads(out)


def ffprobe(path: Path):
    if path.suffix.lower() not in PROBE_EXTS:
        return {}
    try:
        return run_json([
            "ffprobe", "-v", "error",
            "-show_format", "-show_streams",
            "-print_format", "json",
            str(path),
        ])
    except subprocess.CalledProcessError as exc:
        return {"error": exc.output.strip() or str(exc)}
    except Exception as exc:
        return {"error": str(exc)}


def classify(path: Path, probe: dict):
    name = path.name.lower()
    if path.suffix.lower() == ".drp":
        return "resolve_project"
    streams = probe.get("streams", [])
    has_video = any(s.get("codec_type") == "video" for s in streams)
    has_audio = any(s.get("codec_type") == "audio" for s in streams)
    if "cam" in name and has_video:
        return "video_iso"
    if path.suffix.lower() in {".wav", ".aif", ".aiff"} and has_audio:
        return "hq_audio"
    if path.suffix.lower() in {".png", ".jpg", ".jpeg"}:
        return "brand_or_image"
    if has_video:
        return "video"
    if has_audio:
        return "audio"
    return "other"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("root")
    ap.add_argument("--out", required=True)
    args = ap.parse_args()

    root = Path(args.root).expanduser().resolve()
    files = []
    for p in root.rglob("*"):
        if p.is_file() and p.suffix.lower() in MEDIA_EXTS and not p.name.startswith("._"):
            rel = str(p.relative_to(root))
            probe = ffprobe(p)
            files.append({
                "path": str(p),
                "relative_path": rel,
                "size": p.stat().st_size,
                "kind": classify(p, probe),
                "probe": probe,
            })

    out = {
        "root": str(root),
        "files": files,
        "summary": {
            "count": len(files),
            "video_iso": sum(1 for f in files if f["kind"] == "video_iso"),
            "hq_audio": sum(1 for f in files if f["kind"] == "hq_audio"),
            "brand_or_image": sum(1 for f in files if f["kind"] == "brand_or_image"),
            "resolve_project": sum(1 for f in files if f["kind"] == "resolve_project"),
        },
    }
    out_path = Path(args.out).expanduser().resolve()
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(out, indent=2), encoding="utf-8")
    print(out_path)


if __name__ == "__main__":
    main()
