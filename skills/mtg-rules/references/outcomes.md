# Outcomes — Ending the Game

*Synthesized from the Comprehensive Rules effective 2026-09-25
(`data/rules/cr.json`).*

A game ends immediately when a player wins, when the game is a draw, or when
the game is restarted (104.1). Everything below is the machinery behind that
sentence: the routes into each terminal, the effects that modify them, and
what an engine's outcome checker must evaluate. Outcome modification is the
family `deontics.md` §6 explicitly evicted — "can't" over an outcome is not
action legality. Team (Two-Headed Giant) outcomes (810.8a–b) are owned here;
range-of-influence and Emperor outcome overrides live in `variants.md` §2
(outcomes.md rows).

## 1. Routes to loss, win, draw, restart

**Loss routes** (104.3):

| Route | Rule(s) | Mechanism |
|---|---|---|
| Life 0 or less | 104.3b, 704.5a | SBA |
| Drew from empty library | 104.3c, 704.5b | SBA (draws what's left first) |
| Ten or more poison counters | 104.3d, 704.5c | SBA |
| 21+ combat damage from one commander | 104.3j, 903.10a, 704.6c | variant SBA (Brawl doesn't use it, 903.12h) |
| Effect says "loses the game" | 104.3e | immediate on resolution |
| Concession | 104.3a | immediate, any time |
| Team concession (Two-Headed Giant) | 810.8b | one player's concession removes the whole team from the game immediately; that team loses |
| Judge penalty | 104.3k | tournament only |
| Would both win and lose at once | 104.3f | loses (arbitration, §2) |
| Variant routes (full list) | 104.3g, 104.3h, 104.3i | team: all players on the team lost (104.3g); limited range of influence: a win effect instead makes in-range opponents lose, and the game may continue (104.3h, 801.14); Emperor: the team loses if its emperor does (104.3i, 809.5b) |

- The SBA routes fire "the next time a player would receive priority"
  (104.3b–d); the whole check-and-apply loop is 704.3 (`turn.md` §2).
- Two-Headed Giant swaps in team checks: team life (704.6a), fifteen or more
  team poison counters (704.6b — 704.5c is ignored, per its own text).
  Outcomes are team-only: either player losing makes the team lose, and
  either player winning makes the team win (810.8a); a team concession is
  the 810.8b row in the table above.
- Commander damage is tracked per commander over the whole game (903.10a);
  all normal ending rules still apply on top (903.10).
- **Concession is unstoppable.** It is the *single* exception to
  card-text-beats-rules (101.1), and a player being controlled can still
  concede — their controller can't prevent it (723.6). No "can't lose"
  effect stops it. Where a concession lands relative to an atomic event, and
  who follows a resolving object's instructions when its controller concedes,
  are open: `underdetermined.md` UD-7.

**Win routes** (104.2): all opponents have left the game — immediate, and it
"overrides all effects that would preclude that player from winning the
game" (104.2a); or an effect says you win (104.2b). Variant routes (full
list): in a game between teams, a team with at least one player still in the
game wins when all other teams have left, and every member wins, even one who
had already lost (104.2c); in an Emperor game, a team wins if its emperor
wins (104.2d, 809.5a); in Two-Headed Giant, either member winning wins for
the team (810.8a); with limited range of influence, a win effect becomes
in-range opponents losing (104.3h, 801.14).

**Draw routes** (104.4): all remaining players lose simultaneously (104.4a);
in a game not using limited range of influence, a "loop" of mandatory
actions with no way out (104.4b — a loop containing an optional action is
not a draw; qualified by 732.4–732.6, §3); an effect says so (104.4c);
intentional draw in a tournament (104.4i). Variant routes (full list): all
remaining teams lose simultaneously (104.4d); with limited range of
influence, an effect draw (104.4e, 801.15) and a mandatory loop (104.4f,
801.16) are a draw only for the controller, or each player who controls an
object involved in the loop, plus each player within any such player's
range, and only those players leave; a team is drawn if the game is a draw
for all its remaining players (104.4g); an Emperor team is drawn if the game
is a draw for its emperor (104.4h, 809.5c).

**Restart** (Karn Liberated): 104.6 points at rule 727. The restarted game
ends with *no* winner, loser, or draw (727.1); the controller of the
restarting effect starts the new game (727.1a). Participants are the
players still in the game (104.6, 727.1; Karn ruling); with limited range of
influence, all players in the game (727.7). Carryover: every Magic card
involved in the old game comes along — including cards brought in from
outside the game — with ownership unchanged (727.2); no counters, emblems,
or prior-game actions carry over (Karn rulings). A player with fewer than
seven library cards loses at the first upkeep's SBA check, regardless of
mulligans (727.3). The restarting effect finishes resolving just before the
new first turn's untap step, and any leftover instructions execute then
(727.4); no player has priority at that point, so triggers wait for the next
priority, usually the first upkeep (727.4). Effects may exempt cards from
the restart procedure (727.5); an exempted commander starts outside the
command zone but remains the deck's commander (727.5a).

**Subgames** (Shahrazad): rule 729. A subgame is a completely separate game
created by an effect (729.1a) with an entirely new set of zones, built from
the players' main-game libraries (729.2). The first player is random (729.2,
unlike restart's 727.1a), and a player with fewer than seven library cards
loses the subgame at its first upkeep's SBA check (729.3). All objects in
the main game and all cards outside the main game are "outside the game"
relative to the subgame (729.4); conversely, subgame objects are in none of
the main game's zones and so are outside it (400.11, 729.2). Effects in one
have no meaning in the other except as the creating effect defines (729.1b).
Main-game abilities that trigger on cards leaving main-game zones wait to go
on the stack until the main game resumes (729.4a). A player's main-game
counters are not part of the subgame but are kept for the resumption, and
counters gained in the subgame cease to exist when it ends (729.4b). At the
end, each player shuffles the traditional cards they own — *other than
those in the subgame command zone* — into their main-game library (729.5);
supplementary decks, vanguards, and commanders instead return to the
main-game command zone (729.5a–c). (Commanders move into the subgame
command zone as the subgame starts, 729.2c.) The main game then resumes:
first the creating spell or ability finishes resolving, then the queued
main-game triggers go on the stack (729.5). Subgames nest (729.6);
restarting a subgame leaves the main game untouched (727.6).

**Elimination.** A player who loses, or for whom the game is a draw, leaves
the game (104.5), and rule 800.4 handles the fallout: all objects they own
leave the game, control-granting effects end, their non-card stack objects
cease to exist, and anything they still control is exiled — immediately, not
as an SBA (800.4a). Scope caveat: 800.4 is multiplayer-section machinery
("Unlike two-player games, multiplayer games can continue…", 800.4); in a
two-player game there is no leave-game cleanup (**engine inference** from
800.4's multiplayer scope), because the first loss ends the whole game: the
loser leaves (104.5), the survivor wins immediately (104.2a) — or both losing
at once is a draw (104.4a) — and 104.1 ends the game. Commander elimination
is this same rule — a Commander game may be two-player or multiplayer
(903.2), and only in the multiplayer case does the eliminated player's
commander and every card they own leave with them per 800.4a; in a
two-player Commander game the caveat above applies, and the game simply
ends.

## 2. Outcome modification

This is the family `deontics.md` §6 evicted from the Cant compiler: a
"can't" ranging over an outcome modifies §104/§704 machinery, not choice
legality.

- **"You can't lose the game / opponents can't win the game"** (Platinum
  Angel, verified oracle text): no CR rule defines the *base* semantics of
  can't-lose/can't-win. Its rules home is 101.1: the card text directly
  contradicts 104.3b–e and the loss SBAs, so the card takes precedence and
  the loss simply doesn't happen — the "can't" gates each application,
  consuming nothing (101.2, 704.3; this holds for SBAs only, see the
  state-trigger bullet below). What happens when the effect ends is
  per-SBA: 704.5a and 704.5c are standing state predicates ("has 0 or less
  life," "has ten or more poison counters"), so a still-true condition
  fires at the first check after the effect ends (Abyssal Persecutor
  leaves with an opponent at −5: that player loses as an SBA, no window to
  respond); 704.5b is a *windowed event* predicate ("attempted to draw …
  since the last time state-based actions were checked"), so the window
  lapses at each check and there is no retroactive empty-draw loss once
  can't-lose ends. The CR's one dedicated text is the Two-Headed
  Giant team lift: 810.8a raises a player's can't-win/can't-lose to their
  whole team (its example names Platinum Angel). Codified edges: concession
  pierces it (101.1, 104.3a); the last-player-standing win pierces "can't
  win" (104.2a). A judge penalty (104.3k; tournament policy via 100.6/MTR,
  not a 101.1 card override) and draw outcomes not built from losses are not
  gated either: effect draws (104.4c; Platinum Angel [2004-12-01], Abyssal
  Persecutor [2017-11-17]), mandatory-loop draws (104.4b; Transcendence
  ruling [2004-10-04]), and tournament intentional draws (104.4i). A 104.4a
  draw is gated indirectly, because it needs every remaining player to lose.
- **Partial exemptions** use the same 101.1 mechanism: "The card overrides
  only the rule that applies to that specific situation" (101.1). Phyrexian
  Unlife and Transcendence ("You don't lose the game for having 0 or less
  life") exempt only the life route; the player can still lose to ten
  poison counters or an empty-library draw (Phyrexian Unlife ruling
  [2011-06-01]), and under Two-Headed Giant the exemption lifts to the team
  (810.8a Transcendence example). Concession (101.1, 104.3a) and judge
  penalties (104.3k) stay ungated whatever the card says.
- **Contrast: state triggers.** A "you lose the game" state trigger whose
  loss is gated re-triggers after each resolution while its condition still
  holds (603.8), so can't-lose plus a still-true trigger condition forms a
  loop. Players may break it, for example by removing either card, but none
  can be forced to with an action outside the loop (732.5). If nobody does,
  the game is a draw (104.4b, 732.4; Transcendence ruling [2004-10-04]).
- **Win + lose simultaneously → lose** (104.3f). The arbitration is fixed:
  loss wins the race.
- **Loss replacement** (Lich's Mirror — the rule's own example): if multiple
  SBAs would have the same result at the same time, a single replacement
  effect replaces *all* of them (704.7). One Mirror shuffle answers a
  simultaneous 704.5a + 704.5b loss.
- **Turn-scoped can't-lose** (Angel's Grace, verified oracle text): "You
  can't lose the game this turn…" is the same 101.1 mechanism with a
  duration. Its famous life-stays-at-1 clause is the card's *own* damage
  replacement rider, not outcome machinery — don't look for a rule behind
  it.
- Adjacent but different: "can't lose life" (119.8) gates life *changes*,
  not outcomes — a player at 0 with lockable life still loses to 704.5a.

## 3. Engine note

Outcome checks ride the SBA loop: on would-get-priority, check all
conditions, perform all applicable SBAs simultaneously as one event, repeat
until stable (704.3). The outcome layer adds an **override lattice evaluated
before applying**:

```
OutcomeCheck(player):
  flags: can_win?                 # 101.1-compiled card effects, with durations
  gates: can_lose[route] for route in {704.5a life, 704.5b empty-library
         draw, 704.5c poison, 704.6a team life, 704.6b team poison, 704.6c
         commander damage, 104.3e effect loss}. "Can't lose the game" sets
         all of them. "Don't lose the game for having 0 or less life" sets
         only 704.5a and, through the 810.8a team lift, 704.6a (Phyrexian
         Unlife ruling [2011-06-01]; 810.8a Transcendence example).
         can_win=false suppresses 104.2b wins; 104.2a bypasses it
  combine: 104.3f  win∧lose → lose
           704.7   one replacement consumes the whole same-result SBA batch
  immediate (not SBA): 104.3a concede (ungated, always), 104.3k penalty
           (ungated), 104.3e / 104.2b effect outcomes (gated by
           can_lose[104.3e] / can_win), 104.4c effect draw (ungated),
           104.2a opponents-all-left
```

Then split **per-player elimination** from **whole-game terminal**: two
players → the loser leaves (104.5), the survivor wins immediately (104.2a),
or both losing at once is a draw (104.4a), and 104.1 ends the game;
multiplayer → run the leave-game cleanup of 800.4a (objects out — ante-zone
objects excepted, 800.4n — control effects end, residue exiled) and
continue, aggregating team outcomes per the variant's aggregation rule:
all-members loss (104.3g) and all-remaining-members draw (104.4g);
either-member (810.8a, Two-Headed Giant); emperor-only (104.2d, 104.3i,
104.4h, 809.5a–c). Team-level terminals: a team with any member still in the
game wins when all other teams have left (104.2c), and every member of the
winning team wins, even one who had already lost. The whole game is a draw
when all remaining teams lose simultaneously (104.4d).

Draw detection needs the mandatory-loop monitor (104.4b; limited range:
104.4f/801.16; equality test: UD-11). An action available outside the loop
does not make the loop optional: no player can be forced to take a
loop-ending action other than one called for by an object involved in the
loop (732.5). If nobody voluntarily breaks it, it is a draw (732.4;
Transcendence ruling [2004-10-04]). An unexercised "[A] unless [B]" leaves
the loop mandatory (732.6). A fragmented loop obliges the active (or first
involved) player to choose differently (732.3), so it is not a draw.

**Restart is not a reset** — it's a terminal event that constructs a fresh
game state with explicit carryover: the card pool including outside-game
additions, with ownership preserved (727.2); the starting player = the
restarter's controller (727.1a); minus the exemption set (727.5, 727.5a);
plus the restarting effect's trailing instructions executed pre-untap
(727.4). **Subgame is a context push**: a whole second game state on a stack
of games (729.1a, 729.6), sharing the card pool and the players (not life
totals or counters, 729.4b); the result reaches the main game only as the
creating effect defines (729.1b), and the main game resumes with the
creator's completion and the queued 729.4a triggers (729.5).
