# Queries — The Predicate & Value Language

*Synthesized from the Comprehensive Rules effective 2026-08-07
(`data/rules/cr.json`). Orientation only — verify load-bearing specifics
with `scripts/rule` before citing. Run `scripts/cite check` after CR
refreshes.*

The emergent shared layer. Every taxonomy doc parameterizes over an
informal predicate-and-value language: `deontics.md`'s guards,
`events.md`'s trigger patterns, `costs.md`'s scaling riders,
`choices.md`'s option constraints, `keyword-classification.md`'s `how`
decompositions. This doc is that language's semantics. The parser
compiles `grammar.md` §5–6's surface forms *into* it; the engine
evaluates it; §7 is the contract between the two.

## 1. Object and player predicates

**Characteristic tests.** The testable fields are the closed 109.3 list
(name, mana cost, color, …, power, toughness — `state.md` §5). The values
compared are *layer-system outputs* read at query time (`effects.md`); P/T
in particular is the result of the 613.4 sublayers (CDAs first, 613.4a),
so "power 2 or less" sees the post-layers number, and comparisons may use
negative values directly (107.1b). Field specifics:

- **Color** — an object's colors come from mana symbols, color indicator,
  or a CDA (105.2); monocolored = exactly one, multicolored = two or more,
  colorless = none (105.2a, 105.2b, 105.2c).
- **Name** — self-names are identity, not string-match (§3; 201.5);
  interchangeable names are the same name for all game purposes (201.3a);
  "choose a card name" ranges over the Oracle reference (201.4).
- **Mana value** — total of the mana cost (202.3); no mana cost = 0
  (202.3a); {X} counts as the announced value on the stack, 0 elsewhere
  (202.3e); hybrid uses the largest half (202.3f), Phyrexian counts 1
  (202.3g).
- Type/subtype/supertype and P/T are open vocabularies →
  `data/catalogs/*.json` (card-types, creature-types, supertypes, powers…).

**Description defaults — the implicit zone quantifier.** A bare description
with a card type or subtype but no zone and no "card," "spell," "source,"
or "scheme" means a *permanent on the battlefield* (109.2). "Card" + zone
means a card there (109.2a); "spell" means on the stack (109.2b); "source"
means a source of ability/damage/mana in any zone (109.2c). Every parsed
noun phrase gets its domain from this rule before any predicate applies.

**State tests** — explicitly *not* characteristics (109.3): **status**, the
four binary categories tapped/flipped/face-down/phased (110.5; permanents
only, 110.5d); **attacking/blocking**, which hold from legal declaration
(508.1a, 509.1a) until removal from combat or end of combat (glossary via
`scripts/define`); **face-down** objects expose only the characteristics
their enabler lists — default a 2/2 with no name (708.2, 708.2a;
`information.md` §2).

**Relational tests**: controller (only stack/battlefield objects have one,
109.4); owner (108.3); attached-to (not a characteristic, 109.3 — per-object
state, `state.md` §6); the AGENT coordinate of an event's cause — "a spell
or ability an opponent controls" as destroyer/causer is a predicate over
the cause triple (`events.md` §3); and **targeting tests** (115.9): "with
[N] targets" counts instances chosen at stack-put (115.9a), "that targets
[something]" checks the targets' *current* state, ignoring departed ones
without LKI (115.9b), "targets only" counts distinct chosen targets, then
checks current state (115.9c).

**Zone tests**: the closed 400.1 list (library, hand, battlefield,
graveyard, stack, exile, command, ante); per-player vs shared in
`state.md` §3.

## 2. Quantifiers and selectors

| Selector | Semantics | Rules |
|---|---|---|
| `target [desc]` | chosen at stack-put; only the word "target" targets (115.10a; "you" never does, 115.10b); declared per 115.1; default domain: permanents (115.2) | 115.1, 601.2c |
| `N target` | exactly N distinct picks per instance of "target" (115.3); the same object may be re-picked across *different* instances | 115.3 |
| variable-count targets | count announced before the targets, then locked even if the defining information changes | 601.2c |
| `any target` | damage shorthand: creature, player, planeswalker, or battle; nothing else choosable | 115.4 |
| `up to N target` | 0..N; with zero chosen the spell/ability isn't targeted | 115.6 |
| `each [desc]` | untargeted universal over the domain at evaluation time | 109.2 domain; 608.2h read |
| `any number` | includes zero | 107.1c |
| `among [set]` | restricts a selector to a previously computed collection ("from among them") | corpus |
| division `among` targets | split announced with targets, min 1 each (§4) | 601.2d |

