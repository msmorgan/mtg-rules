# Casting — The Spell/Ability Pipeline

*Synthesized from the Comprehensive Rules effective 2026-04-17
(`data/rules/cr.json`). Orientation only — verify load-bearing specifics
with `scripts/rule` before citing. Run `scripts/cite check` after CR
refreshes.*

How an engine moves an object onto the stack, pays for it, and resolves it.
Casting (601) and activating (602) share one step machine; resolving (608)
is the consumer. For the abilities that get cast/activated, see
`abilities.md`; for the zones and stack they read/write, see `state.md`; for
the one-shot/continuous effects resolution produces, see `effects.md`.

## 1. The 601.2 step sequence

To cast a spell is to move it from where it is (usually hand) to the stack
and pay its costs (601.2). The casting is split into **proposal** (601.2a–d)
and **determination + payment of costs** (601.2f–h) (601.2). Steps run **in
order**; if a player can't comply with a step while performing it, the cast
is illegal and the game rewinds to before proposal (601.2, see §3). A player
must be legally allowed to begin (601.3, see §3).

1. **601.2a — move to stack.** Move the card (or copy) to the stack as the
   topmost object; it gets all the card's characteristics and the player
   becomes its controller. Cast-time continuous characteristic-modifiers
   (611.2f) and one-shot ability-granting effects (610.5) begin applying here
   (601.2a, 611.2f, 610.5).
2. **601.2b — choices: modes / splice / alt+additional costs / X / hybrid /
   Phyrexian.** Announce modal choice, reveal splice cards, declare intent to
   pay alternative and/or additional costs (buyback, kicker), announce the
   value of any {X}, and choose how hybrid/Phyrexian symbols will be paid
   (601.2b). **Only one alternative cost *and* one alternative casting method
   per spell** — 601.2b alone bars two alternative *methods of casting* or two
   alternative *costs*; 118.9a covers only the one-alternative-cost half
   (601.2b, 118.9a). This step picks *what* the cost will be; it does not pay
   it.
3. **601.2c — targets.** Announce a target for each required target; targeting
   triggers fire now but wait to go on the stack until casting finishes
   (601.2c). Target count, once determined, doesn't change (601.2c).
4. **601.2d — division.** If the spell divides/distributes (damage, counters)
   among targets, announce the division; each target gets at least one
   (601.2d).
5. **601.2e — legality check.** The game checks the proposed spell is legal
   to cast; if illegal, rewind to before proposal (601.2e, rule 733). This is
   the legality gate at the *end of proposal*; for the unified rewind semantics
   (can't-comply, can't-pay, and post-proposal prohibitions all rewind) see §3.
6. **601.2f — determine total cost; lock it in.** Total cost = the mana cost
   *or* alternative cost (chosen in 601.2b) **plus** all additional costs and
   cost **increases**, **minus** all cost **reductions** (601.2f). Multiple
   reductions may be applied **in any order** by the player; the mana
   component floors at {0} and can't go below (601.2f). Then "any effects that
   directly affect the total cost are applied," after which the total cost
   is **"locked in"** — later cost-changing effects do nothing (601.2f). This
   is the letter that locks the cost.
7. **601.2g — mana abilities.** If the total cost includes mana, the player
   may now activate mana abilities; they must be activated **before** costs
   are paid (601.2g, 605).
8. **601.2h — pay.** Pay the total cost: first all costs without random
   elements or library-to-public-zone moves (any order), then the rest (any
   order). No partial payments; unpayable costs can't be paid (601.2h).
9. **601.2i — spell becomes cast.** Once 601.2a–h finish, cast-as-it's-cast
   characteristic modifiers apply and the spell **becomes cast**. Cast/
   put-on-stack triggers (including the targeting triggers from 601.2c) fire
   now; the controller, if they had priority, gets priority back (601.2i).

601.4 lets a player make a normally-later choice early when an earlier choice
depends on it (e.g. announcing extra modes that only a later kicker payment
unlocks) (601.4). 601.7: casting a cost-altering spell doesn't touch spells/
abilities already on the stack (601.7).

## 2. Costs (118)

A cost is an action/payment necessary to take another action (118.1). You
can't pay a cost without resources to pay it fully (118.3); paying mana
removes it from the pool, paying life subtracts it (118.3a, 118.3b);
activating mana abilities is never mandatory (118.3c).

