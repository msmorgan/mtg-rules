# Outcomes — Ending the Game

*Synthesized from the Comprehensive Rules effective 2026-08-07
(`data/rules/cr.json`). Orientation only — verify load-bearing specifics
with `scripts/rule` before citing. Run `scripts/cite check` after CR
refreshes.*

A game ends immediately when a player wins, when the game is a draw, or when
the game is restarted (104.1). Everything below is the machinery behind that
sentence: the routes into each terminal, the effects that modify them, and
what an engine's outcome checker must evaluate. Outcome modification is the
family `deontics.md` §6 explicitly evicted — "can't" over an outcome is not
action legality.

## 1. Routes to loss, win, draw, restart

**Loss routes** (104.3):

| Route | Rule(s) | Mechanism |
|---|---|---|
| Life 0 or less | 104.3b, 704.5a | SBA |
| Drew from empty library | 104.3c, 704.5b | SBA (draws what's left first) |
| Ten or more poison counters | 104.3d, 704.5c | SBA |
| 21+ combat damage from one commander | 104.3j, 903.10a, 704.6c | variant SBA |
| Effect says "loses the game" | 104.3e | immediate on resolution |
| Concession | 104.3a | immediate, any time |
| Judge penalty | 104.3k | tournament only |

- The SBA routes fire "the next time a player would receive priority"
  (104.3b–d); the whole check-and-apply loop is 704.3 (`turn.md` §2).
- Two-Headed Giant swaps in team checks: team life (704.6a), fifteen or more
  team poison counters (704.6b — 704.5c is ignored, per its own text).
- Commander damage is tracked per commander over the whole game (903.10a);
  all normal ending rules still apply on top (903.10).
- **Concession is unstoppable.** It is the *single* exception to
  card-text-beats-rules (101.1), and a player being controlled can still
  concede — their controller can't prevent it (723.6). No "can't lose"
  effect stops it.

**Win routes** (104.2): all opponents have left the game — immediate, and it
"overrides all effects that would preclude that player from winning the
game" (104.2a); or an effect says you win (104.2b).

**Draw routes** (104.4): all remaining players lose simultaneously (104.4a);
a "loop" of mandatory actions with no way out (104.4b — a loop containing an
optional action is not a draw); an effect says so (104.4c); intentional draw
in a tournament (104.4i).

**Restart** (Karn Liberated): 104.6 points at rule 727. The restarted game
ends with *no* winner, loser, or draw (727.1); the controller of the
restarting effect starts the new game (727.1a). Carryover: every Magic card
involved in the old game comes along — including cards brought in from
outside the game — with ownership unchanged (727.2). The restarting effect
finishes resolving just before the new first turn's untap step, and any
leftover instructions execute then (727.4). Effects may exempt cards from
the restart procedure (727.5); an exempted commander starts outside the
command zone but remains the deck's commander (727.5a).

**Subgames** (Shahrazad): rule 729. A subgame is a completely separate game
created by an effect (729.1a) with an entirely new set of zones, built from
the players' main-game libraries (729.2). Main-game objects are "outside the
game" relative to the subgame and vice versa (729.4), and effects in one
have no meaning in the other except as the creating effect defines (729.1b).
At the end, each player shuffles the traditional cards they own — *other
than those in the subgame command zone* — into their main-game library
(729.5); supplementary decks, vanguards, and commanders instead return to
the main-game command zone (729.5a–c). (Commanders move into the subgame
command zone as the subgame starts, 729.2c.) Subgames nest (729.6);
restarting a subgame leaves the main game untouched (727.6).

**Elimination.** A player who loses, or for whom the game is a draw, leaves
the game (104.5), and rule 800.4 handles the fallout: all objects they own
leave the game, control-granting effects end, their non-card stack objects
cease to exist, and anything they still control is exiled — immediately, not
as an SBA (800.4a). Scope caveat: 800.4 is multiplayer-section machinery
("Unlike two-player games, multiplayer games can continue…", 800.4); in a
two-player game there is no leave-game cleanup, because the first loss ends
the whole game (104.1). Commander elimination is this same rule — a
Commander game may be two-player or multiplayer (903.2), and only in the
multiplayer case does the eliminated player's commander and every card they
own leave with them per 800.4a; in a two-player Commander game the caveat
above applies, and the game simply ends.

## 2. Outcome modification

This is the family `deontics.md` §6 evicted from the Cant compiler: a
"can't" ranging over an outcome modifies §104/§704 machinery, not choice
legality.

- **"You can't lose the game / opponents can't win the game"** (Platinum
  Angel, verified oracle text): no CR rule defines the *base* semantics of
  can't-lose/can't-win. Its rules home is 101.1: the card text directly
  contradicts 104.3b–e and the loss SBAs, so the card takes precedence and
  the loss simply doesn't happen — the "can't" gates each application,
  consuming nothing (101.2, 704.3). What happens when the effect ends is
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
  win" (104.2a).
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
  flags: can_lose? can_win?       # 101.1-compiled card effects, with durations
  gates: can_lose=false suppresses 704.5a/704.5b/704.5c/704.6c for player;
         team SBAs 704.6a/704.6b suppress at *team* level — one player's
         can_lose=false lifts to the whole team (810.8a)
         can_win=false suppresses 104.2b wins; 104.2a bypasses it
  combine: 104.3f  win∧lose → lose
           704.7   one replacement consumes the whole same-result SBA batch
  immediate (not SBA): 104.3a concede (ungated, always), 104.3e / 104.2b
           effect outcomes (gated by flags), 104.2a opponents-all-left
```

Then split **per-player elimination** from **whole-game terminal**: two
players → first loss is terminal (104.1); multiplayer → run the leave-game
cleanup of 800.4a (objects out — ante-zone objects excepted, 800.4n —
control effects end, residue exiled) and
continue, aggregating team outcomes where the variant says so (104.3g,
104.4d). Draw detection needs the mandatory-loop monitor (104.4b) — only
loops with no optional action qualify.

**Restart is not a reset** — it's a terminal event that constructs a fresh
game state with explicit carryover: the card pool including outside-game
additions, with ownership preserved (727.2); the starting player = the
restarter's controller (727.1a); minus the exemption set (727.5, 727.5a);
plus the restarting effect's trailing instructions executed pre-untap
(727.4). **Subgame is a context push**: a whole second game state on a stack
of games (729.1a, 729.6), sharing nothing but the card pool, whose result
returns to the main game as mere information (729.1b).
