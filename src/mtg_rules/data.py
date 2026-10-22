"""Data discovery shared by all runtime commands and hooks."""

import os
import sys
from pathlib import Path


def discover_data(skill: Path, env=None) -> Path:
    return locate_data(skill, env)[0]


def locate_data(skill: Path, env=None) -> tuple[Path, str]:
    """Return the data directory and the source label it was found through."""
    env = os.environ if env is None else env
    home = Path(env.get("HOME", str(Path.home())))
    codex = Path(env.get("CODEX_HOME") or home / ".codex")
    opencode = Path(env.get("XDG_DATA_HOME") or home / ".local/share") / "opencode"
    hosts = [
        (codex, codex / "plugins/data/mtg-rules/data"),
        (home / ".gemini", home / ".gemini/config/plugins/mtg-rules/data"),
        (home / ".claude", home / ".claude/plugins/data/mtg-rules/data"),
        (opencode, opencode / "plugins/data/mtg-rules/data"),
    ]
    candidates = [(Path(env[k]), "$" + k) for k in ("MTG_RULES_DATA", "PLUGIN_DATA", "CLAUDE_PLUGIN_DATA") if env.get(k)]
    for host, data in hosts:
        if skill.is_relative_to(host) or (
            host == opencode and skill.is_relative_to(home / ".config/opencode")
        ):
            candidates.append((data, "host plugin data"))
            break
    candidates += [(skill.parents[1] / "data", "repo-relative"), (skill.parent / "data", "repo-relative")]
    candidates += [(data, "host plugin data") for _, data in hosts]
    unique = {}
    for path, label in candidates:
        unique.setdefault(path, label)
    candidates = list(unique.items())
    for candidate, label in candidates:
        if os.access(candidate / "rules/cr.json", os.R_OK):
            return candidate, label
        if label == "$MTG_RULES_DATA":
            print(f"mtg-rules: warning: MTG_RULES_DATA is set but {candidate}/rules/cr.json is unreadable — trying other locations", file=sys.stderr)
    raise ValueError("mtg-rules: could not find data directory. Tried:\n" +
                     "\n".join(f"  {p}" for p, _ in candidates) +
                     f"\nPopulate plugin data with: {skill}/scripts/setup-data --runtime [--cards]")
