# mtg-rules

This repo is three things at once: a **Codex and Claude Code plugin marketplace** (`.agents/plugins/marketplace.json` and `.claude-plugin/marketplace.json`, both sourcing the repository root), the **development home of the mtg-rules skill** (`skills/mtg-rules/`), and the **data workspace** that grounds it (`data/`, gitignored, 2.3 GB fetched). The skill's purpose: judge-grade MTG rules answers and implementation-facing taxonomies for an MTG engine + card-grammar project.

## Layout

- `skills/mtg-rules/SKILL.md` — triggers, rigid workflow, routing to docs/scripts.
- `skills/mtg-rules/references/*.md` — synthesized reference docs (see SKILL.md's table for the roster).
- `skills/mtg-rules/scripts/` — fish lookup tools (`rule`, `rule-search`, `define`, `keyword`, `card`, `rulings`, `mtr`, `corpus`, `cite`, `setup-data`); all source `lib.fish`, which resolves data via `$MTG_RULES_DATA` → the current host's persistent plugin data directory → repo-relative.
- `skills/mtg-rules/keywords-classified.json` — all keywords classified intrinsic / composite / composite-given(P) / marker.
- `scripts/` — repo-level data pipeline (`fetch_data.fish`, `build_derived.fish`).
- `tests/test_skill_scripts.fish` — the assertion harness; every script change is TDD'd here.

## The distillation approach (how the reference docs are made)

The Comprehensive Rules are the only authority; the docs are **synthesis with receipts**:

1. **Never write from memory.** Every claim is verified through the lookup scripts against the local CR before it's written. Rule numbers guessed in plans/briefs are treated as hypotheses for the implementer to confirm or correct.
2. **Dotted citation on every claim.** `skills/mtg-rules/scripts/cite check` machine-verifies that every `NNN.Nx` cited anywhere in `references/` and the keywords JSON exists in the current CR *and* that its text still matches the lockfile (`skills/mtg-rules/cr-citations.lock` pins normalized-text checksums; staleness classes CHANGED/GONE/UNLOCKED/MALFORMED) — the staleness tripwire for quarterly CR updates. Accept intended rewording with `cite bless`.
3. **Adversarial review before merge.** Each doc gets a refutation pass: a reviewer tries to *break* claims against the CR text (and official rulings via `scripts/rulings`). Fixes are re-verified. Reviewer errors get caught too — fix agents re-verify prescriptions before applying them.
4. **Closed lists in full; open vocabularies by pointer** (to `data/catalogs/*.json`). Taxonomies are written implementation-facing: enumerable, typed, citing per row.
5. **Ground truth beyond the CR**: `references/rulings-check.md` validates derivations against WotC's official card rulings; the worked examples in `effects.md` quote rulings verbatim with dates.
6. **Honesty about gaps**: claims the CR underdetermines are flagged as engine inference and registered in `references/underdetermined.md` (admission standard: an entry survives only if no rule settles it). Design-space asymmetries live in `references/generalizations.md`.
7. **Doc conventions**: italic synthesized-from-CR header (with effective date), ≤ ~300 lines, cross-ref sibling docs instead of duplicating, maintenance note where applicable.

## Working in this repo

- **VCS is jj** (colocated). Use jj exclusively. **Never push or move bookmarks autonomously** — the user owns pushes; report "N commits ahead of origin" instead.
- **Parallel subagents must not run jj/git** — jj snapshots the whole working copy, so a commit from one agent captures others' half-written files. Batch work: write files only; one final agent commits.
- The Bash tool runs `/bin/bash` even though the env reports fish — invoke the fish scripts as executables; don't use fish syntax inline.
- Verification before completion: `fish tests/test_skill_scripts.fish` (all green) and `cd skills/mtg-rules && scripts/cite check` (exit 0) before any commit that touches `skills/mtg-rules/`.
- Prefer the most capable model tier for synthesis/review subagents; cheap tiers only for mechanical fixes/wiring.

## Refresh workflow (after WotC updates)

`scripts/fetch_data.fish` → `scripts/build_derived.fish` → `skills/mtg-rules/scripts/cite check` (for each CHANGED hit: `cite diff <rule>`, fix the doc or accept the rewording; GONE/UNLOCKED/MALFORMED: fix the cite; then `cite bless` to re-pin the lockfile) → re-derive the probes in `references/rulings-check.md` → re-test `references/underdetermined.md` entries (a new rule may settle one) → re-examine `references/generalizations.md` empty cells (a newly printed instance is a finding).
