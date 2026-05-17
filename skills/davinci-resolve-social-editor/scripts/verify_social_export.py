#!/usr/bin/env python3
import argparse
import json
import re
import subprocess
from pathlib import Path


def run(cmd):
    return subprocess.check_output(cmd, text=True, stderr=subprocess.STDOUT)


def probe(path: Path):
    return json.loads(run([
        "ffprobe", "-v", "error",
        "-show_format", "-show_streams",
        "-print_format", "json",
        str(path),
    ]))


def duration(probe_json):
    return float(probe_json.get("format", {}).get("duration", 0) or 0)


def parse_loudness(log: str):
    summary = log.split("Summary:")[-1]
    integrated = re.search(r"I:\s+(-?\d+(?:\.\d+)?) LUFS", summary)
    lra = re.search(r"LRA:\s+(-?\d+(?:\.\d+)?) LU", summary)
    peak = re.search(r"Peak:\s+(-?\d+(?:\.\d+)?) dBFS", summary)
    return {
        "integrated_lufs": float(integrated.group(1)) if integrated else None,
        "loudness_range_lu": float(lra.group(1)) if lra else None,
        "true_peak_dbfs": float(peak.group(1)) if peak else None,
    }


def video_stream(probe_json):
    for stream in probe_json.get("streams", []):
        if stream.get("codec_type") == "video":
            return stream
    return {}


def warnings_for(probe_json, loudness):
    warnings = []
    video = video_stream(probe_json)
    width = int(video.get("width") or 0)
    height = int(video.get("height") or 0)
    if (width, height) != (1080, 1920):
        warnings.append(f"Expected 1080x1920 vertical export, found {width}x{height}.")
    integrated = loudness.get("integrated_lufs")
    if integrated is not None and not (-16.5 <= integrated <= -13.5):
        warnings.append(f"Integrated loudness {integrated:.1f} LUFS is outside the -16 to -14 social target band.")
    true_peak = loudness.get("true_peak_dbfs")
    if true_peak is not None and true_peak > -1.0:
        warnings.append(f"True peak {true_peak:.1f} dBFS is hotter than the -1 dBTP target.")
    return warnings


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("render")
    ap.add_argument("--out-dir", required=True)
    ap.add_argument("--timestamps", default="")
    args = ap.parse_args()

    render = Path(args.render).expanduser().resolve()
    out_dir = Path(args.out_dir).expanduser().resolve()
    out_dir.mkdir(parents=True, exist_ok=True)

    p = probe(render)
    dur = duration(p)
    if args.timestamps:
        times = [float(x) for x in args.timestamps.split(",") if x.strip()]
    else:
        times = sorted(set([2, max(0, dur * 0.15), dur * 0.35, dur * 0.60, dur * 0.85, max(0, dur - 3)]))

    stills = []
    for t in times:
        if t >= dur:
            continue
        out = out_dir / f"review_{t:06.2f}s.jpg"
        subprocess.run([
            "ffmpeg", "-y", "-ss", f"{t:.3f}", "-i", str(render),
            "-frames:v", "1", str(out),
        ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
        stills.append(str(out))

    loudness_log = ""
    try:
        loudness_log = run([
            "ffmpeg", "-i", str(render),
            "-filter_complex", "ebur128=peak=true",
            "-f", "null", "-"
        ])
    except subprocess.CalledProcessError as exc:
        loudness_log = exc.output
    (out_dir / "loudness_ebur128.log").write_text(loudness_log, encoding="utf-8")
    loudness = parse_loudness(loudness_log)

    report = {
        "render": str(render),
        "duration": dur,
        "probe": p,
        "review_stills": stills,
        "loudness_log": str(out_dir / "loudness_ebur128.log"),
        "loudness": loudness,
        "warnings": warnings_for(p, loudness),
    }
    report_path = out_dir / "verification_report.json"
    report_path.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(report_path)


if __name__ == "__main__":
    main()
