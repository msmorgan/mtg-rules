"""Lookup CLI implementations; source data and maps remain separate authorities."""

import argparse
import contextlib
import hashlib
import io
import json
import os
import re
import sqlite3
import subprocess
import sys
from functools import cached_property
from pathlib import Path

from . import cite
from .cards import card_text, ruling_text
from .data import locate_data
from .references import USAGE, Maps, rule_pattern
from .setup_data import normalize_glossary


def read_json(path):
    return json.loads(path.read_text(encoding='utf-8'))


def regex(value):
    try:
        return re.compile(value, re.I)
    except re.error as error:
        raise ValueError(f"invalid regex: {value}: {error}") from error


def clipped(text, limit):
    return text[:limit] + '…' if len(text) > limit else text


class Runtime:
    def __init__(self, skill: Path):
        self.skill = skill.resolve()

    @cached_property
    def located(self):
        return locate_data(self.skill)

    @property
    def data(self):
        return self.located[0]

    @cached_property
    def rules(self):
        return read_json(self.data / 'rules/cr.json')

    @cached_property
    def glossary(self):
        return read_json(self.data / 'rules/glossary.json')

    @cached_property
    def unofficial(self):
        return read_json(self.data / 'rules/unofficial-glossary.json')

    @cached_property
    def keywords(self):
        path = self.skill / 'keywords-classified.json'
        return read_json(path)['keywords'] if path.is_file() else []

    @cached_property
    def mtr(self):
        return read_json(self.data / 'rules/mtr.json')['content']

    @cached_property
    def maps(self):
        return Maps(self.skill)

    def rule_lines(self, number, *, footer=True):
        pattern = rule_pattern(number)
        hits = [v for k, v in self.rules.items() if pattern.search(k)]
        if not hits:
            raise ValueError(f"rule: no CR entry matches {pattern.pattern}")
        lines = []
        for value in hits:
            num = value['ruleNumber']
            lines.append(num + (' ' if num[-1].isalpha() else '. ') + value['ruleText'])
            lines.extend('    Example: ' + example for example in value.get('examples') or [])
        if footer and '.' in number:
            try:
                reports = sorted(self.maps.cites(number, self.data), key=lambda r: -r.count)
                labels = [f"{r.doc} §{r.label()[:24] if r.label() == r.heading else r.label()}" for r in reports if r.heading != '(header)'][:3]
                if labels:
                    lines.append('maps: ' + ', '.join(labels) + ' (ref <doc> <n> to read)')
            except (OSError, ValueError):
                pass  # Navigation is optional; a broken map cannot hide source text.
        return lines

    @property
    def manifest(self):
        root = self.skill.parents[1]
        return next((p for p in (root / '.codex-plugin/plugin.json', root / '.claude-plugin/plugin.json', self.skill / '.claude-plugin/plugin.json') if p.is_file()), None)


def require(args, command, *, exactly=None):
    if not args or not ' '.join(args) or (exactly is not None and len(args) != exactly):
        raise ValueError(f'usage: {command} <argument>')
    return ' '.join(args)


def command_parser(command):
    return argparse.ArgumentParser(prog=command)


def define(runtime, term):
    def norm(s):
        return s.replace('’', "'").replace('“', '"').replace('”', '"').replace('—', '--')
    query = norm(term.lower())
    official = {norm(k): v for k, v in runtime.glossary.items()}
    unofficial = {norm(k): v for k, v in runtime.unofficial.items()}
    value = official.get(query) or unofficial.get(query)
    if not value:
        near = sorted({k for k in official.keys() | unofficial.keys() if query in k})[:30]
        raise ValueError(f'define: no exact entry for "{term.lower()}". Near matches: ' + ', '.join(near) if near else f'define: no glossary entry for "{term.lower()}"')
    tag = '' if query in official else ' (unofficial)'
    out = f"{value['term']}{tag}: {value['definition']}"
    print(out)
    if match := re.search(r'See rules? ([0-9]{3}\.[0-9]+[a-z]*)', out):
        try:
            lines = runtime.rule_lines(match[1])
        except ValueError:
            return
        first = lines[0]
        if len(first) > 500:
            first = first[:500].rstrip() + '…'
        print('→ ' + first)
        if len(lines) > 1 or len(lines[0]) > 500:
            print(f'  (scripts/rule {match[1]} for the rest)')