**"Another" / "other" — exclusion semantics (verified finding).** The CR
has **no general rule** defining the exclusion — not 109.5 (that defines
"you"/"your", §3); the only rule quoting the word is 115.4 (the
any-target shorthand). It is templating-level English, spelled out inside
keyword definitions when load-bearing: champion (702.72a), soulbond
(702.95a), station (702.184a). Two compilations. *Source-default*:
`[desc] ∧ ≠ this object` ("each other creature with flying", corpus).
*Co-target* ("2 damage to any target and 1 damage to any *other*
target", Arc Trail): a **set-distinctness constraint evaluated on the
final target set**, not exclusion of a fixed binding — retargeting may
swap the two targets, and only the final set is checked for legality
(115.7e).

**Set-level constraints.** Some predicates take the whole declaration set,
not a member: menace's "can't be blocked except by two or more creatures"
(702.111b) is `|S| ≥ 2` over the blocker set — the legality argument is
the set (`deontics.md` §5). The language needs set variables too.

## 3. Binding and anaphora

This section also covers stored per-object slots — it **folds what was
sketched as a standalone object-memory doc**; there is no separate file.

- **"You"/"your"** (109.5): the object's controller, its would-be
  controller while being played/cast/activated, or its owner if it has no
  controller — with per-ability-kind refinements (activator for activated
  abilities; controller-at-trigger-time for triggered ones).
- **Self-reference**: an object naming itself means *that very object*,
  not name-mates (201.5); a granted ability naming its granter tracks the
  specific source object (201.5a); an ability gained by a differently
  named object reads the old name as the new object (201.5b). Surface
  forms (full name, "this ⟨type⟩"): `grammar.md` §5.
- **Pronouns**: "it" / "that [noun]" / "those [nouns]" bind to the most
  recent matching antecedent in the same ability (`grammar.md` §5).
  Amount anaphora — "that much" — binds a previously computed quantity
  (corpus example in §6).
- **Bindings vs zone changes**: an object that changes zones becomes a
  new object with no memory of its previous existence — the 400.7 default
  *breaks* bindings. Its exceptions 400.7a–m make "return it to the
  battlefield… it gains haste" work: especially 400.7j, an effect (or the
  spell or ability whose cost moved the object) can find the new object
  it moved to a *public* zone. With no exception and the object merely
  gone from its expected zone, value reads fall back to LKI (608.2h, §5);
  contrast "that targets [something]": *current* state only, departed
  targets ignored, no LKI (115.9b).
- **"This way" = agent-identity equality** (`events.md` §3): match exactly
  the logged events whose cause-agent is *this* spell or ability instance.
  Corpus: "Creatures destroyed this way can't be regenerated." Related:
  later sentences modify the meaning of earlier ones — read the whole
  text (608.2c).
- **Stored bindings / object memory.** Linked abilities: the second
  ability refers *only* to what the first did, never to another ability's
  results (607.1). The full slot schema (the 607.2 letters): cards
  exiled-with (607.2a; via replacement, 607.2b; while paying the spell's
  cost, 607.2q; the "exiled with [this]" idiom, 406.6); objects put onto
  the battlefield / created with (607.2c); the chosen [value] (607.2d);
  noted information (607.2e); a chosen rules-meaningless word (607.2f); a
  cost paid as it entered (607.2g); actions taken under a same-paragraph
  static (607.2h, 603.11); whether an additional cost was paid (607.2i)
  and its chosen value (607.2j); champion's exile/return pair (607.2k);
  the chosen anchor word (607.2m; mechanics 614.12c, joint cost-payability
  for simultaneous entries 614.12b). Two letters break the strictly
  per-object framing: 607.2n links *across objects by name* (pre-game
  exile read by "cards named [this name]"), and 607.2p's pre-game CDA
  choice *persists across zone changes*, surviving 400.7. Links may also
  span creator and created: a token, emblem, or permanent put onto the
  battlefield by the source's ability (607.1d). **Copy multiplicity**
  (607.3): if the first ability ran multiple times (usually a copied
  ability), the slot is multi-valued — a variable reading it takes the
  SUM of the answers, actions on "the" card hit each card, and "a" card
  means the ability's controller picks one. Slot inventory: `state.md`
  §6; slot queries are ordinary predicates with the slot as an extra
  context coordinate ("Sacrifice a creature of the chosen type", corpus).
  **Hidden slots**: hidden agenda's noted name is readable only through
  the same object's linked "chosen name" ability (702.106d) — a slot
  with a visibility mask (`information.md` §4).

