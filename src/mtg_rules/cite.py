"""CR citation resolution, locking and review reports.

Checksums establish existence and text stability, never semantic support.
The executable in the skill is a thin bootstrap; this module is testable without
an agent host or third-party Python packages.
"""

from __future__ import annotations

import argparse
import fnmatch
import hashlib
import json
import os
import re
import subprocess
import sys
import textwrap
import urllib.error
import urllib.request
from pathlib import Path

from .data import discover_data
from .exemptions import exempt_lines

BRACKETED = re.compile(r"\[CR#([^\]]*)\]")
BARE = re.compile(r"\b[1-9][0-9]{2}\.[0-9]+[a-z]?\b")
RULE = re.compile(r"[0-9]{1,3}(?:\.[0-9]+[a-z]*)?\Z")
NONCOMPLIANT = [re.compile(p) for p in (
    r"CR ?[0-9]{1,3}(\.[0-9]+[a-z]*)?",
    r"(?<![\w-])rule [0-9]{1,3}(\.[0-9]+[a-z]*)?",
    r"\b[0-9]{3}\.[0-9]+[a-z]*\b",
)]


def normalize(text: str) -> str:
    return " ".join(text.split())


def checksum(text: str) -> str:
    return hashlib.sha256(normalize(text).encode()).hexdigest()[:16]


def effective_date(text: str) -> str:
    match = re.search(r"effective as of ([A-Z][a-z]+) ([0-9]+), ([0-9]+)", text)
    if not match:
        raise ValueError("cite: cannot parse the effective date from cr.txt")
    months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
    month, day, year = match.groups()
    if month not in months:
        raise ValueError(f"cite: unknown month in effective date: {month}")
    return f"{int(year):04d}-{months.index(month) + 1:02d}-{int(day):02d}"


def parse_rule_text(text: str) -> tuple[dict[str, str], list[str]]:
    """Read document order and full bodies, excluding illustrative examples."""
    texts, order = {}, []
    target = None
    for line in text.splitlines():
        match = re.match(r"^([0-9]{1,3}(?:\.[0-9]+[a-z]*)?)\.? (.+)$", line)
        if match:
            target, body = match.groups()
            if "." in target and target not in texts:
                order.append(target)
            texts[target] = normalize(body)
        elif line[:1].isspace() and normalize(line) and not line.strip().startswith("Example:") and target:
            texts[target] += " " + normalize(line)
        else:
            target = None
    return texts, order


class Snapshot:
    def __init__(self, rules_dir: Path):
        rules = json.loads((rules_dir / "cr.json").read_text(encoding="utf-8"))
        text = (rules_dir / "cr.txt").read_text(encoding="utf-8")
        self.date = effective_date(text)
        self.texts = {m[1]: m[2] for m in re.finditer(r"^([0-9]{1,3})\. (.*)$", text, re.M)}
        self.texts.update({key: value["ruleText"] for key, value in rules.items()})
        self.order = list(parse_rule_text(text)[1])
        if not self.order:
            raise ValueError("cite: no numbered rules found in cr.txt")
        self.index = {key: n for n, key in enumerate(self.order)}

    def resolve(self, raw: str) -> tuple[str, list[str]]:
        if re.fullmatch(r"\s*(?:\.{3}|…)\s*", raw):
            return "placeholder", []
        parts = [part.split("..") for part in raw.split(",")]
        if any(len(part) not in (1, 2) or any(not RULE.fullmatch(x) for x in part) for part in parts):
            return "skip", []
        members = []
        for part in parts:
            if len(part) == 1:
                members += part
            else:
                a, b = (self.index.get(x) for x in part)
                if a is None or b is None or a > b:
                    return "gone", []
                members.extend(self.order[a:b + 1])
        return "ok", members