- **Additional costs** (118.8) — paid at the same time as the mana/activation
  cost; *any number* may apply (118.8a); some optional (118.8b). They don't
  change the spell's mana cost, only what's paid (118.8d).
- **Alternative costs** (118.9) — paid *instead of* the mana cost; **only one
  per spell** (118.9a), generally optional (118.9b). Additional costs,
  increases, and reductions still apply *on top of* an alternative cost
  (118.9d). Doesn't change the spell's mana cost (118.9c).
- **Total cost & order (601.2f):** base (mana or alternative) **+ additional
  costs + increases − reductions**, reductions in any order, mana floored at
  {0}, then direct total-cost effects, then **locked in** (601.2f). Generic
  reductions hit only the generic component (118.7a); a colored/colorless
  reduction with no matching component spills to generic (118.7b); over-
  reduction of a colored/colorless component spills the remainder to generic
  (118.7c, 118.7d); hybrid/Phyrexian/snow reductions resolve per 118.7e–g.
- **"Cost can't be paid" vs "can't cast":** beginning to cast is gated by
  601.3 / 601.2e (legality). Failing to *pay* at 601.2h is a separate failure,
  but it is **not** exempted from rewind: being unable to comply with 601.2h
  makes the cast illegal and the game returns to before proposal (601.2 intro,
  733.1). A later *prohibition* rewinds too (601.5) — nothing survives a
  completed proposal except conditional flash (601.5a). Paying a reduced/changed
  cost still counts as paying the original (118.7, 118.11).
- **X handling:** if X isn't defined by text, the controller announces it as
  part of casting, at 601.2b (107.3a, 601.2b). A spell cast for neither its
  mana cost nor an X-bearing alternative cost forces X = 0 (107.3b). Cards off
  the stack treat {X} as 0 (107.3g).
- **Free / {0} costs (118.5):** a {0} cost (or one reduced to {0}) still must
  be paid — the payment is the player's acknowledgment; it isn't automatic
  (118.5, 118.5a).
- **Unpayable costs (118.6):** an object with no mana cost has an unpayable
  cost. *Casting* it is legal; *paying* the unpayable cost is illegal
  (118.6). Increases/additional costs keep it unpayable, but an alternative
  cost (incl. "without paying its mana cost") can be paid (118.6a).
- Each payment applies to only one spell/ability/effect (118.10).

## 3. Backing out / illegal casts

A player may **begin** casting only if a rule/effect allows it and none
prohibits it (601.3). The 601.3 sub-letters split into two jobs: **601.3a**
lets a player **ignore a prohibition** when a yet-to-be-made proposal choice
could change the prohibited quality (Void Winnower vs an {X} spell);
**601.3b–d** let a player **gain flash** — 601.3b when a proposal choice could
change the spell's qualities to match a flash-granting effect (bestow → Aura),
601.3c when flash is granted only if an alternative/additional cost is paid,
601.3d when the spell has flash only while certain conditions are met; and
**601.3e–f** are **legality checks**, 601.3e for casting under an alternative
set of characteristics (morph/adventure off the top of library) and 601.3f for
casting from among **face-down cards in exile** (only if the player may look at
the card) (601.3a, 601.3b, 601.3c, 601.3d, 601.3e, 601.3f).

Both kinds of "cost trouble" rewind — they are not opposed cases:

- **(a) Can't comply / can't pay → full rewind.** If a player is *unable to
  comply* with the requirements of any step 601.2a–i — including determining
  the cost (601.2f) or *paying* it (601.2h) — the cast is illegal and the game
  **returns to the moment before proposal** (601.2 intro). The rewind lives in
  **rule 733, "Handling Illegal Actions"**: the entire action is reversed,
  payments already made are canceled, no abilities trigger / no effects apply,
  the spell returns to the zone it came from, and the player may redo it
  legally (733.1). Actions that moved cards to a library, moved cards out of a
  library to anywhere but the stack, shuffled a library, or revealed cards from
  a library **can't be reversed** (733.1).
