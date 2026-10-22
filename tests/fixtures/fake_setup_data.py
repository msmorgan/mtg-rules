#!/usr/bin/env python3
"""Deterministic offline runtime provisioner for bootstrap tests."""
import argparse
import json
import os
import sqlite3
import sys
import time
from pathlib import Path

parser = argparse.ArgumentParser()
parser.add_argument('--dest', type=Path, required=True)
parser.add_argument('--runtime', action='store_true', required=True)
args = parser.parse_args()
if 'MTG_RULES_FAKE_SETUP_FAIL' in os.environ:
    print('fake setup failure', file=sys.stderr)
    raise SystemExit(1)
if delay := os.environ.get('MTG_RULES_FAKE_SETUP_DELAY'):
    time.sleep(float(delay))
if name := os.environ.get('MTG_RULES_FAKE_SETUP_COUNT'):
    counter = Path(name)
    count = int(counter.read_text()) if counter.is_file() else 0
    counter.write_text(str(count + 1) + '\n')
for tier in ('rules', 'catalogs', 'mtgjson'):
    (args.dest / tier).mkdir(parents=True, exist_ok=True)
(args.dest / 'rules/cr.txt').write_text('Magic: The Gathering Comprehensive Rules\n\nThese rules are effective as of April 17, 2026.\n\n100. General\n100.1. Fixture rule text.\n')
(args.dest / 'rules/cr.json').write_text(json.dumps({'100.1': {'ruleNumber': '100.1', 'ruleText': 'Fixture rule text.', 'examples': None}}))
for file in ('keywords.json', 'unofficial-glossary.json', 'mtr.json'):
    (args.dest / 'rules' / file).write_text('{}')
(args.dest / 'rules/glossary.json').write_text('{"fixture":{"term":"Fixture","definition":"Fixture glossary entry."}}')
for catalog in ['card-names', 'artist-names', 'word-bank', 'supertypes', 'card-types', 'artifact-types', 'battle-types', 'creature-types', 'enchantment-types', 'land-types', 'planeswalker-types', 'spell-types', 'powers', 'toughnesses', 'loyalties', 'keyword-abilities', 'keyword-actions', 'ability-words', 'flavor-words', 'watermarks']:
    (args.dest / 'catalogs' / (catalog + '.json')).write_text('{"object":"catalog","data":[]}')
with sqlite3.connect(args.dest / 'mtgjson/AllPrintings.sqlite') as db:
    db.execute('CREATE TABLE cards(name TEXT, faceName TEXT, layout TEXT, manaCost TEXT, type TEXT, text TEXT, power TEXT, toughness TEXT, loyalty TEXT, defense TEXT, side TEXT)')
    db.execute('INSERT INTO cards VALUES (?, NULL, ?, ?, ?, ?, NULL, NULL, NULL, NULL, NULL)', ('Lightning Bolt', 'normal', '{R}', 'Instant', 'Lightning Bolt deals 3 damage to any target.'))
