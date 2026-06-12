# Rulings Check — The Model vs Official Rulings

*Synthesized from the Comprehensive Rules effective 2026-04-17
(`data/rules/cr.json`). Orientation only — verify load-bearing specifics
with `scripts/rule` before citing. Run `scripts/cite check` after CR
refreshes.*

This doc validates the skill's model against WotC's own answer key. For
eighteen subsystem probes it states our **independent** derivation (from the
sibling reference docs + `scripts/rule`), then quotes the official ruling
(`scripts/rulings`, date-stamped `[YYYY-MM-DD]`) and records a verdict.
Probes 1–10 validate the original synthesis layer; 11–18 the newer docs
(costs, events, choices, information, outcomes, mana, temporal, queries).

**Renumber-drift warning:** official ruling texts embed CR numbers from their
publication date; the CR renumbers over time. Every CR number below was
re-resolved against the *current* cr.json — never repeat a ruling's cited
number without re-checking it with `scripts/rule`. A verdict of `RULING STALE`
means the ruling predates a CR change; in that case we cite the current rule,
not "fix" a doc to match the stale text.

**How to use this doc:** when answering a rules question, imitate these
derivation patterns — orient with the named reference doc, then quote the
specific dotted CR rule that does the work, then sanity-check against the
card's official rulings. Ruling first, citations second.

All eighteen probes verdict **MATCH** on the current CR; no sibling-doc fixes
were required. Re-run them (see Maintenance) after each CR refresh.

## 1. Humility + Opalescence — layers/timestamps

**Q:** Two static base-P/T setters in the same sublayer — what are creatures'
final P/T, and who controls it? **Frame:** `effects.md` §10 (worked stack) +
§4 (layers).

- Both set base P/T, which lands in **layer 7b** (613.4b "base P/T" setters);
  Opalescence's type change is **L4**, Humility's ability-strip is **L6**.
- 613.6 is the crux: an effect keeps applying to its locked object set in
  every later layer **even after L6 strips the source's own ability**, so both
  7b sets survive.
- Within 7b, earlier timestamp applies first (613.7); the **last** 7b set to
  apply wins. So Humility-later → **1/1**; Opalescence-later → **4/4**.

Official `[2009-10-01]`: "Layer 7b: Humility becomes 4/4 and Worship becomes
4/4. (Opalescence). Humility becomes 1/1 and Worship becomes 1/1 (Humility).
But if Humility entered before Opalescence … Humility becomes 1/1 … Humility
becomes 4/4 … (Opalescence)." **MATCH.**

## 2. Blood Moon + Urborg — dependency

**Q:** Do timestamps decide, or does one effect override? **Frame:**
`effects.md` §10 (worked stack) + §4 dependency (613.8).

- Both are L4 type-changers, neither a CDA — 613.8a(a) same sublayer and (c)
  CDA-parity hold; dependency turns on (b).
- Blood Moon sets nonbasics to Mountain *not in addition*, which by **305.7**
  strips abilities from the land's rules text. Applied to Urborg (a nonbasic),
  it deletes Urborg's "each land is a Swamp" ability → changes the
  **existence** of Urborg's effect: **Urborg depends on Blood Moon** (613.8a).
- The reverse fails — Urborg only *adds* Swamp, changing nothing about Blood
  Moon. One-directional dependency, so timestamps are irrelevant (613.8):
  Blood Moon applies first; Urborg then contributes nothing (613.8c).

Official `[2021-03-19]` (Urborg): "If an effect such as that of Magus of the
Moon causes Urborg to lose its abilities by setting it to a basic land type
not in addition to its other types, it won't turn lands into Swamps, no matter
in what order those effects started to apply." **MATCH.**

## 3. Clone — copy characteristics

**Q:** What does Clone copy when it enters as a copy of a modified creature?
**Frame:** `effects.md` §4 (L1 copiable values) + 707.2.

- A copy acquires the original's **copiable values** = values from printed text
  (name, mana cost, color indicator, types, rules text, P/T, loyalty), as
  modified by other copy effects / face-down / "as ~ enters" P/T-setters
  (707.2).
