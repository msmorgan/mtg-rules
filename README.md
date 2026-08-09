# mtg-rules

Marketplace and development repository for the **mtg-rules** plugin — a judge-grade Magic: The Gathering rules skill grounded in the Comprehensive Rules, with verified citations and synthesized engine/grammar taxonomies. Compatible with **Codex**, **Claude Code**, and **Google Antigravity (agy)**.

## Installation

### Codex

Add this repository as a marketplace, then install the plugin:

```bash
codex plugin marketplace add msmorgan/mtg-rules
codex plugin add mtg-rules@mtg-rules-dev
```

For local development, pass the checkout path instead of `msmorgan/mtg-rules`.
Start a new Codex thread after installation so the bundled skill is loaded.

### Claude Code

Install via the plugin marketplace:

```
/plugin marketplace add /path/to/mtg-rules
# or a repo URL:
/plugin marketplace add https://github.com/msmorgan/mtg-rules

/plugin install mtg-rules@mtg-rules
```

### Google Antigravity (agy)

Install globally by cloning or copying the repository into your global plugins directory:

```bash
git clone https://github.com/msmorgan/mtg-rules ~/.gemini/config/plugins/mtg-rules
```

Or for a specific workspace, clone or copy the repository into `.agents/plugins/mtg-rules` under your project root:

```bash
mkdir -p .agents/plugins
git clone https://github.com/msmorgan/mtg-rules .agents/plugins/mtg-rules
```

### Automatic First-Run Data

The plugin automatically downloads its hook runtime—base rules, catalogs, and
MTGJSON's `AllPrintings.sqlite`—into persistent host storage before the first
model turn. Codex and Claude Code use `SessionStart`; agy uses its equivalent
`PreInvocation` hook. A lock prevents concurrent sessions from duplicating the
download, payloads are validated in staging, and a data-ABI marker makes
later session checks local and fast. Hook setup failures produce a warning but
do not block prompts or tools.

Required local tools are `fish`, `curl`, `jq`, `xz`, and `sqlite3`.

The first run requires hook trust on hosts that prompt for newly installed hook
definitions. If automatic setup reports a failure, retry from the plugin root:

```bash
skills/mtg-rules/scripts/setup-data --runtime
```

**Data tiers** (all are idempotent — re-run to refresh):

| Tier | Flag | Size | Enables |
|------|------|------|---------|
| Base rules + catalogs | *(default)* | ~4 MB | `rule`, `define`, `keyword`, `mtr`, `cite` |
| Hook runtime | `--runtime` | large | base + `card`, `rulings`, hooks |
| Card corpus | `--cards` | ~790 MB | runtime + `corpus` |
| Official rulings DB | `--rulings` | large | `rulings` |

Example — refresh the automatic runtime:

```bash
skills/mtg-rules/scripts/setup-data --runtime
```

Example — full install:

```bash
skills/mtg-rules/scripts/setup-data --cards
```

When available, data lands in the host-provided `$PLUGIN_DATA` (Codex) or
`$CLAUDE_PLUGIN_DATA` (Claude Code). Otherwise it uses
`$CODEX_HOME/plugins/data/mtg-rules/data/` (or
`~/.codex/plugins/data/mtg-rules/data/`) for Codex,
`~/.gemini/config/plugins/mtg-rules/data/` for agy, or
`~/.claude/plugins/data/mtg-rules/data/` for Claude Code. Set
`$MTG_RULES_DATA` or pass `--dest` to override it.

## Development Setup (Repo Checkout)

```bash
git clone https://github.com/msmorgan/mtg-rules
cd mtg-rules
scripts/fetch_data.fish          # populate data/ in-repo

# Optional: symlink skill into your personal skills directory
ln -s "$PWD/skills/mtg-rules" ~/.claude/skills/mtg-rules
```

Set `MTG_RULES_DATA` to override where scripts look for data:

```fish
set -x MTG_RULES_DATA /path/to/your/data
```

## Data Directory Contract (versioned)

