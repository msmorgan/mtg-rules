# Designations — The Scattered Global Flags, Unified

*Synthesized from the Comprehensive Rules effective 2026-09-25
(`data/rules/cr.json`).*

A **designation** is a status the CR attaches to a player, an object, or the
game itself — *not* a characteristic (109.3), *not* a counter (122), *not*
status (110.5). Most are introduced with "is a designation" (e.g. 701.15b,
725.1, 731.1). Four are conferred with "designated" phrasing instead: a
battle's protector (310.9), the planar controller (311.5), the commander
(903.3), and the archenemy (904.2a, covered in `variants.md`). They appear one
at a time across §310–§312, §701–§731, and §901–§904, with no central list and
no glossary entry for "designation". This doc is that list.

**Value shapes** (closed list): a flag (most); a flag held once per goading
player (goaded, 701.15c–701.15d); two independent flags on one permanent
(left/right half unlocked, 709.5c); an enum (sector: alpha, beta, or gamma,
702.158b); a number (Class level, read as 1 when absent, 716.2b, 716.2d); a
player (a battle's protector, 310.9); and a game-level value that starts as
neither and, once set, is always day or night (731.1). An object's
designation is never copied: copy effects take only copiable values (707.2),
and no designation is among them, as several rules restate (701.15b, 701.54b,
701.60b, 716.2b, 702.158b). Where the CR addresses it, a designation is also
not an ability (701.15b, 701.37b, 701.60b, 701.64b, 702.112b). Abilities can
key on a designation, and those abilities can be copiable (709.5). An
object's designations end when it changes zones, because it becomes a new
object (400.7; none of 400.7a-400.7m preserves one); the commander is the
only designation the CR states survives a zone change (903.3).

The CR calls seven of them pure markers, with "no rules meaning other than to
act as a marker": city's blessing, enduring story, monstrous, renowned,
harnessed, solved, saddled (702.131c, 702.195b, 701.37b, 702.112b, 701.64b,
719.3b, 702.171b). The rest carry behavior their rules define: monarch,
initiative, day/night, planar controller, battle protector, goaded, suspected,
unlocked halves, prepared, Ring-bearer (via The Ring emblem, 701.54c), and
commander (903.8–903.10a); Class level and sector are values that card
abilities read (716.2a, 716.2d; 702.158d). Several keyword *actions* simply
toggle a designation — those keywords live in `keywords.json`; the
designations they set are enumerated here. Engine storage cross-ref: `state.md`.

Scope: speed (702.179) is a per-player value the CR never calls a designation
(`state.md` §2). Archenemy (904.2a), emperor (809.2), primary player (805.2)
and Grand Melee turn markers "designated for removal" (807.4e–807.4g) are
variant setup roles or bookkeeping; use the 8xx/9xx rules indexed by
`variants.md`.

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
  whenever a player takes the initiative they venture into Undercity. (Venture
  into Undercity is the 'venture into [quality]' variant, 701.49d; Undercity is
  the dungeon type, 205.3p. With no dungeon in the command zone you start
  Undercity; otherwise you follow 701.49b–c: advance in your current dungeon,
  or, from its bottommost room, complete it and then start Undercity (701.49c;
  Aarakocra Sneak ruling 2022-06-10).)
- **CR home:** 726.1–726.5.

### City's blessing
- **Carrier:** a player; **any number** of players may have it simultaneously
  (702.131c). It is one of the multi-holder player designations, along with
  enduring story (702.195b).
- **Gained by:** the ascend keyword. On an instant/sorcery (spell ability) or
  on a permanent (static ability): if you control ten or more permanents and
  don't have it, you get it for the rest of the game (702.131a, 702.131b).
- **Lost by / persistence:** never — "for the rest of the game" (702.131a). No
  lose path defined.
- **Effect:** pure marker, no inherent rules meaning; other cards check for it
  (702.131c). Gaining it reapplies continuous effects before trigger conditions
  are checked (702.131d).
- **CR home:** 702.131a–702.131d.

### Enduring story
- **Carrier:** a player; **any number** of players may have it simultaneously
  (702.195b).
- **Gained by:** the storied keyword. If you control three or more permanents
  that are artifacts, Sagas, and/or legendary permanents and don't have an
  enduring story, you gain one for the rest of the game (702.195a). This is a
  three-permanent threshold across the union of those qualities, not three of
  each.
- **Lost by / persistence:** never — "for the rest of the game" (702.195a).
  No lose path is defined.
- **Effect:** pure marker, no inherent rules meaning; other cards can check for
  it (702.195b). Gaining it reapplies continuous effects before trigger
  conditions are checked (702.195c).
- **CR home:** 702.195a–702.195c.

### Planar controller
- **Carrier:** a player (Planechase). Normally exactly one whenever a face-up
  plane or phenomenon card exists (311.5, 312.4, 901.6). Grand Melee
  Planechase designates several at once: each player who will start the game
  with a turn marker sets a starting plane, and "Each of them is a planar
  controller" (901.14a). Several planes or phenomena may then be face up at
  once (901.14).
- **Gained by:** being the active player by default — the planar controller is
  normally whoever the active player is (901.6). Succession when the current
  planar controller would leave the game: the next player in turn order who
  wouldn't leave the game becomes the planar controller instead (901.6). In
  the team variant, the planar controller is normally the primary player of
  the active team; if that team would leave the game, the primary player of
  the next team in turn order becomes the planar controller (901.12b).
- **Lost by / persistence:** lost when the holder leaves the game (replaced by
  succession, 901.6), or when a different player becomes the active player —
  whichever comes first (311.5, 901.6). Grand Melee replaces succession: if a
  player's leaving would reduce the number of turn markers, that player first
  ceases to be a planar controller "but no other player becomes a planar
  controller". Each face-up plane or phenomenon they controlled goes to the
  bottom of its owner's planar deck, and no player has planeswalked (901.14b).
- **Effect:** controls the face-up plane or phenomenon card (311.5, 312.4).
- **Underdetermined** (UD-22): with several
  planar controllers, the CR doesn't say which face-up plane each one
  controls. Nor does it say who controls a plane while its passed turn marker
  waits to start a turn (807.4c, 807.4d), or what remains after one of them
  planeswalks, since planeswalking moves every face-up plane away (701.31b,
  901.11c). Engine inference: store a face-up plane → planar-controller map,
  not one player reference.
- **CR home:** 311.5, 312.4, 901.6, 901.12b, 901.14–901.14b.

## Game-carried designations

### Day / Night
- **Carrier:** the **game itself** (731.1). The game starts with neither.
- **Gained by:** "it becomes day" / "it becomes night" (731.1). Daybound and
  nightbound set it from neither at any time, not only in the untap step. Any
  time a player controls a permanent with daybound and it's neither day nor
  night, it becomes day (702.145d). Any time a player controls a permanent
  with nightbound, it's neither, and there are no permanents with daybound on
  the battlefield, it becomes night (702.145g). So a daybound and a nightbound
  permanent arriving together make it day (Brutal Cathar ruling, 2021-09-24).
  Other effects can also make it day or night (731.1). Once it becomes day or
  night, the game always has exactly one of the two thereafter (731.1).
- **Lost by / persistence:** never lost outright once present, only switched —
  "day becomes night" / "night becomes day" loses the first and gains the
  second (731.1a). So "whenever day becomes night" triggers don't fire when
  the game first becomes day or night (Celestus Sanctifier ruling,
  2021-09-24). Checked each untap step (second part) against the previous
  turn: day→night if the previous active player cast no spells; night→day if
  they cast two or more; if neither, no check (502.2, 731.2a–731.2c). Shared
  team turns: day→night if no player on the previous turn's active team cast
  a spell; night→day if any one player on that team cast two or more spells
  (731.2a–731.2b, 502.2a).
- **Effect:** a marker that cards read; not a player flag. Daybound's statics
  make its permanent enter transformed at night and transform it as it becomes
  night; nightbound's transform it as it becomes day (702.145b, 702.145e).
  Separately, any time a player controls a front-face-up daybound permanent
  while it's night, or a back-face-up nightbound permanent while it's day,
  that player transforms it: "This happens immediately and isn't a
  state-based action" (702.145c, 702.145f). 702.145c, 702.145d, 702.145f and
  702.145g aren't among the abilities daybound and nightbound represent
  (702.145b, 702.145e). Engine inference: implement them as rule-level checks,
  outside both the permanent's static abilities and the 704.5 SBA list.
- **CR home:** 731.1–731.2 (untap check 502.2, 502.2a, 703.4b); daybound/nightbound
  702.145b–702.145g.

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
- **Carrier:** a permanent (701.15b), held once per goading player. A creature
  can be goaded by multiple players, each adding combat requirements
  (701.15c); the same player goading it again has no effect and adds none
  (701.15d). The goader is "the controller of the permanent, spell, or ability
  that caused it to be goaded" (701.15b). For a static, engine inference reads
  that as its source's current controller (611.3a).
- **Gained by:** the goad keyword action — "Until the next turn of the
  controller of that spell or ability, that creature is goaded" (701.15a). Or
  any effect that says a permanent is goaded, which sets its own duration
  (611.2a, 611.3a). Statics: "Creatures your opponents control with power less
  than Baeloth Barrityl's power are goaded"; "Enchanted creature gets +1/+1
  and is goaded" (Martial Impetus). One-shots with stated durations: "goaded
  for the rest of the game"; "goaded for as long as this Saga remains on the
  battlefield" (Oracle corpus).
- **Lost by / persistence:** each instance ends on its own clock. A goad
  action's instance ends at its goader's next turn (701.15a), or when that
  turn would have begun if the goader left the game (800.4m; Sly Instigator
  ruling 2021-04-16). A static's instance ends when the static stops applying
  (Baeloth Barrityl ruling 2022-06-10: "goaded for as long as Baeloth
  Barrityl is on battlefield, has the ability, and has sufficient power"). A
  stated duration ends when it lapses. Effects can also remove it ("each
  creature you control is no longer goaded", Serene Sleuth); engine inference:
  a static goad that still applies makes it goaded again at once (611.3a).
  Attacking doesn't end it, and neither does a control change (Martial Impetus
  ruling 2023-06-30). Not an ability, not a copiable value (701.15b).
- **Effect:** the creature attacks each combat if able, and attacks a player
  other than its goader if able (701.15b). If several opponents goaded it, it
  must attack an opponent who hasn't goaded it if able (requirement
  maximization 508.1d; Martial Impetus ruling 2023-06-30).
- **Underdetermined** (UD-21): 701.15d says only
  that the same player goading again "has no effect". It doesn't say whether
  that covers one player's instances with different durations, such as a
  static goad plus a goad action. If the later instance is a no-op, the
  creature stops being goaded when the earlier one ends. If it exists, it must
  add no requirements while both apply (701.15d).
- **CR home:** 701.15a–701.15d.

### Protector (battles)
- **Carrier:** a battle; the value is a player — "Each battle has a player
  designated as its protector" (310.9). A battle can have only one protector
  at a time (310.9f). The CR confers it with "designated as" phrasing, like
  planar controller and commander (310.9; glossary "Protect, Protector").
- **Gained by:** as the battle enters, its controller chooses its protector.
  The battle type decides who is eligible, and a battle with no battle type
  can be protected only by its controller (310.9a). Siege is the only battle
  type (205.3q), and a Siege's protector must be an opponent of its controller
  (310.12a). Another player becoming its protector ends the old one's
  (310.9f). State-based actions re-choose: if a battle has no player in the
  game as its protector and no creatures are attacking it (704.5x), or its
  protector is a player who can't be its protector (704.5y), its controller
  chooses an appropriate player; if none can be chosen, the battle is put into
  its owner's graveyard (704.5x, 704.5y).
- **Lost by / persistence:** it doesn't change if the permanent stops being a
  battle or becomes a copy of another battle (310.9g). A change of protector
  removes the battle from combat (506.4). A battle that leaves and returns is
  a new object (400.7) and gets a fresh choice as it enters (310.9a).
- **Effect:** the protector can't attack it. Any attacking player for whom the
  protector is a defending player can, so a Siege's own controller can
  (310.9b). Only the protector may block creatures attacking it (310.9c), and
  "defending player" for an attacked battle means its protector (310.9d).
  Decider rebinding: `choices.md`.
- **Underdetermined** (UD-23): 310.11 restricts
  both repairs to "a battle that isn't being attacked", but 704.5y (ineligible
  protector) has no such condition. A control change already removes the
  battle from combat (506.4), so the two texts give different results only
  when eligibility changes mid-attack without one. Example: an attacked Siege
  loses its battle type, which leaves only its controller eligible (310.9a).
- **CR home:** 310.9–310.9g, 310.11, 310.12a (SBAs 704.5x, 704.5y).

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
  704.5u). Players who don't control a space-sculptor permanent choose first,
  then the others (702.158c, 704.5u); a change of controller doesn't remove or
  reassign a sector, since it is kept until no player controls a space-sculptor
  permanent or ability source (702.158b; Space Beleren ruling 2022-10-07).
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
- **Carrier:** a permanent (702.171b); in card practice, a Mount.
- **Gained by:** saddle N (tap any number of *other* untapped creatures you
  control with total power N or greater, as a sorcery; 702.171a), or any effect
  that says the permanent becomes saddled. A creature "saddles" it as it's
  tapped for that cost (702.171c).
