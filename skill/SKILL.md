---
name: mtg-rules
description: Use for ANY Magic: The Gathering rules question, card interaction or ruling, judge call, tournament-policy (MTR) question, MTG engine design (game-state modeling, action/effect taxonomy), oracle-text grammar/parsing work, and mechanic design-space analysis (asymmetric rule families, generalization feasibility, keyword intrinsic/composite classification). Provides authoritative local lookups (Comprehensive Rules, glossaries, MTR, exact card oracle text) plus synthesized taxonomies of game state, actions, abilities, effects, and designations. Never answer MTG specifics from memory — verify with this skill's scripts.
---

# MTG Rules

Answers are grounded in local authoritative data. The Comprehensive Rules
(CR) text in this repo is the only authority; the reference docs orient you,
but the CR text is what you cite.

All paths below are relative to this skill's directory.

## Workflow (rigid)

1. Classify the question: rules mechanics | card-specific | tournament
   policy | engine taxonomy | grammar | mechanic design-space.
2. Orient with the matching reference doc (table below). Routing by
   question type:

   | question type | start here |
   |---|---|
   | engine taxonomy | `references/state.md` + `references/actions.md` |
   | mechanic design-space (generalizing/unifying, custom-mechanic feasibility) | `references/generalizations.md` + `references/engine.md` |
   | capability/restriction/permission ("can't", "only", "as though", "if able", ward-style tolls) | `references/deontics.md` |
   | keyword intrinsic/composite class, engine instruction-set | `references/keyword-classification.md`; per-keyword: `scripts/classify cascade` |
   | cost/payment | `references/costs.md` |
   | event/trigger schema | `references/events.md` |
   | decision/choice | `references/choices.md` |
   | visibility/hidden information | `references/information.md` |
   | game-ending | `references/outcomes.md` |
   | predicate/value language | `references/queries.md` |
   | mana | `references/mana.md` |
   | duration/lock | `references/temporal.md` |
   | "rules-defined or engine choice?" | `references/underdetermined.md`; per-entry: `scripts/underdetermined UD-7` |
   | variant/multiplayer | `references/variants.md` |
3. **Verify every load-bearing specific with the scripts before asserting
   it.** Start broad with `scripts/lookup` when unsure where an answer
   lives. Quote rule text with rule numbers. For card questions, fetch exact
   oracle text first (`scripts/card`) — never trust memory of a card's
   wording.
4. Answer: ruling first, then supporting citations (rule numbers + brief
   quotes).

## Scripts

| command | purpose |
|---|---|
| `scripts/lookup <query>` | unified meta-search: one regex fanned out over CR rules, glossaries, keywords, MTR, and reference-doc headings, hits labeled by source — recommended FIRST call for orientation |
| `scripts/rule 601.2` | rule + subrules + examples; `rule 601` = whole section |
| `scripts/rule-search <regex> [--max N]` | case-insensitive search over all CR rule text |
| `scripts/define <term>` | official + unofficial glossary |
| `scripts/keyword <name>` | keyword ability/action → its full CR section |
| `scripts/card <name>` | exact oracle text + characteristics (MTGJSON atomic) |
| `scripts/rulings <name>` | official per-card rulings (MTGJSON), date-stamped — re-resolve any CR numbers they cite |
| `scripts/mtr 1.7` / `--list` / `--search <re>` | Magic Tournament Rules sections |
| `scripts/corpus [--type T] [--keyword K] [--match RE] [--all]` | distinct oracle-text lines (grammar corpus) |
| `scripts/classify <keyword>` | a keyword's intrinsic/composite classification record (class, given, how, cites) from keywords-classified.json |
| `scripts/underdetermined [<id>]` | the CR-underdetermined registry by durable id (`UD-7`); no arg lists every entry |
| `scripts/cite check` / `bless` / `show <citation>` / `diff <rule>` | citation staleness guard with text-drift lockfile |
| `scripts/health` | self-diagnosis: data resolution, CR date, per-doc staleness, data tiers, citation check |
| `scripts/version` | machine-readable conformance manifest (plugin version, commit, CR date, keywords sha) |