The on-disk layout under the resolved data dir (`$MTG_RULES_DATA` →
host-specific plugin data → repo `data/`) is a compatibility
contract, versioned with the plugin (current: 1.10.0; layout changes are
called out in [CHANGELOG.md](CHANGELOG.md)). Consumers pin the manifest from
`skills/mtg-rules/scripts/version` and re-sync on any bump.

| Tier | Files | Built by | Enabling scripts |
|------|-------|----------|------------------|
| base | `rules/cr.txt`, `rules/cr.json`, `rules/glossary.json`, `rules/unofficial-glossary.json`, `rules/keywords.json`, `rules/mtr.json`, `catalogs/*.json` | fetched: `skills/mtg-rules/scripts/setup-data` or repo `scripts/fetch_data.fish` | `rule`, `rule-search`, `define`, `keyword`, `mtr`, `lookup`, `classify`, `underdetermined`, `cite`, `health`, `version` |
| runtime | base + `mtgjson/AllPrintings.sqlite` | automatic hook bootstrap or `setup-data --runtime` | all base scripts, `card` (SQLite), `rulings`, hooks |
| cards | runtime + `mtgjson/AtomicCards.json` (fetched), `derived/cards.jsonl` (**built, never fetched**) | fetched: `setup-data --cards` or `fetch_data.fish`; derived: `setup-data --cards` builds it inline, repo checkouts run `scripts/build_derived.fish` | `card` (SQLite), `rulings`, `corpus`, `evals/coverage.fish` |
| rulings | `mtgjson/AllPrintings.sqlite` (shared with the cards tier) | fetched: `setup-data --rulings`, `setup-data --cards`, or `fetch_data.fish` | `rulings` |

**Who builds `derived/`:** consumers hosting their own shared data dir
(pointing `MTG_RULES_DATA` at it) must run the `cards.jsonl` build step
themselves after every `AtomicCards.json` refresh — either re-run
`setup-data --cards` (which rebuilds it) or run repo
`scripts/build_derived.fish`. A fetched-but-underived data dir makes `corpus`
fail with a pointer to this step; `card` queries `AllPrintings.sqlite` directly.
`skills/mtg-rules/scripts/health`
reports which tiers are present and warns per reference doc whose stated
synthesis date lags the live CR effective date.

## Maintenance (post-refresh checklist)

After WotC publishes updated rules or card data:

1. `scripts/fetch_data.fish` — re-fetch upstream sources
2. `scripts/build_derived.fish` — rebuild the derived card index (`data/derived/cards.jsonl`)
3. `cd skills/mtg-rules && scripts/cite check` — verify every in-skill citation still resolves and its rule text matches the lockfile
4. Review CHANGED diffs via `scripts/cite diff <rule>`; fix docs that drifted (or accept the rewording), then `scripts/cite bless` to re-pin the lockfile
5. Re-derive the validation probes in `skills/mtg-rules/references/rulings-check.md` against fresh `skills/mtg-rules/scripts/rulings` output; fix any doc that drifted
6. Re-test `skills/mtg-rules/references/underdetermined.md` entries — a new rule may settle one
7. Re-examine `skills/mtg-rules/references/generalizations.md` empty cells — a newly printed instance is a finding
8. Classify any new keywords — they land unclassified in `skills/mtg-rules/keywords-classified.json`

## Lookup Scripts

| Script | Example |
|--------|---------|
| `rule` | `skills/mtg-rules/scripts/rule 104.3a` |
| `define` | `skills/mtg-rules/scripts/define deathtouch` |
| `keyword` | `skills/mtg-rules/scripts/keyword flying` |
| `mtr` | `skills/mtg-rules/scripts/mtr 3.4` |
| `rule-search` | `skills/mtg-rules/scripts/rule-search 'last known information'` |
| `card` | `skills/mtg-rules/scripts/card "Lightning Bolt"` |
| `corpus` | `skills/mtg-rules/scripts/corpus --type Creature --match 'deals damage'` |
| `rulings` | `skills/mtg-rules/scripts/rulings Humility` |
| `lookup` | `skills/mtg-rules/scripts/lookup 'last known information'` |
| `classify` | `skills/mtg-rules/scripts/classify cascade` |
| `underdetermined` | `skills/mtg-rules/scripts/underdetermined UD-7` |
| `cite` | `cd skills/mtg-rules && scripts/cite check` |
| `health` | `skills/mtg-rules/scripts/health` |
| `version` | `skills/mtg-rules/scripts/version` (conformance manifest — consumers pin this) |

