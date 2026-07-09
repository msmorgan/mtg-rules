# Designations — The Scattered Global Flags, Unified

*Synthesized from the Comprehensive Rules effective 2026-06-19
(`data/rules/cr.json`). Orientation only — verify load-bearing specifics
with `scripts/rule` before citing. Run `scripts/cite check` after CR
refreshes.*

A **designation** is an ad-hoc boolean flag the CR attaches to a player, a
permanent, or the game itself — *not* a characteristic (109.3), *not* a
counter (122), *not* status (110.5). The rules introduce them one at a time,
scattered across §701–§731 and §903, with no central list and no glossary
entry of their own. This doc is that list. Most are *marker* designations
with "no rules meaning other than to act as a marker that spells and abilities
can identify" (701.37b); a few (monarch, initiative, day/night, unlocked,
suspected) carry inherent rules behavior. Several keyword *actions* simply
toggle a designation — those keywords live in `keywords.json`; the
designations they set are enumerated here. Engine storage cross-ref:
`state.md`.

Per designation: **carrier** (who holds it), **gained by**, **lost by /
persistence**, **effect**, **CR home**.

## Player-carried designations

### Monarch
- **Carrier:** a player; at most one in the game at a time (725.3).
- **Gained by:** an effect instructing a player to become the monarch; there
  is no monarch until one does (725.1). The current monarch ceases to be as
  another becomes it (725.3).
- **Lost by / persistence:** persists until someone else becomes monarch. If
  the monarch leaves the game, the active player (or next eligible player in
  turn order) becomes monarch; if none can, the game continues with no monarch
  (725.4).
- **Effect:** two inherent (source-less) triggered abilities — the monarch
  draws a card at the beginning of their end step, and whenever a creature
  deals combat damage to the monarch, its controller becomes the monarch
  (725.2). A static effect keyed to "the monarch" does nothing while there is
  no monarch (725.5).
- **CR home:** 725.1–725.5.

### The initiative
- **Carrier:** a player; at most one at a time (726.3).
- **Gained by:** an effect instructing a player to take the initiative; none
  exists until one does (726.1). Taking it removes it from the current holder
  (726.3).
- **Lost by / persistence:** persists until another player takes it. If the
  holder leaves the game, the active player (or next in turn order) takes it
  (726.4). Re-instructing the current holder to take the initiative does not
  make a second designation; it only re-triggers the last ability in 726.2
  (726.5).
- **Effect:** three inherent (source-less) triggered abilities (726.2): at the
  holder's upkeep they venture into Undercity; when creatures deal combat
  damage to the holder, that attacker's controller takes the initiative; and
  whenever a player takes the initiative they venture into Undercity. (Undercity
  is the dungeon, 205.3p.)
- **CR home:** 726.1–726.5.

### City's blessing
- **Carrier:** a player; **any number** of players may have it simultaneously
  (702.131c) — the only player designation that is not single-holder.
- **Gained by:** the ascend keyword. On an instant/sorcery (spell ability) or
  on a permanent (static ability): if you control ten or more permanents and
  don't have it, you get it for the rest of the game (702.131a, 702.131b).
- **Lost by / persistence:** never — "for the rest of the game" (702.131a). No
  lose path defined.
- **Effect:** pure marker, no inherent rules meaning; other cards check for it
  (702.131c). Gaining it reapplies continuous effects before trigger conditions
  are checked (702.131d).
- **CR home:** 702.131a–702.131d.

### Planar controller
- **Carrier:** a player (single); exactly one whenever a face-up plane or
  phenomenon card exists (Planechase) (311.5, 312.4, 901.6).
- **Gained by:** being the active player by default — the planar controller is
  normally whoever the active player is (901.6). Succession when the current
  planar controller would leave the game: the next player in turn order who
  wouldn't leave the game becomes the planar controller instead (901.6). In
  the team variant, the planar controller is normally the primary player of
  the active team; if that team would leave the game, the primary player of
  the next team in turn order becomes the planar controller (901.12b).
- **Lost by / persistence:** lost when the holder leaves the game (replaced by
  succession, 901.6), or when a different player becomes the active player —
  whichever comes first (311.5, 901.6).
- **Effect:** controls the face-up plane or phenomenon card (311.5, 312.4).
- **CR home:** 311.5, 312.4, 901.6, 901.12b.

## Game-carried designations

### Day / Night
- **Carrier:** the **game itself** (731.1). The game starts with neither.
- **Gained by:** "it becomes day" / "it becomes night" — via daybound/nightbound
  (702.145) or other effects (731.1). Once it becomes day or night, the game
  always has exactly one of the two thereafter (731.1).
