# Turn Structure, Priority, and Combat

*Synthesized from the Comprehensive Rules effective 2026-09-25
(`data/rules/cr.json`).*

How an engine sequences a turn: five phases, their steps, who gets priority
when, and the combat sub-machine. A turn = beginning, precombat main,
combat, postcombat main, ending — every turn, even if empty (500.1). The
beginning, combat, and ending phases break into steps that proceed in order
(500.1). The turn-based actions referenced below are mapped in full in
`actions.md` §2 (703.4 letters); this doc cross-cites them rather than
restating their text.

Sibling pointers for combat questions this doc doesn't derive: attack/block
triggers → `events.md`; attack/block requirements and restrictions →
`deontics.md`; multiplayer combat and first-turn variants → `variants.md`.

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
| Beginning | Draw | 504 | AP draws a card (703.4d, 504.1); in a two-player game the starting player skips the draw step of their first turn (103.8a; multiplayer differs, 103.8b-c, see `variants.md`) | Yes — after the draw (504.2) |
| Precombat main | — (no steps) | 505 | Archenemy scheme (703.4e), Saga lore counters (703.4f), roll Attractions (703.4g) | Yes — after those (505.6); ends on pass-in-succession (505.2) |
| Combat | Beginning of combat | 507 | Choose defending player in some multiplayer (703.4h, 507.1) | Yes (507.2) |
| Combat | Declare attackers | 508 | AP declares attackers (703.4i, 508.1) | Yes — after declaration (508.2) |
| Combat | Declare blockers | 509 | Defending player declares blockers (703.4j, 509.1) | Yes — after declaration (509.2) |
| Combat | Combat damage | 510 | Assign damage (703.4k, 510.1), then deal it simultaneously (703.4m, 510.2) | Yes — after damage dealt (510.3) |
| Combat | End of combat | 511 | none (511.1) | Yes (511.1) |
| Postcombat main | — (no steps) | 505 | none | Yes (505.6); ends on pass-in-succession (505.2) |
| Ending | End | 513 | none (513.1) | Yes (513.1) |
| Ending | Cleanup | 514 | Discard to max hand size (703.4n, 514.1), then remove damage + end "until end of turn" effects (703.4p, 514.2) | **Normally no** (514.3) — exception in §4 |

"At the beginning of [the next] end step" abilities that enter or are created
during the end step wait for the next turn's end step; the step doesn't back
up (513.2). "Until end of turn" effects are unaffected and still end in
cleanup (513.2, 514.2).

The combat phase has five steps in order; declare-blockers and combat-damage
are skipped if no creature was declared as an attacker or put onto the
battlefield attacking (508.8, 506.1), and there are two combat-damage steps
if any attacker/blocker has first/double strike (506.1). As each step/phase
ends, "until end of [that step/phase]" effects expire and unspent mana
empties (turn-based action 703.4q, 500.5).

**Untap step selection (502.3).** The AP first determines which of their
permanents will untap, then untaps them all simultaneously. Normally all of
them untap, but effects can keep some from untapping (502.3, 703.4c). Effects
that untap other players' permanents during this step (e.g. Seedborn Muse)
untap them at the same time (Bender's Waterskin ruling [2025-10-02]). "Doesn't
untap during [your / its controller's] untap step" and "you may choose not to
untap" act on that determination. They neither replace the untap event nor
forbid untapping. A replacement keyed to the permanent untapping during the
untap step doesn't apply, "because it wouldn't untap" (Freyalise's Winds
ruling [2009-10-01]). Spells and abilities can still untap it (Alirios,
Enraptured ruling [2020-01-24]). A stun counter, by contrast, is a replacement
on any untap (122.1d). *Inference* from the Freyalise's Winds ruling: a stun
counter on a permanent held by a "doesn't untap" effect isn't removed during
that untap step. A one-shot "doesn't untap during its controller's next untap
step" effect:

- applies at the next untap step that isn't skipped (614.10a; Yosei, the
  Morning Star ruling [2017-11-17]), and expires during it even if the
  permanent is already untapped (Spore Cloud ruling [2008-10-01]);
