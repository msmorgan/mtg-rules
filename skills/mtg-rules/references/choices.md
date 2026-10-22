# Choices — Decision Points

*Synthesized from the Comprehensive Rules effective 2026-09-25
(`data/rules/cr.json`).*

Every place the game stops and asks a player something. The CR never defines
"decision" as a first-class object — there is no glossary entry for "choose";
choices are introduced rule-by-rule (announce a mode here, declare attackers
there). This doc is the unified inventory: who decides, what the options are,
when the choice locks, and who can see it. The engine record at §6 is the
UI/AI boundary.

## 1. The decider-resolution layer

Every decision has a **nominal decider** (the player a rule or ability names)
and an **actual decider** (whoever the resolved authority is after
delegation). `generalizations.md` §9 (Family 9, decision-authority
delegation) develops this; the resolution steps:

- **Default attribution.** Most rules name the decider directly: the spell's
  controller announces modes and targets (601.2b–c), the active player
  declares attackers (508.1a), the defending player declares blockers
  (509.1a). For replacement-effect ordering, the decider is the **affected**
  object's controller (or owner if uncontrolled) or the affected player
  (616.1) — not the effects' controllers.
- **Simultaneous deciders → APNAP.** If multiple players would choose at
  once, the active player chooses first, then each nonactive player in turn
  order; then the actions happen simultaneously (101.4). Later players know
  earlier players' choices (101.4b), except hidden-zone picks may stay
  concealed (101.4a). One player's multiple simultaneous choices happen in
  the specified order, or an order that player picks (101.4c). A choice that
  spawns a new choice for an earlier player restarts APNAP for everything
  outstanding (101.4d).
- **Textual delegation.** Some spells have an opponent make a casting choice
  the controller normally would (mode, targets); the opponent does so when
  the controller normally would (601.7). With several eligible opponents,
  the controller picks which one chooses (601.7a); controller-then-opponent
  ordering is an explicit exception to 101.4 (601.7b). Modes of spells *and
  abilities* (including triggered) may be chosen by another player, at the
  time the controller normally would; with several eligible players the
  controller picks (700.2e). Smaller examples:
  discard normally lets the affected player pick the card, but effects can
  require random discard or let another player choose (701.9b); copy effects
  may let the copy's controller choose new targets (707.10c).
- **Role rebinding.** A battle's protector, not its controller, is the
  "defending player" for every rule and effect about attacks on that battle
  (310.9d) — a whole decision *class* re-rooted to another player.
- **Keyword rebinding.** Banding swaps the damage-division decider. For an
  attacking creature blocked by a creature with banding (or by a qualifying
  "bands with other" pair), the defending player divides its damage
  (702.22j). For a blocking creature that blocks a creature with banding (or
  such a pair), the active player divides its damage (702.22k). Both are
  exceptions to 510.1c-d.
- **Whole-player control.** While controlling another player, you make all
  choices and decisions that player is allowed or required to make by rules
  or objects (723.5) — but only those: no choices outside the game, none
  called for by tournament rules (723.5b).
- **Constraint-flavored delegation.** Goad never moves the decider; it adds
  requirements to the attack declaration (701.15b) that the 508.1d solver
  enforces (§5).

Engine: route every prompt through
`decide(kind, nominal_decider) → actual_decider + constraints`.

## 2. Decision kinds and lock stages

