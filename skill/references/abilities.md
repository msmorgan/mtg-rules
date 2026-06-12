# Abilities — Taxonomy

*Synthesized from the Comprehensive Rules effective 2026-04-17
(`data/rules/cr.json`). Orientation only — verify load-bearing specifics
with `scripts/rule` before citing. Run `scripts/cite check` after CR
refreshes.*

How an engine should classify what a card can do. The four general
categories partition every ability (113.3); the cross-cutting sub-kinds
overlay them with special timing/stack rules. Closed lists are enumerated
in full. For mapping surface card text to these categories, see the planned
sibling `grammar.md`.

## 1. The four kinds

Rule 113.3 names four general categories. The first three are *abilities of
objects*; only activated and triggered abilities can exist as objects on
the stack (113.1c, 113.9).

- **Spell ability** (113.3a) — instructions followed while an instant or
  sorcery spell resolves. Any text on an instant/sorcery is a spell ability
  unless it's an activated, triggered, or 113.6-qualifying static ability
  (113.3a). Grammar cue: imperative sentences with no cost/colon and no
  when/whenever/at. See `grammar.md`.
- **Activated ability** (113.3b) — has a cost and an effect, written
  "[Cost]: [Effect.] [Activation instructions (if any).]" (113.3b, 602.1).
  The cost is everything before the colon (602.1a). Activate whenever you
  have priority; it goes on the stack (113.3b, 602.1c). The *only* kind of
  ability that can be activated; a bare "activate an ability" means this
  kind (602.1c).
- **Triggered ability** (113.3c) — has a trigger condition and an effect,
  written "[Trigger condition], [effect]," and includes (usually begins
  with) "when," "whenever," or "at" (113.3c). When the event occurs it goes
  on the stack the next time a player would receive priority (113.3c, 603.3).
- **Static ability** (113.3d) — written as a statement; it's simply true,
  creating a continuous effect active while the source is in the appropriate
  zone (113.3d, 604.1). Does not use the stack and can't be countered
  (113.9, 604.1). See `effects.md`.

**Keyword abilities** (702.1) are notational shorthand: each keyword resolves
to one or more abilities of the four kinds above (e.g. a keyword line may
bundle an activated cost, a triggered effect, and a static clause together).
The machine-readable list of keyword abilities lives in
`data/rules/keywords.json`; `scripts/keyword <name>` prints a keyword's
defining CR section.

## 2. Cross-cutting sub-kinds

These overlay the four kinds. Each carries special timing or stack behavior
an engine must special-case.

| Sub-kind | Defining rule | Underlies kind(s) | Recognize by |
|---|---|---|---|
| Mana ability (activated) | 605.1a | activated | no target, could add mana, not a loyalty ability |
| Mana ability (triggered) | 605.1b | triggered | no target, triggers off a mana ability / mana added, could add mana |
| Loyalty ability | 606.2 | activated | loyalty symbol in the cost |
| Characteristic-defining (CDA) | 604.3a | static | states a defining characteristic (color/subtype/P/T) about itself |
| Linked abilities | 607.1 | activated/triggered/static | one ability refers to what another did ("the exiled cards," "the chosen color") |
| Delayed triggered | 603.7 | triggered | created by a resolving effect; "when/whenever/at" not at the start |
| State trigger | 603.8 | triggered | triggers while a game *state* holds, not on an event |
| Intervening-"if" trigger | 603.4 | triggered | "When/Whenever/At [event], **if** [condition], [effect]" |
| Reflexive triggered | 603.12 | triggered | "When you do, ..." referring to an action taken during the same resolution |

**Mana abilities** (605.1) — two disjoint definitions:
- *Activated*: no target, *could* add mana on resolution, and not a loyalty
  ability (605.1a). *Triggered*: no target, could add mana, and triggers
  off activating/resolving a mana ability or off mana being added (605.1b).
