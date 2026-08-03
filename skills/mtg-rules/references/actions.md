# Game Actions — Everything the Game Can Do

*Synthesized from the Comprehensive Rules effective 2026-06-19
(`data/rules/cr.json`). Orientation only — verify load-bearing specifics
with `scripts/rule` before citing. Run `scripts/cite check` after CR
refreshes.*

The closed, enumerable categories of things that happen in a game. Closed
lists are enumerated in full; the open keyword-action list points at
`data/rules/keywords.json`.

## 1. Events

Anything that happens in a game is an *event* (700.1). One "happening" may
be one event to one ability and several to another; triggered-ability and
replacement text define the events they watch for (700.1). Distinguish:
an **action** is something a player or the game does; an **event** is the
fact of it happening (the unit triggers and replacements match against);
an **effect** is what a resolving spell/ability or a static ability does to
the game (609). Many events occur during one resolution (700.1).

## 2. Turn-based actions

Game actions that happen automatically when a step/phase begins or ends;
they don't use the stack, aren't controlled by any player, and are dealt
with before SBAs, triggers, and priority (703.1, 703.2, 703.3). Abilities
that merely *watch* for a step beginning are triggered, not turn-based
(703.1a). Full list (703.4):

| Rule | Action | Step / phase |
|------|--------|--------------|
| 703.4a | Phasing: AP's permanents phase out/in simultaneously | Untap, on begin |
| 703.4b | Day/night designation check (only if game has one) | Untap, after phasing |
| 703.4c | AP determines and untaps their permanents simultaneously | Untap, after day/night check |
| 703.4d | Active player draws a card | Draw, on begin |
| 703.4e | Archenemy sets top scheme in motion | Precombat main, on begin |
| 703.4f | AP puts a lore counter on each Saga they control | Precombat main, on begin |
| 703.4g | AP rolls to visit their Attractions | Precombat main, after lore counters |
| 703.4h | AP chooses defending player (some multiplayer games) | Begin combat, on begin |
| 703.4i | Active player declares attackers | Declare attackers, on begin |
| 703.4j | Defending player declares blockers | Declare blockers, on begin |
| 703.4k | Each player in APNAP order announces how each attacking or blocking creature they control assigns its combat damage | Combat damage, immediately on begin (510.1) |
| 703.4m | All combat damage dealt simultaneously | Combat damage, after assignment |
| 703.4n | AP discards down to maximum hand size | Cleanup, on begin |
| 703.4p | Damage removed; "until end of turn"/"this turn" effects end | Cleanup, after discard |
| 703.4q | Unspent mana empties from each pool | As each step/phase ends |

## 3. State-based actions (SBAs)

Automatic actions performed whenever listed conditions are met; no stack,
no player control (704.1, 704.2). **Checked** each time a player *would*
get priority: all applicable SBAs are performed **simultaneously as a
single event**, then re-checked; once none fire, waiting triggers go on the
stack, then check again, until stable (704.3). They also run during cleanup
(704.3). SBAs ignore mid-resolution game state (704.4). If several SBAs
share one result, a single replacement can replace them all (704.7); a
permanent leaving via an SBA uses last-known-info from before the batch
(704.8). Full list (704.5):

| Rule | Condition → action |
|------|--------------------|
| 704.5a | Player at 0 or less life loses the game |
| 704.5b | Player who drew from an empty library loses the game |
| 704.5c | Player with 10+ poison counters loses the game |
| 704.5d | Token outside the battlefield ceases to exist |
| 704.5e | Spell copy off the stack (or card copy off stack/battlefield) ceases to exist |
| 704.5f | Creature with 0 or less toughness → owner's graveyard (regen can't replace) |
| 704.5g | Creature (toughness > 0) with lethal marked damage is destroyed (704.5g) |
| 704.5h | Creature (toughness > 0) dealt damage by a deathtouch source since the last SBA check is destroyed (regeneration can replace) (704.5h) |
| 704.5i | Planeswalker with 0 loyalty → owner's graveyard |
| 704.5j | Legend rule: controller of same-name legendaries chooses one to keep; the rest go to their owners' graveyards (704.5j) |
| 704.5k | World rule: only newest world permanent survives |
| 704.5m | Aura attached illegally / unattached → owner's graveyard |
| 704.5n | Equipment/Fortification attached illegally becomes unattached, stays |
| 704.5p | Battle/creature (or other non-Aura/Equip/Fort) attached → unattached, stays |
| 704.5q | +1/+1 and -1/-1 counters on a permanent annihilate in pairs |
| 704.5r | Counters above an enforced max are removed down to the max |
| 704.5s | Saga at/past final chapter (no pending trigger) is sacrificed |
| 704.5t | Venture marker on bottom room (no pending trigger) → dungeon removed from game |
| 704.5u | Space sculptor: assign sector designations to creatures lacking one |
| 704.5v | Battle with 0 defense (no pending trigger) → owner's graveyard |
| 704.5w | Battle with no protector and no attackers → choose protector or graveyard |
| 704.5x | Siege whose controller is its protector → choose opponent protector or graveyard |
| 704.5y | Multiple same-controller Roles on a permanent: keep newest, rest → graveyard |
| 704.5z | Permanent with start your engines! and no speed → speed becomes 1 |

**Variant SBAs** (apply only in those formats) (704.6): Two-Headed Giant
team at 0 life loses (704.6a); 2HG team with 15+ poison loses (704.6b);
**Commander** — 21+ combat damage from one commander loses (704.6c), and a
commander newly in graveyard/exile may be moved to the command zone
(704.6d); Archenemy non-ongoing scheme (no pending trigger) goes face down
to bottom of scheme deck (704.6e); Planechase face-up phenomenon (no
pending trigger) → planar controller planeswalks (704.6f).

