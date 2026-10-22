# Costs — The Cost Algebra

*Synthesized from the Comprehensive Rules effective 2026-09-25
(`data/rules/cr.json`).*

What a cost is, where costs attach, what resources they consume, how the
total is computed and locked, and when payment can fail. The reduction
arithmetic and the casting-pipeline context live in `casting.md` §2 (don't
re-derive them here); the may/can't/toll legality algebra lives in
`deontics.md`; payment as an event batch lives in `events.md`.

## 1. What a cost is — and isn't

A **cost** is an action or payment necessary to take another action or to
stop another action from taking place; paying it means carrying out the
instructions specified by the spell, ability, or effect that contains it
(118.1). If a cost includes a mana payment, the payer gets a chance to
activate mana abilities; paying the cost of a spell or activated ability
follows 601.2f–h (118.2).

The cost-vs-effect boundary, by syntax:

- **Before the colon** — everything before the ":" of an activated ability
  is its activation cost, paid by the activating player (602.1a). Text
  after the colon may define further aspects of the cost (602.1b), and a
  modification of how the activation cost is paid applies to the ability's
  total cost (602.1e).
- **"As an additional cost …" clauses** — costs in rules text, paid along
  with the mana/activation cost (118.8).
- **Loyalty symbols** — an activated ability with a loyalty symbol in its
  cost is a loyalty ability (606.2), and its cost is putting that many
  loyalty counters on the permanent or removing them (606.4). The +N/−N is
  *in the cost*, so
  counter-doublers — which key on *effects* putting counters (614.16) —
  don't touch it, while a planeswalker's entering loyalty (an effect) is
  doubled. That distinction decided the Doubling Season ruling
  (official guidance: `scripts/rulings "Doubling Season"`).
- **Resolution-stage payments** — "Counter target spell unless its
  controller pays {3}" (Mana Leak). The CR is explicit that the unless-action
  *is* a cost, paid when the containing spell or ability resolves
  (118.12, 118.12a) — but its *position* is an instruction inside the
  resolving object's effect. It is not a cost of the original action: the
  targeted spell was cast fully and legally with its own costs. This is
  exactly `deontics.md`'s toll split — declaration-gating tolls condition
  legality; resolution-stage tolls leave the action legal and punish later.

## 2. Positions — where costs attach

| Position | Lives where | Paid when | Rules |
|---|---|---|---|
| **Printed mana cost** | symbols in the card's upper corner | 601.2h, as part of the total | 202.1, 202.1a |
| **Activation cost** | before the ":" (loyalty symbols included) | 602's mirror of 601.2f–h | 602.1a, 606.2, 606.4 |
| **Additional — mandatory** | rules text or outside effect; "As an additional cost…" | with the mana/activation cost; any number may stack | 118.8, 118.8a |
| **Additional — optional** | keyword slots (kicker) and "you may" clauses | announced at 601.2b, paid at 601.2h | 118.8b, 702.33a |
| **Alternative** | rules text or outside effect; "rather than pay" | instead of the mana cost; **only one** per spell | 118.9, 118.9a, 601.2b |
| **Declaration toll** | "can't attack/block unless [player] pays…" | as attackers/blockers are declared; never *required*; total locked at 508.1h/509.1d, then paid in any order | 508.1d, 509.1c, 508.1h–j, 509.1d–f |
| **Optional attack cost** | "as [this creature] attacks" costs a player may pay (enlist) | chosen at 508.1g, then totalled, locked and paid with the declaration costs | 508.1g, 702.154b, 508.1h–j |
| **Resolution toll** | ward; "unless … pays" inside a resolving object | during resolution of the trigger/spell that demands it | 702.21a, 118.12a |
| **Recurring** | echo [cost]; cumulative upkeep [cost] | during resolution of the keyword's upkeep trigger | 702.30a, 702.24a |
| **Special action** | [cost] a special action references (suspend, morph) | as the special action is taken; X and multi-way symbols chosen immediately before payment | 107.3d, 118.13c |
| **Replacement cost** | "As [this permanent] enters, you may pay …" (shockland) | as the permanent enters; with several permanents entering at once, no choice may leave the combined costs unpayable | 614.1c, 614.12b |

