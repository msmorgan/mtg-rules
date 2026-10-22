"""Contract tests for the dependency-free citation runtime."""

import contextlib
import io
import json
import os
import shutil
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from mtg_rules.cite import Repository, Snapshot, checksum, main, scan, stale
from mtg_rules.data import discover_data

FIXTURES = Path(__file__).parent / "fixtures/cite"


class CiteTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        shutil.copytree(FIXTURES, self.root, dirs_exist_ok=True)
        self.snapshot = Snapshot(self.root / "data/rules")
        self.repo = Repository(self.root / "cfg-good.json")

    def run_cli(self, *args, text=""):
        output = io.StringIO()
        with patch.dict(os.environ, {"MTG_RULES_DATA": str(self.root / "data"),
                                     "MTG_RULES_CITE_WIZARDS_URL": (self.root / "old-cr.txt").as_uri()}), \
                patch("sys.stdin", io.StringIO(text)), contextlib.redirect_stdout(output):
            status = main(["--config", str(self.root / "cfg-good.json"), *args])
        return status, output.getvalue()

    def test_lock_compatible_and_whitespace_stable(self):
        self.assertEqual(checksum(" First\n child.  "), checksum("First child."))
        self.assertEqual(checksum("First child."), "9d3f2db28ef2b4d6")
        status, output = self.run_cli("bless")
        self.assertEqual(status, 0)
        self.assertIn("blessed 6 rules", output)
        lock = json.loads(self.repo.lock_path.read_text())
        self.assertEqual(set(lock), {"checksums", "cr_date", "wizards_url"})
        self.assertEqual(self.run_cli("check")[0], 0)

    def test_resolution_distinguishes_invalid_and_missing(self):
        for raw in ("", "word", "104.4b-class", "100.1, 702"):
            self.assertEqual(self.snapshot.resolve(raw), ("skip", []))
        for raw in ("…", "...", " … "):
            self.assertEqual(self.snapshot.resolve(raw), ("placeholder", []))
        self.assertEqual(self.snapshot.resolve("999.9"), ("ok", ["999.9"]))
        self.assertEqual(self.snapshot.resolve("704.5n..704.5k"), ("gone", []))
        self.assertEqual(self.snapshot.resolve("704.5k..704.5n"),
                         ("ok", ["704.5k", "704.5m", "704.5n"]))

    def test_stale_classes(self):
        sites = scan("[CR#100.1] [CR#702] [CR#999.9] [CR#xyz] [CR#…]", "f", "bracketed", self.snapshot)
        report = stale(sites, {"100.1": "new", "702": "same"}, {"100.1": "old"})
        self.assertEqual([line.split()[0] for line in report], ["CHANGED", "UNLOCKED", "GONE", "MALFORMED"])

    def test_bare_scan_contract(self):
        sites = scan("100.1a 704.5aa 702", "f", "bare", self.snapshot)
        self.assertEqual([site["raw"] for site in sites], ["100.1a"])

    def test_context_cap_only_ledgers_shown_rules(self):
        ledger = self.root / "seen"
        status, output = self.run_cli("context", "--seen", str(ledger), "--max", "1",
                                      text="[CR#100.1,702,999.9]")
        self.assertEqual(status, 0)
        self.assertIn("2 more first-seen citations", output)
        self.assertEqual(ledger.read_text(), "100.1\n")
        self.assertEqual(self.run_cli("context", "--seen", str(ledger), text="[CR#100.1]")[1], "")

    def test_no_external_process_for_glob_check(self):
        self.run_cli("bless")
        with patch("subprocess.run", side_effect=AssertionError("external dependency")):
            self.assertEqual(self.run_cli("check")[0], 0)
            self.assertEqual(self.run_cli("list")[0], 0)
            self.assertEqual(self.run_cli("show", "702")[0], 0)
            self.assertEqual(self.run_cli("diff", "702.22a")[0], 0)

    def test_data_precedence_and_fallback(self):
        home = self.root / "home"
        skill = home / ".codex/plugins/cache/mtg-rules/skills/mtg-rules"
        host = home / ".codex/plugins/data/mtg-rules/data"
        (host / "rules").mkdir(parents=True)
        (host / "rules/cr.json").write_text("{}")
        env = {"HOME": str(home), "PLUGIN_DATA": str(self.root / "data-v2")}
        self.assertEqual(discover_data(skill, env), self.root / "data-v2")
        env["MTG_RULES_DATA"] = str(self.root / "data")
        self.assertEqual(discover_data(skill, env), self.root / "data")
        self.assertEqual(discover_data(skill, {"HOME": str(home)}), host)


if __name__ == "__main__":
    unittest.main()
