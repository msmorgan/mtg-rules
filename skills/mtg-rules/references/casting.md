# Casting — The Spell/Ability Pipeline

*Synthesized from the Comprehensive Rules effective 2026-09-25
(`data/rules/cr.json`).*

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
must be legally allowed to begin (601.3, see §3). When a spell may be cast or
an ability activated: default windows 117.1a–b (`turn.md` §2); combat-point
windows 506.8–506.8f, which 506.8g extends to activations; activation-window
modifiers (602.5b, 602.5d–e) in §4 and `deontics.md` §3.

1. **601.2a — move to stack.** Move the card (or copy) to the stack as the
   topmost object; it gets all the card's characteristics and the player
   becomes its controller. Cast-time continuous characteristic-modifiers
   (611.2f) and one-shot ability-granting effects (610.5) begin applying here
   (601.2a, 611.2f, 610.5). Which half, face or alternative set goes on the
   stack, and is checked for castability: `state.md` §5 (Card forms).
2. **601.2b — choices: modes / splice / alt+additional costs / X / hybrid /
   Phyrexian.** Announce modal choice, reveal splice cards, declare intent to
   pay alternative and/or additional costs (buyback, kicker), announce the
   value of any {X}, and choose how hybrid/Phyrexian symbols will be paid
   (601.2b). **Only one alternative cost *and* one alternative casting method
   per spell** — 601.2b alone bars two alternative *methods of casting* or two
   alternative *costs*; 118.9a covers only the one-alternative-cost half
   (601.2b, 118.9a). A variable defined by a choice the player would make later
   in the announcement or resolution is chosen now instead; previously made
   choices (casting with flashback from a graveyard, casting a creature face
   down) may restrict the player's options here (601.2b). This step picks
   *what* the cost will be; it does not pay it.
3. **601.2c — targets.** Announce a target for each required target; some
   targets are required only if a kicker/alternative cost or a particular mode
   was chosen (601.2c). A variable number of targets is announced before the
   targets themselves (601.2c). The same target can't be chosen twice for one
   instance of the word "target," but can be chosen once per instance when the
   text says "target" in several places (601.2c). Becomes-the-target triggers
   trigger now but wait to go on the stack until casting finishes (601.2c).
   Target count, once determined, doesn't change (601.2c). When "must be
   chosen as a target" effects compete, the maximum-must-target arbitration is
   in `choices.md` §5 (601.2c).
4. **601.2d — division.** If the spell divides/distributes (damage, counters)
   among targets, announce the division; each target gets at least one
   (601.2d).
5. **601.2e — legality check.** The game checks the proposed spell is legal
   to cast; if illegal, rewind to before proposal (601.2e, rule 733). This is
   the legality gate at the *end of proposal* (601.6); for the rewind
   semantics after it (can't-comply, can't-pay) see §3.
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
   put-on-stack triggers trigger now (601.2i). The becomes-the-target triggers
   that already triggered at 601.2c are still waiting and go on the stack with
   them the next time a player would receive priority (601.2c, 603.3). The
   controller, if they had priority, gets priority back (601.2i).

601.4 lets a player make a normally-later choice early when an earlier choice
depends on it (e.g. announcing extra modes that only a later kicker payment
unlocks) (601.4). 601.5 is the same idea for the target and division
announcements (601.2c–d): when some options are available only if other
choices are made later, the controller may consider those later choices,
including which objects will be used to pay costs (601.5). 601.8: casting a
cost-altering spell doesn't touch spells/abilities already on the stack
(601.8). Choices another player makes for the spell go through `choices.md` §1
(601.7–601.7b; 602.3–602.3b is the activation analog).

**Modes beyond the pick (700.2).** A mode can't be chosen twice unless the
text says "You may choose the same mode more than once". A repeated mode then
counts as that mode written that many times in sequence, and each repetition
may take the same or a different target (700.2d). A cost printed before a mode
is an additional cost, owed at 601.2f–h if that mode is chosen (700.2h). Spree
and tiered are built this way (702.172a, 702.183a), so a spree spell cast
"without paying its mana cost" still owes its chosen modes' costs (Final
Showdown `[2024-04-12]`). Changing a spell's targets can't change its mode
(700.2f). A copy keeps the original's modes (700.2g, §7). Another player told
to choose the mode does so when the controller normally would; with several
eligible players, the controller picks one (700.2e; for opponents 601.7).

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
  Oracle usually overrides the 118.7b/c spill to generic for colored
  reductions. It does so with a rider: `This effect reduces only the amount of
  colored mana you pay.` (Edgewalker: `Cleric spells you cast cost {W}{B} less
  to cast. This effect reduces only the amount of colored mana you pay.`), or
  with a single-color version (`… This effect reduces only the amount of blue
  mana you pay.`, Defiler of Dreams). 9 of the 10 supported lines with a
  colored `cost {…} less to cast` amount carry the rider. The tenth restates
  the default in reminder text (`Spells you cast cost {W}{U}{B}{R}{G} less to
  cast. (This can reduce generic costs.)`, Avatar Aang). *Engine inference:* a
  cost reduction needs a colored-only flag alongside the 118.7 default
  (118.7a, 118.7b, 118.7c).