| Kind | Decider (nominal) | Lock stage | Rules |
|---|---|---|---|
| Mode(s) of a spell or activated ability | Controller | Announce | 601.2b, 602.2b, 700.2a |
| Splice; alternative/additional-cost intentions; X; hybrid/Phyrexian payment | Controller | Announce | 601.2b |
| Targets (incl. how many, if variable) | Controller | Announce | 601.2c |
| Division/distribution among targets | Controller | Announce | 601.2d |
| Modes/targets/division of a triggered ability | Controller | Put on stack | 603.3c–d, 700.2b |
| Resolution-stage choices ("may", chosen-on-resolution options, untargeted division) | Player the effect names | Resolution | 608.2d |
| Vote | Each player, in turn order from a specified player | Resolution | 701.38a |
| Search: which matching cards to find | Searching player; simultaneous searchers look at once, then decide in APNAP order | Resolution | 701.23a, 701.23i |
| Attack declaration (set + what each attacks) | Active player | Declare attackers | 508.1a-b, 508.1e, 508.1g |
| Block declaration (set + what each blocks) | Defending player | Declare blockers | 509.1a |
| Combat damage assignment | Each combatant's controller, APNAP (defending/active player swap under banding, 702.22j-k) | Combat damage step start | 703.4k, 510.1 |
| Order own simultaneous triggers onto stack (two APNAP passes) | Each controller, APNAP | Put on stack | 603.3b |
| Order of replacement/prevention effects | Affected object's controller / affected player | Per application | 616.1 |
| Fixed-window yes/no ("sacrifice unless you pay…") | Named player | Resolution of the trigger | 608.2d, 118.12a |
| First-turn choice; mulligans; companion reveal; opening-hand actions; sticker sheets (limited: the player chooses up to three; constructed: three at random, an RNG pick per §4); conspiracy cards to the command zone; shuffling or cutting opponents' decks | Per pre-game rule | Pre-game | 103.1, 103.5, 103.5b, 103.2b, 103.2d, 103.2e, 103.3, 103.6 |
| Mulligan bottoming (which N cards + order) | Mulliganing player | Pre-game (concealed) | 103.5 |
| Special actions (play land, turn morph face up, companion to hand…) | Player with priority | On taking the action | 116.1–116.2, 702.37e, 116.2g |
| Priority: act or pass | Player with priority | Each priority window | 117.3d |
| Legend rule / sector / battle protector / commander to command zone | Controller, affected player, or owner (903.9a) | SBA check | 704.5j, 704.5u, 704.5x-y, 903.9a |
| Turn-based non-declaration choices (untap determination, defending-player choice, cleanup discard) | Active player | Turn-based action | 703.4c, 502.3, 703.4h, 507.1, 703.4n, 514.1 |
| As-enters choices (replacement-effect choices, battle protector, enters-attacking/blocking, commander replacement) | Entering permanent's controller | Before the permanent enters | 614.12a-b, 310.9a, 310.12a, 508.4, 509.4, 903.9b |

Notes:

- **Casting choices lock at announcement.** Modes, costs, X, targets, and
  division are all announced during 601.2b–d; legality is then checked, and
  an illegal proposal rewinds wholesale (601.2e → 733.1). The total cost
  locks at 601.2f. After a spell is legally cast, its targets change only if
  an effect changes them — never by the player re-deciding. An X defined by
  a later choice in the spell's text is made at announcement instead
  (601.2b). The order of cost reductions is the caster's choice at 601.2f.
- **Mode choices.** Each bulleted option is a mode (700.2). A player
  choosing several can't choose the same mode twice unless the spell or
  ability permits it ("You may choose the same mode more than once"; 700.2d).
  A mode chosen that way is treated as appearing that many times in
  sequence, and each instance may take the same target or a different one
  (700.2d). Engine inference: identify modes by list position, not text.
  700.2 makes each option a mode, so two options with identical text are
  two modes, and 700.2d doesn't bar choosing both. Targets that only a mode
  names are chosen only with that mode (700.2c; branch targets below). A
  cost printed before a mode is an additional cost paid if that mode is
  chosen (700.2h; spree, 702.172a). Modes lock harder than targets:
  changing a target can't change the mode (700.2f), and a copy keeps the
  original's modes even when its controller may choose new targets (700.2g,
  707.10c). A player other than the controller may be named to choose the
  mode, doing so when the controller would (700.2e; §1).
- **Triggered abilities mirror casting**: modes when the ability is put on
  the stack (700.2b, 603.3c), then targets/division per 601.2c–d (603.3d).
  Trigger ordering is two APNAP passes. First, every player in APNAP order
  orders their triggers whose trigger condition isn't another ability
  triggering. Then every player in APNAP order orders the rest (603.3b).
