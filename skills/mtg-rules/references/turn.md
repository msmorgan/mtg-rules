# Turn Structure, Priority, and Combat

*Synthesized from the Comprehensive Rules effective 2026-08-07
(`data/rules/cr.json`). Orientation only — verify load-bearing specifics
with `scripts/rule` before citing. Run `scripts/cite check` after CR
refreshes.*

How an engine sequences a turn: five phases, their steps, who gets priority
when, and the combat sub-machine. A turn = beginning, precombat main,
combat, postcombat main, ending — every turn, even if empty (500.1). The
beginning, combat, and ending phases break into steps that proceed in order
(500.1). The turn-based actions referenced below are mapped in full in
`actions.md` §2 (703.4 letters); this doc cross-cites them rather than
restating their text.

## 1. Phase / step table

A phase/step with priority ends when the stack is empty and all players pass
in succession — merely emptying the stack isn't enough, so everyone gets a
chance to add to it first (500.2). A step with no priority ends when its
specified actions complete; the only such steps are untap (502) and certain
cleanup steps (514) (500.3). When a phase/step begins, "at the beginning of"
abilities trigger and go on the stack at the next priority (500.6). No game
events occur between steps, phases, or turns (500.12).

| Phase | Step | Rule | Turn-based actions | Priority? |
|-------|------|------|--------------------|-----------|
| Beginning | Untap | 502 | Phasing (703.4a), day/night check (703.4b), AP untaps (703.4c) | **No** (502.4) — triggers held to upkeep |
| Beginning | Upkeep | 503 | none (503.1) | Yes — AP gets it once step begins (503.1) |
| Beginning | Draw | 504 | AP draws a card (703.4d, 504.1) | Yes — after the draw (504.2) |
| Precombat main | — (no steps) | 505 | Archenemy scheme (703.4e), Saga lore counters (703.4f), roll Attractions (703.4g) | Yes — after those (505.6); ends on pass-in-succession (505.2) |
| Combat | Beginning of combat | 507 | Choose defending player in some multiplayer (703.4h, 507.1) | Yes (507.2) |
| Combat | Declare attackers | 508 | AP declares attackers (703.4i, 508.1) | Yes — after declaration (508.2) |
| Combat | Declare blockers | 509 | Defending player declares blockers (703.4j, 509.1) | Yes — after declaration (509.2) |
| Combat | Combat damage | 510 | Assign damage (703.4k, 510.1), then deal it simultaneously (703.4m, 510.2) | Yes — after damage dealt (510.3) |
| Combat | End of combat | 511 | none (511.1) | Yes (511.1) |
| Postcombat main | — (no steps) | 505 | none | Yes (505.6); ends on pass-in-succession (505.2) |
| Ending | End | 513 | none (513.1) | Yes (513.1) |
| Ending | Cleanup | 514 | Discard to max hand size (703.4n, 514.1), then remove damage + end "until end of turn" effects (703.4p, 514.2) | **Normally no** (514.3) — exception in §4 |

The combat phase has five steps in order; declare-blockers and combat-damage
are skipped if no attackers (508.8), and there are two combat-damage steps if
any attacker/blocker has first/double strike (506.1). As each step/phase
ends, "until end of [that step/phase]" effects expire and unspent mana
empties (turn-based action 703.4q, 500.5).

## 2. Priority (117)

Priority is the system that decides who may act when no spell/ability is
telling a player to (117.1). The player with priority may **cast spells,
activate abilities, and take special actions** (117.1):

- **Instants** — any time you have priority (117.1a).
- **Noninstants** (sorcery-speed) — your main phase, with priority **and an
  empty stack** (117.1a).
- **Activated abilities** — any time you have priority (117.1b).
- **Special actions** — some any time with priority; others (e.g. play a
  land) only your main phase with priority + empty stack (117.1c; see
  `actions.md` §4). Special actions don't use the stack (116.1).
- **Mana abilities** — whenever you have priority, *or* while paying a mana
  cost, even mid-cast/mid-resolution (117.1d); they resolve immediately, not
  via priority.

**Who gets priority, and when** (117.3):
- AP receives priority at the beginning of most steps/phases, *after*
  turn-based actions are done and beginning-of-step triggers are on the stack
  (117.3a). No priority in the untap step; usually none in cleanup (117.3a).
- AP receives priority after a spell/ability (other than a mana ability)
  resolves (117.3b).
- A player who casts/activates/takes a special action keeps priority
  afterward (117.3c).