- Special behavior: neither uses the stack — each resolves immediately and
  can't be targeted, countered, or responded to (605.3b, 605.4a). An
  activated mana ability may be activated whenever priority is held *or*
  whenever a mana payment is asked for, even mid-cast/mid-resolution
  (605.3a). Once begun, it can't be activated again until it resolves
  (605.3c). Stays a mana ability even when it can't currently produce mana
  (605.2). A spell is never a mana ability (605.5b); an ability with a
  target never is (605.5a).

**Loyalty abilities** (606) — an activated ability with a loyalty symbol in
its cost (606.2); normally only planeswalkers have them (606.2). Activate
only with priority, an empty stack, during a main phase of your turn, and
only if no loyalty ability of *that permanent* was activated this turn
(606.3). The cost is putting on or removing loyalty counters as the symbol
shows (606.4); multiple add/remove costs combine into one (606.5). A
negative-cost ability needs at least that many counters present (606.6).

**Linked abilities** (607) — two abilities where one takes an action and the
other refers only to *that* action's objects/players (607.1). The second
("the exiled card," "the chosen color," etc.) ignores anything any other
ability did (607.1). Recognize the closed list of linkage patterns in
607.2: exile-then-reference (607.2a), replacement-exile reference (607.2b),
put-onto-battlefield reference (607.2c), "choose a [value]" / "the chosen
[value]" (607.2d), noted-information reference (607.2e), choose-a-word
reference (607.2f), enters-cost reference (607.2g), static-plus-its-own-
triggers in one paragraph (607.2h), additional-cost-paid reference (607.2i),
variable-cost-paid reference (607.2j), champion (607.2k), anchor word
(607.2m), pre-game-exile-by-name reference (607.2n), pre-game CDA choice
(607.2p), and spell-cast-cost-exile reference (607.2q). An ability may
belong to more than one linked pair (607.4); copy/grant can establish a
link on a new object (607.5). Engine: track what the first ability did so
the second can resolve (see `state.md` linked-ability tracking).

**Characteristic-defining ability** (604.3) — a static ability conveying a
characteristic normally found elsewhere on the object (604.3). The closed
criteria (604.3a): it defines (1) color, subtype, power, or toughness; (2)
is printed on / granted to the token / copied/text-changed onto the object;
(3) doesn't directly affect other objects' characteristics; (4) isn't one
the object grants itself; (5) doesn't set the value only conditionally. A
CDA functions in *all* zones, outside the game, and before the game begins
(604.3, 113.6a). In the layer system, CDA-defined P/T applies in layer 7a
ahead of other P/T effects (613.4a), and CDAs apply first within layers 2–6
(613.3).

**Delayed triggered ability** (603.7) — created during resolution of a
spell/ability, by a replacement effect, or by a static ability allowing an
action (603.7a). Contains "when/whenever/at," usually not at the start
(603.7). It won't trigger until actually created, even if its event just
happened (603.7a). Triggers only once — the next time its event occurs —
unless given a duration (603.7b). Source/controller are fixed by 603.7d–h
depending on what created it.

**State trigger** (603.8) — triggers when a game *state* matches its
condition (e.g., "Whenever you have no cards in hand"), not on a discrete
event (603.8). Fires as soon as the state holds and goes on the stack at
the next opportunity; it won't trigger again until it has left the stack,
then re-triggers if the state still holds (603.8). Distinct from
state-based actions (603.8).

**Intervening-"if" trigger** (603.4) — "When/Whenever/At [event], **if**
[condition], [effect]" (603.4). The condition is checked when the event
occurs (no trigger if false) *and again* on resolution (removed from the
stack if false then), mirroring the legal-target check (603.4). This rule
applies only to an "if" immediately following the trigger condition;
elsewhere "if" has its plain meaning (603.4).

