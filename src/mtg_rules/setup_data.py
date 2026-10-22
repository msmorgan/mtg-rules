"""Fetch and validate plugin data with Python's standard library.

Stage downloads before promotion. Retain the last distinct CR edition so cite
can compare against a locked baseline without depending on an upstream URL.
"""

import argparse
import contextlib
import json
import lzma
import os
import shutil
import sqlite3
import sys
import tempfile
import time
import urllib.request
from pathlib import Path

from .cite import Snapshot, effective_date

RULES = {"link/cr": "cr.txt", "cr": "cr.json", "cr/keywords": "keywords.json",
         "cr/glossary": "glossary.json", "cr/unofficial-glossary": "unofficial-glossary.json", "mtr": "mtr.json"}
CATALOGS = ["card-names", "artist-names", "word-bank", "supertypes", "card-types", "artifact-types", "battle-types", "creature-types", "enchantment-types", "land-types", "planeswalker-types", "spell-types", "powers", "toughnesses", "loyalties", "keyword-abilities", "keyword-actions", "ability-words", "flavor-words", "watermarks"]
CARD_FIELDS = ["name", "side", "layout", "manaCost", "manaValue", "type", "types", "supertypes", "subtypes", "text", "power", "toughness", "loyalty", "defense", "colors", "colorIdentity"]


def default_destination(skill: Path) -> Path:
    for key in ("MTG_RULES_DATA", "PLUGIN_DATA", "CLAUDE_PLUGIN_DATA"):
        if os.environ.get(key):
            return Path(os.environ[key])
    home = Path.home()
    codex = Path(os.environ.get("CODEX_HOME") or home / ".codex")
    opencode = Path(os.environ.get("XDG_DATA_HOME") or home / ".local/share") / "opencode"
    for host, data in ((codex, codex / "plugins/data/mtg-rules/data"),
                       (home / ".gemini", home / ".gemini/config/plugins/mtg-rules/data"),
                       (home / ".claude", home / ".claude/plugins/data/mtg-rules/data"),
                       (opencode, opencode / "plugins/data/mtg-rules/data"),
                       (home / ".config/opencode", opencode / "plugins/data/mtg-rules/data")):
        if skill.is_relative_to(host):
            return data
    return skill.parents[1] / "data"


def download(url: str, target: Path, *, compressed=False) -> None:
    """Stream large downloads; publish only after the transfer/decode succeeds."""
    target.parent.mkdir(parents=True, exist_ok=True)
    print(f"setup-data: fetching {url}", file=sys.stderr)
    for attempt in range(3):
        temp = None
        try:
            with tempfile.NamedTemporaryFile(dir=target.parent, delete=False) as stream:
                temp = Path(stream.name)
                with urllib.request.urlopen(url, timeout=60) as response:
                    if compressed:
                        with lzma.LZMAFile(response) as decoded:
                            shutil.copyfileobj(decoded, stream)
                    else:
                        shutil.copyfileobj(response, stream)
            os.replace(temp, target)
            return
        except (OSError, EOFError, lzma.LZMAError):
            if temp is not None:
                temp.unlink(missing_ok=True)
            if attempt == 2:
                raise
            time.sleep(attempt + 1)


def normalize_glossary(value: dict) -> dict:
    if not isinstance(value, dict):
        raise ValueError("setup-data: glossary must be an object")
    envelope = value.get("glossary")
    definition = envelope.get("definition") if isinstance(envelope, dict) else None
    if isinstance(definition, str):
        value = {}
        for entry in definition.split("\u00a0\n"):
            if entry:
                lines = entry.split("\n")
                term = lines[0]
                key = term.translate(str.maketrans("ABCDEFGHIJKLMNOPQRSTUVWXYZ", "abcdefghijklmnopqrstuvwxyz"))
                value[key] = dict(term=term, definition="\n".join(lines[1:]).rstrip("\n"))
    if not value or "glossary" in value or any(not isinstance(v, dict) or
            not isinstance(v.get("term"), str) or not isinstance(v.get("definition"), str) for v in value.values()):
        raise ValueError("setup-data: normalized glossary failed validation")
    return value