- **Lost by / persistence:** never lost outright once present, only switched —
  "day becomes night" / "night becomes day" loses the first and gains the
  second (731.1a). Checked each untap step (second part) against the previous
  turn: day→night if the previous active player cast no spells; night→day if
  they cast two or more; if neither, no check (502.2, 731.2a–731.2c).
- **Effect:** marker the daybound/nightbound transform abilities and other
  cards read; not a player flag.
- **CR home:** 731.1–731.2 (untap check 502.2, 703.4b).

## Permanent-carried designations

### Ring-bearer (+ The Ring)
- **Carrier:** a permanent (a creature you control) per player; the Ring is an
  emblem the player gets (701.54c).
- **Gained by:** "the Ring tempts you" — choose a creature you control to
  become your Ring-bearer (701.54a). On first temptation the player also gets
  an emblem named The Ring (701.54c). The temptation fires and increments the
  per-player temptation count even if choosing a Ring-bearer was impossible
  (e.g., you control no creatures) (701.54d).
- **Lost by / persistence:** until another creature becomes your Ring-bearer or
  another player gains control of it (701.54a). Not a copiable value (701.54b).
- **Effect:** The Ring emblem grants escalating abilities to your Ring-bearer
  by number of times the Ring has tempted you (1: legendary + can't be blocked
  by greater power; 2+: draw/discard on attack; 3+: blocker's controller
  sacrifices it **at end of combat**; 4+: opponents lose 3 life on combat
  damage) (701.54c). "Is your Ring-bearer" =
  on the battlefield under your control with the Ring-bearer designation
  (701.54e). The temptation count is tracked per player (701.54c).
- **CR home:** 701.54a–701.54e.

### Goaded
- **Carrier:** a permanent (a creature) (701.15b).
- **Gained by:** a spell/ability that goads it (701.15a).
- **Lost by / persistence:** until the next turn of the controller of the
  goading spell/ability (701.15a). A creature can be goaded by multiple players
  (each adds requirements, 701.15c); the same player goading again does nothing
  (701.15d). Not an ability, not a copiable value (701.15b).
- **Effect:** the creature attacks each combat if able, and attacks a player
  other than the goader's controller if able (701.15b).
- **CR home:** 701.15a–701.15d.

### Suspected
- **Carrier:** a permanent only (701.60b).
- **Gained by:** a spell/ability instructing a player to suspect a creature
  (701.60a).
- **Lost by / persistence:** until it leaves the battlefield or a spell/ability
  causes it to no longer be suspected (701.60a). Can't become suspected again
  while already suspected (701.60d). Neither an ability nor copiable (701.60b).
- **Effect:** the permanent has menace and "This creature can't block" while
  suspected (701.60c). (Unlike pure markers, this designation grants abilities
  directly.)
- **CR home:** 701.60a–701.60d.

### Left half / right half unlocked (Room doors)
- **Carrier:** a permanent with a shared type line (e.g. a Room) on the
  battlefield (709.5c). The two together are the "unlocked designations"; a
  half is "unlocked" if it has its designation, else "locked" (709.5c). A
  "door" is a half (709.5j).
- **Gained by:** entering with the half cast as a spell gives that half's
  unlocked designation (709.5d); paying a locked half's mana cost — the
  "unlock cost," a special action with priority and an empty stack in a main
  phase of the player's turn (709.5e, 116.2m); or an effect that "unlocks" a
  half (709.5f).
- **Lost by / persistence:** an effect that "locks" a half removes its unlocked
  designation (709.5g). Otherwise persists.
- **Effect:** while a half lacks its unlocked designation, the permanent
  doesn't have that half's name, mana cost, or rules text (709.5). Triggers
  fire on unlocking a half (709.5h) and on "fully unlocking" (gaining the
  second of the two) (709.5i).
- **CR home:** 709.5–709.5j (unlock special action 116.2m).

### Class level
- **Carrier:** any permanent (716.2b) — set via a class level bar (716.2).
- **Gained by:** activating a class level bar's ability ("[Cost]: Level N —"),
  legal only from level N-1 and as a sorcery (716.2a). "Gain a Class level" =
  activate such an ability (716.2c).
- **Lost by / persistence:** a Class retains its level even if it stops being a
  Class (716.2b). Not a copiable characteristic (716.2b). A permanent with no
  level is treated as level 1 (716.2d).
- **Effect:** the static side grants abilities "as long as this Class is level
  N or greater" (716.2a).
- **CR home:** 716.2–716.2d.

### Sector (alpha / beta / gamma)
- **Carrier:** a permanent (a creature) (702.158b). The three values are alpha,
  beta, gamma sector (702.158b).
- **Gained by:** the space sculptor keyword (Space Beleren) — as an SBA, while
  a space-sculptor permanent and any creatures without a sector coexist,
  controllers choose a sector for each such creature (702.158a, 702.158c,
  704.5u).
