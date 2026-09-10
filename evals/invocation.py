#!/usr/bin/env python3
"""Run one cold discovery probe, or grade a saved Claude stream without a model call."""

import argparse
import json
from pathlib import Path
import shlex
import subprocess
import tempfile

EVALS = Path(__file__).resolve().parent
PLUGIN = EVALS.parent


def is_skill(name):
    return isinstance(name, str) and name.split(":")[-1] == "mtg-rules"


def script_commands(command, require_success_boundary=True):
    """Recognize literal executable positions, excluding echoed paths and comments."""
    lexer = shlex.shlex(command, posix=True, punctuation_chars=";&|()\n")
    lexer.whitespace = " \t\r"
    lexer.whitespace_split = True
    try:
        tokens = list(lexer)
    except ValueError:
        return set()
    groups = [[]]
    for token in tokens:
        if token and all(c in ";&|()\n" for c in token):
            groups.append([])
        else:
            groups[-1].append(token)
    groups = [g for g in groups if g]
    # Only credit a single command, optionally following a successful cd.
    # A later command can mask a failed lookup's exit status.
    if require_success_boundary and len(groups) == 2 and groups[0][0] == "cd" and "&&" in tokens:
        groups = groups[1:]
    if require_success_boundary and len(groups) != 1:
        return set()
    found = set()
    for group in groups:
        if not group:
            continue
        if Path(group[0]).name == "fish":
            group = group[1:]
            if group and group[0] == "--no-config":
                group = group[1:]
        if not group:
            continue
        path = group[0].removeprefix("./")
        if "/skills/mtg-rules/scripts/" in path or path.startswith("skills/mtg-rules/scripts/") or path.startswith("scripts/"):
            found.add(Path(path).name)
    return found


def grade(probe, events):
    available = False
    completed = False
    pending = {}
    loaded = False
    attempted = False
    scripts, docs = set(), set()
    for event in events:
        if event.get("type") == "system" and event.get("subtype") == "init":
            available = any(is_skill(s if isinstance(s, str) else s.get("name"))
                            for s in event.get("skills", []))
        if event.get("type") == "result":
            completed = (event.get("subtype") == "success"
                         and not event.get("is_error", False)
                         and bool(event.get("result")))
        message = event.get("message", {})
        content = message.get("content", [])
        if not isinstance(content, list):
            continue
        for block in content:
            if block.get("type") == "tool_use":
                name, args = block.get("name"), block.get("input", {})
                path = args.get("file_path", "").replace("\\", "/")
                skill_load = (name == "Skill" and is_skill(args.get("skill"))) or (
                    name == "Read" and (path.endswith("/skills/mtg-rules/SKILL.md")
                                        or path == "skills/mtg-rules/SKILL.md"))
                commands = script_commands(args.get("command", "")) if name == "Bash" else set()
                command_attempts = script_commands(args.get("command", ""), False) if name == "Bash" else set()
                doc = None
                if name == "Read" and ("/skills/mtg-rules/references/" in path
                                       or path.startswith("skills/mtg-rules/references/")):
                    doc = Path(path).name
                attempted |= bool(skill_load or command_attempts or doc)
                pending[block["id"]] = (skill_load, commands, doc)
            elif block.get("type") == "tool_result":
                action = pending.pop(block.get("tool_use_id"), None)
                if action and not block.get("is_error", False) and block.get("content"):
                    skill_load, commands, doc = action
                    loaded |= skill_load
                    scripts.update(commands)
                    if doc:
                        docs.add(doc)
    failures = []
    if not available:
        failures.append("INCONCLUSIVE: init event does not advertise mtg-rules")
    if not completed:
        failures.append("INCONCLUSIVE: no successful final result")
    if probe["invoke"]:
        if not loaded:
            failures.append("missing successful skill load")
        failures.extend("missing successful script: " + s for s in probe["scripts"] if s not in scripts)
        failures.extend("missing successful reference read: " + d for d in probe["docs"] if d not in docs)
    elif attempted:
        failures.append("unexpected MTG skill activity")
    return failures


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("probe")
    parser.add_argument("--answer-probe", action="store_true",
                        help="use a numbered rulings probe and its frame_docs as route expectations")
    parser.add_argument("--dry", action="store_true")
    parser.add_argument("--transcript", type=Path, help="grade saved stream-json; no model call")
    parser.add_argument("--model", default="sonnet")
    args = parser.parse_args()
    source = "probes.json" if args.answer_probe else "invocation-probes.json"
    probes = json.loads((EVALS / source).read_text())["probes"]
    if args.answer_probe:
        probes = [{**p, "invoke": True, "scripts": ["card", "rule"],
                   "docs": p["frame_docs"]} for p in probes]
    probe = next((p for p in probes if str(p["id"]) == args.probe), None)
    if probe is None:
        parser.error("unknown probe; choose " + ", ".join(str(p["id"]) for p in probes))
    if args.dry:
        print(probe["question"])
        return 0
    transcript = args.transcript
    if transcript is None:
        # An unrelated working directory excludes this repo's CLAUDE.md and answer key.
        workspace = Path(tempfile.mkdtemp(prefix="mtg-invocation-"))
        transcript = workspace / "trace.jsonl"
        command = ["claude", "-p", probe["question"], "--model", args.model,
                   "--plugin-dir", str(PLUGIN), "--output-format", "stream-json",
                   "--verbose", "--no-session-persistence", "--permission-mode", "dontAsk",
                   "--add-dir", str(PLUGIN / "skills/mtg-rules"), "--tools", "Skill,Read,Bash",
                   "--disallowedTools", "Edit,Write", "--allowedTools", "Skill", "Read"]
        for script in ("lookup", "rule", "rule-search", "define", "keyword", "card",
                       "rulings", "mtr", "corpus", "classify", "underdetermined"):
            command.append(f"Bash({PLUGIN / 'skills/mtg-rules/scripts' / script} *)")
        print(f"Running one paid probe; transcript: {transcript}", flush=True)
        with transcript.open("w") as output, (workspace / "stderr.txt").open("w") as error:
            result = subprocess.run(command, cwd=workspace, stdout=output, stderr=error, check=False)
        if result.returncode:
            print(f"INCONCLUSIVE: claude exited {result.returncode}; see {workspace / 'stderr.txt'}")
            return 2
    try:
        events = [json.loads(line) for line in transcript.read_text().splitlines() if line.strip()]
        if any(not isinstance(event, dict) for event in events):
            raise ValueError("stream events must be objects")
        failures = grade(probe, events)
    except (OSError, ValueError, TypeError, KeyError, AttributeError) as error:
        print(f"INCONCLUSIVE: invalid transcript: {error}")
        return 2
    print(f"{'FAIL' if failures else 'PASS'}: {probe['id']}")
    for failure in failures:
        print("  " + failure)
    return int(bool(failures))


if __name__ == "__main__":
    raise SystemExit(main())
