# Changelog

**Consumers pin the version manifest** (`skills/mtg-rules/scripts/version` →
`{plugin_version, git_commit, cr_effective, keywords_classified_sha}`) as
their conformance baseline; **a version bump here is the re-sync trigger** —
re-run your alignment pass against the new taxonomy and data before
re-pinning. Taxonomy-meaning changes (reclassifications, primitive
mints/retirements, notation changes) are always called out explicitly.

## 1.9.0 — 2026-08-07

- **Bracketed card context.** A `UserPromptSubmit` hook resolves exact card
  names such as `[Brazen Cannonade]` and injects their full local card data
  into the same turn's context. Repeated names are deduplicated and invalid
  bracketed prose is ignored. Canonical combined names such as
  `[Start // Finish]` render every face; a lone face name is not treated as a
  full card name. **No taxonomy or CR-data change.**

## 1.8.4 — 2026-08-04

**Citation context hook fixes**, all found by turning `CITE_ON_BASH` on:

- **Large payloads produced nothing.** The hook passed tool output through
  argv, and Linux caps a *single* argument at 128 KB — `cite list` output
  (~700 KB) failed the exec and the annotation vanished silently. Every stage
  now moves through files.
- **Calls into this skill are exempt on `Bash`.** `rule`, `cite show`,
  `cite audit` already print rule text; annotating them duplicated it. Both
  path and bare command-position invocations are recognized, and a test
  asserts the exempt list covers `scripts/`.
- **Reports are capped** at 40 rules (`CITE_CONTEXT_MAX`, `0` lifts it).
  Uncapped, one `cite list` in a large consumer repo injected ~53k tokens.
  Truncation states how many citations were held back; the session ledger
  records only what was actually shown.
- **Tests are hermetic against `set -Ux`.** `CITE_ON_*` is exactly the kind
  of switch a developer exports universally, and fish hands universals to
  every child regardless of the parent environment — the default-off
  assertions used to pass or fail depending on who ran them.

## 1.8.3 — 2026-08-04

**Citation context hook.** A new `PostToolUse` hook (`hooks/hooks.json` →
`skills/mtg-rules/scripts/hooks/cite_context.fish`) prints the official CR
text for citations seen for the first time in a session, turning a rule
number written into code into an immediate claim-vs-rule-text check. It is
scoped to repos that consume the skill — those whose VCS root holds a
`cite-config.json` — so this repo's own tree is excluded and unrelated
projects pay ~11 ms per tool call. `Write`/`Edit` are annotated by default;
`Read` and `Bash` are opt-in via `CITE_ON_READ` / `CITE_ON_BASH`
(`CITE_CONTEXT_FULL`, `CITE_CONTEXT_OFF` also recognized). Backed by a new
`cite context` subcommand, which reads text on stdin and reuses the existing
resolver, lockfile, and coverage config. **No taxonomy or CR-data change.**

## 1.8.2 — 2026-08-03

Codex packaging and runtime compatibility: the canonical skill now lives at
`skills/mtg-rules/`, the repository has native Codex plugin and marketplace
manifests plus skill UI metadata, and installed Codex copies resolve their
data from a persistent directory outside the versioned plugin cache. Claude
Code and agy continue to use the same canonical skill tree. **No taxonomy or
CR-data change.**

## 1.8.1 — 2026-07-19

Skill **description** (frontmatter) trimmed to trigger-only: mechanism and
post-fire-behavior prose that already lives in the skill body was moved out
of the always-loaded router, cutting per-session token cost. **No taxonomy,
CR data, or behavior change** — `cr_effective` and `keywords_classified_sha`
are unchanged, so consumers pinning the version manifest need no re-sync.

## 1.8.0 — 2026-07-09

CR refresh to the **June 19, 2026** Comprehensive Rules (Marvel Super
Heroes / MSH, the SOS→MSH diff) plus the pending citation-tooling change.
Re-synthesized against the new CR: all cited rules re-verified
(`cite check` clean, lockfile re-blessed at `cr_date 2026-06-19`), all 18
`rulings-check.md` probes still MATCH, no `underdetermined.md` entry newly
settled, no `generalizations.md` empty cell newly filled. The effective-date
header on every reference doc is now 2026-06-19.

### Taxonomy additions

- **Three new keywords classified** (all `composite`): **Heal** (701.69,
  action — remove marked damage, reusing the cleanup/regeneration
  operation), **Power-up** (702.193, ability — conditional self-cost-reduction
  if it entered this turn + "activate only once", cf. Affinity + Exhaust),
  **Teamwork** (702.194, ability — optional additional cost tapping creatures
  of total power N, plus a "cast using teamwork" was-X memory, cf.
  Bargain/Kicker). Counts: total **260 → 263** (ability 192 → 194, action
  68 → 69), composite **215 → 218**. No existing row was reclassified — purely
  additive, but the count/`keywords_classified_sha` change is a consumer
  re-sync trigger for enum drift-guards.

### Citation fixes (CR renumbering)

- **601.5–601.7 block renumber.** The MSH CR inserted a new 601.5
  ("announcing targets — options available only if other choices are made
  later"), shifting the block: old 601.5→601.6 (prohibition rewind),
  601.5a→601.6a (conditional flash), 601.6/a/b→601.7/a/b (opponent choices),
  601.7→601.8 (cost-altering doesn't touch the stack). All sites in
  `casting.md`, `choices.md`, `generalizations.md` re-pointed; content
  unchanged.
- **Connive block renumber (topic-drift, hash-checker-invisible).** Old
  701.50c (connive LKI) → 701.50b and old 701.50e (Connive N) → 701.50d, with
  a brand-new 701.50e (connive 0). The cites in `underdetermined.md`
  (701.50c→701.50b) and `keywords-classified.json` Connive (701.50e→701.50d)
  now point at the intended rules — a re-point `cite bless` would otherwise
  have silently re-pinned to the wrong topic.

### Tooling

- `scripts/cite audit [--diff] [files…]`: new subcommand that prints each
  citation site's claim line next to the **full official text** of every rule
  it cites — the semantic check the checksum checker can't do (it proves a
  rule *exists*, not that it's the rule the claim names). `--diff` audits only
  the lines added in a unified diff (stdin, or `jj diff`/`git diff`). And
  `cite bless` now prints a **"newly registered rule(s)"** list so each cite
  entering the lock gets one forced glance against its claim — the cheapest
  point to catch a right-number-wrong-topic cite.
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
  (`skills/mtg-rules/cr-citations.lock`, normalized-text checksums; staleness classes
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