**Reflexive triggered ability** (603.12) — created by a resolving spell/
ability that lets/instructs a player to act, triggering "when [a player]
[does/doesn't]" or "when [something happens] this way" (603.12). It follows
the delayed-trigger rules but is checked *immediately* after creation,
triggering on whether the event occurred earlier during the *same*
resolution (603.12). Normally triggers once per occurrence, but a
"pay this cost any number of times" / "when you pay one or more times"
pairing triggers it only once (603.12a).

## 3. Where abilities function

Default (113.6): abilities of an instant/sorcery spell function only while
it's on the stack; abilities of all other objects function only while on
the battlefield. The full list of exceptions (113.6a–p):

- 113.6a — characteristic-defining abilities function everywhere, even
  outside the game and before it begins.
- 113.6b — an ability stating which zones it functions in functions only
  from those zones.
- 113.6c — an ability stating which zones it *doesn't* function in functions
  everywhere else, even outside/before the game.
- 113.6d — an alternative-cost / cost-modifying ability for that object
  functions on the stack.
- 113.6e — an ability restricting/modifying how *that* object can be
  played/cast functions in any zone it could be played/cast from and on the
  stack; one that *grants another ability* doing so functions only on the
  stack.
- 113.6f — an ability restricting/modifying *what zones* that object can be
  played/cast from functions everywhere, even outside the game.
- 113.6g — "can't be countered" / "can't be copied" functions on the stack.
- 113.6h — an ability modifying how that object enters the battlefield
  functions as it enters (see 614.12).
- 113.6i — "counters can't be put on this" functions as it enters *and*
  while on the battlefield.
- 113.6j — an activated ability whose cost can't be paid on the battlefield
  functions from any zone where its cost can be paid.
- 113.6k — a trigger condition that can't trigger from the battlefield
  functions in all zones it can trigger from; other conditions of the same
  ability may function in different zones.
- 113.6m — an ability that moves its object out of a particular zone
  functions only in that zone (with stated exceptions for being put there
  first, or an Aura's enchanted permanent leaving).
- 113.6n — a deck-construction-modifying ability functions before the game
  begins.
- 113.6p — abilities of emblems, plane, vanguard, scheme, and conspiracy
  cards function in the command zone.

(Static-ability variants are restated by 604.5 for the stack and 604.6 for
play-from-hand wording.)

## 4. Abilities as objects vs as properties

An ability is normally a *property* — a characteristic an object has that
lets it affect the game (113.1a), or, for a player, something granted by an
effect that changes how the game affects them (113.1b). But an activated or
triggered ability *on the stack* is itself an **object** (113.1c).

Once activated or triggered, an ability on the stack exists **independently
of its source** — destroying or removing the source afterward doesn't affect
the ability (113.7a). Some abilities make the *source* do something rather
than acting directly; such an ability checks source information when it's
put on the stack (if needed then) or otherwise on resolution, and falls
back to the source's last known information if the source has left its
expected zone — the source can still perform the action even if it no longer
exists (113.7a). The source of an ability is the object that generated it
(113.7); its controller is set by 113.8 (delayed triggers: 603.7d–f).
Abilities on the stack aren't spells and can't be countered by spell-only
counters, though "counter target ability" effects work; static abilities
never use the stack and can't be countered at all (113.9).

## 5. Granted and lost abilities

Effects can add or remove abilities: an adding effect says the object
"gains" or "has" the ability, a removing effect says it "loses" it (113.10).
Removing an ability removes *all* instances of it (113.10b); adding an
activated ability may include activation instructions that become part of it
(113.10a). These changes are continuous effects applied in **layer 6**
(ability-adding, keyword counters, ability-removing, and "can't have")
(613.1f); generally the most recent add/remove of the same ability prevails,
subject to dependency (113.10c, 613.3). See `effects.md` for the layer
system.

"Can't have" effects (113.11) go further: the object loses the ability if it
has it, and no effect or keyword counter can add it — a continuous effect
that would add it simply doesn't apply that part (113.11). Note "loses all
abilities" / "all creatures lose all abilities" applies the moment a
permanent is on the battlefield, so it can strip an enters-the-battlefield
trigger before it would fire (603.6b). Distinguish granting an ability from
*setting a characteristic* or *stating a quality*: "[permanent] is
[value]" defines a characteristic (a CDA-style effect, 604.3) and
"[creature] can't be blocked" states a quality — neither is a granted
ability, so neither is removed by "loses all abilities" (113.12).