def scan(text: str, file: str, fmt: str, snapshot: Snapshot) -> list[dict]:
    sites = []
    if fmt == "bracketed" and "[CR#" not in text:
        return sites
    pattern = BRACKETED if fmt == "bracketed" else BARE
    for n, line in enumerate(text.splitlines(), 1):
        if fmt == "bracketed" and "[CR#" not in line:
            continue
        for match in pattern.finditer(line):
            raw = match[1] if fmt == "bracketed" else match[0]
            status, members = snapshot.resolve(raw)
            sites.append(dict(file=file, line=n, ctx=line.strip(), raw=raw, status=status, members=members))
    return sites


def noncompliant_hits(text: str) -> list[tuple[int, str, str]]:
    hits = []
    exempt = exempt_lines(text)
    for n, line in enumerate(text.splitlines(), 1):
        if n in exempt:
            continue
        blanked = BRACKETED.sub("§", line)
        matches = {}
        for pattern in NONCOMPLIANT:
            for match in pattern.finditer(blanked):
                matches.setdefault(match.start(), match[0])
        hits.extend((n, matches[offset], line.strip()) for offset in sorted(matches))
    return hits


def tracked_files(root: Path) -> list[str]:
    """Prefer jj; retain support for consumers that use Git without jj."""
    for command in (["jj", "--no-pager", "file", "list"], ["git", "ls-files"]):
        try:
            result = subprocess.run(command, cwd=root, capture_output=True, text=True, check=False)
        except FileNotFoundError:
            continue
        if result.returncode == 0 and result.stdout.strip():
            return result.stdout.splitlines()
    raise ValueError(f"cite: no tracked files (neither jj nor git answered in {root})")


class Repository:
    def __init__(self, config_path: Path):
        if not config_path.is_file():
            raise ValueError(f"cite: config not readable: {config_path}")
        self.root = config_path.resolve().parent
        self.config = json.loads(config_path.read_text(encoding="utf-8"))
        self.fmt = self.config.get("format", "bracketed")
        if self.fmt not in ("bracketed", "bare"):
            raise ValueError(f"cite: bad format in config: {self.fmt}")
        self.lock_path = self.root / self.config.get("lockfile", "cr-citations.lock")

    def sources(self) -> list[Path]:
        source = self.config.get("sources", {})
        if source.get("tracked"):
            names = tracked_files(self.root)

        else:
            names = [str(p.relative_to(self.root)) for p in self.root.rglob("*")
                     if p.is_file() and not p.is_symlink() and
                     any(fnmatch.fnmatchcase(str(p.relative_to(self.root)), g) for g in source.get("globs", []))]
        files = [self.root / name for name in sorted(set(names), key=lambda name: Path(name).parts if source.get("tracked") else name)
                 if not any(name.startswith(p) for p in source.get("exclude", []))
                 and (not source.get("extensions") or Path(name).suffix[1:] in source["extensions"])
                 and (self.root / name).is_file() and not (self.root / name).is_symlink()]
        if not files:
            raise ValueError("cite: no source files matched the config")
        return files

    def sites(self, snapshot: Snapshot) -> list[dict]:
        return [site for path in self.sources() for site in
                scan(path.read_text(encoding="utf-8"), str(path).removeprefix(str(self.root) + os.sep), self.fmt, snapshot)]

    def lock(self, command: str) -> dict:
        if not self.lock_path.is_file():
            raise ValueError(f"cite {command}: lockfile missing: {self.lock_path} (run: cite bless)")
        text = self.lock_path.read_text(encoding="utf-8")
        if not text.startswith("{"):
            raise ValueError(f"cite {command}: {self.lock_path} is not JSON (legacy TOML lock?) — regenerate with: cite bless")
        return json.loads(text)

    def relative_argument(self, arg: str) -> str:
        path = Path(arg)
        return str(path.relative_to(self.root)) if path.is_absolute() and path.is_relative_to(self.root) else arg


def hashes(sites: list[dict], snapshot: Snapshot) -> dict[str, str]:
    members = {member for site in sites if site["status"] == "ok" for member in site["members"]}
    return {member: checksum(snapshot.texts[member]) for member in members if member in snapshot.texts}