- **Not copied:** other continuous effects (type/text/P/T changes), status,
  counters, stickers (707.2). So a Clone of an animated Chimeric Staff copies
  the *artifact*, not the 5/5 Construct (707.2 example).
- ETB and "as ~ enters"/"enters with" abilities of the chosen creature do
  apply to Clone, since they are part of the copied rules text (707.2a, 614.1c
  for the "enters with" replacement).

Official `[2025-10-02]`: "Clone copies exactly what was printed on the original
creature and nothing else … It doesn't copy whether that creature is tapped …
has any counters … or any non-copy effects that have changed its power,
toughness, types, color, or so on." **MATCH.**

## 4. Yixlid Jailer — where abilities function

**Q:** Which graveyard abilities does "cards in graveyards lose all abilities"
shut off? **Frame:** `abilities.md` §"where abilities function" (113.6).

- Default: a card's abilities don't function in the graveyard at all (113.6) —
  so Yixlid only matters for abilities that *would* function there. CDAs are
  the headline exception: they function everywhere (113.6a), so Tarmogoyf's
  `*` P/T defines normally — but Yixlid is in layer 6 ability-removal, so it
  strips even the CDA → `*` becomes 0 (the CDA is gone; 613.4a / undefined `*`
  = 0).
- Abilities that trigger from the graveyard "from anywhere" (113.6k allows the
  trigger to function there) are removed → they don't trigger (603.2g: no
  ability, nothing triggers).
- Abilities that trigger on leaving the *battlefield* trigger from the
  battlefield (113.6c / 603.6c) — they are gone by the time the card is in the
  graveyard, so Yixlid doesn't touch them.

Official `[2021-03-19]`: "If a card in a graveyard has an ability that defines
a * in its power or toughness, that * is 0 … If an ability triggers when the
object that has it is put into a graveyard from anywhere other than the
battlefield … Yixlid Jailer stops those abilities … If an ability triggers
when the object … is put into a graveyard from the battlefield, that ability
triggers from the battlefield and isn't affected." **MATCH.**

## 5. Panharmonicon + Torpor Orb — trigger-count, not replacement

**Q:** Are these replacement effects? **Frame:** `actions.md` (trigger
determination) — verified the CR/rulings use the **603.2** trigger framework,
NOT replacement effects (614).

- Panharmonicon ("that ability triggers an additional time") is governed by
  **603.2d**: an effect may state a triggered ability triggers additional
  times; you determine how many times it triggers, then it triggers that many
  times. It does **not** invoke itself, and stacks additively across copies
  (603.2d).
- Torpor Orb ("creatures entering don't cause abilities to trigger") removes
  the match: with no trigger event, nothing triggers (603.2 / 603.2g). Look at
  the permanent as it exists on the battlefield to decide whether a trigger
  condition is met (603.6b).
- Both are **outside** 614: replacement effects use "instead"/"skip"/ETB
  wording (614.1a–e); a trigger *count* modifier and a trigger *suppressor*
  are neither. Hence ETB replacement effects (e.g. "enters with a counter")
  are untouched by either card.

Official Panharmonicon `[2021-03-19]`: "Replacement effects are unaffected by
Panharmonicon's ability." Official Torpor Orb `[2024-04-12]`: "Replacement
effects are unaffected by Torpor Orb's ability." **MATCH** — neither is a
replacement effect; the framework is 603.2.

## 6. Doubling Season — counter/token replacement; loyalty nuance

**Q:** Does it double a planeswalker's entering loyalty? A loyalty ability's
counters? **Frame:** `effects.md` §6 (614.16 doublers).

- Doubling Season is a **614.16** replacement: it applies when an effect would
  create tokens or put counters on a permanent you control.
- A planeswalker "enters with N loyalty counters" via the **614.1c**
  replacement created by its intrinsic ability (306.5b). That is an *effect*
  putting counters on entry, so Doubling Season replaces it → enters with 2N
  (614.16). Same for battle defense counters (310.4b).
