"""Read-only, parameterized card and official-ruling queries."""

import contextlib
import sqlite3
from pathlib import Path


@contextlib.contextmanager
def database(data: Path):
    path = data / "mtgjson/AllPrintings.sqlite"
    if not path.is_file():
        raise ValueError(f"card database missing: {path}; run scripts/setup-data --runtime")
    with contextlib.closing(sqlite3.connect(f"{path.resolve().as_uri()}?mode=ro", uri=True)) as db:
        db.row_factory = sqlite3.Row
        yield db


def card_text(data: Path, name: str, *, full_name=False) -> str:
    with database(data) as db:
        face = "" if full_name else " OR faceName = ? COLLATE NOCASE"
        columns = ['name', 'faceName', 'layout', 'manaCost', 'type', 'text', 'power', 'toughness', 'loyalty', 'defense', 'side']
        rows = db.execute("SELECT DISTINCT " + ", ".join(f"NULLIF({c}, '') AS {c}" for c in columns) +
                          " FROM cards WHERE name = ? COLLATE NOCASE" + face +
                          " ORDER BY CASE side WHEN 'a' THEN 0 WHEN 'b' THEN 1 ELSE 2 END, faceName",
                          (name,) if full_name else (name, name)).fetchall()
        if not rows:
            near = db.execute("SELECT DISTINCT name FROM cards WHERE instr(lower(name), lower(?)) > 0 ORDER BY name LIMIT 8", (name,)).fetchall()
            if near:
                raise ValueError(f"card: no exact match for '{name}'. Did you mean: " + ", ".join(r[0] for r in near))
            raise ValueError(f"card: no card named '{name}'")
    lines = []
    for row in rows:
        title = f"# {row['name']}"
        if row['faceName'] and row['faceName'] != row['name']:
            title += f"  (face: {row['faceName']}, {row['layout'] or '?'})"
        lines += [title, f"{row['manaCost'] or '(no mana cost)'}  {row['type'] or 'null'}", row['text'] or '(no rules text)']
        if row['power'] is not None:
            lines.append(f"P/T: {row['power']}/{row['toughness']}")
        for field in ('loyalty', 'defense'):
            if row[field] is not None:
                lines.append(f"{field.title()}: {row[field]}")
        lines.append('')
    return '\n'.join(lines) + '\n'


def ruling_text(data: Path, name: str) -> tuple[str, bool]:
    with database(data) as db:
        prefix = "SELECT DISTINCT c.name FROM cards c JOIN cardRulings r ON r.uuid = c.uuid WHERE "
        names = db.execute(prefix + "c.name = ? COLLATE NOCASE ORDER BY c.name", (name,)).fetchall()
        face = not names
        if not names:
            names = db.execute(prefix + "c.faceName = ? COLLATE NOCASE ORDER BY c.name", (name,)).fetchall()
        if not names:
            raise ValueError(f"rulings: no rulings found for '{name}' (check the exact name with scripts/card; the card may have none)")
        lines = []
        for row in names:
            lines.append(f"# {row[0]}")
            records = db.execute("SELECT DISTINCT r.date, r.text FROM cards c JOIN cardRulings r ON r.uuid = c.uuid WHERE c.name = ? ORDER BY r.date", (row[0],)).fetchall()
            lines.extend(f"[{r[0]}]  {r[1]}" for r in records)
    return '\n'.join(lines) + '\n', face
