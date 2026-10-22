---
name: mtg-rules
description: "Magic: The Gathering rules and card interactions, judge calls and tournament policy, rules-engine and game-model design, Oracle-text parsing, and mechanic design-space analysis including keyword classification."
---

# MTG Rules

All paths below are relative to this skill's directory.

## Authority

Sources decide. Use the local Comprehensive Rules (CR) for game mechanics, the
Magic Tournament Rules (MTR) for tournament policy, and exact Oracle card data
for card wording and characteristics. Official card rulings provide
interpretive checks; their embedded CR numbers must be re-resolved against the
current rules. If a ruling predates a rule change, cite the current rule and
explain the discrepancy. If a judge call requires a policy document outside the
bundled MTR, identify the missing source and limit the answer to what the
available sources establish.

- Numbered rules prevail over glossary entries, official or not. `define`
  prints only the glossary; resolve the rule it points to.
- A cited rule must support the claim in the direction stated. Read the rule's
  text; a rule that merely mentions the topic is not support.
- A claim about where a keyword or wording applies needs a typed corpus probe
  (`scripts/corpus --type T --match <regex>`), not a recalled example.

The reference docs are **maps** of those sources. Each gathers the rules one
subsystem spans, shows how they connect, enumerates the closed lists the CR
scatters, and marks where the CR leaves a choice to the engine. Read a map to
learn which rules to check, then check them. A map claim without a dotted
citation is an engine inference: test it against card text, rulings, or the
corpus before adopting it. When a citation check fails or a map disagrees with
a source, answer from the source and report the drift. Keyword classifications
and the unofficial glossary are maps too.

## Workflow

1. Classify the task.
   - **Verdict**: what happens in a given game situation, what a card or rule
     says, or what tournament policy requires. Go to step 3. For verdicts that
     run through layers, replacement ordering or the damage pipeline, a map
     read (step 2) is optional and often pays.
   - **Model**: design, review, or audit something that encodes the rules (an
     engine, game model, semantics checker, parser, grammar, or catalog);
     enumerate every case of something; generalize a mechanic; write or
     copy-edit card text; or decide whether the CR forces a behavior or leaves
     it to the engine. Model work usually also tests verdicts on specific cards.
2. For model work, read the matching section of each map whose row in the Maps
   table matches the task (usually one or two): `scripts/ref <map>` lists a
   map's sections; `scripts/ref <map> <n|heading>` prints one. This step is
   complete when you have listed the cited rules that bear on the task and the
   uncited claims you will test.
3. **Verify every load-bearing specific with the scripts before asserting it.**
   For a card question, obtain exact text with `scripts/card` first; card data
   injected by this plugin's hook satisfies that lookup. Follow search hits and
   map citations to full source text. For card interactions, derive the result
   from card text and applicable rules, then check `scripts/rulings` for
   relevant official guidance. Absence of a ruling is not confirmation. This
   step is complete when each conclusion has source support or is explicitly
   identified as an inference or unresolved point.
4. Give the ruling or conclusion first, then supporting rule numbers, MTR
   sections, or card/ruling attribution with brief quotes as appropriate.
   Cite rules, not maps.

## Maps

