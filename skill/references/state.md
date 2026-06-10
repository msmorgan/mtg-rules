# Game State — Component Taxonomy

*Synthesized from the Comprehensive Rules effective 2026-04-17
(`data/rules/cr.json`). Orientation only — verify load-bearing specifics
with `scripts/rule` before citing. Run `scripts/check-citations` after CR
refreshes.*

What an engine must track, top to bottom. Closed lists are enumerated in
full; open vocabularies (creature types, etc.) point at `data/catalogs/*.json`.

## 1. Top level

A game state = **players** + **zones** + **objects** + **game-level
bookkeeping** (turn structure, the stack, continuous-effect/replacement
accounting, and game-wide designations). A player is one of the people in the
game (102.1); the *active player* is whose turn it is, the rest are nonactive
(102.1). A zone is a place where objects can be (400.1). An object is a thing
that can exist in a zone (109.1). Game-level bookkeeping is everything in §8.

## 2. Players

Per-player state the rules reference:

- **Life total** — starts at 20 (119.1); variant starts differ: Two-Headed
  Giant 30 (119.1a), Vanguard 20±modifier (119.1b), Commander 40 (119.1c),
  Brawl 25/30 (119.1d), Archenemy archenemy 40 (119.1e). Damage normally
  causes loss of that much life (119.2).
- **Counters a player can have** — counters are placed on an object *or a
  player* (122.1). Player counters defined in §122: **poison** (10+ loses the
  game, "poisoned" = 1+, 122.1f), **rad** (triggers at precombat main phase,
  122.1i). Two more player counters are defined in §107, not §122: **energy**
  (paid as {E}, one removed from the player per symbol, 107.14) and **ticket**
  (a numbered {TK} cost removes that many from the player, 107.17a). Each
  counter has a timestamp (613.7c).
- **Speed** — a player has none until a rule/effect sets it (702.179b); values
  run 1–4, "max speed" = 4 (702.179e). Start your engines! sets a player with
  no speed to 1 as an SBA (704.5z, 702.179a). The inherent triggered ability
  raises speed by 1 when an opponent loses life on the player's turn, only once
  each turn, only while speed < 4 (702.179d). No speed counts as 0 for effects
  that read it (702.179f).
- **Designations a player can have** — monarch (725.1), initiative (726.1),
  city's blessing (702.131c), planar controller (901.6). The *game* can have
  day/night (731.1). Full enumeration with mechanics: see `designations.md`.
- **Maximum hand size** — normally seven; excess discarded in cleanup (402.2, 514.1).
- **Ownership vs control** — owner = who started the game with the card in
  their deck (or brought/started it; 108.3). A card has no controller unless
  it represents a permanent or spell; otherwise use its owner (108.4, 108.4a).
  Only objects on the stack or battlefield have a controller (109.4); see §6.

### Per-turn tracked history (event log required)

Many effects look back at what happened *this turn*; an engine cannot answer
these from the current snapshot, so **an event log keyed by turn is required**
(608.2i states such effects look back in time, not at the current state).
Kinds the rules reference (examples, not exhaustive):

- Spells cast this turn (storm, 702.40a; day/night spell count, 502.2).
- Lands played vs lands playable this turn (305.2a, 305.2b).
- Damage a player/opponent was dealt this turn (bloodthirst, 702.54a; prowl
  combat damage, 702.76a).
- Creatures a player attacked with this turn (608.2i example).
- Permanents that were activated this turn (700.10).
- Permanent cards put into a graveyard this turn — "descended" (700.11);
  gravestorm counts those from the battlefield (702.69a).
- Mana spent on spells this turn — "expend" (700.14).
- Phased-out permanents remembered by who controlled them when they phased
  out, to phase back in (502.1).
- First card drawn this turn (miracle, 702.94a).

Distinct from this: "until end of turn" / "this turn" *effects* end in cleanup
(514.2, 703.4p) — that is duration tracking on effects (§8), not a history log.

## 3. Zones

Closed list (400.1): **library, hand, battlefield, graveyard, stack, exile,
command**; some older cards use **ante** (400.1, 407.1). Per-player: library,
hand, graveyard. Shared: battlefield, stack, exile, command, ante (400.1).
Objects sent to a wrong library/graveyard/hand go to the owner's (400.3).

| Zone | Visibility | Scope | Ordered? |
|------|-----------|-------|----------|
| Library | hidden (402.2-adjacent; 400.2) | per-player (400.1) | yes — face-down pile, order fixed unless allowed (400.5, 401.2) |
| Hand | hidden (400.2) | per-player (400.1) | no (400.5) |
| Battlefield | public (400.2) | shared (400.1) | no — arranged freely but control/tap/attach clear (400.5) |
| Graveyard | public (400.2) | per-player (400.1) | yes — ordered; owner arranges simultaneous adds (400.5, 404.3) |
| Stack | public (400.2) | shared (400.1) | yes — LIFO, top = most recent (400.5, 405.2) |
| Exile | public; cards may be face down (400.2, 406.3) | shared (400.1) | no (face-down piles fixed, 400.5) |
| Command | public (400.2) | shared (400.1) | no (400.5) |
| Ante | public (400.2) | shared (400.1) | no (400.5) |

