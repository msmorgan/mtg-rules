#!/usr/bin/env python3
"""Run the ensure hook from an unpacked plugin."""
import sys
from pathlib import Path

SKILL = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(SKILL.parents[1] / "src"))
from mtg_rules.hooks import main  # noqa: E402

if __name__ == "__main__":
    raise SystemExit(main("ensure", SKILL))