| Task touches | Map |
|---|---|
| Engine state inventory: players, objects, zones, characteristics vs status, identity/LKI, turn history | [state](references/state.md) |
| Engine pseudocode; the damage pipeline (CR 120: results by recipient, prevention order, SBA handoff) | [engine](references/engine.md) |
| Actions: events vs actions vs effects (700.1); turn-based, state-based (704.5-6), special, keyword actions; main loop and SBA/trigger fixpoint; illegal-action rewind (733) | [actions](references/actions.md); per-step priority in [turn](references/turn.md) |
| Turn/step sequence, priority, combat declaration and damage, cleanup, extra turns/phases | [turn](references/turn.md); attack/block triggers in [events](references/events.md), requirements in [deontics](references/deontics.md), multiplayer combat in [variants](references/variants.md) |
| Casting, activating, resolving; spell copies | [casting](references/casting.md) |
| Ability kinds and sub-kinds (mana, loyalty, CDA, linked, delayed/reflexive/state/intervening-if triggers); where abilities function (113.6); granting/removing; abilities on the stack | [abilities](references/abilities.md); look-back and zone-change triggers in [events](references/events.md) |
| Effects: one-shot vs continuous, locked affected sets, layers, timestamps, dependency, text-changing, replacement/prevention and their 616 ordering | [effects](references/effects.md) |
| Event schema; cause/agent ("destroyed", "caused you to discard", "this way"); dies/discard/mill/draw views; composition; trigger matching, look-back | [events](references/events.md) |
| Legality: can't vs may (101.2), attack/block requirement solver, "unless pays" gates, "if able", "as though" (609.4), cast/activate legality, toll vs gate (ward), can't vs replacement | [deontics](references/deontics.md) |
| Costs: cost vs effect, cost positions (additional, alternative, attack/block, resolution "unless pays", special-action), payability, payment substitution (convoke, delve, waterbend) | [costs](references/costs.md) |
| Choice, decider, delegation, APNAP, lock stage, secret choice, randomness (cost classification: costs) | [choices](references/choices.md) |
| Visibility and hidden information: reveal/look/search, look grants, face-down objects, secret choices | [information](references/information.md) |
| Win, loss, draw, concession, can't-lose/win, loss replacement, leaving the game, restart, subgame | [outcomes](references/outcomes.md); team/Emperor outcomes in [variants](references/variants.md) |
| Object/player tests and selectors ("another", "each", "up to N target"); "you"/"it"/"this way"/"exiled with"/"the chosen" references; X, count, mana value, rounding, undefined values; LKI | [queries](references/queries.md) |
| Mana: types, production, pool units and riders, spend restrictions, retention/emptying, payment coercions | [mana](references/mana.md) |
| Durations and expiry; windows; when a value, target, X, cost or object set is fixed vs re-evaluated; once-per-turn limits; skipped or "next" occurrences | [temporal](references/temporal.md) |
| Designations (player/permanent/game/card flags and lifetimes): monarch, initiative, day/night, city's blessing, Ring-bearer, goaded, suspected, Room doors, Class level, protector, commander; exile states plotted/foretold | [designations](references/designations.md) |
| Multiplayer, team, or casual-variant game (2HG, Commander/Brawl, range of influence, Grand Melee, Emperor, Planechase, Archenemy, Vanguard, Conspiracy): which base-map claims change | [variants](references/variants.md), then `scripts/rule 8xx/9xx` |
| Parsing Oracle text: segmentation, ability-kind markers, keyword lines and em-dash forms, frames (Saga/Class/leveler/station), modal headers | [grammar](references/grammar.md); noun-phrase writing in [oracle-style](references/oracle-style.md); `scripts/corpus` for attested text; CR lists (`data/rules/keywords.json`) outrank Scryfall catalogs |
| Writing, templating, or copy-editing card text; how Oracle conventionally phrases something (names, pronouns, `this`/`that`, types, numbers, punctuation, standard effect templates) | [oracle-style](references/oracle-style.md) |
| Keyword engine class (intrinsic/composite/composite-given(P)/marker), `given` primitive basis, classifying a new keyword | [classification](references/keyword-classification.md); `scripts/classify <keyword>` (variants such as megamorph: classify the parent keyword) |
| Generalizing a mechanic; asymmetries; custom-mechanic feasibility (confirm any "no rule/card does X" claim with `scripts/corpus` and `scripts/rule-search`) | [generalizations](references/generalizations.md) |
| CR gap or engine choice: does the CR settle X? (snow timing, undefined values, concession timing, randomness, LKI extent, loop equality, batch order, knowledge after rewind) | [underdetermined](references/underdetermined.md); `scripts/underdetermined <id>` |

## Lookups

| Need | Script |
|---|---|
| Where a topic lives | `scripts/lookup <regex>`: rules, glossary, keywords, MTR, map sections |
| A rule, term, or keyword | `scripts/rule <number>`, `scripts/define <term>`, `scripts/keyword <name>` |
| Card text and official rulings | `scripts/card <name>`, `scripts/rulings <name>` |
| Attested Oracle wording | `scripts/corpus` |
| Tournament policy or judge procedure | `scripts/mtr --search <regex>`, then `scripts/mtr <section>` |
| A keyword's engine class | `scripts/classify <keyword>` |
| An engine-choice registry entry | `scripts/underdetermined <id>` |
| A map section | `scripts/ref <map> <n\|heading>`; `ref --cites <rule>` lists sections citing a rule; `ref --grep <regex>` searches map text |

`lookup` prints `[map]` lines and `rule` prints a footer when map sections bear
on the hit. For model work, follow those pointers with `scripts/ref`; for a
plain verdict they are optional.

## Lookup details

`lookup` and `rule-search` accept case-insensitive regexes. Search previews
locate evidence; `rule <number>` prints the full rule and its descendants,
and `rule <section>` prints a whole section. `define` labels unofficial entries.
`mtr --list` lists policy sections. `card` accepts an exact card or face name;
`card --full-name` requires the canonical combined name for multifaced cards.
`corpus` returns distinct Oracle lines, with `--type`, `--keyword`, and `--match`
filters. `underdetermined` without an id lists the engine-choice registry.
`ref` without arguments lists the maps; its output is banner-marked as a map,
not a source.

## Data and staleness

Hooks provision the lookup runtime before the first model turn. If setup warns
or a lookup reports missing data, run `scripts/setup-data --runtime` and retry;
use `--cards` for the corpus tier. If the retry fails, report which evidence
is unavailable and leave dependent conclusions unresolved.

`scripts/health` reports the resolved data path, live CR date, data tiers, map
synthesis dates, and citation health. `scripts/version` provides the
conformance manifest. In maps, `data/...` paths are relative to the data
directory that `scripts/health` reports, not to this skill's directory.
Repairing maps and repinning citations belong to an explicitly requested
maintenance task.