## 4. Values

**X — the lock point varies by context** (the trio):

| Context | X determined | Rule |
|---|---|---|
| Mana/alternative/additional/activation cost | chosen and announced as part of casting/activating; fixed while on the stack | 107.3a |
| Ward X (and other resolution-evaluated costs) | at resolution of the demanding ability — not locked at trigger | 702.21b |
| Special-action cost (suspend, morph) | immediately before paying | 107.3d |

Refinements: X only in *text* is chosen at stack-put or resolution, as
appropriate (107.3f); text-*defined* X is computed, not chosen, and may
change while on the stack (107.3c); off the stack X = 0 (107.3g; mana
value likewise, 202.3e); an enters ability's X inherits the spell's
announced X (107.3m); another object's {X} reads that object's value
(107.3e). Cost-side: `costs.md` §3; the choice record: `choices.md` §2.

**`*` P/T — two mechanisms** (208.2): either a CDA computing it from a
stated condition — functions in every zone, even outside the game, with
can't-determine → 0 (208.2a; CDA criteria 604.3, 604.3a) — or a
*replacement effect* setting it to one of several listed values as the
creature enters or is turned face up; the choice is copiable, and off the
battlefield such a card's P/T is each considered 0 (208.2b). P/T CDAs
apply in the first layer-7 sublayer (613.4a); every other P/T effect
stacks on top of the computed base.

**Undefined and missing values — ⊥ with two coercions.** Anything that
needs a number it can't determine uses 0 instead (107.2). P/T *existence*
is separate: a noncreature permanent has no power or toughness at all; a
noncreature object off the battlefield has them only if printed (208.3);
a creature somehow lacking a value for one has 0 (208.5). An *undefined
linked choice* — an ability copied without its linked partner, or with no
choice made for it — differs in kind: that part of the ability does
nothing, a NO-OP rather than a zero (607.5a). Engine: undefined is ⊥ with
two coercions — ⊥→0 numeric (107.2), ⊥→skip-that-part choice (607.5a).

