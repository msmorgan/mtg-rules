---
needs: [cite-python-port]
---

# Bring `cite` to parity with deckmaste.rs's `xtask cite` (coverage excepted)

deckmaste.rs's `cargo xtask cite` lives in `crates/xtask/src/cite.rs`, about
2,300 lines of Rust. It began as a shim over this plugin's `cite` in June
2026. In August it was re-implemented in Rust ("ci: make citation checking
repository owned") because deckmaste.rs's CI could not pin the plugin without
submodules. That blocker is gone: CI can check out mtg-rules at a pinned tag.

The goal is for the plugin to own citation checking, so `xtask cite` can
become a pinned shim again. This ticket brings the plugin's `cite` to
everything `xtask cite` does today except the coverage ratchet, which is
`cite-coverage-ratchet`. A 2026-10-22 comparison found the two tools share
their config schema, lockfile format, checksums, citation grammar, staleness
classes and noncompliance patterns. The gaps follow.

## Gaps to close

- **Ranges expand in document order.**
  - `xtask` builds the order from `cr.txt` line order (`cite.rs:601-671`,
    `803-806`). The plugin uses `cr.json` key order, which is not document
    order:
    - single-digit minors come first;
    - lettered children are grouped away from their parents;
    - two- and three-digit minors sort lexically, so 701.70 sorts before 701.7a.
  - Parent-to-child ranges over-expand by hundreds of rules: `112.1..112.1b`,
    `109.2..109.2b`.
  - Number-to-number ranges silently drop lettered children: `118.5..118.6`
    loses 118.5a.
  - On deckmaste.rs, 11 of 14,301 sites expand differently, which causes 981
    false UNLOCKED results. Here, `oracle-style.md`'s `721.1..721.4` drops the
    lettered subrules.
- **Symlinks are skipped in source discovery** (`cite.rs:544-599`). deckmaste.rs's
  `AGENTS.md` is a symlink to the excluded `CLAUDE.md`, so the plugin scans it
  and reports 4 extra sites and 3 noncompliant hits.
- **Glob mode applies `exclude` and `extensions`** (`cite.rs:544-575`). The
  plugin's `find -path` path ignores both.
- **`audit --diff` handles paths with spaces.** Read the `+++ ` path up to a
  TAB, as `cite.rs:1568-1635` does. The plugin's awk takes `$2`.
- **In-source noncompliance exemptions.** `xtask` accepts markers in Rust
  files, validated with syn and hard-coded to deckmaste.rs's catalog crate
  (`cite.rs:1023-1150`, `1200-1210`):
  - `// cite: noncompliant begin/end -- reason` around a block;
  - `// cite: noncompliant-line -- reason` on a single line.

  Design a language-agnostic marker that the plugin honors, keeping the
  existing `noncompliant_exempt` config key. Reject markers inside string
  literals where that is cheap. deckmaste.rs's 54 exempt hits are in
  `crates/deckmaste_catalogs/src/{cr,lib,legacy}.rs`.
- **`diff` works.** Both tools fetch `lock.wizards_url`, but
  `https://academyruins.com/link/cr` now answers with an HTML landing page, so
  every rule reads as absent from the old edition. Keep the previous CR edition
  locally: `setup-data` retains the prior `cr.json` and `cr.txt` on refresh,
  and `diff` reads them. Fall back to a URL only when it serves plain text.
- **Add `cite list --json`,** giving file, line, token, status and expanded
  members per site, for consumers such as the coverage ratchet.
- **Port `xtask`'s 33 citation tests as fixtures**
  (`crates/xtask/src/cite.rs` `#[test]`s). They cover:
  - ranges, including reversed ranges and skipped letters;
  - stale versus malformed;
  - noncompliance cases and bless;
  - audit selection and the spaced-path diff parser;
  - symlinks.

  Also add a range that crosses the numbered/lettered boundary, and one
  over two-digit minors.

## Done when

Run from deckmaste.rs with `--config cite-config.json`, compared with
`target/debug/cargo-xtask cite`:
- `list` output is identical (14,301 sites at the time of writing);
- `check` reports the same citation count with 0 stale (17,561 at the time of
  writing);
- `check --list-noncompliant` reports 0 once deckmaste.rs carries the new
  markers. Before that, the only hits are the known catalog-crate ones.

Also:
- the runtime is within about 1 s on deckmaste.rs (`xtask` 0.26 s, current
  plugin 3.3 s);
- this repo's gates still pass.

## Out of scope

Switching deckmaste.rs over is a separate deckmaste.rs ticket: `xtask cite`
becomes a shim that runs the plugin's `cite` at a version pinned in
`cite-config.json` and checked against `scripts/version`, with a CI checkout of
mtg-rules at that tag.