- **Lost by / persistence:** until end of turn, or until it leaves the
  battlefield (702.171b). Not copiable (702.171b).
- **Effect:** pure marker; "saddled" abilities check for it (702.171b).
- **CR home:** 702.171a–702.171c.

### Pure-marker permanent designations (no inherent rules meaning)

Each "has no rules meaning other than to act as a marker that spells and
abilities can identify"; only permanents can have them; each persists until the
permanent leaves the battlefield; none is an ability or a copiable value. The
four below share the same shape — permanent-carried, gained through their named
mechanic (keyword action: monstrosity 701.37a, harness 701.64a; triggered
keyword ability: renown 702.112a; Case keyword ability: to solve 719.3, 719.3a),
never lost while on the battlefield, no inherent effect beyond being referenced
by abilities — so they're listed compactly; the only difference is how each is
gained. City's blessing, enduring story and saddled, the other three pure
markers, have their own entries.

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
- **Gained by:** designated before the game; normally one legendary card that
  is a creature card, a Vehicle card, or a Spacecraft card with one or more
  power/toughness boxes (903.3). Exceptions: cards that say they can be your
  commander (903.3a, 113.6n); Brawl also allows a legendary planeswalker card
  (903.12c); a partner ability lets a deck designate two commanders instead of
  one, each ability with its own pairing requirement (including choose a
  Background's legendary Background enchantment, 702.124k), and never more than
  two (702.124a, 702.124g).
- **Lost by / persistence:** retained even across zones and while face down or
  copying another card (903.3); a copy of a commander is not a commander
  (903.3 example). Meld/merge results inherit it (903.3b, 903.3c).
- **Effect:** "control/cast/in-zone a commander" all key off this attribute
  (903.3d); effects can read the commander's characteristics in any zone
  (903.3e). Mechanics (tax, command-zone replacement, commander damage) — see
  `state.md` §8.
- **CR home:** 903.3–903.3e.

## Exile-card states (not CR designations)

Plotted and foretold are never called designations, but they have the same
shape. Each is a state a card in exile holds (not a 110.5 status), granted by
its keyword's special action or by other effects, and read by other cards
(glossary "Plotted", "Foretold"). The cast permission belongs to the state, not
to the keyword. Engine inference: each state ends with its object when the card
leaves exile, including by being cast (400.7).

### Plotted
- **Carrier:** a card in exile (702.170a, 702.170c).
- **Gained by:** the plot special action — exile the card from your hand and
  pay its plot cost, after which "It becomes a plotted card" (702.170a,
  116.2k) — or a spell or ability that makes a card in exile become plotted
  (702.170c; "If you do, it becomes plotted"). 116.2k's summary says "during
  their own turn", but 702.170a and the reminder text ("Plot only as a
  sorcery") require a main phase. Only the special action is "plotting a
  card" (702.170e). Engine inference: "becomes plotted" is the event both
  routes produce, so "When this card becomes plotted" (Longhorn Sharpshooter)
  watches both.
- **Effect:** its owner may cast it from exile without paying its mana cost
  during their main phase while the stack is empty, on any turn after the one
  in which it became plotted, "even if it doesn't have the plot ability while
  in exile" (702.170d). That timing binds instants and flash cards too (Aven
  Interrupter ruling, 2024-06-07).
