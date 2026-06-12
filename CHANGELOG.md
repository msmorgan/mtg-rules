# Changelog

**Consumers pin the version manifest** (`skill/scripts/version` →
`{plugin_version, git_commit, cr_effective, keywords_classified_sha}`) as
their conformance baseline; **a version bump here is the re-sync trigger** —
re-run your alignment pass against the new taxonomy and data before
re-pinning. Taxonomy-meaning changes (reclassifications, primitive
mints/retirements, notation changes) are always called out explicitly.

## Unreleased

- `scripts/cite check`: new staleness class **MALFORMED** — a token with the
  bracketed shape (`[CR#…]`) whose contents fail citation parsing is now
  reported (`MALFORMED <token> <file>:<line>`), counted as stale (non-zero
  exit), and listed alongside GONE/CHANGED/UNLOCKED. Previously such tokens
  were silently skipped (inherited from the Rust checker) and invisible to
  `--list-noncompliant` too (its blanking step removes the whole `[CR#…]`
  span before the wide-net patterns run). Additive only — no flag or
  subcommand changes; `list`/`bless` still skip malformed tokens.
  Consumer-requested (deckmaste.rs alignment pass, 2026-06-11).

## 1.7.0 — 2026-06-11

Consumer-driven release (first consumer: deckmaste.rs): taxonomy
corrections + conformance plumbing. The `scripts/cite` CLI surface is now a
cross-repo compatibility contract (deckmaste's `cargo xtask cite` is a live
shim over it); flag/subcommand changes need a matching consumer look before
landing.

### Taxonomy-meaning changes

- **Enlist, Foretell, Hidden Agenda → composite** (were composite-given).
  Enlist's `given: cause-tagged-events` tag contradicted its own `how`
  rationale; the CR names the composition explicitly (702.154a/b: an
  optional cost to attack, 508.1g, plus a linked trigger, 607.2h). The
  composite-given sweep returned Foretell and Hidden Agenda to plain
  composite on the same standard. Counts for this step: composite-given
  23 → 20, composite 212 → 215.
- **Vigilance → intrinsic; the `cause-tagged-events` primitive is retired.**
  New dependents discipline, codified in `keyword-classification.md`: a
  `given` primitive must have ≥ 2 keyword dependents; a sole-dependent
  primitive collapses into its keyword as intrinsic. After the Enlist fix,
  `cause-tagged-events` had exactly one dependent. Counts for this step:
  intrinsic 24 → 25 (abilities 8 → 9, actions stay 16), composite-given
  20 → 19. Net across both steps: intrinsic 25, composite-given 19,
  composite 215, marker 1; total stays 260. (`underdetermined.md` U3
  records the retirement as settled-by-policy.)
- **Gate vs Toll**: the two "MayIf" flavors get distinct names in
  `deontics.md` — *Gate* (declaration-gating) vs *Toll* (resolution-stage) —
  and the keyword `how`-field deontic notation was swept to use them.
- **Haste**: worked deontic entry takes a position on its spelling — a
  *flag* read by the standing summoning-sickness Cant rows, not a May-row
  lift (508.1a and 602.5a name haste in their own conditions, so there is
  no permission row to widen; 702.10b–c and 302.6 are prose mirrors).

### Conformance plumbing

- `scripts/cite`: config-driven citation checker with a text-drift lockfile
  (`skill/cr-citations.lock`, normalized-text checksums; staleness classes
  CHANGED/GONE/UNLOCKED) — replaces the old check-citations script.
- `scripts/version`: machine-readable conformance manifest (see top note).
- New lookup surface: `scripts/lookup` (unified meta-search),
  `scripts/classify` (per-keyword classification record),
  `scripts/health` (self-diagnosis incl. per-reference-doc staleness
  warnings), `scripts/underdetermined` (registry entry lookup by id).
- `keywords-classified.json`: every record gains a PascalCase `ident`
  (engine-enum spelling, e.g. First Strike → FirstStrike; derivation rule
  documented in `meta.ident_rule`) for mechanical drift-guarding of
  consumer keyword enums.
- Harness lints: a composite-given `how` must name its `given` primitive;
  every `given` must be in `meta.given_vocabulary`.
- `underdetermined.md`: durable `UD-NNN` entry ids with the category on
  every entry line; convention documented — the skill records what the CR
  underdetermines, engine-agnostically; consumers ADR-key their choices by
  UD id.
- Data-dir layout documented as a versioned contract (README), including
  who builds `derived/`.
- `evals/coverage.fish`: corpus coverage report — % of distinct supported
  oracle lines matched per taxonomy kind + union coverage.

## 1.2.0 → 1.6.0 (pre-changelog history, reconstructed from the jj log)

- **1.6.0** — variants index (`variants.md`), rulings-check expansion,
  carrier fold, SKILL.md routing table.
- *(1.3.0–1.5.0 were never tagged; their work shipped with 1.6.0:)*
  generalizations reference (asymmetric rule families); keyword
  intrinsic/composite classification + engine primitive basis; deontics
  reference (May/Cant/Must/toll algebra) + deontic notation in keyword
  how-fields; cost/event/choice/information/outcome and query/mana/temporal
  taxonomies; underdetermined-semantics registry.
- **1.2.0** — first marketplace release: plugin/marketplace manifests,
  `setup-data` fetcher, data resolution chain (`$MTG_RULES_DATA` → plugin
  data dir → repo layout), core lookup scripts (rule, rule-search, define,
  keyword, mtr, card, corpus, rulings, check-citations) and the synthesized
  reference-doc roster (state, actions, designations, abilities, effects,
  casting, turn, grammar, engine, rulings-check).
