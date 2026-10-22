# Variants — Where 8xx/9xx Override the Base Docs (Thin Index)

*Synthesized from the Comprehensive Rules effective 2026-09-25
(`data/rules/cr.json`).*

The sibling reference docs synthesize the **core game + Commander**; the
multiplayer options (CR 801–805) and variants (806–811, 901–905) silently
override many of their claims. This doc is a pure pointer index — no variant
synthesis — of which 8xx/9xx rules override which base-doc claim, so a base
claim is never quoted into a variant answer unmodified (the leak pattern:
hand privacy vs 810.5, per-player can't-lose vs 810.8a). **Policy: variant
answers come from `scripts/rule 8xx`/`9xx` lookups, never from a base doc's
claim alone** — the base claim may be exactly what the variant rewrites. A base
doc with no section below has not been certified override-free, so an absent
row is not proof that nothing overrides.

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
| 903 | Commander | in scope — folded into the base docs except the rows below |
| 904 | Archenemy | rows below |
| 905 | Conspiracy Draft | rows below |

## 2. Overrides by base doc

### state.md

| Base claim area | Overriding rule(s) | Delta |
|---|---|---|
| One active player, rest nonactive (§1) | 805.4a, 805.9 | shared team turns: active *team*; each member is an active player — an "active player" ability picks one |
| One active player (§1) | 807.4, 807.4b | Grand Melee: concurrent turns, one active player per turn marker; APNAP across concurrent turns: see UD-39 |
| Per-player life total (§2) | 810.4, 810.9, 810.9a, 810.11 | 2HG: one shared team life total; damage/loss/gain happen per player, result applied to the team (810.9); reads of a player's life use the team's (810.9a); special cases 810.9b–810.9h (simultaneous pay cap, set, set-each, exchange, redistribute, can't-gain/can't-lose team locks); +15 team starting life per member beyond the second (810.11); Archenemy Commander option similar (904.13b) |
| Poison: player loses at ten (§2) | 810.10, 810.10a, 810.10b, 810.10c, 810.10d, 810.11, 704.6b | 2HG: poison shared by the team, loss at fifteen; +5 to the loss threshold per team member beyond the second (810.11); a player is "poisoned" if their team has one or more poison counters, and counter-kind reads use the player's kinds plus the team's (810.10d); "a player loses poison counters" removes them from the team (810.10b); "can't get poison counters" locks the whole team (810.10c); Archenemy Commander keeps poison individual (904.13c) |
| Owner = player who started with the card (§2, 108.3) | 901.15b | Planechase single-planar-deck option: the planar controller is considered the owner of every card in the planar deck |
| Maximum hand size seven (§2) | 902.5, 902.5b | Vanguard: hand modifier shifts starting and maximum hand size |
| One shared LIFO stack (§8) | 807.5, 807.5a, 807.5b | Grand Melee: one stack per turn marker; priority and spell placement scoped per stack |

### turn.md

| Base claim area | Overriding rule(s) | Delta |
|---|---|---|
| First-turn draw step (§1; two-player skip 103.8a) | 800.7, 103.8c | multiplayer (non-2HG): the starting player does *not* skip their first draw step |
| First-turn draw step (§1) | 810.6, 103.8b | 2HG: the starting *team* skips its first draw step |
| Players take turns; per-player priority (§2) | 805.4, 805.5, 805.5b | shared team turns: teams take turns and hold/pass priority; each member draws (805.4b) and may play a land (805.4c) per team turn |
| One turn at a time (§1) | 807.4, 807.4b | Grand Melee: multiple simultaneous turns via numbered turn markers |
| Defending player = the nonactive player (§3, 506.2) | 802.2, 802.2a, 802.4, 802.5 | attack multiple players: every opponent is a defending player; blocks and damage assignment proceed in APNAP order; "defending player" in any rule/effect = one specific defending player (802.2a): for an attacking creature's ability, or text naming both an attacking creature and a defending player, it is the player that creature is (or was) attacking, or the controller of the planeswalker / protector of the battle it is (or was) attacking, determined per creature; otherwise, if several qualify, the controller of the spell or ability chooses one |
| AP declares attackers, DP blockers (§3) | 805.10a, 805.10b, 805.10c, 805.10d, 805.10e, 805.10f | team combat: one combined team attack and one combined team block, each legal as a whole; "defending player" binds per 805.10e, "attacking player" per 805.10c (the controller of the attacker that blocking creature blocks) |
| Extra turns/phases/steps queue per player (§5) | 805.8 | shared turns: a player's extra or skipped turn/phase/step belongs to their team; one effect hitting both teammates adds/skips it once |
| Turn machinery assumes an active player | 800.4j, 800.4k | if the AP leaves, the turn completes with no active player; a departed player's queued turn never begins |
| Combat damage assignment (§3, 510.1) | 800.4e | combat damage that would be assigned to a departed player isn't assigned |

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
| Draw ends the game for everyone (104.4) | 801.15, 801.16, 104.4e, 104.4f | effect-draws and mandatory-loop draws are scoped to the controller/loop players + their ranges; only those players leave |
| Concession is per player (§1) | 810.8a, 810.8b | 2HG: team outcomes are owned by `outcomes.md` §1 — see its team-concession row and 2HG team note |
| Per-player loss/eliminate (§1) | 809.5a, 809.5b, 809.5c | Emperor: a team wins/loses/draws exactly as its emperor does |
| Restart (727) | 801.17 | range of influence: restart effects are exempt; every player in the game starts the new game |
| 21+ commander damage SBA (§1, 704.6c) | 903.12h | Brawl doesn't use it |

### events.md

| Base claim area | Overriding rule(s) | Delta |
|---|---|---|
| Trigger = predicate over (event, state) (§6) | 801.7, 801.7a | range of influence: an ability triggers only if the whole event happens within its controller's range |
| Trigger batching APNAP per controller (§4) | 805.7 | shared turns: active team's members order all their triggers in any order, then each nonactive team in turn order; APNAP across concurrent turns: see UD-39 |
| "At the beginning of" phase/step triggers (§2) | 805.4d | shared turns: "each player's/opponent's" step triggers trigger once per appropriate team member only if the trigger condition, effect, or intervening if refers to "that player"/"that opponent" (805.4d); otherwise once |
| LKI is for departed objects (§5) | 800.4i | departed *players*: effects use last known information about the player; their past actions remain findable |
| Triggers go on the stack at next priority (§4, §7, 603.3b) | 800.4d | a trigger that would be controlled by a departed player is never put on the stack |

### choices.md

| Base claim area | Overriding rule(s) | Delta |
|---|---|---|
| APNAP order (§1, 101.4) | 805.6, 805.6a | shared turns: team-by-team ordering; within a team, members choose in any order they like |
| APNAP order (§1) | 905.2a | Conspiracy draft: no priority, no APNAP — contested simultaneous draft actions happen in random order |
| APNAP order (§1, 101.4) | 807.4, 807.5 | Grand Melee: several active players at once; APNAP and "the active player" are unspecified — see UD-39 |
| A nominal decider always exists (§1) | 800.4f, 800.4g, 800.4h | departed decider: the object's controller picks a substitute (an opponent if it was an opponent's choice); rule-mandated choices pass to the next player in turn order; a cost a departed player would pay, or choose whether to pay, is not paid (800.4f) |
| Each decision has one decider (§1) | 805.2, 801.5a, 801.5b, 801.5c | team disagreement: the primary player decides; range of influence: object/player picks must be in range (801.5a) but mode/option choices are not range-limited (801.5b), and a choice no in-range player can make falls to the closest appropriate player to the left (801.5c) |
| Whole-player control (§1, 723.5) | 805.8 | shared turns: controlling a player controls that player's whole team |
| Role rebinding (§1, 310.9d) | 802.2a, 805.9, 805.10c, 805.10e | role nouns bind to one specific player, not to every holder of the role: "defending player" (802.2a, 805.10e), "attacking player" (805.10c), "active player" under shared team turns (805.9) |
| Mulligans starting-player-first (§2, 103.5) | 805.3a | shared turns: starting team first, teammates may consult, all mulligans taken simultaneously |
| First-turn choice (§2, 103.1) | 805.3, 808.4, 809.4, 904.6 | team variants determine a starting *team* (Team vs. Team picks a random team and its center-seat player goes first, 808.4; Emperor picks a random emperor, 809.4); Archenemy: the archenemy always takes the first turn |

