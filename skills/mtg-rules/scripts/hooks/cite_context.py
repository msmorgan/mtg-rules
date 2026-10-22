#!/usr/bin/env python3
"""Inject citation context from an unpacked plugin."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[4] / "src"))
from mtg_rules.cite_hook import main  # noqa: E402

if __name__ == "__main__":
    raise SystemExit(main())
