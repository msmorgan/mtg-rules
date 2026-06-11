# mtg-rules-skill

Marketplace and development repository for the **mtg-rules** Claude Code plugin — a judge-grade Magic: The Gathering rules skill grounded in the Comprehensive Rules, with verified citations and synthesized engine/grammar taxonomies.

## Install via Plugin Marketplace

```
/plugin marketplace add /path/to/mtg-rules-skill
# or a repo URL:
/plugin marketplace add https://github.com/msmorgan/mtg-rules-skill

/plugin install mtg-rules@mtg
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
git clone https://github.com/msmorgan/mtg-rules-skill
cd mtg-rules-skill
scripts/fetch_data.fish          # populate data/ in-repo

# Optional: symlink skill into your personal skills directory
ln -s "$PWD/skill" ~/.claude/skills/mtg-rules
```

Set `MTG_RULES_DATA` to override where scripts look for data:

```fish
set -x MTG_RULES_DATA /path/to/your/data
```

## Data Refresh Workflow

```bash
# 1. Re-fetch upstream sources
scripts/fetch_data.fish

# 2. Rebuild derived files (cards.jsonl, subtypes, etc.)
scripts/build_derived.fish

# 3. Verify all in-skill citations resolve
skill/scripts/check-citations skill/references/*.md skill/SKILL.md

# 4. Spot-check official rulings probes
skill/scripts/rulings-check
```

## Lookup Scripts

| Script | Example |
|--------|---------|
| `rule` | `skill/scripts/rule 104.3a` |
| `define` | `skill/scripts/define deathtouch` |
| `keyword` | `skill/scripts/keyword flying` |
| `mtr` | `skill/scripts/mtr 3.4` |
| `card` | `skill/scripts/card "Lightning Bolt"` |
| `corpus` | `skill/scripts/corpus "damage prevention"` |
| `rulings` | `skill/scripts/rulings "Lightning Bolt"` |
| `check-citations` | `skill/scripts/check-citations skill/references/effects.md` |
