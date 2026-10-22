"""Ported xtask cases plus plugin-specific parity and migration contracts."""

import contextlib
import io
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path
from unittest.mock import patch

import pytest

from mtg_rules.cite import (
    Repository,
    Snapshot,
    added_diff_lines,
    bless,
    checksum,
    hashes,
    main,
    noncompliant_hits,
    parse_rule_text,
    scan,
    stale,
)
from mtg_rules.cite_hook import render
from mtg_rules.exemptions import exempt_lines
from mtg_rules.setup_data import download, normalize_glossary, promote_rules, setup

FIXTURES = Path(__file__).parent / "fixtures/cite"
CASES = json.loads((FIXTURES / "xtask-cases.json").read_text())


@pytest.fixture
def repo(tmp_path):
    shutil.copytree(FIXTURES, tmp_path, dirs_exist_ok=True)
    return Repository(tmp_path / "cfg-good.json")


def fixture_snapshot(root):
    rules = root / "rules"
    rules.mkdir(exist_ok=True)
    text = (FIXTURES / "xtask-cr.txt").read_text()
    texts, order = parse_rule_text(text)
    (rules / "cr.txt").write_text(text)
    # Reverse JSON order to ensure the parser never accidentally depends on it.
    (rules / "cr.json").write_text(json.dumps({r: {"ruleText": texts[r]} for r in reversed(order)}))
    return Snapshot(rules)


@pytest.mark.parametrize("case", CASES, ids=lambda c: c["origin"])
def test_xtask_fixture(case, tmp_path):
    kind = case["kind"]
    if kind in {"noncompliant", "legacy"}:
        hits = [hit[1] for hit in noncompliant_hits(case["source"])]
        if kind == "legacy":
            assert hits  # Old AST-specific markers cannot silently gain broader powers.
        else:
            assert hits == case["matches"]
    elif kind == "marker-error":
        with pytest.raises(ValueError):
            exempt_lines(case["source"])
    elif kind == "diff":
        assert added_diff_lines(case["source"]) == {tuple(pair) for pair in case["added"]}
    elif kind == "parse":
        texts, order = parse_rule_text((FIXTURES / "xtask-cr.txt").read_text())
        assert texts[case["rule"]] == case["text"]
        assert order == ["100.1", "100.1a", "100.1c", "200.1"]
        assert texts["100"] == "General"
        assert checksum(texts[case["rule"]]) == checksum(case["text"])
        assert case.get("excluded", "never-present") not in texts[case["rule"]]
    else:
        snapshot = fixture_snapshot(tmp_path)
        if kind == "resolve":
            assert snapshot.resolve(case["raw"]) == (case["status"], case["members"])
            assert snapshot.resolve("100.1c..100.1a") == ("gone", [])
            assert snapshot.resolve("100..200") == ("gone", [])
            return
        if kind == "stale":
            sites = scan("[CR#100.1]\n[CR#rule]", "f", "bracketed", snapshot)
            report = stale(sites, hashes(sites, snapshot), {"100.1": "deadbeefdeadbeef"})
            assert [line.split()[0] for line in report] == ["CHANGED", "MALFORMED"]
            return
        (tmp_path / "cite-config.json").write_text(json.dumps({"sources": {"globs": ["*.md"], "exclude": ["EXEMPT.md"]}, "noncompliant_exempt": ["exempt.rs"]}))
        (tmp_path / "SCANNED.md").write_text("[CR#100.1a..100.1c,200.1]")
        repository = Repository(tmp_path / "cite-config.json")
        if kind == "bless":
            with patch.dict(os.environ, {"MTG_RULES_CITE_WIZARDS_URL": "https://example.invalid/cr.txt"}):
                bless(repository, snapshot, repository.sites(snapshot))
                locked = repository.lock("check")
                assert list(locked["checksums"]) == ["100.1a", "100.1c", "200.1"]
                assert locked["cr_date"] == "2026-01-02"
                (tmp_path / "SCANNED.md").write_text("[CR#200.1]")
                bless(repository, snapshot, repository.sites(snapshot))
                assert list(repository.lock("check")["checksums"]) == ["200.1"]
        elif kind == "file-exemption":
            (tmp_path / "SCANNED.md").write_text("CR 200.1")
            (tmp_path / "exempt.rs").write_text("rule 200.1")
            repository.config["sources"]["globs"].append("*.rs")
            selected = [p for p in repository.sources() if not any(str(p).endswith(s) for s in repository.config["noncompliant_exempt"])]
            assert sum(len(noncompliant_hits(p.read_text())) for p in selected) == 2
        elif kind == "audit-selection":
            assert repository.relative_argument(str(tmp_path / "SCANNED.md")) == "SCANNED.md"
            assert repository.relative_argument("SCANNED.md") == "SCANNED.md"
            assert len([s for s in repository.sites(snapshot) if s["file"] == "SCANNED.md"]) == 1
        elif kind == "symlink":
            (tmp_path / "EXEMPT.md").write_text("CR 100.1 [CR#100.1]")
            (tmp_path / "LINK_EXEMPT.md").symlink_to("EXEMPT.md")
            (tmp_path / "LINK_SCANNED.md").symlink_to("SCANNED.md")
            assert [p.name for p in repository.sources()] == ["SCANNED.md"]
            assert len(repository.sites(snapshot)) == 1
        else:
            pytest.fail(f"unhandled fixture kind: {kind}")


