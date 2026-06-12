# Costs — The Cost Algebra

*Synthesized from the Comprehensive Rules effective 2026-04-17
(`data/rules/cr.json`). Orientation only — verify load-bearing specifics
with `scripts/rule` before citing. Run `scripts/cite check` after CR
refreshes.*

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
  is its activation cost, paid by the activating player (602.1a).
- **"As an additional cost …" clauses** — costs in rules text, paid along
  with the mana/activation cost (118.8).
- **Loyalty symbols** — an activated ability with a loyalty symbol in its
  cost is a loyalty ability (606.2). The +N/−N is *in the cost*, so
  counter-doublers — which key on *effects* putting counters (614.16) —
  don't touch it, while a planeswalker's entering loyalty (an effect) is
  doubled. That distinction decided the Doubling Season ruling
  (`rulings-check.md` §6).
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
| **Activation cost** | before the ":" (loyalty symbols included) | 602's mirror of 601.2f–h | 602.1a, 606.2 |
| **Additional — mandatory** | rules text or outside effect; "As an additional cost…" | with the mana/activation cost; any number may stack | 118.8, 118.8a |
| **Additional — optional** | keyword slots (kicker) and "you may" clauses | announced at 601.2b, paid at 601.2h | 118.8b, 702.33a |
| **Alternative** | rules text or outside effect; "rather than pay" | instead of the mana cost; **only one** per spell | 118.9, 118.9a, 601.2b |
| **Declaration toll** | "can't attack/block unless [player] pays…" | as attackers/blockers are declared; never *required* | 508.1d, 509.1c |
| **Resolution toll** | ward; "unless … pays" inside a resolving object | during resolution of the trigger/spell that demands it | 702.21a, 118.12a |
| **Recurring** | echo [cost]; cumulative upkeep [cost] | during resolution of the keyword's upkeep trigger | 702.30a, 702.24a |
| **Special action** | [cost] a special action references (suspend, morph) | as the special action is taken; X and multi-way symbols chosen immediately before payment | 107.3d, 118.13c |

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
- **Declaration tolls** gate legality of the declaration, but the player is
  never forced to pay — not even to maximize attack/block requirements
  (508.1d, 509.1c). Oracle reminder text agrees: "(This cost is paid as
  attackers are declared.)"
- **Resolution tolls**: ward is a *triggered ability* — "counter that spell
  or ability unless that player pays [cost]" (702.21a); a ward X is
  evaluated at resolution, not locked at trigger time (702.21b).
- **Recurring** positions are named [cost] slots paid inside an upkeep
  trigger's resolution: echo — sacrifice unless you pay (702.30a);
  cumulative upkeep — pay per age counter, all-or-nothing, partial payments
  disallowed (702.24a).
- **OR-branch costs** ("forage or pay {B}" — corpus): the branch is fixed
  as the total cost is determined (601.2f); cumulative upkeep instead makes
  the choice separately for each age counter, then pays the entire set or
  none of it (702.24a).
- **Pacts are not a cost position.** "At the beginning of your next upkeep,
  pay {3}{U}{U}. If you don't, you lose the game" (Pact of Negation): the
  pay-action *is* a cost whether or not it's ever paid — 118.12 classifies
  the "[do something]" action as a cost paid at resolution — but the card
  has no cost slot; the spell itself cost {0}, paid in full at casting.
  The wording is 118.12's *mandatory* form ("pay", not "you may pay"); the
  practical right to decline flows from 118.3c — mana abilities are never
  mandatory, so the player can simply not produce the mana. Echo differs
  precisely in having a parameterized [cost] slot the rules can reference
  and errata can fill (702.30b). Classify pacts as
  trigger-with-resolution-cost, like any other 118.12 instruction.

## 3. Component resources

**Mana symbols** (the closed list is 107.4): numeric and {X} symbols are
generic, payable with any mana (107.4b; when casting or activating, X is
announced at 601.2b per 107.3a);
{C} demands colorless specifically (107.4c); {0} is a placeholder payable
with nothing — but still paid (107.4d, §5); hybrid symbols offer two halves,
monocolored hybrid {2/B} = one black or two generic (107.4e); Phyrexian and
hybrid-Phyrexian symbols offer one mana of the color *or 2 life* (107.4f);
snow {S} takes one mana of any type from a snow source, and generic
reductions don't touch it (107.4h).

**Other symbols**: {T} taps the permanent — already-tapped can't pay, and a
creature's {T} ability needs continuous control since the controller's most
recent turn began (107.5); {Q} untaps, with the same control constraint
(107.6); {E} removes one energy counter from the player (107.14).

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
mana symbol. The action-component vocabulary is open — a cost is "carrying
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

**Payment-stage substitutions are a different animal.** Convoke, delve, and
improvise each state they are "*neither an additional nor an alternative
cost*" and apply "only after the total cost is determined": tap a creature
per colored/generic mana (702.51a, 702.51b), exile a graveyard card per
generic mana (702.66a, 702.66b), tap an artifact per generic mana (702.126a,
702.126b). Assist modifies the rules of payment itself (explicitly 601.2g–h):
a chosen player may pay any amount of the generic component before you do
(702.132a). None of them touch the locked total; they edit *how* (or by
whom) it is paid, inside the 601.2g–h payment window.

