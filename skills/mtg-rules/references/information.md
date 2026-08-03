# Information — Visibility & Hidden State

*Synthesized from the Comprehensive Rules effective 2026-06-19
(`data/rules/cr.json`). Orientation only — verify load-bearing specifics
with `scripts/rule` before citing. Run `scripts/cite check` after CR
refreshes.*

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
| Library | no one — not even the owner (401.2) | hidden; no player may look at or change it (401.2) | public: anyone may count any library at any time (401.3) |
| Hand | owner only; others may not look (402.3) — base-game default; multiplayer variants can override: 2HG teammates may review each other's hands at any time (810.5) | owner arranges freely (402.3) | public: others may count at any time (402.3) |
| Graveyard | everyone — any player may examine any graveyard at any time (404.2) | face-up single pile; order normally can't be changed (404.2) | public |
| Battlefield | everyone (400.2); face-down permanents are the exception (§2) | n/a | public |
| Stack | everyone (400.2) | public, tracked — each new object goes on top (405.2) | public |
| Exile | everyone by default (406.3); face-down exile is the exception (§2) | no defined order; face-down exiled cards kept in separate piles (406.4) | public |
| Command, ante | everyone (400.2); face-down conspiracies are the exception (§4) | n/a | public |

Order edge cases: when an effect puts two or more cards into a specific
library position at once, the owner picks their relative order and *does
not reveal it* (401.4). Simultaneous graveyard arrivals: owner picks the
order (404.3). Graveyard order is normally immutable but 404.2 explicitly
defers to tournament rules that may allow reordering.

## 2. Face-down sub-model (708)

The one sanctioned breach of the public-zone default.

- **Characteristics**: a face-down spell or permanent has only the
  characteristics listed by the ability or rules that allowed it to be face
  down (708.2); if nothing is listed, it's a 2/2 creature with no text, no
  name, no subtypes, no mana cost (708.2a). A card exiled face down has *no*
  characteristics at all (406.3a).
- **Controller's look rights**: at any time you may look at a face-down
  spell you control on the stack or a face-down permanent you control (even
  phased out). You can't look at anyone else's face-down spells or
  permanents, nor at face-down cards in any other zone (708.5).
- **Differentiation duty**: a player controlling multiple face-down objects
  must keep them distinguishable at all times — what made each face down,
  cast/entry order, which attacked last turn (708.6). This is the CR
  mandating engine-grade bookkeeping at the table.
- **Four enablers, two procedure families** (each turn-up is a special
  action that doesn't use the stack, 116.2b):
  - *Cast face down*: morph — cast as the face-down 2/2 by paying {3}
    rather than the mana cost (702.37a); disguise is morph plus ward {2}
    (702.168a). Turn-up: show all players what the permanent's
    morph/disguise cost *would be* face up, then pay that cost (702.37e,
    702.168d). While face down, effects and prohibitions that gate casting
    see only the face-down characteristics (702.37c, 702.168b, 708.4).
  - *Put onto the battlefield face down*: manifest (701.40a); cloak is
    manifest plus ward {2} (701.58a). Turn-up: show all players that the
    card is a creature card and what its mana cost is, then pay that mana
    cost (701.40b, 701.58b). A manifested/cloaked instant or sorcery card
    that would turn face up is instead revealed and stays face down
    (701.40g, 701.58g).
  - Spells normally can't be turned face up at all (708.7). On turn-up,
    copiable values revert and enters-the-battlefield abilities don't fire
    again (708.8).
- **Reveal-on-leave verification duty** (708.9): a face-down permanent or
  face-down component of a merged permanent leaving the battlefield, or a
  face-down spell leaving the stack for any zone but the battlefield, is
  revealed to all players as it moves; a player leaving the game reveals
  all their face-down permanents, merged-permanent components, and spells;
  at game end everything face down is revealed. This is the CR's audit step — proof
  after the fact that the hidden commitment was legal all along.
- **Face-down exile**: such cards can't be examined except when
  instructions allow it — and once a player is allowed to look, that
  permission *persists* until the card leaves exile or is shuffled into a
  pile, even after the granting instruction lapses (406.3). Look rights are
  stateful, not derivable from the current zone. Face-down exiled cards
  are kept in separate piles by when and how they were exiled (406.4), with
  further pile separation to track distinct ways of returning (406.5).
  Choosing among them: a specific face-down card only if you're allowed to
  look at it; otherwise choose a pile and a card is picked from it at
  random (406.4). Castability is gated on look permission — you may begin
  to cast a spell from among face-down cards in exile only if you can look
  at the face-down card (601.3f, 406.3b); unless it's being cast face down,
  the card turns face up just before announcement (406.3a).

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
- **Continuous visibility statics** (corpus-verified): `Play with your hand
  revealed.`, `Your opponents play with their hands revealed.`, `Play with
  the top card of your library revealed.` These are subscriptions — the
  entitlement holds for as long as the effect applies. Top-card machinery:
  if the top card changes while a spell is being cast, an ability is being
  activated, or a special action is being taken, the new top card isn't
  revealed and can't be looked at until that process completes (401.5,
  completion per 601.2i); a revealed top card that stops being revealed for
  any length of time becomes a new object when re-revealed (401.6).
- **One-shot inspections are snapshots, not subscriptions** (corpus: `Look
  at target opponent's hand.`): the look is an event that ends; nothing
  entitles the looker to updates when the hand changes. What the player
  remembers afterward is player memory, outside the game state — the CR
  models *ongoing* entitlement only via the statics above.

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
- **Linked memory and its privacy**: the noted name is readable only
  through the same object's linked "the chosen name" ability (702.106d);
  the per-object hidden-state inventory is in `state.md` §6. Contrast
  exile-linking — "cards exiled with [this object]" (406.6) uses identical
  linked-ability bookkeeping, but its payload (which cards) is public.

## 5. Information events

- **Shuffle destroys order information for everyone**: to shuffle is to
  randomize the cards so that *no player* knows their order (701.24a).
  Revealed cards in a library that get shuffled or reordered stop being
  revealed and become new objects (701.20d).
- **Why library actions are irreversible** (733.1): when an illegal action
  is reversed, players may *not* reverse actions that moved cards to a
  library, moved cards from a library to any zone other than the stack,
  caused a library to be shuffled, or caused cards from a library to be
  revealed. The reason is informational: knowledge can't be un-learned, so
  rewinding would leave a player knowing cards the restored state says are
  hidden. The CR forbids restoring that state rather than pretend the
  knowledge is gone. (Rewind mechanics: `casting.md`; the event log:
  `events.md`.)
- **Random disclosure**: `Target opponent reveals a card at random from
  their hand.` (corpus) — RNG as the discloser: information moves without
  any player choosing what to show. Same shape as the random pick from a
  face-down exile pile (406.4).
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
    }

- Visibility transitions are events — reveal, look, shuffle, turn face up,
  zone change — and belong in the event log (`events.md`). Reveal windows
  (701.20a) are event-scoped lifetimes, not standing state flags.
- Replay, netplay, and AI all consume this layer: a server that ships full
  state to clients leaks library order; an AI must search over the
  information set, not the true state; a replay viewer needs per-player
  projections to answer "what did they know when".
- Hidden-state commitments need verifiable bookkeeping: the differentiation
  duty (708.6) and the forced reveals (708.9, 702.106e) are the CR's audit
  protocol. Engine equivalent: commit (e.g., hash) the hidden payload when
  it's created and open the commitment at the forced reveal — morph
  identities and noted names become checkable without trusting the client.
- Look permission is stateful per (player, object) (406.3): store grant
  records; it cannot be recomputed from zone and face-down status alone.