- **Targets inside resolution-time branches still lock at announcement.**
  Whether a target is required is settled at announcement: by a chosen
  alternative or additional cost or mode (601.2c, 700.2c), or by a
  variable count such as "up to one" (601.2c). It is never settled by a
  resolution-time branch. "You may" and an "unless" payment are choices
  made while the effect is applied (608.2d), and "if you do" and
  "otherwise" are conditions read as the instructions are followed in
  order (608.2c). Either way, every target the spell or ability itself
  names in those branches is announced when the spell is cast or the
  ability is activated or put on the stack (115.1, 601.2c, 602.2b,
  603.3d). The rulings for Daretti, Ingenious Iconoclast, Insatiable
  Appetite and Stingerfling Spider all choose the target then and the
  sacrifice or "may" on resolution. Consequences: becomes-the-target
  triggers such as ward (702.21a) trigger at announcement whether or not
  the branch later happens (601.2c). The "may" doesn't excuse a missing
  target: with no legal choice the cast or activation is illegal (601.2e,
  602.2b) and a triggered ability is removed from the stack (603.3d). If
  every target is illegal on resolution, the spell or ability doesn't
  resolve and the branch's choice is never offered (608.2b; Insatiable
  Appetite: "You won't sacrifice a Food"). The condition and any
  "otherwise" arm read the announced target ("If you do, target creature
  gets +5/+5 … Otherwise, that creature gets +3/+3"). Contrast a
  triggered ability that a branch creates, such as the reflexive "When
  you do, …" (603.12) or a delayed trigger (603.7): it is created
  mid-resolution, and its targets are chosen when it is put on the stack
  (603.3d). The original ability "goes on the stack without a target"
  (Heart-Piercer Manticore ruling).
- **Resolution choices** are announced *while applying* the effect, and an
  illegal or impossible option can't be picked (608.2d).
- **Votes are keyed to the word "vote."** To vote, each player chooses one
  listed option, starting with a specified player and proceeding in turn
  order (701.38a). That player needn't be the active player, so this order
  isn't APNAP (contrast 101.4). Options may be objects, rules-meaningless
  words each tied to an effect, or other variables (701.38b). Text that
  refers to voting ("Whenever players finish voting", "While voting, you
  get an additional vote") sees only an actual vote, never a group decision
  made without the word "vote" (701.38c). Menacing Ogre's "each player
  secretly chooses a number" is not a vote. A secret council's "secretly
  votes" is a vote, and it stays committed-hidden until revealed (§3). A
  player's extra votes all happen when that player would otherwise have
  voted (701.38d). Engine: vote is its own Decision kind (§6), never
  inferred from the shape of a group choice.
- **Declaration sets are constraint-solved, not free** (§5): the chosen set
  must maximize requirements obeyed without violating restrictions
  (508.1d, 509.1c). Damage assignment is checked as a *total* assignment;
  an illegal one rewinds the whole assignment (510.1e).
- **SBA, turn-based and as-enters choices.** SBA choices are made by the
  player each rule names; when several players choose at once they use
  APNAP (101.4), except that 704.5u has controllers without a space
  sculptor choose first. As-enters choices are made before the permanent
  enters (614.12a). An effect that merely states a creature "is attacking"
  (the second branch of 508.4) is chosen at resolution, not as-enters.
- **Pay-or-else upkeep triggers** (corpus template: "At the beginning of
  your upkeep, sacrifice this artifact unless you pay {1}") are
  resolution-stage choices: "X unless you pay C" means "you may pay C; if
  you don't, X" (118.12a), and C *is* a cost paid during resolution
  (118.12), so 118.3's payability rules apply (608.2d: a player who can't
  pay can't choose that option). It is not a cost of casting or activating
  anything; that is `deontics.md`'s toll split (`costs.md` §1).
- **Pre-game**: the determined player chooses who takes the first turn
  (103.1); companion is revealed pre-game (103.2b, 702.139a) but joins the
  hand via an in-game special action (116.2g); mulligan keep/take decisions
  run starting-player-first with all mulligans taken simultaneously (103.5);
  opening-hand actions (Leyline-style) follow in turn order (103.6).
  Simultaneous starting-game choices use APNAP with the starting player as
  active player (101.4e); 103.1's choice precedes that, and 103.5/103.6
  (team variants 103.5d/103.6c) fix their own order.
- **London bottoming**: taking a mulligan includes putting a number of the
  drawn cards equal to mulligans taken on the bottom of the library, the
  player choosing which cards and in what order (103.5) — opponents never
  see the picks. Multiplayer/Brawl: the first mulligan doesn't count toward
  that number (103.5c).

## 3. Visibility classes

Cross-ref `information.md` for the zone/visibility model; here, only what a
*choice* can look like to other players:

- **Open** — the default. Choices are made publicly and later deciders see
  earlier choices (101.4b).
- **Committed-hidden** — chosen, binding, concealed. The morph identity: the
  face-down spell/permanent has only the 2/2 no-name characteristics
  (702.37a, 702.37c, 708.2), only its controller may look at it (708.5), yet
  which card it is was fixed at cast. Hidden agenda: turn the conspiracy
  face down and secretly choose a card name, noted in writing (702.106a–b).
  Corpus: "secretly choose" text overrides 101.4b's knowledge of prior
  choices (101.1); the CR operationalizes secrecy only for hidden agenda
  (702.106b). Two shapes occur. One is single-player hidden commitment with
  no reveal instruction (Ominous Lockbox), which is committed-hidden like
  hidden agenda. The other is multi-player commitment whose text then
  reveals the choices; official guidance there is to write the choice down
  and reveal simultaneously (`scripts/rulings "Wheel of Misfortune"`,
  `"Mob Verdict"`; Prisoner's Dilemma: choices are made during resolution).
  APNAP hidden-zone picks may stay face down but must be clearly indicated
  (101.4a) — committed without being disclosed.
  London-mulligan bottoming (§2) is committed-hidden too: which cards went
  to the library bottom, and in what order, binds the player but is never
  disclosed (103.5) — and unlike morph, it carries no audit duty.
- **Revealed-later verification duty** — commitments must be auditable: a
  face-down permanent leaving the battlefield (or face-down spell leaving
  the stack for anywhere but the battlefield, or its owner leaving the game,
  or the game ending) must be revealed to all players (708.9).

Engine: committed-hidden choices need a payload visible to a player subset
plus an audit obligation that fires on zone-change/game-end events.

## 4. Randomness as pseudo-decider

The game treats random processes as deciders that consume no information:

- **Coin flip** (705): any two-outcome equal-likelihood method players agree
  on (705.1); win/lose flips exist only when the flipper calls it — only the
  flipper wins or loses the flip (705.2).
- **Die roll** (706): a dN has N equally likely outcomes numbered 1 to N
  (706.1a); the natural result plus modifiers gives the result (706.2).
  Note the choice *re-entry*: modifiers may be optional or carry costs
  (706.2a), and if multiple effects would modify the result, the roller
  chooses which to apply, in stages — reroll effects are considered first,
  then increase/decrease-by-N modifiers (706.2b) — randomness output feeds
  back into player decisions. The roll, same-paragraph modifiers,
  result-contingent instructions and any results table are one ability
  (706.3b), so no player gets to respond between the result and its
  effect (Berserker's Frenzy ruling). A results table's "Roll again" uses
  the same kind and number of dice, with the applicable modifiers (706.3c).
- **Overridden outputs — a break in the abstraction.** Effects can rewrite
  what the RNG said: an effect may fix a flip's result or winner, ignoring
  the actual flip (705.3), and an ignored die roll is considered to have
  never happened — nothing triggers from it, no effects apply to it
  (706.6). Ignoring is another re-entry: a player told to ignore the
  lowest roll, with several rolls tied for lowest, chooses which one is
  ignored (706.6). Unlike a player's locked choice, the pseudo-decider's
  output is revisable after the fact.
- **The planar die has no numerical result.** It is six-sided, with one
  Planeswalker face, one chaos face and four blanks (901.3a), but it is not
  the numbered dN of 706.1a. Rolling it triggers abilities that trigger
  whenever a player rolls one or more dice, yet every effect that refers
  to a numerical result of a die roll, including exchanges and
  comparisons, ignores it (706.7, 901.9d). Engine: emit a roll event with
  no result value, so result readers and modifiers never see it.
- **Random discard** — the rules explicitly contrast it with the default
  affected-player-chooses discard (701.9b): same decision kind, decider
  swapped to RNG.
- **Random mode** ("choose one at random": Cult of Skaro; Outlaws'
  Merriment; Umaro, Raging Yeti) is drawn at the ordinary mode-choice
  point, as the ability is put on the stack (700.2b), so players respond
  knowing the result (Outlaws' Merriment [2019-10-04]; Umaro
  [2025-06-06]). The draw is over legal modes only (700.2a-b), since a
  mode with no legal target "can't be chosen at random", and it happens
  before targets are chosen (Summon: Magus Sisters [2025-06-06]). For the
  distribution, see `underdetermined.md` UD-8.
- **Shuffle** — randomization such that *no player* knows the order
  (701.24a): a decider nobody is, producing state nobody saw. This is why
  most library actions can't be rewound (733.1; library→stack is the
  exception — see §5; `information.md`).
- **Payment ordering**: costs that don't involve random elements or moving
  objects from the library to a public zone are paid first, in any order;
  then all remaining costs, in any order (601.2h) — the rules sequence
  deterministic choices ahead of unpredictable reveals so the chooser
  can't condition on them.

Engine: RNG implements the decider interface with an empty information set;
seedable for replay (engine inference: seeds must stay unknowable to players
during the game to satisfy 701.24a; see UD-8). 706.2b-style follow-ups are
ordinary decisions whose options depend on the RNG event.

## 5. Constraint arbitration

What happens when choices are constrained, impossible, or illegal.
Cross-ref `deontics.md` §4 (the obligation solver) — this section is the
choice-side view.

- **Requirement maximization.** Attack and block declarations must obey the
  maximum possible number of requirements without disobeying any
  restriction (508.1d, 509.1c) — a constraint-satisfaction problem, not a
  veto. A cost-gated requirement never forces the payment (508.1d). Target
  choices obey the same scheme: maximize must-be-chosen effects without
  violating can't-be-targeted ones (601.2c).
- **Illegal options are unpickable, not pickable-then-punished.** A mode
  that would be illegal can't be chosen (700.2a–b); a resolution option
  that's illegal or impossible can't be chosen (608.2d). Two carve-outs:
  an empty library doesn't make drawing a card an impossible action
  (608.2d, 121.3) — you may choose to draw from nothing; and a player may
  choose to search even when the follow-up actions are illegal or
  impossible (701.23g).
- **No legal choice → the decision's carrier evaporates.** A modal triggered
  ability with no chosen mode is removed from the stack (603.3c); a
  triggered ability with a required choice and no legal choices is removed
  from the stack (603.3d).
- **Mode history is an object's memory, defined by rulings, not the CR.**
  "Choose one that hasn't been chosen [this turn] —" (Gandalf the Grey;
  Demonic Pact; Galadriel, Light of Valinor; Kargan Intimidator) filters
  the modes against a history that no CR rule defines: 700.2d bars repeats
  only within one choice. Rulings fix the record. It belongs to that
  specific object, so a second copy keeps its own (Demonic Pact
  [2015-06-22]; Kargan Intimidator [2020-09-25]). It is forgotten when the
  object changes zones, since it is then a new object (Gandalf the Grey
  [2023-06-16]; 400.7). It ignores who chose, so a new controller is
  bound by earlier choices (Demonic Pact; Gandalf the Grey). It is
  written when the mode is chosen, as the ability is activated or put on
  the stack (700.2a-b), not when it resolves. A countered instance still
  counts (Gandalf the Grey), and simultaneous instances must choose
  different modes (Gala Greeters [2022-04-29]; Galadriel). With every mode
  used, no mode can be chosen and the ability is removed from the stack
  (603.3c; Captive Audience [2019-01-25]). INFERENCE: carrying these
  rulings over to cards that have none.
- **Illegal proposal → rewind.** An illegally cast spell rewinds to before
  the proposal (601.2e); the general rule reverses the entire action and
  cancels payments — but not actions that moved cards to a library, moved
  cards from a library to any zone *other than the stack*, shuffled, or
  revealed library cards (733.1). Library→stack is reversible: a spell
  cast from the library rewinds fine. An illegal total damage assignment
  rewinds the assignment (510.1e).
- **"Do as much as possible" is for effects, not choosers.** If an *effect*
  attempts something impossible, it does as much as possible (609.3);
  impossible instruction parts are ignored (101.3). That governs the game
  executing an outcome — a player facing options never picks an impossible
  one (608.2d above). Don't model partial compliance as a choice.
  **Exception: searches.** Searching a hidden zone for cards with a stated
  quality lets the searcher find fewer than are present (701.23b), so the
  found set is a choice; see the search bullet below.
- **Search find-obligations depend on zone and wording.** To search is to
  look at every card in the zone, hidden or not, and find matches
  (701.23a). How many must be found, in full:
  - **Hidden zone, stated quality** ("a creature card", "all cards with
    that name"): finding some or all is optional even with matches present
    (701.23b), even when a number is stated (Boreas Charger ruling: "You
    can find fewer Plains cards than the difference"). Library and hand
    stay hidden even when every card in them is revealed (400.2).
  - **Hidden zone, bare quantity** ("a card", "three cards"): find that
    many, or as many as the zone holds (701.23d).
  - **Hidden zone, undefined quality** (e.g., the name of a card that was
    never chosen): search, but find nothing (701.23c).
  - **Public zone** (graveyard; 400.2): 701.23b-d don't apply, so the
    wording governs. "All cards with the same name" must find every match
    there (701.23b's example: "Splinter's controller must find the Howling
    Mine in the graveyard"; Splinter and Eradicate rulings: "The copies
    must be found if they are in publicly viewable zones").
  - **Outside the game**: the player may choose an appropriate card they
    own (701.23j).

  The quantity word can waive the find in any zone: "any number" includes
  zero (107.1c), so Memoricide may leave copies in the graveyard (its
  ruling). Found cards aren't revealed unless the effect says so
  (701.23e). A player offered "search and [act]" may search even if the
  act is illegal or impossible (701.23g). Engine: compute the find's lower
  bound per zone from (visibility, quantity word, stated or bare quality),
  not from the quantity alone.

## 6. Engine note

```
Decision{
  kind,                      # mode | target | division | declaration-set |
                             # ordering | yes-no | vote | search-find | pre-game | special-action …
  nominal_decider -> actual, # §1 resolution: delegation, rebinding, 723-control
  options(state),            # legal options only (700.2a, 608.2d), except: "choose new
                             # targets" may keep illegal targets unchanged (115.7d,
                             # 707.10c); empty-library draws (121.3); searches with
                             # impossible follow-ups (701.23g)
  constraints,               # requirements/restrictions fed to the 508.1d-style solver
  lock_stage,                # announce | put-on-stack | declaration | resolution |
                             # pre-game | as-enters | sba | tba | priority
                             # (tba = turn-based actions other than the 703.4i-k
                             # declarations, which are `declaration`)
  visibility,                # open | committed-hidden(payload, audit-duty) | rng
  rng?,                      # present iff the decider is the RNG pseudo-player
}
```

The UI/AI boundary is exactly this record: a human client, an AI, and the
RNG all implement "given options and constraints, return a selection."
Replays serialize the selections; 733.1's library carve-out marks which
selections are irreversible.

## Cross-references

- `generalizations.md` §9 — Family 9 (decision-authority delegation); the
  decider-resolution layer here is its engine directive.
- `deontics.md` §4–5 — the obligation solver and modal evaluation that prune
  the option set before a Decision is ever presented; toll split for
  pay-or-else triggers.
- `costs.md` — cost-attached choices (alternative/additional intentions,
  Phyrexian, X) and the resolution-toll position: the unless-payment is a
  cost paid at resolution (118.12, 118.12a), not a cost of the original
  action (§1).
- `events.md` — choices consume events (trigger conditions) and emit them
  (declarations, payments); ordering decisions batch per 603.3b.
- `information.md` — the visibility machinery behind §3 (face-down model,
  reveal operations, per-player information sets).
- `state.md` §2 — player state the deciders read; `casting.md` — the full
  601.2 announcement pipeline these lock stages live in.
