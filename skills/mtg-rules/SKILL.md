---
name: mtg-rules
description: "Magic: The Gathering rules and card interactions, judge calls and tournament policy, engine modeling, Oracle-text parsing, and mechanic design-space analysis including keyword classification."
---

# MTG Rules

All paths below are relative to this skill's directory.

## Authority

Use the local Comprehensive Rules (CR) for game mechanics, the Magic Tournament
Rules (MTR) for tournament policy, and exact Oracle card data for card wording
and characteristics. Official card rulings provide interpretive checks; their
embedded CR numbers must be re-resolved against the current rules. If a ruling
predates a rule change, cite the current rule and explain the discrepancy.
Synthesized references, keyword classifications, and the unofficial glossary
orient the search; distinguish engine inferences from rules requirements.
If a judge call requires a policy document outside the bundled MTR, identify
the missing source and limit the answer to what the available sources establish.

## Workflow

1. Select the applicable routes below. For a card question, obtain exact text
   with `scripts/card` first; card data injected by this plugin's hook satisfies
   that lookup. Use reference docs when the question needs their synthesis;
   direct lookups suffice for straightforward questions.
2. **Verify every load-bearing specific with the scripts before asserting it.**
   Follow search hits to full source text. For card interactions, derive the
   result from card text and applicable rules, then check `scripts/rulings`
   for relevant official guidance. Absence of a ruling is not confirmation.
   This step is complete when each conclusion has source support or is explicitly
   identified as an inference or unresolved point.
3. Give the ruling or conclusion first, then supporting rule numbers, MTR
   sections, or card/ruling attribution with brief quotes as appropriate.

## Routes

| Question | Start here |
|---|---|
| Rules question with no known section | `scripts/lookup <regex>`, then the indicated source or doc |
| Named rule, term, or keyword | `scripts/rule <number>`, `scripts/define <term>`, or `scripts/keyword <name>` |
| Card text or interaction | `scripts/card <name>`; for interactions, the relevant rules route and `scripts/rulings <name>` |
| Tournament policy or judge procedure | `scripts/mtr --search <regex>` then `scripts/mtr <section>` |
| Oracle grammar or parsing | [grammar](references/grammar.md); `scripts/corpus` for attested text |
| Engine state: players, zones, objects, identity/LKI | [state](references/state.md) |
| Engine actions: turn-based, state-based, special, keyword; main loop | [actions](references/actions.md) |
| Engine pseudocode or damage pipeline | [engine](references/engine.md) |
| Mechanic generalization, asymmetry, custom-mechanic feasibility | [generalizations](references/generalizations.md) |
| Keyword intrinsic/composite/marker class or primitive basis | [classification](references/keyword-classification.md); `scripts/classify <keyword>` |
| Permission, restriction, requirement, "as though", "if able", toll | [deontics](references/deontics.md) |
| Costs, modification, payability | [costs](references/costs.md) |
| Event schema, cause, composition, trigger matching | [events](references/events.md) |
| Choice, decider, lock stage, randomness | [choices](references/choices.md) |
| Visibility, hidden information, face-down objects | [information](references/information.md) |
| Win, loss, draw, restart, subgame | [outcomes](references/outcomes.md) |
| Predicate, selector, binding/anaphora, value | [queries](references/queries.md) |
| Mana production, units, payment, pool policy | [mana](references/mana.md) |
| Duration, window, lock, reevaluation | [temporal](references/temporal.md) |
| Rules requirement versus engine choice | [underdetermined](references/underdetermined.md); `scripts/underdetermined <id>` |
| Multiplayer or variant overrides | [variants](references/variants.md) |
| Designations: monarch, initiative, day/night, flags | [designations](references/designations.md) |
| Ability kinds, sub-kinds, where abilities function | [abilities](references/abilities.md) |
| Effects, layers, timestamps, dependency, replacement/prevention | [effects](references/effects.md) |
| Casting, activation, resolution, spell copies | [casting](references/casting.md) |
| Turn structure, priority, combat, cleanup | [turn](references/turn.md) |

## Lookup details

`lookup` and `rule-search` accept case-insensitive regexes. Search previews
locate evidence; `rule <number>` prints the full rule and its descendants,
and `rule <section>` prints a whole section. `define` labels unofficial entries.
`mtr --list` lists policy sections. `card` accepts an exact card or face name;
`card --full-name` requires the canonical combined name for multifaced cards.
`corpus` returns distinct Oracle lines, with `--type`, `--keyword`, and `--match`
filters. `underdetermined` without an id lists the engine-choice registry.

## Data and staleness

Hooks provision the lookup runtime before the first model turn. If setup warns
or a lookup reports missing data, run `scripts/setup-data --runtime` and retry;
use `--cards` for the corpus tier. If the retry fails, report which evidence
is unavailable and leave dependent conclusions unresolved.

`scripts/health` reports the resolved data path, live CR date, data tiers, and
citation health. `scripts/version` provides the conformance manifest.
Reference headers record their synthesis date. When a citation check fails or
a reference disagrees with current source text, answer from the source and
report the reference drift. Repairing reference docs and repinning citations
belong to an explicitly requested maintenance task.
