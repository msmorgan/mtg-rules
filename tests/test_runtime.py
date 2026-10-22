"""Runtime behavior, packaging, lifecycle and dependency-removal contracts."""

import contextlib
import io
import json
import os
import shutil
import sqlite3
import subprocess
import sys
from pathlib import Path
from unittest.mock import patch

import pytest

from mtg_rules import bootstrap, hooks
from mtg_rules.cards import card_text, database, ruling_text
from mtg_rules.cite import Repository, Snapshot, hashes
from mtg_rules.lookups import main
from mtg_rules.references import Document, Maps
from mtg_rules.setup_data import CATALOGS

ROOT = Path(__file__).resolve().parents[1]
FAKE_SETUP = ROOT / 'tests/fixtures/fake_setup_data.py'


@pytest.fixture
def plugin(tmp_path, monkeypatch):
    root = tmp_path / 'plugin with spaces'
    skill = root / 'skills/mtg-rules'
    data = root / 'data'
    shutil.copytree(ROOT / 'src', root / 'src', ignore=shutil.ignore_patterns('__pycache__'))
    shutil.copytree(ROOT / 'skills/mtg-rules/scripts', skill / 'scripts')
    shutil.copytree(ROOT / 'tests/fixtures/cite/data/rules', data / 'rules')
    (skill / 'references').mkdir()
    (skill / 'references/fixture.md').write_text('# Fixture\n\n*Synthesized from CR effective 2026-04-17.*\n\n## 1. First\nA claim per 100.1a.\n\n### 1.1 Nested\nMore about 702.22a.\n\n## 2. Second\nPriority.\n')
    (skill / 'references/underdetermined.md').write_text('# Registry\n### UD-7 — Fixture — category: open\nAn engine choice.\n\n### U3 — Retired — category: settled\nRetired.\n')
    (skill / 'cite-config.json').write_text(json.dumps({'format': 'bare', 'sources': {'globs': ['references/*.md']}}))
    records = [{'name': 'Banding', 'kind': 'ability', 'class': 'composite', 'ident': 'Banding', 'rule': '702.22', 'how': 'Fixture', 'cites': ['702.22a'], 'core_referenced': False}]
    (skill / 'keywords-classified.json').write_text(json.dumps({'keywords': records}))
    (data / 'rules/glossary.json').write_text(json.dumps({'banding': {'term': 'Banding', 'definition': 'See rule 702.22a.'}, 'city’s blessing': {'term': 'City’s Blessing', 'definition': 'A designation.'}}))
    (data / 'rules/unofficial-glossary.json').write_text(json.dumps({'fixture': {'term': 'Fixture', 'definition': 'Unofficial.'}}))
    (data / 'rules/keywords.json').write_text('{}')
    (data / 'rules/mtr.json').write_text(json.dumps({'content': [{'section': 1, 'subsection': None, 'title': 'General', 'content': 'Policy.'}, {'section': 1, 'subsection': 7, 'title': 'Judge', 'content': 'Judge policy.'}]}))
    (data / 'catalogs').mkdir()
    for name in CATALOGS:
        (data / 'catalogs' / (name + '.json')).write_text('{"data":[]}')
    (data / 'derived').mkdir()
    cards = [{'name': 'A', 'types': ['Creature'], 'text': 'Flying\nSame line', 'supported': True}, {'name': 'B', 'types': ['Creature'], 'text': 'Same line\nUn-card', 'supported': False}]
    (data / 'derived/cards.jsonl').write_text(''.join(json.dumps(c) + '\n' for c in cards))
    (data / 'mtgjson').mkdir()
    with sqlite3.connect(data / 'mtgjson/AllPrintings.sqlite') as db:
        db.execute('CREATE TABLE cards(uuid TEXT, name TEXT, faceName TEXT, layout TEXT, manaCost TEXT, type TEXT, text TEXT, power TEXT, toughness TEXT, loyalty TEXT, defense TEXT, side TEXT)')
        for row in [('a', "O'Brien // Ice", "O'Brien", 'split', '{R}', 'Instant', 'First face.', None, None, None, None, 'a'), ('b', "O'Brien // Ice", 'Ice', 'split', '{U}', 'Instant', 'Second face.', None, None, None, None, 'b')]:
            db.execute('INSERT INTO cards VALUES (?,?,?,?,?,?,?,?,?,?,?,?)', row)
            db.execute('INSERT INTO cards VALUES (?,?,?,?,?,?,?,?,?,?,?,?)', row)
        db.execute('CREATE TABLE cardRulings(uuid TEXT, date TEXT, text TEXT)')
        db.execute("INSERT INTO cardRulings VALUES ('a', '2026-01-01', 'Official ruling.')")
        db.execute("INSERT INTO cardRulings VALUES ('a', '2026-01-01', 'Official ruling.')")
    (data / bootstrap.MARKER).write_text('2\n')
    (root / '.codex-plugin').mkdir()
    (root / '.codex-plugin/plugin.json').write_text('{"version":"1.11.0"}')
    repo, snapshot = Repository(skill / 'cite-config.json'), Snapshot(data / 'rules')
    repo.lock_path.write_text(json.dumps({'cr_date': snapshot.date, 'wizards_url': 'file:///unused', 'checksums': hashes(repo.sites(snapshot), snapshot)}))
    monkeypatch.setenv('MTG_RULES_DATA', str(data))
    monkeypatch.setenv('PLUGIN_DATA', str(data))
    monkeypatch.delenv('MTG_RULES_SETUP_DATA', raising=False)
    return root, skill, data


