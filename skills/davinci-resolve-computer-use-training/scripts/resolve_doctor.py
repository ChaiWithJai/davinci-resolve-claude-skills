#!/usr/bin/env python3
"""Check DaVinci Resolve automation readiness for Codex skills."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path

from resolve_common import MODULES, SCRIPT_API, SCRIPT_LIB, USER_SCRIPTS, get_resolve


def process_rows() -> list[dict[str, str]]:
    result = subprocess.run(
        ["ps", "-axo", "pid,ppid,stat,etime,%cpu,%mem,rss,command"],
        check=True,
        text=True,
        capture_output=True,
    )
    rows = []
    for line in result.stdout.splitlines()[1:]:
        if "DaVinci Resolve" in line or "fuscript" in line:
            parts = line.split(None, 7)
            if len(parts) == 8:
                rows.append(
                    {
                        "pid": parts[0],
                        "ppid": parts[1],
                        "stat": parts[2],
                        "etime": parts[3],
                        "cpu_percent": parts[4],
                        "mem_percent": parts[5],
                        "rss_kb": parts[6],
                        "command": parts[7],
                    }
                )
    return rows


def connect_resolve() -> dict[str, object]:
    try:
        resolve = get_resolve()
    except Exception as exc:  # pragma: no cover - diagnostic script
        return {"connected": False, "error": str(exc)}

    project_manager = resolve.GetProjectManager()
    project = project_manager.GetCurrentProject() if project_manager else None
    timeline = project.GetCurrentTimeline() if project else None
    database = project_manager.GetCurrentDatabase() if project_manager else None

    return {
        "connected": True,
        "product_name": resolve.GetProductName(),
        "version": resolve.GetVersionString(),
        "current_page": resolve.GetCurrentPage(),
        "database": database,
        "project": project.GetName() if project else None,
        "timeline": timeline.GetName() if timeline else None,
        "timeline_start_frame": int(timeline.GetStartFrame()) if timeline else None,
        "timeline_tracks": {
            "video": timeline.GetTrackCount("video") if timeline else None,
            "audio": timeline.GetTrackCount("audio") if timeline else None,
        },
    }


def main() -> int:
    report = {
        "paths": {
            "script_api": str(SCRIPT_API),
            "script_api_exists": SCRIPT_API.exists(),
            "script_lib": str(SCRIPT_LIB),
            "script_lib_exists": SCRIPT_LIB.exists(),
            "modules": str(MODULES),
            "modules_exists": MODULES.exists(),
            "user_scripts": str(USER_SCRIPTS),
        },
        "processes": process_rows(),
        "resolve": connect_resolve(),
    }
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["resolve"].get("connected") else 1


if __name__ == "__main__":
    raise SystemExit(main())
