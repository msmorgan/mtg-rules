# Information — Visibility & Hidden State

*Synthesized from the Comprehensive Rules effective 2026-09-25
(`data/rules/cr.json`).*

Who is entitled to see what, and when that changes. The CR's information
model has four layers: zone visibility defaults (§1), the face-down
exception machinery (§2), explicit reveal/look operations (§3), and
noted-in-secret payloads (§4). §5 treats information changes as events; §6
gives the engine shape. For *what* is tracked see `state.md`; for the
decisions hidden information feeds see `choices.md`; for the event log see
`events.md`.

## 1. Zone visibility defaults

**Hidden vs public is a property of the zone, not of the cards in it**
(400.2). Public zones — graveyard, battlefield, stack, exile, ante, command
— are zones in which all players can see the cards' faces, except cards
some rule or effect specifically allows to be face down. Hidden zones —
library and hand — are hidden *"even if all the cards in one such zone
happen to be revealed"* (400.2). A Telepathy-style static therefore never
converts a hand into a public zone; it grants visibility on top of an
unchanged hidden default.

| Zone | Faces visible to | Order | Count |
|---|---|---|---|
| Library | no one — not even the owner (401.2); double-faced cards must be indistinguishable from the other cards (712.7) | hidden; no player may look at or change it (401.2) | public: anyone may count any library at any time (401.3) |
| Hand | owner only; others may not look (402.3) — base-game default; multiplayer variants can override: 2HG teammates may review each other's hands at any time (810.5); other team variants: `variants.md` (808.5, 809.7, 811.5); double-faced cards must be indistinguishable from the other cards (712.7) | owner arranges freely (402.3) | public: others may count at any time (402.3) |
| Graveyard | everyone — any player may examine any graveyard at any time (404.2) | face-up single pile; order normally can't be changed (404.2) | public |
| Battlefield | everyone (400.2); face-down permanents are the exception (§2) | n/a | public |
| Stack | everyone (400.2); face-down spells are the exception, controller only (708.4, 708.5) | public, tracked — each new object goes on top (405.2) | public |
| Exile | everyone by default (406.3); face-down exile is the exception (§2) | unordered, except face-down piles, whose order is fixed (400.5); piles separated by when/how exiled (406.4-406.5) | public |
| Command, ante | everyone (400.2); exceptions: face-down conspiracies (§4) and the face-down planar and scheme decks kept there (901.4, 904.4; 701.31b, 701.33b) | planar/scheme decks are face-down piles with fixed order (400.5); otherwise n/a | public |

Order edge cases: when an effect puts two or more cards into a specific
library position at once, the owner picks their relative order and *does
not reveal it* (401.4). Simultaneous graveyard arrivals: owner picks the
order (404.3). Graveyard order is normally immutable but 404.2 explicitly
defers to tournament rules that may allow reordering. A card put "Nth from
the top" of a library with fewer than N cards goes on the bottom (401.7). N
is unbounded, so the placement clamps to the bottom rather than failing.

## 2. Face-down sub-model (708)

The one sanctioned breach of the public-zone default.

- **Characteristics**: a face-down spell or permanent has only the
  characteristics listed by the ability or rules that allowed it to be face
  down (708.2); if nothing is listed, a face-down *permanent* (turned face
  down or entering face down) is a 2/2 creature with no text, name,
  subtypes or mana cost (708.2a). A card exiled face down has *no*
  characteristics at all (406.3a), and neither does a face-down conspiracy
  card (315.5b). A reveal of a face-down permanent that needs information
  about it uses its characteristics ignoring any continuous effects
  (708.12).
- **Controller's look rights**: at any time you may look at a face-down
  spell you control on the stack or a face-down permanent you control (even
  phased out). You can't look at anyone else's face-down spells or
  permanents, nor at face-down cards in any other zone (708.5). That ban is
  a default that card text overrides (101.1): Lens of Clarity lets you look
  at face-down creatures you don't control, but not face-down spells on the
  stack (Lens of Clarity ruling 2014-09-20).
- **Differentiation duty**: a player controlling multiple face-down objects
  must keep them distinguishable at all times — what made each face down,
  cast/entry order, which attacked last turn (708.6). This is the CR
  mandating engine-grade bookkeeping at the table.
