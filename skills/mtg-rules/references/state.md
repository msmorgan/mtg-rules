# Game State — Component Taxonomy

*Synthesized from the Comprehensive Rules effective 2026-09-25
(`data/rules/cr.json`).*

What an engine must track, top to bottom. Closed lists are enumerated in
full; subtype classes are CR-enumerated (205.3g–q, check with
`scripts/rule 205.3<letter>`); only printed values (power, toughness,
loyalty) are open vocabularies → `data/catalogs/*.json`.
A pseudo-code rendering of this taxonomy (plus the damage pipeline) lives in
`engine.md`.

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
  counter has a timestamp (613.7c). Counter kinds are an open, Oracle-defined
  vocabulary (e.g. experience counters on players); the CR defines only these
  four for players (122.1 makes kinds name-defined).
- **Speed** — a player has none until a rule/effect sets it (702.179b). The CR
  fixes no range: the inherent trigger raises speed only while it is less than
  4 (702.179d), and cards set their own limits (Spikeshell Harrier can't
  reduce speed below 1; Gomif, Fast Racer lets it exceed 4). A player has max
  speed if their speed is 4 (702.179e). Start your engines! sets a player with
  no speed to 1 as an SBA (704.5aa, 702.179a). The inherent triggered ability
  raises speed by 1 when an opponent loses life on the player's turn, only once
  each turn, only while speed < 4 (702.179d). No speed counts as 0 for effects
  that read it (702.179f).
- **Designations a player can have** — monarch (725.1), initiative (726.1),
  city's blessing (702.131c), enduring story (702.195b), planar controller
  (901.6; Grand Melee Planechase can have several at once, 901.14, 901.14a,
  so an engine keeps a map from each face-up plane to its controller,
  UD-22). The *game* can have day/night
  (731.1). Full enumeration with mechanics: see `designations.md`.
- **Maximum hand size** — normally seven; excess discarded in cleanup (402.2, 514.1).
- **Mana pool** — per player; by default empties at the end of each step and
  phase (106.4), but retention can keep a unit (702.189a); model in `mana.md`.
- **Controlled by** — a player-controlling effect applies to the next turn the
  affected player actually takes (723.1); the latest overwrites (723.1a); it
  waits through skipped turns (723.1b). Only control of the player changes,
  not of their objects (723.3), and a player who has left the game never
  controls another player (800.4b); see `choices.md`.
- **In game / left the game** (104.5, 800.4a), with last known information
  about departed players (800.4i); see `outcomes.md` and `variants.md`.
- **Ownership vs control** — owner = who started the game with the card in
  their deck (or brought/started it; 108.3). A card has no controller unless
  it represents a permanent or spell; otherwise use its owner (108.4, 108.4a).
  Only objects on the stack or battlefield have a controller (109.4); see §6.

### Per-turn tracked history (event log required)

Many effects look back at what happened *this turn*; an engine cannot answer
these from the current snapshot, so **an event log keyed by turn is required**
(608.2i states such effects look back in time, not at the current state).
Kinds the rules reference (examples, not exhaustive):

- Spells cast this turn by every player, as an ordered log of casts rather
  than resolutions. Storm copies the spell "for each other spell that was cast
  before it this turn" by any player (702.40a). That count is fixed by cast
  order relative to the storm spell, not a tally read when the trigger
  resolves, so spells cast in response while the trigger waits don't count.
  Spells cast from any zone count, and so do spells that were countered
  (`scripts/rulings "Grapeshot"`). Copies are never cast, so they never count
  (707.10). Each instance of storm triggers separately (702.40b). The
  day/night check reads the previous turn's entries for that turn's active
  player (502.2; 502.2a for shared team turns).
- Lands played vs lands playable this turn (305.2a, 305.2b).
- Damage a player/opponent was dealt this turn (bloodthirst, 702.54a; prowl
  combat damage, 702.76a).
- Creatures a player attacked with this turn (608.2i example).
- Permanents that were activated this turn (700.10).
- Permanent cards put into a graveyard this turn — "descended" (700.11);
  gravestorm counts those from the battlefield (702.69a).
- Mana spent on spells this turn — "expend" (700.14).
- Activations this turn per ability instance per object (602.5b, 602.5c);
  "do this only once each turn" actions per controller (603.2h); resolutions
  of an ability this turn (603.7h), where a copy counts as the same ability
  (707.10b).
