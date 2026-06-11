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
| Base rules + catalogs | *(default)* | ~4 MB | `rule`, `define`, `keyword`, `mtr`, `check-citations` |
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

## Maintenance (post-refresh checklist)

After WotC publishes updated rules or card data:

1. `scripts/fetch_data.fish` — re-fetch upstream sources
2. `scripts/build_derived.fish` — rebuild the derived card index (`data/derived/cards.jsonl`)
3. `skill/scripts/check-citations` — verify every in-skill citation resolves; fix flagged docs
4. Re-derive the validation probes in `skill/references/rulings-check.md` against fresh `skill/scripts/rulings` output; fix any doc that drifted
5. Re-test `skill/references/underdetermined.md` entries — a new rule may settle one
6. Re-examine `skill/references/generalizations.md` empty cells — a newly printed instance is a finding
7. Classify any new keywords — they land unclassified in `skill/keywords-classified.json`

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
| `check-citations` | `skill/scripts/check-citations` |

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