- **"Cost can't be paid" vs "can't cast":** beginning to cast is gated by
  601.3 / 601.2e (legality). Failing to *pay* at 601.2h is a separate failure,
  but it is **not** exempted from rewind: being unable to comply with 601.2h
  makes the cast illegal and the game returns to before proposal (601.2 intro,
  733.1). A rule or effect that would make the casting illegal only while
  costs are determined or paid does not matter (601.6, §3). Paying a
  reduced/changed cost still counts as paying the original (118.7, 118.11).
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

After 601.2e, only the can't-comply / can't-pay case (a) rewinds; (b) is the
proposal-time legality rule plus its "doesn't matter" clause:

- **(a) Can't comply / can't pay → full rewind.** If a player is *unable to
  comply* with the requirements of any step 601.2a–i — including determining
  the cost (601.2f) or *paying* it (601.2h) — the cast is illegal and the game
  **returns to the moment before proposal** (601.2 intro). The rewind lives in
  **rule 733, "Handling Illegal Actions"**: the entire action is reversed,
  payments already made are canceled, no abilities trigger / no effects apply,
  and the spell returns to the zone it came from (733.1). Each player may also
  reverse legal mana abilities they activated during the attempt, unless mana
  from those abilities, or from triggered mana abilities they caused to
  trigger, was spent on another mana ability that wasn't reversed (733.1). The
  player who had priority retains it and may take another action or pass; the
  player may redo the reversed action in a legal way (733.2). Actions that
  moved cards to a library, moved cards out of a library to anywhere but the
  stack, shuffled a library, or revealed cards from a library **can't be
  reversed** (733.1).
- **(b) Legality is settled when proposal completes.** 601.6: legality is
  settled when proposal completes (601.2e). If the completed proposal is not
  allowed (e.g. a 601.3a/601.3b exemption whose proposal choices did not
  remove the prohibition or bring the spell under the flash grant), the
  casting is illegal and rewinds (601.6, 733). A prohibition that arises
  during proposal itself (e.g. an X choice that makes the spell match Void
  Winnower) still rewinds (601.6, 601.2e). A rule or effect that would make
  casting illegal only while costs are determined or paid (601.2f–h), or after
  the spell is cast, does not matter (601.6). For example, sacrificing
  Herigast to pay the emerge cost it granted does not stop the cast (Herigast
  ruling 2024-06-07; Lurrus ruling 2020-04-17). 601.6a is a separate, wider
  carve-out for conditional flash: once a player has begun casting a spell
  that had flash because conditions were met (601.3d), they may keep casting
  it as though it had flash even if those conditions stop being met at any
  later point, including during proposal (601.6a).

The 601.2f **cost lock** is a real boundary but a different one: it isn't a
rewind boundary, it's where the total cost is fixed so that later cost-changing
effects no-op (601.2f).

## 4. Activating abilities (602)

Activating mirrors casting: put the ability on the stack and pay its costs
(602.2). Only the object's controller (or owner if none) may activate it
unless stated (602.2). Announcements and payments can't be altered after
they've been made (602.2). The activation cost is everything before the colon
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
  Activation-limit persistence and the per-acquired-ability scope of a limit
  are in `temporal.md` §4 (602.5b–c).
- **Loyalty abilities** are activated abilities with a loyalty symbol cost;
  their special timing (sorcery-speed, once per permanent per turn) lives in
  606.3 — see `abilities.md` §2 (Loyalty abilities).

## 5. Triggered abilities on the stack (603.3)