- Cards drawn this turn, counted per player; "the first card you've drawn
  this turn" is the one with none before it (miracle, 702.94a).

Distinct from this: "until end of turn" / "this turn" *effects* end in cleanup
(514.2, 703.4p) — that is duration tracking on effects (§8), not a history log.

## 3. Zones

Closed list (400.1): **library, hand, battlefield, graveyard, stack, exile,
command**; some older cards use **ante** (400.1, 407.1). Per-player: library,
hand, graveyard. Shared: battlefield, stack, exile, command, ante (400.1).
Objects sent to a wrong library/graveyard/hand go to the owner's (400.3).

| Zone | Visibility | Scope | Ordered? |
|------|-----------|-------|----------|
| Library | hidden (400.2, 401.2) | per-player (400.1) | yes — face-down pile, order fixed unless allowed (400.5, 401.2) |
| Hand | hidden (400.2) | per-player (400.1) | no (400.5) |
| Battlefield | public (400.2) | shared (400.1) | no — arranged freely but control/tap/attach clear (400.5) |
| Graveyard | public (400.2) | per-player (400.1) | yes — ordered; owner arranges simultaneous adds (400.5, 404.3) |
| Stack | public (400.2) | shared (400.1) | yes — LIFO, top = most recent (400.5, 405.2) |
| Exile | public; cards may be face down (400.2, 406.3) | shared (400.1) | no (face-down piles fixed, 400.5) |
| Command | public (400.2) | shared (400.1) | no (400.5) |
| Ante | public (400.2) | shared (400.1) | no (400.5) |

"Outside the game" (sideboard, etc.) is **not** a zone (400.11, 400.11a).
**Command zone** holds emblems (114.1, 408.2), commanders (903.6), dungeons
(309.2a–b), and the nontraditional cards that start there in the Planechase,
Vanguard, Archenemy and Conspiracy Draft variants (408.3), including
conspiracies a player puts there from their sideboard (905.4). Planar and
scheme decks are in the command zone, not outside the game (311.2, 312.2,
314.2, 901.4), and so is an Attraction deck (717.2); the discarded-Attraction
"junkyard" is a face-up pile there, not its own zone (717.6a). The owner's
venture marker tracks a dungeon's current room (309.4). Six card types are
never permanents and can't be cast: conspiracy (315.3), dungeon (309.2c),
phenomenon (312.2), plane (311.2), scheme (314.2) and vanguard (313.2). A
conspiracy, phenomenon, plane, scheme or vanguard card that would leave the
command zone stays there (400.4b). A dungeon leaves only by leaving the game
(309.2c). Their abilities work from the command zone; 113.6p says so for
planes, vanguards, schemes and conspiracies, and the per-type rules below
cover the rest:

- **Plane, scheme and vanguard:** static, triggered and activated abilities
  (311.4, 314.4, 313.4). A plane's or scheme's abilities work only while it is
  face up.
- **Conspiracy:** static or triggered abilities, which work while it is face
  up (315.5).
- **Phenomenon:** a triggered ability that triggers when you encounter it
  (312.5).
- **Dungeon:** room abilities, which may trigger while the dungeon is in the
  command zone (309.4c).

Controllers of emblems, planes, phenomena, vanguards, schemes and
conspiracies: §6 Controller (109.4c–g). A dungeon's room abilities are
controlled by its owner (309.4c). Other command-zone objects, such as a
commander, have no controller (109.4). In **Commander**, each player's
commander starts there (903.6) and may return there (903.9); see §8.

## 4. Objects

Closed list (109.1). The kinds overlap: a card on the stack is also a spell,
and a card on the battlefield is also a permanent. A description selects among
them by 109.2's words — "card" (109.2a), "spell" (109.2b), "source" (109.2c),
"scheme" (109.2d); with none of them and no specific zone it means a permanent
on the battlefield (109.2).