- **Enablers and procedure families** (an open list: 708.2a covers any
  spell or ability that turns a permanent face down or puts it onto the
  battlefield face down). Each enabler's controller turn-up procedure is a
  special action that doesn't use the stack (116.1, 116.2b); effects can
  also turn face-down permanents face up:
  - *Cast face down*: morph — cast as the face-down 2/2 by paying {3}
    rather than the mana cost (702.37a); megamorph is a morph variant whose
    cost is a morph cost (702.37b); disguise is morph plus ward {2}
    (702.168a). Turn-up: show all players what the permanent's
    morph/disguise cost *would be* face up, then pay that cost (702.37e,
    702.168d). While face down, effects and prohibitions that gate casting
    see only the face-down characteristics (702.37c, 702.168b, 708.4).
  - *Put onto the battlefield face down*: manifest (701.40a); manifest
    dread routes through manifest (701.62a); cloak is manifest plus ward
    {2} (701.58a). Turn-up: show all players that the card is a creature
    card and what its mana cost is, then pay that mana cost (701.40b,
    701.58b). A manifested/cloaked instant or sorcery card that would turn
    face up is instead revealed and stays face down (701.40g, 701.58g).
  - *Generic route* (a spell or ability turns a permanent face down, or
    puts it onto the battlefield face down): it has the 708.2a default or
    the characteristics the effect lists, and no special-action turn-up
    unless the object itself has morph or disguise (708.7, 702.37e,
    702.168d). Ixidron is the example. Double-faced permanents can't be
    turned face down (712.16); a double-faced card that is cast or enters
    face down stays hidden behind a face-down substitute card and/or opaque
    sleeves (712.15).
  - Face-down exile enablers (foretell 702.143a, hideaway 702.75a) are in
    the Face-down exile bullet below; hidden agenda is in §4.
  - Spells normally can't be turned face up at all (708.7). On turn-up,
    copiable values revert, effects already applied to the face-down
    permanent still apply, and abilities relating to entering the
    battlefield don't trigger or have any effect, because the permanent has
    already entered (708.8). If it entered face down, its own
    enters-the-battlefield abilities did not apply on entry either (708.3).
- **Reveal-on-leave verification duty** (708.9): a face-down permanent or
  face-down component of a merged permanent leaving the battlefield, or a
  face-down spell leaving the stack for any zone but the battlefield, is
  revealed to all players as it moves; a player leaving the game reveals
  all their face-down permanents, merged-permanent components, and spells;
  at game end, all face-down permanents, merged components and spells are
  revealed (708.9); face-down exile is not, except foretold cards
  (702.143f). This is the CR's audit step — proof after the fact that the
  hidden commitment was legal all along.
- **Face-down exile**: such cards can't be examined except when
  instructions allow it — and once a player is allowed to look, that
  permission *persists* until the card leaves exile or is shuffled into a
  pile, even after the granting instruction lapses (406.3). Look rights are
  stateful, not derivable from the current zone. Face-down exiled cards
  are kept in separate piles by when and how they were exiled (406.4), with
  further pile separation to track distinct ways of returning (406.5).
  Choosing among them: a specific face-down card only if you're allowed to
  look at it; otherwise choose a pile and a card is picked from it at
  random (406.4). If choosing is part of casting a spell or activating an
  ability, the chosen card isn't revealed until that cost is fully paid
  (406.4). Castability is gated on look permission — you may begin
  to cast a spell from among face-down cards in exile only if you can look
  at the face-down card (601.3f, 406.3b); unless it's being cast face down,
  the card turns face up just before announcement (406.3a). A player who
  owns multiple foretold cards must keep them distinguishable from each
  other and from their other face-down exiled cards (702.143e). A
  double-faced card exiled face down stays hidden behind a face-down
  substitute card and/or opaque sleeves (712.17).