- A player who declines passes; the next player in turn order gets priority
  (117.3d).

**Before priority is granted** the game loops: perform all applicable SBAs as
one event, repeat until none; then put triggered abilities on the stack;
repeat the whole loop until no SBAs fire and nothing triggers — then the
player gets priority (117.5).

**Passing.** If all players pass in succession (no actions between passes):
the top object on the stack resolves, or, if the stack is empty, the
phase/step ends (117.4, 500.2).

**Not gated by priority** (117.2): triggered abilities just *wait* — nothing
happens when they trigger; each is put on the stack at the next priority
(117.2a). Static abilities apply continuously, priority irrelevant (117.2b).
Turn-based actions happen automatically at step boundaries, before priority,
and none is granted after end-of-step ones (117.2c). SBAs happen
automatically before priority (117.2d). **No player has priority while a
spell/ability resolves**, even if it asks for choices or mana (117.2e).
Casting/activating with another object already on the stack is acting "in
response"; the newer object resolves first (117.7).

## 3. Combat, step by step (506–511)

Only creatures attack/block; only a player, planeswalker, or battle can be
attacked (506.3). AP is the attacking player; in a two-player game the
nonactive player is the defending player (506.2). A permanent is removed from
combat if it leaves the battlefield, changes controller or protector, phases out, an
effect removes it, the attacked planeswalker/battle stops being one, or an
attacker/blocker regenerates, stops being a creature, or becomes a battle
(506.4).

**Beginning of combat (507)** — in some multiplayer games AP chooses a
defending player (507.1); then AP gets priority (507.2).

**Declare attackers (508)** — AP declares attackers as a turn-based action;
if AP can't comply at any step, the declaration is illegal and the game backs
up (508.1, 733). The declaration procedure (508.1 letters):

| Rule | Step in declaring attackers |
|------|------------------------------|
| 508.1a | Choose attackers — must be untapped, not battles, and have haste or have been controlled continuously since the turn began |
| 508.1b | Announce which player/planeswalker/battle each attacks (if choices exist) |
| 508.1c | Check **restrictions** ("can't attack"); any disobeyed → illegal |
| 508.1d | Check **requirements** ("attacks if able"); obeying fewer than the max possible without breaking a restriction → illegal; costs to attack are never forced |
| 508.1e | Announce banding / "bands with other" groupings |
| 508.1f | Tap the chosen creatures (this is *not* a cost — attacking just taps them) |
| 508.1g | Choose which optional costs ("as ~ attacks") to pay |
| 508.1h | Determine and lock in the total cost to attack |
| 508.1i–j | Activate mana abilities, then pay all costs in any order (no partial payment) |
| 508.1k | Each still-controlled chosen creature becomes an attacking creature |
| 508.1m | Abilities that trigger on attackers being declared trigger |

A creature *put onto the battlefield* attacking is "attacking" but never
"attacked" for triggers (508.4). Then AP gets priority; triggers from the
declaration go on the stack first (508.2, 508.2b). If no attackers, skip
declare-blockers and combat-damage (508.8).

**Declare blockers (509)** — defending player declares blockers as a
turn-based action; can't-comply → illegal + back up (509.1, 733). Procedure
(509.1 letters):

| Rule | Step in declaring blockers |
|------|-----------------------------|
| 509.1a | Choose blockers — untapped, not battles; for each, pick one attacking creature it blocks (attacking that player / their planeswalker / their battle) |
| 509.1b | Check **restrictions** ("can't block", incl. evasion abilities like flying/menace — cumulative); disobeyed → illegal |
| 509.1c | Check **requirements** ("must block"); obeying fewer than the max possible without breaking a restriction → illegal; block costs never forced |
| 509.1d–f | Determine + lock in block costs, activate mana abilities, pay (no partial payment) |
| 509.1g | Each chosen creature becomes a blocking creature |
| 509.1h | Each attacked creature with ≥1 declared blocker becomes *blocked*; others *unblocked* — stays blocked even if all blockers leave |
| 509.1i | Abilities that trigger on blockers being declared trigger |

Then AP gets priority; declaration triggers go on the stack first (509.2,
509.2a).

**Combat damage (510)** — turn-based, two parts: (1) AP announces how each
attacking creature assigns its combat damage, then defending player announces
for each blocking creature (510.1); (2) all assigned damage is dealt
simultaneously — no player can act between assignment and dealing (510.2).
Then AP gets priority (510.3). Assignment rules (510.1 letters):