| Object kind | Where it can exist |
|-------------|--------------------|
| Ability on the stack | stack (603.3, 405.1) |
| Card | any zone (108.2, 400.1); on the stack it is also a spell (112.1), on the battlefield also a permanent (110.1) |
| Copy of a card | wherever the copy is made (e.g., on the stack, 707) |
| Token | battlefield; ceases to exist elsewhere (111.1, 111.7) |
| Spell | stack — a card on the stack (112.1), a cast copy of a card (112.1b, 707.12), or a copy of a spell put onto the stack without being cast (112.1a, 707.10) (405.1) |
| Permanent | battlefield only (110.1, 403.3) |
| Emblem | command zone (114.1, 109.4c) |

**Piles are groupings, not objects or zones.** When an effect separates
objects into piles (Fact or Fiction), each affected object goes into exactly
one pile unless the effect says otherwise (700.3a). A pile may be empty
(700.3d). Each member is still an individual object, and the pile itself is
not an object (700.3b). Members don't leave their zone while grouped (700.3c).
Fact or Fiction's revealed cards stay in the library until they are put into a
hand or graveyard. A graveyard split into piles keeps its order (700.3c).
Engine inference: represent an effect's piles as a partition of object ids
bound for that effect, with no zone move and no new object. The CR uses "pile"
in a separate sense for zone layout: each library and graveyard is kept as a
single pile (401.2, 404.2), and exiled cards are kept in separate piles by how
and when they were exiled and how they may return (406.4, 406.5). Those are
layout rules (`information.md` §1), except that 406.4's face-down piles also
govern choice: a player who can't look at a face-down exiled card chooses a
pile, and a card is chosen from it at random (406.4).

**Token characteristics.** A token has exactly the characteristics its
creating spell or ability defines. Those act as its printed text and its
copiable values, and anything left undefined is absent. A "1/1 green Saproling
creature token" has no mana cost, supertypes, rules text or abilities (111.3).
The creator sets the name and subtypes together. An unnamed token is named for
its subtypes plus "Token", and once it is on the battlefield, changing either
doesn't change the other (111.4). "Create [name], a ..." just supplies the name
(111.9). A token isn't a card (111.6). A predefined token uses its 111.10
definition, which the creating effect may modify or add to (111.10). The
predefined tokens (111.10a–x) are Treasure, Food, Gold, Walker, Shard, Clue,
Blood, Powerstone, Incubator (double-faced), the seven Roles (Cursed, Monster,
Royal, Sorcerer, Virtuous, Wicked, Young Hero), Map, Junk, Lander, Mutagen,
Vibranium and Heartwood. Any other token created by name alone takes the
Oracle characteristics of the card with that name (111.11). Rule 111 names
three cases in which no token is created (111.5, 111.12). An Aura token with
no legal host is another (303.4g, 303.4i):

- A rule or effect says a permanent with one or more of the token's
  characteristics can't enter the battlefield.
- It would be a copy of an instant or sorcery card.
- It would be a copy of a nonexistent object, unless last-known information
  applies.

## 5. Characteristics

Closed list, verbatim (109.3): **name, mana cost, color, color indicator,
card type, subtype, supertype, rules text, abilities, power, toughness,
loyalty, defense, hand modifier, and life modifier.** Objects can have some or
all of these (109.3). Anything else about an object is *not* a characteristic —
explicitly excluded: tapped state, a spell's target, owner/controller, what an
Aura enchants (109.3). Closed value lists, from the CR:

- **Colors:** white, blue, black, red, green (105.1).
- **Card types:** artifact, battle, conspiracy, creature, dungeon,
  enchantment, instant, kindred, land, phenomenon, plane, planeswalker,
  scheme, sorcery, vanguard (205.2a, 300.1).
- **Supertypes:** basic, legendary, ongoing, snow, world (205.4a).
- **Basic land types:** Plains, Island, Swamp, Mountain, Forest (305.6).

Six card types are **permanent types**: artifact, battle, creature,
enchantment, land, planeswalker (110.4). A "permanent card" has one of them
(110.4a). A "permanent spell" has one of them other than land (110.4b),
because a land is played, never cast (305.9). Define both by membership in
these lists, not by excluding instants and sorceries. Instants and sorceries
can never be permanents (110.4), but kindred depends on the card: each kindred
card has another card type and is cast and resolved as that type (308.1), so
it is a permanent card exactly when that other type is a permanent type
(110.4). Six other card types are neither permanents nor castable: conspiracy,
dungeon, phenomenon, plane, scheme, vanguard (§3). Subtypes are CR-enumerated
per card type in 205.3g–205.3q and the lists grow with each CR revision;
phenomenon, scheme, vanguard and conspiracy cards have no subtypes (205.3r).
Check membership with `scripts/rule 205.3<letter>`; the CR governs, and Oracle
determines which subtypes a card has (205.3f).

