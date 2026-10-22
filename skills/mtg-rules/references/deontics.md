# Deontic Layer — May / Can't / Must / Gate / Toll Algebra

*Synthesized from the Comprehensive Rules effective 2026-09-25
(`data/rules/cr.json`).*

The CR scatters *capability* across keywords, combat steps, casting rules,
and continuous effects, but they all answer one question: **is this player
allowed to take this action right now?** This doc is the single algebra over
that question. It merges what `generalizations.md` splits into Family 1
(cast/play permission), Family 3 (timing permission), Family 6
(targeting/interaction permission), and Family 9 (combat-requirement
delegation) — they are one deontic system on one carrier.

## 1. Action instances

The carrier is an **action instance** — a proposed game action with:

- **verb** — Cast, Play, Activate, Attack, Block, Target, Crew,
  Pay-as-cost, …
- **subject** — the actor (a player; for combat, the declaring player).
- **object** — what is acted on (the spell, the creature, the target).
- **params** — declaration-set members, chosen X, alternative/additional
  costs, chosen targets.
- **window** — when it is being proposed (priority phase, a declare step,
  the resolution of a spell).

The action is **incomplete** while choices remain open; legality is judged
over the *completions* (see §5).

## 2. Four polarities

Every deontic clause is one of four predicate kinds over action instances.

