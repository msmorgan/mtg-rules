---
needs: [cite-xtask-parity]
---

# A configurable CR-coverage ratchet in `cite`

Move the coverage ratchet out of deckmaste.rs (`crates/xtask/src/coverage.rs`,
741 lines, run as `cargo xtask cite coverage [--check|--bless]`) into the
plugin, driven by config. All citation tooling would then be owned by the
plugin.

## What it does today

- **Tiers.** It files every cited rule under the strongest tier any of its
  citation sites reaches, by path:
  - Mentioned: `docs/` or `.md` files;
  - Tested: `/tests/`, `/Proofs/` or `plugins/testing/`;
  - Bound: everything else.

  It also reads `#[cr("…")]` attributes.
- **Lock.** A committed `cr-coverage.lock` holds two sets: `tested`, and
  `strong` (Tested plus Bound). `--check` fails if a rule leaves either set.
  `--bless` re-records the sets.
- **Report.** With no flag, it divides by the `cr.json` rules minus
  `coverage.out_of_scope`. That key takes a whole section (`123`), a section
  range (`800..999`) or a rule prefix (`103.4`). Each key must match an
  existing rule and carry a non-empty reason.
- **Current numbers** on deckmaste.rs: 619 tested, 1,587 strong.

## Decisions

- **Configuration.** Everything deckmaste.rs-specific becomes config under
  `coverage`:
  - tier names and their path globs, in strength order;
  - which tier unions are ratcheted;
  - extra citation extractors as regexes (for example the `#[cr("…")]`
    attribute);
  - the lockfile path;
  - `out_of_scope`.
- **Shared parser.** It reads sites through the same parser and resolver as
  `cite list --json`, not through its own scanner. That fixes two defects in
  today's scanner:
  - a `A..B` range yields only its endpoints, so `112.1..112.1b` misses 112.1a;
  - text matching on `#[cr(` put junk entries in the lock, such as
    `")\n .and_then(|rest| rest.strip_suffix('`.
- **Hard-coded lists become config.** Today's skip directories and extensions
  (`coverage.rs:89-98`) become config, with defaults that reproduce
  deckmaste.rs's current behavior.

## Done when

- With deckmaste.rs's config translated, the ratchet reproduces its `tested`
  and `strong` sets. The only differences are those explained by the two
  scanner fixes, and they are listed in the change description.
- `cite coverage --check` and `--bless` behave like `xtask`'s. The two flags
  conflict, and a regression message names the rule and the tier it lost.