- **Who may look at a face-down exiled card**: no one unless instructions
  allow it (406.3). The rules-level sources, in full:
  - *The instruction*: a player who is instructed to look at a card and
    then exile it face down, or who is allowed to look at one in exile, may
    keep looking until it leaves exile or is part of a pile that's
    shuffled, even after the instruction stops applying (406.3). The
    permission crosses the move into exile and stays with that player.
    Gonti's controller may still look after Gonti leaves the battlefield,
    and a player who gains control of Gonti may not (Gonti, Lord of Luxury
    rulings, 2016-09-20).
  - *Foretell*: the player who foretold the card, or the owner of a card
    that becomes foretold, may look at it while it remains in exile
    (702.143a, 702.143d).
  - *Hideaway*: the exiled card gains "The player who controls the
    permanent that exiled this card may look at this card in the exile
    zone" (702.75a). The grant names the current controller and 406.3 keeps
    each grant, so anyone who has controlled the permanent since the exile
    may look (Mosswort Bridge ruling, 2022-04-29).
  - Card text adds the rest (open; `scripts/corpus --match "may look at"`).
    Some lines scope the look to the instruction (`You may look at that
    card for as long as it remains exiled.`); others scope it to the source
    (`You may look at cards exiled with this creature.`). Source-scoped
    grants work like hideaway: a new controller of the source may look, and
    earlier controllers keep looking (Grimoire Thief rulings, 2013-07-01).

## 3. Reveal and look operations

- **Reveal = show to all players** (701.20a). The window is scoped: the
  card stays revealed as long as necessary for the parts of the effect it's
  relevant to; a reveal that's part of a cost — or caused by activating an
  ability from a hidden zone (602.2a) — lasts until the spell/ability
  leaves the stack; a reveal that causes a triggered ability to trigger
  extends until that trigger leaves the stack, but if the ability isn't
  put onto the stack the next time a player would receive priority, the
  card ceases to be revealed (701.20a). Revealing doesn't
  move the card out of its zone (701.20b), and an already-revealed card can
  be revealed again — paying a reveal cost with a card Telepathy already
  shows is legal (701.20c).
- **Look = reveal to a named subset**: looking at a card follows the same
  rules as revealing it, except it's shown only to the specified player
  (701.20e).
- **Continuous visibility statics** (corpus-verified). Reveal form: `Play
  with your hand revealed.`, `Your opponents play with their hands
  revealed.`, `Play with the top card of your library revealed.` Look form
  (private): `You may look at the top card of your library any time.`,
  `You may look at face-down creatures you don't control any time.` (Lens
  of Clarity), `You may look at cards exiled with this creature.` 401.5
  names both the reveal and the look form for the top card. These are
  subscriptions — the entitlement holds for as long as the effect applies.
  Top-card machinery: if the top card changes while a spell is being cast,
  an ability is being activated, or a special action is being taken, the
  new top card isn't revealed and can't be looked at until that process
  completes (401.5, completion per 601.2i); a card drawn mid-cast is
  likewise kept face down, with no characteristics, until the spell becomes
  cast or the casting is reversed, and can't pay a cost that needs specific
  characteristics (121.8); a revealed top card that stops being revealed for
  any length of time becomes a new object when re-revealed (401.6).