def section_id(section):
    if section['section'] is None:
        return 'intro'
    return str(section['section']) + ('.' + str(section['subsection']) if section.get('subsection') is not None else '')


def mtr(runtime, argv):
    parser = command_parser('mtr')
    parser.add_argument('-l', '--list', action='store_true')
    parser.add_argument('-s', '--search')
    parser.add_argument('section', nargs='?')
    args = parser.parse_args(argv)
    if args.list or args.search is not None:
        if args.section:
            raise ValueError('usage: mtr --list / --search take no positional args')
        if args.list:
            for s in runtime.mtr:
                prefix = '' if s['section'] is None else str(s['section']) + '. ' if s.get('subsection') is None else section_id(s) + '  '
                print(prefix + s['title'])
        else:
            pattern = regex(args.search)
            hits = [s for s in runtime.mtr if pattern.search((s.get('content') or '') + ' ' + (s.get('title') or ''))]
            if not hits:
                raise ValueError(f'mtr: no sections match /{args.search}/')
            for s in hits:
                print(section_id(s) + '  ' + s['title'])
        return
    if not args.section or not re.fullmatch(r'[0-9]+(?:\.[0-9]+)?', args.section):
        raise ValueError('usage: mtr <sec[.sub]> | mtr --list | mtr --search <regex>')
    nums = list(map(int, args.section.split('.')))
    hits = [s for s in runtime.mtr if s['section'] == nums[0] and (len(nums) == 1 or s.get('subsection') == nums[1])]
    if not hits:
        raise ValueError(f'mtr: no section {args.section}')
    for s in hits:
        print(f"## {section_id(s)} {s['title']}\n\n{s['content']}\n")


def ref(runtime, argv):
    if not argv or argv[0] in ('-h', '--help'):
        print(USAGE)
        if not argv:
            print()
            for doc in runtime.maps.docs:
                title = doc.lines[0].removeprefix('# ') if doc.lines else ''
                print(f"{doc.name:26s} {title}  [{doc.date or 'no date'}]")
        return
    if argv[0] in ('--cites', '--grep'):
        query = require(argv[1:], 'ref ' + argv[0], exactly=1 if argv[0] == '--cites' else None)
        reports = runtime.maps.cites(query, runtime.data) if argv[0] == '--cites' else runtime.maps.grep(regex(query))
        if not reports:
            raise ValueError(f'ref: no reference lines match {query}')
        for report in reports:
            print(report.render())
        print('→ read a section: ref <doc> <number or heading text>')
        return
    doc = runtime.maps.find(argv[0])
    if len(argv) == 1:
        print(doc.lines[0] if doc.lines else '')
        print(f"synthesized from CR {doc.date or 'no synthesis date'} — a map, not a source; cite the CR rules")
        print('\n'.join(doc.section_lines()))
        return
    wanted = ' '.join(argv[1:]).removeprefix('§').strip()
    hits = doc.select(wanted)
    if not hits:
        raise ValueError(f"ref: no section '{wanted}' in {doc.name}. Sections:\n" + '\n'.join(doc.section_lines()) + f'\nusage: ref {doc.name} <section number or heading text>')
    if len(hits) > 1:
        others = ', '.join('§' + h.text for h in hits[1:5]) + (', …' if len(hits) > 5 else '')
        print(f"ref: note: {len(hits)} sections match '{wanted}'; showing the first. Others: {others}", file=sys.stderr)
    h = hits[0]
    source = 'synthesized from CR ' + doc.date if doc.date else 'no synthesis date'
    print(f'[map] {doc.name} §{h.text} (lines {h.start}-{h.end}) — {source}. A map, not a source: cite the CR rules (scripts/rule), not the map; uncited claims are inferences.')
    print('\n'.join(doc.lines[h.start - 1:h.end]))


