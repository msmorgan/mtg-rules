"""Persistent runtime provisioning with serialized, recoverable startup."""

import argparse
import contextlib
import json
import os
import sqlite3
import subprocess
import sys
import tempfile
import time
from pathlib import Path

from .setup_data import (
    CATALOGS,
    RULES,
    default_destination,
    normalize_glossary,
    promote_rules,
    setup,
)

ABI = '2'
MARKER = '.mtg-rules-runtime-v2'
LOCK = '.mtg-rules-runtime.lock'
RUNTIME_FILES = [*(f'rules/{name}' for name in RULES.values()),
                 *(f'catalogs/{name}.json' for name in CATALOGS), 'mtgjson/AllPrintings.sqlite']


def ready(dest: Path) -> bool:
    try:
        return (dest / MARKER).read_text().strip() == ABI and all((dest / name).stat().st_size > 0 for name in RUNTIME_FILES)
    except OSError:
        return False


def validate(dest: Path) -> None:
    for name in RUNTIME_FILES:
        path = dest / name
        if not path.is_file() or not path.stat().st_size:
            raise ValueError(f'ensure-data: staged runtime missing {name}')
        if path.suffix == '.json':
            value = json.loads(path.read_text(encoding='utf-8'))
            if path.name == 'glossary.json' and ('glossary' in value or normalize_glossary(value) != value):
                raise ValueError('ensure-data: staged glossary is not normalized')
    database = dest / 'mtgjson/AllPrintings.sqlite'
    with contextlib.closing(sqlite3.connect(f'{database.resolve().as_uri()}?mode=ro', uri=True)) as db:
        db.execute('SELECT 1 FROM cards LIMIT 1').fetchone()


def owner_alive(owner: str) -> bool:
    if not owner.isascii() or not owner.isdigit() or int(owner) <= 0:
        return False
    try:
        os.kill(int(owner), 0)
        return True
    except (ProcessLookupError, OverflowError):
        return False
    except PermissionError:
        return True


def lock_owner(lock: Path) -> str:
    try:
        return (lock / 'pid').read_text().strip()
    except OSError:
        return ''


def remove_lock(lock: Path, expected: str) -> None:
    # A changed owner means somebody else won recovery. Leave their lock alone.
    if lock_owner(lock) != expected:
        return
    with contextlib.suppress(FileNotFoundError):
        (lock / 'pid').unlink(missing_ok=True)
        lock.rmdir()


def ensure(dest: Path, *, timeout=580, interval=1.0) -> None:
    if ready(dest):
        return
    dest.mkdir(parents=True, exist_ok=True)
    lock = dest / LOCK
    deadline = time.monotonic() + timeout
    orphan_ticks = 0
    owned = False
    mine = str(os.getpid())
    try:
        while time.monotonic() < deadline:
            if ready(dest):
                return
            try:
                lock.mkdir()
                owned = True
                (lock / 'pid').write_text(mine)
                break
            except FileExistsError:
                owner = lock_owner(lock)
                if owner.isascii() and owner.isdigit() and int(owner) > 0:
                    orphan_ticks = 0
                    if not owner_alive(owner):
                        remove_lock(lock, owner)
                        continue
                else:
                    orphan_ticks += 1
                    if orphan_ticks >= 3:
                        remove_lock(lock, owner)
                        orphan_ticks = 0
                        continue
                time.sleep(interval)
        if not owned:
            raise ValueError(f'ensure-data: timed out waiting for {lock}')
        if ready(dest):
            return
        print(f'ensure-data: preparing MTG rules and SQLite card data in {dest}', file=sys.stderr)
        with tempfile.TemporaryDirectory(prefix='.mtg-rules-runtime.', dir=dest) as staging:
            stage = Path(staging)
            if override := os.environ.get('MTG_RULES_SETUP_DATA'):
                # Explicit injectable setup executable, used by offline fixtures.
                subprocess.run([override, '--dest', str(stage), '--runtime'], check=True)
            else:
                setup(stage, runtime=True)
            validate(stage)
            # Invalidate any old readiness marker before the first promotion.
            # The final marker is the publication boundary for other sessions.
            (dest / MARKER).unlink(missing_ok=True)
            promote_rules(stage / 'rules', dest / 'rules')
            for tier in ('catalogs', 'mtgjson'):
                (dest / tier).mkdir(exist_ok=True)
                for path in (stage / tier).iterdir():
                    os.replace(path, dest / tier / path.name)
            marker = dest / f'{MARKER}.tmp.{mine}'
            try:
                marker.write_text(ABI + '\n')
                os.replace(marker, dest / MARKER)
            finally:
                marker.unlink(missing_ok=True)
        print('ensure-data: runtime ready', file=sys.stderr)
    finally:
        if owned:
            remove_lock(lock, mine)


def main(argv=None):
    parser = argparse.ArgumentParser(prog='ensure-data')
    parser.add_argument('--dest', type=Path)
    args = parser.parse_args(argv)
    skill = Path(__file__).resolve().parents[2] / 'skills/mtg-rules'
    try:
        ensure((args.dest or default_destination(skill)).resolve())
    except (OSError, ValueError, sqlite3.Error, subprocess.SubprocessError) as error:
        print(f'ensure-data: {error}; retry with {skill}/scripts/setup-data --runtime', file=sys.stderr)
        return 1
    return 0