**This section is the defining home of `keyword-classification.md`'s
`cost-modification-hook` primitive**: a permission that edits how an
already-determined total cost is paid — neither additional nor alternative.
Delve, convoke, improvise, assist, and waterbend all compile to this one
hook; an engine that exposes a payment-substitution interface at 601.2g–h
gets all five for free.

## 5. Payability

- **Unpayable costs** (118.6): no mana cost = unpayable; *attempting* to
  cast such a spell is legal, *paying* the unpayable cost is illegal.
  Increases and additional costs keep it unpayable, but an alternative cost
  — including "without paying its mana cost" — can be paid (118.6a).
  Failure at the payment step is not a special case: being unable to pay at
  601.2h makes the cast illegal and the whole action rewinds (733.1; the
  unified rewind semantics are `casting.md` §3).
- **{0} is still a payment** (118.5): the action is the player's
  acknowledgment; a {0} spell won't cast itself (118.5a).
- **Multi-way-symbol timing** (Phyrexian, hybrid): for mana costs and
  activation costs, the per-symbol choice is *announced* as the spell or
  ability is proposed (118.13a, 601.2b); the life is actually subtracted at
  payment (601.2h, 118.3b). Resolution-paid and special-action costs choose
  symbols — and X — immediately before payment (118.13b–c, 107.3d).
- **Partial payment is illegal** (601.2h). Payment ordering: first all
  costs without random elements or library-to-public-zone moves, in any
  order; then the rest, in any order (601.2h).
- **One payment, one cost** (118.10): one sacrificed creature can't pay two
  sacrifice costs, and a resolving effect doing what a cost asks doesn't pay
  that cost.
- **Modified payment still pays** (118.11): if effects change the actions
  actually performed (e.g. a replaced draw for a "draw a card" cumulative
  upkeep), the cost is still considered paid.
- **Life-total locks make life costs unpayable**: under "can't gain life,"
  a cost that involves that player gaining life can't be paid (119.7);
  under "can't lose life," a cost that involves that player paying life
  can't be paid (119.8).
- **Mana abilities are never forced** (118.3c): activating them is not
  mandatory even when paying a cost is — the engine may not auto-tap a
  player into a mandatory payment.

## 6. Grammar markers (corpus-verified)

| Marker | Position signaled | Corpus evidence |
|---|---|---|
| `[Cost]:` | activation cost (602.1a) | "{1}{B}, Remove a +1/+1 counter from this creature: …" |
| `As an additional cost to cast this spell,` | additional cost (118.8) | 139 distinct lines |
| `rather than pay` | alternative cost (118.9) | 127 distinct lines |
| `You may pay [cost] rather than` | optional alternative (118.9b) | 52 distinct lines |
| `without paying its mana cost` | alternative, limiting case (118.9) | 361 distinct lines |
| `unless you pay` / `unless … pays` | resolution toll (118.12a, 702.21a) | 145 distinct "unless you pay" lines |
| `can't attack unless` | declaration toll (508.1d) | 40 distinct lines; reminder text "(This cost is paid as attackers are declared.)" |
| `for each` | scaling cost component | additional-cost-with-"for each" lines; cumulative upkeep pays per age counter (702.24a) |

Bare `unless … pays` signals a resolution toll, but a `can't attack/block
… unless` prefix re-binds the same word to a *declaration* toll — paid as
attackers or blockers are declared (508.1d, 509.1c), never at resolution.

## 7. Engine note

```
Cost {
  components: [Component],      # symbol | life | action(instruction) | keyword-action
  position:   MANA | ACTIVATION | ADDITIONAL | ALTERNATIVE
            | DECLARATION_TOLL | RESOLUTION_TOLL | RECURRING | SPECIAL_ACTION,
  optional:   bool,             # 118.8b / 118.9b / toll choices
  modification_trace: [Step],   # base → +adds/incr → −reductions → floor → direct → lock (601.2f)
  locked:     bool,             # set at 601.2f; substitutions may not edit the total after
}
```

Payment is a **transactional event batch** (`events.md`): collect the
component events (mana removed, life subtracted, permanents tapped or
sacrificed, counters removed…), order them per 601.2h's two-phase rule,
apply `cost-modification-hook` substitutions (§4) at payment time, and
commit atomically — partial payment is illegal (601.2h), so any failure
aborts the whole action per 733.1's rewind — with 733.1's precise carve-out:
moves *to* a library, moves from a library to any zone *other than the
stack*, shuffles, and library reveals can't be reversed, but a
library-to-stack move can. Cause-tag every event in
the batch as cost-payment (`events.md` §3): "sacrificed to pay a cost" vs
"sacrificed by an effect" is trigger-visible language, and 118.10's
one-payment-one-cost rule needs the batch boundary to be first-class.