## Reference docs

| doc | covers |
|---|---|
| `references/state.md` | component taxonomy of a game state: players, zones, objects, characteristics, per-object state, identity/LKI, game-level state |
| `references/engine.md` | pseudo-code game-state model + the damage pipeline (CR 120) |
| `references/generalizations.md` | asymmetric rule families, the generalized mechanic each implies, and 12 engine modeling directives |
| `references/keyword-classification.md` | every keyword classified intrinsic / composite / composite-given(P) / marker, + the 5-primitive engine basis (full data: skill/keywords-classified.json) |
| `references/deontics.md` | the deontic layer: May/Cant/Must/Gate/Toll algebra over action legality — "can't", "only", "as though", "if able" unified |
| `references/costs.md` | the cost algebra: positions, components, modification pipeline, payability |
| `references/events.md` | event ontology: types, cause triples, composition, trigger interface |
| `references/choices.md` | decision points: kinds, lock stages, deciders, visibility, randomness |
| `references/information.md` | visibility & hidden state: zones, face-down, reveals, per-player info sets |
| `references/outcomes.md` | game end: losses/wins/draws/restart/subgames + outcome modification |
| `references/queries.md` | the predicate & value language: selectors, bindings/anaphora, stored memory, undefined values — the grammar↔engine contract |
| `references/mana.md` | the mana subsystem: unit schema, production, payment predicates, pool policy |
| `references/temporal.md` | durations, windows, and the lock taxonomy |
| `references/underdetermined.md` | registry of CR-underdetermined semantics, durable `UD-NNN` ids — the engine's ADR seed list (assumed/open/representation-only/settled); consumers ADR-key choices by UD id |
| `references/variants.md` | which multiplayer/variant rules (CR 8xx–9xx) override base-game claims — lookup-first index |
| `references/actions.md` | everything the game can do: events; turn-based, state-based, special, and keyword actions; the priority→stack→resolve loop |
| `references/designations.md` | the scattered global flags, unified: monarch, initiative, day/night, city's blessing, ring-bearer, goaded, suspected, … |
| `references/abilities.md` | ability kinds + sub-kinds (mana, loyalty, linked, CDA, delayed/state/reflexive triggers), where abilities function |
| `references/effects.md` | one-shot vs continuous, layers + timestamps + dependency, replacement/prevention and ordering |
| `references/casting.md` | the 601.2 casting pipeline, costs, activation, resolution, spell copies |
| `references/turn.md` | turn structure, priority, combat step by step, cleanup |
| `references/grammar.md` | oracle-text grammar for parsing card text |
| `references/rulings-check.md` | the model validated against official card rulings — imitate its derivation patterns |

## Staleness

Reference docs state the CR effective date they were synthesized from; the
live data's date is in line 3 of `../data/rules/cr.txt`. If
`scripts/cite check` fails, or a cited rule reads differently than a
doc claims, trust the CR text, answer from it, and flag the doc for re-sync.
For a CHANGED citation: inspect the drift with `scripts/cite diff <rule>`,
fix the doc (or accept the rewording), then `scripts/cite bless` to re-pin
the lockfile.

## Data (repo `data/`, refreshed by repo-root `scripts/fetch_data.fish`)

- `rules/cr.{txt,json}` — Comprehensive Rules (json keyed by rule number)
- `rules/{glossary,unofficial-glossary,keywords}.json` — terms + keyword lists
- `rules/mtr.json` — Magic Tournament Rules
- `catalogs/*.json` — Scryfall closed vocabularies (types, keywords, word-bank)
- `mtgjson/` — card data; `derived/cards.jsonl` built by repo-root
  `scripts/build_derived.fish` (rebuild after refreshes)

Installed plugin copies resolve data via `$MTG_RULES_DATA` →
`~/.claude/plugins/data/mtg-rules/data` → repo layout; populate with
`scripts/setup-data [--cards] [--rulings]`.