"Outside the game" (sideboard, etc.) is **not** a zone (400.11, 400.11a).
**Command zone** holds emblems (114.1), commanders (903.6), dungeons with a
venture marker (309.4), and Planechase/Archenemy/Vanguard cards (408.1). In
**Commander**, each player's commander starts there (903.6) and may return
there (903.9); see §8.

## 4. Objects

Closed list (109.1) — an object is one of these:

| Object kind | Where it can exist |
|-------------|--------------------|
| Ability on the stack | stack (603.3, 405.1) |
| Card | any zone other than the stack as a bare card; library/hand/graveyard/exile/command (108.2, 400.1) |
| Copy of a card | wherever the copy is made (e.g., on the stack, 707) |
| Token | battlefield; ceases to exist elsewhere (111.1, 111.7) |
| Spell | stack — a card/copy put on the stack to be cast (111.13, 405.1, 112) |
| Permanent | battlefield only (110.1, 403.3) |
| Emblem | command zone (114.1, 109.4c) |

## 5. Characteristics

Closed list, verbatim (109.3): **name, mana cost, color, color indicator,
card type, subtype, supertype, rules text, abilities, power, toughness,
loyalty, defense, hand modifier, and life modifier.** Objects can have some or
all of these (109.3). Anything else about an object is *not* a characteristic —
explicitly excluded: tapped state, a spell's target, owner/controller, what an
Aura enchants (109.3). Card types, subtypes, supertypes, powers, toughnesses,
loyalties, etc. are open vocabularies → `data/catalogs/*.json` (card-types,
creature-types, land-types, supertypes, powers, toughnesses, loyalties …).

## 6. Per-object state beyond characteristics

These are tracked *per object*, not characteristics (109.3 says owner,
controller, target, tapped, what an Aura enchants are not characteristics):

- **Controller** — only stack/battlefield objects have one (109.4); six
  exceptions (mana ability, waiting trigger, emblem, plane/phenomenon, scheme,
  vanguard/conspiracy) in 109.4a–g. Permanent's controller defaults to who it
  entered under (110.2).
- **Owner** — 108.3; token owner = its creator (111.2).
- **Status** (permanents only, 110.5d) — closed list, four categories each with
  two values (110.5): **tapped/untapped, flipped/unflipped, face up/face down,
  phased in/phased out.** Enter untapped/unflipped/face up/phased in unless
  stated (110.5b); retained until changed (110.5c). Status is not a
  characteristic (110.5a).
- **Class level** — a *level* designation any permanent can have (716.2b),
  set by a class level bar; a Class retains its level even if it stops being a
  Class, and level is not a copiable characteristic (716.2b). A permanent with
  no level is treated as level 1 (716.2d).
- **Room door designations** — a Room (shared-type-line permanent) tracks the
  "left half unlocked" / "right half unlocked" designations; a half is
  "unlocked" if it has the matching designation, else "locked" (709.5c).
- **Secretly noted card name(s)** — hidden agenda: a face-down conspiracy in
  the command zone has a card name (two for double agenda) noted in secret
  with it (702.106b); per-object hidden state until turned face up.
- **Counters** on the object — kinds, mechanics, and SBA interactions in §122
  (+1/+1 & -1/-1 annihilate, 122.3; loyalty 122.1e; defense 122.1g; shield
  122.1c; stun 122.1d; finality 122.1h; keyword counters 122.1b). Lost on zone
  change (122.2). Each has a timestamp (613.7c).
- **Attachments** — what an Aura/Equipment/Fortification is attached to (an
  Aura's enchanted object is explicitly not a characteristic, 109.3); must stay
  clear on the battlefield (400.5).
- **Marked damage** — on creatures; lethal if ≥ toughness (SBA), removed on
  regeneration and in cleanup (120.6, 514.2).
- **Timestamp** — assigned on entering a zone (613.7d), re-assigned on
  attach (613.7e), face up/down flip (613.7f), transform/convert (613.7g);
  used to order continuous effects (613.7). Counters and stickers also carry
  timestamps (613.7c, 613.7k).
- **Casting choices** (for a spell on the stack) — modes (601.2b), targets and
  their count (601.2c), division/distribution among targets (601.2d), value of
  X (601.2b), and which costs/alternative costs were chosen (601.2b, 601.2f).
  An ability of the resulting permanent can reference what was paid (400.7d).
- **Linked-ability tracking** — for linked abilities, the engine must remember
  what the first ability did so the second can refer to it (607.1): cards
  "exiled with [this]" (607.2a, 607.2b, 607.2q), objects "put onto the
  battlefield with [this]" (607.2c), the chosen [value]/word (607.2d, 607.2f),
  noted information (607.2e), whether/what additional cost was paid (607.2i,
  607.2j).
- **Control-since-turn-began** ("summoning sickness") — a creature can't attack
  or use {T}/{Q} abilities unless controlled continuously since its
  controller's most recent turn began (302.6); haste bypasses this (702.10b,
  702.10c).