def invoke(skill, command, *args):
    output, errors = io.StringIO(), io.StringIO()
    with contextlib.redirect_stdout(output), contextlib.redirect_stderr(errors):
        code = main(command, skill, list(args))
    return code, output.getvalue(), errors.getvalue()


def test_sqlite_names_are_bound_and_connections_are_read_only(plugin):
    _, _, data = plugin
    rendered = card_text(data, "O'Brien // Ice", full_name=True)
    assert rendered.count('# ') == 2
    assert rendered.index('First face.') < rendered.index('Second face.')
    assert card_text(data, "o'brien").count('# ') == 1
    with pytest.raises(ValueError, match='no exact match'):
        card_text(data, "O'Brien", full_name=True)
    with pytest.raises(ValueError):
        card_text(data, "' OR 1=1 --")
    text, face = ruling_text(data, "O'Brien")
    assert face and text.count('Official ruling.') == 1
    with database(data) as db, pytest.raises(sqlite3.OperationalError, match='readonly'):
        db.execute('DELETE FROM cards')


def test_glossary_corpus_and_argument_errors(plugin):
    _, skill, _ = plugin
    code, out, _ = invoke(skill, 'define', "city's blessing")
    assert code == 0 and 'City’s Blessing' in out
    assert 'unofficial' in invoke(skill, 'define', 'fixture')[1]
    assert invoke(skill, 'corpus', '--type', 'creature')[1] == 'Flying\nSame line\n'
    assert invoke(skill, 'corpus', '--all', '--match', 'Un-card')[1] == 'Un-card\n'
    assert invoke(skill, 'corpus', '--match', '[')[0] == 1
    assert invoke(skill, 'rule-search', '--max', '0', 'rule')[0] == 1
    assert invoke(skill, 'mtr', '1.7.9')[0] == 1
    assert invoke(skill, 'card', '')[0] == 1


def test_heading_boundaries_fences_and_duplicate_hits(plugin):
    _, skill, _ = plugin
    doc = Document(skill / 'references/fixture.md')
    first = doc.select('1')[0]
    assert 'Nested' in '\n'.join(doc.lines[first.start - 1:first.end])
    assert 'Second' not in '\n'.join(doc.lines[first.start - 1:first.end])
    assert doc.select('§1. First') == [first]
    report = doc.report({6, 9})
    assert [(r.heading, r.count) for r in report] == [('1. First', 1), ('1.1 Nested', 1)]
    path = skill / 'references/fences.md'
    path.write_text('# Fence\n```\n## Not real\n```\n## 1. Real\nBody\n~~~\n### Not real either\n~~~\n')
    assert [h.text for h in Document(path).headings] == ['Fence', '1. Real']
    assert Maps(skill).find('fen').name == 'fences'


