# Mana — The Mana Subsystem

*Synthesized from the Comprehensive Rules effective 2026-04-17
(`data/rules/cr.json`). Orientation only — verify load-bearing specifics
with `scripts/rule` before citing. Run `scripts/cite check` after CR
refreshes.*

The game's primary resource, modeled as a pool of *units* that carry more
than a type. This doc is the **promotion of `generalizations.md` Family 13**
("Mana attributes: color is a type, everything else is a rider") to a full
reference — its unit schema, danger notes, and directive 10 are the seed.
Division of labor: symbol-by-symbol *cost-side* semantics live in
`costs.md` §3 (don't re-derive); mana abilities are classified in CR 605
(pointers only); the tapped-for-mana event row is `events.md` §2; payment
mechanics are `casting.md` §2–3.

## 1. Types — and the colorless/generic distinction

Mana is the primary resource; players spend it to pay costs, usually when
casting spells and activating abilities (106.1). There are **five colors**
of mana (106.1a) but **six types**: white, blue, black, red, green, and
colorless (106.1b). Mana is represented by mana symbols (106.2, 107.4),
which also represent mana costs (202.1a).

**Colorless is a TYPE; generic is a COST category.** The two never collapse:

- **{C}** represents one colorless mana, and as a cost it can be paid
  *only* with one colorless mana (107.4c) — a type test.
- **{1}, {2}, … {X}** represent generic mana in costs, payable with *any
  type* of mana (107.4b) — the absence of a type test.
- On the production side a generic symbol adds that much *colorless* mana
  (106.10) — so "{C} vs {1}" is purely a cost-side distinction; there is
  no "generic mana" in any pool, only colorless.

Snow is **neither a color nor a type** (107.4h) — it's a property of the
producing *source*, carried on the unit (§2).

## 2. The unit schema

Each unit of mana in a pool carries: **type + source snapshot + riders +
persistence**. The CR attests every field (one evaluation-timing detail is
engine inference, flagged below):

- **Type** — exactly one of the six (106.1b). Nothing below changes it
  (106.6 is explicit).
- **Source snapshot** — if mana is produced by a spell, its source is that
  spell; if by an ability, the source of that ability (106.3, 113.7).
  Snow-ness is checked *through the source*: {S} in a cost is payable with
  one mana of any type produced by a snow source (107.4h). The CR never
  states *when* snow-ness is evaluated; snapshotting it at add-time is an
  **engine inference** from 107.4h's past-tense "produced by a snow
  source" wording — it keeps a later supertype-changing effect from
  corrupting payments already banked.
- **Riders** — producing effects may restrict how the mana can be spent,
  attach an additional effect to the spell or ability it's spent on, or
  create a delayed triggered ability (603.7a) that triggers when the mana
  is spent; none of this affects the mana's type (106.6). Under
  production-doubling replacement effects, restrictions and additional
  effects apply to *all* mana produced, and a **separate** delayed trigger
  (or continuous/replacement effect) is created **per mana** (106.6a) —
  the rule that proves riders live on the unit, not on the producing
  effect.
- **Persistence** — the pool empties at the end of each step and phase,
  and the player is said to *lose* this mana (106.4); mechanically a
  turn-based action (703.4q) sequenced after until-end-of-step/phase
  effects expire (500.5). Persistence is a per-unit override point:
  firebending's trigger adds {R} with "Until end of combat, you don't
  lose this mana as steps and phases end" (702.189a), and the corpus has
  21 distinct "don't lose this mana as steps and phases end" lines plus
  the static form "Players don't lose unspent mana as steps and phases
  end."

Pool contents are public on demand: a player announces what mana remains
after spending from the pool (106.4a) and whenever they pass priority with
mana in it (106.4b).

## 3. Production

**Mana abilities** are CR 605's classification, not this doc's: an
activated ability is a mana ability if it requires no target, could add
mana on resolution, and isn't a loyalty ability (605.1a); a triggered mana
ability must additionally trigger off a mana ability or off mana being
added (605.1b). They can be activated whenever a rule or effect asks for a
mana payment, even mid-cast or mid-resolution (605.3a), don't use the
stack (605.3b), and are never mandatory, even if paying a cost is
(118.3c). Mana may *also* be produced by spells and by non-mana abilities
(106.3).

**"Add" semantics**: a producing effect instructs a player to add mana
(106.3); added mana goes to that player's pool, where it pays costs
immediately or sits as *unspent mana* (106.4).

**Production-side symbol readings differ from cost-side readings** — same
symbols, two interpreters:

| Symbol added by an effect | What enters the pool | Rule |
|---|---|---|
| hybrid | the player chooses one half; colored half → that color, generic half → that much colorless | 106.8 |
| Phyrexian | one mana of the symbol's color — never a life option | 106.9 |
| generic ({1}, {X}…) | that much colorless | 106.10 |
| snow {S} | that much colorless | 106.11 |

The cost-side readings (pay-with predicates, the 2-life option, the
snow-source test) are 107.4e/f/h and live in `costs.md` §3.

**Producing the undefined and the hypothetical**:

- An ability that would produce mana of an **undefined type** produces no
  mana instead (106.5 — Meteor Crater with no colored permanents).
- **"Could produce"** (106.7): the types a permanent could produce are
  whatever its abilities would produce if they resolved now, taking
  applicable replacement effects into account *in any possible order* and
  ignoring whether costs could be paid; if nothing would be produced or no
  type is definable, there's no type it could produce (Exotic Orchard
  chains resolve through this rule). Note: rule 106 ends at 106.13 —
  no higher-numbered subrules exist.