def promote_rules(stage: Path, rules: Path) -> None:
    """Validate the pair, then preserve the old edition on a date transition.

    Re-fetching the same edition must not overwrite the useful previous one.
    Incomplete downloads never reach this function.
    """
    incoming = Snapshot(stage)
    rules.mkdir(parents=True, exist_ok=True)
    old_json, old_txt = rules / "cr.json", rules / "cr.txt"
    if old_json.is_file() and old_txt.is_file():
        previous = Snapshot(rules)
        if previous.date != incoming.date:
            saved = rules / "previous"
            saved.mkdir(exist_ok=True)
            for name in ("cr.json", "cr.txt"):
                shutil.copyfile(rules / name, saved / (name + ".tmp"))
            for name in ("cr.json", "cr.txt"):
                os.replace(saved / (name + ".tmp"), saved / name)
    for path in stage.iterdir():
        if path.is_file():
            os.replace(path, rules / path.name)


def build_cards(source: Path, target: Path) -> None:
    data = json.loads(source.read_text(encoding="utf-8"))["data"]
    target.parent.mkdir(parents=True, exist_ok=True)
    with target.open("w", encoding="utf-8") as stream:
        for faces in data.values():
            for face in faces:
                record = {key: face.get(key) for key in CARD_FIELDS}
                record["face"] = face.get("faceName")
                record["supported"] = face.get("legalities", {}).get("vintage", "Banned") != "Banned" and face.get("layout") != "reversible_card"
                stream.write(json.dumps(record, ensure_ascii=False) + "\n")


def setup(dest: Path, *, runtime=False, cards=False, rulings=False) -> None:
    dest.mkdir(parents=True, exist_ok=True)
    print(f"setup-data: destination {dest}", file=sys.stderr)
    with tempfile.TemporaryDirectory(prefix=".setup-", dir=dest) as staging:
        stage = Path(staging)
        for endpoint, filename in RULES.items():
            download(f"https://api.academyruins.com/{endpoint}", stage / "rules" / filename)
        # Validate every JSON payload before promoting any part of the refresh.
        for path in (stage / "rules").glob("*.json"):
            value = json.loads(path.read_text(encoding="utf-8"))
            if path.name == "glossary.json":
                path.write_text(json.dumps(normalize_glossary(value), ensure_ascii=False) + "\n", encoding="utf-8")
        effective_date((stage / "rules/cr.txt").read_text(encoding="utf-8"))
        for catalog in CATALOGS:
            target = stage / f"catalogs/{catalog}.json"
            download(f"https://api.scryfall.com/catalog/{catalog}", target)
            json.loads(target.read_text(encoding="utf-8"))
            time.sleep(0.1)
        if runtime or cards or rulings:
            database = stage / "mtgjson/AllPrintings.sqlite"
            download("https://mtgjson.com/api/v5/AllPrintings.sqlite.xz", database, compressed=True)
            with contextlib.closing(sqlite3.connect(f"{database.as_uri()}?mode=ro", uri=True)) as db:
                db.execute("SELECT 1 FROM cards LIMIT 1").fetchone()
        if cards:
            atomic = stage / "mtgjson/AtomicCards.json"
            download("https://mtgjson.com/api/v5/AtomicCards.json.xz", atomic, compressed=True)
            build_cards(atomic, stage / "derived/cards.jsonl")
        promote_rules(stage / "rules", dest / "rules")
        for tier in ("catalogs", "mtgjson", "derived"):
            if (stage / tier).is_dir():
                (dest / tier).mkdir(exist_ok=True)
                for path in (stage / tier).iterdir():
                    os.replace(path, dest / tier / path.name)
    print(f"setup-data: done. Data in {dest}", file=sys.stderr)


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(prog="setup-data", description="Fetch base rules and catalogs; retain the previous CR edition locally.")
    parser.add_argument("--dest", type=Path)
    parser.add_argument("--runtime", action="store_true", help="fetch base + AllPrintings.sqlite for automatic hooks")
    parser.add_argument("--cards", action="store_true", help="fetch AllPrintings.sqlite + AtomicCards.json and build cards.jsonl")
    parser.add_argument("--rulings", action="store_true", help="fetch AllPrintings.sqlite for official rulings")
    args = parser.parse_args(argv)
    dest = args.dest or default_destination(Path(__file__).resolve().parents[2] / "skills/mtg-rules")
    try:
        setup(dest.resolve(), runtime=args.runtime, cards=args.cards, rulings=args.rulings)
    except (OSError, ValueError, sqlite3.Error, lzma.LZMAError, EOFError) as error:
        print(f"setup-data: {error}", file=sys.stderr)
        return 1
    return 0