def lookup(runtime, query):
    pattern = regex(query)
    groups = []
    rules = [f"[rule] {k}: {clipped(v['ruleText'].replace(chr(10), ' '), 120)}" for k, v in runtime.rules.items() if pattern.search(v['ruleText'])]
    gloss = [f"[gloss] {v['term']}: {clipped(v['definition'].replace(chr(10), ' '), 110)}" for g in (runtime.glossary, runtime.unofficial) for v in g.values() if pattern.search(v['term'] + ' ' + v['definition'])]
    keywords = [f"[keyword] {k} {v['ruleText']}" for k, v in runtime.rules.items() if re.fullmatch(r'70[12]\.[0-9]+', k) and pattern.search(v['ruleText'])]
    keywords += [f"[keyword] {v['name']} — {v['class']}" + (f" given: {v['given']}" if v.get('given') else '') + f" [{v['rule']}] — scripts/classify" for v in runtime.keywords if pattern.search(v['name'])]
    policies = [f"[mtr] {section_id(s)}  {s['title']}" for s in runtime.mtr if pattern.search((s.get('content') or '') + ' ' + (s.get('title') or ''))]
    for name, hits, limit, next_call in [('rule', rules, 8, 'scripts/rule-search'), ('gloss', gloss, 5, 'scripts/define'), ('keyword', keywords, 8, 'scripts/keyword, scripts/classify'), ('mtr', policies, 4, 'scripts/mtr --search')]:
        groups.extend(hits[:limit])
        if len(hits) > limit:
            groups.append(f'[{name}] (+{len(hits) - limit} more — {next_call})')
    maps = sorted(runtime.maps.grep(pattern), key=lambda r: -r.count)
    groups.extend(f"[map] {r.doc} §{r.heading}  (ref {r.doc} '{r.label()}')" for r in maps[:6])
    if len(maps) > 6:
        groups.append(f"[map] (+{len(maps) - 6} more — ref --grep '{query}')")
    if not groups:
        raise ValueError(f'lookup: nothing matches /{query}/ in CR rules, glossaries, keywords, MTR, or reference docs')
    print('\n'.join(groups))
    print('→ drill down with scripts/rule, define, keyword, mtr, or Read the doc')


def version(runtime):
    manifest = runtime.manifest
    if not manifest:
        raise ValueError(f'version: cannot find a Codex or Claude plugin manifest from {runtime.skill}')
    commit = None
    root = runtime.skill.parents[1]
    try:
        result = subprocess.run(['jj', '--no-pager', '--ignore-working-copy', 'log', '-r', '@-', '--no-graph', '-T', 'commit_id'], cwd=root, capture_output=True, text=True, check=False)
        if result.returncode == 0:
            commit = result.stdout.strip() or None
    except FileNotFoundError:
        pass
    try:
        effective = cite.effective_date((runtime.data / 'rules/cr.txt').read_text(encoding='utf-8'))
    except (OSError, ValueError):
        effective = None
    print(json.dumps(dict(plugin_version=read_json(manifest)['version'], git_commit=commit,
                          cr_effective=effective, keywords_classified_sha=hashlib.sha256((runtime.skill / 'keywords-classified.json').read_bytes()).hexdigest()), indent=2))


