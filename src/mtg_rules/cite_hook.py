"""Nonblocking PostToolUse citation context, without shell utilities."""

import argparse
import contextlib
import io
import json
import os
import re
import sys
import tempfile
from pathlib import Path

from .cite import Repository, Snapshot, context
from .data import discover_data

# Shared with the shell harness's coverage assertion. Command positions only.
SCRIPT_NAMES = "(rule-search|underdetermined|setup-data|ensure-data|normalize-glossary|classify|corpus|rulings|keyword|version|define|health|lookup|card|cite|ref|rule|mtr)"
SKILL_CALL = re.compile(r"(^|[;&|(]|env( +[A-Za-z_][A-Za-z0-9_]*=[^ ]*)+ +)\s*(\./)*" + SCRIPT_NAMES + r"(\s|$)")


def render(payload: dict) -> str:
    if "CITE_CONTEXT_OFF" in os.environ:
        return ""
    tool = payload.get("tool_name")
    inputs, response = payload.get("tool_input") or {}, payload.get("tool_response") or {}
    if tool == "Write":
        text = inputs.get("content", "")
    elif tool == "Edit":
        text = inputs.get("new_string", "")
    elif tool == "Read" and "CITE_ON_READ" in os.environ:
        text = response if isinstance(response, str) else response.get("file", {}).get("content", response.get("content", ""))
    elif tool == "Bash" and "CITE_ON_BASH" in os.environ:
        command = inputs.get("command", "")
        if "mtg-rules" in command or SKILL_CALL.search(command):
            return ""
        text = response if isinstance(response, str) else response.get("stdout", "")
    else:
        return ""
    cwd = Path(payload.get("cwd") or Path.cwd()).resolve()
    root = next((p for p in (cwd, *cwd.parents) if (p / "cite-config.json").is_file()
                 and ((p / ".jj").is_dir() or (p / ".git").exists())), None)
    if root is None or not text:
        return ""
    repo = Repository(root / "cite-config.json")
    if "[CR#" not in text and not (repo.fmt == "bare" and re.search(r"[1-9][0-9]{2}\.[0-9]+", text)):
        return ""
    skill = Path(__file__).resolve().parents[2] / "skills/mtg-rules"
    snapshot = Snapshot(discover_data(skill) / "rules")
    directory = Path(os.environ.get("TMPDIR") or tempfile.gettempdir()) / "mtg-rules-cite"
    directory.mkdir(parents=True, exist_ok=True)
    session = re.sub(r"[^A-Za-z0-9._-]", "_", str(payload.get("session_id", "nosession")))
    limit = os.environ.get("CITE_CONTEXT_MAX", "40")
    if not re.fullmatch(r"[0-9]+", limit):
        limit = "40"
    args = argparse.Namespace(seen=str(directory / (session + ".seen")), max=limit,
                              full="CITE_CONTEXT_FULL" in os.environ)
    output = io.StringIO()
    with contextlib.redirect_stdout(output), contextlib.redirect_stderr(io.StringIO()):
        context(repo, snapshot, args, text=text)
    return output.getvalue()


def main() -> int:
    try:
        text = render(json.load(sys.stdin))
        if text:
            print(json.dumps({"hookSpecificOutput": {"hookEventName": "PostToolUse", "additionalContext": text}}))
    except Exception:  # A context hook must never block the invoking tool.
        pass
    return 0