- doesn't accumulate. Several such effects all expire during the same untap
  step (701.43b for exert; Niblis of Frost ruling [2016-07-13]). This differs
  from "skip your next untap step", which skips one step per effect (614.10a;
  Yosei ruling);
- tracks the permanent, not its controller. After a control change it applies
  at the new controller's next untap step (Ajani Vengeant ruling
  [2008-10-01]).

An effect scoped to "its controller's untap step" doesn't apply when the
permanent untaps during another player's untap step (Bender's Waterskin
ruling [2025-10-02]). *Engine inference:* model all of these as a filter on
502.3's selection, not as an untap replacement or a standing "can't untap".

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
one event, repeating until a check performs none; then put triggered
abilities on the stack; repeat until no SBAs are performed and no abilities
trigger, then the player gets priority (117.5).

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
nonactive player is the defending player (506.2).

"Defending player" in an ability of an attacking creature, or in a spell or
ability that refers to both an attacking creature and a defending player,
means the player that creature is attacking, the controller of the
planeswalker it's attacking, or the protector of the battle it's attacking,
unless otherwise specified. Once the creature is no longer attacking, it
means the one it was attacking before it was removed from combat (508.5;
protector, 310.9d). In multiplayer it always names one specific player. It is
determined separately for each attacking creature a spell or ability could
apply to, and when several defending players could be chosen, the spell's or
ability's controller chooses one (508.5a, 802.2a). *Engine inference:*
resolve the referent from an attacker parameter, and keep each attacker's
last attack target after it leaves combat so the referent survives removal.

A permanent is removed from combat if it leaves the battlefield, changes
controller or protector, phases out, an effect removes it, the attacked
planeswalker/battle stops being one, or an attacker/blocker regenerates,
stops being a creature, or becomes a battle (506.4). Tapping or untapping a
declared attacker or blocker doesn't remove it from combat or stop its combat
damage (506.4b). Effects that would have stopped it attacking or blocking
don't remove it once it is declared (506.4a). If the planeswalker or battle it
attacks is removed from combat, the creature stays an attacking creature that
attacks nothing. It can still be blocked; if unblocked it deals no combat
damage (506.4c, 510.1b), except as allowed by trample over planeswalkers
(702.19e).

"Attacks alone" means the creature was the only one declared as an attacker;
"attacking alone" means it is the only attacking creature. "Blocks alone" and
"blocking alone" are the blocker counterparts (506.5). Exalted uses "attacks
alone" (702.83b). "Attacks a player alone" requires the creature to be
declared attacking a player and no other creature to be declared attacking
that same player. "Attacking a player alone" is the current-state form
(506.6). Creatures attacking that player's planeswalkers or battles, or other
players, don't count, so this differs from 506.5 even in a two-player game
(official ruling, Jiang Yanggu, Alone, 2026-08-21). The "attacks"/"blocks"
forms count only declared creatures; the "attacking"/"blocking" forms count
current state.

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

Then AP gets priority; triggers from the declaration go on the stack first
(508.2, 508.2b). If no creature was declared as an attacker or put onto the
battlefield attacking, skip declare-blockers and combat-damage (508.8, 506.1).

**Entering combat without a declaration (508.4, 509.4).** A creature put onto
the battlefield attacking, or that an effect states is attacking, is
*attacking* until it's removed from combat or the combat phase ends. For the
purposes of trigger events and effects it never "attacked" (508.4), so
"whenever ~ attacks" doesn't trigger (508.3a). Its controller chooses which
defending player, planeswalker a defending player controls, or battle a
defending player protects it attacks, unless the effect specifies one
(508.4). Entering or being stated attacking doesn't tap it: the tap belongs
to the declaration (508.1f), and a creature put onto the battlefield
attacking enters untapped unless the effect says otherwise (110.5b).
Requirements and restrictions on declaring attackers don't apply to it
(508.4c). In these cases a permanent still enters but is never an attacking
creature (506.3a–c, 506.3f, 508.4a–b):