- A loyalty *ability* puts/removes counters as a **cost** (606.2 — the loyalty
  symbol is *in the cost*), not as an effect — 614.16 keys doublers on effects,
  so activation costs are **not** doubled.

Official `[2024-11-08]`: "Planeswalkers will enter with double the normal
number of loyalty counters. However, if you activate an ability whose cost has
you put loyalty counters on a planeswalker, the number you put on isn't
doubled. This is because those counters are put on as a cost, not as an
effect." **MATCH.**

## 7. Teferi's Protection — phasing + "life total can't change"

**Q:** What does phasing-out + a frozen life total actually do? **Frame:**
`actions.md` / keyword 702.26 (phasing) + 609.3 (do-as-much-as-possible).

- Phasing out (702.26b): a phased-out permanent is treated as though it
  doesn't exist — can't be targeted, statics off, can't be attacked/blocked;
  it does **not** change zones, so no LTB/ETB triggers fire (702.26d).
- Counters/attachments ride along: counters stay (702.26d); attached
  Auras/Equipment phase out indirectly and phase back attached (702.26g,i).
- "Life total can't change": a damage/life event still resolves but its
  life-changing part does nothing (609.3 — does as much as possible);
  damage-dealt side effects (lifelink, infect, triggers) still see the damage,
  but no life is lost.

Official `[2017-08-25]`: "Spells and abilities that would normally cause you to
gain or lose life still resolve while your life total can't change, but the
life-gain or life-loss part simply has no effect." And: damage that can't be
prevented "has any other effects … (such as effects from lifelink or infect)
and triggers and effects can see that damage was dealt even though your life
total didn't change." **MATCH.**

## 8. Valki // Tibalt — MDFC characteristics off-battlefield

**Q:** In the hand/library/graveyard, is Valki // Tibalt a {1}{B} 2/1 creature
or a 7-mana planeswalker? **Frame:** 712 (modal double-faced cards),
712.8a.

- Each face of an MDFC has its own characteristics (712.8). In any zone other
  than the battlefield or stack (and outside the game), it has **only the
  front face's** characteristics (712.8a) — so in hand/library/graveyard it is
  Valki: {1}{B}, mana value 1, Legendary Creature.
- On the stack/battlefield, it has the characteristics of whichever face is up
  (712.8d, 712.11–712.13). An MDFC can't be transformed (712.9, ruling
  below).
- This differs from a transforming (nonmodal) DFC, whose mana value off the
  battlefield still uses the front face but which *can* be cast/enter
  transformed (712.8c).

Official `[2021-02-05]`: "The mana value of a modal double-faced card is based
on the characteristics of the face that's being considered. On the stack and
battlefield, consider whichever face is up. In all other zones, consider only
the front face." And: "A modal double-faced card can't be transformed or be
put onto the battlefield transformed." **MATCH.**

## 9. Mirror Room // Fractured Realm — Rooms / door unlock

**Q:** How do a Room's doors and unlock work, and does Fractured Realm double
"when you unlock this door" triggers from casting? **Frame:**
`designations.md` §"Left half / right half unlocked" (709.5) + actions §603.2d.

- A Room is one card (709.5b) with two doors (halves; 709.5j). While a half
  lacks its unlocked designation, the permanent lacks that half's name, mana
  cost, and rules text (709.5); its on-battlefield characteristics combine its
  unlocked doors.
- Casting a door unlocks it as the Room enters (709.5d); you may also pay a
  locked door's mana cost as a **special action** with priority on an empty
  stack in your main phase (709.5e). "When you unlock this door" triggers
  whether unlocked on entry or later (709.5h).
- Fractured Realm ("a triggered ability … triggers an additional time") is a
  **603.2d** count modifier (same framework as Panharmonicon, probe 5) — but
  an unlock-on-entry trigger is caused by the *door becoming unlocked as the
  Room enters*, and 603.2d effects keyed to "enters" don't apply to it.