## Double-Bracketed Card Context Hook

Write an exact card name in double square brackets to inject its full card data
into the same turn's model context before the prompt is processed:

```text
How does [[Brazen Cannonade]] interact with [[Rest in Peace]]?
```

The `UserPromptSubmit` hook performs case-insensitive exact-name lookups with
the local `card` command. It ignores bracketed text that is not a card name,
deduplicates repeated names, and requires a multifaced card's canonical
combined name, including its ` // ` separator—for example,
`[[Start // Finish]]`. Combined names render every face. The SQLite card
database is part of the automatically installed hook runtime (see Automatic
First-Run Data above).

## Citation Context Hook (consumer repos)

A `PostToolUse` hook prints the official CR text for any citation a tool call
surfaces for the first time in a session, so a rule number written into code
is checked against the rule it names while the claim is still fresh.

It activates **only in repos that consume the skill** — that is, repos whose
VCS root holds a `cite-config.json` (deckmaste.rs does). This repo keeps its
config under `skills/mtg-rules/`, so the skill's own development tree is
excluded automatically and no path is hardcoded. Elsewhere the hook exits in
~11 ms without touching the CR.

`Write` and `Edit` are annotated by default: those are the moments a claim
enters the tree, and one edit cites a handful of rules. `Read` and `Bash` are
opt-in because they annotate per *file*, not per *delta* — a `Read` of a
127-citation engine module injects roughly 7k tokens.

| Variable | Effect |
|----------|--------|
| `CITE_ON_READ=1` | also annotate `Read` — every rule the file covers |
| `CITE_ON_BASH=1` | also annotate `Bash` stdout |
| `CITE_CONTEXT_FULL=1` | never clip rules already in the lockfile |
| `CITE_CONTEXT_MAX=N` | rules reported per call (default 40; `0` lifts the cap) |
| `CITE_CONTEXT_OFF=1` | disable the hook entirely |

Presence is what counts, not value — `CITE_ON_READ=0` still turns it *on*.
Unset the variable to turn it off.

**Bash calls into this skill are exempt.** `rule`, `cite show`, `cite audit`
and friends already print rule text, so annotating them would duplicate it —
and one uncapped `cite list` in a large consumer repo resolves to ~1,180
rules (~53k tokens). Both the path form (`skills/mtg-rules/scripts/cite …`)
and a bare command-position name (`cite list`) are recognized. Independent of
that, `CITE_CONTEXT_MAX` bounds every call, and a truncated report says how
many citations it held back rather than trailing off silently.

Rules absent from the consumer repo's lockfile are flagged `new to this
repo` and printed in full; already-locked rules are clipped to a preview.
Citations that resolve to nothing are flagged `NOT FOUND IN THE CR`, and
citations landing in a `coverage.out_of_scope` range are flagged as such.
The same machinery is available directly:

```sh
printf 'fn end_step() { /* [CR#514.1] */ }' \
  | skills/mtg-rules/scripts/cite --config /path/to/repo/cite-config.json context
```

## License & Fan Content Notice

Original content of this repository (scripts, tooling, document structure,
and synthesis) is licensed under the [MIT License](LICENSE).

**mtg-rules is unofficial Fan Content permitted under the
[Wizards of the Coast Fan Content Policy](https://company.wizards.com/en/legal/fancontentpolicy).
Not approved/endorsed by Wizards. Portions of the materials used are property
of Wizards of the Coast. ©Wizards of the Coast LLC.** Quoted excerpts from
the Magic: The Gathering Comprehensive Rules and official card rulings in
`skills/mtg-rules/references/` remain the property of Wizards of the Coast LLC and are
not covered by the MIT license. The repository ships no card data; users
fetch rules text and card data themselves from public sources (Wizards via
Academy Ruins, Scryfall, MTGJSON) using the bundled tooling.