- **Stickers** — name/ability/power-toughness/art (123.1); a "stickered" object
  has ≥1 (123.4); not copiable values (123.1); each has a timestamp (613.7k).

## 7. Object identity across zones

Default: an object that moves zones becomes a **new object with no memory of
its previous existence** (400.7). Exceptions enumerated in 400.7:

- 400.7a — effects changing characteristics/controller of a permanent spell
  carry to the permanent it becomes.
- 400.7b — static-ability-granted battlefield abilities carry to that permanent.
- 400.7c — prevention effects on a permanent spell's damage carry over.
- 400.7d — a permanent can reference costs/mana paid to cast the spell.
- 400.7e — leaves-a-zone triggers find the new object in the destination (if
  public).
- 400.7f — enchanted-leaves triggers find the Auras' new objects in the
  graveyard.
- 400.7g–j — cast/play-enabling effects find the new object on stack/battlefield
  (and any effect moving an object to a public zone can find it, 400.7j).
- 400.7k — madness: effects can find the discarded card after it moves to a
  public zone.
- 400.7m — stickers persist across public zones (123.5) and keep applying.

Related identity rules: exiling an already-exiled object makes a new object
(400.8); command-zone face-down flip (400.9) or re-entry (400.10) makes a new
object. **Last known information (LKI):** when an effect needs info from an
object that has left the public zone it was expected in, it uses the object's
last known information (608.2h, 113.7a); targets/sources use LKI when checking
legality if the source has left (608.2b); deathtouch/lifelink/wither/infect on
a source that changed zones before dealing damage use LKI (702.2e, 702.15c,
702.80b, 702.90d). **Tokens** in any zone other than the battlefield cease to
exist (SBA, 111.7); a token that has left the battlefield can't return and
ceases to exist at the next SBA check (111.8). A copy of a permanent spell
becomes a token as it resolves (111.13). **Merged permanents:** a merged
permanent is one object represented by multiple components — the card/copy that
merged plus the components already there (730.2); it has only the topmost
component's characteristics (730.2a). The engine must track every component,
because when the merged permanent leaves the battlefield each component is put
into its own appropriate zone (730.3) and a finder effect finds all of them
(730.3c).

## 8. Game-level state

- **Turn order / active player** — active player is whose turn it is (102.1).
- **Phase / step** — five phases in order: beginning, precombat main, combat,
  postcombat main, ending; beginning/combat/ending have ordered steps (500.1).
- **Priority holder** — the player who may cast/activate/take special actions
  (117.1); timing rules in 117.1a–d.
- **Pending skips + extra-turn queue** — "skip [X]" is a replacement effect
  (614.10); pending skips must be *counted*, since two skip-next effects make a
  player skip the next two occurrences (614.10a). Extra turns are queued and
  taken LIFO — added one at a time (APNAP if multiple players), most recently
  created taken first (500.7).
- **The stack** — LIFO of spells and abilities (405.1, 405.2); top resolves
  first.
- **Triggers waiting to go on the stack** — abilities that have triggered are
  put on the stack the next time a player would get priority, in APNAP order
  (603.3, 603.3b); a waiting trigger is controlled by who controlled its source
  when it triggered (603.3a, 109.4b).
- **Delayed triggered abilities** — created during resolution / by replacement
  / by static permission; persist until their trigger event (603.7, 603.7a–b),
  with tracked source and controller (603.7d–g).
- **Continuous-effect bookkeeping** — timestamps order effects within a layer
  (613.7); the dependency system can override timestamps (613.8, 613.8a). Layer
  details: see `effects.md`.
- **Replacement effects already applied** — a replacement effect gets only one
  opportunity per event and does not invoke itself repeatedly (614.5);
  Commander's command-zone replacement is an explicit exception that may apply
  more than once (903.9b). The engine must track which replacements have
  already applied to a given event.
- **Day / night** — game-level designation; starts as neither, then exactly
  one (731.1); checked each untap step against the previous turn (502.2,
  731.2).
- **Dungeon progress** — per owner, a venture marker on the current room of a
  dungeon card in the command zone (309.4, 309.4a); venture moves it (309.5).
- **Attraction state** (niche) — per player: a face-down Attraction deck in the
  command zone (717.2) and a face-up "junkyard" pile of discarded Attractions
  (717.6a); each precombat main phase a controller of Attractions rolls a d6 to
  visit them (701.52).
- **The Ring** — each tempting gives/updates an emblem named The Ring and sets
  the player's Ring-bearer (701.54a, 701.54c); Ring-bearer is a permanent
  designation (701.54b); the number of times the Ring has tempted a player is
  tracked (701.54c).
- **Monarch / initiative** — single-holder designations; monarch (725.1),
  initiative with its inherent triggered abilities (726.1, 726.2).
- **Commander state** — per player: commander designation is an attribute of
  the card, retained across zones (903.3); **commander tax** = +{2} per
  previous cast from the command zone (903.8); **commander damage** — 21+
  combat damage from one commander loses the game, tracked per
  (dealer-commander, recipient) pair as an SBA (903.10a). Commanders may be
  redirected to the command zone (903.9a, 903.9b).
