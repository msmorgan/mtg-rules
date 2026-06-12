# Deontic Layer — May / Can't / Must / Toll Algebra

*Synthesized from the Comprehensive Rules effective 2026-04-17
(`data/rules/cr.json`). Orientation only — verify load-bearing specifics
with `scripts/rule` before citing. Run `scripts/cite check` after CR
refreshes.*

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
| **May**(a) | a is permitted | cast: 117.1a–c; attack: 508.1a; block: 509.1a | keyword/effect rows ("may play this as though…", flash 702.8a) |
| **Cant**(a) | a is forbidden | — (none; absence of Cant) | 508.1c attack-restrictions, 509.1b block-restrictions, "can't be…" |
| **Must**(a) | a is required if able | — | "attacks if able" 508.1d, "blocks if able" 509.1c, goad 701.15b |
| **MayIf**(a, cost) — *declaration-gate* | a is legal *only if* the toll is paid at declaration | — | "can't attack/block unless … pays" (508.1d / 509.1c), play-gating "can't cast unless" |
| **MayIf**(a, cost) — *resolution-stage* | a is *fully legal*; a later trigger/resolution punishes unless the toll is paid | — | ward 702.21a, Mana-Leak-style "counter … unless its controller pays {N}" |

**May** is the existential floor: an action with *no* matching permission
row is illegal. Casting needs a permission and no prohibition (601.3); the
seven hand-zone play rules, 117.1a–c, and every "cast from" keyword are
permission rows in one table (generalizations.md Family 1).

**Cant** is pure subtraction. **Must** is satisfied-if-able and arbitrated
by the maximize-without-violating solver (§4). **MayIf** splits in two by
*when* the toll bites. A **declaration-gating** toll is conditional *legality*:
"can't attack/block unless a player pays a cost" makes the declaration illegal
unless paid — yet the actor is never *required* to pay, even to satisfy a
requirement (508.1d / 509.1c state this explicitly). A **resolution-stage**
toll leaves the action fully legal: ward (702.21a) and Mana-Leak-style "counter
… unless … pays {N}" let the spell be cast / the target be chosen normally,
then a *trigger or the resolving counter* punishes (counters it) unless the
toll is paid. §8's ward row is the resolution-stage form; don't model it as a
gate on casting.

## 3. Modifiers

Two operators take a polarity clause and return a refined one.

