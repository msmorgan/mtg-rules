---
needs: []
---

# Port `cite` from fish and jq to Python

Rewrite `skills/mtg-rules/scripts/cite` in Python. Today it is 533 lines of
fish plus `scripts/cite-lib/{sites,resolve,classify,texts,noncompliant,audit}.jq`,
with data-dir discovery from `scripts/lib.fish`. The rewrite should keep the
same behavior, so callers and the existing harness don't change. This ticket
is the base that `cite-xtask-parity` builds on.

## Decisions

- **Same executable, same interface.** The script stays at `scripts/cite`,
  now with a `python3` shebang. It keeps the same subcommands:
  `check [--list-noncompliant]`, `bless`, `list`, `show [--plain]`, `diff`,
  `audit [--diff] [files…]`, and `context [--seen F] [--full] [--max N]`.
  It also keeps the same global `--config FILE`, config schema, environment
  variables (`MTG_RULES_DATA`, `MTG_RULES_CITE_WIZARDS_URL`), output lines and
  exit codes. Its callers then need no change:
  - `scripts/hooks/cite_context.fish`
  - `tests/test_skill_scripts.fish`
  - SKILL.md and README
  - deckmaste.rs's config
- **Lockfile and checksums are unchanged.** The lockfile is JSON with
  `checksums`, `cr_date` and `wizards_url`, and keys are sorted. Each checksum
  is the first 16 hex characters of SHA-256 over whitespace-normalized rule
  text. Existing locks in this repo, in `evals/` and in deckmaste.rs must
  verify unchanged.
- **Standard library only.** The plugin has no install step.
- **Data discovery moves into the Python module.** It replicates `lib.fish`'s
  chain: `MTG_RULES_DATA`, then the host plugin data dirs, then
  `<plugin>/data`. Fish scripts keep using `lib.fish`.
- **Fixing bugs is allowed.** The `cite-xtask-parity` bugs, such as range
  order, may be fixed here when that's cheaper than porting them, provided a
  test covers each fix.

## Done when

- `fish tests/test_skill_scripts.fish` passes with its existing `cite` and hook
  assertions unchanged.
- `scripts/cite check` and `scripts/cite --config evals/cite-config.json check`
  give the same results as the fish version on this repo.
- Python unit tests for the module run under the repo's test gates. Add them to
  CLAUDE.md's "Before completing skill changes" commands.
- The fish implementation and `cite-lib/*.jq` are deleted.

## Open

- **Minimum Python version.** jj-kata already requires 3.11. The plugin's
  hosts run `python3` for the evals today.

## Completion

Implemented with Python 3.11+ and the jj-sensei layout: a thin executable,
`src/mtg_rules`, `pyproject.toml`, and a development-only pytest/Ruff toolchain.
The citation runtime uses only the standard library (plus jj for tracked-file
listing and interactive diff acquisition). The existing lockfiles are unchanged.

Validation: 250 shell assertions and 23 Python tests passed; Ruff passed.
The skill and eval citation checks retain their original results: 7,813 and
263 checked citations respectively, both with zero stale. Fixture setup now
copies `src/` instead of the removed jq library; existing assertions are intact.
