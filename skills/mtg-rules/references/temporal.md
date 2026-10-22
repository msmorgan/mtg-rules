# Temporal Scope — Durations, Windows, Locks

*Synthesized from the Comprehensive Rules effective 2026-09-25
(`data/rules/cr.json`).*

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
  beginning of the end of combat step (500.5a, 511.2). "Until [step/phase]"
  effects expire as that step/phase begins (500.4); "until end of
  [step/phase]" effects expire as it ends (500.5). "Until your next turn"
  ends as that player's next turn begins (implied by 800.4m; Nivix, Aerie
  of the Firemind ruling [2006-02-01]), and an additional beginning phase
  within the current turn doesn't end it (Sphinx of the Second Sun ruling).
  "Next" means the next occurrence actually taken, not skipped (614.10a;
  723.1–723.1b for player control). If that player leaves the game, such
  durations last until that turn would have begun (800.4m).
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
  ends when its condition stops holding and does not resume if the
  condition holds again later (Master Thief [2011-09-22]: regaining
  control of Master Thief doesn't return the artifact; Willbreaker
  ruling) — including when it merely loses *sight* of its object: a "for
  as long as" duration tracking a permanent ends when that permanent
  phases out, and does not resume on phase-in (702.26f).
- **Rest of game** — no stated duration means the effect lasts until the
  end of the game (611.2a).
- **One-shot: N/A** — one-shot effects do something once and *have no
  duration* (610.1; `effects.md` §2).
- **Skip effects: continuous replacements, not one-shots.** Skip effects
  are continuous replacement effects (614.1, 614.1b): "skip X" means
  "instead of doing X, do nothing" (614.10). A resolved "skip your next X"
  persists until it has replaced one occurrence that wasn't already
  started or skipped (614.10, 614.10a). A static skip applies while its
  source is in the appropriate zone (611.3b). They are not one-shot
  effects, and they are not durations — see §2, `effects.md` §6 and
  `turn.md` §5.

Delayed start: a "the next spell you cast …" effect doesn't begin
immediately; it begins when the appropriate spell is put on the stack and
applies to it (611.2f). Static-ability effects have no duration of their
own — they apply at all times their source is in the appropriate zone
(611.3b), except that a battlefield ability granted along with a static
play/cast permission lasts as stated, or until end of game if no duration
is stated (611.3d, an explicit exception to 611.3a–b); their re-evaluation
story is §4.

## 2. Window grammar

The surface forms that scope rules text in time, and where each is modeled:

- **"during [step/phase/turn]"** — containment in a turn-structure interval
  (`turn.md` §1). Used as a timing restriction on actions ("Activate only
  during the upkeep step of the card's owner", forecast 702.57b) and as an
  event filter on triggers. "Only during …" / "only as a sorcery" are
  *deontic* windows — permission refinements, not durations
  (`deontics.md` §3). The sorcery window is a closed test: the player has
  priority, it is the main phase of their turn, and the stack is empty. It
  never asks whether a sorcery could actually be cast (307.5). Its
  look-back mirror, "if you cast it any time a sorcery couldn't have been
  cast," is the same test negated at the moment of casting: no priority,
  *or* not that player's main phase (so any opponent's turn), *or* another
  object on the stack (307.5a). The cast event must therefore carry those
  three facts for the later check (engine inference).
- **"at the beginning of [step/phase]"** — a trigger window at the entry
  event of a structure point (`events.md` §§2, 6; `turn.md` §1). Delayed
  triggered abilities wait for the *next* occurrence after they're created
  — an event that happened just before creation doesn't count (603.7a).
  Abilities trigger only as the step/phase begins (603.2b), so a
  permanent's or a delayed "at the beginning of the end step" trigger that
  appears during the end step waits for the next turn's end step; the step
  doesn't back up (513.2). This doesn't apply to "until end of turn" /
  "this turn" durations (513.2).
- **"only before/after [combat point]"** (cast or activate) — keyed to the
  start of the declare-attackers/blockers step, regardless of whether any
  attackers or blockers are declared (506.8a–b). With multiple combats,
  first combat phase only, unless the text also says "during combat" or
  "during [a player's] combat phase" (506.8c–d). Fallbacks apply when the
  point or phase is skipped (506.8e–f). Applies to abilities too (506.8g).
  Derived in `turn.md` §3.