| Rule | Assignment rule |
|------|------------------|
| 510.1a | Each creature assigns combat damage equal to its power; 0-or-less assigns none |
| 510.1b | Unblocked creature → the player/planeswalker/battle it attacks (none if attacking nothing) |
| 510.1c | Blocked creature → its blockers; one blocker takes all; two+ divided as controller chooses |
| 510.1d | Blocking creature → the creature(s) it blocks, divided as its controller chooses |
| 510.1e | The *total* assignment (not per-creature) is legality-checked; illegal → back up (733) |

**First / double strike** (510.4): if any attacker/blocker has first or
double strike as the combat-damage step begins, only those creatures assign
in that step; the phase then gets a *second* combat-damage step where the
remaining (non-first-strike) creatures and any double strikers assign
(506.1, 510.4).

**Trample / deathtouch interaction.** Trample is a static ability that
modifies attacking-creature damage assignment (702.19a): the controller first
assigns lethal damage to all blockers, then may assign excess to the
defender; lethal accounts for marked damage and same-step damage but ignores
effects that change actual damage dealt (702.19b). **Deathtouch makes any
nonzero combat damage from that source count as lethal** when checking for
excess (702.2c) — so a 1-power deathtouch trampler needs assign only 1 to a
blocker before the rest tramples through. With no blockers present at
assignment, a blocked trampler assigns to the defender as if all blockers got
lethal (702.19d).

**End of combat (511)** — no turn-based actions; AP gets priority (511.1).
"At end of combat" triggers fire as the step begins; "until end of combat"
effects expire at the *end of the combat phase* (511.2, 500.5a). When the
step ends, all creatures/battles/planeswalkers are removed from combat and
the postcombat main phase begins (511.3).

## 4. Cleanup (514)

First (514.1) the AP discards down to maximum hand size (normally seven) as a
turn-based action. Second (514.2), simultaneously: all damage marked on
permanents (including phased-out ones) is removed and all "until end of turn"
and "this turn" effects end. Normally **no player gets priority** in cleanup
(514.3). Exception (514.3a): if any SBAs would be performed or any triggered
abilities are waiting (including "at the beginning of the next cleanup step"),
those SBAs are performed, the triggers go on the stack, and AP gets priority;
players may act. Once the stack empties and all players pass in succession,
**another cleanup step begins** — the loop repeats until a cleanup step
passes with nothing to do.

## 5. Extra turns, phases, and steps (500.7–500.11)

- **Extra turns** are added directly after the specified turn, one at a time;
  if multiple players get extra turns they're added in APNAP order, and the
  most recently created turn is taken first (500.7) — i.e. LIFO. See
  `state.md` for how the extra-turn queue interacts with skips.
- **Extra phases** are added directly after the specified phase; among
  multiple added after the same phase, the most recently created occurs first
  (500.8). Only the first main phase is precombat; all others (including a
  main phase from an added combat) are postcombat (505.1a).
- **Extra steps** are added directly after or before a specified step; among
  several added after the same step, the most recent occurs first (500.9).
- An effect adding a step "after a phase" first creates the containing phase
  with only that step; other steps of that phase are skipped (500.10).
  "You get" extra steps/phases targeting another player's turn add nothing
  (500.10a).
- To **skip** a step/phase/turn is to proceed past it as if it didn't exist
  (500.11; see 614.10).

## 6. Engine note

Per turn, iterate the phases (500.1) and, for phases with steps, the steps in
order (501.1, 506.1, 512.1). For each step/phase:

1. **On begin:** expire "until that step/phase" effects (500.4); perform the
   step's *begin* turn-based actions (703.3, `actions.md` §2); queue "at the
   beginning of" triggers (500.6) — they go on the stack at the first
   priority.
2. **Priority loop (only if the step grants priority):** run the
   SBA-then-trigger loop until stable (117.5), grant AP priority (117.3a),
   then for each player in turn order: act (return to the SBA loop) or pass;
   on all-pass-in-succession, resolve the top of the stack and re-loop, or if
   the stack is empty, end the step (117.4, 500.2). Untap grants no priority;
   cleanup grants none unless 514.3a fires (502.4, 514.3).
3. **On end:** perform any *end* turn-based actions, expire "until end of that
   step/phase" effects, then empty mana pools (703.4q, 500.5).

The untap step ends purely when its actions complete (500.3); a normal
cleanup step likewise (500.3), but re-runs if 514.3a triggers. Maintain the
extra-turn / extra-phase / extra-step queues as LIFO insertions per
500.7–500.10.