- **CR home:** 702.170a–702.170f (special action 116.2k).

### Foretold
- **Carrier:** a card in exile. A spell "was foretold" if it was a foretold
  card before it was cast, even if it was cast for a cost other than a
  foretell cost (702.143c).
- **Gained by:** the foretell special action — pay {2} and exile a card with
  foretell from your hand face down, any time you have priority during your
  turn (702.143a, 116.2h) — or an effect stating that a card in exile becomes
  foretold, which may also give it a foretell cost (702.143d). Only the
  special action is "foretelling a card" (702.143c): "Whenever you foretell a
  card" doesn't trigger when a card merely becomes foretold (Ethereal Valkyrie
  ruling, 2021-02-05).
- **Effect:** its owner may look at it while it remains in exile. They may
  cast it for any foretell cost it has once the turn it became foretold has
  ended, "even if the resulting spell doesn't have foretell" (702.143a,
  702.143d). Owners must keep foretold cards distinguishable, including
  their exile order and any non-printed foretell costs (702.143e). Foretold
  cards are revealed when their owner leaves the game and at game end
  (702.143f). Engine inference: the spell must carry a was-foretold bit from
  its card, because "If this spell was foretold" reads the card's state from
  before the cast (702.143c).
- **CR home:** 702.143a–702.143f (special action 116.2h).

