#!/usr/bin/env python3
"""Copy the finished front page into the directory make.fun expects.

Reads entry.png from this file's own directory and writes it to
$MAKEFUN_OUTPUT_DIR (or the current directory when the variable is unset).
Only the Python standard library is used.

Usage:
    python3 main.py
    MAKEFUN_OUTPUT_DIR=/path/to/output python3 main.py
"""

import os
import shutil
import sys
from pathlib import Path

SOURCE_NAME = "entry.png"


def main() -> int:
    here = Path(__file__).resolve().parent
    source = here / SOURCE_NAME
    if not source.is_file():
        print(
            f"cannot copy: {SOURCE_NAME} is missing next to main.py "
            f"(looked in {here})",
            file=sys.stderr,
        )
        return 1
    target_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR") or ".")
    target_dir.mkdir(parents=True, exist_ok=True)
    target = target_dir / SOURCE_NAME
    shutil.copyfile(source, target)
    if target.stat().st_size != source.stat().st_size:
        print(f"copy size mismatch: {source} -> {target}", file=sys.stderr)
        return 1
    print(f"copied {source} -> {target} ({target.stat().st_size} bytes)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
