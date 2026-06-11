# Rulings Check — The Model vs Official Rulings

*Synthesized from the Comprehensive Rules effective 2026-04-17
(`data/rules/cr.json`). Orientation only — verify load-bearing specifics
with `scripts/rule` before citing. Run `scripts/check-citations` after CR
refreshes.*

This doc validates the skill's model against WotC's own answer key. For ten
subsystem probes it states our **independent** derivation (from the
sibling reference docs + `scripts/rule`), then quotes the official ruling
(`scripts/rulings`, date-stamped `[YYYY-MM-DD]`) and records a verdict.

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

All ten probes verdict **MATCH** on the current CR; no sibling-doc fixes were
required. Re-run them (see Maintenance) after each CR refresh.

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
- A loyalty *ability* puts/removes counters as a **cost** (606.5), not as an
  effect — Doubling Season keys on effects, so activation costs are **not**
  doubled.

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

## Maintenance

Re-run every probe after any CR refresh — renumbering may move the cited rules
even when the rulings are unchanged. For each probe: `scripts/rulings <card>`
and `scripts/card <card>` for ground truth, `scripts/rule <n>` to re-resolve
each dotted citation above, then re-derive and re-compare. If a derivation now
disagrees with a current-CR reading, fix the sibling reference doc and commit
that fix separately before updating this doc. If a *ruling* now looks stale
relative to a CR change, record `RULING STALE` with the current rule proving
it — do not edit docs to match a stale ruling. Finish with
`scripts/check-citations` (exit 0).