**Tapped-for-mana** is a defined production event: "tap [a permanent] for
mana" = activate one of its mana abilities that includes {T} in the cost
(106.12). Triggers on "is tapped for mana [of a type]" fire when such an
ability *resolves and produces* the mana (106.12a); replacements modify
the production event during that resolution (106.12b) — corpus: "If a land
is tapped for mana, it produces {B} instead of any other type." Event
fields and cause tags are `events.md` §2.

**Conditional rider patterns** (corpus-attested 106.6 shapes): spend
restriction — "Spend this mana only to cast creature spells" (143 distinct
"Spend this mana only" lines) and "This mana can't be spent to cast
nonartifact spells" (3 lines; the broader "mana can't be spent" family
has 28); additional effect — "If that mana is spent on a creature spell,
it gains riot" (7 "If that mana is spent on" lines); delayed trigger —
"When that mana is spent to cast an instant or sorcery spell, copy that
spell" (1 line; the "When that mana is spent" family has 3; one 603.7a
trigger per unit under doublers per 106.6a).

## 4. Payment

Cost symbols are **payment predicates over units** — the symbol-by-symbol
algebra is `costs.md` §3; the one-line summary is 202.1a: paying a mana
cost requires matching the type of any colored or colorless symbols and
paying the generic component with anything. Paying mana removes the
indicated mana from the pool (118.3a).

**Coercions are payment-side only** (609.4b): an effect letting a player
spend mana "as though it were mana of any type" — or saying "mana of any
type can be spent" (31 corpus lines) — affects only *how a cost may be
paid*. It doesn't change the cost, and it doesn't change what mana was
actually spent. The unit in the pool keeps its real type, source, and
riders; the coercion lives in the payment solver.

**Spend-restrictions are enforced at payment time**: the total cost is
locked at 601.2f, then the payment window opens — mana abilities first
(601.2g), then payment of the total, partial payments disallowed (601.2h).
A unit's "spend only on X" predicate (106.6) is consulted as units are
assigned to symbols inside that window — after the lock, which matters for
predicates over mutable state ("spend only to cast Dragon spells" checks
the spell being paid for, not the world at add-time).

## 5. Edges

- **Emptying ≠ damage**: when the pool empties, the player "is said to
  lose this mana" (106.4) — a resource lapse with no life consequence.
  The glossary entry "Mana Burn (Obsolete)" confirms the old
  unspent-mana-causes-life-loss rule **no longer exists** (run
  `scripts/define 'mana burn (obsolete)'`); don't cite a rule number for
  mana burn, there isn't one.
- **Mana can change pools intact** (106.13, the Drain Power rule): mana
  lost by one player and re-added to another keeps its producing
  source and any restrictions or additional effects unchanged — transfer
  moves whole units.
- **"Can't add mana" doesn't exist**: no CR rule and no oracle line says a
  player can't add mana. The real levers are upstream: undefined-type
  production yields nothing (106.5), tapped-for-mana replacements rewrite
  the production event (106.12b, 13 corpus "produces … instead" lines),
  and activation bans ("activated abilities can't be activated") are
  `deontics.md` can't-effects that happen to catch mana abilities.
- **Symbol pointers**: {C} 107.4c, hybrid 107.4e, Phyrexian 107.4f (and
  the {H} umbrella, 107.4g), snow 107.4h — cost-side detail in
  `costs.md` §3; production-side readings in §3's table above.

## 6. Engine note

```
ManaUnit {
  type:            W | U | B | R | G | C,          # closed, 106.1b
  source_snapshot: {object, characteristics-at-add}, # 106.3/113.7; add-time
                                                     #   snow-ness freeze is
                                                     #   inference, 107.4h (§2)
  spend_predicate: Predicate | None,    # "Spend this mana only…" (106.6)
  riders:          [OnSpendEffect | DelayedTrigger], # 106.6; replicated
                                                     #   per unit (106.6a)
  persistence:     STEP_PHASE_END | UNTIL(event) | GAME,  # 106.4/703.4q
                                                     #   vs 702.189a-style
}
Pool = per-player Multiset[ManaUnit]    # announced per 106.4a-b
```

This is `generalizations.md` directive 10 verbatim: units carry (type,
source-snapshot, spend-predicate, riders, persistence); cost symbols
compile to payment predicates over units ({R} = type-is-red, {S} =
snow(source_snapshot), {C} = type-is-colorless, generic = always-true);
a future quality-tested symbol is the same compile target. Keep 609.4b
coercions in the payment solver — they never mutate units. Evaluate
spend-predicates inside the 601.2g–h window, after the 601.2f lock.
Emptying is the 703.4q turn-based action filtered by per-unit
persistence; transfer (106.13) moves units whole. The production event
(what 106.12a triggers and 106.12b replacements see) must be first-class
and carry the producing ability's identity, since "tapped for mana of a
specified type" filters on its output.