- **"until [marker/event]"** — a duration terminator (§1).
- **"this turn"** — two distinct readings an engine must not conflate:
  *duration* ("gets +1/+1 this turn" — ends in cleanup, 514.2) vs
  *history look-back* ("if you attacked this turn" — a query over the
  turn-keyed event log, 608.2i; `state.md` §2).
- **"since the beginning of your last upkeep"** (echo, 702.30a) — a
  look-back window read at the beginning of an upkeep and again on
  resolution (603.4). "Last" is the upkeep *before* the one whose beginning
  fired the trigger. Anchoring at the current onset leaves the window
  empty, so echo never triggers. Anchoring by turn breaks extra upkeeps:
  echo that triggered in a turn's first upkeep doesn't trigger again in a
  Paradox Haze upkeep that turn (Paradox Haze ruling [2006-09-25]). "Came
  under your control" matches entering, gaining control, and regaining it
  (Orcish Hellraiser ruling [2019-06-14]). Contrast "since their most
  recent turn began" (302.6), which includes the current turn. With no
  earlier upkeep, the window starts at the beginning of the game (engine
  inference; UD-36).
- **Skipped windows** — anything scheduled for a skipped step/phase/turn
  doesn't happen; "the next" occurrence means the first one *not* skipped,
  and a started step/phase/turn can no longer be skipped (614.10, 614.10a).
- **Delayed triggers fire once unless given a duration** (603.7b). Their
  referent lock is in §3 (603.7c).

## 3. The lock taxonomy

The core table: values the rules freeze at a definite point. Locks are
scattered across `casting.md` (the 601.2 pipeline), `choices.md` §2 (who
decides, when), `effects.md` (object sets), and the keyword rules; here
they are assembled in one place.

| What locks | When | What can still change | Recheck point |
|---|---|---|---|
| Target set + count | Announce (601.2c) | Targets' legality (zone, characteristics); which objects are targeted, but only via change-target / choose-new-targets effects (115.7a–e); the count stays fixed (601.2c) — even if its defining information changes — and any announced division stays fixed (115.7f) | Resolution (608.2b): illegal targets unaffected by the parts of the effect for which they're illegal (608.2b); all illegal → doesn't resolve |
| Player-chosen division among targets | Announce, min 1 per target (601.2d) | Nothing, not even when targets are changed (115.7f); illegal targets' shares are lost (608.2b; Arc Lightning ruling [2014-09-20]) | Resolution (608.2b); *untargeted* division locks at resolution instead (608.2d). A rules-determined division with no player choice (e.g. "divided evenly") is computed at resolution among the still-legal targets (Fireball ruling [2017-11-17]) |
| Total cost | Determination step (601.2f) | *How* it's paid — mana abilities and payment-stage substitutions happen after the lock (601.2g–h; `costs.md` §4); later cost-changing effects do nothing (601.2f; illustrated by the 601.2h example) | None |
| X | Varies: spell/ability cost X at announce (107.3a); special-action cost X immediately before payment (107.3d); ward-style trigger X at resolution, not as it triggers (702.21b); undefined text-only X at stack-placement or resolution (107.3f); inherited X: an ETB trigger/replacement takes its spell's X (107.3m), a delayed trigger takes its creator's X (107.3n); a spell-text X defined by a later choice is pulled forward to announcement (601.2b) | Text-*defined* X is not locked while on the stack (107.3c); it snapshots at application (608.2h) | Per context; continuous-effect X is fixed once, on resolution (611.2d, 608.2h) |
| Copiable values of a copy | When the copy is made (707.2b); for a static ability's copy effect, when it first starts to apply (707.2c) | The original — later changes to it don't propagate (707.2b); the cache itself is the layer-1 output (613.2c) | None |
| Affected-object set of a resolved continuous effect | When the effect begins, *if* it modifies characteristics or control (611.2c); phased-out permanents are excluded from the set (702.26e) | Rules-modifying parts stay open to new objects (611.2c); static-ability effects never lock (611.3a) | None — the set is fixed; membership predicates aren't re-run |
| Face-down (morph) identity | Committed when the card becomes face down: e.g. cast face down via morph/disguise (702.37a, 702.168a), put onto the battlefield face down via manifest/cloak (701.40a, 701.58a), or any other effect that turns it face down or puts it onto the battlefield face down (708.2a) (`choices.md` §3 committed-hidden) | Its *characteristics*, via effects/counters as usual; never which physical card it is | Audit: reveal when it moves from the battlefield to another zone, when a face-down spell moves from the stack to any zone other than the battlefield, when its owner leaves the game, and at game end (708.9) |
| Triggered-ability modes (+ targets/division) | Stack placement (603.3c), then targets/division as per casting (603.3d) | Target legality, as above; the intervening-"if" condition is NOT locked | Resolution (608.2b targets; 603.4 condition — §4) |
| Object a delayed trigger refers to | Creation (603.7a); if the creating effect moved the object to a public zone, the referent is the object in that zone, so "exile it … return it at the beginning of the next end step" refers to the exiled card (400.7j) | Its characteristics; the ability still affects it (603.7c) | Resolution: if it is no longer in the zone it's expected to be in, the ability won't affect it, even if it left and came back, because that is a new object (603.7c, 400.7); reads of the departed object use last known information (608.2h) |
| Source information | Fixed at stack placement when needed to announce an activated ability or put a triggered ability on the stack; otherwise read when the ability resolves, using LKI if the source has left its zone (113.7a, 608.2h) | n/a | None |