A triggered ability isn't cast or activated. Once it has triggered, its
controller puts it on the stack as a non-card object the next time a player
would get priority (603.3); multiple triggers go up in APNAP order in a
two-part process (603.3b). Choices are made **then, while putting it on the
stack**: a modal trigger's mode is chosen now, and an illegal/no mode removes
it (603.3c). The remainder "is identical to the process for casting a spell
listed in rules 601.2c–d" — i.e. targets and division (603.3d). If no legal
choice can be made for it, or if a rule or a continuous effect otherwise makes
the ability illegal, the ability is simply removed from the stack (603.3d).

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
  **Illegal targets yield no information.** When the spell or ability does
  resolve, rule-changing continuous effects it creates (613.11) don't apply to
  its illegal targets, and a part of the effect that needs information about
  an illegal target "fails to determine any such information" and doesn't
  happen (608.2b). No last known information substitutes for an illegal
  target. 608.2h's LKI fallback serves only the source, untargeted objects,
  and targets that were legal at the 608.2b check but left their zone during
  resolution (608.2h). For example, Swords to Plowshares uses the exiled
  creature's power "from when it was last on the battlefield" (Swords to
  Plowshares `[2022-12-08]`). Bite Down's creature deals no damage if either
  target is illegal (Bite Down `[2022-09-09]`). A Heartfire Immolator
  sacrificed to pay for its ability deals damage equal to its last-known power
  (Heartfire Immolator `[2020-06-23]`). Fight, exchange and moving a counter
  are stricter still: `events.md` §4.
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
  (608.2h), but an illegal target yields no information at all (608.2b,
  above). 608.2i covers look-back-in-time effects; 608.2j: an effect checks
  only the specified characteristics (608.2i, 608.2j).
- **608.2g — casting/mana during resolution.** An effect may have the player
  cast a spell mid-resolution via 601.2a–i with **no priority after** (608.2g).
- **608.2k — untargeted objects named by a cost or trigger.** If an ability's
  effect refers to a specific untargeted object that the ability's cost or
  trigger condition previously referred to, it still affects that object even
  if the object has changed characteristics (608.2k).
- **608.2n / 608.2p — cleanup & triggers.** An instant/sorcery goes to its
  owner's graveyard, an ability ceases to exist (608.2n); then on-resolution
  triggers fire (608.2p).
- **Stack exits and the windows that watch them.** An instant or sorcery spell
  reaches its owner's graveyard by three rule routes: the last step of
  resolving (608.2n), being countered (701.6a), and not resolving because
  every target is illegal (608.2b). An effect can also move a spell without
  countering it (Mindbreak Trap exiles target spells; Commit puts one into its
  owner's library), and a spell that leaves the stack after it starts
  resolving still resolves fully (608.2m). Replacement and trigger text
  watches one of three windows over these exits:

  | Window (wording) | Matches | CR instances |
  |---|---|---|
  | Resolution only — "as it resolves", "during its resolution" | the 608.2n move alone; not a counter, a fizzle, or an effect move | buyback (702.27a), rebound (702.88a), Adventure (715.3d), Omen (720.3d); haunt on an instant or sorcery triggers on this window (702.55a) |
  | Graveyard-bound — "If that spell would be put into [a/your] graveyard" | the 608.2n, counter, and fizzle moves; not a move to another zone | none (card text only) |
  | Any departure — "any time it would leave the stack" | every exit, including a counter that sends the spell to hand | flashback (702.34a), aftermath (702.127a), jump-start (702.133a), harmonize (702.180a) |

  The last column lists every CR rule that uses the wording for a stack exit.
  Card text adds members to all three rows, so match on the window, not on a
  keyword list. Rulings, row by row: a countered or fizzled rebound spell "is
  simply put into your graveyard" (Staggershock `[2010-06-15]`), and an
  Adventure that leaves the stack "in any way other than resolving" isn't
  exiled (Bonecrusher Giant `[2019-10-04]`). A spell cast with Goblin
  Dark-Dwellers that "is countered … will be exiled", but one that goes "to a
  zone other than exile or a graveyard" won't be (Goblin Dark-Dwellers
  `[2016-01-22]`). A flashback spell "will always be exiled afterward, whether
  it resolves, is countered, or leaves the stack in some other way" (Think
  Twice `[2024-11-08]`), including when Remand counters it (Remand
  `[2021-03-19]`).

  **Engine inference:** no single "spell → graveyard" event can drive all
  three rows, so each stack exit needs its route as a cause tag: resolution
  step (608.2n), fizzle (608.2b), counter (701.6a), or effect move
  (`events.md` §3).
- **Permanent spells (608.3):** 608.3a/b run first, then one of 608.3c–e
  (608.3). No-target permanent spell → enters the battlefield (608.3a). A
  targeted one rechecks its target like 608.2b; an illegal target sends a
  bestow/mutate spell to resolve as a creature, otherwise the spell goes to
  the graveyard (608.3b). Aura → enters attached (608.3c); mutating creature
  merges (608.3d); a permanent spell that *can't* enter goes to the graveyard
  (608.3e). An Aura that enters without being cast: `state.md` §6
  (Attachments). A copy of a permanent spell becomes a **token** as it enters and
  is not "created" (608.3f).