def test_numbered_lettered_and_two_digit_boundaries(tmp_path):
    snapshot = fixture_snapshot(tmp_path)
    assert snapshot.resolve("100.1..100.1c") == ("ok", ["100.1", "100.1a", "100.1c"])
    assert snapshot.resolve("100.1..200.1") == ("ok", ["100.1", "100.1a", "100.1c", "200.1"])
    text = "These rules are effective as of January 2, 2026.\n701.7. Seven.\n701.7a Child.\n701.8. Eight.\n701.70. Seventy.\n"
    rules = tmp_path / "rules"
    (rules / "cr.txt").write_text(text)
    (rules / "cr.json").write_text(json.dumps({r: {"ruleText": r} for r in ["701.7", "701.70", "701.7a", "701.8"]}))
    snapshot = Snapshot(rules)
    assert snapshot.resolve("701.7..701.8") == ("ok", ["701.7", "701.7a", "701.8"])
    assert snapshot.resolve("701.8..701.70") == ("ok", ["701.8", "701.70"])


def test_globs_apply_extensions_and_exclusions(repo):
    repo.config["sources"] = {"globs": ["src/*"], "extensions": ["md"], "exclude": ["src/malformed", "src/gone"]}
    assert {p.name for p in repo.sources()} == {"good.md", "more.md", "placeholder.md"}


def test_tracked_symlinks_and_component_order(repo):
    (repo.root / "src/a.md").symlink_to("good.md")
    (repo.root / "src/good").mkdir()
    (repo.root / "src/good/child.md").write_text("[CR#100.1]")
    repo.config["sources"] = {"tracked": True}
    result = subprocess.CompletedProcess([], 0, stdout="src/good.md\nsrc/a.md\nsrc/good/child.md\n")
    with patch("subprocess.run", return_value=result):
        assert [str(p.relative_to(repo.root)) for p in repo.sources()] == ["src/good/child.md", "src/good.md"]


def test_list_json_includes_bad_sites_and_expansions(repo, monkeypatch, capsys):
    monkeypatch.setenv("MTG_RULES_DATA", str(repo.root / "data"))
    code = main(["--config", str(repo.root / "cfg-malformed.json"), "list", "--json"])
    assert code == 0
    sites = json.loads(capsys.readouterr().out)
    assert all(set(s) == {"file", "line", "token", "status", "members"} for s in sites)
    assert any(s["status"] == "malformed" and s["members"] == [] for s in sites)
    assert any(s["members"] == ["704.5k", "704.5m", "704.5n"] for s in sites)