| polarity | meaning | standing defaults | granted/imposed by |
|---|---|---|---|
| **May**(a) | a is permitted | cast: 117.1a (plus the per-type hand-zone rules 301.1–310.1, generalizations.md Family 1); activate: 117.1b (117.1d for mana abilities); special actions: 117.1c; attack: 508.1a; block: 509.1a | keyword/effect rows ("may play this as though…", flash 702.8a) |
| **Cant**(a) | a is forbidden | — (none; absence of Cant) | 508.1c attack-restrictions, 509.1b block-restrictions, "can't be…", "can't cast … unless [condition]" (601.3) |
| **Must**(a) | a is required if able | — | "attacks if able" 508.1d, "blocks if able" 509.1c, "must be blocked if able" (509.1c; one blocker suffices, Gaea's Protector ruling), goad 701.15b, provoke (702.39a), "must be chosen as a target" (601.2c; Oracle form "must choose … if able", e.g. Flagbearer) |
| **Gate**(a, cost) — the declaration-gating MayIf flavor | a is legal *only if* the price is paid at declaration | — | "can't attack/block unless … pays" (508.1c / 509.1b; price locked in and paid by 508.1h–j / 509.1d–f; never compulsory, 508.1d / 509.1c) |
| **Toll**(a, cost) — the resolution-stage MayIf flavor | a is *fully legal*; a later trigger/resolution punishes unless the price is paid | — | ward 702.21a, Mana-Leak-style "counter … unless its controller pays {N}" |

**May** is the existential floor: an action with *no* matching permission
row is illegal. Casting needs a permission and no prohibition (601.3); the
seven hand-zone play rules, 117.1a–c, and every "cast from" keyword are
permission rows in one table (generalizations.md Family 1).

**Cant** is pure subtraction. **Must** is satisfied-if-able and arbitrated
by the maximize-without-violating solver (§4). **MayIf** splits in two by
*when* the price bites; the flavors are named **Gate** and **Toll**. A
**Gate** (declaration-gating) is conditional *legality*: "can't attack/block
unless a player pays a cost" makes the declaration illegal unless paid — yet
the actor is never *required* to pay, even to satisfy a requirement (508.1d /
509.1c state this explicitly). "Can't cast … unless [condition]" is not a
priced Gate: it is a conditional **Cant** (601.3), true or false of the
proposal. An optional "as … attacks" cost (508.1g) is neither Gate nor Toll.
A **Toll** (resolution-stage) leaves the
action fully legal: ward (702.21a) and Mana-Leak-style "counter … unless …
pays {N}" let the spell be cast / the target be chosen normally, then a
*trigger or the resolving counter* punishes (counters it) unless the price
is paid. §8's ward row is a Toll; don't model it as a Gate on casting.

## 3. Modifiers

Two operators take a polarity clause and return a refined one.

- **Only** — refines a permission by *intersection*: replaces "may, in
  window W" with "may, only in window W′ ⊆ W" (or only by predicate P).
  "Activate only as a sorcery" (602.5d, 307.5) / "only as an instant" (602.5e)
  swaps the activation window for the sorcery/instant timing window —
  *without* requiring the player to actually hold such a card. "Only during
  your turn", "only once each turn" (602.5b) stack as further window
  intersections. "Cast only before/after [a point in combat]" is a window
  intersection too: 506.8 and 506.8a–f fix the combat points ("attackers are
  declared," "blockers are declared," "the combat damage step," and so on),
  and 506.8g extends them to activated abilities. Effects that preclude
  casting sorcery spells don't affect an "only as a sorcery" restriction
  (307.5; the exception is actually casting a sorcery spell). On the blocker
  side, "can only be blocked by X" is written in Oracle as the **Cant**-except
  form (§8, §9), not as an Only, and "can block only creatures with flying"
  is a blocker-side restriction of the **Cant** form (§9).

- **AsThough** — installs a *scoped counterfactual premise*: "treat the game
  exactly as if [condition] were true, **for purposes of that effect only**;
  for all other purposes treat the game normally" (609.4). Two AsThough
  effects whose conditions chain both apply (609.4a). A payment-flavored
  AsThough ("spend mana as though it were any color") changes only *how* a
  cost may be paid, not the cost itself nor what was actually spent (609.4b).

## 4. Conflict law and the obligation solver

**Cant beats May (101.2):** "When a rule or effect allows or directs
something to happen, and another effect states that it can't happen, the
'can't' effect takes precedence." So legality is **allow-minus-prohibit**:
a completion is legal iff some **May** matches it *and* no **Cant** forbids
it. (101.2a carves out ability add/remove — that is the layer system, not
this conflict rule.)

*Scope of 101.2.* 101.2 arbitrates **effect vs effect**: the allowing side may
be a rule *or* an effect, but the prohibiting side that wins must be an
**effect**. Rule-level restrictions are *not* subtracted by 101.2 — they are
subtracted by the rules that state them. The rule-level combat restrictions
are 508.1a (attack) and 509.1a (block; 802.4a in multiplayer), while the
effect restrictions are 508.1c (attack) and 509.1b (block). The casting gate
(601.3, "only if … allows … and no … rule or effect prohibits") and the
activation begin-gate (602.5, "A player can't begin to activate an ability
that's prohibited from being activated") each fold their own prohibitions
into legality directly. So in the engine, restriction subtraction is "each
stating rule over its own restrictions" (508.1a/508.1c, 509.1a/509.1b, 601.3,
602.5), and 101.2 is the tiebreaker layered *on top* for effect-vs-effect
"can't" clashes. 101.1 is a separate precedence rule: card text that directly
contradicts a rule overrides only that rule, in that specific situation
("can block any number of creatures" vs 509.1a, Noble Ox), and its one stated
exception is concession (104.3a). It doesn't displace 101.2, so a "can't
block" effect still beats a 101.1 permission. "Can block as though untapped"
is not a 101.1 case; it is an AsThough premise (§3, 609.4).

*Activation bans reach mana abilities.* "A player can't begin to activate
an ability that's prohibited from being activated" (602.5). A mana
ability's activation "follows the rules for activating any other activated
ability" except as 605.3a–c say (605.3), and none of those exceptions lifts
a prohibition. 605.3a's extra windows widen a **May**, and a "can't" effect
beats them (101.2). So "activated abilities of X can't be activated" stops
X's mana abilities too: "No abilities of creatures your opponents control
can be activated, including mana abilities" (Linvala, Keeper of Silence
ruling; the Null Rod, Stony Silence, and Cursed Totem rulings agree). A
mana ability escapes only when the prohibition's own scope excludes it.
Split second forbids activating "abilities that aren't mana abilities"
(702.61a; 702.61b restates the exemption), and Damping Matrix and Pithing
Needle say "can't be activated unless they're mana abilities." Write the
exemption as the row's predicate, `Cant(Activate(p, A) where ¬Mana(A))`,
never as an engine-wide pass for mana abilities. 702.61b also lets players
take special actions under split second. Those are a separate kind of
action (116.1–116.2), not activations.

**Must** is not "do it"; it is "the declaration is illegal if you could have
obeyed more requirements without breaking a restriction." The combat solver
(508.1d attackers, 509.1c blockers): maximize the number of requirements
obeyed subject to every restriction, with the Gate caveat above (a Gate's
price is never compulsory). Restrictions
(508.1c) and requirements (508.1d) are checked by *different* rules: 508.1c
fails a declaration that disobeys any restriction; 508.1d fails one that
obeys fewer requirements than the maximum possible. The same
maximize-without-violating solver governs target choice: "the player
chooses targets so that they obey the maximum possible number of such
effects without violating any rules or effects that say that an object or
player can't be chosen as a target" (601.2c). "Cast … if able" is not a
declaration-time Must but a resolution-time instruction, and its impossible
parts are ignored (101.3). Whether a creature "had to attack" is fixed by
the requirements in force when attackers were declared (506.7).

**What counts as one requirement.** The tally counts requirements, and
509.1c's parenthetical names the per-creature kind ("effects that say a
creature must block"). Three blocking wordings feed it different numbers:

- **"Target creature blocks [X] this turn if able"** (Trumpeting Armodon;
  provoke, 702.39a): one requirement, on that one creature.
- **"All creatures able to block [X] do so"** (Lure): one requirement on
  *each* creature able to block X. A creature blocks one attacker (509.1a),
  so against two such attackers each creature obeys one of its two
  requirements: creatures "must block one Prized Unicorn, but they don't
  all have to block the same Prized Unicorn" (Prized Unicorn ruling).
- **"[X] must be blocked [this turn] if able"** (Gaea's Protector, Frodo
  Baggins, Loathsome Catoblepas): worded on the attacker, outside the
  per-creature parenthetical. The rulings make it one requirement on the
  defending player's declaration, obeyed when at least one creature blocks
  X: "only one creature is required to block it. Other creatures may also
  block it and are free to block other creatures or not block at all"
  (Frodo Baggins ruling). Obedience is a predicate on the blocker set, the
  requirement-side twin of menace's set-level restriction (§5). Counted
  variants are set-level too: "by exactly one creature" (Nacatl War-Pride;
  if that is impossible, the defender "may block it with multiple creatures
  or may leave it unblocked") and "by two or more creatures" (Gorm the Great).

Compiling "must be blocked" to Lure's per-creature form forces every able
creature onto X, the overcount these rulings rule out. Repeats add no
blockers: activating Loathsome Catoblepas's ability again "provides no
additional benefit", and "One creature equipped with multiple Slayer's
Cleavers only requires a single Eldrazi to block it." *Engine inference:*
score a "must be blocked" requirement as one unit in the same 509.1c tally
as per-creature ones. A lone defending creature facing a "must be blocked"
attacker while it "blocks [another attacker] if able" may then block either
(one requirement obeyed each way), but not neither. The CR fixes duplicate
weight only for goad (701.15c–d). Whether repeated requirements count once
or once per effect when they compete is left open
(UD-15).

Goad piles on — each goading player adds requirements (701.15c). 701.15b says
a goaded creature "attacks each combat if able **and** attacks a player other
than [the goader] **if able**." *Both* legs are **requirements** ("if able"),
arbitrated by 508.1d — *not* a restriction. So each distinct goader adds one
pair, **Must**(Attack(This)) ∧ **Must**(Attack(This, d) where Player(d) ∧
d ≠ goader), with **no** Cant; a repeat goad by the same player adds nothing
(701.15d). Why it matters: with two or more goaders and every attackable
player a goader, attacking any goader obeys the Attack requirement plus every
*other* goader's "attack a player other than [goader]" requirement, while
attacking a planeswalker or battle obeys strictly fewer. So 508.1d requires
attacking a player, and the controller chooses which (Disrupt Decorum
ruling). With a single goader who is the only attackable player, the target
requirement is unsatisfiable, and attacking that player or their
planeswalker/battle are equally legal (same ruling). Read as a
**Cant**(Attack the goader), a creature goaded by everyone who can attack only
goaders would illegally be unable to attack at all — the opposite of goad's
intent.

Restrictions and evasion bind only at declaration: once a creature has been
declared as an attacker or blocker, a later effect that would have kept it
from attacking or blocking doesn't remove it from combat (506.4a), and an
attacking creature that gains or loses an evasion ability after a legal block
has been declared doesn't change that block (509.1b). A "must attack this
turn if able" effect is a rules-modifying effect, applied after all other
continuous effects and in timestamp order (613.11).

## 5. Modal evaluation over completions (601.3)

Because an action is judged while choices are still open, legality is
checked in two phases.

- **Begin-gate: existential over completions.** 601.3 (602.5 for
  activation) decides whether the player may begin: a player may begin an
  action if **some** completion is legal.
- **Recheck after proposal.** Once the proposal is made (601.2a–d), the
  chosen completion must itself be legal (601.2e, 601.6; applied to
  activation via 602.2b), or the action rewinds (733.1). Legality changes
  during cost determination and payment (601.2f–h), or after the spell has
  been cast, don't matter (601.6).

The begin-gate cases:

- 601.3a: if an effect prohibits casting spells with a quality, and a
  choice in the proposal (e.g. the value of X) could change that quality so
  the prohibition no longer applies, the player may begin — *ignoring* the
  effect (Void Winnower vs an {X} spell). The recheck then holds the chosen
  completion to the restriction: Endless One is castable with X equal to 5,
  but not with X equal to 6 (Void Winnower ruling).
- 601.3b and 601.3c are existential over proposal choices: 601.3b over a
  choice that changes a quality (bestow's alternative cost making the spell
  an Aura, under an effect that lets you cast Auras as though they had
  flash), 601.3c over paying the alternative or additional cost a granting
  effect requires.
- 601.3d is a present-tense check, not an existential one: a spell that
  would have flash only if certain conditions are met may begin to be cast
  as though it had flash if those conditions are met, whether the flash is
  its own text or a granting effect. Once casting has begun, that flash
  persists even if the conditions stop being met (601.6a). The persistence
  doesn't extend to 601.3b/c cases, whose chosen completion must still
  qualify. Conditions that only a proposal choice can satisfy (Silver
  Scrutiny's X; Flash Photography's and Timely Ward's targets) need 601.3b's
  existential reading. The CR doesn't say a target is a "quality" the choice
  can change, so that extension is an *engine inference*
  (UD-20).

So the engine does not pre-commit choices before checking legality; it asks
"∃ a legal completion?" at the begin-gate, then rechecks the completion the
player actually proposed. This is why **set-level** predicates are mandatory.

**Set-level predicates.** Menace ("can't be blocked except by two or more
creatures", 702.111b) is not a per-creature check — it constrains the *whole
declaration set*. 509.1c evaluates the entire blocker set against the menace
restriction (its own example walks one creature's "blocks if able"
requirement against menace: obeying that requirement without breaking
menace's restriction forces both of the player's creatures to block).
The legality predicate's argument is the declaration set, not one creature at
a time. Requirements can be set-level too: "[X] must be blocked if able" is
obeyed by the blocker set, not by any one creature (§4). So is "can't attack
alone" / "can't block alone" (506.5; the 508.1c example: two creatures each
with "This creature can't attack alone" may both be declared). The per-player
reading of 506.6 applies only to text that says "attacks a player alone".
(Banding is *not* a menace-style set-restriction: it is primarily a
band-*declaration* and combat-*damage-assignment* modifier — 702.22 — that
changes who chooses damage division, not a Cant on the blocker set; keep it
out of this set-restriction bucket.)

## 6. The deontic / event-edit boundary

The crucial distinction: **"can't" / choice-legality (deontic)** vs
**"doesn't" / "skip" / replacement (event-edit)**. They live in different
systems.

- **Deontic** clauses gate whether a *choice* is legal at declaration/
  proposal time. They are this doc.
- **Event-edits** rewrite an event that is *actually happening* —
  replacement effects (614.1), "skip" = replace-with-nothing (614.1b),
  prevention (615). Replacement, skip, and the 614.17 statement are
  `effects.md` §6; prevention is `effects.md` §7.

The CR states the boundary itself: 614.17 — "Some effects state that
something can't happen. These effects **aren't** replacement effects, but
follow similar rules." A "can't" must exist before the event (614.17a),
can't fund a cost (614.17b: "If an event can't happen, a player can't choose
to pay a cost that includes that event"), and a forbidden event can be
replaced only by a self-replacement effect (614.17c).

**Scope caveat — "can't" over outcomes is not action legality.** A "can't"
ranging over a game *outcome* (can't lose the game, can't win the game) is
not a choice-legality clause, so do **not** compile it to Cant. This
"not deontic" split is this engine's taxonomy, not a CR statement. The
base can't-lose/can't-win semantics are in `outcomes.md` §2 (settled entry
U5 in `underdetermined.md`).

- **Outcomes.** "Can't lose" blocks the loss routes (the 704.5a–c SBAs, the
  variant 704.6a–c SBAs, and 104.3e effects) while it applies; "can't win"
  blocks wins from effects (104.2b). Neither stops concession (101.1's stated
  exception; 104.3a) or a tournament penalty (104.3k; policy, not a card
  override, `outcomes.md` §2). The last-player-standing win overrides
  can't-win: it "happens immediately and overrides all effects that would
  preclude that player from winning the game" (104.2a; not an SBA).
  Separately, 104.3f arbitrates simultaneous win-and-lose to a loss, and
  704.7 lets one replacement answer simultaneous same-result SBAs; neither
  is overridden by can't-lose.
- **Life.** "Can't gain/lose life" and "life total can't change" are 614.17
  can't-events over life-change events (119.7, 119.8; `effects.md` §6), not
  outcome machinery. Their deontic shadow is a Cant on Pay-as-cost for any
  cost that includes the forbidden event (614.17b, 119.7, 119.8): pay-life
  costs and Phyrexian life payment (601.2b) are illegal, except that 0 life
  can always be paid (119.4b). Payability is `costs.md` §5.

**Worked contrast — vigilance vs defender.** Both touch attacking; only one
is deontic.

- **Defender** (702.3b): "A creature with defender **can't attack**." Pure
  **Cant**(Attack) — it removes the declare-attackers permission. Deontic.
- **Vigilance** (702.20b): "Attacking **doesn't** cause creatures with
  vigilance to tap." Attacking stays fully legal; the *tap event* that
  declaring normally produces (508.1f) simply never happens for it —
  rules text on the procedure itself (702.20a; classified intrinsic,
  `keyword-classification.md`). Event-side, not deontic — never a Cant.
  Same combat step, opposite layer.

**Worked trap — "can't be regenerated."** It surface-reads deontic ("can't")
but is an event-edit. Regeneration is itself a replacement effect: a shield
that replaces the next destruction (701.19a–b). "Can't be regenerated" does
**not** make activating an ability or casting a spell that creates a shield
illegal (701.19c: it "doesn't preclude such abilities from being activated or
such spells from being cast"); it causes the regeneration *shields not to be
applied* — suppression of a replacement, in the 614.17-adjacent "can't ≠
replacement" layer, not a Cant on any action.

## 7. Flash, pinned

Flash is the canonical permission-window case — keep three things separate:

1. **Intrinsic flash** (702.8a): "You may play this card any time you could
   cast an instant." A *wider window* on the Play/Cast-permission row — the
   default cast window is 117.1a (sorcery-speed for noninstants); flash
   widens it to instant-speed. This is a **May** with a broadened window, not
   an AsThough.
2. **Granted "as though it had flash"**: an **AsThough** premise (609.4)
   pinned to *another* permanent's casting — "you may cast spells as though
   they had flash." The game pretends the spell has flash for that cast only.
3. **The 601.3 wrinkle**: granted-flash has two checks (§5). 601.3b and
   601.3c are existential over proposal choices: a player may begin casting
   as-though-flash if some choice (a quality-changing choice such as bestow,
   or paying the required alternative or additional cost) brings the
   as-though-flash effect into range. 601.3d is a present-tense check of the
   conditions under which the spell would have flash, whether from its own
   text or a granting effect, and that flash persists once casting has begun
   even if the conditions lapse (601.6a).

## 8. Worked notation

Notation: `Cant(Verb(actor, object) where ⟨pred⟩)`,
`May(Verb …)`, `Must(Verb …)`, `Gate(Verb …, cost)`, `Toll(Verb …, cost)`.

| mechanic | algebra |
|---|---|
| **Flying** (702.9b) | `Cant(Block(b, This) where ¬(Flying(b) ∨ Reach(b)))` |
| **Menace** (702.111b) | `Cant(BlockSet(S, This) where |S| < 2)` — set-level |
| **Defender** (702.3b) | `Cant(Attack(This))` |
| **Shroud** (702.18a) | `Cant(Target(x, This))` for all sources — symmetric |
| **Hexproof** (702.11b) | `Cant(Target(x, This) where Opponent(controller(x)))` — asymmetric |
| **Protection from Q** (DEBT, 702.16) | `Cant(Target(x,This) where Q(x))` (b) ∧ `Cant(Enchant/Equip(x,This) where Q(x))` (c/d) ∧ `Cant(Block(b,This) where Q(b))` (f) ∧ Damage from Q-sources prevented (e — *prevention*, an event-edit leg, not deontic) ∧ Auras/Equipment/Fortifications with Q already attached are removed by SBA (c/d — *SBA cleanup*, executed by 704.5m–n, outside the deontic layer). 702.16j/k extend all legs to everything and to a player |
| **Ward [cost]** (702.21a) | `trigger on BecomesTarget(This, s) where Opponent(controller(s), controller(This)) ⇒ Toll(resolve(s), controller(s) pays [cost])` — counter unless paid; never a Gate on casting. [cost] may be non-mana (life, discard, poison counters); X is determined as the ward trigger resolves (702.21b) |
| **Goad** (701.15b–d) | `Must(Attack(This)) ∧ Must(Attack(This, d) where Player(d) ∧ d ≠ goader)`, one pair per distinct goader — *both* legs are "if able" **requirements** (508.1d), not a Cant; each additional goader adds requirements (701.15c), a repeat goad by the same player adds none (701.15d) |
| **Haste** (702.10b–c) | a *flag* the standing Cant rows read, not a May-row lift: `Cant(Attack(This) where ¬Haste(This) ∧ ¬ContinuouslyControlled(This))` (508.1a) ∧ `Cant(Activate(p, A) where Creature(src(A)) ∧ {T}/{Q} ∈ cost(A) ∧ ¬Haste(src(A)) ∧ ¬ContinuouslyControlled(src(A)))` (602.5a; evaluate `Creature` at activation, which catches an animated land that came under control this turn) |
| **Split second** (702.61a–b) | while This is on the stack: `Cant(Cast(p, s) where s ≠ This) ∧ Cant(Activate(p, A) where ¬Mana(A))`. The mana exemption is the row's own predicate (§4); special actions are untouched (702.61b) |
| **"Activate only as a sorcery"** (602.5d, 307.5) | `Only`-refine: `May(Activate(p, A))` window ∩ sorcery-timing window |

Protection's five legs are not all deontic: Target/Enchant-Equip/Block are
**Cant** (deontic); Damage is **prevention** (event-edit, `effects.md` §7);
the attachment cleanup (702.16c–d, executed by 704.5m–n) is a state-based
action, also outside the deontic layer. That split is the whole point of §6.

Haste is spelled as a flag in the Cant predicates (the reach pattern —
meaning living in another rule's predicate) rather than a May-row lift
because the summoning-sickness restrictions name haste in their own
conditions: 508.1a's declaration legality reads "must either have haste or
have been controlled by the active player continuously since the turn
began," and 602.5a says "Ignore this rule for creatures with haste" — so
there is no separate permission row for haste to widen; 302.6 and
702.10b–c are prose mirrors of those two predicates.

## 9. Grammar → algebra marker table

Surface phrases that signal a deontic clause (corpus-verified lines).

| marker | polarity | real corpus line |
|---|---|---|
| `can't be blocked except by …` | Cant (block) | "It can't be blocked except by two or more creatures." (menace reminder) |
| `can't attack` / `can't block` | Cant | "Target creature can't attack or block this turn." |
| `can't be blocked by more than one` | Cant (set) | "Each creature you control can't be blocked by more than one creature." |
| `can't attack alone` / `can't block alone` | Cant (set; 506.5, the 508.1c example) | "This creature can't attack alone." |
| `can block only …` | Cant (blocker side) | "This creature can block only creatures with flying." |
| `can't be the target of …` | Cant (target) | shroud/hexproof keyword text (702.18a / 702.11b) |
| `Activate only as a sorcery` | Only (window) | "{0}: Attach target Equipment you control to this creature. Activate only as a sorcery." |
| `Activate only during your turn / once each turn` | Only (window) | "Activate only during your turn and only once each turn." |
| `attacks each combat if able` | Must | "Goad target creature. (Until your next turn, that creature attacks each combat if able …)" |
| `blocks … if able` | Must (that creature) | "{1}{G}: Target creature blocks this creature this turn if able." |
| `all creatures able to block … do so` | Must (each able creature; §4) | "All creatures able to block enchanted creature do so." |
| `must be blocked … if able` | Must (one, on the blocker set; §4) | "This creature must be blocked if able." |
| `can't attack … unless … pays` | Gate | "Creatures can't attack you unless their controller pays {2} for each creature they control that's attacking you." |
| `unless … pays {N}` | Toll | "Counter target spell unless its controller pays {2}." |
| `Ward {N}` | Toll | "Ward {1} (Whenever this creature becomes the target of a spell or ability an opponent controls, counter it unless that player pays {1}.)" |
| `as though it didn't have [keyword]` | AsThough | "This creature can attack this turn as though it didn't have defender." |
| `may cast … as though they had flash` | AsThough (permission) | "You may cast spells this turn as though they had flash." |
| `spend mana as though it were …` | AsThough (payment) | "you may spend mana as though it were mana of any color to cast that spell." (609.4b) |

Note: the Oracle idiom is **"can't … except by"**, not "can only be blocked
by" (the latter returns no corpus hits). Map both intuitions to the Cant
form. See `grammar.md` §2 for the activation-instruction surface forms
("Activate only …") and its §4 boundary note for how these markers divide
from the replacement layer.

## 10. Engine evaluation

```
legal(a):                          # a = action instance, choices may be open
    completions = enumerate_completions(a)          # 601.3 modal step
    return ∃ c ∈ completions:
        (∃ row ∈ permissions(verb(a)): row.matches(c))   # May floor, 117.1/508.1a/509.1a/601.3
        ∧ (¬∃ row ∈ restrictions(verb(a)): row.forbids(c))  # restriction subtraction:
        # 508.1a/c, 509.1a/b, 601.3, and 602.5 (activation begin-gate) subtract
        # their own restrictions; 101.2 is only the effect-vs-effect
        # "can't beats may" tiebreaker.
        # Gates are conditional permissions: a Gate row .matches(c) only if
        # its price is among c's paid costs; the actor is never forced to pay,
        # so unpaid-Gate completions simply don't match. Payment only adds
        # options and never raises the required maximum (508.1d / 509.1c).
        # Tolls (ward, counter-unless-pays) never enter declare-legality —
        # they bite downstream, as triggers or at resolution.

recheck(c):                        # after the proposal (601.2a–d)
    # the chosen completion must itself be legal (601.2e, 601.6; activation
    # via 602.2b), else rewind (733.1). Legality changes during cost
    # determination and payment (601.2f–h) or after casting don't matter
    # (601.6); flash held because its conditions were met persists (601.6a),
    # but that doesn't extend to 601.3b/c cases.
    return c is still a legal completion

declare_combat(player, side):                       # attackers 508 / blockers 509
    sets = all candidate declaration sets
    legal_sets = { S ∈ sets : ∀ member: legal(...)        # per-member Cant
                              ∧ set_predicates_ok(S) }     # menace, set-level (not
                              # banding: that's a 702.22 declaration/damage modifier)
    # obligation solver (508.1d / 509.1c): the bar is set over sets that pay
    # no Gate. Payment only adds options and never raises the required
    # maximum, so the player is not forced to pay even if paying would obey
    # more requirements.
    # requirement units (§4): per-creature rows ("blocks X if able", each
    # Lure-bound creature) and set-level rows ("X must be blocked if able":
    # obeyed iff ≥1 blocker on X; engine inference from rulings)
    maximum = max over S ∈ legal_sets with no Gate paid of obeyed_requirements(S)
    require player picks some legal S, with or without paid Gates,
            whose obeyed_requirements(S) reaches maximum
```

Evaluation order: enumerate completions → permission floor → restriction
subtraction → (cast/activate: recheck the chosen completion after proposal)
→ obligation maximization over sets that pay no Gate → pay any Gates the
chosen set incurs (Tolls bite later, at trigger/resolution time). AsThough is
applied as a premise-rewrite *inside* `matches`/`forbids` for the scoped
effect only (609.4).

## Cross-references

- `generalizations.md` Families 1 (cast/play permission), 3 (timing
  permission), 6 (targeting/interaction permission), 9 (combat-requirement
  delegation) — **this layer is their merge**: one algebra, one carrier.
- `effects.md` §6 and §7 — the event-edit side of the §6 boundary here
  (§6: replacement 614.1, skip 614.1b, the 614.17 "can't ≠ replacement"
  statement; §7: prevention 615).
- `grammar.md` §2 (activation instructions) and the §4 boundary note — where
  the surface forms of these clauses are described.
- `outcomes.md` §2 — the outcome side of §6 here ("can't lose" / "can't win").
- `choices.md` §5 — the choice-side view of the obligation solver, including
  the target-choice requirement of 601.2c.
- `variants.md` §2 "deontics.md" — multiplayer overrides of the §2/§4
  legality checks (801.3, 801.4, 801.6, 802.3a, 802.4a–b, 803.1a–b, 809.3c,
  811.4).
- `keyword-classification.md` — which keywords compile to deontic predicates
  (flying, menace, ward, protection, shroud) vs need an engine opcode.
