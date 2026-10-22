# Citation fixtures

`xtask-cases.json` maps all 33 citation tests in deckmaste.rs's
`crates/xtask/src/cite.rs` as inspected on 2026-10-22. Each `origin` is the
upstream test name; `test_cite_parity.py` executes every fixture. The small
`xtask-cr.txt` carries its synthetic rule bodies, with reordered JSON generated
by the test to expose accidental dependence on JSON key order.

The plugin keeps JSON rule bodies for checksum compatibility while using the
text document for order. The raw-text parser also handles continuation lines
and excludes examples for URL diffs, matching the upstream text parser.

Exemption tests have deliberate adaptations: xtask validates Rust AST positions
and hardcodes catalog paths/helpers; this plugin uses language-independent
comment markers. Its new `allow-noncompliant` spelling opts into whole-line or
whole-scope exemptions. Legacy marker fixtures must still produce diagnostics,
including wrong helpers, wrong files and shadowing: those annotations do not
acquire broader powers during migration. The `adaptation` fields identify other
contract differences, including the retained `noncompliant_exempt` config key.
Additional tests cover structural marker errors, quoted-marker spoofing,
numbered/lettered boundaries, two-digit minors, source filters, JSON output,
local edition retention, failed refreshes and the dependency-free hook.