- **Only** — refines a permission by *intersection*: replaces "may, in
  window W" with "may, only in window W′ ⊆ W" (or only by predicate P).
  "Activate only as a sorcery" (602.5d) / "only as an instant" (602.5e)
  swaps the activation window for the sorcery/instant timing window —
  *without* requiring the player to actually hold such a card. "Only during
  your turn", "only once each turn" (602.5b) stack as further window
  intersections. On the blocker side, "can only be blocked by X" is written
  in Oracle as the **Cant**-except form (§6), not as an Only.

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
subtracted by the rules that state them. The declare-attackers restriction
check (508.1c) and the casting gate (601.3, "only if … allows … and no … rule
or effect prohibits") each fold their own restrictions into legality directly.
So in the engine, restriction subtraction is "508.1c/601.3 over rule-or-effect
restrictions," and 101.2 is the tiebreaker layered *on top* for effect-vs-
effect "can't" clashes.

**Must** is not "do it"; it is "the declaration is illegal if you could have
obeyed more requirements without breaking a restriction." The combat solver
(508.1d attackers, 509.1c blockers): maximize the number of requirements
obeyed subject to every restriction, with the toll caveat above. Restrictions
(508.1c) and requirements (508.1d) are checked by *different* rules: 508.1c
fails a declaration that disobeys any restriction; 508.1d fails one that
obeys fewer requirements than the maximum possible.

Goad piles on — each goading player adds requirements (701.15c). 701.15b says
a goaded creature "attacks each combat if able **and** attacks a player other
than [the goader] **if able**." *Both* legs are **requirements** ("if able"),
arbitrated by 508.1d — *not* a restriction. So goad composes as
**Must**(Attack(This)) ∧ **Must**(Attack-target(This, ¬goader)), with **no**
Cant. Why it matters: with two goaders and one legal defender, the two
"attack a player other than [goader]" requirements are jointly unsatisfiable.
508.1d maximizes — the creature still attacks (the Attack requirement is
obeyed) and the contradictory target requirements go unmet. Read as a
**Cant**(Attack the goader), a creature goaded by everyone who can attack only
goaders would illegally be unable to attack at all — the opposite of goad's
intent.

## 5. Modal evaluation over completions (601.3)

Because an action is judged while choices are still open, legality is
**existential over completions**: a player may begin an action if **some**
completion is legal.

- 601.3a: if an effect prohibits casting spells with a quality, and a
  choice in the proposal (e.g. the value of X) could change that quality so
  the prohibition no longer applies, the player may begin — *ignoring* the
  effect (Void Winnower vs an {X} spell).
- 601.3b: if you may cast a spell with a quality "as though it had flash"
  and a proposal choice (bestow's alternative cost making the spell an Aura)
  could grant that quality, you may begin to cast it as though it had flash.
- 601.3c–d: cost-conditioned and condition-gated flash resolve the same way.

So the engine does not pre-commit choices before checking legality; it asks
"∃ a legal completion?" This is why **set-level** predicates are mandatory.

**Set-level predicates.** Menace ("can't be blocked except by two or more
creatures", 702.111b) is not a per-creature check — it constrains the *whole
declaration set*. 509.1c evaluates the entire blocker set against the menace
restriction (its own example walks a two-blocker requirement against menace).
The legality predicate's argument is the declaration set, not one creature at
a time. (Banding is *not* a menace-style set-restriction: it is primarily a
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
  prevention (615). They are `effects.md` §6.

The CR states the boundary itself: 614.17 — "Some effects state that
something can't happen. These effects **aren't** replacement effects, but
follow similar rules." A "can't" must exist before the event (614.17a),
can't fund a cost (614.17b: "If an event can't happen, a player can't choose
to pay a cost that includes that event"), and a forbidden event can be
replaced only by a self-replacement effect (614.17c).

**Scope caveat — "can't" over outcomes is not action legality.** A "can't"
ranging over a game *outcome* (can't lose the game, can't win the game, life
total can't change) is **not** deontic; it modifies a state-based action or
outcome, so do **not** compile it to Cant. "Can't lose / opponents can't win"
overrides the loss/win SBAs (704.5a a player at ≤0 life loses; 104.2a the
last-player-standing win that "overrides all effects that would preclude that
player from winning"; 104.3f simultaneous win-and-lose resolves to lose; the
704.7 SBA-replacement combiner). These touch §704/§104 outcome machinery, not
the declare/cast legality this doc governs.

**Worked contrast — vigilance vs defender.** Both touch attacking; only one
is deontic.

- **Defender** (702.3b): "A creature with defender **can't attack**." Pure
  **Cant**(Attack) — it removes the declare-attackers permission. Deontic.
- **Vigilance** (702.20b): "Attacking **doesn't** cause creatures with
  vigilance to tap." Attacking stays fully legal; the *tap event* that
  declaring normally produces (508.1f) is edited out. Event-edit, not
  deontic. Same combat step, opposite layer.

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
   default cast window is 117.1a–b (sorcery-speed for noninstants); flash
   widens it to instant-speed. This is a **May** with a broadened window, not
   an AsThough.
2. **Granted "as though it had flash"**: an **AsThough** premise (609.4)
   pinned to *another* permanent's casting — "you may cast spells as though
   they had flash." The game pretends the spell has flash for that cast only.
3. **The 601.3 wrinkle**: granted-flash is evaluated existentially —
   601.3b–d let a player begin casting as-though-flash if some proposal
   choice (bestow, an alternative cost, a met condition) brings the
   as-though-flash effect into range.

## 8. Worked notation

Notation: `Cant(Verb(actor, object) where ⟨pred⟩)`,
`May(Verb …)`, `Must(Verb …)`, `MayIf(Verb …, cost)`.

| mechanic | algebra |
|---|---|
| **Flying** (702.9b) | `Cant(Block(b, This) where ¬(Flying(b) ∨ Reach(b)))` |
| **Menace** (702.111b) | `Cant(BlockSet(S, This) where |S| < 2)` — set-level |
| **Defender** (702.3b) | `Cant(Attack(This))` |
| **Shroud** (702.18a) | `Cant(Target(x, This))` for all sources — symmetric |
| **Hexproof** (702.11b) | `Cant(Target(x, This) where Opponent(controller(x)))` — asymmetric |
| **Protection from Q** (DEBT, 702.16) | `Cant(Target(x,This) where Q(x))` (b) ∧ `Cant(Enchant/Equip(x,This) where Q(x))` (c/d) ∧ `Cant(Block(b,This) where Q(b))` (f) ∧ Damage from Q-sources prevented (e — *prevention*, an event-edit leg, not deontic) |
| **Ward {N}** (702.21a) | trigger ⇒ `MayIf(resolve(spell/ability targeting This), pay {N})` — counter unless paid |
| **Goad** (701.15b–c) | `Must(Attack(This)) ∧ Must(Attack-target(This, ¬goader))` — *both* legs are "if able" **requirements** (508.1d), not a Cant; multiple goaders ⇒ additional requirements (701.15c) |
| **"Activate only as a sorcery"** (602.5d) | `Only`-refine: `May(Activate(p, A))` window ∩ sorcery-timing window |

Protection's four legs are not all deontic: Target/Enchant-Equip/Block are
**Cant** (deontic); Damage is **prevention** (event-edit, `effects.md` §6).
That split is the whole point of §6.

## 9. Grammar → algebra marker table

Surface phrases that signal a deontic clause (corpus-verified lines).

| marker | polarity | real corpus line |
|---|---|---|
| `can't be blocked except by …` | Cant (block) | "It can't be blocked except by two or more creatures." (menace reminder) |
| `can't attack` / `can't block` | Cant | "Target creature can't attack or block this turn." |
| `can't be blocked by more than one` | Cant (set) | "Each creature you control can't be blocked by more than one creature." |
| `can't be the target of …` | Cant (target) | shroud/hexproof keyword text (702.18a / 702.11b) |
| `Activate only as a sorcery` | Only (window) | "{0}: Attach target Equipment you control to this creature. Activate only as a sorcery." |
| `Activate only during your turn / once each turn` | Only (window) | "Activate only during your turn and only once each turn." |
| `attacks each combat if able` | Must | "Goad target creature. (Until your next turn, that creature attacks each combat if able …)" |
| `unless … pays {N}` | MayIf (toll) | "Counter target spell unless its controller pays {2}." |
| `Ward {N}` | MayIf (toll) | "Ward {1} (Whenever this creature becomes the target of a spell or ability an opponent controls, counter it unless that player pays {1}.)" |
| `as though it didn't have [keyword]` | AsThough | "This creature can attack this turn as though it didn't have defender." |
| `may cast … as though they had flash` | AsThough (permission) | "You may cast spells this turn as though they had flash." |
| `spend mana as though it were …` | AsThough (payment) | "you may spend mana as though it were mana of any color to cast that spell." (609.4b) |

Note: the Oracle idiom is **"can't … except by"**, not "can only be blocked
by" (the latter returns no corpus hits). Map both intuitions to the Cant
form. See `grammar.md` §4–5 for parsing these surface markers.

## 10. Engine evaluation

```
legal(a):                          # a = action instance, choices may be open
    completions = enumerate_completions(a)          # 601.3 modal step
    return ∃ c ∈ completions:
        (∃ row ∈ permissions(verb(a)): row.matches(c))   # May floor, 117.1/508.1a/509.1a/601.3
        ∧ (¬∃ row ∈ restrictions(verb(a)): row.forbids(c))  # restriction subtraction:
        # 601.3 / 508.1c subtract rule-or-effect restrictions themselves;
        # 101.2 is only the effect-vs-effect "can't beats may" tiebreaker.
        # tolls are conditional permissions: a MayIf row .matches(c) only if
        # the toll is among c's paid costs; the actor is never forced to pay
        # (508.1d / 509.1c), so unpaid-toll completions simply don't match.

declare_combat(player, side):                       # attackers 508 / blockers 509
    sets = all candidate declaration sets
    legal_sets = { S ∈ sets : ∀ member: legal(...)        # per-member Cant
                              ∧ set_predicates_ok(S) }     # menace, set-level (not
                              # banding: that's a 702.22 declaration/damage modifier)
    # obligation solver: keep only sets maximizing #(requirements obeyed)
    best = argmax_{S ∈ legal_sets} obeyed_requirements(S) # 508.1d / 509.1c
    require player picks some S ∈ best
```

Evaluation order: enumerate completions → permission floor → restriction
subtraction → obligation maximization → price any chosen tolls. AsThough is
applied as a premise-rewrite *inside* `matches`/`forbids` for the scoped
effect only (609.4).

## Cross-references

- `generalizations.md` Families 1 (cast/play permission), 3 (timing
  permission), 6 (targeting/interaction permission), 9 (combat-requirement
  delegation) — **this layer is their merge**: one algebra, one carrier.
- `effects.md` §6 — the event-edit side of the §6 boundary here
  (replacement 614.1, skip 614.1b, the 614.17 "can't ≠ replacement"
  statement).
- `grammar.md` §4–5 — surface markers that parse into these clauses.
- `keyword-classification.md` — which keywords compile to deontic predicates
  (flying, menace, ward, protection, shroud) vs need an engine opcode.