Reading the table: "locked" never means the *world* stops moving — it means
the recorded value stops responding to the world. The recheck column is the
one sanctioned look back at the world before the value is used.

## 4. Re-evaluation semantics

The opposite pole from locking — what the game re-computes, and how often:

- **Static-ability effects: continuously.** Never locked in, except a
  static copy effect's copiable values, which are fixed when the effect
  first starts to apply (707.2c); they apply at any given moment to
  whatever their text currently indicates (611.3a), while the source is in
  the appropriate zone (611.3b), with instantaneous recomputation through
  the layer system (613.5; `effects.md` §4).
- **Intervening "if": exactly twice.** Checked when the trigger event
  occurs (no trigger if false) and again as the ability resolves (removed
  from the stack if false) — mirroring the target legality recheck (603.4).
  Between the two checks the condition may oscillate freely.
- **"For as long as": continuously monitored start/stop.** A live
  predicate with the §1 edge rules (611.2b); once it stops holding it
  doesn't resume (Master Thief [2011-09-22]; Willbreaker ruling), and the
  same goes for losing sight of its object by phasing out (702.26f).
- **Resolution-stage queries: once, at application.** Game information
  used by an effect is determined a single time, when the effect is
  applied, with last known information substituting for departed objects
  (608.2h); look-back effects instead read the event log (608.2i).
- **Replacement/prevention effects: per event.** Evaluated as each event
  would occur, never locked ahead (614.1, 615.1); see `effects.md` §§6–7.
- **Once-per-turn and once-only limiters: flags, not windows — with two
  scopes.** *Activation* restrictions ("Activate only once each turn",
  boast, 702.142a) are **object-scoped**: the flag follows the object,
  continuing to apply even if its controller changes (602.5b), and is
  instance-scoped — an acquired ability's restriction applies only to that
  ability as acquired from that object, not to identically worded ones
  (602.5c). "Activate only once" without "each turn" (exhaust, 702.177a;
  power-up, 702.193a) is the same object-scoped flag, but over the
  object's whole existence. It survives a control change (602.5b) and
  resets only when the permanent changes zones and returns as a new object
  (400.7; Boommobile ruling [2025-02-07]). An effect that lets you
  activate exhaust abilities "as though they haven't been activated"
  suspends the flag for its own purpose only (609.4). "As long as you
  haven't activated an exhaust ability this turn" is a per-player
  look-back that counts any exhaust activation already *begun* (702.177b).
  The *triggered* cousin "Do this only once each turn" counts the
  **action**, keyed to the ability on its source (not to each triggered
  instance of it) and to its source's controller. It triggers only if "its
  source's controller has not yet taken the indicated action" that turn
  (603.2h), so declining a "may" leaves it free to trigger again. The
  action counted is the one taken with this ability, not with an
  identically worded one: two Nykthos Paragons each allow it once
  (Riveteers Ascendancy [2022-04-29]). Once the action is taken, that
  ability's instances already on the stack do nothing (Nykthos Paragon
  [2021-06-18]; Calix, Guided by Fate [2023-05-12]; Spider-Verse
  [2025-09-19]). This resolution-time gate is settled by ruling and is not
  in 603.2h (UD-41). The distinct template "This
  ability triggers only once each turn" counts *triggerings*, not actions,
  even while the first is still on the stack (Elvish Warmaster
  [2021-02-05]). The CR uses the template in 702.179d but never defines it
  (UD-35). Both need per-turn history (`state.md`
  §2). Forecast composes a window ("only during the upkeep step of the
  card's owner") *and* a flag ("only once each turn") (702.57b).
- **Ordinal-within-turn wordings: windows, not flags.** "Whenever you gain
  life for the first time each turn", "your second card each turn", "your
  first spell during each opponent's turn", and the replacement form "The
  first time you would … each turn" are part of the trigger event (603.2)
  or the replaced event (614.1a) and test the turn's event log (`events.md`
  §5). They do not count the ability's own uses. No CR rule defines them;
  official rulings fix the reading. A matching event earlier that turn uses
  up "first" even if it happened before the source was on the battlefield
  (Attended Healer [2020-09-25], Wavebreak Hippocamp [2020-01-24]). The
  test is whether the creature "hasn't yet been the target of a spell or
  ability you control this turn" (Heartfire Hero [2024-07-26]; Angelic Cub
  [2024-11-08]). By the same reading, an event that happened while the
  ability was present but couldn't trigger also uses it up (engine
  inference). Tokens created before the source came under your control use
  up the replacement form, and so does declining it (Moonlit Meditation
  [2025-07-25]). Contrast the cap "This ability triggers only once each
  turn", which appears in CR text only inside 702.179d's speed ability. The
  cap counts this ability's own triggerings, whether or not they resolve
  (Elvish Warmaster [2021-02-05]), and each grantor's copy of a granted
  ability counts separately (Cursed Wombat [2024-06-07]), the triggered
  analogue of 602.5c (UD-35).