### designations.md

| Base claim area | Overriding rule(s) | Delta |
|---|---|---|
| Planar controller (player-carried; 901.6, 901.12b, 901.14a–901.14b already folded in) | 901.12c, 901.12d | 2HG Planechase: the face-up plane's "you" applies to both members of the planar controller's team; each active-team member may roll the planar die |

### effects.md

| Base claim area | Overriding rule(s) | Delta |
|---|---|---|
| An effect applies to every object/player its text describes (§1–§3) | 801.10 | range of influence: the parts that would affect out-of-range objects or players do nothing; the rest applies; the same limit holds at resolution (`casting.md` §6); planes/phenomena exempt except in Grand Melee (801.18, 901.13) |
| Replacement/prevention modify the event (§6, §7) | 801.13, 801.13a, 801.13b | range of influence: out-of-range portions of a replaced event do nothing; prevention reaches only in-range sources and recipients, and when neither is specified, both must be in range; planes/phenomena exempt except in Grand Melee (801.18, 901.13) |
| Control-changing effects (§4, layer 2) | 800.4b | departed players: no object changes to a departed player's control, no token is created under it, and an object that would enter the battlefield or stack under it stays in its current zone |

### actions.md

| Base claim area | Overriding rule(s) | Delta |
|---|---|---|
| SBAs 704.5k / 704.5m / 704.5n (§3) | 801.8, 801.9, 801.12 | range of influence: an Aura/Equipment/Fortification attached to something outside its controller's range is illegally attached; the world rule applies to a permanent only if other world permanents are within its controller's range |
| 21+ commander damage SBA (§3, 704.6c) | 903.12h | Brawl doesn't use it |

