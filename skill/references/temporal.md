# Temporal Scope — Durations, Windows, Locks

*Synthesized from the Comprehensive Rules effective 2026-04-17
(`data/rules/cr.json`). Orientation only — verify load-bearing specifics
with `scripts/rule` before citing. Run `scripts/cite check` after CR
refreshes.*

This doc is an **index-unification**: the pieces are owned elsewhere —
durations by `effects.md` §3, the announcement pipeline by `casting.md` §1,
per-decision lock stages by `choices.md` §2, turn structure by `turn.md`,
trigger windows by `events.md` §6. What no single doc shows is the *whole*
temporal model: every value in the game is either **continuously
re-evaluated**, **scoped to a window**, or **locked at a known point**. The
lock table in §3 is this doc's contribution; the rest is signposting.

## 1. Duration taxonomy

How long a continuous effect lasts (611.2 letters; details in `effects.md`
§3 — this is the temporal view):

- **Fixed** — "lasts as long as stated" (611.2a). End markers are
  turn-structure events: "until end of turn" / "this turn" effects end in
  cleanup, simultaneously with damage removal (514.2) — and a repeated
  cleanup (514.3a) re-runs that sweep, so effects created *during* cleanup
  still end this turn; "until end of
  combat" effects expire at the end of the combat *phase*, not at the
  beginning of the end of combat step (500.5a, 511.2); "until your next
  turn" and friends end when the named structure point arrives.
- **Until [event]** — terminated by an event pattern rather than a
  structure point: "until this creature leaves the battlefield", "until
  [player] discards a card". A special-action variant lets a player *end*
  the effect themselves any time they have priority, "for as long as the
  effect allows it" (116.2c).
- **Conditional ("for as long as …", 611.2b)** — a tracked predicate, with
  three edge rules: if the duration *never starts*, the effect does
  nothing; if it *ended before the effect would first apply* (and doesn't
  begin again during that resolution), the effect does nothing; it never
  "starts and immediately stops", and never lasts forever. Once running it
  ends when its condition stops holding — including when it merely loses
  *sight* of its object: a "for as long as" duration tracking a permanent
  ends when that permanent phases out, and does not resume on phase-in
  (702.26f).
- **Rest of game** — no stated duration means the effect lasts until the
  end of the game (611.2a).
- **One-shot: N/A** — one-shot effects do something once and *have no
  duration* (610.1; `effects.md` §2).