Printed powers, toughnesses and loyalties are the open vocabularies →
`data/catalogs/*.json`. The catalogs (including card-types, creature-types,
supertypes and the other subtype files) come from Scryfall and aren't CR-exact
in either direction. They add non-CR entries (for example Boss and Hero in
card-types.json, Elite and Token in supertypes.json, Terminus in
artifact-types.json, Klingon in creature-types.json, Duck in
planeswalker-types.json) and can lag new CR entries (artifact-types.json lacks
Heartwood, Lander, Mutagen and Vibranium). Use them as Oracle-attestation aids
only.

**Zone-dependent values.** Loyalty is a characteristic only planeswalkers have
(306.5), and defense is one battles have (310.4). Off the battlefield, each is
the printed number (306.5a, 310.4a). On the battlefield, each is the number of
loyalty or defense counters on the permanent (306.5c, 310.4c). The permanent
enters with that many counters through an intrinsic replacement effect
(306.5b, 310.4b). Modeling hazard: if an engine stores the printed number as
the live value, every battlefield read is wrong. That includes "deals damage
equal to its loyalty", damage removing counters (120.3c, 120.3h), and the
0-loyalty and 0-defense SBAs (704.5i, 704.5v, 704.5w). A non-planeswalker with
loyalty counters has no loyalty (306.5). Mana value also varies with zone and
face on multi-face cards; see Card forms below.

### Card forms: which characteristic set an object has

Some layouts carry more than one set of characteristics. Which set an object
has depends on its layout, its zone, how it was cast and, for double-faced
permanents, which face is up. Each such card is still one card (for example
709.2, 715.2c, 720.2c, 722.2c).

- **Split (709).** Outside the stack the card has both halves' characteristics
  combined. It has each half's card types and abilities (709.4c), and a
  combined mana cost that sets its colors and mana value (709.4b, 202.3d). The
  caster chooses a half before putting the card on the stack (709.3). Only
  that half is checked for castability and put on the stack (709.3a), and on
  the stack the other half's characteristics don't exist (709.3b). A fused
  split spell is the exception: its halves stay combined on the stack (709.4d,
  202.3d). On a shared-type-line split (Room), both halves exist as copiable
  values even on the stack (709.5b). On the battlefield a locked half lacks
  its name, mana cost and rules text (709.5; door designations: §6).
- **Flip (710).** A flip card has its normal characteristics everywhere except
  as a flipped permanent. A flipped permanent uses the alternative name, text
  box, type line, power and toughness (710.1b, 710.2), but flipping doesn't
  change its color or mana cost, and changes from external effects still apply
  (710.1c). Flipped is a status (110.5), and flipping is one-way. A flipped
  permanent that leaves the battlefield keeps no memory of having flipped
  (710.4).
- **Double-faced (712).** Each face of a non-meld DFC has its own
  characteristics (712.8). Outside the game, or in any zone other than the
  battlefield and stack, a DFC has only its front face's characteristics
  (712.8a).
  - **On the stack.** A DFC is cast front face up by default (712.11). The
    caster of an MDFC chooses which face to cast. Only that face is checked
    for castability and put on the stack (712.11b, 712.11c). A nonmodal DFC
    cast "transformed" or "converted" goes on the stack back face up
    (712.11a), and the front-face ability allowing this also counts toward
    castability (712.11d). That spell has only the back face's
    characteristics, but its mana value comes from the front face's mana cost
    (712.8c). A meld card on the stack has only its front face (712.8b).
  - **On the battlefield.** Only the face that is up applies (712.8d–f). By
    default, a resolving DFC enters with the face that was up on the stack
    (712.13; exception 712.13a). By default, a DFC put onto the battlefield
    from any other zone enters front face up (712.14), unless it is put
    "transformed" or "converted" (712.14a). A player playing an MDFC as a land
    chooses a land face (712.12). If an effect tries to put an MDFC whose front
    face isn't a permanent card onto the battlefield, the card stays where it
    is (712.14b).
  - **Mana value.** A nonmodal back face uses the front face's mana cost.
    Anything copying such a back face has mana value 0 (712.8e, 202.3a–b). An
    MDFC uses the mana cost of the face that is up (712.8f). A melded permanent
    has only the combined back face's characteristics. Its mana value is the
    sum of its front faces' mana values, and a copy of it has mana value 0
    (712.8g, 202.3c). Meld back faces have characteristics only as part of a
    melded permanent (712.4b).