Official `[2024-09-20]`: "An ability that triggers 'when you unlock this door'
triggers when that door becomes unlocked. This can happen … (2) the door
becomes unlocked as the Room enters the battlefield because you cast the
corresponding half. In the latter case … effects that cause abilities that
trigger when a permanent enters to trigger an additional time (such as that of
Panharmonicon) won't apply." And special action: "you may pay the mana cost of
a locked door … That door becomes unlocked. This is a special action."
**MATCH.**

## 10. Invasion of Alara — battles / Sieges

**Q:** How does a Siege enter, get attacked, and flip? **Frame:** 310
(battles) + 310.11 (Sieges).

- A battle enters with defense counters equal to its printed defense via a
  **614.1c** replacement from its intrinsic ability (310.4b); Invasion of
  Alara enters with 7.
- As a Siege enters, its controller chooses an **opponent** as protector
  (310.11a, 310.8a); the protector can never attack it, and a Siege's own
  controller *can* attack it (310.8b). Only the protector's creatures may
  block attackers of that battle (310.8c).
- Damage removes that many defense counters (310.6); a Siege has the intrinsic
  trigger "when the last defense counter is removed … exile it, then you may
  cast it transformed without paying its mana cost" (310.11b). At 0 defense
  (and not the source of a pending trigger) the battle is put into the
  graveyard as an SBA (310.7).

Official `[2023-04-14]`: "Sieges each have an intrinsic triggered ability. That
ability is 'When the last defense counter is removed from this permanent,
exile it, then you may cast it transformed without paying its mana cost.'" And:
"A battle can be attacked by all players other than its protector. Notably,
this means a Siege's controller can attack it." And: "As a Siege enters the
battlefield, its controller chooses an opponent to be its protector."
**MATCH.**

## 11. Trinisphere — total-cost pipeline and the 601.2f lock

**Q:** When does "costs three mana to cast" apply, and what if Trinisphere
taps as part of payment? **Frame:** `costs.md` §4 (modification pipeline).

- The pipeline: base (mana or alternative, 601.2b) → + additional costs and
  increases → − reductions → floor {0} → **effects that directly affect the
  total** → locked (601.2f). Trinisphere is the direct-total stage — applied
  after every increase and reduction, last before the lock.
- After 601.2f nothing changes the total; the 601.2h example is on point — a
  cost-reducer sacrificed *as part of payment* doesn't re-raise the price, so
  Trinisphere tapping or leaving inside the 601.2g–h payment window changes
  nothing either. (Mana value never moves regardless: 202.3.)

Official `[2020-08-07]`: "… start with the mana cost or alternative cost
you're paying, add any cost increases, then apply any cost reductions.
Finally, apply Trinisphere's effect … The mana value of the spell remains
unchanged …" And:
"If Trinisphere leaves the battlefield or becomes tapped or untapped as a cost
to cast a spell, this cost is paid after you've locked in the total cost."
**MATCH.**

## 12. Guerrilla Tactics — discard cause: the agent coordinate

**Q:** Which discards match "a spell or ability an opponent controls causes
you to discard this card"? **Frame:** `events.md` §3 (cause tags).

- The trigger is a predicate over the discard event's **cause triple**: verb
  = discard (701.9a), agent kind = spell-or-ability, agent controller = an
  opponent (`events.md` names this exact oracle family).
- Discarding **as a cost** carries agency = cost-payment (601.2h), not
  effect-instruction — no spell or ability is the causing agent — so
  cost-discards never match. **Optionality is not a coordinate**: an
  opponent's resolving spell that merely *lets* you discard still has that
  spell as agent → trigger fires; who picks the card (default: the affected
  player, 701.9b) doesn't matter either.

Official `[2004-10-04]`: "Discarding as a cost to cast a spell will not
trigger the ability. Only discarding as an effect will trigger the ability."
And: "The second ability will trigger even on an optional discard caused by
an opponent." **MATCH.**

## 13. Krark's Thumb — replacement per flip, revisable RNG

**Q:** How does it apply to multi-coin effects, and when is the ignore choice
made? **Frame:** `choices.md` §4 (randomness as pseudo-decider).