def test_every_installed_entrypoint_works_without_utilities(plugin, tmp_path):
    root, skill, data = plugin
    bin_dir = tmp_path / 'only-python'
    bin_dir.mkdir()
    (bin_dir / 'python3').symlink_to(sys.executable)
    env = dict(os.environ, PATH=str(bin_dir), TMPDIR=str(tmp_path))
    commands = {
        'rule': ['100.1'], 'rule-search': ['Placeholder'], 'define': ['Banding'],
        'keyword': ['Banding'], 'mtr': ['1.7'], 'card': ["O'Brien // Ice"],
        'rulings': ["O'Brien"], 'corpus': ['--type', 'Creature'], 'lookup': ['Banding'],
        'ref': ['fixture', '1'], 'classify': ['Banding'], 'underdetermined': ['7'],
        'health': [], 'version': [], 'normalize-glossary': [str(data / 'rules/glossary.json')],
        'data-path': [], 'ensure-data': ['--dest', str(data)], 'setup-data': ['--help'],
        'cite': ['check'],
    }
    scripts = skill / 'scripts'
    assert {p.name for p in scripts.iterdir() if p.is_file()} == set(commands)
    for name, args in commands.items():
        result = subprocess.run([str(scripts / name), *args], env=env, capture_output=True, text=True, timeout=20)
        assert result.returncode == 0, (name, result.stdout, result.stderr)
    (root / '.jj').mkdir()
    (root / 'cite-config.json').write_text('{"format":"bracketed"}')
    payloads = {
        'ensure_data.py': {},
        'card_context.py': {'prompt': "[[O'Brien // Ice]]"},
        'cite_context.py': {'cwd': str(root), 'session_id': 'isolated', 'tool_name': 'Edit', 'tool_input': {'new_string': '[CR#100.1]'}},
    }
    assert {p.name for p in (scripts / 'hooks').iterdir() if p.is_file()} == set(payloads)
    for name, payload in payloads.items():
        result = subprocess.run([str(scripts / 'hooks' / name)], env=env, input=json.dumps(payload), text=True, capture_output=True, timeout=20)
        assert result.returncode == 0, (name, result.stderr)
        parsed = json.loads(result.stdout)
        if name != 'ensure_data.py':
            assert parsed.get('hookSpecificOutput'), (name, result.stdout)


def test_card_hook_protocols_and_transcript_whitespace(plugin, tmp_path):
    _, skill, _ = plugin
    payload = {'prompt': "[[O'Brien // Ice]] and [[o'brien // ice]] [[not a card]] [[Ice]]"}
    response = hooks.card_context(payload, skill)['hookSpecificOutput']
    assert response['hookEventName'] == 'UserPromptSubmit'
    assert response['additionalContext'].count('# ') == 2
    transcript = tmp_path / 'transcript'
    transcript.write_text('not json\n' + json.dumps({'type': 'USER_INPUT', 'content': 'Old prompt'}) + '\n' + json.dumps({'type': 'USER_INPUT', 'content': "[[O'Brien // Ice]]"}) + '\n')
    response = hooks.card_context({'transcriptPath': str(transcript), 'invocationNum': 1}, skill)
    assert 'First face.' in response['injectSteps'][0]['ephemeralMessage']
    assert hooks.card_context({'prompt': '[Ice]'}, skill) == {}


@pytest.mark.parametrize('kind', ['card', 'ensure'])
@pytest.mark.parametrize('payload', ['garbage', '[]', '{"prompt": 7}', '{"invocationNum":0}'])
def test_hooks_contain_bad_payloads_and_setup_failures(plugin, kind, payload):
    _, skill, _ = plugin
    with patch.object(sys, 'stdin', io.StringIO(payload)), patch('mtg_rules.hooks.ensure_main', return_value=1), contextlib.redirect_stdout(io.StringIO()) as out:
        assert hooks.main(kind, skill) == 0
    result = json.loads(out.getvalue())
    if kind == 'ensure':
        assert 'injectSteps' in result if 'invocationNum' in payload else result['continue'] is True


def offline_setup(stage, **kwargs):
    subprocess.run([sys.executable, str(FAKE_SETUP), '--dest', str(stage), '--runtime'], check=True)


