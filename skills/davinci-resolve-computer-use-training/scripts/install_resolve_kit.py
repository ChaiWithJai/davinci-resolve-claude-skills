#!/usr/bin/env python3
"""Install Codex Resolve helper scripts into Resolve's Workspace > Scripts menu."""

from __future__ import annotations

import shutil
from pathlib import Path

from resolve_common import USER_SCRIPTS


SKILL_DIR = Path(__file__).resolve().parents[1]
SCRIPT_DIR = SKILL_DIR / "scripts"
TARGET_DIR = USER_SCRIPTS / "Utility" / "Codex"

MENU_SCRIPTS = {
    "Codex Resolve Doctor.py": SCRIPT_DIR / "resolve_doctor.py",
    "Codex Stage Folder Timeline.py": SCRIPT_DIR / "stage_folder_timeline.py",
    "Codex Validate Timeline.py": SCRIPT_DIR / "validate_timeline.py",
}


def main() -> int:
    TARGET_DIR.mkdir(parents=True, exist_ok=True)
    copied = []
    for target_name, source in MENU_SCRIPTS.items():
        target = TARGET_DIR / target_name
        shutil.copy2(source, target)
        copied.append(str(target))

    common_target = TARGET_DIR / "resolve_common.py"
    shutil.copy2(SCRIPT_DIR / "resolve_common.py", common_target)
    copied.append(str(common_target))

    print("Installed Resolve kit scripts:")
    for path in copied:
        print(f"- {path}")
    print("Restart Resolve or refresh scripts if the Workspace > Scripts menu does not show them.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
