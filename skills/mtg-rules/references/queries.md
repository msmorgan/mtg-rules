# Queries — The Predicate & Value Language

*Synthesized from the Comprehensive Rules effective 2026-09-25
(`data/rules/cr.json`).*

The emergent shared layer. Every taxonomy doc parameterizes over an
informal predicate-and-value language: `deontics.md`'s guards,
`events.md`'s trigger patterns, `costs.md`'s scaling riders,
`choices.md`'s option constraints, `keyword-classification.md`'s `how`
decompositions. This doc is that language's semantics. The parser
compiles `grammar.md` §5–6's surface forms *into* it; the engine
evaluates it; §7 is the contract between the two. It answers: what
"another", "each", "up to N target" and "that targets" select; what
"you", "it", "this way", "exiled with" and "the chosen [value]" refer
to; when X, counts and mana value are determined and how rounding and
undefined values behave; when LKI applies.

## 1. Object and player predicates

**Characteristic tests.** The testable fields are the closed 109.3 list
(name, mana cost, color, …, power, toughness — `state.md` §5). The values
compared are *layer-system outputs* read at query time (`effects.md`); P/T
in particular is the result of the 613.4 sublayers (CDAs first, 613.4a),
so "power 2 or less" sees the post-layers number, and comparisons may use
negative values directly (107.1b). Field specifics:

- **Color** — an object's colors come from mana symbols, color indicator,
  or a CDA (105.2); monocolored = exactly one, multicolored = two or more,
  colorless = none (105.2a, 105.2b, 105.2c).
- **Name** — self-names are identity, not string-match (§3; 201.5);
  interchangeable names are the same name for all game purposes (201.3a);
  "choose a card name" ranges over the Oracle reference (201.4).
  Comparison is set-based. Objects have the same name if they share at
  least one name, so a two-named object matches either name (201.2a). A
  nameless object (by default a face-down permanent, 708.2a) has the same
  name as nothing, not even another nameless object (201.2a). "Different"
  is not the complement. A group has different names only if every member
  has a name and no two share one; a face-down Demon spoils Liliana's
  Contract (201.2b). One object has a different name than others only if
  it has a name and shares none with them; nameless others don't stop
  that (201.2c). So a nameless object, as the object being tested,
  neither has the same name as nor a different name than anything, though
  a named object does differ from it (201.2c). Names can change in layer
  3: see `effects.md` §5.
- **Mana value** — total of the mana cost (202.3); no mana cost = 0
  (202.3a), except the back face of a nonmodal DFC permanent or spell,
  including one cast transformed or converted (front face's mana cost,
  202.3b, 712.8c, 712.8e), and a melded permanent (combined mana costs of
  its front faces, 202.3c, 712.8g). A copy of either has mana value 0
  (202.3b, 202.3c). Split cards use their combined halves off the stack
  or when fused, and the chosen half otherwise (202.3d, 709.4b). {X}
  counts as the announced value on the stack, 0 elsewhere (202.3e);
  hybrid uses the largest half (202.3f), Phyrexian counts 1 (202.3g).
- Colors, card types, supertypes, basic land types and the permanent
  types are closed CR lists, with "permanent card" and "permanent spell"
  defined by membership (105.1, 205.2a, 205.4a, 305.6, 110.4a-b).
  Colors: white, blue, black, red, green (105.1). Card types: artifact,
  battle, conspiracy, creature, dungeon, enchantment, instant, kindred,
  land, phenomenon, plane, planeswalker, scheme, sorcery, vanguard
  (205.2a). Supertypes: basic, legendary, ongoing, snow, world (205.4a).
  Basic land types: Plains, Island, Swamp, Mountain, Forest (305.6).
  Permanent types: artifact, battle, creature, enchantment, land,
  planeswalker; a permanent spell is any of these except land (110.4a-b).
  Subtype membership is authoritative in the CR's 205.3 lists.
  `data/catalogs/*.json` is Scryfall-derived and includes non-CR values
  (card-types adds Boss, Emblem, Event, Hero; supertypes adds Elite,
  Token; artifact-types adds Terminus and lacks Heartwood, Lander,
  Mutagen, Vibranium; other subtype catalogs diverge too). Use the
  catalogs only as a parsing convenience, checked against 205.3. Power
  and toughness are not a vocabulary: they are integers (107.1, 208.1) or
  `*` (208.2); `powers.json` and `toughnesses.json` are printed-string
  inventories, not value domains.