- **(b) Prohibition arises after proposal → also a full rewind.** If a player
  is *no longer allowed* to cast the spell after completing its proposal
  (601.2a–d), the casting is illegal and the game **returns to the moment
  before the casting was proposed** (601.5, via rule 733). The "it doesn't
  matter" clause is what makes this universal: the rewind applies regardless of
  whether the prohibiting rule/effect would make the casting illegal *while
  determining or paying costs* (601.2f–h) **or any time after the spell has
  already been cast** (601.5). The **only** thing that persists past a completed
  proposal is **conditional flash**: once a player has legally begun casting a
  spell that had (or could be cast as though it had) flash because certain
  conditions were met, they may continue casting it as though it had flash even
  if those conditions stop being met (601.5a).

The 601.2f **cost lock** is a real boundary but a different one: it isn't a
rewind boundary, it's where the total cost is fixed so that later cost-changing
effects no-op (601.2f).

## 4. Activating abilities (602)

Activating mirrors casting: put the ability on the stack and pay its costs
(602.2). Only the object's controller (or owner if none) may activate it
unless stated (602.2). The activation cost is everything before the colon
(602.1a); text after the colon may be **activation instructions** (who/when/
cost definition), which function at all times and are *not* part of the effect
(602.1b).

- **602.2a** is the analog of 601.2a: announce activation, reveal the card if
  from a hidden zone, create the ability on the stack as a non-card object
  with only the ability's text (602.2a).
- **602.2b: the rest is identical to 601.2b–i** — those casting steps apply to
  activation, with the ability's **activation cost** standing in for the
  spell's mana cost wherever 601.2f references it (602.2b). So
  modes/targets/division/legality/cost-lock/mana/payment/completion all run
  exactly as in §1.
- A player can't begin activating a prohibited ability (602.5). {T}/{Q}-cost
  creature abilities need the summoning-sickness check unless haste (602.5a);
  "Activate only as a sorcery/instant" imposes timing only (602.5d, 602.5e).
- **Loyalty abilities** are activated abilities with a loyalty symbol cost;
  their special timing (sorcery-speed, once per permanent per turn) lives in
  606.3 — see `abilities.md` §loyalty.

## 5. Triggered abilities on the stack (603.3)

A triggered ability isn't cast or activated. Once it has triggered, its
controller puts it on the stack as a non-card object the next time a player
would get priority (603.3); multiple triggers go up in APNAP order in a
two-part process (603.3b). Choices are made **then, while putting it on the
stack**: a modal trigger's mode is chosen now, and an illegal/no mode removes
it (603.3c). The remainder "is identical to the process for casting a spell
listed in rules 601.2c–d" — i.e. targets and division (603.3d). If no legal
choice can be made, the ability is simply removed from the stack (603.3d).

## 6. Resolving (608)

When all players pass in succession, the top object resolves (608.1). For an
instant/sorcery/ability, 608.2a then 608.2b run **first**, 608.2c–m run as
appropriate **in no specific order**, and 608.2n/608.2p run **last** (608.2).

- **608.2a — intervening "if".** A triggered ability with an intervening "if"
  rechecks its condition; if false it's removed and does nothing (608.2a).
- **608.2b — target legality / fizzle.** Recheck every target. A target out
  of its zone is illegal; LKI is used for a source that left its zone. **If
  *all* targets (every instance of "target") are illegal, the spell/ability
  doesn't resolve** — removed from the stack, and if a spell put into its
  owner's graveyard (608.2b). With *some* legal targets it resolves, skipping
  the parts illegal targets can't be affected by (608.2b). **Zero-target
  corollary:** 608.2b only fires "if the spell or ability specifies targets,"
  so a spell that specifies **no** targets is never subject to it — it always
  resolves; and a spell with some legal and some illegal targets still
  resolves, the illegal ones merely unaffected by the parts they're illegal for
  (608.2b).
- **608.2c — instructions in order.** Follow text in written order; later text
  may modify earlier; replacement effects may modify actions (608.2c).
- **608.2d — on-resolution choices.** Choices not already made at cast time
  are announced now; can't pick illegal/impossible options (608.2d).
  Untargeted division is chosen now (each gets ≥1); *targeted* division was
  already fixed at 601.2d (608.2d).
- **608.2e/f — multi-player/multi-object actions** in APNAP order, processed
  simultaneously where possible (608.2e, 608.2f).
- **608.2h — current vs last-known info.** Game info is read once when applied;
  an object still in its expected public zone uses current info, otherwise LKI
  (608.2h). 608.2i covers look-back-in-time effects; 608.2j: an effect checks
  only the specified characteristics (608.2i, 608.2j).