- **One-shot inspections are snapshots, not subscriptions** (corpus: `Look
  at target opponent's hand.`): the look is an event that ends; nothing
  entitles the looker to updates when the hand changes. What the player
  remembers afterward is player memory, outside the game state. Ongoing
  entitlements come from: reveal/look statics (both forms named in 401.5);
  standing look grants (406.3, including look-then-exile-face-down; 708.5;
  315.7; 702.143a, 702.143d; hideaway's granted ability, 702.75a); and team
  hand review in team variants (808.5, 809.7, 810.5; 811.5 limits it to
  adjacent teammates). A one-shot look at a card that stays in a hidden zone
  creates none. The full derivation is in §2 ("Who may look at a face-down
  exiled card") and §6.
- **Search = private look at a whole zone**: to search is to look at all
  cards in the zone, even a hidden one, and find a card that matches the
  description (701.23a). Found cards are not revealed unless the effect also
  says to reveal them (701.23e). When several players search at once, each
  looks at the same time, then they decide in APNAP order which card to
  find (701.23i).
- **Unverifiable hidden-zone qualities**: a player searching a hidden zone
  for cards with a stated quality (a type, a color) isn't required to find
  any of them even if present (701.23b), whereas a search simply for a
  quantity of cards must find that many, or as many as possible (701.23d). A
  search for an undefined quality may proceed but finds nothing (701.23c;
  the undefined values are UD-6). The same shape recurs: a player needn't
  cast a spell "if able" whose mandatory additional cost involves cards with
  a stated quality in a hidden zone (118.8c); a card discarded face down into
  a hidden zone has all characteristics undefined (701.9c); and cards chosen
  in a hidden zone may stay face down as long as each choice is clearly
  indicated (101.4a). Interpretation, not CR text: read as the CR's response
  to qualities no one can audit; the CR states no rationale.

## 4. Noted and secret information

- **Hidden agenda** (702.106a): as the conspiracy is put into the command
  zone, turn it face down and secretly choose a card name. "Secretly
  choose" is operationalized: note the name on a piece of paper kept with
  the face-down card (702.106b) — chosen, binding, and concealed. The
  turn-up special action reveals the chosen name (702.106c). Double agenda
  conceals even *how many* names were chosen until reveal (702.106f). The
  reveal duty on leaving the game or at game end mirrors 708.9 (702.106e).
- **Simultaneous secret commitment** (corpus-verified): `Each player
  secretly chooses a number 0 or greater, then all players reveal those
  numbers simultaneously…`; `Each opponent secretly chooses silence or
  snitch, then the choices are revealed.`; secret council votes — `Each
  player secretly votes for…, then those votes are revealed.` The pattern
  is commit-then-reveal: decisions made without information leaking between
  deciders, then opened together. Decision mechanics live in `choices.md`.
- **Linked memory and its privacy**: two separate questions. The
  per-object hidden-state inventory is in `state.md` §6.
  - *Visibility*: the controller makes the secret choice (702.106a,
    702.106b) and may look at the face-down conspiracy at any time (315.7).
    Others may not, until the controller turns it face up, which reveals the
    name (702.106c), or until the forced reveal when that player leaves the
    game or the game ends (702.106e).
  - *Reference*: the object's "the chosen name" ability refers only to the
    name chosen by that object's own hidden agenda (702.106d, 607.2d).
  - Contrast exile-linking — "cards exiled with [this object]" (406.6) uses
    identical linked-ability bookkeeping, but its membership is public
    (which pile, 406.4-406.5; each card's owner, per the Bane Alley Broker
    ruling 2013-01-24), while identities are public only for face-up
    exile. Face-down linked exile (hideaway 702.75a, Bane Alley Broker)
    hides identities behind 406.3 look grants.

## 5. Information events

- **Shuffle destroys order information for everyone**: to shuffle is to
  randomize the cards so that *no player* knows their order (701.24a).
  Revealed cards in a library that get shuffled or reordered stop being
  revealed and become new objects (701.20d). A look follows the reveal
  rules (701.20e) and lasts until the effect is done with the card
  (701.20a). So the same holds for looked-at cards that a library effect
  reorders: cards that scry or fateseal moves to the bottom or rearranges
  on top, and cards that surveil keeps on top in a new order (701.22a,
  701.29a, 701.25a). The text doesn't settle whether a looked-at card
  counts as reordered when it ends where it started, or when its order
  relative to the other cards is unchanged (e.g. scry 1 kept on top);
  registered as UD-28. No official ruling addresses
  either point; this is an engine inference resting on reading 701.20e and
  701.20d together.
- **Why library actions are irreversible** (733.1): when an illegal action
  is reversed, players may *not* reverse actions that moved cards to a
  library, moved cards from a library to any zone other than the stack,
  caused a library to be shuffled, or caused cards from a library to be
  revealed. 733.1 lists these actions and gives no reason. Read as
  informational (docs assumption; registered as UD-10): knowledge can't be
  un-learned, so rewinding would leave a player knowing cards the restored
  state says are hidden, and the CR forbids restoring that state rather
  than pretend the knowledge is gone. UD-10 also records the gap: no rule
  addresses a legal reversal of a non-library disclosure (an illegally cast
  spell returning to a hand everyone has now seen). (Rewind mechanics:
  `casting.md`; the event log: `events.md`.)
- **Random disclosure**: `Target opponent reveals a card at random from
  their hand.` (corpus) — RNG as the discloser: information moves without
  any player choosing what to show. Same shape as the random pick from a
  face-down exile pile (406.4). This doc treats RNG only as the discloser;
  what "at random" and a shuffle's randomness require is
  `underdetermined.md` UD-8.
- **Derived vs free information is tournament policy, not CR**: the CR
  never grades information by the effort needed to compute it. MTR §4.1
  defines four categories — status, free, derived, private — with distinct
  player obligations. One pointer: `scripts/mtr 4.1`. Don't cite MTR
  categories as game rules.

## 6. Engine note

The information layer is a projection system over the true state:

    PlayerView = project(GameState, player)   -- that player's information set
    ObjectInfo {
      identity,            -- the actual card (engine-side truth)
      visibility_mask,     -- per player: face? position? existence-only?
      committed_payload?,  -- face-down enabler + listed characteristics;
                           --   noted names (hidden agenda)
      look_grants,         -- persistent (player, object) permissions
                           --   (face-down exile, 406.3)
    }

- Visibility transitions are events — reveal, look, shuffle, turn face up,
  zone change — and belong in the event log (`events.md`). Reveal windows
  (701.20a) are event-scoped lifetimes, not standing state flags.
- Replay, netplay, and AI all consume this layer: a server that ships full
  state to clients leaks library order; an AI must search over the
  information set, not the true state; a replay viewer needs per-player
  projections to answer "what did they know when".
- Hidden-state commitments need verifiable bookkeeping: the differentiation
  duty and forced reveals (708.6, 708.9, 702.106e, 702.143e, 702.143f) are
  the CR's audit protocol. Engine equivalent: commit (e.g., hash) the hidden
  payload when it's created and open the commitment at the forced reveal —
  morph identities and noted names become checkable without trusting the
  client.
- Face-down-exile look permission is stateful per (player, object) (406.3):
  once granted, it outlives the instruction that granted it, so store grant
  records; it cannot be recomputed from zone and face-down status alone.
  Every other entitlement is either a live predicate (hand, face-down
  controller, statics such as 401.5's) or a one-shot look, which follows the
  reveal rules (701.20e) and ends with 701.20a's window.
- **No single owner-or-controller key** (engine inference from the rules
  listed). The rules-level look entitlements, in full (from a CR search for
  look at / examine / review):
  - hand → its player at any time (402.3); a hand holds only its owner's
    cards (400.3). A card drawn while a spell is being cast or an ability
    activated stays face down, with no characteristics, until that process
    finishes or is reversed (121.8). Team variants widen hand access
    (`variants.md`).
  - library → no one, owner included (401.2). Only effects open it:
    top-card statics (401.5), reveals and looks (701.20a, 701.20e), and
    searches (701.23a).
  - face-down spell or permanent → its controller, not its owner (708.5,
    §2).
  - face-down conspiracy in the command zone → its controller (315.7),
    which is its owner (315.6).
  - face-down card in exile → only §2's sources (406.3).
  - moving card → as it's drawn, its drawer, if an effect offers to reveal
    it (121.9). Before it moves to a public zone, its owner looks at it if
    they'll be able to look at it there, and for the battlefield so does
    every other player who will (400.6).

  Anyone allowed to look at a double-faced card may look at both faces
  (712.6). An "owns or controls" test gets three rows wrong outright and a
  fourth in part. It opens the viewer's own library twice: through
  ownership, and through control, because off the stack and battlefield
  nothing has a controller and a controller query falls back to the owner
  (109.4, 108.4a). It also opens a face-down exiled card to its owner
  (406.3), and a face-down permanent the viewer owns but an opponent
  controls (708.5). It also shows a drawer the card 121.8 keeps face down
  mid-cast, and it never opens a teammate's hand where a team variant allows
  it (`variants.md`).
- **Look-grant ledger** (engine inference): visibility = the live per-row
  predicates above ∪ live card-text statics (§3; e.g. `Play with your hand
  revealed.`, `You may look at face-down creatures you don't control any
  time.`) ∪ open reveal/look windows (701.20a, 701.20e) ∪ the 406.3 ledger.
  Write an entry whenever one of §2's exile sources first lets a player
  look, source-scoped ones included, because 406.3 keeps the permission
  after its source lapses. For look-then-exile-face-down, write the entry on
  the exiled object. The move makes a new object (400.7), but 406.3 carries
  the permission across it, so a ledger whose entries die on zone change
  loses it. Remove entries when the card leaves exile or its pile is
  shuffled (406.3). Library looks write no entry: what a player recalls of a
  scry is memory (§3; the CR keeps no knowledge state, UD-10), and a shuffle
  randomizes the order so that no player knows it (701.24a).