def stale(sites: list[dict], current: dict, locked: dict) -> list[str]:
    result = []
    for site in sites:
        status = site["status"]
        if status == "placeholder":
            continue
        items = [("MALFORMED" if status == "skip" else "GONE", site["raw"])] if status != "ok" else [
            ("GONE" if member not in current else "UNLOCKED" if member not in locked else
             "CHANGED" if current[member] != locked[member] else "", member) for member in site["members"]]
        result.extend(f"{tag}  {rule}  {site['file']}:{site['line']}  {site['ctx']}" for tag, rule in items if tag)
    return result


def token(site: dict, fmt: str) -> str:
    return f"[CR#{site['raw']}]" if fmt == "bracketed" else site["raw"]


def added_diff_lines(text: str) -> set[tuple[str, int]]:
    added = set()
    file, n = "", 0
    for line in text.splitlines():
        if line.startswith("+++ "):
            file = line[4:].split("\t", 1)[0].removeprefix("b/")
        elif match := re.match(r"@@ .*?\+(\d+)(?:,\d+)? @@", line):
            n = int(match[1]) - 1
        elif line.startswith("+"):
            n += 1
            if file and file != "/dev/null":
                added.add((file, n))
        elif line.startswith(" "):
            n += 1
    return added


def bless(repo: Repository, snapshot: Snapshot, sites: list[dict]) -> int:
    current = hashes(sites, snapshot)
    old = {}
    if repo.lock_path.is_file():
        text = repo.lock_path.read_text(encoding="utf-8")
        try:
            old = json.loads(text)
        except json.JSONDecodeError:
            match = re.search(r'wizards_url = "([^"]*)"', text)
            old = {"wizards_url": match[1] if match else ""}
    url = os.environ.get("MTG_RULES_CITE_WIZARDS_URL", "")
    if "MTG_RULES_CITE_WIZARDS_URL" not in os.environ:
        try:
            with urllib.request.urlopen(urllib.request.Request("https://academyruins.com/link/cr", method="HEAD"), timeout=15) as response:
                url = response.url
        except (OSError, urllib.error.URLError):
            pass
    url = url or old.get("wizards_url")
    if not url:
        raise ValueError("cite bless: cannot resolve the wizards URL (offline?) and no existing lock to reuse")
    new = sorted(current.keys() - old.get("checksums", {}).keys())
    if repo.lock_path.is_file() and new:
        print("newly registered rule(s) — eyeball each against its citing claim:")
        for rule in new:
            print(f"  {rule}: {snapshot.texts[rule][:110]}")
    repo.lock_path.write_text(json.dumps(dict(cr_date=snapshot.date, wizards_url=url, checksums=current),
                                         indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"blessed {len(current)} rules at cr_date {snapshot.date} -> {repo.lock_path}")
    return 0


def context(repo: Repository, snapshot: Snapshot, args, *, text: str | None = None) -> int:
    if not re.fullmatch(r"[0-9]+", args.max):
        raise ValueError("cite context: --max wants a non-negative integer")
    sites = scan(sys.stdin.read() if text is None else text, "", repo.fmt, snapshot)
    batch = list(dict.fromkeys(m for s in sites if s["status"] == "ok" for m in s["members"]))
    seen_path = Path(args.seen) if args.seen else None
    seen = set(seen_path.read_text(encoding="utf-8").splitlines()) if seen_path and seen_path.is_file() else set()
    new = [m for m in batch if m not in seen]
    limit = int(args.max)
    shown = new[:limit] if limit else new
    held = len(new) - len(shown)
    if not shown:
        return 0
    try:
        known = repo.lock("context").get("checksums", {}) if repo.lock_path.is_file() else batch
    except (ValueError, OSError):
        known = {}
    print(f"mtg-rules · {len(shown)} CR citation{'s' if len(shown) != 1 else ''} referenced for the first time this session:")
    for rule in shown:
        body = normalize(snapshot.texts.get(rule, ""))
        tag = "  ·  NOT FOUND IN THE CR" if rule not in snapshot.texts else "  ·  new to this repo" if rule not in known else ""
        section = int(rule.split(".")[0])
        for span in repo.config.get("coverage", {}).get("out_of_scope", {}):
            endpoints = [int(x) for x in span.split("..")]
            if endpoints[0] <= section <= endpoints[-1]:
                tag += "  ·  out-of-scope range"
                break
        if rule in known and not args.full and len(body) > 240:
            cut = body.rfind(" ", 0, 240)
            body = body[:cut if cut > 0 else 239] + " …"
        print(f"\n[CR#{rule}]{tag}")
        if body:
            print(f"    {body}")
    if held:
        print(f"\n… {held} more first-seen citation{'s' if held != 1 else ''} not shown (cap: CITE_CONTEXT_MAX).")
    if seen_path:
        with seen_path.open("a", encoding="utf-8") as ledger:
            ledger.write("".join(rule + "\n" for rule in shown))
    return 0


def parser() -> argparse.ArgumentParser:
    result = argparse.ArgumentParser(prog="cite")
    result.add_argument("--config", type=Path, default=Path(__file__).resolve().parents[2] / "skills/mtg-rules/cite-config.json")
    commands = result.add_subparsers(dest="command")
    check = commands.add_parser("check")
    check.add_argument("--list-noncompliant", action="store_true")
    commands.add_parser("bless")
    listing = commands.add_parser("list")
    listing.add_argument("--json", action="store_true")
    show = commands.add_parser("show")
    show.add_argument("citation", nargs="?")
    show.add_argument("--plain", action="store_true")
    diff = commands.add_parser("diff")
    diff.add_argument("rule", nargs="?")
    audit = commands.add_parser("audit")
    audit.add_argument("--diff", action="store_true")
    audit.add_argument("files", nargs="*")
    ctx = commands.add_parser("context")
    ctx.add_argument("--seen")
    ctx.add_argument("--full", action="store_true")
    ctx.add_argument("--max", default="40")
    return result


def run(args) -> int:
    repo = Repository(args.config)
    skill = Path(__file__).resolve().parents[2] / "skills/mtg-rules"
    data = discover_data(skill)
    command = args.command or "check"
    if command == "check" and getattr(args, "list_noncompliant", False):
        if repo.fmt != "bracketed":
            raise ValueError("cite: --list-noncompliant applies to the bracketed format only")
        hits = []
        for path in repo.sources():
            name = path.relative_to(repo.root).as_posix()
            if any(name.endswith(suffix) for suffix in repo.config.get("noncompliant_exempt", [])):
                continue
            hits.extend(f'{name}:{n}  "{match}"  {line}' for n, match, line in noncompliant_hits(path.read_text(encoding="utf-8")))
        for hit in hits:
            print(hit)
        print(f"{len(hits)} non-compliant citation-looking string(s)")
        return int(bool(hits))
    snapshot = Snapshot(data / "rules")
    if command == "context":
        return context(repo, snapshot, args)
    if command == "show":
        if not args.citation:
            raise ValueError("cite show: missing citation argument")
        raw = args.citation.strip()
        if raw.startswith("[") and raw.endswith("]"):
            raw = raw[1:-1]
        raw = raw.removeprefix("CR#").strip()
        status, members = snapshot.resolve(raw)
        errors = {"skip": "malformed citation", "gone": "range endpoint not found", "placeholder": "not a citation, an ellipsis placeholder"}
        if status in errors:
            raise ValueError(f"cite show: {errors[status]}: {args.citation}")
        missing = 0
        try:
            width = int(os.environ.get("COLUMNS", "80"))
        except ValueError:
            width = 80
        if width <= 20:
            width = 80
        for member in members:
            text = snapshot.texts.get(member)
            if not text:
                print(f"[CR#{member}]  (not found in the CR)", file=sys.stderr)
                missing += 1
            elif args.plain:
                print(f"{member}  {text}")
            else:
                print(f"[CR#{member}]")
                print(textwrap.indent(textwrap.fill(text, width=max(21, width) - 4), "    "))
        return int(bool(missing))
    if command == "diff":
        if not args.rule:
            raise ValueError("cite diff: missing rule number")
        lock = repo.lock("diff")
        previous = data / "rules/previous"
        old_json, old_txt = previous / "cr.json", previous / "cr.txt"
        oldtext = ""
        if old_json.is_file() and old_txt.is_file() and effective_date(old_txt.read_text(encoding="utf-8")) == lock.get("cr_date"):
            oldtext = Snapshot(previous).texts.get(args.rule, "")
        else:
            url = lock.get("wizards_url")
            if not url:
                raise ValueError("cite diff: no matching previous edition and no wizards_url in the lockfile")
            with urllib.request.urlopen(url, timeout=60) as response:
                media = response.headers.get_content_type()
                old = response.read().decode("utf-8-sig")
            # A successful HTTP response can be an HTML landing page. Never
            # present that as an edition with every rule missing.
            if media not in ("text/plain", "application/octet-stream") or re.search(r"<(?:!doctype|html)\b", old, re.I):
                raise ValueError("cite diff: URL did not serve plain CR text; refresh with setup-data to retain a local previous edition")
            texts, order = parse_rule_text(old)
            if not order:
                raise ValueError("cite diff: URL contains no numbered rules")
            oldtext = texts.get(args.rule, "")
        print(f"[CR#{args.rule}]\n- {oldtext or '(absent in old version)'}\n+ {snapshot.texts.get(args.rule, '(absent in current CR)')}")
        return 0
    sites = repo.sites(snapshot)
    if command == "check":
        locked = repo.lock("check").get("checksums", {})
        report = stale(sites, hashes(sites, snapshot), locked)
        for line in report:
            print(line)
        count = sum(len(s["members"]) if s["status"] == "ok" else int(s["status"] != "placeholder") for s in sites)
        print(f"checked {count} citations against cr.json (eff. {snapshot.date}); {len(report)} stale")
        return int(bool(report))
    if command == "bless":
        return bless(repo, snapshot, sites)
    if command == "list":
        if args.json:
            print(json.dumps([dict(file=s["file"], line=s["line"], token=token(s, repo.fmt),
                                   status="malformed" if s["status"] == "skip" else s["status"],
                                   members=s["members"]) for s in sites], ensure_ascii=False))
            return 0
        for site in sites:
            if site["status"] == "ok":
                print(f"{site['file']}:{site['line']}  {token(site, repo.fmt)}  -> {', '.join(site['members'])}")
        return 0
    if args.diff:
        if sys.stdin.isatty():
            result = subprocess.run(["jj", "--no-pager", "diff", "--git"], cwd=repo.root, capture_output=True, text=True, check=True)
            diff = result.stdout
        else:
            diff = sys.stdin.read()
        selected = added_diff_lines(diff)
        sites = [s for s in sites if (s["file"], s["line"]) in selected]
    elif args.files:
        files = {repo.relative_argument(arg) for arg in args.files}
        sites = [s for s in sites if s["file"] in files]
    for site in sites:
        heading = f"{site['file']}:{site['line']}  {token(site, repo.fmt)}"
        if site["status"] != "ok":
            print(f"{heading}  !! {site['status']} — fix before auditing\n")
        else:
            print(f"{heading}\n  > {site['ctx']}")
            for member in site["members"]:
                print(f"    {member}: {snapshot.texts.get(member, '(not found)')}")
            print()
    print(f"audited {len(sites)} citation site(s) — " + ("read each rule text against its claim" if sites else "nothing selected"))
    return 0


def main(argv: list[str] | None = None) -> int:
    args = parser().parse_args(argv)
    try:
        return run(args)
    except (OSError, ValueError, subprocess.SubprocessError) as error:
        print(str(error), file=sys.stderr)
        return 1