## 5. Engine note

Three orthogonal fields fall out of §§1–4:

- **`duration`** on every continuous-effect instance:
  `FixedUntil(start_of step|phase|turn)` | `FixedUntil(end_of step|phase)` |
  `UntilEvent(pattern)` | `ForAsLongAs(predicate, started: bool)` |
  `EndOfGame` — plus `None` for one-shots (610.1). `FixedUntil(start_of …)`
  is swept as that point begins (500.4); `FixedUntil(end_of step|phase)` as
  it ends (500.5). Cleanup sweeps `FixedUntil(end_of_turn)` (514.2); the
  combat phase end sweeps `FixedUntil(end_of_combat)` (500.5a);
  `ForAsLongAs` is checked on every state change, with `started` guarding
  the 611.2b never-started/already-ended cases.
- **`window`**: a predicate over (turn-structure position, event log) —
  shared by timing restrictions, trigger conditions, and "this turn"
  queries (§2). Turn-keyed history lives in the event log (608.2i;
  `state.md` §2), including the once-per-turn flags of §4.
- **`lock_point`** enum on every recorded choice/value:
  `Announce | StackPlacement | TotalCost | Payment | EffectBegin |
  CopyCreation | Resolution | Declaration(attack|block) | DamageAssignment |
  PreGame | SpecialAction | PerApplication | Never(static) |
  FirstApplication` — i.e. §3's "when" column plus the declaration
  (508.1a, 509.1a), damage-assignment (510.1), pre-game (103.1, 103.5),
  special-action (116.1–116.2) and per-application (616.1) stages of
  `choices.md` §2. `FirstApplication` (707.2c) is the exception to
  `Never(static)`. This is the same axis as `choices.md` §2's lock-stage
  column (for *decisions*) and `effects.md` §3's locked-object-set rules
  (for *sets*). The principal recheck points are 608.2b (targets, using
  the source's LKI if it has left its zone) and 603.4 (intervening "if");
  others include 603.7c (a delayed trigger's referent must still be in the
  expected zone), the "Do this only once each turn" gate at resolution
  (Calix, Guided by Fate; Riveteers Ascendancy rulings) and the 708.9
  face-down reveal audit. Resolution-time reads under 608.2h/113.7a are
  first reads, not rechecks (§4).

A useful invariant: every number or set the engine stores should carry
either a `lock_point` (it is a snapshot, with at most one sanctioned
recheck) or a re-evaluation rule (it is a view over live state / the event
log). Bugs in temporal handling are almost always one of these two being
treated as the other — exactly the confusion 611.2c calls out between
resolved-effect object sets and static-ability effects.