- The Thumb replaces the **flip event**, and its own text defines the event
  it watches (700.1): "flip two coins" is two would-flip-a-coin events, each
  replaced separately into flip-two-ignore-one — one opportunity per event,
  no re-invoking on its own replacement flips (614.5), so pairs stay pairs.
- `choices.md`: the RNG is a pseudo-decider whose **output is revisable after
  the fact** (the 705.3 override family); "ignore one" is a **follow-up
  decision fed by the RNG events** (the 706.2b shape) — made after the flips,
  whose results are public, so all simultaneous flips are visible first.

Official `[2019-01-25]`: "… you flip two coins, flip two coins, and then
ignore one flip from each pair of flips. You will know the results of all
simultaneous flips before choosing which to ignore." And `[2004-10-04]`: "If
you and your opponent both flip at the same time, you can see your opponent's
result before choosing which result to keep." **MATCH.**

## 14. Ixidron — face-down identity, look rights, copiable blanks

**Q:** What are the creatures Ixidron turns face down, who may look at them,
and what does a copy of one copy? **Frame:** `information.md` §2 (face-down).

- Ixidron's effect lists no characteristics, so the 708.2a default applies:
  a 2/2 face-down creature with no text, name, subtypes, or mana cost — and
  those defaults are the **copiable values** (708.2a): a copy of one copies
  the blank 2/2, not the hidden card (707.2, "as modified by … face-down
  status").
- Look rights: a controller may look at their own face-down permanents at
  any time — morph not required (708.5); other players never may. The
  **differentiation duty** (708.6) still applies: every face-down object
  must stay distinguishable.

Official `[2006-09-25]`: "The controller of a face-down creature can look at
it at any time, even if it doesn't have morph. Other players can't, but …
'you must ensure at all times that your face-down spells and permanents can
be easily differentiated from each other.'" And `[2018-04-27]`: "Creatures
turned face down by Ixidron are 2/2 creatures with no text, no name, no
subtypes … These values are copiable … and their normal values are not
copiable." **MATCH.**

## 15. Abyssal Persecutor — can't-lose: standing vs windowed SBAs

**Q:** What still ends an opponent's game while it's out, and what happens
the instant it leaves? **Frame:** `outcomes.md` §2 (outcome modification).

- No CR rule defines can't-win/can't-lose base semantics; the home is 101.1 —
  the card text contradicts 104.2b/104.3e and the loss SBAs and takes
  precedence, gating **each application** while consuming nothing.
- The SBA split: 704.5a and 704.5c are **standing state predicates** ("has 0
  or less life") — still true at the first check after Persecutor leaves, and
  SBAs run before any player gets priority (704.3): the opponent at −5 loses
  with no response window. 704.5b is a **windowed event predicate**
  ("attempted to draw … since the last check"); a suppressed empty-library
  draw lapses with its window.
- Pierces and edges: concession is the single exception to card-beats-rules
  (101.1, 104.3a); judge penalties bypass it too (104.3k); draws are neither
  wins nor losses (104.4c); life still drops below 0 — the gate is on the
  outcome, not the life change — but life *payments* stay capped (119.4).

Official `[2017-11-17]`: "If Abyssal Persecutor leaves the battlefield while
an opponent has 0 or less life, that opponent will lose the game as a
state-based action. No player can respond …" And: "An opponent will lose a
game if they concede, if that player is penalized …" And: "Effects that say
the game is a draw … are not affected by Abyssal Persecutor." **MATCH.**

## 16. Exotic Orchard — 106.7 could-produce

**Q:** Which colors can it tap for? **Frame:** `mana.md` §3 (producing the
hypothetical).

- "Could produce" = whatever an opponent's land's abilities **would produce
  if they resolved now**, replacement effects considered in any possible
  order, **ignoring costs entirely** (106.7) — tapped status, missing charge
  counters, any activation cost: invisible. Riders never matter either: they
  don't touch the **type** (106.6), and 106.7 asks only after types.
- "Any color" ranges over the five colors (105.1); colorless is a sixth
  *type*, not a color (106.1b, `mana.md` §1) — the Orchard can never make {C}.
- Fixpoint: if the only feeders are themselves could-produce lands, no type
  is definable and no mana is produced (106.7's no-type clause; its example
  is an Exotic Orchard chain); one real Forest anywhere in the web gives
  every chained land {G}.

Official `[2009-02-01]`: "It doesn't matter whether Vivid Crag has a charge
counter on it, and it doesn't matter whether it's untapped." And: "Exotic
Orchard can't be tapped for colorless mana, even if a land an opponent
controls could produce colorless mana." And: "… if you control a Forest and
an Exotic Orchard, and your opponent controls an Exotic Orchard and a
Reflecting Pool, then each of those lands can be tapped to produce {G}."
**MATCH.**

## 17. Phyrexian Fleshgorger — ward amount fixed at resolution

**Q:** Ward—Pay life equal to its power: when is the amount determined?
**Frame:** `temporal.md` §3 lock row 4 (X) + `queries.md` §4 (the X trio).

- Ward is a triggered ability demanding a **resolution toll** — "counter that
  spell or ability unless that player pays [cost]" (702.21a; `costs.md`'s
  resolution-toll position) — and the variable amount is **not locked as the
  ability triggers**: ward X is determined as the demanding ability resolves
  (702.21b). "Equal to this creature's power" is the same shape read through
  608.2h (information determined once, when applied): the power is read at
  ward-resolution time.
- Source gone before the ward resolves → **last known information** supplies
  the power (608.2h, 113.7a); if Fleshgorger was also the spell's only
  target, the spell won't resolve no matter what is paid (608.2b).

Official `[2022-10-14]`: "The amount of life an opponent needs to pay … is
equal to Phyrexian Fleshgorger's power at the time the ward ability resolves,
which may be different from its power when the ward ability triggered. If
Phyrexian Fleshgorger is no longer on the battlefield … use the power it had
the last time it was on the battlefield … (though if Phyrexian Fleshgorger
was the only target, the spell … would not resolve even if they pay the
life)." **MATCH.**

## 18. Cone of Flame — "another"/"a third": final-set distinctness

**Q:** 1, 2, and 3 damage to three targets — must they differ, and can the
amounts move if a target goes illegal? **Frame:** `queries.md` §2
("another"/"other"). *(Substitute for the ruling-less Arc Trail.)*

- Three separate instances of "target": 115.3 alone would *allow* re-picking
  the same object across instances; the distinctness comes from "another"/"a
  third" — `queries.md`'s verified finding: templating-level English compiling
  to a **set-distinctness constraint on the final target set** (115.7e — its
  CR example is Arc Trail). At announcement the final set is the announced
  set: three distinct legal targets per 601.2c or the proposal rewinds
  (601.2e).
- The amounts are bound per target instance by the spell's own text — nothing
  is "divided," so nothing can reflow. A target illegal at resolution is
  simply unaffected; the parts aimed at the others apply unchanged (608.2b) —
  the no-redistribution behavior of `temporal.md`'s division lock row.

Official `[2014-07-18]`: "Each of the three targets must be different. If
there aren't three different legal targets available, you can't cast the
spell." And: "If one or two of Cone of Flame's targets are illegal when it
resolves, you can't change how much damage will be dealt to the remaining
legal targets." **MATCH.**

## Maintenance

Re-run every probe after any CR refresh — renumbering may move the cited rules
even when the rulings are unchanged. For each probe: `scripts/rulings <card>`
and `scripts/card <card>` for ground truth, `scripts/rule <n>` to re-resolve
each dotted citation above, then re-derive and re-compare. If a derivation now
disagrees with a current-CR reading, fix the sibling reference doc and commit
that fix separately before updating this doc. If a *ruling* now looks stale
relative to a CR change, record `RULING STALE` with the current rule proving
it — do not edit docs to match a stale ruling. Finish with
`scripts/cite check` (exit 0).