- **Adventurer (715) and omen (720).** These cards have only their normal
  characteristics, except while on the stack as an Adventure or Omen (715.4,
  720.4). Cast that way, only the inset characteristics are checked for
  castability, and the spell has only those characteristics (715.3a–b,
  720.3a–b). A copy of such a spell is also an Adventure or Omen (715.3c,
  720.3c). An Adventure spell is exiled as it resolves, and its controller may
  play the card while it stays exiled, though not as an Adventure through that
  permission (715.3d). An Omen spell is shuffled into its owner's library as
  it resolves (720.3d).
- **Prototype (718).** A spell cast prototyped uses the alternative mana cost,
  power and toughness in place of the normal ones, and so does the permanent
  it becomes (718.3b). A colored alternative mana cost also sets its colors
  (718.3b), and its other characteristics don't change (718.5). In any other
  zone, or if it wasn't cast prototyped, it has only its normal
  characteristics (718.4). Copies keep the prototyped values (718.3c–d).
- **Preparation (722).** A preparation card has only its normal
  characteristics in every zone (722.4). Its prepare spell defines only the
  exiled copy that becoming prepared creates (722.3, 722.3c; `designations.md`
  Prepared).
- **Copiable values.** The alternative characteristic sets are copiable values
  (715.2b, 718.2a, 720.2b, 722.2b). Copying a double-faced permanent uses the
  face that is up (707.8), and a token created as a copy of a DFC is itself
  double-faced (707.8a; not a token that becomes a copy through a replacement
  effect).
- **Not a second set.** A leveler's striations are level-symbol static
  abilities keyed to level counters (711.2a–b). Off the battlefield a leveler
  has the power and toughness in its uppermost box (711.6).
- **Transform and convert are not status.** Transforming or converting turns a
  DFC permanent's other face up without making a new object (712.18). Only
  permanents represented by DFCs or double-faced tokens can do it (701.27a,
  712.9), and meld cards can't (712.4c). It is a different game action from
  turning a permanent face up or face down (701.27b). Which face is up isn't
  one of the four status categories (110.5). Engine inference: track it as a
  separate per-permanent field. A "transformed permanent" is a DFC on the
  battlefield with its back face up. A permanent with its front face up never
  is one, even if it was transformed before, and neither is a melded or merged
  permanent (701.27g).

## 6. Per-object state beyond characteristics

These are tracked *per object*, not characteristics (109.3 says owner,
controller, target, tapped, what an Aura enchants are not characteristics):

- **Controller** — only stack/battlefield objects have one (109.4); seven
  listed exceptions, 109.4a–g (the lead-in says "six"): mana ability, waiting
  non-delayed trigger, emblem, face-up plane/phenomenon, vanguard, scheme,
  conspiracy. A permanent's controller is, *by default*, the player it entered
  under (110.2, 110.2a). That is only the base value. Control-changing effects
  apply in layer 2 (613.1b), so the controller is a derived value even though
  it isn't a characteristic (109.3). Rules that ask who controls a permanent
  read the post-layer-2 value: which permanents untap (502.3), summoning
  sickness (302.6), who controls its triggered abilities (603.3a), who may
  sacrifice it (701.21a), and who gains life from its lifelink (702.15b).
- **Owner** — 108.3; token owner = its creator (111.2).
- **Status** (permanents only, 110.5d) — closed list, four categories each with
  two values (110.5): **tapped/untapped, flipped/unflipped, face up/face down,
  phased in/phased out.** Enter untapped/unflipped/face up/phased in unless
  stated (110.5b); retained until changed (110.5c). Status is not a
  characteristic (110.5a).