def health(runtime):
    data = runtime.data
    print(f'data: {data} (via {runtime.located[1]})')
    try:
        text = (data / 'rules/cr.txt').read_text(encoding='utf-8')
        date = cite.effective_date(text)
        match = re.search(r'effective as of (.+?)\.?$', text, re.M)
        print(f"CR effective: {match[1] if match else date}")
    except (OSError, ValueError):
        date = None
        print(f'CR effective: date unknown (cr.txt absent; cr.json has {len(runtime.rules)} rules)')
    if date:
        docs = runtime.maps.docs
        synced = sum(d.date == date for d in docs)
        print(f'reference docs: {synced}/{len(docs)} synthesized from CR {date} (live {date}); verify map claims against the cited rules')
        lag = [f"{d.path.name} ({d.date or 'no date'})" for d in docs if d.date != date]
        if lag:
            print('  lagging or undated (warning only): ' + ', '.join(lag))
    catalogs = bool(list((data / 'catalogs').glob('*.json')))
    def mark(path):
        return '✓' if (data / path).is_file() else 'absent'
    print(f"tier base:    rules ✓, catalogs {'✓' if catalogs else 'absent'} — rule, rule-search, define, keyword, mtr, lookup, ref, classify, underdetermined, cite, version")
    print(f"tier cards:   AllPrintings.sqlite {mark('mtgjson/AllPrintings.sqlite')} — card; cards.jsonl {mark('derived/cards.jsonl')}, AtomicCards.json {mark('mtgjson/AtomicCards.json')} — corpus")
    print(f"tier rulings: AllPrintings.sqlite {mark('mtgjson/AllPrintings.sqlite')} — rulings")
    print(f'keywords-classified: {len(runtime.keywords)} keywords')
    classified = {v['rule'] for v in runtime.keywords}
    unclassified = [f"{k} {v['ruleText']}" for k, v in runtime.rules.items() if re.fullmatch(r'70[12]\.[0-9]+', k) and k not in ('701.1', '702.1') and k not in classified]
    if unclassified:
        more = f', +{len(unclassified) - 8} more' if len(unclassified) > 8 else ''
        print(f'warn: {len(unclassified)} CR keyword heading(s) with no row in keywords-classified.json: ' + ', '.join(unclassified[:8]) + more)
    print('plugin version: ' + (read_json(runtime.manifest)['version'] if runtime.manifest else 'unknown (plugin manifest not found)'))
    out = io.StringIO()
    with contextlib.redirect_stdout(out), contextlib.redirect_stderr(out):
        code = cite.main(['--config', str(runtime.skill / 'cite-config.json'), 'check'])
    print('citations: ' + (out.getvalue().splitlines() or ['no output'])[-1])
    if code or not catalogs:
        raise ValueError('health: NOT healthy (base tier or citations failed)')
    print('health: OK (base tier + citations)')