## 4. Special actions

Actions a player may take **while holding priority** that don't use the
stack; not auto-generated like turn-based/SBAs (116.1). After taking one,
that player gets priority again (116.3). Full list (116.2a–m):

| Rule | Action | Timing |
|------|--------|--------|
| 116.2a | Play a land | Priority + empty stack, own main phase; once/turn by default |
| 116.2b | Turn a face-down creature face up | Any time with priority |
| 116.2c | Take an action to end a continuous/delayed effect | Any time with priority (or as effect allows) |
| 116.2d | Ignore a static ability's effect for a duration | Any time with priority |
| 116.2e | Discard Circling Vultures | Any time you could cast an instant |
| 116.2f | Exile a suspend card from hand | When you could begin casting it |
| 116.2g | Pay {3} to bring a companion to hand | Priority + empty stack, own main phase; once/game |
| 116.2h | Pay {2} to foretell (exile face down) | Any time with priority during your turn |
| 116.2i | Planechase: roll the planar die | Priority + empty stack, own main phase (escalating cost) |
| 116.2j | Conspiracy Draft: turn a face-down conspiracy face up | Any time with priority |
| 116.2k | Exile a plot card from hand | Priority + empty stack, your own turn |
| 116.2m | Pay an unlock cost to unlock a locked half | Priority + empty stack, own main phase |

## 5. Keyword actions

Specialized verbs in rules text with defined meanings (701.1). The
machine-readable list is `data/rules/keywords.json` (`.keywordActions`).
Full enumeration (701.2–701.68), grouped thematically:

- **Casting & the stack** — Activate (701.2), Cast (701.5), Play (701.18),
  Counter (701.6).
- **Zone movement** — Create (701.7), Destroy (701.8), Discard (701.9),
  Exile (701.13), Sacrifice (701.21), Mill (701.17), Search (701.23),
  Shuffle (701.24), Reveal (701.20), Regenerate (701.19).
- **Permanent state** — Attach (701.3), Tap and Untap (701.26), Transform
  (701.27), Convert (701.28), Meld (701.42), Manifest (701.40), Cloak
  (701.58), Exert (701.43).
- **Library / top-of-deck** — Scry (701.22), Surveil (701.25), Fateseal
  (701.29), Behold (701.4).
- **Numeric / counters** — Double (701.10), Triple (701.11), Exchange
  (701.12), Proliferate (701.34), Bolster (701.39), Support (701.41),
  Monstrosity (701.37), Adapt (701.46), Amass (701.47), Endure (701.63),
  Incubate (701.53).
- **Combat / aggression** — Fight (701.14), Goad (701.15), Detain (701.35),
  Blight (701.68), Suspect (701.60).
- **Card advantage / value** — Investigate (701.16), Populate (701.36),
  Explore (701.44), Learn (701.48), Connive (701.50), Discover (701.57),
  Collect Evidence (701.59), Forage (701.61), Manifest Dread (701.62),
  Harness (701.64).
- **Choices / votes / dice** — Vote (701.38), Clash (701.30), Assemble
  (701.45), Face a Villainous Choice (701.55), The Ring Tempts You (701.54),
  Time Travel (701.56).
- **Bending (Avatar)** — Airbend (701.65), Earthbend (701.66), Waterbend
  (701.67).
- **Subgame structures** — Venture into the Dungeon (701.49), Open an
  Attraction (701.51), Roll to Visit Your Attractions (701.52), Planeswalk
  (701.31), Set in Motion (701.32), Abandon (701.33).

## 6. The main loop

The engine cycle once a step/phase has begun (turn-based actions already
handled; 703.3):

1. **Priority handshake.** Before any player gets priority, perform all
   SBAs (repeat until none), then put waiting triggers on the stack (APNAP
   order when multiple players have waiting triggers, 603.3b), then
   re-check — repeat until stable (704.3, 117.5). The active player gets
   priority at step/phase start and after each resolution; a player keeps
   priority after acting (117.3a, 117.3b, 117.3c).
2. **Act or pass.** The player with priority may **cast a spell** (601,
   instants any time; sorcery-speed needs empty stack + own main phase,
   117.1a), **activate an ability** (602, any time, 117.1b), or **take a
   special action** (116, 117.1c). Mana abilities resolve immediately
   (117.1d). Triggered abilities just wait — they hit the stack at the next
   priority check (603.3, 117.2a). Acting → return to step 1.
3. **Passing.** A player choosing no action passes; priority moves to the
   next player in turn order (117.3d). If **all players pass in
   succession** (117.4): if the stack has an object, the top object
   resolves (608.1) — then back to step 1; if the stack is empty, the
   step/phase ends.
4. **Resolution.** A resolving spell/ability follows the effect pipeline
   (608.1) and may instruct players to make choices, but **no player has
   priority during resolution** (117.2e). Player choices otherwise occur
   when casting (targets, modes, costs: 601.2a–c), when activating (602),
   or when putting a triggered ability on the stack (603.3, modes 700.2b).

## 7. Illegal actions

If a player takes an illegal action or can't legally complete one, the
entire action is reversed and payments canceled — no triggers fire, no
effects apply, and a spell returns whence it came (733.1). Players may also
reverse legal mana abilities used during the attempt, but actions touching
actions that moved cards to a library, moved cards from a library to any
zone other than the stack (casting from a library can be reversed), caused
a library to be shuffled, or caused cards from a library to be revealed are
never reversed (733.1).