- the specified player has left the game, or the specified planeswalker or
  battle has left the battlefield, stopped being a planeswalker or battle, or
  is no longer controlled or protected by a defending player (506.3c,
  508.4a). For an "is attacking" effect this is judged as the effect resolves
  (508.4b);
- it's a noncreature permanent (506.3a) or a creature that's also a battle
  (506.3f);
- its controller isn't an attacking player (506.3b).

A resolving effect that would make a battle an attacking or blocking creature
does nothing for that part (506.3g). Entering during declare blockers or
later makes it unblocked (506.3d, 508.4d; see the blocked/unblocked state
under Declare blockers). Blocking mirrors this. A creature put onto the
battlefield blocking is *blocking* but, for the purposes of trigger events and
effects, never "blocked" (509.4), so "whenever ~ blocks" doesn't trigger
(509.3a). Its controller chooses which attacker it blocks unless the effect
specifies one (509.4), and declaration requirements and restrictions don't
apply (509.4b). It enters but never blocks if the specified attacker is no
longer attacking, or isn't attacking the entering creature's controller, a
planeswalker they control, or a battle they protect (509.4a, 506.3e).

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
| 509.1h | Each attacking creature with ≥1 declared blocker becomes *blocked*; each with none becomes *unblocked*. Unchanged until it's removed from combat, an effect says it becomes blocked or unblocked, or the combat phase ends — it stays blocked even if all its blockers leave |
| 509.1i | Abilities that trigger on blockers being declared trigger |

Then AP gets priority; declaration triggers go on the stack first (509.2,
509.2a).

**Blocked / unblocked is a three-valued combat state of attacking creatures**
(not a status in the 110.5 sense). An attacking creature is neither until the
declare blockers step assigns one or an effect says it becomes blocked
(509.1h): "Before then, attacking creatures are neither blocked nor unblocked"
(Ninja of the Deep Hours ruling [2021-03-19]). The exception is a creature put
onto the battlefield attacking during the declare blockers, combat damage, or
end of combat step, which enters unblocked (508.4d). A creature that isn't
attacking is neither (glossary "Blocked Creature", "Unblocked Creature"), and
removal from combat clears both (506.4). After that point the state changes
only when an effect says the creature becomes blocked or unblocked, including
an effect that puts a creature onto the battlefield blocking it (509.1h,
509.3c). The state doesn't follow the current blockers. A blocked creature
whose blockers are all gone stays blocked and assigns no combat damage
(510.1c) unless it has trample or trample over planeswalkers (702.19d) or an
effect lets it assign as though it weren't blocked. *Engine inference:* store
the state on each attacking creature as one of three values (none / blocked /
unblocked) instead of deriving it. "Unblocked" is not ¬blocked, and "blocked"
is not "has a blocker". So ninjutsu's "Return an unblocked attacking creature
you control" (702.49a) has no legal choice before blockers are declared.
Sneak's "unblocked creature you control" (702.190a) never matches a creature
that isn't attacking.

Attack and block trigger matching, including "attacks and isn't blocked"
(508.3f, 509.3g) and the once-per-combat rules for "blocks" and "becomes
blocked" (509.3a, 509.3c): `events.md`.

**Combat damage (510)** — turn-based, two parts: (1) AP announces how each
attacking creature assigns its combat damage, then defending player announces
for each blocking creature (510.1); (2) all assigned damage is dealt
simultaneously — no player can act between assignment and dealing (510.2).
Then AP gets priority (510.3). Assignment rules (510.1 letters):

