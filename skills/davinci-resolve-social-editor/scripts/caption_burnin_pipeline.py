#!/usr/bin/env python3
"""Create Netflix-style ASS captions and optionally burn them into a review video."""

from __future__ import annotations

import argparse
import html
import re
import subprocess
from pathlib import Path


def parse_srt_time(value: str) -> str:
    hh, mm, rest = value.strip().split(":")
    ss, ms = rest.split(",")
    centiseconds = int(round(int(ms) / 10))
    return f"{int(hh)}:{int(mm):02d}:{int(ss):02d}.{centiseconds:02d}"


def wrap_caption(text: str, limit: int = 34) -> str:
    words = text.split()
    lines: list[str] = []
    current: list[str] = []
    for word in words:
        candidate = " ".join(current + [word])
        if current and len(candidate) > limit and len(lines) < 1:
            lines.append(" ".join(current))
            current = [word]
        else:
            current.append(word)
    if current:
        lines.append(" ".join(current))
    return r"\N".join(lines[:2])


def srt_to_events(srt_text: str) -> list[tuple[str, str, str]]:
    blocks = re.split(r"\n\s*\n", srt_text.strip(), flags=re.MULTILINE)
    events: list[tuple[str, str, str]] = []
    for block in blocks:
        lines = [line.strip() for line in block.splitlines() if line.strip()]
        timing = next((line for line in lines if "-->" in line), None)
        if not timing:
            continue
        start_raw, end_raw = [part.strip().split()[0] for part in timing.split("-->")]
        text_lines = lines[lines.index(timing) + 1 :]
        text = html.unescape(" ".join(text_lines))
        text = re.sub(r"\s+", " ", text).strip()
        if text:
            events.append((parse_srt_time(start_raw), parse_srt_time(end_raw), wrap_caption(text)))
    return events


def write_ass(srt_path: Path, ass_path: Path) -> None:
    events = srt_to_events(srt_path.read_text(errors="replace"))
    header = """[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Netflix,Arial,68,&H00FFFFFF,&H00FFFFFF,&H00000000,&HAA000000,-1,0,0,0,100,100,0,0,3,4,0,2,88,88,190,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    lines = [header]
    for start, end, text in events:
        safe_text = text.replace("{", "").replace("}", "")
        lines.append(f"Dialogue: 0,{start},{end},Netflix,,0,0,0,,{safe_text}\n")
    ass_path.parent.mkdir(parents=True, exist_ok=True)
    ass_path.write_text("".join(lines))


def burn(video: Path, ass_path: Path, out: Path) -> None:
    out.parent.mkdir(parents=True, exist_ok=True)
    ass_filter = str(ass_path).replace("\\", "\\\\").replace(":", "\\:")
    cmd = [
        "ffmpeg",
        "-y",
        "-i",
        str(video),
        "-vf",
        f"subtitles='{ass_filter}'",
        "-c:v",
        "libx264",
        "-preset",
        "medium",
        "-crf",
        "18",
        "-c:a",
        "copy",
        str(out),
    ]
    subprocess.run(cmd, check=True)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--srt", required=True, help="Reviewed SRT captions.")
    parser.add_argument("--ass-out", required=True, help="ASS caption output path.")
    parser.add_argument("--video", help="Optional input video for burned-in review render.")
    parser.add_argument("--out", help="Optional burned-in review render output path.")
    args = parser.parse_args()

    ass_path = Path(args.ass_out)
    write_ass(Path(args.srt), ass_path)
    print(f"Wrote {ass_path}")
    if args.video or args.out:
        if not args.video or not args.out:
            raise SystemExit("--video and --out must be provided together.")
        burn(Path(args.video), ass_path, Path(args.out))
        print(f"Wrote {args.out}")


if __name__ == "__main__":
    main()