@pytest.mark.parametrize("prefix,suffix", [("//", ""), ("#", ""), ("--", ""), ("<!--", " -->")])
def test_language_independent_exemptions(prefix, suffix):
    source = f"{prefix} cite: allow-noncompliant begin -- quoted fixture{suffix}\nrule 100.1\n{prefix} cite: allow-noncompliant end{suffix}\nrule 200.1"
    assert [h[1] for h in noncompliant_hits(source)] == ["rule 200.1", "200.1"]


@pytest.mark.parametrize("source", [
    '"// cite: allow-noncompliant-line -- quoted marker"; // rule 100.1',
    'r##"\n// cite: allow-noncompliant begin -- quoted marker\nrule 100.1\n// cite: allow-noncompliant end\n"##',
    '"""\n# cite: allow-noncompliant begin -- quoted marker\nrule 100.1\n# cite: allow-noncompliant end\n"""',
])
def test_markers_in_strings_have_no_effect(source):
    assert [h[1] for h in noncompliant_hits(source)] == ["rule 100.1", "100.1"]


def test_refresh_retains_previous_and_same_date_does_not_replace_it(repo, monkeypatch, capsys):
    rules = repo.root / "data/rules"
    before = (rules / "cr.json").read_bytes()
    new = repo.root / "incoming"
    shutil.copytree(rules, new)
    (new / "cr.txt").write_text((new / "cr.txt").read_text().replace("April 17", "April 18"))
    updated = json.loads((new / "cr.json").read_text())
    updated["702.22a"]["ruleText"] = "New wording."
    (new / "cr.json").write_text(json.dumps(updated))
    promote_rules(new, rules)
    assert (rules / "previous/cr.json").read_bytes() == before
    for name in ("cr.json", "cr.txt"):
        shutil.copyfile(rules / name, new / name)
    promote_rules(new, rules)
    assert (rules / "previous/cr.json").read_bytes() == before
    repo.lock_path.write_text(json.dumps({"cr_date": "2026-04-17", "wizards_url": "https://invalid/"}))
    monkeypatch.setenv("MTG_RULES_DATA", str(repo.root / "data"))
    with patch("urllib.request.urlopen", side_effect=AssertionError("network must not be used")):
        assert main(["--config", str(repo.root / "cfg-good.json"), "diff", "702.22a"]) == 0
    output = capsys.readouterr().out
    assert "- Banding is a static" in output and "+ New wording." in output


def test_diff_rejects_html_and_wrong_local_date(repo, monkeypatch, capsys):
    monkeypatch.setenv("MTG_RULES_DATA", str(repo.root / "data"))
    html = repo.root / "landing.html"
    html.write_text("<!doctype html><html>Download the CR</html>")
    repo.lock_path.write_text(json.dumps({"wizards_url": html.as_uri(), "cr_date": "2020-01-01"}))
    shutil.copytree(repo.root / "data-v2/rules", repo.root / "data/rules/previous")
    assert main(["--config", str(repo.root / "cfg-good.json"), "diff", "100.1"]) == 1
    output = capsys.readouterr()
    assert "plain CR text" in output.err and "absent" not in output.out


def test_failed_refresh_leaves_current_and_previous_untouched(repo):
    before = {p.name: p.read_bytes() for p in (repo.root / "data/rules").iterdir()}
    with patch("mtg_rules.setup_data.download", side_effect=OSError("failed transfer")), pytest.raises(OSError):
        setup(repo.root / "data")
    assert before == {p.name: p.read_bytes() for p in (repo.root / "data/rules").iterdir()}


def test_downloader_and_glossary_use_stdlib(tmp_path):
    import lzma
    source = tmp_path / "source.xz"
    source.write_bytes(lzma.compress(b'example data'))
    with patch("subprocess.run", side_effect=AssertionError("external tool")):
        download(source.as_uri(), tmp_path / "out", compressed=True)
    assert (tmp_path / "out").read_bytes() == b'example data'
    glossary = json.loads((FIXTURES.parent / "glossary-envelope.json").read_text())
    assert normalize_glossary(glossary)["active player"]["term"] == "Active Player"