| Rule | Assignment rule |
|------|------------------|
| 510.1a | Each creature assigns combat damage equal to its power; 0-or-less assigns none |
| 510.1b | Unblocked creature → the player/planeswalker/battle it attacks (none if attacking nothing) |
| 510.1c | Blocked creature → its current blockers. None left → assigns no combat damage (trample overrides this, 702.19d; card effects that let it assign "as though it weren't blocked" also can). One blocker → all. Two or more → divided as its controller chooses (with banding the defending player chooses instead, 702.22j) |
| 510.1d | Blocking creature → the creature(s) it blocks, divided as its controller chooses |
| 510.1e | The *total* assignment (not per-creature) is legality-checked; illegal → back up (733) |

**First / double strike** (510.4): if any attacker/blocker has first or
double strike as the combat-damage step begins, only those creatures assign
in that step; the phase then gets a *second* combat-damage step (506.1) where
the remaining attackers/blockers that had neither first strike nor double
strike *as the first combat-damage step began* (a snapshot), plus remaining
creatures that *currently* have double strike, assign (510.4; giving or
removing first strike after the first step doesn't change this, 702.7c;
losing double strike during the first combat damage step stops the second
hit, 702.4c).

**Trample / deathtouch interaction.** Trample is a static ability that
modifies attacking-creature damage assignment (702.19a). Lethal damage must
be assigned to every blocker before *any* damage can go to the
player/planeswalker/battle it attacks; the controller may instead keep all
damage on the blockers, and excess may go to blockers or to that attack target
(702.19b). When the creature attacks a planeswalker or battle, excess can go
only to that permanent, never to its controller or protector (702.19b,
702.19f). Trample over planeswalkers is the exception, and only for
planeswalkers: once lethal damage is assigned to every blocker and damage at
least equal to the planeswalker's loyalty is assigned to it, further excess
may go to that planeswalker's controller (702.19c). If that planeswalker has
been removed from combat, the excess may go to the defending player
(702.19e). Lethal accounts for marked damage and same-step damage but ignores
effects that change actual damage dealt (702.19b). **Deathtouch makes any
nonzero combat damage from that source count as lethal** when checking for
excess (702.2c) — so a 5-power deathtouch trampler blocked by a 4/4 needs
assign only 1 to it; the other 4 may go to the player (702.2c, 702.19b). With
no blockers present at assignment, a blocked trampler assigns to the defender
as if all blockers got lethal (702.19d).

**End of combat (511)** — no turn-based actions; AP gets priority (511.1).
"At end of combat" triggers fire as the step begins; "until end of combat"
effects expire at the *end of the combat phase* (511.2, 500.5a). When the
step ends, all creatures/battles/planeswalkers are removed from combat and
the postcombat main phase begins (511.3).

**Combat-relative timing restrictions (506.8).** These are restrictions of
the form "Cast this spell only [before/after] [point]", where the point is
"attackers are declared", "blockers are declared", "the combat damage step",
"the end of combat step", "the combat phase", or "combat" (506.8). Activation
restrictions worded the same way follow the same rules (506.8g).

- "Attackers / blockers are declared" names the turn-based declaration. The
  boundary is the beginning of the declare attackers or declare blockers step,
  whether or not any creature is declared (506.8a, 506.8b).
- A restriction that also says "during combat" or "during a certain player's
  combat phase" applies in every combat phase of the turn (506.8c). Any other
  before/after restriction refers only to the turn's first combat phase
  (506.8d).
- When the point is missing: if the declare blockers and combat damage steps
  are skipped (no creature declared as an attacker or put onto the battlefield
  attacking, 508.8), "only before [point]" closes when the declare attackers
  step ends. If the relevant combat phase is skipped, it closes when the
  precombat main phase ends (506.8e). "Only during combat after blockers are
  declared" can't be used in a combat phase whose declare blockers step is
  skipped (506.8f). The CR gives no rule for "only after [point]" when that
  point is skipped (e.g. Glyph of Reincarnation's "only after combat" in a
  turn whose combat phase is skipped): `UD-37`
  in `underdetermined.md`.