**Description defaults — the implicit zone quantifier.** A description
gets its domain from 109.2 when it has a card type or subtype and no
zone, "card", "spell", "source" or "scheme" — a *permanent on the
battlefield*; from 109.2a when it has "card" plus a zone (a card there);
from 109.2b for "spell" (on the stack); from 109.2c for "source" (a
source of ability/damage/mana in any zone); and from 109.2d for "this
scheme". Other phrases take their domain from their head noun (permanent
= on the battlefield, 110.1; player; token; ability) or, for targets,
from 115.2. A participial readback ("the exiled creature", "the
sacrificed creature's power") names the object as the deed found it,
reading the head noun as 109.2 would at deed time (engine inference).
Oracle writes "the exiled creature" for one exiled from the battlefield,
and "the exiled card" or "the exiled creature card" for one exiled from a
library or graveyard (corpus regularity, not CR text). Its values come
from that past state, the permanent as it last existed (LKI, 608.2h).
Curie, Emergent Intelligence ruling: "Curie's last ability refers to the
exiled creature, not the exiled card", even though 400.7j lets the effect
find the card in exile. Linked readbacks: §3 (607.2a).

**State tests** — explicitly *not* characteristics (109.3): **status**,
the four binary categories tapped/flipped/face-down/phased (110.5;
permanents only, 110.5d); **attacking/blocking**, which hold from the
declaration (508.1k, 509.1g), or from entering or being stated
attacking/blocking (508.4, 509.4), until removal from combat or the end
of the combat phase (508.1k, 509.1g, 506.4; glossary via
`scripts/define`); **blocked/unblocked**, a combat state only attacking
creatures have (not a 110.5 status), assigned by the blocker declaration,
by entering attacking during the declare blockers step or later, or by an
effect: three-valued, and "unblocked" is not ¬blocked (509.1h, 508.4d;
`turn.md` §3); a creature remains blocked even if all the creatures
blocking it are removed from combat (509.1h); **face-down** objects
expose only the characteristics their enabler lists — default a 2/2 with
no name (708.2, 708.2a; `information.md` §2). "Attacked" (an event, at
declaration) differs from "attacking" (a state): a creature put onto the
battlefield attacking is attacking but never "attacked" (508.4;
likewise blocking and "blocked", 509.4).
**Alone**: "attacks alone" and "blocks alone" are declaration events
(506.5; exalted, 702.83b); "attacking alone" and "blocking alone" are
states (506.5); "attacks a player alone" (event) and "attacking a player
alone" (state) are scoped to each attacked player (506.6). The two
families diverge in both directions, in any game size: 506.6 holds
without 506.5 when other attackers attack a different player, a
planeswalker, or a battle; 506.5 holds without 506.6 when the lone
attacker attacks a planeswalker or battle.

**Rule-defined derived tests**: named tests the CR defines from
characteristics, state, or turn history rather than as designations
(contrast `designations.md`). Objects: *historic* = legendary, artifact,
or Saga (700.6). *Modified* = has a counter, is equipped, or is enchanted
by an Aura controlled by the permanent's own controller, so an opponent's
Aura doesn't count (700.9). *Outlaw* = Assassin, Mercenary, Pirate,
Rogue, and/or Warlock (700.12); "outlaws you control" considers
permanents only (700.12a). *Worthy* = a legendary, non-Villain creature
that is red and/or white (700.16). *Suspended* = a card in exile with
suspend and a time counter (702.62b). *Unpaired* = not paired (702.95b).
*Stickered*: `state.md` §6 (123.4). *Had to attack* = an effect required
it to attack as attackers were declared (506.7). A permanent *activated
this turn* (700.10) and the player trackers *poisoned*, *max speed*,
*descended* and *expend N* are in `state.md` §2 (122.1f, 702.179e,
700.11, 700.14). A player *commits a crime* as they cast a spell,
activate an ability, or put a triggered ability on the stack that targets
an opponent, a permanent, spell, or ability an opponent controls, or a
card in an opponent's graveyard (700.13). The vocabulary is open, since
sets add terms: `scripts/define`, `scripts/rule-search`. Aggregates
(devotion, party): §4.

**Relational tests**: controller (only stack and battlefield objects have
one, 109.4; exceptions include pending triggers, 109.4b, and emblems,
109.4c; full list in `state.md` §6); owner (108.3); attached-to (not a
characteristic, 109.3 — per-object state, `state.md` §6); the AGENT
coordinate of an event's cause — "a spell or ability an opponent
controls" as destroyer/causer is a predicate over the cause triple
(`events.md` §3); and **targeting tests** (115.9): "with [N] targets"
counts instances chosen at stack-put (115.9a), "that targets
[something]" checks the targets' *current* state, ignoring departed ones
without LKI (115.9b), "targets only" counts distinct chosen targets, then
checks current state (115.9c).

**Keyword tests** ("with flying", "has hexproof", "loses trample"):
whether a test on a base keyword finds that keyword's variants is settled
rule by rule where the CR speaks (typecycling, 702.29f; hexproof from,
702.11e) and is an engine choice elsewhere (commander ninjutsu, whose rule
says only "a variant", 702.49d; `UD-29`). The
closed list of variants, with what each rule says, is in
`keyword-classification.md` (Keyword variants).

**Zone tests**: the closed 400.1 list (library, hand, battlefield,
graveyard, stack, exile, command, ante); per-player vs shared in
`state.md` §3.

## 2. Quantifiers and selectors

| Selector | Semantics | Rules |
|---|---|---|
| `target [desc]` | chosen at stack-put; targeted only by the word "target" in the text, or in a keyword's rule, such as an Aura spell's enchant ability, bestow, mutate or equip (115.10a, 115.1e, 115.1b, 702.103b, 702.140a, 702.6a); "you" never targets (115.10b); declared per 115.1; default domain: permanents (115.2) | 115.1, 601.2c |
| `N target` | exactly N distinct picks per instance of "target" (115.3); the same object may be re-picked across *different* instances | 115.3 |
| variable-count targets | count announced before the targets, then locked even if the defining information changes | 601.2c |
| `any target` | damage shorthand: creature, player, planeswalker, or battle; nothing else choosable | 115.4 |
| `up to N target` | 0..N; with zero chosen the spell/ability isn't targeted | 115.6 |
| `each [desc]` | untargeted universal over the domain at evaluation time | 109.2 domain; 608.2h read |
| `any number` | includes zero | 107.1c |
| `among [set]` | restricts a selector to a previously computed collection ("from among them") | corpus |
| division `among` targets | split announced with targets, min 1 each (§4) | 601.2d |

**"Another" / "other" — exclusion and its anchor (verified finding).**
The CR has **no general rule** for the exclusion. 109.5 defines only
"you"/"your" (§3), and 115.4 only lists "another target" among the damage
shorthands. The CR uses "another"/"other" as ordinary English throughout
its own prose (e.g. 701.14a, 702.134c, 121.2c). As a card-text selector
it appears only inside quoted templates and examples. Keyword
definitions use the word when it matters, and there a bare object-head
use always excludes the source: champion (702.72a), soulbond (702.95a),
station (702.184a), reconfigure ("another target creature you control",
702.151a), backup ("If that's another creature", 702.165a) and support.
Support writes "up to N *other* target creatures" on a permanent but "up
to N target creatures" on an instant or sorcery (701.41a). Rulings show
what a printed "other" excludes, its *anchor*:

- *A same-kind mention in the same ability, either earlier (an earlier
  sentence included) or later in the same sentence.* Engine inference
  (`UD-31`).
  - Earlier, same sentence: Arc Trail ("... 1 damage to any *other*
    target") excludes its first target. This is a **set-distinctness
    constraint evaluated on the final target set**, not exclusion of a
    fixed binding. Retargeting may swap the two targets, and only the
    final set is checked (115.7e example).
  - An earlier target is the anchor. Pit Fight (2013-01-24), Domri Rade
    (2017-03-14) and Ulvenwald Tracker (2017-03-14) all rule that the
    second target "can't be the same creature as the first target". Only
    the Tracker's source is itself a creature. Its ruling names no limit
    tied to the source, so "an earlier target beats a choosable source"
    is inferred from that silence, not stated.
  - Earlier sentence: Bond of Passion ("Gain control of target creature
    until end of turn. Untap that creature. It gains haste until end of
    turn. Bond of Passion deals 2 damage to any other target.") excludes
    the creature targeted in its first sentence. That is ordinary
    anaphora across sentences, since the whole text is read and later
    text can modify earlier text (608.2c), and the check is the same
    set-distinctness constraint on the final target set. The source is a
    spell, which "any target" can't select (115.4), so a source default
    would exclude nothing. No ruling states the exclusion, so it rests on
    the English reading.
  - Non-target mentions: Selvala, Heart of the Wilds (2016-08-23
    ruling): "The new creature's power is compared to the power of each
    other creature on the battlefield". Farrel's Mantle (2011-01-25
    ruling): "The enchanted creature's controller cannot choose to have
    the enchanted creature deal damage to itself". Pain for All's
    "enchanted creature deals damage ... to any other target" reads the
    same way by analogy (it has no rulings).
  - Later in the same sentence (cataphoric): Inquisitor's Flail's second
    ability, "If *another* creature would deal combat damage to equipped
    creature, it deals double that damage to equipped creature instead",
    contrasts "another creature" with the equipped creature named after
    it. No ruling covers this shape, so it rests on the English reading.
- *The source (`[desc] ∧ ≠ this object`), only when the ability has
  neither an earlier nor a later same-sentence mention:* "each other
  creature with flying", "Polukranos fights another target creature", and
  the keyword definitions above. The player analogue is "you": "Whenever
  a creature you control dies, each other player sacrifices a creature of
  their choice."

**Not this construction.** Some uses are outside this resolver:
- Definite `the other [N]` picks the other member of a two-participant
  event or pair, not the complement of the nearest mention. Venomous
  Fangs ("Whenever enchanted creature deals damage to a creature, destroy
  the other creature") destroys the damaged creature; its 2004-10-04
  ruling speaks of "the damaged creature ... destroyed by this effect".
  Charisma, Mammoth Harness, Venom and Infinite Authority work the same
  way, as do partner's "the other" (702.124j-m).
- `other than <NP>` names its anchor explicitly.
- `its other types` / `all other abilities` are not object exclusions
  (701.47a, 702.128a).

Corpus: the supported corpus has 16 "any other target" lines (17 regex
hits, minus Spectral Adversary's "that many other target"). 8 anchor on
an earlier target (Bond of Passion's is in an earlier sentence), which in
3 is also the damage dealer. 7 anchor on the source as subject, and 1 on
enchanted creature (Pain for All).

Engine inference (`UD-31`): a generic resolver takes a
same-kind mention in the same ability, earlier (an earlier sentence
included) or later in the same sentence, whose kind and types fit the
head; with none, the source for an object head or "you" for a player
head. A mention fits only if the head could select it: "any target"
can't select a spell or a noncreature Aura (115.4). The thing "other"
describes is never its own anchor.

**Superlatives and ties.** The game has no default for ties; the text
says what to do in one (609.5). The predicate form, "[a/target] creature
with the greatest power among ...", is membership in the tied set, so any
tied member qualifies. Crackling Doom's sacrificing player picks among
creatures tied for greatest power (ruling). Topple's reminder says "If
two or more creatures are tied for greatest power, target any one of
them." As a condition ("draw a card if you control a creature with the
greatest power among creatures on the battlefield"), a tie between your
creature and an opponent's satisfies it (Primal Empathy ruling). A
*definite* superlative that picks an object or player ("the creature with
the least toughness", "the player with the most life") carries its own
tie rule in every corpus line, as 609.5 requires, and those rules differ.
"Or tied for" admits the whole tied set (dethrone, 702.105a; bolster's
indefinite form likewise, 701.39a). "If two or more creatures are tied
..., you choose one of them" picks the object the earlier sentence acts
on, so the choice comes first (Purging Scythe; 608.2c). Other lines say
"the game is a draw", "repeat this process until the tie is broken", or
guard with an intervening if ("if a player has more life than each other
player", Wild Dogs). A definite superlative that only reads a value needs
none ("the opponent with the most cards in hand"). Engine: a superlative
is a `Pred` (argmax membership). A definite superlative compiles to that
`Pred` plus its line's tie rule, never to a bare singular selector.

**Set-level constraints.** Some predicates take the whole declaration set,
not a member: menace's "can't be blocked except by two or more creatures"
(702.111b) is `|S| ≥ 2` over the blocker set — the legality argument is
the set (`deontics.md` §5). The language needs set variables too.

## 3. Binding and anaphora

This section also covers stored per-object slots — it **folds what was
sketched as a standalone object-memory doc**; there is no separate file.

- **"You"/"your"** (109.5): the object's controller, its would-be
  controller while being played/cast/activated, or its owner if it has no
  controller — with per-ability-kind refinements (activator for activated
  abilities; controller-at-trigger-time for triggered ones, except
  delayed triggered abilities, 603.7d-f; for a static ability, the
  current controller of the object it's on, 109.5). The controller
  exceptions are listed in `state.md` §6.
- **"Your team"** (102.4): shorthand for "you and/or your teammates" — the
  player set `{you} ∪ teammates(you)`, "you" bound as above. Teammates
  exist only in a multiplayer game between teams, where a player's
  teammates are the other players on their team and their opponents are
  *all* players not on it (102.3): Team vs. Team, Emperor, Two-Headed
  Giant, Alternating Teams (808.1, 809.1, 810.1, 811.1; glossary "Team"),
  and Archenemy, whose default setup is Team vs. Team with exactly two
  teams, one of them the lone archenemy (904.2, 904.2a; not the
  Supervillain Rumble option, a Free-for-All, 904.12a). In any other game
  "your team" means "you" (102.4): "Dragons your team controls" is
  "Dragons you control". Two consequences. "Opponent" is not "another
  player": a teammate is neither you nor an opponent (102.3); in a
  two-player game the opponent is the other player (102.2), and in
  Free-for-All players compete as individuals (806.1). And as a condition
  the "and/or" is existential: "if your team gained life this turn" holds
  if any player on the team gained life at any point that turn, whatever
  later losses or net team total (Regna, the Redeemer ruling 2018-06-08;
  in 2HG each player gains life individually, 810.9). *Engine inference:*
  one same-team predicate, with every player a singleton team outside
  team games, serves "your team", "teammate", and "opponent". Range of
  influence can cut a teammate out (801.2, 801.5a, 801.11): `variants.md`
  §2.
- **Self-reference**: an object naming itself means *that very object*,
  not name-mates (201.5); a granted ability naming its granter tracks the
  specific source object (201.5a); an ability gained by a differently
  named object reads the old name as the new object (201.5b). A "this
  [quality]" reference, or the anaphoric "that [quality]" of 700.7's own
  example, names that particular object even after it loses the quality.
  A delayed "Destroy that creature" destroys it even if it is no longer a
  creature (700.7). Surface forms (full name, "this ⟨type⟩"): `grammar.md`
  §5.
- **Pronouns**: "it" / "that [noun]" / "those [nouns]" refer back to an
  object or player named earlier in the same ability. The CR has **no
  proximity rule**. Its only instruction is to read the whole text and
  apply the rules of English (608.2c). The antecedent procedure, with its
  worked rulings, is an engine inference (`UD-32`):
  `grammar.md` §5.
- **Bindings vs zone changes**: an object that changes zones becomes a
  new object with no memory of its previous existence — the 400.7 default
  *breaks* bindings. Its exceptions 400.7a–m make "return it to the
  battlefield… it gains haste" work: especially 400.7j, an effect (or the
  spell or ability whose cost moved the object) can find the new object
  it moved to a *public* zone. A delayed trigger's object, no longer in
  the zone it's expected in when the trigger resolves, is not affected;
  if it left and returned it is a new object (603.7c, 400.7). The full
  derivation, including the creating effect's 400.7j binding and the
  Sneak Attack and Angrath rulings, is in `abilities.md` §2 (*Object
  binding*). With no exception and the object merely gone from its
  expected zone, value reads fall back to LKI (608.2h, §5), except that
  information about an illegal target is not determined, so the part that
  needs it doesn't happen (608.2b); contrast "that targets [something]":
  *current* state only, departed targets ignored, no LKI (115.9b). Every
  400.7 exception that lets an effect find a moved object reaches a public
  zone (400.7e, 400.7j, 400.7k; milled cards, 701.17c). An effect that
  moved an object from a public zone to a hidden one reads it by LKI
  (608.2h), and a card discarded into a hidden zone without being
  revealed has undefined characteristics (701.9c). Yet Oracle acts on
  cards an effect has just moved from a library into a hand: "Draw a card
  and reveal it. If it isn't a land card, discard it." Instrument of the
  Bards: "reveal it, and put it into your hand. If that card is
  legendary, ...". 121.6c and 614.11b presuppose "additional actions on a
  card after it's drawn." No rule licenses that tracking; the hidden-zone
  reach of 603.6e and 903.3e is specific to Aura triggers and commanders.
  Engine inference: an effect keeps the cards it moved into a hidden zone
  for its later instructions (`UD-33`).
- **"This way" = agent-identity equality** (`events.md` §3): match exactly
  the logged events whose cause-agent is *this* spell or ability instance.
  That means every event of the named kind that this spell or ability
  caused, including in paying its costs, not only the nearest action:
  Sinister Concierge's "Each card exiled this way" covers both of its
  exiles, and "Sacrifice another creature: ... If an outlaw was sacrificed
  this way" reads the cost. The phrase's other words may narrow it further
  ("exiled from their hand this way"). Corpus: "Creatures destroyed this
  way can't be regenerated." Related: later sentences modify the meaning
  of earlier ones, so read the whole text (608.2c).
- **Stored bindings / object memory.** Linked abilities: the second
  ability refers *only* to what the first did, never to another ability's
  results (607.1). The full slot schema (the 607.2 letters): cards
  exiled-with (607.2a; via replacement, 607.2b; while paying the spell's
  cost, 607.2q; the "exiled with [this]" idiom, 406.6); objects put onto
  the battlefield / created with (607.2c); the chosen [value] (607.2d);
  noted information (607.2e); a chosen rules-meaningless word (607.2f); a
  cost paid as it entered (607.2g); actions taken under a same-paragraph
  static (607.2h, 603.11); whether an additional cost was paid (607.2i)
  and its chosen value (607.2j); champion's exile/return pair (607.2k);
  the chosen anchor word (607.2m; mechanics 614.12c; 607.2m's own "see
  614.12b" is a stale CR cross-reference). Two letters break the strictly
  per-object framing: 607.2n links *across objects by name* (pre-game
  exile read by "cards named [this name]"), and 607.2p's pre-game CDA
  choice *persists across zone changes*, surviving 400.7. Links may also
  span creator and created: a token, emblem, or permanent put onto the
  battlefield by the source's ability (607.1d). Such a link is per
  resolution. Each token refers only to the card exiled by the resolution
  that created it, and all tokens one resolution creates (several, via a
  replacement effect) share that link (Hofri Ghostforge and Timothar,
  Baron of Bats rulings). A copy of the token is not linked. An ability
  the token got from its creator's copy exception is copiable (707.9a), so
  the copy has the text, but that text returns nothing (Hofri ruling). An
  ability the token merely gained is not copied at all (707.2; Timothar
  ruling). **Copy multiplicity** (607.3), for exiled-card slots (607.2a,
  607.2b, 607.2q): if the linked ability exiled multiple cards (usually
  because it was copied), a reference to a single exiled card ("the
  exiled card," "a card exiled with [this object]," or a similar wording
  that refers to a single exiled card) refers to each of them — a variable
  reading it takes the SUM of the answers, actions on "the" card hit each
  card, a token that is a copy of "the" card is created once for each
  exiled card (a copy of each), and "a" card means the ability's
  controller picks one. 607.3 doesn't cover other slot kinds (607.2c
  objects put onto the battlefield, 607.2d chosen values, 607.2e noted
  information); extending it to them would be an engine inference. Slot
  inventory: `state.md` §6; slot queries are ordinary predicates with the
  slot as an extra context coordinate ("Sacrifice a creature of the chosen
  type", corpus). **Hidden slots**: hidden agenda's noted name has two
  separate properties. Visibility: the controller makes the secret choice
  (702.106a-b) and may look at the face-down conspiracy at any time
  (315.7); others may not until it is turned face up (702.106c) or the
  forced reveal when its controller leaves the game or the game ends
  (702.106e). That is the slot's visibility mask (`information.md` §4).
  Reference: the object's "the chosen name" ability refers only to the
  name chosen by that object's own hidden agenda (702.106d, 607.2d). That
  is the linkage.

## 4. Values

**X — the lock point varies by context** (the trio):

| Context | X determined | Rule |
|---|---|---|
| Mana/alternative/additional/activation cost | chosen and announced as part of casting/activating; fixed while on the stack | 107.3a |
| Ward X (and other resolution-evaluated costs) | at resolution of the demanding ability — not locked at trigger | 702.21b |
| Special-action cost (suspend, morph) | immediately before paying | 107.3d |

Refinements: X only in *text* is chosen at stack-put or resolution, as
appropriate (107.3f). Text-*defined* X is computed, not chosen, even when
X also appears in a cost, and it may change while on the stack (107.3c).
{X} in the mana cost of a card off the stack is 0 (107.3g; mana value
likewise, 202.3e). An effect that has a player pay an object's mana cost
reads its {X} as 0 unless the object is a spell on the stack (107.3h).
Another object's {X} reads that object's value (107.3e). **Scope**: all
instances of X on one object normally share one value (107.3i), with
three exceptions. An activated ability's activation-cost X is independent
of the object's other X values and of its other activations (107.3k). An
ability the object *gains* uses the X that ability defines, else 0
(107.3j). An enters-the-battlefield trigger or replacement effect reads
the X chosen for the spell that became the permanent, though the
permanent's own X is 0 (107.3m). A delayed trigger that doesn't define X
inherits the X chosen for its creating spell's or ability's costs
(107.3n). Y follows X's rules (107.3p). Free casting forces X = 0:
`casting.md` (107.3b). Cost-side: `costs.md` §3; the choice record:
`choices.md` §2.

**`*` P/T — two mechanisms** (208.2): either a CDA computing it from a
stated condition — functions in every zone, even outside the game, with
can't-determine → 0 (208.2a; CDA criteria 604.3, 604.3a) — or a
*replacement effect* setting it to one of several listed values as the
creature enters or is turned face up; the choice is copiable, and off the
battlefield such a card's P/T is each considered 0 (208.2b). P/T CDAs
apply in the first layer-7 sublayer (613.4a); every other P/T effect
stacks on top of the computed base.

**Base power/toughness** = P/T after 7a (CDAs) and 7b (setting effects)
only, ignoring modifications and counters (208.4b; 613.4a-b). Layers 1-6
still apply.

**Undefined and missing values — ⊥ and its coercions.** Anything that
needs a number it can't determine uses 0 instead (107.2). P/T *existence*
is separate: a noncreature permanent has no power or toughness at all; a
noncreature object off the battlefield has them only if printed (208.3);
a creature somehow lacking a value for one has 0 (208.5). An *undefined
linked choice* — an ability copied without its linked partner, or with no
choice made for it — differs in kind: that part of the ability does
nothing, a NO-OP rather than a zero (607.5a). *Information about an
illegal target* is likewise not determined, and any part of the effect
that requires it won't happen (608.2b): if either target is illegal as
Soul's Fire resolves, no damage is dealt (ruling). With Soul's Fire alone
a 0 coercion gives the same result (120.8: a source that would deal 0
damage deals none); skip and zero differ for, e.g., an effect that sets
base P/T from a target's value. Engine assumption (UD-6,
`scripts/underdetermined UD-6`): the CR gives only per-case rules, and
the engine models them as one ⊥ with coercions — ⊥→0 numeric (107.2),
⊥→skip-that-part choice (607.5a), ⊥→part-does-not-happen for
illegal-target information (608.2b). The coercions leave out the
cost-position "unpayable" outcome (903.4f); see `underdetermined.md` UD-6.

**Count expressions**: "the number of [desc]", "equal to", and scaling
"for each [desc]" all denote `Count` over a domain (§1's 109.2 defaults);
corpus: "…deals damage equal to the number of creatures you control…".
Timing is *not* uniform (§5): a one-shot effect reads the count once, as
it applies (608.2h); a continuous effect from a resolved spell or ability
locks variables at resolution (611.2d) and separately freezes its affected
set (611.2c); a static's count re-evaluates at all times (611.3a).

**Party: a matching, not a count** (700.8). A party is up to one each of
Cleric, Rogue, Warrior and Wizard the player controls. The game computes
its size, 0-4, and players declare nothing (700.8a). A creature with
several party types fills only one role, counted to get the highest
result (700.8b): a Cleric plus a Cleric Wizard is 2 (Archpriest of Iona
ruling), and a lone Cleric Rogue is 1 (700.8b). A full party is 4
(700.8c). Engine: a maximum matching of the four roles to distinct
creatures (changelings make it a real matching), not a count of distinct
subtypes. Stick Together's *choose a party* is a player choice, not this
computation (700.8d).

**Devotion: counted before most layers** (700.5). Devotion counts the
mana symbols of [color] among the mana costs of permanents the player
controls. "[color 1] and [color 2]" counts each symbol that is either or
both colors once, so a {B/G} hybrid adds 1, not 2 (700.5; a hybrid symbol
is all its colors, 107.4e; Phyrexian symbols are colored, 107.4f).
Devotion, including effects that modify it, is computed after copy,
control and text-changing effects but before any other
characteristic-modifying effect, an exception to 613.10 (700.5a). In its
example, Purphoros's "isn't a creature" type change reads a devotion
fixed before that change applies.

**Arithmetic and rounding**: integers only (107.1). **No global rounding
default** — an effect that could produce a fraction states the direction
itself (107.1a): "loses half their life, *rounded up*" (corpus; "rounded
down" likewise attested). Negatives are used in calculations and
comparisons, but a negative *result* becomes 0 — except effects that
double, triple, or set life or P/T (107.1b). The clamp still applies to a
look-alike pump: Chameleon Colossus at −2/4 activating "gets +X/+X ...,
where X is its power" stays −2/4 (107.1b example). Doubling P/T is a
layer-7c modification, not a set (701.10a, 613.4c). It gives +X/+0 with X
read as the doubling resolves (701.10b), but a negative power gets −X/−0,
X being its distance from 0, so −2 becomes −4 (701.10c). Tripling adds
twice the value, with the same negative branch (701.11b, 701.11c). An
engine that lowers doubling to the generic clamped +X gets negative
doubling wrong; one that exempts every +X from the clamp gets Chameleon
Colossus wrong. Doubling a life total gains or loses life to reach twice
the current value (701.10d). Counters, mana and damage: 701.10e-g (damage
doubling is a replacement effect, 701.10g). "Twice/half" are plain
arithmetic: "…X is twice the number of cards exiled this way" (corpus).

**Division**: targeted division ("divided as you choose among one or two
targets") is announced together with the targets and **each target must
receive at least one** of what's divided (601.2d). *Untargeted* division
is chosen at resolution instead, with the same min-1-per-chosen floor
(608.2d). Retargeting never changes the original division (115.7f).

## 5. Evaluation timing

- **Continuous (statics)**: a static's effect isn't locked in — it applies
  at any moment to whatever its text then indicates (611.3a), at all
  times the source is in the right zone (611.3b); CDAs evaluate in every
  zone (604.3).
- **Locked at announce**: target set and count (601.2c), division
  (601.2d), cost-position X (107.3a). The lock table across all docs:
  `temporal.md` §3.
- **Locked at resolution**: a continuous effect generated by a resolved
  spell or ability fixes any variable once, on resolution (611.2d). A
  *distinct* lock: if it modifies characteristics or changes control, its
  affected set is determined when the effect begins and never changes
  (611.2c) — rule-modifying parts are not frozen this way.
- **Resolution re-checks**: target legality is re-tested (608.2b — source
  gone means LKI; all-illegal means the spell doesn't resolve; partially
  illegal targets are skipped by the parts they're illegal for);
  instructions run in written order (608.2c); resolution choices admit
  only legal options (608.2d), with the empty-library draw carve-out
  (121.3); intervening-if conditions are queried twice — at trigger and
  at resolution (603.4, 608.2a).
- **One-shot reads**: information the game supplies is determined once,
  when the effect is applied (608.2h); a variable in a continuous effect
  that a resolving spell or ability creates is likewise determined once,
  on resolution (611.2d). A reference to a trigger's event participants
  and a fresh description in the same ability read different things.
  Lightmine Field's "deals damage to each of those creatures equal to the
  number of attacking creatures" damages exactly the creatures declared as
  attackers: one since removed from combat is included, and one put onto
  the battlefield attacking is excluded. The amount counts creatures
  attacking as the ability resolves (rulings). Engine: bind "those
  [nouns]" to the event record and evaluate a fresh description's `Count`
  at resolution; never substitute one for the other (608.2h; the binding
  half rests on rulings, since the CR has no general rule binding "those"
  to trigger participants).
- **LKI as query-context substitution**: when a resolving spell or
  ability's effect needs information from a specific object (608.2h),
  including a variable that a continuous effect locks on resolution
  (611.2d), or when an activated or triggered ability needs information
  about its source (113.7a), use the object's last known information if it
  is no longer in the public zone it was expected in, or if the effect
  moved it from a public zone to a hidden zone. Exclusions: static
  abilities never use LKI (604.7); "that targets" checks ignore departed
  targets (115.9b); information about an illegal target is not
  determined, and the part that needs it doesn't happen (608.2b);
  look-back effects read the historical state (608.2i; 603.10 for
  look-back triggers). For a batch of state-based actions the snapshot is
  taken *before* the batch (704.8); the extent of a snapshot is open
  (UD-9, `scripts/underdetermined UD-9`). Duration/window taxonomy:
  `temporal.md`.

## 6. Grammar mapping (surface form → AST)

Surface forms from `grammar.md` §5–6; every example is a real corpus line.

| Surface form | AST node | Corpus example |
|---|---|---|
| `target [desc]` | `Select{target, pred, n, lock:announce}` (115.1) | "Destroy up to X target nonblack creatures…" |
| `any target` | `Select{target, pred:damageable}` (115.4) | "It deals that much damage to any target." |
| `up to N target` | count 0..N (115.6) | "Chandra deals 1 damage to up to one target player or planeswalker." |
| `each [desc]` | `Forall{pred}` | "…deals 1 damage to each other creature with flying." |
| `another/other [desc]` | `pred ∧ Exclude(binding)` (§2) | "Polukranos fights another target creature." |
| `from among [set]` | `Subset{set}` | "You may put a creature card from among them into your hand." |
| `where X is …` | `Let{X ← Value}` (107.3c for spells and activated abilities, 107.3 for other abilities such as triggered ones; computed, not chosen, and may change while on the stack); read per §5 (608.2h, 611.2d, 611.3a) | "…where X is the number of Shrines you control." |
| `the number of` / `for each` | `Count{pred, timing}` — timing per §5: one-shot read / resolution lock / continuous | "[0]: Surveil 2. Then draw a card for each opponent who lost life this turn." |
| `that much` | `ValueRef(antecedent)` | "Remove any number of charge counters from this artifact: It deals that much damage to any target." |
| `twice/half …, rounded up/down` | `Arith` (107.1a) | "…that player loses half their life, rounded up." |
| `divided as you choose among` | `Divide{min:1, lock:announce}` (601.2d) | "[−2]: Ral deals 3 damage divided as you choose among one, two, or three targets." |
| `the chosen [value]` | `SlotRef(607.2d)` | "Sacrifice a creature of the chosen type: …" |
| `exiled with [this]` | `SlotRef(607.2a)` | "Choose a card exiled with this artifact. You may play that card this turn." |
| `[verb]ed this way` | `AgentEq(self)` (events.md §3) | "Creatures destroyed this way can't be regenerated." |

## 7. Engine note — the parser↔engine contract

```
Pred  ::= Char(field, op, Value)        # 109.3 fields, layer outputs (613.4)
        | Char(basePower|baseToughness, op, Value)  # 208.4b: after 7a-7b only
        | Status(cat, val)              # 110.5
        | Zone(z) | Controller(p) | Owner(p) | AttachedTo(x)
        | Targets(mode, …)              # 115.9a–c three modes
        | AgentEq(self) | SlotPred(slot, Pred)
        | Superlative(op, Value, Pred)  # 609.5: argmax membership
        | And | Or | Not | Exclude(binding)
Sel   ::= Target{Pred, count, lock} | Forall{Pred}
        | Subset{set, count} | SetPred{S, Pred(S)}   # menace-style
Value ::= Const(n) | X{lock_point}      # announce | resolution | pre-payment
        | Star(mode)                    # 208.2a CDA | 208.2b enters-replacement
        | Count(Pred, timing)           # §5: one-shot | resolution lock | continuous
        | Party(p)                      # 700.8: maximum matching
        | Devotion(p, colors)           # 700.5, 700.5a
        | Arith(op, Value…, round?)
        | ValueRef(binding) | SlotRef(slot)
        | ⊥                              # coerced: →0 numeric (107.2), →no-op choice (607.5a), →part-does-not-happen for illegal-target information (608.2b)
QueryCtx = {state, event?, bindings, slots(+visibility), lki_snapshots}
```

`grammar.md`'s parser emits these nodes; the engine evaluates them
against a `QueryCtx` whose timing discipline is §5. Consumers embed the
nodes directly: `deontics.md` guards are `Pred` over action instances,
`events.md` trigger conditions are `Pred` over (event, state), `costs.md`
scaling riders are `Value`, `choices.md` option filters are `Pred`, and
`keyword-classification.md`'s composite rows bottom out in these nodes.

## Cross-references

- `grammar.md` §5–6 — the surface forms compiled into §6's AST.
- `events.md` §3, §6 — cause/agent coordinate; (event, state) predicates.
- `deontics.md` — `where ⟨pred⟩` guards; set-level legality (§5 there).
- `costs.md` / `choices.md` — X announcement, division locks, option
  legality filtering.
- `state.md` §5–6 — characteristics vs per-object state; slot inventory.
- `information.md` §4 — visibility masks on hidden slots.
- `temporal.md` — durations, windows, and the cross-doc lock table.