- **Lost by / persistence:** kept until no player controls a space-sculptor
  permanent or ability source (702.158b). Not copiable (702.158b).
- **Effect:** marker for "choose a sector / each creature in that sector"
  effects; two permanents are "in the same sector" if their sectors match
  (702.158d, 702.158e).
- **CR home:** 702.158a–702.158e (SBA 704.5u).

### Prepared
- **Carrier:** a permanent that has a prepare spell (722.3a).
- **Gained by:** a spell/ability causing it to become prepared, or entering
  prepared, *only* if it has the prepare-spell alternative characteristics and
  doesn't already have the designation (722.3a).
- **Lost by / persistence:** an effect can make it "unprepared," removing the
  designation (722.3b); it is also lost when the prepared copy is cast, at the
  moment it becomes cast (722.3c).
- **Effect:** gaining it (or phasing in prepared) creates a castable copy in
  exile with only the prepare spell's characteristics, which persists while the
  permanent stays prepared (722.3c).
- **CR home:** 722.3a–722.3d.

### Saddled
- **Carrier:** a permanent (a Mount) (702.171b).
- **Gained by:** the saddle activated ability — tap untapped creatures of total
  power N or more, as a sorcery (702.171a). A creature "saddles" it as it's
  tapped for that cost (702.171c).
- **Lost by / persistence:** until end of turn, or until it leaves the
  battlefield (702.171b). Not copiable (702.171b).
- **Effect:** pure marker; "saddled" abilities check for it (702.171b).
- **CR home:** 702.171a–702.171c.

### Pure-marker permanent designations (no inherent rules meaning)

Each "has no rules meaning other than to act as a marker that spells and
abilities can identify"; only permanents can have them; each persists until the
permanent leaves the battlefield; none is an ability or a copiable value. These
four share the same shape — permanent-carried, gained by their named keyword
action, never lost while on the battlefield, no inherent effect beyond being
referenced by abilities — so they're listed compactly; the only difference is
how each is gained.

- **Solved** — a Case becomes solved via "To solve — [Condition]" at your end
  step; enables its "Solved —" ability (719.3a–719.3c).
- **Monstrous** — set by "Monstrosity N" (put N +1/+1 counters, become
  monstrous, only if not already) (701.37a, 701.37b).
- **Renowned** — set by the renown triggered ability on dealing combat damage
  to a player (702.112a, 702.112b).
- **Harnessed** — set by "Harness [this permanent]" if not already harnessed
  (701.64a, 701.64b).

## Card-attribute designation (not a board flag)

### Commander
- **Carrier:** a card (an *attribute of the card*, not a characteristic of the
  object) (903.3).
- **Gained by:** designated during deck construction; one legendary creature /
  Vehicle / Spacecraft card per deck (903.3).
- **Lost by / persistence:** retained even across zones and while face down or
  copying another card (903.3); a copy of a commander is not a commander
  (903.3 example). Meld/merge results inherit it (903.3b, 903.3c).
- **Effect:** "control/cast/in-zone a commander" all key off this attribute
  (903.3d); effects can read the commander's characteristics in any zone
  (903.3e). Mechanics (tax, command-zone replacement, commander damage) — see
  `state.md` §8.
- **CR home:** 903.3–903.3e.

## Engine note — where each designation lives

State location terms cross-ref `state.md` (player state §2, per-object state
§6, game-level state §8).

| Designation | Carrier | State location |
|-------------|---------|----------------|
| Monarch | player (single) | game flag = player ref (`state.md` §8) |
| Initiative | player (single) | game flag = player ref (`state.md` §8) |
| City's blessing | player (multi) | per-player flag (`state.md` §2) |
| Planar controller | player (single) | per-player flag (`state.md` §2) |
| Day / Night | game | game flag (tri-state) (`state.md` §8) |
| Ring-bearer (+ Ring emblem, count) | permanent + player | object flag + per-player emblem/count (`state.md` §6, §8) |
| Goaded | permanent | object flag w/ duration + goader set (`state.md` §6) |
| Suspected | permanent | object flag (`state.md` §6) |
| Left/right half unlocked | permanent | per-object flag pair (`state.md` §6) |
| Class level | permanent | per-object level value (`state.md` §6) |
| Sector (α/β/γ) | permanent | per-object enum (`state.md` §6) |
| Prepared | permanent | object flag + exiled copy ref (`state.md` §6) |
| Saddled | permanent | object flag w/ EOT duration (`state.md` §6) |
| Solved / Monstrous / Renowned / Harnessed | permanent | per-object boolean (`state.md` §6) |
| Commander | card | card attribute, zone-independent (`state.md` §8) |