def test_hook_without_external_tools(repo, monkeypatch):
    (repo.root / ".jj").mkdir()
    shutil.copyfile(repo.root / "cfg-good.json", repo.root / "cite-config.json")
    monkeypatch.setenv("MTG_RULES_DATA", str(repo.root / "data"))
    monkeypatch.setenv("TMPDIR", str(repo.root))
    monkeypatch.delenv("CITE_CONTEXT_OFF", raising=False)
    payload = {"cwd": str(repo.root), "session_id": "test", "tool_name": "Edit", "tool_input": {"new_string": "[CR#100.1]"}}
    with patch("subprocess.run", side_effect=AssertionError("external tool")):
        assert "Placeholder first rule" in render(payload)
        assert render(payload) == ""


def test_hook_contains_bad_payloads_and_emits_json(repo, monkeypatch):
    from mtg_rules.cite_hook import main as hook_main
    for payload in ("broken", "[]", '{"tool_name":"Edit","tool_input":5}'):
        with patch.object(sys, "stdin", io.StringIO(payload)), contextlib.redirect_stdout(io.StringIO()) as output:
            assert hook_main() == 0
            assert not output.getvalue()


def test_git_only_consumer_fallback_is_preserved(tmp_path):
    from mtg_rules.cite import tracked_files
    results = [FileNotFoundError(), subprocess.CompletedProcess([], 0, stdout="src/a.rs\n")]
    with patch("subprocess.run", side_effect=results) as run:
        assert tracked_files(tmp_path) == ["src/a.rs"]
        assert run.call_args.args[0] == ["git", "ls-files"]


def test_invalid_staged_pair_cannot_replace_previous(repo):
    rules = repo.root / "data/rules"
    staged = repo.root / "broken"
    staged.mkdir()
    (staged / "cr.json").write_text('{}')
    (staged / "cr.txt").write_text('These rules are effective as of April 18, 2026.\n<html>No CR</html>')
    old = (rules / "cr.json").read_bytes()
    with pytest.raises(ValueError, match="no numbered rules"):
        promote_rules(staged, rules)
    assert (rules / "cr.json").read_bytes() == old
    assert not (rules / "previous").exists()


def test_exemption_scope_cannot_hide_trailing_prose():
    with pytest.raises(ValueError, match="own line"):
        exempt_lines('<!-- cite: allow-noncompliant begin -- fixture --> rule 100.1')


def test_successful_staged_refresh_validates_and_retains_old_pair(repo):
    import sqlite3

    data = repo.root / "data"
    before = (data / "rules/cr.json").read_bytes()

    def fetch(url, target, *, compressed=False):
        target.parent.mkdir(parents=True, exist_ok=True)
        if target.name == "AllPrintings.sqlite":
            with sqlite3.connect(target) as db:
                db.execute("CREATE TABLE cards(name TEXT)")
                db.execute("INSERT INTO cards VALUES ('Fixture')")
        elif target.parent.name == "rules":
            if target.name in {"cr.json", "cr.txt"}:
                text = (data / "rules" / target.name).read_text()
                target.write_text(text.replace("April 17", "April 18"))
            elif target.name == "glossary.json":
                target.write_text('{"fixture":{"term":"Fixture","definition":"A fixture."}}')
            else:
                target.write_text('{}')
        else:
            target.write_text('{"data":[]}')

    with patch("mtg_rules.setup_data.download", side_effect=fetch), patch("time.sleep"):
        setup(data, runtime=True)
    assert (data / "rules/previous/cr.json").read_bytes() == before
    assert "April 18" in (data / "rules/cr.txt").read_text()
    assert (data / "mtgjson/AllPrintings.sqlite").is_file()
    assert not list(data.glob('.setup-*'))


def test_failed_xz_download_does_not_replace_existing_file(tmp_path):
    source = tmp_path / "bad.xz"
    source.write_bytes(b'not xz')
    target = tmp_path / "existing"
    target.write_bytes(b'keep me')
    import lzma
    with patch("time.sleep"), pytest.raises(lzma.LZMAError):
        download(source.as_uri(), target, compressed=True)
    assert target.read_bytes() == b'keep me'
    assert {p.name for p in tmp_path.iterdir()} == {'bad.xz', 'existing'}


def _tty_stdin():
    stdin = io.StringIO("")
    stdin.isatty = lambda: True
    return stdin