### temporal.md

| Base claim area | Overriding rule(s) | Delta |
|---|---|---|
| "Until [player]'s next turn" ends when that turn begins (§1) | 800.4m | if that player has left the game, the effect ends when that turn would have begun; it neither expires immediately nor lasts indefinitely |

### queries.md

| Base claim area | Overriding rule(s) | Delta |
|---|---|---|
| "Your team" = you and every teammate (§3, 102.4) | 801.2d, 801.10, 801.11 | range of influence: an effect can't affect or see an out-of-range teammate or their objects — an Emperor general (default range 1, 809.3a) doesn't reach the other general across the emperor (809.1, 809.2); Alternating Teams seats teams equally spaced with no teammate adjacent (811.3), so with three or more teams teammates start beyond the recommended range 2 (811.2a; ranges recompute each turn, 801.2c) |

## 3. Deltas the base docs already fold in (don't re-add)

- `state.md` §2 variant starting life totals (119.1a–119.1e); §3/§8 Commander
  command zone and commander state (903.6, 903.8, 903.9, 903.10a).
- `outcomes.md` leave-game cleanup (800.4a, 800.4n), 2HG team SBAs (704.6a,
  704.6b), the 810.8a team outcomes (either-member loss/win and the
  can't-win/can't-lose lift) and 810.8b team concession (one 810.8b row,
  owned by `outcomes.md`), commander damage (903.10a), team aggregation and
  team-level terminals (104.2c, 104.3g, 104.4d, 104.4g), and the variant
  route lists (104.2c–d, 104.3g–i, 104.4d–h).
- `information.md` §1 2HG teammate hand review (810.5).
- `choices.md` §2 multiplayer first-mulligan-free (103.5c, restated at 800.6).
- `turn.md` §1/§3 Archenemy scheme action (703.4e) and the multiplayer
  choose-defending-player action (703.4h, 507.1).
- `designations.md` planar controller (901.6, 800.4p, 901.12b, 901.14a–901.14b)
  and the Commander card attribute (903.3).
- `queries.md` §3 "your team" and team-relative "opponent" (102.3, 102.4).
