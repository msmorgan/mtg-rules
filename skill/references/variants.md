# Variants — Where 8xx/9xx Override the Base Docs (Thin Index)

*Synthesized from the Comprehensive Rules effective 2026-04-17
(`data/rules/cr.json`). Orientation only — verify load-bearing specifics
with `scripts/rule` before citing. Run `scripts/check-citations` after CR
refreshes.*

The sibling reference docs synthesize the **core game + Commander**; the
multiplayer options (CR 801–805) and variants (806–811, 901–905) silently
override many of their claims. This doc is a pure pointer index — no variant
synthesis — of which 8xx/9xx rules override which base-doc claim, so a base
claim is never quoted into a variant answer unmodified (the leak pattern:
hand privacy vs 810.5, per-player can't-lose vs 810.8a). **Policy: variant
answers come from `scripts/rule 8xx`/`9xx` lookups, never from a base doc's
claim alone** — the base claim may be exactly what the variant rewrites.

## 1. Section roster (CR 800–811, 900–905)

| Rules | Variant / option | In this index |
|---|---|---|
| 800 | Multiplayer general — leaving the game (800.4), mulligan (800.6), first draw (800.7) | rows below |
| 801 | Limited range of influence option | rows below |
| 802 | Attack multiple players option | rows below |
| 803 | Attack left / attack right options | rows below |
| 804 | Deploy creatures option | no rows — grants each creature one teammate-control ability (804.2); touches no mapped doc |
| 805 | Shared team turns option | rows below |
| 806 | Free-for-All | no rows — only picks default options (806.2a–c) |
| 807 | Grand Melee | rows below |
| 808 | Team vs. Team | rows below |
| 809 | Emperor | rows below |
| 810 | Two-Headed Giant | rows below |
| 811 | Alternating Teams | rows below |
| 901 | Planechase | rows below |
| 902 | Vanguard | rows below |
| 903 | Commander | in scope already — folded throughout the docs |
| 904 | Archenemy | rows below |
| 905 | Conspiracy Draft | rows below |

## 2. Overrides by base doc

### state.md

| Base claim area | Overriding rule(s) | Delta |
|---|---|---|
| One active player, rest nonactive (§1) | 805.4a, 805.9 | shared team turns: active *team*; each member is an active player — an "active player" ability picks one |
| One active player (§1) | 807.4, 807.4b | Grand Melee: concurrent turns, one active player per turn marker |
| Per-player life total (§2) | 810.4, 810.9, 810.9a | 2HG: one shared team life total; reads of a player's life use the team's (set/exchange special cases 810.9c–810.9h); Archenemy Commander option similar (904.13b) |
| Poison: player loses at ten (§2) | 810.10, 810.10a, 704.6b | 2HG: poison shared by the team, loss at fifteen; Archenemy Commander keeps poison individual (904.13c) |
| Maximum hand size seven (§2) | 902.5, 902.5b | Vanguard: hand modifier shifts starting and maximum hand size |
| One shared LIFO stack (§8) | 807.5, 807.5a, 807.5b | Grand Melee: one stack per turn marker; priority and spell placement scoped per stack |

### turn.md

| Base claim area | Overriding rule(s) | Delta |
|---|---|---|
| First-turn draw step (§1; two-player skip 103.8a) | 800.7, 103.8c | multiplayer (non-2HG): the starting player does *not* skip their first draw step |
| First-turn draw step (§1) | 810.6, 103.8b | 2HG: the starting *team* skips its first draw step |
| Players take turns; per-player priority (§2) | 805.4, 805.5, 805.5b | shared team turns: teams take turns and hold/pass priority; each member draws (805.4b) and may play a land (805.4c) per team turn |
| One turn at a time (§1) | 807.4, 807.4b | Grand Melee: multiple simultaneous turns via numbered turn markers |
| Defending player = the nonactive player (§3, 506.2) | 802.2, 802.4, 802.5 | attack multiple players: every opponent is a defending player; blocks and damage assignment proceed in APNAP order |
| AP declares attackers, DP blockers (§3) | 805.10a, 805.10b, 805.10d, 805.10f | team combat: one combined team attack and one combined team block, each legal as a whole |
| Extra turns/phases/steps queue per player (§5) | 805.8 | shared turns: a player's extra or skipped turn/phase/step belongs to their team; one effect hitting both teammates adds/skips it once |
| Turn machinery assumes an active player | 800.4j, 800.4k | if the AP leaves, the turn completes with no active player; a departed player's queued turn never begins |

### deontics.md

| Base claim area | Overriding rule(s) | Delta |
|---|---|---|
| Attack permission/restriction check (§2, §4) | 801.3 | range of influence: attack only in-range opponents (their planeswalkers/battles); no one in range → can't attack |
| Attack restriction check (§4) | 803.1a, 803.1b | attack left/right: only the opponent seated immediately in that direction |
| Attack restriction check (§4) | 809.3c, 811.4 | Emperor / Alternating Teams: attack only opponents seated immediately next to you |
| Targeting legality (§8 `Cant(Target…)`) | 801.4 | out-of-range objects and players can't be targeted |
| Activation permission (§2, 117.1b row) | 801.6 | can't activate abilities of out-of-range objects |
| Solver runs over one declaration set (§4) | 802.3a | per-player restrictions/requirements bind only creatures attacking that player; the whole attacking set must still be legal |
| Block permission floor (§2) | 802.4a, 802.4b | a defender blocks only creatures attacking them; other players' combats are ignored for block legality |

### information.md

| Base claim area | Overriding rule(s) | Delta |
|---|---|---|
| Hand: owner only (§1 — 810.5 already folded in) | 808.5, 809.7, 811.5 | Team vs. Team / Emperor: teammates may review each other's hands; Alternating Teams: only adjacent teammates |
| Effects read the whole game state | 801.11 | range of influence: a spell/ability requiring game information sees only within its controller's range |
| Visibility model is in-game (§1–§4) | 905.1c, 905.2b, 905.2c | Conspiracy draft: drafted cards are hidden, except noted information (public to all) and face-up drafted cards |

### outcomes.md

| Base claim area | Overriding rule(s) | Delta |
|---|---|---|
| "Effect says you win" route (104.2b) | 801.14, 104.3h | range of influence: the win-effect instead makes in-range opponents lose; the game may continue |
| Draw ends the game for everyone (104.4) | 801.15, 801.16, 104.4e | effect-draws and mandatory-loop draws are scoped to the controller/loop players + their ranges; only those players leave |
| Concession is per player (§1) | 810.8b | 2HG: one player's concession removes the whole team from the game; that team loses |
| Per-player loss/eliminate (§1) | 809.5a, 809.5b, 809.5c | Emperor: a team wins/loses/draws exactly as its emperor does |

### events.md

| Base claim area | Overriding rule(s) | Delta |
|---|---|---|
| Trigger = predicate over (event, state) (§6) | 801.7, 801.7a | range of influence: an ability triggers only if the whole event happens within its controller's range |
| Trigger batching APNAP per controller (§4) | 805.7 | shared turns: active team's members order all their triggers in any order, then each nonactive team in turn order |
| "At the beginning of" phase/step triggers (§2) | 805.4d | shared turns: "each player's/opponent's" step triggers can fire once per team member |
| LKI is for departed objects (§5) | 800.4i | departed *players*: effects use last known information about the player; their past actions remain findable |
| Triggers go on the stack at next priority (§6) | 800.4d | a trigger that would be controlled by a departed player is never put on the stack |

### choices.md

| Base claim area | Overriding rule(s) | Delta |
|---|---|---|
| APNAP order (§1, 101.4) | 805.6, 805.6a | shared turns: team-by-team ordering; within a team, members choose in any order they like |
| APNAP order (§1) | 905.2a | Conspiracy draft: no priority, no APNAP — contested simultaneous draft actions happen in random order |
| A nominal decider always exists (§1) | 800.4g, 800.4h | departed decider: the object's controller picks a substitute (an opponent if it was an opponent's choice); rule-mandated choices pass to the next player in turn order |
| Each decision has one decider (§1) | 805.2, 801.5a, 801.5c | team disagreement: the primary player decides; range of influence: object/player picks must be in range (801.5a), and a choice no in-range player can make falls to the closest appropriate player to the left (801.5c) |
| Mulligans starting-player-first (§2, 103.5) | 805.3a | shared turns: starting team first, teammates may consult, all mulligans taken simultaneously |
| First-turn choice (§2, 103.1) | 805.3, 904.6 | team variants determine a starting *team*; Archenemy: the archenemy always takes the first turn |

### designations.md

| Base claim area | Overriding rule(s) | Delta |
|---|---|---|
| Planar controller (player-carried; 901.6, 901.12b already folded in) | 901.12c, 901.12d | 2HG Planechase: the face-up plane's "you" applies to both members of the planar controller's team; each active-team member may roll the planar die |

## 3. Deltas the base docs already fold in (don't re-add)

- `state.md` §2 variant starting life totals (119.1a–119.1e); §3/§8 Commander
  command zone and commander state (903.6, 903.8, 903.9, 903.10a).
- `outcomes.md` leave-game cleanup (800.4a, 800.4n), 2HG team SBAs (704.6a,
  704.6b), the 810.8a team can't-win/can't-lose lift, commander damage
  (903.10a), team aggregation pointers (104.3g, 104.4d).
- `information.md` §1 2HG teammate hand review (810.5).
- `choices.md` §2 multiplayer first-mulligan-free (103.5c, restated at 800.6).
- `turn.md` §1/§3 Archenemy scheme action (703.4e) and the multiplayer
  choose-defending-player action (703.4h, 507.1).
- `designations.md` planar controller (901.6, 901.12b) and the Commander card
  attribute (903.3).