Notes per row:

- **Additional** costs don't change the spell's mana cost, only what's paid
  (118.8d); they can come from keywords (kicker: "you may pay an additional
  [cost] as you cast this spell," 702.33a) or be imposed by other effects
  (118.8). Intentions are announced at 601.2b.
- **Alternative**: only one alternative cost (or alternative casting
  method) can apply to one spell (118.9a, 601.2b); generally optional
  (118.9b), though an effect granting the cast may force it (118.9b).
  Additional costs, increases, and reductions then apply *on top of* the
  alternative (118.9d). "Without paying its mana cost" is the limiting
  case (118.9).
- **Keyword cost class** comes from the keyword's definition: "an
  additional [cost]" or "as an additional cost" makes it additional
  (118.8); "rather than [paying] [its] mana cost" or "without paying its
  mana cost" makes it alternative (118.9). Most such rules end by naming
  the rules they follow ("follows the rules for paying additional costs,"
  702.81a; "... alternative costs," 702.34a), but some don't: offering
  (702.48a), offspring (702.175a), spree (702.172a), tiered (702.183a),
  miracle (702.94a), disturb (702.146a), and sneak (702.190a). Search the
  definition, not that closing sentence. For one keyword's class:
  `scripts/classify <keyword>`.
- **Cast-from-zone permissions carry a cost class, and it decides what
  combines.** A keyword that lets a card be cast from outside the hand
  does so in one of three ways:
  - *Alternative cost*: from the graveyard, flashback (702.34a), escape
    (702.138a), harmonize (702.180a), mayhem [cost] (702.187b), disturb
    (702.146a); from exile, e.g. madness (702.35b), foretell (702.143a),
    plot (702.170d). The permission fills the spell's one alternative-cost
    slot (118.9a, 601.2b), so no other alternative cost applies, "without
    paying its mana cost" included (118.9). Additional costs, increases,
    and reductions still do (118.9d). Official guidance:
    `scripts/rulings "Snapcaster Mage"` (flashback), `"Ox of Agonas"`
    (escape), `"Fist of Suns"` (an outside alternative cost doesn't
    combine with flashback; additional costs do).
  - *Additional cost*: retrace (702.81a) and jump-start (702.133a) pay the
    mana cost plus a discard. The slot stays free, so an alternative cost
    from another source can replace the mana cost while the discard is
    still paid (118.8a, 118.9a, 118.9d); official guidance for jump-start:
    `scripts/rulings "Radical Idea"`. For retrace no ruling covers this;
    the reading is derived from 702.81a, 118.9a and 118.9d.
  - *No cost change*: aftermath (702.127a) and warp's later cast from
    exile (702.185a) grant the zone only; the usual mana cost, or any one
    applicable alternative cost, is paid. Cost-less mayhem (702.187c) is a
    *play* permission; its one printed card is a land, played at no cost
    (305.1).

  601.2b also bars two "alternative methods of casting," a term the CR
  doesn't define. These answers don't depend on it, because 601.2b bars
  two methods or two costs, not one of each. *Engine inference*: give each
  cast permission a cost class (`generalizations.md` §1's cost-mode slot).
  Encoding an additional-cost permission as an alternative cost that
  restates the mana cost ("its mana cost plus a discard, rather than its
  mana cost") fills the 118.9a slot and wrongly refuses another
  alternative cost.
- **Declaration tolls** gate legality of the declaration, but the player is
  never forced to pay — not even to maximize attack/block requirements
  (508.1d, 509.1c). Oracle reminder text agrees: "(This cost is paid as
  attackers are declared.)" Once the total cost to attack or block is
  determined it is "locked in" (508.1h, 509.1d); the player then
  activates mana abilities (508.1i, 509.1e) and pays all costs in any
  order, with no partial payments (508.1j, 509.1f). That is a second lock
  with plain any-order payment, not 601.2h's two-phase ordering; the full
  procedure is in `turn.md`'s 508.1/509.1 tables.
- **Optional attack costs** are costs a player may pay "as" a creature
  attacks; the active player chooses which, if any, to pay (508.1g) —
  enlist's static ability is one (702.154b). They are totalled with any
  required attack costs and locked and paid under 508.1h–j.
- **Replacement costs**: "As [this permanent] enters, you may pay …"
  effects are replacement effects (614.1c), and the payment is a cost of
  that effect (614.12b). 118.12 covers only spells, activated abilities,
  and triggered abilities, so these are not resolution tolls. When several
  permanents enter at once, the player may not make choices for those
  effects that would leave their combined costs unpayable (614.12b).
- **Resolution tolls**: ward is a *triggered ability* — "counter that spell
  or ability unless that player pays [cost]" (702.21a); a ward X is
  evaluated at resolution, not locked at trigger time (702.21b).
- **Recurring** positions are named [cost] slots paid inside an upkeep
  trigger's resolution: echo — sacrifice unless you pay (702.30a);
  cumulative upkeep — pay per age counter, all-or-nothing, partial payments
  disallowed (702.24a).
- **OR-branch costs** ("forage or pay {B}" — corpus): the branch is
  announced at 601.2b, as part of announcing intentions to pay additional
  costs (118.8a, 601.2b), and paid at 601.2h. The same shape appears for
  hybrid symbols ("announces the nonhybrid equivalent cost," 118.13a) and
  for keyword costs that choose at 601.2b and pay at 601.2h (702.48b,
  702.119c, 702.180b); 601.4 is secondary, covering options that depend on
  choices normally made later. *Derived*
  (UD-19): 601.2f needs the branch to compute the
  total, so it is the latest possible point, and 118.8a and the analogs
  place the choice at 601.2b. Cumulative upkeep instead makes the choice
  separately for each age counter, then pays the entire set or none of it
  (702.24a).
- **Pacts are not a cost position.** "At the beginning of your next upkeep,
  pay {3}{U}{U}. If you don't, you lose the game" (Pact of Negation): the
  pay-action *is* a cost whether or not it's ever paid — 118.12 classifies
  the "[do something]" action as a cost paid at resolution — but the card
  has no cost slot; the spell itself cost {0}, paid in full at casting.
  The wording is 118.12's *mandatory* form ("pay", not "you may pay"); the
  practical right to decline flows from 118.3c — mana abilities are never
  mandatory, so the player can simply not produce the mana. *Derived*:
  118.3c's escape covers only producing mana; if the mana is already in
  the pool, the 118.12 mandatory payment has no opt-out. What the "If you
  don't" clause checks is the 118.12 bullet in §5. Official guidance, as
  corroboration only:
  `scripts/rulings "Pact of the Titan"` ("Okay, you don't have to, but it's
  a fairly good idea"). Echo differs
  precisely in having a parameterized [cost] slot the rules can reference
  and errata can fill (702.30b). Classify pacts as
  trigger-with-resolution-cost, like any other 118.12 instruction.

## 3. Component resources

**Mana symbols** (the closed list is 107.4): numeric and {X} symbols are
generic, payable with any mana (107.4b; when casting or activating, X is
announced at 601.2b per 107.3a);
{C} demands colorless specifically (107.4c); {0} is a placeholder payable
with nothing — but still paid (107.4d, §5); hybrid symbols offer two halves,
monocolored hybrid {2/B} = one black or two generic, and the {C/W} family =
one colorless mana or one mana of the named color (107.4, 107.4e); Phyrexian
and hybrid-Phyrexian symbols offer one mana of the color *or 2 life*
(107.4f); snow {S} takes one mana of any type from a snow source, and
generic reductions don't touch it (107.4h). {H} (107.4g) is a rules-text
referent for the Phyrexian mana symbols, not a payable symbol.

**Other symbols**: {T} taps the permanent — already-tapped can't pay, and a
creature's {T} ability needs continuous control since the controller's most
recent turn began (107.5); {Q} untaps, with the same control constraint
(107.6); {E} removes one energy counter from the player (107.14); loyalty
symbols put loyalty counters on the permanent or remove them (107.7,
606.4); a numbered ticket symbol {TK} is a ticket cost, paid by removing
that many ticket counters from yourself (107.17a).

**Life**: a player may pay life greater than 0 only if their life total is
greater than or equal to the amount; the payment is subtracted from the
life total — "in other words, the player loses that much life" (119.4).
Paying life is thus *one* event with dual identity, cost-payment *and*
life-loss (`events.md`): loss-of-life triggers see it. 0 life is always
payable at any life total, even if an effect says players can't pay life
(119.4b). The pay-fully-or-not-at-all principle is 118.3: a player at
1 life can't pay 2 life.

**Non-symbol action components**: sacrifice, discard, exile, reveal,
return-to-hand, remove counters — any instruction can sit in a cost slot
("{1}{G}, Remove a +1/+1 counter from this creature:", "As an additional
cost to cast this spell, sacrifice a creature" — corpus). **Keyword actions
serve as cost components** too: collect evidence N — exile cards totaling
mana value N+ from your graveyard (701.59a), unchoosable if you can't reach
N (701.59b); forage — exile three from graveyard or sacrifice a Food
(701.61a). Corpus shows both in activation-cost position ("{2}, Forage:")
and additional-cost position ("As an additional cost to cast this spell,
forage or pay {B}").

**Open vs closed**: the symbol vocabulary is closed — 107.4 enumerates every
mana symbol, and 107.5, 107.6, 107.7, 107.14 and 107.17 give the non-mana
cost symbols. The action-component vocabulary is open — a cost is "carrying
out the instructions" (118.1), so any imperative the game can express can be
priced. An engine should hard-code symbol payment and interpret action
components through the same machinery as effect instructions.

## 4. Modification pipeline — and payment-stage substitution

The computation is `casting.md` §2's; one line here: **base (mana or
alternative, per 601.2b) → + additional costs and increases → − reductions
(any order) → mana floor {0} → effects that directly affect the total →
LOCKED** (601.2f). After the lock, nothing changes the total — the 601.2h
example: sacrificing your cost-reducer *as part of payment* doesn't re-raise
the price. Paying a changed or reduced cost still counts as paying the
original (118.7, 118.11).

**Payment-stage substitutions are a different animal**, and they come in two
scopes.

- **(a) Whole-total substitutions.** Convoke, delve, and improvise each
  state that the ability "isn't an additional or alternative cost and
  applies only after the total cost ... is determined" (702.51b, 702.66b,
  702.126b): tap a creature per colored/generic mana (702.51a), exile a
  graveyard card per generic mana (702.66a), tap an artifact per generic
  mana (702.126a). Assist modifies the rules of payment itself (explicitly
  601.2g–h): a chosen player may pay any amount of the generic component
  before you do (702.132a), so it changes *who* pays. None of them touch
  the locked total; they edit *how* (or by whom) it is paid, inside the
  601.2g–h payment window.
- **(b) Per-component substitutions.** "Waterbend [cost]" means "Pay
  [cost]. For each generic mana in that cost, you may tap an untapped
  artifact or creature you control rather than pay that mana" (701.67a).
  The substitution attaches to its own cost component and may pay only the
  generic mana in the waterbend cost itself, even if the total cost holds
  other generic mana (701.67b). It is applied wherever that component is
  paid: in an activation or additional cost (701.67b), in an alternative
  cost (Hama:
  "by waterbending {X} rather than paying its mana cost" — corpus), as a
  resolution "unless" cost ("discard a card unless you waterbend {2}" —
  corpus; 118.12, 118.12a), or inside ward ("Ward—Waterbend {4}" — corpus;
  702.21a). "Whenever a player waterbends" triggers however the cost was
  paid (701.67c).

**This section is the defining home of `keyword-classification.md`'s
`cost-modification-hook` primitive**: one primitive, a *payment
substitution*, with two scopes. Scope (a) is a permission that edits how an
already-determined total cost is paid — neither additional nor alternative
— and applies to the whole total during 601.2g–h: convoke, delve and
improvise, with assist changing who pays. Scope (b) is a permission
attached to one cost component and applied wherever that component is
paid: waterbend. All five compile to this one primitive. An engine needs
both attachment points: a whole-total substitution at 601.2g–h for (a), plus
a per-component substitution invoked wherever that component is paid for
(b).

## 5. Payability

- **Unpayable costs** (118.6): no mana cost = unpayable; *attempting* to
  cast such a spell is legal, *paying* the unpayable cost is illegal.
  Increases and additional costs keep it unpayable, but an alternative cost
  — including "without paying its mana cost" — can be paid (118.6a).
  Failure at the payment step is not a special case: being unable to pay at
  601.2h makes the cast illegal and the whole action rewinds (733.1; the
  rewind semantics are `casting.md` §3).
- **{0} is still a payment** (118.5): the action is the player's
  acknowledgment; a {0} spell won't cast itself (118.5a).
- **Multi-way-symbol timing** (Phyrexian, hybrid): for mana costs and
  activation costs, the per-symbol choice is *announced* as the spell or
  ability is proposed (118.13a, 601.2b); the life is actually subtracted at
  payment (601.2h, 118.3b). Resolution-paid and special-action costs choose
  symbols immediately before payment (118.13b–c), and a special-action
  cost's X is chosen immediately before payment too (107.3d). An X in a
  resolution-paid cost is defined by the object's text or chosen at the
  appropriate time (107.3c, 107.3f), and ward's X is determined as the
  ability resolves (702.21b).
- **Partial payment is illegal** (601.2h). Payment ordering: first all
  costs without random elements or library-to-public-zone moves, in any
  order; then the rest, in any order (601.2h). That two-phase ordering is
  601.2h's, which activations share via 602.2b; costs to attack or block
  are paid in any order with no partial payments (508.1j, 509.1f).
- **One payment, one cost** (118.10): one sacrificed creature can't pay two
  sacrifice costs, and a resolving effect doing what a cost asks doesn't pay
  that cost.
- **Modified payment still pays** (118.11): if effects change the actions
  actually performed (e.g. a replaced draw for a "draw a card" cumulative
  upkeep), the cost is still considered paid.
- **"Can't" events make costs unpayable**: a player can't choose to pay a
  cost that includes an event that can't happen (614.17b); the life locks
  below are special cases (119.7, 119.8); `deontics.md` quotes 614.17b.
  Discarding to pay a cost that specifies a characteristic is illegal if
  the card goes to a hidden zone unrevealed (701.9c). Paying 0 life stays
  possible even then (119.4b, §3).
- **Life-total locks make life costs unpayable, whoever's life it is.** A
  cost's action can fall on a player other than the payer ("An opponent
  gains 1 life," Wall of Shards' cumulative upkeep; "you may have an
  opponent gain 3 life," Invigorate's alternative cost); the payer still
  pays by carrying out the instruction (118.1). The lock follows the player
  the action affects: under "can't gain life," a cost that involves having
  that player gain life can't be paid (119.7); under "can't lose life," a
  cost that involves having that player pay life can't be paid (119.8).
  These are not resource checks on the payer (118.3): a gain-life cost
  needs no resources, but it is unpayable while its recipient can't gain
  life. A replacement differs from a lock: if the gain would be replaced
  ("gains no life instead," Sulfuric Vortex), the cost can still be paid
  and counts as paid (118.11); under "can't gain life," the cost is
  unpayable outright, and a replacement effect that would replace that
  player's life gain does nothing (119.7). Official guidance:
  `scripts/rulings Invigorate`. Under cumulative upkeep, the choice of
  opponent is made separately for each age counter (702.24a), so Wall of
  Shards may name a different opponent per counter
  (`scripts/rulings "Wall of Shards"`).
- **Loyalty costs**: a negative loyalty cost, with any additional costs, is
  unpayable unless the permanent has at least that many loyalty counters
  (606.6); multiple loyalty costs combine into one (606.5).
- **"If you do" checks the choice, not the outcome** (118.12): in "[Do
  something]. If [a player] [does, doesn't, or can't], [effect]," the
  clause checks whether the player chose to pay an optional cost or started
  to pay a mandatory one, regardless of what events actually occurred.
  Standstill's sacrifice can't be paid, so its clause is false; Dermoplasm's
  return still happens although the creature it put onto the battlefield
  entered under another player's control, because the player chose to pay
  (118.12 examples). Related one-liners: an "If you do" after an offered
  search checks only that the player chose to search (118.12b); a
  mandatory additional cost naming cards with a stated quality in a hidden
  zone doesn't force a spell cast "if able" (118.8c); "mana of any type can
  be spent" lets mana pay as though colorless or any color (118.14); in
  Two-Headed Giant, paying life is limited by the team's life total
  (119.4a).
- **Mana abilities are never forced** (118.3c): activating them is not
  mandatory even when paying a cost is — the engine may not auto-tap a
  player into a mandatory payment.

## 6. Grammar markers (corpus-verified)

Counts are `scripts/corpus --match` lines in the default (supported) scope
and drift with data refreshes.

| Marker | Position signaled | Corpus evidence |
|---|---|---|
| `[Cost]:` | activation cost (602.1a) | "{1}{B}, Remove a +1/+1 counter from this creature: …" |
| `As an additional cost to cast this spell,` | additional cost (118.8) | 158 distinct lines |
| `rather than pay` | alternative cost (118.9) | 130 distinct lines |
| `You may pay [cost] rather than` | optional alternative (118.9b) | 55 distinct lines |
| `without paying its mana cost` | alternative, limiting case (118.9) | 377 distinct lines |
| `unless you pay` / `unless … pays` | resolution toll (118.12a, 702.21a) | 145 distinct "unless you pay" lines |
| `can't attack unless` | declaration toll (508.1d) | 41 distinct lines; reminder text "(This cost is paid as attackers are declared.)" |
| `for each` | scaling cost component | additional-cost-with-"for each" lines; cumulative upkeep pays per age counter (702.24a) |

Bare `unless … pays` signals a resolution toll, but a `can't attack/block
… unless` prefix re-binds the same word to a *declaration* toll — paid as
attackers or blockers are declared (508.1d, 509.1c), never at resolution:
the total is locked in (508.1h, 509.1d), mana abilities come next (508.1i,
509.1e), and the costs are paid in any order with no partial payments
(508.1j, 509.1f).

## 7. Engine note

```
Cost {
  components: [Component],      # symbol | life | action(instruction) | keyword-action
  position:   MANA | ACTIVATION | ADDITIONAL | ALTERNATIVE
            | DECLARATION_TOLL | OPTIONAL_ATTACK_COST | RESOLUTION_TOLL
            | RECURRING | SPECIAL_ACTION | REPLACEMENT_COST,
  optional:   bool,             # 118.8b / 118.9b / 508.1g / toll choices
  modification_trace: [Step],   # base → +adds/incr → −reductions → floor → direct → lock (601.2f)
  locked:     bool,             # position-dependent, see below; whole-total substitutions may not edit the total after
}
```

`locked` is set where the position's pipeline locks the total: at 601.2f
for spells, at 602.2b (which applies 601.2f) for activations, and at
508.1h / 509.1d for declaration costs (`DECLARATION_TOLL`,
`OPTIONAL_ATTACK_COST`). `REPLACEMENT_COST` makes no `locked` claim beyond
being determined as the permanent enters (614.12b). Ordering likewise
varies by position: the two-phase ordering is 601.2h's (casting, and
activating via 602.2b); declaration costs use 508.1j / 509.1f's any-order
payment.

Payment is a **transactional event batch** (`events.md`): collect the
component events (mana removed, life subtracted, permanents tapped or
sacrificed, counters removed…), order them per the position's rule (601.2h's
two-phase rule for spells and activations; any order for declaration costs,
508.1j, 509.1f), apply `cost-modification-hook` substitutions (§4) at
payment time — whole-total ones during 601.2g–h, per-component ones
wherever their component is paid — and commit atomically — partial payment is illegal (601.2h), so any failure
aborts the whole action per 733.1's rewind — with 733.1's precise carve-out:
moves *to* a library, moves from a library to any zone *other than the
stack*, shuffles, and library reveals can't be reversed, but a
library-to-stack move can. Cause-tag every event in
the batch as cost-payment (`events.md` §3): "sacrificed to pay a cost" vs
"sacrificed by an effect" is trigger-visible language, and 118.10's
one-payment-one-cost rule needs the batch boundary to be first-class.