- **608.2g — casting/mana during resolution.** An effect may have the player
  cast a spell mid-resolution via 601.2a–i with **no priority after** (608.2g).
- **608.2n / 608.2p — cleanup & triggers.** An instant/sorcery goes to its
  owner's graveyard, an ability ceases to exist (608.2n); then on-resolution
  triggers fire (608.2p).
- **Permanent spells (608.3):** 608.3a/b run first, then one of 608.3c–e
  (608.3). No-target permanent spell → enters the battlefield (608.3a). A
  targeted one rechecks its target like 608.2b; an illegal target sends a
  bestow/mutate spell to resolve as a creature, otherwise the spell goes to
  the graveyard (608.3b). Aura → enters attached (608.3c); mutating creature
  merges (608.3d); a permanent spell that *can't* enter goes to the graveyard
  (608.3e). A copy of a permanent spell becomes a **token** as it enters and
  is not "created" (608.3f).

## 7. Copies of spells (707)

- **Copiable values (707.2):** the values from printed text (name, mana cost,
  color indicator, types, rules text, P/T, loyalty), as modified by other copy
  effects, face-down status, and "as … enters/turned-up" P/T-setters. Type/
  text changes, status, counters, stickers are **not** copied (707.2). Copying
  the original later won't change an existing copy (707.2b).
- **Copying a spell/ability (707.10):** to copy is to **put a copy on the
  stack — it isn't cast/activated** (707.10). The copy takes the
  characteristics **and the decisions** already made: modes, targets, X,
  additional/alternative costs (707.10). Choices normally made on resolution
  are *not* copied (707.10). "May choose new targets" lets the controller keep
  or legally change targets (707.10c). A copy of a spell is itself a spell
  (112.1a, 707.10). A copy off the stack ceases to exist as an SBA (707.10a).
  A copied permanent spell becomes a token on resolution (707.10f, 608.3f).
- **Casting a copy (707.12):** distinct from copying — an effect that says to
  **cast a copy of an object** follows the casting rules (601.2a–h then
  becomes cast), except the copy is created in the object's current zone and
  cast while another spell/ability is resolving (707.12). Such a copy is a
  spell that can resolve or be countered (112.1b, 707.12). Because this routes
  through 601.2, the caster makes fresh mode/target/X choices, unlike 707.10's
  inherited choices.

## 8. Engine note — the pipeline as states

Model one object's life as an explicit state machine driven by §1/§4:

```
proposed   ── 601.2a moved to stack (controller, characteristics set)
announced  ── 601.2b modes/splice/alt+additional/X/hybrid/Phyrexian declared
choices    ── 601.2c targets, 601.2d division locked
                (targeting triggers queued, not yet on stack)
legal?     ── 601.2e gate; fail → rewind to pre-proposal (733)
cost-locked── 601.2f total cost computed (alt/base + add'l + inc − red),
                then "locked in" — later cost effects no-op
paid       ── 601.2g mana abilities, 601.2h pay (no partials, no unpayable);
                can't-comply / can't-pay here → rewinds (601.2 intro, 733);
                a later *prohibition* rewinds too (601.5) — nothing survives a
                completed proposal except conditional flash (601.5a)
cast       ── 601.2i becomes cast; cast/put-on-stack triggers fire;
                controller may regain priority
… stack …  ── waits; pass-in-succession (608.1)
resolving  ── 608.2a "if" → 608.2b targets/fizzle → 608.2c–m effects
done       ── 608.2n to graveyard / ceases; 608.3a–g for permanents
   or countered (701.6) / fizzled (608.2b all-targets-illegal)
```

Activated abilities use the same machine via 602.2a + 602.2b→601.2b–i;
triggered abilities skip cast/pay and enter at the choices stage via 603.3.
There is **no point-of-no-return *during* casting**: every failure mode rewinds
until casting completes legally (subject to 733.1's irreversible library-action
caveat). The one boundary an engine must respect is the **cost lock** (601.2f):
after the total cost is locked in, later cost-changing effects are inert — it is
a *fixing* boundary, not a rewind boundary. Both *any* inability to comply with
a step 601.2a–i (including can't-pay at 601.2h, 601.2 intro + 733) **and** a
player becoming no longer allowed to cast after proposal completes (601.5) send
the game back to before proposal; the **only** thing that survives a completed
proposal is **conditional flash** (601.5a).
