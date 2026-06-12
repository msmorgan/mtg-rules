# mtg-rules

Marketplace and development repository for the **mtg-rules** Claude Code plugin — a judge-grade Magic: The Gathering rules skill grounded in the Comprehensive Rules, with verified citations and synthesized engine/grammar taxonomies.

## Install via Plugin Marketplace

```
/plugin marketplace add /path/to/mtg-rules
# or a repo URL:
/plugin marketplace add https://github.com/msmorgan/mtg-rules

/plugin install mtg-rules@mtg-rules
```

### First-Run Data Setup

After installing, populate the data directory with the bundled fetcher:

```
scripts/setup-data
```

**Data tiers** (all are idempotent — re-run to refresh):

| Tier | Flag | Size | Enables |
|------|------|------|---------|
| Base rules + catalogs | *(default)* | ~4 MB | `rule`, `define`, `keyword`, `mtr`, `cite` |
| Card lookups + corpus | `--cards` | ~155 MB | `card`, `corpus` |
| Official rulings DB | `--rulings` | large | `rulings` |

Example — base tier only:

```
scripts/setup-data
```

Example — full install:

```
scripts/setup-data --cards --rulings
```

Data lands in `~/.claude/plugins/data/mtg-rules/data/` by default, or in `$MTG_RULES_DATA` if that variable is set.

## Development Setup (Repo Checkout)

```bash
git clone https://github.com/msmorgan/mtg-rules
cd mtg-rules
scripts/fetch_data.fish          # populate data/ in-repo

# Optional: symlink skill into your personal skills directory
ln -s "$PWD/skill" ~/.claude/skills/mtg-rules
```

Set `MTG_RULES_DATA` to override where scripts look for data:

```fish
set -x MTG_RULES_DATA /path/to/your/data
```

## Data Directory Contract (versioned)

The on-disk layout under the resolved data dir (`$MTG_RULES_DATA` →
`~/.claude/plugins/data/mtg-rules/data` → repo `data/`) is a compatibility
contract, versioned with the plugin (current: 1.7.0; layout changes are
called out in [CHANGELOG.md](CHANGELOG.md)). Consumers pin the manifest from
`skill/scripts/version` and re-sync on any bump.

| Tier | Files | Built by | Enabling scripts |
|------|-------|----------|------------------|
| base | `rules/cr.txt`, `rules/cr.json`, `rules/glossary.json`, `rules/unofficial-glossary.json`, `rules/keywords.json`, `rules/mtr.json`, `catalogs/*.json` | fetched: `skill/scripts/setup-data` or repo `scripts/fetch_data.fish` | `rule`, `rule-search`, `define`, `keyword`, `mtr`, `lookup`, `classify`, `underdetermined`, `cite`, `health`, `version` |
| cards | `mtgjson/AtomicCards.json` (fetched), `derived/cards.jsonl` (**built, never fetched**) | fetched: `setup-data --cards` or `fetch_data.fish`; derived: `setup-data --cards` builds it inline, repo checkouts run `scripts/build_derived.fish` | `card`, `corpus`, `evals/coverage.fish` |
| rulings | `mtgjson/AllPrintings.sqlite` | fetched: `setup-data --rulings` or `fetch_data.fish` | `rulings` |

**Who builds `derived/`:** consumers hosting their own shared data dir
(pointing `MTG_RULES_DATA` at it) must run the `cards.jsonl` build step
themselves after every `AtomicCards.json` refresh — either re-run
`setup-data --cards` (which rebuilds it) or run repo
`scripts/build_derived.fish`. A fetched-but-underived data dir makes `card`
and `corpus` fail with a pointer to this step. `skill/scripts/health`
reports which tiers are present and warns per reference doc whose stated
synthesis date lags the live CR effective date.

## Maintenance (post-refresh checklist)

After WotC publishes updated rules or card data:

1. `scripts/fetch_data.fish` — re-fetch upstream sources
2. `scripts/build_derived.fish` — rebuild the derived card index (`data/derived/cards.jsonl`)
3. `cd skill && scripts/cite check` — verify every in-skill citation still resolves and its rule text matches the lockfile
4. Review CHANGED diffs via `scripts/cite diff <rule>`; fix docs that drifted (or accept the rewording), then `scripts/cite bless` to re-pin the lockfile
5. Re-derive the validation probes in `skill/references/rulings-check.md` against fresh `skill/scripts/rulings` output; fix any doc that drifted
6. Re-test `skill/references/underdetermined.md` entries — a new rule may settle one
7. Re-examine `skill/references/generalizations.md` empty cells — a newly printed instance is a finding
8. Classify any new keywords — they land unclassified in `skill/keywords-classified.json`

## Lookup Scripts

| Script | Example |
|--------|---------|
| `rule` | `skill/scripts/rule 104.3a` |
| `define` | `skill/scripts/define deathtouch` |
| `keyword` | `skill/scripts/keyword flying` |
| `mtr` | `skill/scripts/mtr 3.4` |
| `rule-search` | `skill/scripts/rule-search 'last known information'` |
| `card` | `skill/scripts/card "Lightning Bolt"` |
| `corpus` | `skill/scripts/corpus --type Creature --match 'deals damage'` |
| `rulings` | `skill/scripts/rulings Humility` |
| `lookup` | `skill/scripts/lookup 'last known information'` |
| `classify` | `skill/scripts/classify cascade` |
| `underdetermined` | `skill/scripts/underdetermined UD-7` |
| `cite` | `cd skill && scripts/cite check` |
| `health` | `skill/scripts/health` |
| `version` | `skill/scripts/version` (conformance manifest — consumers pin this) |

## License & Fan Content Notice

Original content of this repository (scripts, tooling, document structure,
and synthesis) is licensed under the [MIT License](LICENSE).

**mtg-rules is unofficial Fan Content permitted under the
[Wizards of the Coast Fan Content Policy](https://company.wizards.com/en/legal/fancontentpolicy).
Not approved/endorsed by Wizards. Portions of the materials used are property
of Wizards of the Coast. ©Wizards of the Coast LLC.** Quoted excerpts from
the Magic: The Gathering Comprehensive Rules and official card rulings in
`skill/references/` remain the property of Wizards of the Coast LLC and are
not covered by the MIT license. The repository ships no card data; users
fetch rules text and card data themselves from public sources (Wizards via
Academy Ruins, Scryfall, MTGJSON) using the bundled tooling.