**Suspended** is not a held state: a card is suspended if it's in exile, has
suspend, and has a time counter on it (702.62b). Engine inference: derive it,
because a stored flag goes stale when the card loses suspend or its last time
counter.

## Engine note — where each designation lives

State location terms cross-ref `state.md` (player state §2, per-object state
§6, game-level state §8). The last three rows (plotted, foretold, suspended)
are exile-card states, not CR designations.

| Designation | Carrier | State location |
|-------------|---------|----------------|
| Monarch | player (single) | game flag = player ref (`state.md` §8) |
| Initiative | player (single) | game flag = player ref (`state.md` §8) |
| City's blessing | player (multi) | per-player flag (`state.md` §2) |
| Enduring story | player (multi) | per-player flag (`state.md` §2) |
| Planar controller | player (normally single; several in Grand Melee, 901.14a) | per-player flag + face-up plane → controller map (`state.md` §2) |
| Day / Night | game | game flag (tri-state) (`state.md` §8) |
| Ring-bearer (+ Ring emblem, count) | permanent + player | object flag + per-player emblem/count (`state.md` §6, §8) |
| Goaded | permanent | per-goader instances, each with its own duration — not one flag + goader set (`state.md` §6) |
| Protector | battle → player (one per battle) | per-object player ref (`state.md` §6) |
| Suspected | permanent | object flag (`state.md` §6) |
| Left/right half unlocked | permanent | per-object flag pair (`state.md` §6) |
| Class level | permanent | per-object level value (`state.md` §6) |
| Sector (α/β/γ) | permanent | per-object enum (`state.md` §6) |
| Prepared | permanent | object flag + exiled copy ref (`state.md` §6) |
| Saddled | permanent | object flag w/ EOT duration (`state.md` §6) |
| Solved / Monstrous / Renowned / Harnessed | permanent | per-object boolean (`state.md` §6) |
| Commander | card | card attribute, zone-independent (`state.md` §8) |
| Plotted | card in exile | per-object flag (`state.md` §6) |
| Foretold | card in exile; spell's was-foretold history | per-object flag + optional granted foretell cost; was-foretold bit on the spell (`state.md` §6) |
| Suspended | card in exile | derived predicate, never stored (702.62b) |
