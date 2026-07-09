# Choices — Decision Points

*Synthesized from the Comprehensive Rules effective 2026-06-19
(`data/rules/cr.json`). Orientation only — verify load-bearing specifics
with `scripts/rule` before citing. Run `scripts/cite check` after CR
refreshes.*

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
  ordering is an explicit exception to 101.4 (601.7b). Smaller examples:
  discard normally lets the affected player pick the card, but effects can
  require random discard or let another player choose (701.9b); copy effects
  may let the copy's controller choose new targets (707.10c).
- **Role rebinding.** A battle's protector, not its controller, is the
  "defending player" for every rule and effect about attacks on that battle
  (310.8d) — a whole decision *class* re-rooted to another player.
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
| Attack declaration (set + what each attacks) | Active player | Declare attackers | 508.1a |
| Block declaration (set + what each blocks) | Defending player | Declare blockers | 509.1a |
| Combat damage assignment | Each combatant's controller, APNAP | Combat damage step start | 703.4k, 510.1 |
| Order own simultaneous triggers onto stack | Each controller, APNAP | Put on stack | 603.3b |
| Order of replacement/prevention effects | Affected object's controller / affected player | Per application | 616.1 |
| Fixed-window yes/no ("sacrifice unless you pay…") | Named player | Resolution of the trigger | 608.2d |
| First-turn choice; mulligans; companion reveal; opening-hand actions | Per pre-game rule | Pre-game | 103.1, 103.5, 103.2b, 103.6 |
| Mulligan bottoming (which N cards + order) | Mulliganing player | Pre-game (concealed) | 103.5 |
| Special actions (play land, turn morph face up, companion to hand…) | Player with priority | On taking the action | 116.1–116.2, 702.37e, 116.2g |

Notes:

- **Casting choices lock at announcement.** Modes, costs, X, targets, and
  division are all announced during 601.2b–d; legality is then checked, and
  an illegal proposal rewinds wholesale (601.2e → 733.1). The total cost
  locks at 601.2f. After a spell is legally cast, its targets change only if
  an effect changes them — never by the player re-deciding.
- **Triggered abilities mirror casting**: modes when the ability is put on
  the stack (700.2b, 603.3c), then targets/division per 601.2c–d (603.3d).
- **Resolution choices** are announced *while applying* the effect, and an
  illegal or impossible option can't be picked (608.2d).
- **Declaration sets are constraint-solved, not free** (§5): the chosen set
  must maximize requirements obeyed without violating restrictions
  (508.1d, 509.1c). Damage assignment is checked as a *total* assignment;
  an illegal one rewinds the whole assignment (510.1e).
- **Pay-or-else upkeep triggers** (corpus template: "At the beginning of
  your upkeep, sacrifice this artifact unless you pay {1}") are ordinary
  resolution-stage yes/no choices under 608.2d — the payment is a choice
  inside an effect, not a cost (`costs.md`; `deontics.md` toll split).
- **Pre-game**: the determined player chooses who takes the first turn
  (103.1); companion is revealed pre-game (103.2b, 702.139a) but joins the
  hand via an in-game special action (116.2g); mulligan keep/take decisions
  run starting-player-first with all mulligans taken simultaneously (103.5);
  opening-hand actions (Leyline-style) follow in turn order (103.6).
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
  Corpus: "secretly choose" cards (Prisoner's Dilemma-style simultaneous
  commitment, then reveal). APNAP hidden-zone picks may stay face down but
  must be clearly indicated (101.4a) — committed without being disclosed.
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
- **Die roll** (706): N equally likely outcomes (706.1); the natural result
  plus modifiers gives the result (706.2). Note the choice *re-entry*:
  if multiple effects would modify the result, the roller chooses which to
  apply, in stages — reroll effects are considered first, then
  increase/decrease-by-N modifiers (706.2b) — randomness output feeds back
  into player decisions.
- **Overridden outputs — a break in the abstraction.** Effects can rewrite
  what the RNG said: an effect may fix a flip's result or winner, ignoring
  the actual flip (705.3), and an ignored die roll is considered to have
  never happened — nothing triggers from it, no effects apply to it
  (706.6). Unlike a player's locked choice, the pseudo-decider's output is
  revisable after the fact.
- **Random discard** — the rules explicitly contrast it with the default
  affected-player-chooses discard (701.9b): same decision kind, decider
  swapped to RNG.
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
seedable for replay. 706.2b-style follow-ups are ordinary decisions whose
options depend on the RNG event.

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
  that's illegal or impossible can't be chosen (608.2d). One carve-out:
  an empty library doesn't make drawing a card an impossible action
  (608.2d, 121.3) — you may choose to draw from nothing.
- **No legal choice → the decision's carrier evaporates.** A modal triggered
  ability with no chosen mode is removed from the stack (603.3c); a
  triggered ability with a required choice and no legal choices is removed
  from the stack (603.3d).
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

## 6. Engine note

```
Decision{
  kind,                      # mode | target | division | declaration-set |
                             # ordering | yes-no | vote | pre-game | special-action …
  nominal_decider -> actual, # §1 resolution: delegation, rebinding, 723-control
  options(state),            # legal options only (700.2a, 608.2d filter first)
  constraints,               # requirements/restrictions fed to the 508.1d-style solver
  lock_stage,                # announce | put-on-stack | declaration | resolution | pre-game
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
  Phyrexian, X) and why resolution tolls aren't costs.
- `events.md` — choices consume events (trigger conditions) and emit them
  (declarations, payments); ordering decisions batch per 603.3b.
- `information.md` — the visibility machinery behind §3 (face-down model,
  reveal operations, per-player information sets).
- `state.md` §2 — player state the deciders read; `casting.md` — the full
  601.2 announcement pipeline these lock stages live in.