- **608.3g — stack-functioning static ability that creates a delayed trigger.**
  If the resolving object has a static ability that functions on the stack and
  creates a delayed triggered ability (dash, blitz, warp), that delayed
  trigger is created as the permanent is put onto the battlefield in any of
  the steps above (608.3g, 702.109, 702.152, 702.185).

## 7. Copies of spells (707)

- **Copiable values (707.2):** the values from printed text (name, mana cost,
  color indicator, types, rules text, P/T, loyalty), as modified by other copy
  effects, face-down status, and "as … enters/turned-up" P/T-setters. Type/
  text changes, status, counters, stickers are **not** copied (707.2). Copying
  the original later won't change an existing copy (707.2b). Exceptions to the
  copying process: `effects.md` §4 (707.9).
- **Copying a spell/ability (707.10):** to copy is to **put a copy on the
  stack — it isn't cast/activated** (707.10). The copy takes the
  characteristics **and the decisions** already made: modes, targets, X,
  additional/alternative costs (707.10). Choices normally made on resolution
  are *not* copied (707.10). An effect of the copy that refers to objects used
  to pay its costs uses the objects used to pay the original's costs (707.10;
  its example is Fling). A copy of a spell is owned by the player under whose
  control it was put on the stack, and a copy of a spell or ability is
  controlled by that player (707.10). A copy of an ability has the same source
  as the original ability (707.10b). "May choose new targets" lets the
  controller leave any number of targets unchanged, even if those targets
  would be illegal, or change some or all of them to new legal targets
  (707.10c). Two variants set the copy's targets instead of inheriting them. A
  copy made "for each player or object it could target" aims every instance of
  "target" at that one player or object. It isn't made for a player or object
  that isn't legal for every instance, and the copies go on the stack in the
  order their controller chooses (707.10d). An effect that names the copy's
  new target likewise aims every instance at it and creates no copy if it
  isn't legal for each instance. If a replacement effect makes that target
  several objects, the copy's controller picks one legal one (707.10e; its
  example is Frontline Heroism with Anointed Procession). A copy of a spell is
  itself a spell (112.1a, 707.10). A copy off the stack ceases to exist as an
  SBA (707.10a). A copied permanent spell becomes a token on resolution
  (707.10f, 608.3f). A copy of a double-faced permanent spell is double-faced
  too. Each face takes the copiable values of the same face of the original,
  it starts with the original's face up, and it resolves into a double-faced
  token (707.10g). Redirects and copies as becomes-target events: `events.md`
  §2 (Becomes-target).
- **Casting a copy (707.12):** distinct from copying — an effect that says to
  **cast a copy of an object** follows the casting rules (601.2a–h then
  becomes cast), except the copy is created in the object's current zone and
  cast while another spell/ability is resolving (707.12). Such a copy is a
  spell that can resolve or be countered (112.1b, 707.12). Because this routes
  through 601.2b–c, the caster makes fresh mode and target choices, unlike
  707.10's inherited ones (inference from 707.12 + 601.2b–c). X is announced
  fresh too, but when the copy is cast without paying its mana cost, X must be
  0 (107.3b; Mizzix's Mastery ruling 2015-11-04). An effect that creates
  several copies and says a player "may cast" them lets that player choose
  individually, for each copy, whether to cast it (707.12a). The owner of a
  copy created and cast this way is the player instructed to create it and
  given permission to cast it (112.2a).

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
                a prohibition that would apply while costs are determined or
                paid does not matter (601.6)
cast       ── 601.2i becomes cast; cast/put-on-stack triggers fire;
                controller may regain priority
… stack …  ── waits; pass-in-succession (608.1)
resolving  ── 608.2a "if" → 608.2b targets/fizzle → 608.2c–m effects
done       ── 608.2n to graveyard / ceases; 608.3a–g for permanents
triggers   ── 608.2p on-resolution triggers fire
   or countered (701.6) / fizzled (608.2b all-targets-illegal)
   or removed (608.2a / 603.3c–d)
```

Activated abilities use the same machine via 602.2a + 602.2b→601.2b–i;
triggered abilities skip cast/pay and enter at the choices stage via 603.3.
Four boundaries an engine must respect: legality is fixed at the end of
proposal (601.2e, 601.6); conditional flash is fixed when casting begins
(601.6a); the total cost is fixed at the 601.2f lock — a *fixing* boundary,
not a rewind boundary, after which later cost-changing effects are inert
(601.2f); and after 601.2e only can't-comply / can't-pay failures (including
can't-pay at 601.2h) rewind the cast (601.2 intro, 733), subject to 733.1's
irreversible library-action caveat.
