#!/usr/bin/env python3
"""Rank audio sources with FFmpeg-derived dialogue-quality signals."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path


AUDIO_EXTS = {".wav", ".mp3", ".m4a", ".aac", ".flac", ".aiff", ".aif", ".mov", ".mp4", ".mkv"}


def run(cmd: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(cmd, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)


def discover(paths: list[str]) -> list[Path]:
    found: list[Path] = []
    for raw in paths:
        path = Path(raw).expanduser()
        if path.is_dir():
            found.extend(
                p
                for p in path.rglob("*")
                if p.suffix.lower() in AUDIO_EXTS and p.is_file() and not p.name.startswith("._")
            )
        elif path.is_file() and path.suffix.lower() in AUDIO_EXTS and not path.name.startswith("._"):
            found.append(path)
    return sorted(set(found))


def ffprobe(path: Path) -> dict:
    proc = run([
        "ffprobe",
        "-v",
        "error",
        "-show_entries",
        "format=duration:stream=codec_type,channels,sample_rate",
        "-of",
        "json",
        str(path),
    ])
    if proc.returncode != 0:
        return {"error": proc.stderr.strip()}
    return json.loads(proc.stdout or "{}")


def parse_float(pattern: str, text: str) -> float | None:
    match = re.search(pattern, text)
    return float(match.group(1)) if match else None


def input_args(path: Path, sample_seconds: float | None) -> list[str]:
    args = ["-i", str(path)]
    if sample_seconds:
        args.extend(["-t", str(sample_seconds)])
    return args


def volumedetect(path: Path, sample_seconds: float | None) -> dict:
    proc = run(["ffmpeg", "-hide_banner", "-nostats", *input_args(path, sample_seconds), "-af", "volumedetect", "-f", "null", "-"])
    text = proc.stderr
    return {
        "mean_volume_db": parse_float(r"mean_volume:\s*(-?\d+(?:\.\d+)?) dB", text),
        "max_volume_db": parse_float(r"max_volume:\s*(-?\d+(?:\.\d+)?) dB", text),
    }


def silence(path: Path, sample_seconds: float | None) -> dict:
    proc = run([
        "ffmpeg",
        "-hide_banner",
        "-nostats",
        *input_args(path, sample_seconds),
        "-af",
        "silencedetect=noise=-35dB:d=0.35",
        "-f",
        "null",
        "-",
    ])
    text = proc.stderr
    starts = [float(v) for v in re.findall(r"silence_start:\s*([0-9.]+)", text)]
    ends = [float(v) for v in re.findall(r"silence_end:\s*([0-9.]+)", text)]
    duration = 0.0
    for start, end in zip(starts, ends):
        duration += max(0.0, end - start)
    return {"silence_events": len(starts), "silence_seconds_est": round(duration, 3)}


def ebur128(path: Path, sample_seconds: float | None) -> dict:
    proc = run([
        "ffmpeg",
        "-hide_banner",
        "-nostats",
        *input_args(path, sample_seconds),
        "-af",
        "ebur128=peak=true",
        "-f",
        "null",
        "-",
    ])
    text = proc.stderr
    integrated = re.findall(r"I:\s*(-?\d+(?:\.\d+)?) LUFS", text)
    true_peak = re.findall(r"Peak:\s*(-?\d+(?:\.\d+)?) dBFS", text)
    return {
        "integrated_lufs": float(integrated[-1]) if integrated else None,
        "true_peak_dbfs": float(true_peak[-1]) if true_peak else None,
    }


def score(row: dict) -> float:
    score_value = 100.0
    duration = row.get("duration_seconds") or 0
    mean = row.get("mean_volume_db")
    maxv = row.get("max_volume_db")
    lufs = row.get("integrated_lufs")
    silence_pct = row.get("silence_percent_est") or 0
    if duration < 10:
        score_value -= 35
    if mean is None or mean < -35:
        score_value -= 30
    elif mean < -25:
        score_value -= 10
    if maxv is not None and maxv > -0.5:
        score_value -= 15
    if lufs is not None and (lufs < -24 or lufs > -10):
        score_value -= 10
    if silence_pct > 45:
        score_value -= 25
    elif silence_pct > 25:
        score_value -= 10
    return round(max(0.0, min(100.0, score_value)), 1)


def analyze(path: Path, sample_seconds: float | None) -> dict:
    probe = ffprobe(path)
    streams = probe.get("streams", []) if "error" not in probe else []
    audio_stream = next((s for s in streams if s.get("codec_type") == "audio"), {})
    duration = float((probe.get("format") or {}).get("duration") or 0)
    row = {
        "path": str(path),
        "duration_seconds": round(duration, 3),
        "channels": audio_stream.get("channels"),
        "sample_rate": audio_stream.get("sample_rate"),
    }
    row.update(volumedetect(path, sample_seconds))
    row.update(silence(path, sample_seconds))
    row.update(ebur128(path, sample_seconds))
    row["sample_seconds"] = sample_seconds
    row["silence_percent_est"] = round((row["silence_seconds_est"] / duration) * 100, 2) if duration else None
    row["dialogue_source_score"] = score(row)
    return row


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("paths", nargs="+", help="Audio/video files or directories to audit.")
    parser.add_argument("--out", help="Write JSON report to this path.")
    parser.add_argument("--sample-seconds", type=float, help="Analyze only the first N seconds for fast intake ranking.")
    args = parser.parse_args()

    files = discover(args.paths)
    if not files:
        raise SystemExit("No audio-capable files found.")
    rows = [analyze(path, args.sample_seconds) for path in files]
    rows.sort(key=lambda row: row["dialogue_source_score"], reverse=True)
    result = {"count": len(rows), "best_candidate": rows[0], "items": rows}
    payload = json.dumps(result, indent=2)
    if args.out:
        out = Path(args.out)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(payload + "\n")
    print(payload)


if __name__ == "__main__":
    main()