- **Phased out by/under controller X** — a phased-out permanent phases in
  during the untap step of the player who controlled it when it phased out
  (502.1, 702.26). Per Aura, Equipment or Fortification, record whether it
  phased out directly or indirectly (702.26g, 702.26h) and, if directly, what
  it was attached to (702.26i).
- **Class level** — a *level* designation any permanent can have (716.2b),
  set by a class level bar; a Class retains its level even if it stops being a
  Class, and level is not a copiable characteristic (716.2b). A permanent with
  no level is treated as level 1 (716.2d).
- **Room door designations** — a Room (shared-type-line permanent) tracks the
  "left half unlocked" / "right half unlocked" designations; a half is
  "unlocked" if it has the matching designation, else "locked" (709.5c).
- **Permanent designations** — per-permanent flags and values; gain and loss
  rules are in `designations.md`. Goaded, held once per goading player, each
  instance with its own duration (701.15a–d); suspected (701.60b);
  Ring-bearer (701.54b); sector (702.158b); prepared,
  with a reference to the exiled copy (722.3a–c); saddled, until end of turn
  (702.171b); solved, monstrous, renowned and harnessed, each until the
  permanent leaves the battlefield (719.3b, 701.37b, 702.112b, 701.64b). Each
  of those rules says its designation is not part of the permanent's copiable
  values (701.15b, 701.54b, 701.60b, 702.158b, 702.171b, 719.3b, 701.37b,
  702.112b, 701.64b), except that 722.3 is silent for prepared. Goaded,
  suspected, solved, monstrous, renowned and harnessed are also stated not to
  be an ability (701.15b, 701.60b, 719.3b, 701.37b, 702.112b, 701.64b).
- **Protector (battles)** — a per-battle player reference: "Each battle has a
  player designated as its protector" (310.9), only one at a time (310.9f). It
  is chosen as the battle enters (310.9a) and doesn't change if the permanent
  stops being a battle or becomes a copy of another battle (310.9g).
  State-based actions re-choose it (704.5x, 704.5y). Gain and loss rules:
  `designations.md`.
- **Secretly noted card name(s)** — hidden agenda: a face-down conspiracy in
  the command zone has a card name (two for double agenda) noted in secret
  with it (702.106b); per-object hidden state until turned face up.