- **Skip-grant "durations"? No.** "Skip [something]" is a one-shot
  replacement effect over turn-structure events ("instead of doing X, do
  nothing", 614.10), not a duration — see §2 and `turn.md` §5.

Delayed start: a "the next spell you cast …" effect doesn't begin
immediately; it begins when the appropriate spell is put on the stack and
applies to it (611.2f). Static-ability effects have *no* duration of their
own — they apply at all times their source is in the appropriate zone
(611.3b); their re-evaluation story is §4.

## 2. Window grammar

The surface forms that scope rules text in time, and where each is modeled:

- **"during [step/phase/turn]"** — containment in a turn-structure interval
  (`turn.md` §1). Used as a timing restriction on actions ("Activate only
  during the upkeep step of the card's owner", forecast 702.57b) and as an
  event filter on triggers. "Only during …" / "only as a sorcery" are
  *deontic* windows — permission refinements, not durations
  (`deontics.md` §3).
- **"at the beginning of [step/phase]"** — a trigger window at the entry
  event of a structure point (`events.md` §§2, 6; `turn.md` §1). Delayed
  triggered abilities wait for the *next* occurrence after they're created
  — an event that happened just before creation doesn't count (603.7a).
- **"until [marker/event]"** — a duration terminator (§1).
- **"this turn"** — two distinct readings an engine must not conflate:
  *duration* ("gets +1/+1 this turn" — ends in cleanup, 514.2) vs
  *history look-back* ("if you attacked this turn" — a query over the
  turn-keyed event log, 608.2i; `state.md` §2).
- **Skipped windows** — anything scheduled for a skipped step/phase/turn
  doesn't happen; "the next" occurrence means the first one *not* skipped,
  and a started step/phase/turn can no longer be skipped (614.10, 614.10a).

## 3. The lock taxonomy

The core table: values the rules freeze at a definite point. Locks are
scattered across `casting.md` (the 601.2 pipeline), `choices.md` §2 (who
decides, when), `effects.md` (object sets), and the keyword rules; here
they are assembled in one place.

| What locks | When | What can still change | Recheck point |
|---|---|---|---|
| Target set + count | Announce (601.2c) | Targets' legality (zone, characteristics); the count never changes even if its defining information does (601.2c) | Resolution (608.2b): illegal targets unaffected; all illegal → doesn't resolve |
| Division / distribution among targets | Announce, min 1 per target (601.2d) | Nothing is redistributed; shares of targets that became illegal are simply lost | Resolution (608.2b); *untargeted* division locks at resolution instead (608.2d) |
| Total cost | Determination step (601.2f) | *How* it's paid — mana abilities and payment-stage substitutions happen after the lock (601.2g–h; `costs.md` §4); later cost-changing effects do nothing (601.2h example) | None |
| X | Varies: spell/ability cost X at announce (107.3a); special-action cost X immediately before payment (107.3d); ward-style trigger X at resolution, not as it triggers (702.21b); undefined text-only X at stack-placement or resolution (107.3f) | Text-*defined* X is not locked while on the stack (107.3c); it snapshots at application (608.2h) | Per context; continuous-effect X is fixed once, on resolution (611.2d, 608.2h) |
| Copiable values of a copy | When the copy is made (707.2b); for a static ability's copy effect, when it first starts to apply (707.2c) | The original — later changes to it don't propagate (707.2b); the cache itself is the layer-1 output (613.2c) | None |
| Affected-object set of a resolved continuous effect | When the effect begins, *if* it modifies characteristics or control (611.2c); phased-out permanents are excluded from the set (702.26e) | Rules-modifying parts stay open to new objects (611.2c); static-ability effects never lock (611.3a) | None — the set is fixed; membership predicates aren't re-run |
| Face-down (morph) identity | Committed at cast — the card cast face down as the 2/2 blank (702.37a; `choices.md` §3 committed-hidden) | Its *characteristics*, via effects/counters as usual; never which physical card it is | Audit: reveal on leaving the battlefield/stack or at game end (708.9) |
| Triggered-ability modes (+ targets/division) | Stack placement (603.3c), then targets/division as per casting (603.3d) | Target legality, as above; the intervening-"if" condition is NOT locked | Resolution (608.2b targets; 603.4 condition — §4) |

Reading the table: "locked" never means the *world* stops moving — it means
the recorded value stops responding to the world. The recheck column is the
one sanctioned look back at the world before the value is used.

## 4. Re-evaluation semantics

The opposite pole from locking — what the game re-computes, and how often:

- **Static-ability effects: continuously.** Never locked in; they apply at
  any given moment to whatever their text currently indicates (611.3a),
  while the source is in the appropriate zone (611.3b), with instantaneous
  recomputation through the layer system (613.5; `effects.md` §4).
- **Intervening "if": exactly twice.** Checked when the trigger event
  occurs (no trigger if false) and again as the ability resolves (removed
  from the stack if false) — mirroring the target legality recheck (603.4).
  Between the two checks the condition may oscillate freely.
- **"For as long as": continuously monitored start/stop.** A live
  predicate with the §1 edge rules (611.2b); it ends — permanently — when
  it stops holding or loses sight of its object (702.26f).
- **Resolution-stage queries: once, at application.** Game information
  used by an effect is determined a single time, when the effect is
  applied, with last known information substituting for departed objects
  (608.2h); look-back effects instead read the event log (608.2i).
- **Once-per-turn limiters: flags, not windows — with two scopes.**
  *Activation* restrictions ("Activate only once each turn", boast,
  702.142a) are **object-scoped**: the flag follows the object, continuing
  to apply even if its controller changes (602.5b), and is
  instance-scoped — an acquired ability's restriction applies only to that
  ability as acquired from that object, not to identically worded ones
  (602.5c). The *triggered* cousin "Do this only once each turn" is
  **controller-scoped**: it triggers only if "its source's controller has
  not yet taken the indicated action" that turn (603.2h). Both need
  per-turn history (`state.md` §2). Forecast composes a window ("only
  during the upkeep step of the card's owner") *and* a flag ("only once
  each turn") (702.57b).

## 5. Engine note

Three orthogonal fields fall out of §§1–4:

- **`duration`** on every continuous-effect instance:
  `FixedUntil(marker)` | `UntilEvent(pattern)` |
  `ForAsLongAs(predicate, started: bool)` | `EndOfGame` — plus `None` for
  one-shots (610.1). Cleanup sweeps `FixedUntil(end_of_turn)` (514.2); the
  combat phase end sweeps `FixedUntil(end_of_combat)` (500.5a);
  `ForAsLongAs` is checked on every state change, with `started` guarding
  the 611.2b never-started/already-ended cases.
- **`window`**: a predicate over (turn-structure position, event log) —
  shared by timing restrictions, trigger conditions, and "this turn"
  queries (§2). Turn-keyed history lives in the event log (608.2i;
  `state.md` §2), including the once-per-turn flags of §4.
- **`lock_point`** enum on every recorded choice/value:
  `Announce | StackPlacement | TotalCost | Payment | EffectBegin |
  CopyCreation | Resolution | Never(static)` — i.e. §3's "when" column.
  This is the same axis as `choices.md` §2's lock-stage column (for
  *decisions*) and `effects.md` §3's locked-object-set rules (for *sets*);
  the recheck points (608.2b targets, 603.4 conditions) are the only
  places a locked record consults the live state again.

A useful invariant: every number or set the engine stores should carry
either a `lock_point` (it is a snapshot, with at most one sanctioned
recheck) or a re-evaluation rule (it is a view over live state / the event
log). Bugs in temporal handling are almost always one of these two being
treated as the other — exactly the confusion 611.2c calls out between
resolved-effect object sets and static-ability effects.