**Count expressions**: "the number of [desc]", "equal to", and scaling
"for each [desc]" all denote `Count` over a domain (§1's 109.2 defaults);
corpus: "…deals damage equal to the number of creatures you control…".
Timing is *not* uniform (§5): a one-shot effect reads the count once, as
it applies (608.2h); a continuous effect from a resolved spell or ability
locks variables at resolution (611.2d) and separately freezes its affected
set (611.2c); a static's count re-evaluates at all times (611.3a).

**Arithmetic and rounding**: integers only (107.1). **No global rounding
default** — an effect that could produce a fraction states the direction
itself (107.1a): "loses half their life, *rounded up*" (corpus; "rounded
down" likewise attested). Negatives are used in calculations and
comparisons, but a negative *result* becomes 0 — except effects that
double, triple, or set life or P/T (107.1b). "Twice/half" are plain
arithmetic: "…X is twice the number of cards exiled this way" (corpus).

**Division**: targeted division ("divided as you choose among one or two
targets") is announced together with the targets and **each target must
receive at least one** of what's divided (601.2d). *Untargeted* division
is chosen at resolution instead, with the same min-1-per-chosen floor
(608.2d). Retargeting never changes the original division (115.7f).

## 5. Evaluation timing

- **Continuous (statics)**: a static's effect isn't locked in — it applies
  at any moment to whatever its text then indicates (611.3a), at all
  times the source is in the right zone (611.3b); CDAs evaluate in every
  zone (604.3).
- **Locked at announce**: target set and count (601.2c), division
  (601.2d), cost-position X (107.3a). The lock table across all docs:
  `temporal.md` §3.
- **Locked at resolution**: a continuous effect generated by a resolved
  spell or ability fixes any variable once, on resolution (611.2d). A
  *distinct* lock: if it modifies characteristics or changes control, its
  affected set is determined when the effect begins and never changes
  (611.2c) — rule-modifying parts are not frozen this way.
- **Resolution re-checks**: target legality is re-tested (608.2b — source
  gone means LKI; all-illegal means the spell doesn't resolve; partially
  illegal targets are skipped by the parts they're illegal for);
  instructions run in written order (608.2c); resolution choices admit
  only legal options (608.2d), with the empty-library draw carve-out
  (121.3); intervening-if conditions are queried twice — at trigger and
  at resolution (603.4, 608.2a).
- **One-shot reads** (one-shot effects only): information the game
  supplies is determined once, when the effect is applied (608.2h).
- **LKI as query-context substitution**: when the queried object has left
  the public zone it was expected in, every predicate and value above is
  evaluated against its last-known snapshot instead of live state (608.2h,
  113.7a); for a batch of state-based actions the snapshot is taken
  *before* the batch (704.8). Duration/window taxonomy: `temporal.md`.

## 6. Grammar mapping (surface form → AST)

Surface forms from `grammar.md` §5–6; every example is a real corpus line.

| Surface form | AST node | Corpus example |
|---|---|---|
| `target [desc]` | `Select{target, pred, n, lock:announce}` (115.1) | "Destroy up to X target nonblack creatures…" |
| `any target` | `Select{target, pred:damageable}` (115.4) | "It deals that much damage to any target." |
| `up to N target` | count 0..N (115.6) | "Chandra deals 1 damage to up to one target player or planeswalker." |
| `each [desc]` | `Forall{pred}` | "…deals 1 damage to each other creature with flying." |
| `another/other [desc]` | `pred ∧ Exclude(binding)` (§2) | "Polukranos fights another target creature." |
| `from among [set]` | `Subset{set}` | "You may put a creature card from among them into your hand." |
| `where X is …` | `Let{X ← Value}` (107.3f) | "…where X is the number of Shrines you control." |
| `the number of` / `for each` | `Count{pred, timing}` — timing per §5: one-shot read / resolution lock / continuous | "[0]: Surveil 2. Then draw a card for each opponent who lost life this turn." |
| `that much` | `ValueRef(antecedent)` | "Remove any number of charge counters from this artifact: It deals that much damage to any target." |
| `twice/half …, rounded up/down` | `Arith` (107.1a) | "…that player loses half their life, rounded up." |
| `divided as you choose among` | `Divide{min:1, lock:announce}` (601.2d) | "[−2]: Ral deals 3 damage divided as you choose among one, two, or three targets." |
| `the chosen [value]` | `SlotRef(607.2d)` | "Sacrifice a creature of the chosen type: …" |
| `exiled with [this]` | `SlotRef(607.2a)` | "Choose a card exiled with this artifact. You may play that card this turn." |
| `[verb]ed this way` | `AgentEq(self)` (events.md §3) | "Creatures destroyed this way can't be regenerated." |

## 7. Engine note — the parser↔engine contract

```
Pred  ::= Char(field, op, Value)        # 109.3 fields, layer outputs (613.4)
        | Status(cat, val)              # 110.5
        | Zone(z) | Controller(p) | Owner(p) | AttachedTo(x)
        | Targets(mode, …)              # 115.9a–c three modes
        | AgentEq(self) | SlotPred(slot, Pred)
        | And | Or | Not | Exclude(binding)
Sel   ::= Target{Pred, count, lock} | Forall{Pred}
        | Subset{set, count} | SetPred{S, Pred(S)}   # menace-style
Value ::= Const(n) | X{lock_point}      # announce | resolution | pre-payment
        | Star(mode)                    # 208.2a CDA | 208.2b enters-replacement
        | Count(Pred, timing)           # §5: one-shot | resolution lock | continuous
        | Arith(op, Value…, round?)
        | ValueRef(binding) | SlotRef(slot)
        | ⊥                              # coerced: →0 numeric (107.2), →no-op choice (607.5a)
QueryCtx = {state, event?, bindings, slots(+visibility), lki_snapshots}
```

`grammar.md`'s parser emits these nodes; the engine evaluates them
against a `QueryCtx` whose timing discipline is §5. Consumers embed the
nodes directly: `deontics.md` guards are `Pred` over action instances,
`events.md` trigger conditions are `Pred` over (event, state), `costs.md`
scaling riders are `Value`, `choices.md` option filters are `Pred`, and
`keyword-classification.md`'s composite rows bottom out in these nodes.

## Cross-references

- `grammar.md` §5–6 — the surface forms compiled into §6's AST.
- `events.md` §3, §6 — cause/agent coordinate; (event, state) predicates.
- `deontics.md` — `where ⟨pred⟩` guards; set-level legality (§5 there).
- `costs.md` / `choices.md` — X announcement, division locks, option
  legality filtering.
- `state.md` §5–6 — characteristics vs per-object state; slot inventory.
- `information.md` §4 — visibility masks on hidden slots.
- `temporal.md` — durations, windows, and the cross-doc lock table.
