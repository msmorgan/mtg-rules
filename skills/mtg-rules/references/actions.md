# Game Actions — Everything the Game Can Do

*Synthesized from the Comprehensive Rules effective 2026-09-25
(`data/rules/cr.json`).*

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
| 703.4f | AP puts a lore counter on each Saga they control with one or more chapter abilities | Precombat main, on begin (on the archenemy's turn, after 703.4e) |
| 703.4g | If AP controls any Attractions, AP rolls to visit them | Precombat main, after lore counters |
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
no player control (704.1, 704.2).

Abilities that watch for a game state are triggered abilities (state
triggers, 603.8), not SBAs (704.1a); this is the counterpart of 703.1a in
section 2. Some rules act whenever a state holds yet are neither: ascend on
a permanent and storied are static abilities ("Any time you control ...",
702.131b, 702.195a), and the daybound/nightbound mismatch transforms and
day/night initialization are immediate rule actions ("Immediate rule
actions" below). Gaining the city's blessing or an enduring story reapplies
continuous effects before trigger checks (702.131d, 702.195c;
`designations.md`); immediate win/loss routes live in `outcomes.md` section
3. Conversely, an SBA is a game action, not an ability of the object it acts
on (704.1), so "loses all abilities" never removes an SBA. It changes an
SBA's result only through what the condition reads: 704.5r's "an ability
that says ..."; 714.4's "one or more chapter abilities", so a Saga stripped
of its chapters is not sacrificed (Saga paragraph below; Summon: Anima
ruling [2025-06-06]); and an Aura's legal objects, which its enchant ability
sets (702.5a, 303.4c), so an Aura that loses its abilities can't legally
enchant anything and goes to the graveyard under 704.5m (Immovable Rod
ruling [2021-07-23], which also notes an Equipment that loses equip stays
attached).

**Checked** each time a player *would* get priority: the game checks every
listed condition, then performs all applicable SBAs **simultaneously as a
single event** (704.3). The loop is keyed on SBAs *performed*, not on
conditions that hold: if any SBA was performed, check again; otherwise put
waiting triggers on the stack, then check again; once a check performs no
SBA and no trigger is waiting, the player gets priority (704.3; 117.5:
"until no state-based actions are performed"). A condition can hold while
nothing is performed: an indestructible creature with lethal damage ignores
704.5g (702.12b), and a player at 0 life under "can't lose the game" stays
in because the "can't" takes precedence (101.2; Platinum Angel ruling
[2009-10-01]: "You keep playing"; `outcomes.md` section 2). An engine that
loops while any condition holds, or counts proposed rather than performed
actions, never reaches priority in those states. Whether an SBA whose event
is replaced (614.6, 704.7) counts as performed is not stated: see
`underdetermined.md` UD-17. SBAs also run during
cleanup (704.3). SBAs ignore mid-resolution game state (704.4). If several
SBAs share one result, a single replacement can replace them all (704.7); a
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
| 704.5k | World rule: all world permanents except the one that has had the world supertype for the shortest time → owners' graveyards; on a tie, all go |
| 704.5m | Aura attached illegally / unattached → owner's graveyard |
| 704.5n | Equipment/Fortification attached illegally becomes unattached, stays |
| 704.5p | Battle/creature (or other non-Aura/Equip/Fort) attached → unattached, stays |
| 704.5q | +1/+1 and -1/-1 counters on a permanent annihilate in pairs |
| 704.5r | Counters above an enforced max are removed down to the max |
| 704.5s | Saga with one or more chapter abilities and lore counters >= its final chapter number (714.2d), not the source of a chapter ability that has triggered but not yet left the stack → its controller sacrifices it |
| 704.5t | Venture marker on bottom room (no pending trigger) → dungeon removed from game |
| 704.5u | Space sculptor: assign sector designations to creatures lacking one |
| 704.5v | Siege with 0 defense (no pending trigger) → owner's graveyard |
| 704.5w | Non-Siege battle with 0 defense → owner's graveyard |
| 704.5x | Unattacked battle with no protector → choose one allowed by its type (controller if typeless), or graveyard if none |
| 704.5y | Battle with an ineligible protector → choose an eligible one, or graveyard if none |
| 704.5z | Multiple same-controller Roles on a permanent: keep newest, rest → graveyard |
| 704.5aa | Player controls a start-your-engines! permanent and has no speed → that player's speed becomes 1 |

**Saga final chapter number** (704.5s, 714.4). It is read from the chapter
abilities the Saga *currently* has: the greatest chapter value among them,
with `{rN1}, {rN2}--` counting as both values (714.2c, 714.2d; notation
107.15a-107.15b). It is not a count of printed chapter entries: a Saga
printed "I --" and "II, III --" finishes at 3. The final chapter ability is
the one bearing that number (714.2e). A Saga with no chapter abilities has
final chapter number 0 (714.2d). The sacrifice SBA (714.4, 704.5s) and the
precombat-main lore counter (714.3c, 703.4f) both require "one or more
chapter abilities", and read ahead's entry choice is bounded by the same
number (714.3b). So a Saga stripped of its chapters gets no lore counters
and is not sacrificed by 714.4 (Summon: Anima ruling [2025-06-06]: such a
Saga "will not be sacrificed as a state-based action. It will also not gain
a lore counter at the beginning of each of its controller's first main
phases"). That covers layer-6 ability removal (613.1f) and Urza's Saga under
Blood Moon, which loses its rules-text abilities but keeps the enchantment
type Saga (305.7, 205.3h); the Blood Moon application is derived, no ruling
names it. The sacrifice also waits while the Saga is the source of a chapter
ability that has triggered but not yet left the stack (714.4). History of
Benalia ruling [2018-04-27]: it "sacrifices it as soon as its chapter
ability has left the stack". Urza's Saga ruling [2021-06-18]: it is
"sacrificed after its last chapter ability resolves".

**Variant SBAs** (apply only in those formats) (704.6): Two-Headed Giant
team at 0 life loses (704.6a); 2HG team with 15+ poison loses (704.6b);
**Commander** — 21+ combat damage from one commander loses (704.6c; Brawl
doesn't use it, 903.12h), and a commander newly in graveyard/exile may be
moved to the command zone (704.6d); Archenemy: a face-up non-ongoing scheme, with no scheme's
triggered ability on the stack or waiting, is turned face down and put on
the bottom of its owner's scheme deck (704.6e); Planechase face-up
phenomenon (no pending trigger) → planar controller planeswalks (704.6f).

**Immediate rule actions (not SBAs).** Five rules perform an action as soon
as their event or condition occurs and state that it isn't a state-based
action (closed list):

- leave-game cleanup (800.4a);
- exiling an object whose control effect ends after its default controller
  has left (800.4c);
- the planar controller turning up a new plane when a face-up plane leaves
  the game with its owner (901.10);
- the daybound mismatch transform (702.145c);
- the nightbound mismatch transform (702.145f).

None of them waits for the 704.3 check. Engine inference: they can happen
mid-resolution, which SBAs never see (704.4). Daybound and nightbound's
day/night initialization (702.145d, 702.145g) uses the same "any time"
wording. It isn't in 704.5 and the CR doesn't classify it; engine inference:
treat it the same way (`underdetermined.md` UD-18).
Day/night detail: `designations.md`.

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
| 116.2k | Pay a plot cost and exile a plot card from hand | Priority + empty stack, own main phase (702.170a; 116.2k's summary omits the main-phase limit) |
| 116.2m | Pay an unlock cost to unlock a locked half | Priority + empty stack, own main phase |

## 5. Keyword actions

Specialized verbs in rules text with defined meanings (701.1). The
machine-readable list is `data/rules/keywords.json` (`.keywordActions`);
`scripts/keyword <name>` prints any keyword action's rule.
Full enumeration (701.2–701.71), grouped thematically:

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
  Monstrosity (701.37), Adapt (701.46), Amass (701.47), Empower Jace
  (701.71), Endure (701.63), Incubate (701.53).
- **Combat / aggression** — Fight (701.14), Goad (701.15), Detain (701.35),
  Blight (701.68), Suspect (701.60).
- **Card advantage / value** — Investigate (701.16), Populate (701.36),
  Explore (701.44), Learn (701.48), Connive (701.50), Discover (701.57),
  Collect Evidence (701.59), Forage (701.61), Manifest Dread (701.62),
  Harness (701.64), Heal (701.69), Recruit (701.70).
- **Choices / votes / dice** — Vote (701.38), Clash (701.30), Assemble
  (701.45), Face a Villainous Choice (701.55), The Ring Tempts You (701.54),
  Time Travel (701.56).
- **Bending (Avatar)** — Airbend (701.65), Earthbend (701.66), Waterbend
  (701.67).
- **Subgame structures** — Venture into the Dungeon (701.49), Open an
  Attraction (701.51), Roll to Visit Your Attractions (701.52), Planeswalk
  (701.31), Set in Motion (701.32), Abandon (701.33).

**Who performs a keyword action.** The CR words a keyword action in one of
three ways:

1. *A player is instructed.* This is the default: an instruction with no
   stated subject is followed by the controller of the resolving spell or
   ability (608.2c).
2. *A permanent is instructed.* Only fight, explore, connive, and endure
   take this wording (701.14a, 701.44a, 701.50a, 701.63a). Explore, connive,
   and endure hand every step to "that permanent's controller". If the
   permanent has left the battlefield, its last known information fixes
   which object acted and who controlled it (701.44c, 701.50b). Endure gets
   the same through 608.2h; an Anafenza, Unyielding Lineage ruling
   [2025-04-04] says that with no creature to take counters "you'll just
   create a Spirit token". Several permanents explore or connive one at a
   time, the first player in APNAP order picking which of theirs goes next
   (701.44d, 701.50c). Fight has no player step: each creature deals damage
   equal to its power to the other (701.14a). If either creature is gone, is
   no longer a creature, or is an illegal target, neither deals damage
   (701.14b).
3. *A definition over "this permanent".* Adapt (701.46a), monstrosity
   (701.37a), and harness (701.64a) make the permanent the patient, not a
   performer; the player following the instruction acts (608.2c). The CR
   says outright that a permanent's ability "instructs a player to
   'monstrosity X'" (701.37c).

**Search is not "choose from the matching cards."**
- Any zone can be searched; the searcher looks at every card in it, hidden
  zones included (701.23a).
- What must be found depends on the zone and the wording. Hidden zone with a
  stated quality ("a basic land card", "all cards named ..."): finding is
  optional even when matches are present (701.23b). Hidden zone with an
  undefined quality: the player may still search but can't find any cards
  (701.23c). Hidden zone with a bare quantity ("a card", "three cards"): the
  searcher must find that many, or as many as the zone holds (701.23d).
  Public zones (400.2: graveyard, battlefield, stack, exile, ante, command)
  get none of these exemptions: Splinter's searcher "must find the Howling
  Mine in the graveyard" (701.23b example; Eradicate ruling [2005-02-01]:
  "The copies must be found if they are in publicly viewable zones. Finding
  copies while searching private zones is optional.").
- Found cards are revealed only if the same effect says to reveal them
  (701.23e).
- A replacement that narrows a search to part of the zone (Aven Mindcensor)
  leaves the effect's other search instructions in force and still fires
  library-searched triggers; a following shuffle shuffles the whole library
  (701.23f and example).
- An effect that offers an optional search may be taken up even when its
  follow-up actions are illegal or impossible (701.23g).
- Repeated search instructions on one library before its shuffle are a
  single search; the library is searched only once (701.23h). Simultaneous
  searchers look at the same time, then decide what to find in APNAP order
  (701.23i). Searching outside the game finds a card the searcher owns
  (701.23j).

**Shuffle is its own instruction.** A tutor's "then shuffle" is printed
text, not part of searching (701.23 defines no shuffle). When an effect
searches, shuffles, then places what it found, the found cards are left out
of the shuffle and shuffle triggers still fire (701.24b). "Shuffle [objects]
into a library" shuffles even if the objects aren't where expected, were
moved elsewhere, or the set is empty (701.24c, 701.24d). Shuffle triggers
fire for a zero- or one-card library (701.24e) and once per simultaneous
shuffle (701.24f). A shuffle simultaneous with a positional placement yields
a randomized library with that object in its position (701.24g).

**Exchange is all-or-nothing**, the exception to do-as-much-as-possible
(609.3; `choices.md` section 5). If the entire exchange can't be completed,
no part of it occurs: exchanging control of two target creatures when one
was destroyed does nothing to the other (701.12a and example). By kind:
- *Control*: each controller simultaneously gains control of the other's
  permanent. If both permanents have the same controller, the exchange does
  nothing (701.12b).
- *Life totals*: each player gains or loses the difference, so life-gain and
  life-loss replacements and triggers apply. A player who can't gain (lose)
  life can't be given a higher (lower) total, and then "the exchange won't
  happen" (701.12c, 119.7, 119.8).
- *Cards across zones*: allowed only if all the cards are owned by one
  player, and allowed even if one zone is empty (701.12d). If either card
  was attached to an object, the card exchanged in takes over that
  attachment (701.12e). "Exchange two zones" proceeds with one zone empty
  (701.12f).
- *Numerical values*: each becomes the other's previous value. A life total
  moves by gain or loss as above, and a power or toughness gets a layer-7b
  setting effect (701.12g, 613.4b). Switching one creature's power and
  toughness is not an exchange (701.12g).
- *Text boxes* (Exchange of Words): a text-changing effect (701.12h).

Two-Headed Giant life-exchange overrides are in `variants.md`.

Drawing (121.1) and dealing damage (120.1) have their own rules sections and
are not in the 701 list. Whether a multi-object action is one event or
several is `events.md` §4; whether an action that did nothing still produces
an event is `events.md` §2, *Keyword-action events*.

## 6. The main loop

The engine cycle once a step/phase has begun (turn-based actions already
handled; 703.3). `turn.md` section 7 has the per-step loop; this section is
the generic cycle:

0. **Steps without the usual priority.** Untap step: no player gets
   priority, and SBAs aren't checked. Triggers wait until the next time a
   player would receive priority, usually upkeep (502.4, 117.3a). Cleanup:
   after 514.1–514.2, the game makes one SBA/trigger check. If no SBA is
   performed and no trigger is waiting, no one gets priority and the step
   ends (704.3, 514.3). Otherwise SBAs are performed, triggers go on the
   stack, and AP gets priority. Once the stack is empty and all players pass
   in succession, another cleanup step begins (514.3a).
1. **Priority handshake.** Before any player gets priority, perform all
   applicable SBAs, repeating while a check performs any (a condition that
   holds but whose action is prohibited or ignored performs nothing; section
   3), then put waiting triggers on the stack in two APNAP passes (first
   triggers whose condition isn't another ability triggering, then the rest,
   each player ordering their own within each pass, 603.3b), then re-check,
   until a check performs no SBA and no trigger is waiting (704.3, 117.5).
   The active player gets priority at step/phase start (except untap, and
   usually cleanup: step 0) and after a spell or ability other than a mana
   ability resolves (117.3b); a player keeps priority after acting (117.3a,
   117.3b, 117.3c).
2. **Act or pass.** The player with priority may **cast a spell** (601,
   instants any time; sorcery-speed needs empty stack + own main phase,
   117.1a), **activate an ability** (602, any time, 117.1b), or **take a
   special action** (116, 117.1c). Mana abilities don't use the stack: they
   may be activated with priority or while paying (117.1d), activated ones
   resolve immediately (605.3b), and triggered mana abilities resolve right
   after the mana ability that triggered them (605.4a). Triggered abilities
   just wait — they hit the stack at the next priority check (603.3,
   117.2a). Acting → return to step 1.
3. **Passing.** A player choosing no action passes; priority moves to the
   next player in turn order (117.3d). If **all players pass in succession**
   (117.4): if the stack has an object, the top object resolves (608.1) —
   then back to step 1; if the stack is empty, the step/phase ends (in
   cleanup, a new cleanup step begins instead, 514.3a).
4. **Resolution.** A resolving spell/ability follows the effect pipeline
   (608.1) and may instruct players to make choices, but **no player has
   priority during resolution** (117.2e). Outside resolution, players also
   make choices: during casting (601.2b-d modes, cost intentions, X,
   targets, division; 601.2f-h cost-reduction order, mana abilities,
   payment); during activation (602.2b imports 601.2b-i); during trigger
   placement (603.3b ordering, 603.3c-d modes/targets); in turn-based
   actions (section 2: 703.4c, 703.4h, 703.4i-k, 703.4n); in special actions
   (section 4); and in SBAs (704.5j, 704.5u, 704.5x-y, 704.6d). Whenever
   competing replacement/prevention effects would modify an event, in or out
   of resolution, the affected player or the affected object's controller
   chooses which applies (616.1). See `choices.md` for the decider and
   lock-stage model.

## 7. Illegal actions

If a player takes an illegal action or can't legally complete one, the
entire action is reversed and payments canceled — no triggers fire, no
effects apply, and a spell returns whence it came (733.1). Each player may
also reverse legal mana abilities they activated during the illegal play,
unless that mana (or mana from triggered mana abilities they caused) was
spent on an unreversed mana ability. Actions that moved cards to a library,
moved cards from a library to any zone other than the stack (casting from a
library can be reversed), shuffled a library, or revealed cards from a
library are never reversed (733.1). The player who had priority keeps it and
may redo the action legally, take another action, or pass (733.2).