def test_bootstrap_publishes_marker_last_and_uses_fast_path(tmp_path, monkeypatch):
    dest = tmp_path / 'runtime'
    monkeypatch.delenv('MTG_RULES_SETUP_DATA', raising=False)
    observed = []
    replace = os.replace

    def record(source, target):
        if Path(target).name == bootstrap.MARKER:
            assert all((dest / name).is_file() for name in bootstrap.RUNTIME_FILES)
            observed.append('marker')
        return replace(source, target)

    with patch('mtg_rules.bootstrap.setup', side_effect=offline_setup), patch('os.replace', side_effect=record):
        bootstrap.ensure(dest)
    assert observed == ['marker'] and bootstrap.ready(dest)
    assert not (dest / bootstrap.LOCK).exists()
    with patch('mtg_rules.bootstrap.setup', side_effect=AssertionError('setup on hot path')):
        bootstrap.ensure(dest)


def test_bootstrap_failure_keeps_old_data_and_cleans_private_state(plugin, monkeypatch):
    _, _, dest = plugin
    (dest / 'catalogs/card-names.json').unlink()
    old = (dest / 'rules/cr.json').read_bytes()
    monkeypatch.delenv('MTG_RULES_SETUP_DATA', raising=False)
    with patch('mtg_rules.bootstrap.setup', side_effect=OSError('download failed')), pytest.raises(OSError):
        bootstrap.ensure(dest)
    assert (dest / 'rules/cr.json').read_bytes() == old
    assert not bootstrap.ready(dest)
    assert not (dest / bootstrap.LOCK).exists()
    assert not list(dest.glob('.mtg-rules-runtime.*'))


@pytest.mark.parametrize('owner', ['', 'garbled', '0', '999999999'])
def test_bootstrap_reclaims_stale_locks(tmp_path, monkeypatch, owner):
    monkeypatch.delenv('MTG_RULES_SETUP_DATA', raising=False)
    lock = tmp_path / bootstrap.LOCK
    lock.mkdir()
    if owner:
        (lock / 'pid').write_text(owner)
    with patch('mtg_rules.bootstrap.setup', side_effect=offline_setup):
        bootstrap.ensure(tmp_path, timeout=2, interval=.01)
    assert bootstrap.ready(tmp_path) and not lock.exists()


def test_bootstrap_does_not_steal_live_lock(tmp_path):
    lock = tmp_path / bootstrap.LOCK
    lock.mkdir()
    (lock / 'pid').write_text(str(os.getpid()))
    with patch('mtg_rules.bootstrap.setup', side_effect=AssertionError('stole lock')), pytest.raises(ValueError, match='timed out'):
        bootstrap.ensure(tmp_path, timeout=.03, interval=.01)
    assert (lock / 'pid').read_text() == str(os.getpid())


def test_bootstrap_concurrency_with_only_python_on_path(tmp_path):
    dest = tmp_path / 'runtime'
    bin_dir = tmp_path / 'bin'
    bin_dir.mkdir()
    (bin_dir / 'python3').symlink_to(sys.executable)
    count = tmp_path / 'count'
    env = dict(os.environ, PATH=str(bin_dir), MTG_RULES_SETUP_DATA=str(FAKE_SETUP), MTG_RULES_FAKE_SETUP_COUNT=str(count), MTG_RULES_FAKE_SETUP_DELAY='.2')
    command = [sys.executable, str(ROOT / 'skills/mtg-rules/scripts/ensure-data'), '--dest', str(dest)]
    processes = [subprocess.Popen(command, env=env, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True) for _ in range(2)]
    try:
        for process in processes:
            out, err = process.communicate(timeout=15)
            assert process.returncode == 0, (out, err)
    finally:
        for process in processes:
            if process.poll() is None:
                process.kill()
                process.wait()
    assert count.read_text().strip() == '1'
    assert bootstrap.ready(dest)


def test_health_labels_the_source_discovery_used(plugin, monkeypatch, tmp_path):
    root, skill, data = plugin
    monkeypatch.setenv('MTG_RULES_DATA', str(data) + '/')
    assert 'via $MTG_RULES_DATA' in invoke(skill, 'health')[1]
    home = tmp_path / 'home'
    host = home / '.claude/plugins/data/mtg-rules/data'
    host.parent.mkdir(parents=True)
    shutil.move(data, host)
    for key in ('MTG_RULES_DATA', 'PLUGIN_DATA'):
        monkeypatch.delenv(key)
    monkeypatch.setenv('HOME', str(home))
    code, out, err = invoke(skill, 'health')
    assert f'data: {host} (via host plugin data)' in out, (out, err)