def run(command, runtime, argv):
    if command == 'normalize-glossary':
        path = Path(require(argv, command, exactly=1))
        value = normalize_glossary(read_json(path))
        temporary = path.with_name(path.name + f'.tmp.{os.getpid()}')
        try:
            temporary.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
            temporary.replace(path)
        finally:
            temporary.unlink(missing_ok=True)
    elif command == 'data-path':
        parser = command_parser(command)
        parser.add_argument('--field', choices=['rules', 'catalogs', 'mtgjson', 'derived', 'effective'])
        args = parser.parse_args(argv)
        if args.field == 'effective':
            print(cite.effective_date((runtime.data / 'rules/cr.txt').read_text(encoding='utf-8')))
        else:
            print(runtime.data / args.field if args.field else runtime.data)
    elif command == 'rule':
        print('\n'.join(runtime.rule_lines(require(argv, command, exactly=1))))
    elif command == 'rule-search':
        parser = command_parser(command)
        parser.add_argument('-m', '--max', type=int, default=20)
        parser.add_argument('pattern')
        args = parser.parse_args(argv)
        if args.max < 1:
            raise ValueError('rule-search: --max must be a positive integer')
        pattern = regex(args.pattern)
        hits = [(k, v['ruleText']) for k, v in runtime.rules.items() if pattern.search(v['ruleText'])]
        if not hits:
            raise ValueError(f'rule-search: nothing matches /{args.pattern}/')
        for k, text in hits[:args.max]:
            print(f'{k}: {clipped(text, 200)}')
        if len(hits) > args.max:
            print(f'({len(hits) - args.max} more matches — raise --max)')
    elif command == 'define':
        define(runtime, require(argv, command))
    elif command == 'keyword':
        name = require(argv, command).lower()
        found = next((k for k, v in runtime.rules.items() if re.fullmatch(r'70[12]\.[0-9]+', k) and v['ruleText'].lower() == name), None)
        if not found:
            entry = runtime.glossary.get(name) or runtime.glossary.get(name.replace("'", '’'))
            match = re.search(r'rule ([0-9]{3}\.[0-9]+)', entry['definition']) if entry else None
            found = match[1] if match else None
        if not found:
            raise ValueError(f"keyword: no CR section found for '{name}' — try scripts/define or scripts/rule-search")
        print('\n'.join(runtime.rule_lines(found)))
    elif command == 'mtr':
        mtr(runtime, argv)
    elif command == 'card':
        full = argv[:1] == ['--full-name']
        name = require(argv[1:] if full else argv, 'card [--full-name]')
        sys.stdout.write(card_text(runtime.data, name, full_name=full))
    elif command == 'rulings':
        name = require(argv, command)
        text, face = ruling_text(runtime.data, name)
        if face:
            print(f"rulings: no card named exactly '{name}' has rulings; showing cards with that FACE name", file=sys.stderr)
        sys.stdout.write(text)
        print('note: ruling texts may cite CR numbers from their publication date — verify with scripts/rule', file=sys.stderr)
    elif command == 'corpus':
        parser = command_parser(command)
        parser.add_argument('-t', '--type', default='')
        parser.add_argument('-k', '--keyword', default='')
        parser.add_argument('-m', '--match')
        parser.add_argument('-a', '--all', action='store_true')
        args = parser.parse_args(argv)
        pattern = regex(args.match) if args.match else None
        path = runtime.data / 'derived/cards.jsonl'
        if not path.is_file():
            raise ValueError('corpus: data/derived/cards.jsonl missing — run skills/mtg-rules/scripts/setup-data --cards')
        lines = set()
        with path.open(encoding='utf-8') as stream:
            for record in stream:
                card = json.loads(record)
                if not args.all and not card.get('supported'):
                    continue
                if args.type and args.type.lower() not in [t.lower() for t in card.get('types') or []]:
                    continue
                lines.update(line for line in (card.get('text') or '').split('\n') if line and args.keyword.lower() in line.lower() and (not pattern or pattern.search(line)))
        if not lines:
            raise ValueError('corpus: no oracle lines match')
        print('\n'.join(sorted(lines)))
    elif command == 'classify':
        name = require(argv, command).lower()
        hit = next((v for v in runtime.keywords if v['name'].lower() == name), None)
        if not hit:
            near = [v['name'] for v in runtime.keywords if name in v['name'].lower()]
            raise ValueError(f'classify: no keyword "{name}". Near matches: ' + ', '.join(near) if near else f'classify: no keyword "{name}" in keywords-classified.json')
        print(f"{hit['name']} ({hit['kind']}) — {hit['class']}" + (f" given: {hit['given']}" if hit.get('given') else ''))
        for field in ('ident', 'rule', 'how', 'cites', 'core_referenced'):
            value = hit[field]
            print(f"{field}: " + (', '.join(value) if isinstance(value, list) else str(value).lower() if isinstance(value, bool) else str(value)))
    elif command == 'underdetermined':
        lines = (runtime.skill / 'references/underdetermined.md').read_text(encoding='utf-8').splitlines()
        if not argv:
            print('\n'.join(line[4:] for line in lines if line.startswith('### ')))
            return
        identifier = require(argv, command, exactly=1).upper()
        if identifier.isdigit():
            identifier = 'UD-' + identifier
        if not re.fullmatch(r'(UD-|U|S)[0-9]+', identifier):
            raise ValueError(f"underdetermined: bad id '{identifier}' — want UD-N (or a retired S/U id); list with: underdetermined")
        result, active = [], False
        for line in lines:
            if line.startswith('#'):
                active = line.startswith('### ' + identifier + ' ')
            if active:
                result.append(line)
        if not result:
            raise ValueError(f"underdetermined: no entry '{identifier}' — list ids with: scripts/underdetermined")
        print('\n'.join(result))
    elif command == 'ref':
        ref(runtime, argv)
    elif command == 'lookup':
        lookup(runtime, require(argv, command))
    elif command == 'version':
        version(runtime)
    elif command == 'health':
        health(runtime)
    else:
        raise ValueError(f'unknown lookup command: {command}')


def main(command, skill, argv=None):
    try:
        run(command, Runtime(skill), sys.argv[1:] if argv is None else argv)
    except (OSError, ValueError, sqlite3.Error) as error:
        print(str(error), file=sys.stderr)
        return 1
    return 0
