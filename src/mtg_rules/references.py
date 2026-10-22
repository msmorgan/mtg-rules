"""Heading-aware reference maps and source-citation navigation."""

import re
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path

from .cite import Repository, Snapshot

NUMBER = re.compile(r"^([0-9]+(?:\.[0-9]+)*)[.:)]?\s+")
PROSE_RANGE = re.compile(r"(?<![0-9A-Za-z])([1-9][0-9]{2}\.[0-9]+[a-z]?) *[–—-] *([1-9][0-9]{2}\.[0-9]+[a-z]?|[a-z])(?![0-9A-Za-z])")
USAGE = """usage: ref                      list the reference docs
       ref <doc>                list a doc's sections
       ref <doc> <n|heading>    print one section (number, or heading text)
       ref --cites <rule>       sections citing a rule (603 | 603.7 | 603.7e)
       ref --grep <regex>       sections with matching lines (case-insensitive)"""


def rule_pattern(number: str, *, sections=False) -> re.Pattern:
    if re.fullmatch(r"[0-9]{3}", number):
        suffix = r"(?:\.|$)" if sections else r"\."
    elif re.fullmatch(r"[0-9]{3}\.[0-9]+", number):
        suffix = r"[a-z]*$"
    elif re.fullmatch(r"[0-9]{3}\.[0-9]+[a-z]+", number):
        suffix = "$"
    else:
        raise ValueError(f"'{number}' does not look like a CR rule number")
    return re.compile("^" + re.escape(number) + suffix)


def doc_date(lines: list[str]) -> str | None:
    match = re.search(r"effective ([0-9]{4}-[0-9]{2}-[0-9]{2})", "\n".join(lines[:30]))
    return match[1] if match else None


def rule_key(rule: str) -> tuple[int, int, int, str]:
    match = re.fullmatch(r"([0-9]+)\.([0-9]+)([a-z]*)", rule)
    if not match:
        raise ValueError(f"invalid rule: {rule}")
    return int(match[1]), int(match[2]), len(match[3]), match[3]


@dataclass
class Heading:
    start: int
    end: int
    level: int
    text: str
    number: str | None


@dataclass
class Report:
    doc: str
    heading: str
    count: int

    def render(self):
        return f"[map] {self.doc} §{self.heading} ({self.count} {'line' if self.count == 1 else 'lines'})"

    def label(self):
        match = NUMBER.match(self.heading)
        return match[1] if match else self.heading


class Document:
    def __init__(self, path: Path):
        self.path = path
        self.name = path.stem
        self.lines = path.read_text(encoding="utf-8").splitlines()
        self.date = doc_date(self.lines)
        self.headings = []
        fence = False
        for n, line in enumerate(self.lines, 1):
            if re.match(r"^\s*(```|~~~)", line):
                fence = not fence
            match = re.match(r"^(#{1,6})[ \t]+([^ \t].*)$", line)
            if match and not fence:
                level = len(match[1])
                text = re.sub(r"[ \t]+#+$", "", match[2].strip())
                number = NUMBER.match(text)
                self.headings.append(Heading(n, len(self.lines), level, text, number[1] if number else None))
        for n, heading in enumerate(self.headings):
            for following in self.headings[n + 1:]:
                if following.level <= heading.level:
                    heading.end = following.start - 1
                    break

    def report(self, hits: set[int]) -> list[Report]:
        counts = Counter()
        position = -1
        for n in sorted(hits):
            while position + 1 < len(self.headings) and self.headings[position + 1].start <= n:
                position += 1
            counts[position] += 1
        # Stable order: densest first, then document order (pre-heading last).
        order = sorted(counts, key=lambda i: (-counts[i], i if i >= 0 else len(self.headings)))
        return [Report(self.name, self.headings[i].text if i >= 0 and self.headings[i].level > 1 else "(header)", counts[i]) for i in order]

    def section_lines(self) -> list[str]:
        return [f"{'  ' * (h.level - 1)}§{h.text} ({h.end - h.start + 1} lines)" for h in self.headings if 2 <= h.level <= 3]

    def select(self, wanted: str) -> list[Heading]:
        wanted = wanted.removeprefix("§").strip()
        headings = [h for h in self.headings if h.level >= 2]
        if re.fullmatch(r"[0-9]+(?:\.[0-9]+)*\.?", wanted):
            exact = [h for h in headings if h.number == wanted.removesuffix(".")]
            if exact:
                return exact
        wanted = wanted.lower()
        for predicate in (lambda h: h.text.lower() == wanted,
                          lambda h: NUMBER.sub("", h.text.lower()) == wanted,
                          lambda h: wanted in h.text.lower()):
            matches = [h for h in headings if predicate(h)]
            if matches:
                return matches
        return []


class Maps:
    def __init__(self, skill: Path):
        self.skill = skill
        self.docs = [Document(p) for p in sorted((skill / "references").glob("*.md"))]

    def find(self, name: str) -> Document:
        name = Path(name.removesuffix(".md")).name
        exact = [d for d in self.docs if d.name == name]
        found = exact or [d for d in self.docs if d.name.startswith(name)]
        if len(found) != 1:
            raise ValueError(f"ref: no reference doc '{name}'.\n{USAGE}")
        return found[0]

    def grep(self, pattern: re.Pattern) -> list[Report]:
        return [r for d in self.docs for r in d.report({n for n, line in enumerate(d.lines, 1) if pattern.search(line)})]

    def cites(self, number: str, data: Path) -> list[Report]:
        pattern = rule_pattern(number, sections=True)
        snapshot = Snapshot(data / "rules")
        groups = defaultdict(set)
        for site in Repository(self.skill / "cite-config.json").sites(snapshot):
            if site["status"] == "ok" and re.fullmatch(r"references/[^/]+\.md", site["file"]) and any(pattern.search(m) for m in site["members"]):
                groups[Path(site["file"]).stem].add(site["line"])
        queries = [rule_key(rule) for rule in snapshot.order if pattern.search(rule)]
        for doc in self.docs:
            for n, line in enumerate(doc.lines, 1):
                for match in PROSE_RANGE.finditer(line):
                    start, end = match.groups()
                    if len(end) == 1:
                        if not start[-1].isalpha():
                            continue
                        end = re.sub(r"[a-z]+$", "", start) + end
                    lo, hi = rule_key(start), rule_key(end)
                    if not hi[3]:
                        hi = hi[0], hi[1], 1000, ""
                    if any(lo <= q <= hi for q in queries):
                        groups[doc.name].add(n)
        return [r for doc in self.docs for r in doc.report(groups[doc.name])]