A creature "had to attack" only if an effect required it to attack when
attackers were declared. Having no other legal attack doesn't count (506.7).

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
  most recently created turn is taken first (500.7). A global LIFO stack is an
  engine simplification, valid only while every grant is "after this one";
  see `state.md` §8 for the skip interaction (614.10a).
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

## 6. Ending the turn or the combat phase (724)

An effect that ends the turn (724.1), or ends the combat phase (724.2; one
card, Mandate of Peace), is carried out by a fixed procedure that differs from
normal resolution (608), in order:

1. Triggered abilities that triggered before the procedure began but aren't on
   the stack yet cease to exist (724.1a, 724.2a).
2. Every object on the stack is exiled, including the resolving one. Once
   exiled, objects not represented by cards (abilities, spell copies) cease to
   exist at the next SBA check (724.1b, 724.2b). Exiling isn't countering, so
   "can't be countered" doesn't stop it (Time Stop ruling [2004-12-01];
   Sundial of the Infinite ruling [2011-09-22]).
3. SBAs are checked. No player gets priority and no triggered ability is put
   on the stack (724.1c, 724.2c).
4. *End the turn:* the current phase/step ends. If this happens during combat,
   all creatures and planeswalkers are removed from combat. The game skips
   straight to the cleanup step (724.1d). *End combat:* the combat phase ends,
   all creatures and planeswalkers are removed from combat, "until end of
   combat" effects expire, and the game skips to the next phase, usually
   postcombat main (724.2d).

The skipped steps' beginning triggers never fire that turn: "at the beginning
of the end step" (724.1e) and "at end of combat" (724.2e). Those abilities next
trigger in a later turn's end step (Sundial of the Infinite ruling
[2011-09-22]). Abilities that trigger during the procedure go on the stack in
the cleanup step, AP gets priority, and another cleanup step follows (724.1f;
the §4 loop). If none triggered, no player gets priority in that cleanup
unless 514.3a applies (724.1f, 514.3a). For ending combat, they go on the
stack in the following phase (724.2f). Ending the turn during cleanup starts a
new cleanup step (724.1d). Ending the combat phase outside a combat phase does
nothing (724.2g).

**Battle gap.** 724.1d and 724.2d remove only creatures and planeswalkers from
combat, while a normal end of combat removes battles too (511.3). No rule says
whether an attacked battle stays "attacked" after an early end. This is
observable chiefly through 310.11's "a battle that isn't being attacked";
704.5x instead keys on attacking creatures, and none remain (508.1k):
`UD-38` in `underdetermined.md`.

## 7. Engine note

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
3. **On end:** expire "until end of [this step/phase]" effects, then empty
   mana pools. Mana emptying is the only end-of-step turn-based action (500.5,
   703.4q). "Until end of combat" effects expire as the combat phase ends, not
   as the end of combat step begins (500.5a); this is how firebending mana
   survives combat steps and then empties (702.189a). As the end of combat step
   ends, also remove all creatures, battles and planeswalkers from combat
   (511.3). The CR does not order this removal against 500.5's expiry; the
   end-the-combat procedure removes them first (724.2d). If the engine fixes an
   order, register it in `underdetermined.md`. As the declare attackers step
   ends, skip declare blockers and combat damage only if no creature was
   declared as an attacker or put onto the battlefield attacking during this
   combat phase. This is a history check, not a check of current attackers: a
   declared attacker that has since left combat still prevents the skip
   (508.8).

The untap step ends purely when its actions complete (500.3); a normal
cleanup step likewise (500.3), but re-runs if 514.3a triggers. Maintain the
extra-turn / extra-phase / extra-step queues so that, among grants added
after the same point, the most recently created comes first (500.7–500.9); a
single global LIFO stack is only an engine simplification (§5).