- **Foretold / plotted** (cards in exile) — per-card markers on exiled cards.
  The CR calls neither a designation, and neither is status, which only
  permanents have (110.5d); gain and loss rules: `designations.md`
  (Exile-card states). A card becomes foretold or plotted through the
  special action (116.2h, 116.2k) or when an effect says a card in exile
  "becomes foretold" or "becomes plotted" (702.143d, 702.170c). That includes
  a spell the effect has just exiled ("exile target spell. It becomes
  plotted", Oracle-attested). Each marker needs the turn the card became
  foretold or plotted, because casting it waits until a later turn. The owner
  may cast a foretold card for any foretell cost it has once that turn has
  ended (702.143a, 702.143d). An effect that makes a card foretold may give it
  a foretell cost, so that cost is per-card data. That cost works even if the
  resulting spell doesn't have foretell (702.143d). The owner may cast a
  plotted card without paying its mana cost during their main phase, with the
  stack empty, on any later turn, even if the card doesn't have plot while in
  exile (702.170d). The owner may look at a foretold card while it stays in
  exile (702.143a, 702.143d). They must keep foretold cards distinguishable,
  including the order they were exiled in and any foretell costs other than
  the printed ones (702.143e). Becoming plotted is a trigger event ("When this
  card becomes plotted, ...", Oracle-attested). The marker ends with the
  exiled object (400.7). "Foretold" also survives as cast history: a spell
  "that was foretold" is one that was a foretold card before it was cast, even
  if it was cast for a different cost (702.143c). Engine inference: record
  that fact on the spell when it is cast, because "If this spell was foretold,
  ..." reads it at resolution.
- **Counters** on the object — markers, not objects. Counters have no
  characteristics, a counter is not a token, and counters with the same name
  are interchangeable (122.1). §122 gives rules meaning to these kinds:
  - +X/+Y and -X/-Y counters, which also work on creature cards in other
    zones (122.1a); +1/+1 and -1/-1 counters annihilate in pairs as an SBA
    (122.3).
  - Loyalty (122.1e), defense (122.1g), shield (122.1c), stun (122.1d) and
    finality (122.1h).
  - Hone: each hone counter on an Equipment gives +1/+0 to the creature it's
    attached to (122.1j).
  - Keyword counters, which grant their keyword to a permanent or to a card in
    another zone and apply in layer 6 (122.1b, 613.1f). They can be exactly
    flying, first strike, double strike, deathtouch, decayed, exalted, haste,
    hexproof, indestructible, lifelink, menace, reach, shadow, trample, and
    vigilance, "as well as any variants of those keywords" (122.1b). The base
    list is closed, but variants keep it open: "hexproof from [quality]" is a
    hexproof variant (702.11d).

  An SBA enforces "can't have more than N" maxima (122.4, 704.5r). When the
  object changes zones, its counters aren't "removed"; they cease to exist
  (122.2). Each counter has a timestamp (613.7c); a new counter of a kind
  already present gives every counter of that kind a new, identical timestamp
  (613.7c). Counter placement, removal and movement as events: `events.md`
  (Counter placed / removed).
- **Attachments** — what an Aura, Equipment or Fortification is attached to. An
  Aura's enchanted object is explicitly not a characteristic (109.3).
  Attachments must stay clear on the battlefield (400.5).
  - **Aura spell.** It targets (303.4a) and enters attached to its target
    (608.3c).
  - **Aura entering any other way.** It doesn't target, because only an Aura
    *spell* targets (303.4a). Unless the effect names the host, the player it
    enters under chooses, as it enters, an object or player that is legal for
    its enchant ability and any other applicable effects (303.4f). So
    hexproof, which only stops targeting (702.11b), doesn't prevent the
    choice, but protection does (702.16c). Official guidance:
    `scripts/rulings "Zur the Enchanter"`, `"Resurgent Belief"`.
  - **No legal host.** If there's no legal choice, or the named host is
    illegal or undefined, the Aura stays in its current zone. From the stack
    it goes to its owner's graveyard instead, and an Aura token isn't created
    (303.4g, 303.4i). Rulings also forbid choosing a permanent that enters at
    the same time as the Aura (`scripts/rulings "Brago, King Eternal"`).
  - **Other permanents.** A permanent that isn't an Aura, Equipment or
    Fortification enters unattached if an effect tries to put it onto the
    battlefield attached (303.4h). Trying to attach an Aura already on the
    battlefield to an illegal host does nothing (303.4j).
- **Marked damage** — on creatures; lethal if ≥ toughness (SBA), removed on
  regeneration and in cleanup (120.6, 514.2).
- **Flags reset at each SBA check** — per object, dealt damage by a deathtouch
  source since the last check (704.5h, 702.2b); per player, attempted to draw
  from an empty library since the last check (704.5b); per commander, put into
  a graveyard or exile since the last check (903.9a, 704.6d). 704.5s/714.4,
  704.5v/310.7, 704.5t/309.6, 704.6f/312.7 and 314.6 ask whether an object is
  the source of a triggered ability that has triggered but not yet left the
  stack. That is derived from the waiting-trigger queue plus the stack (§8),
  not new stored state.
- **Timestamp** — assigned on entering a zone (613.7d), re-assigned on
  attach (613.7e), turning face up or face down (613.7f), transform/convert
  (613.7g); used to order continuous effects (613.7). Counters and stickers also carry
  timestamps (613.7c, 613.7k); a new counter of a kind already present
  re-stamps every counter of that kind (613.7c). Face-up plane, phenomenon and
  scheme cards are stamped when turned face up (613.7h), vanguard cards at the
  beginning of the game (613.7i), and conspiracy cards at the beginning of the
  game and again when they turn face up (613.7j). Objects that would receive a
  timestamp simultaneously are ordered in APNAP order (613.7m).
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
  702.10c). Any change of controller breaks that continuity, whether a layer-2
  effect starts or ends or control is exchanged. The new controller can't
  attack with the creature or activate its abilities with {T} or {Q} in their
  costs until their next turn begins (302.6). Engine inference: key the clock
  to the object and its post-layer-2 controller, not to a flag set only on
  entry.
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
object that has left the public zone it was expected in, or that an effect has
moved from a public zone to a hidden zone, it uses the object's last known
information (608.2h, 113.7a); a departed source uses LKI during the legality
check, while a departed target is illegal (608.2b); deathtouch/lifelink/wither/
infect on a source that changed zones before dealing damage use LKI (702.2e,
702.15c, 702.80b, 702.90d). SBA-batch departures snapshot pre-batch (704.8);
statics never use LKI (604.7); look-back triggers (603.10a–g). The extent of
the snapshot is CR-underdetermined: see UD-9; same-zone recast identity: UD-4.
**Tokens** in any zone other than the battlefield cease to
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
- **Combat state** — per attacker, what it attacks (a player, planeswalker or
  battle, or nothing after 506.4c) and whether it was declared or put onto the
  battlefield attacking (508.4: attacking but never "attacked"; 508.4d: enters
  unblocked in later steps); per blocker, the attackers it blocks (509.1a);
  blocked/unblocked status that persists independently of the blockers
  (509.1h: a creature remains blocked even if every creature blocking it is
  removed from combat); the defending player(s) chosen at the beginning of
  combat (506.2, 506.2a); the removal-from-combat conditions (506.4,
  506.4a–e); the declared-attacker and declared-blocker sets for "attacks/
  blocks alone" (506.5) and, per defender, "attacks a player alone" / "is
  attacking a player alone" (506.6); the attack requirements in force at
  declaration, for "had to attack" (506.7); and which creatures had first or
  double strike as the first combat damage step began (510.4). Procedure:
  `turn.md` §3.
- **Priority holder** — the player who may cast/activate/take special actions
  (117.1); timing rules in 117.1a–d.
- **Pending skips + extra-turn queue** — "skip [X]" is a replacement effect
  (614.10); pending skips must be *counted*, since two skip-next effects make a
  player skip the next two occurrences (614.10a). Extra turns are inserted
  directly after the specified turn, one at a time (APNAP if multiple
  players), most recently created taken first (500.7). A global LIFO stack is
  an **engine simplification**, valid only while every grant is "after this
  one"; Emrakul, the Promised End anchors the extra turn to the controlled
  turn, which follows skips per 723.1b. A skip is a replacement (614.10) and
  extra turns are turns, so a pending "skip your next turn" consumes the next
  turn the player would take, extra or not (614.10a).
- **The stack** — LIFO of spells and abilities (405.1, 405.2); top resolves
  first.
- **Triggers waiting to go on the stack** — abilities that have triggered are
  put on the stack the next time a player would get priority, in APNAP order
  (603.3, 603.3b); a waiting trigger is controlled by who controlled its source
  when it triggered (603.3a, 109.4b).
- **Delayed triggered abilities** — created during resolution / by replacement
  / by static permission (603.7a). Each triggers only once, the next time its
  event occurs, unless it has a stated duration such as "this turn" (603.7b),
  and never on an event that happened before it was created (603.7a). Track
  its source and controller (603.7d–g; dash, blitz and warp: 608.3g, settled in
  `underdetermined.md` UD-40).
- **Continuous-effect bookkeeping** — timestamps order effects within a layer
  (613.7); the dependency system can override timestamps (613.8, 613.8a). Layer
  details: see `effects.md`.
- **Replacement effects already applied** — a replacement effect gets only one
  opportunity per event and does not invoke itself repeatedly (614.5);
  Commander's and an Attraction's command-zone replacements are explicit
  exceptions that may apply more than once (903.9b, 717.6). The engine must
  track which replacements have already applied to a given event.
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

### Carrier classes (where facts attach)

Every fact in this doc hangs off one of seven carriers: **object** (§§5–6);
**ability instance** — an acquired ability's once-per-turn restriction scopes
to that ability as acquired from that object, not to identically worded ones
(602.5c); **controller** — the "Do this only once each turn" flag is keyed by (the
source's controller, the ability on its source), not by the controller alone
(603.2h; `temporal.md` §4); **player** (§2); **team** — e.g. Two-Headed Giant's
shared life total (810.4); the **card** — a physical card across the objects it
becomes, as with the commander designation (903.3); and the **game** (§8). The
carrier column in
`designations.md` classifies every designation along this axis; `temporal.md`
§4 splits the once-per-turn flags by the same scopes (object/ability instance
for activation restrictions; source's controller keyed by the ability on its
source for the triggered 603.2h flag).