def test_interactive_audit_diff_falls_back_to_git(repo, capsys):
    diff = "+++ b/src/good.md\n@@ -0,0 +1,1 @@\n+Good citations: [CR#702.22a]\n"
    results = [FileNotFoundError(), subprocess.CompletedProcess([], 0, stdout=diff)]
    with patch.object(sys, "stdin", _tty_stdin()), patch("subprocess.run", side_effect=results) as run:
        assert main(["--config", str(repo.root / "cfg-good.json"), "audit", "--diff"]) == 0
    assert run.call_args.args[0][:3] == ["git", "-C", str(repo.root)]
    assert "audited 2 citation site(s)" in capsys.readouterr().out


def test_interactive_audit_diff_falls_back_when_jj_is_not_a_repo(repo, capsys):
    diff = "+++ b/src/good.md\n@@ -0,0 +1,1 @@\n+Good citations: [CR#702.22a]\n"
    results = [subprocess.CompletedProcess([], 1, stdout="", stderr="There is no jj repo"),
               subprocess.CompletedProcess([], 0, stdout=diff)]
    with patch.object(sys, "stdin", _tty_stdin()), patch("subprocess.run", side_effect=results) as run:
        assert main(["--config", str(repo.root / "cfg-good.json"), "audit", "--diff"]) == 0
    assert run.call_args.args[0][:3] == ["git", "-C", str(repo.root)]
    assert "audited 2 citation site(s)" in capsys.readouterr().out


def test_interactive_audit_diff_reports_missing_tools(repo, capsys):
    with patch.object(sys, "stdin", _tty_stdin()), patch("subprocess.run", side_effect=FileNotFoundError()):
        assert main(["--config", str(repo.root / "cfg-good.json"), "audit", "--diff"]) == 1
    assert "neither jj nor git" in capsys.readouterr().err


@pytest.mark.parametrize("source", [
    "const K: &'static str = \"100.1\"; // cite: allow-noncompliant-line -- parser's key\n",
    "fn f<'a, 'b>(x: &'a str) -> &'b str { r\"\\\" } // cite: allow-noncompliant-line -- it's fine\n",
    "let p = r\"\\\"; // cite: allow-noncompliant-line -- raw backslash\nlet q = \"x\";\n",
])
def test_exemption_lexer_handles_lifetimes_and_zero_hash_raw_strings(source):
    assert exempt_lines(source) == {1}


def test_exemption_lexer_still_quotes_apostrophe_strings():
    source = "echo 'a b' # cite: allow-noncompliant-line -- shell\nx = 'it // not'\n"
    assert exempt_lines(source) == {1}
    assert exempt_lines("x = '// cite: allow-noncompliant-line -- quoted'\n") == set()


def test_context_matches_dotted_out_of_scope_keys(repo, capsys):
    config = json.loads((repo.root / "cfg-good.json").read_text())
    config["coverage"] = {"out_of_scope": {"702.22": "x", "100": "y", "800..999": "z", "bogus": "w", "100.1": "v"}}
    (repo.root / "cfg-good.json").write_text(json.dumps(config))
    with patch.dict(os.environ, {"MTG_RULES_DATA": str(repo.root / "data")}), \
            patch.object(sys, "stdin", io.StringIO("[CR#702.22a]")):
        assert main(["--config", str(repo.root / "cfg-good.json"), "context"]) == 0
    captured = capsys.readouterr()
    assert "[CR#702.22a]  ·  out-of-scope range" in captured.out
    assert "bogus" in captured.err


def test_download_reports_each_url_on_stderr(tmp_path, capsys):
    source = tmp_path / "source.txt"
    source.write_text("data")
    download(source.as_uri(), tmp_path / "out")
    assert source.as_uri() in capsys.readouterr().err


def test_setup_reports_destination_on_stderr(tmp_path, capsys):
    with patch("mtg_rules.setup_data.download", side_effect=OSError("stop")), pytest.raises(OSError):
        setup(tmp_path / "dest")
    assert str(tmp_path / "dest") in capsys.readouterr().err
