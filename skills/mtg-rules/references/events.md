# Events — The Event Ontology

*Synthesized from the Comprehensive Rules effective 2026-08-07
(`data/rules/cr.json`). Orientation only — verify load-bearing specifics
with `scripts/rule` before citing. Run `scripts/cite check` after CR
refreshes.*

What "an event" is, the atomic event types an engine needs, the cause tags
the CR's trigger language distinguishes, how events compose, and the
trigger/replacement interface over them. Sibling docs: `actions.md` (who
does things), `effects.md` (replacements/preventions in depth),
`engine.md` (damage pipeline + TurnHistory), `state.md` (what events
mutate), `information.md` (what events reveal).

## 1. What an event is

Anything that happens in a game is an event; multiple events may take
place during one resolution; and **the text of triggered abilities and
replacement effects defines the event they're looking for** — one
"happening" may be a single event to one ability and several to another
(700.1; the example: blocked by two creatures is one "becomes blocked"
event but two "becomes blocked by a creature" events). The action / event /
effect distinction lives in `actions.md` §1 — in short, an event is the
*fact of the happening*, the unit triggers and replacements match against.

## 2. Atomic event types — the engine inventory

**Zone-change is the master event.** Trigger events involving objects
changing zones are "zone-change triggers"; abilities that act on the moved
object look for it in the zone it moved to, and only in the *first* zone
it went to (603.6, 603.6c). Engine record:
`ZoneChange{object, from, to, position, face, cause}` — `position` for
ordered zones (library/graveyard/stack), `face` because face-down objects
are turned face down *before* they enter, so enters-abilities don't see
them (708.3), `cause` per §3. The CR names cause/endpoint-filtered views
of this one event:

| Named view | Filter on the zone change | CR |
|---|---|---|
| dies | battlefield → graveyard, **any cause** | 700.4 |
| destroyed | only via a "destroy" effect or the lethal-damage / deathtouch SBAs (704.5g, 704.5h); any other route isn't "destroyed" | 701.8a, 701.8b |
| sacrificed | controller moves their own permanent battlefield → graveyard; never destruction, so regeneration can't replace it | 701.21a |
| discarded | hand → owner's graveyard | 701.9a |
| milled | top of library → graveyard | 701.17a |
| exiled | anywhere → exile | 701.13a |
| cast | zone → stack, paying costs; "becomes cast" only after the rule 601 steps complete, when cast/put-onto-stack triggers fire | 701.5a, 601.2i |
| played (land) | onto the battlefield via the land-play special action; an effect putting a land onto the battlefield is **not** playing it | 701.18a |
| enters | → battlefield, however it got there; each event putting one or more permanents onto the battlefield is checked against all permanents' enters-triggers | 603.6a |

One note on the enters view: continuous effects that modify a
permanent's characteristics apply the moment it's on the battlefield —
it is never there unmodified — so enters-triggers are checked against
the already-modified object (603.6b).

The other atomic types an engine must emit (each is something CR trigger
or replacement text matches on):

- **Damage** — `{source, recipient, amount, combat?, source-flags}`;
  objects deal damage to battles, creatures, planeswalkers, players
  (120.1); it is combat damage (120.2a) or effect damage (120.2b). The
  full propose → replace → results → commit pipeline is `engine.md` §2 —
  fields only here.
- **Life loss / gain / set** — gain/lose adjusts the total (119.3);
  "set to N" *is* a gain or loss of the difference (119.5); damage to a
  player is normally loss (119.2); **paying life is loss** (119.4). Life
  gain is per-source: "whenever you gain life" means "whenever a source
  causes you to gain life," and 0 life gained is no event (119.9);
  simultaneous lifelink sources are separate gain events (702.15e).
- **Counter placed / removed** — counters go on objects *or players*
  (122.1); "counters put on" includes those given as the object enters
  (122.6).
- **Tap / untap** — status flips; only untapped permanents can be tapped
  and vice versa (701.26a, 701.26b), so a no-op is no event. "Becomes
  tapped/untapped" fires only on the actual transition, not on entering
  in that state (603.2e).
- **Becomes-target** — happens at announcement: chosen objects/players
  become targets during casting, and becomes-target triggers fire then,
  waiting until the spell finishes being cast (601.2c). Exemplar
  consumer: ward (702.21a).
- **Attack / block declaration** — turn-based declarations (508.1,
  509.1). "Whenever [a creature] attacks" = declared as an attacker
  (508.3a); a creature put onto the battlefield attacking is *attacking*
  but for trigger purposes never *attacked* (508.4).
- **Phase / step / turn entry** — "at the beginning of [phase/step]"
  abilities all trigger when it begins (603.2b); watchers are triggered
  abilities, never turn-based actions (703.1a); the five-phase frame is
  500.1.
- **Day/night flip** — the game gains or trades the day/night
  designation (731.1, 731.1a); the untap-step check that flips it is a
  turn-based action (502.2).
- **Phase in / out** — a status change (702.26b) that is explicitly
  *not* a zone change, so zone-change triggers never fire on phasing
  (702.26d); phase-out triggers look back in time (603.10b).
- **Coin flip / die roll** — rule 705 / rule 706. A flip is heads/tails,
  or call-and-win/lose for effects that care (705.2); a roll has a
  natural result plus modifiers (706.1, 706.2); an *ignored* roll "is
  considered to have never happened" — no triggers, no effects (706.6).
- **Shuffle** — randomize a library/pile so no player knows the order
  (701.24a); also an information event (`information.md`).
- **Reveal / look** — reveal shows a card to all players for a scoped
  window (701.20a); look-at is a named subset — visibility model in
  `information.md`.
- **Control change and other "becomes" deltas** — "becomes" trigger
  events (becomes attached, becomes blocked, …) fire only at the moment
  the state changes, never on persistence (603.2e); loses-control /
  opponent-gains-control triggers look back in time (603.10d).

## 3. Cause tags

Events carry a tag for *what caused them*, so rules can match on cause
instead of hardcoding each case. No keyword consumes this as a `given`
primitive — `cause-tagged-events` was retired from
`keyword-classification.md`'s vocabulary when its sole would-be consumer
(vigilance) collapsed to intrinsic under the dependents threshold — but
the cause model stays: trigger predicates need every coordinate of it
regardless (Karmic Justice and the agent predicates below).

The CR already runs on cause-filtered views. "Dies" is the battlefield →
graveyard change *regardless of cause* (700.4), while "destroyed" admits
exactly two causes — a destroy effect or the lethal-damage/deathtouch
SBAs (701.8b, 704.5g, 704.5h) — and "sacrificed" is the
controller-as-cost-or-instruction route that destruction rules and
regeneration never touch (701.21a). Same change, three tag filters.

**Tap causes** — the cleanest demonstration that one event type needs a
cause field:

| Cause of becoming tapped | CR hook |
|---|---|
| Cost payment — {T} in an activation cost | 107.5 |
| Attack declaration — explicitly **not** a cost; "attacking simply causes creatures to become tapped" | 508.1f |
| Crewing — "crews a Vehicle" = tapped to pay a crew cost; "can't crew" restricts exactly that cause | 702.122b, 702.122c |
| Convoke payment — tapped while paying a spell's total cost | 702.51a |
| Tapped for mana — a {T} mana ability resolving and producing mana; dedicated trigger and replacement wording | 106.12, 106.12a, 106.12b |
| Effect instruction — "tap target creature" | 701.26a |

Vigilance is the type specimen of the attack-declaration cause — but not
a consumer: the CR hardcodes "attacking doesn't cause creatures with
vigilance to tap" (702.20b) as rules text on the declare-attackers
procedure's tap (508.1f), and the classification follows it (intrinsic,
`keyword-classification.md`); the null replacement on
tap(cause: attack-declaration) survives only as vigilance's documented
hypothetical decomposition. (Enlist needs no cause tags either: it is an
optional cost to attack, 508.1g, whose trigger keys on that payment via
ability *linkage*, 607.2h — the CR says so itself, 702.154b.)

Other cause dimensions the CR's wording distinguishes:

- **Discard**: cost vs effect vs the cleanup turn-based discard (703.4n).
  Most discard triggers are cause-agnostic, but cost-discards have their
  own illegal-payment rewind nuance (701.9c).
- **Damage**: combat (120.2a) vs spell/ability effect (120.2b) — "combat
  damage" triggers filter on this tag.
- **Life loss**: from damage (119.2), from paying (119.4), from an effect
  (119.3); gain is always source-attributed (119.9).
- **Event vs state**: "attacks" fires only on the declaration cause —
  put-onto-the-battlefield-attacking creatures never "attacked" (508.3a,
  508.4); a land put onto the battlefield by an effect was never "played"
  (701.18a); cast vs other arrivals on the stack (601.2i).

Settled vocabulary — a cause is a *(verb, agency, agent)* triple: the
**verb tag** is the named view performed (destroy, sacrifice, discard,
mill, exile, play, cast, crew, …: the intrinsic keyword actions of
`keyword-classification.md`); the **agency tag** is the machinery that
demanded it: `cost-payment` | `attack-declaration` |
`effect-instruction` | `turn-based-action` | `state-based-action` |
`mana-ability-resolution`; and the **agent** is the causing object plus
its controller — nullable, since turn-based and state-based actions have
neither. The agent coordinate is what oracle text reads when it asks
*who did it*: Karmic Justice's "whenever a spell or ability an opponent
controls destroys a noncreature permanent you control" predicates on
agent kind and agent controller; the whole "when a spell or ability an
opponent controls causes you to discard this card" family does the same
over discard events; and "destroyed this way" / "removed this way" is
agent-*identity* equality — match exactly the events whose agent is this
very spell or ability. Every CR distinction above is a predicate over
one or more coordinates. What cause tags do *not* carry is event
ancestry: "dies from combat damage"-style filters join a death event to
an earlier damage event, which is the §5 log/look-back's job, not a
cause tag's.

## 4. Composition

- **One event, many objects.** An ability triggers once per event but
  repeatedly if one event contains multiple occurrences (603.2c —
  destroy-all-lands triggers a lands-die watcher once per land); whether
  a happening is one event or several is decided by the watcher's text
  (700.1). One event can put several permanents onto the battlefield at
  once (603.6a); all SBAs performed on a check happen "simultaneously as
  a single event" (704.3); all assigned combat damage (510.1) is dealt
  simultaneously as one batch (510.2) — yet that single batch still
  yields a separate life-gain event per lifelink source (702.15e),
  because life gain is per-source by definition (119.9): one commit,
  many cause-distinguished events.
- **Once per event.** A replacement effect gets one opportunity to affect
  an event and the modified events that replace it (614.5); across the
  replacements modifying how permanents enter the battlefield, the same
  object can't be chosen to change zones twice (614.13a, 614.13b).
- **Contained events.** One replacement may apply to an event and another
  to an event *contained within* it — the outer one must be chosen first
  (616.1g: token creation contains entering the battlefield, so Doubling
  Season applies before per-token as-enters choices). Draw N is N
  individual draw events, but effects modifying "the number of cards
  drawn" apply before any individual draw (121.2, 121.2a).
- **Trigger batching.** Everything that triggered since the last priority
  grant goes on the stack in APNAP order, each player ordering their own
  (603.3b) — events commit first, triggers batch after.

## 5. History and look-back

Events are the log. Effects that say "this turn" look back in time at
previous game states and actions, not at the current snapshot (608.2i) —
an engine therefore keeps an event log keyed by turn (`state.md` §2
enumerates the kinds; `engine.md` renders it as `TurnHistory`). When an
effect needs information about an object no longer in its expected public
zone, it uses **last known information** (608.2h, 113.7a) — LKI is a
snapshot read from the log. Timing matters: a permanent that leaves via a
state-based action takes its LKI from *before any of that batch's SBAs
were performed*, not mid-batch (704.8).

## 6. The trigger interface

- A trigger condition is a predicate over **(event, state)**: an ability
  triggers whenever "a game event or game state" matches it (603.2).
- **Intervening "if"**: the stated condition is checked when the event
  occurs (no trigger if false) and *again* on resolution (fizzles if
  false) (603.4).
- **Look-back triggers** (603.10): normally objects as they exist
  *after* the event are checked; the listed exceptions evaluate the
  world immediately *before* it — leaves-the-battlefield, sacrifice,
  leaves-a-graveyard, and visible-card-to-hand/library triggers
  (603.10a), phasing out (603.10b), becoming unattached (603.10c),
  losing control (603.10d), being countered (603.10e), losing the game
  (603.10f), planeswalking away (603.10g). The LTB trigger *category*
  is defined at 603.6c.
- **Visibility gate**: if the object with the trigger is at no time
  visible to all players, it doesn't trigger (603.2f).
- **"Whenever X or Y"** is a pattern union: one ability whose text
  defines a disjunctive event pattern (700.1); it still triggers once
  per matching event occurrence (603.2c).
- **Replaced events trigger nothing**: an event that's prevented or
  replaced won't trigger anything (603.2g).

## 7. Engine schema

```python
class Event:
    type: Enum            # §2 inventory: ZoneChange, Damage, LifeChange, …
    participants: list    # objects/players involved (one event, many objects)
    fields: dict          # per-type payload (from/to/position/face, amount, …)
    cause: (verb, agency, agent)  # §3 triple; agent = causing object
                          # + its controller, None for turn/state-based
    parent: Event|None    # contained-event nesting (616.1g, 121.2a)
    ordering: int         # commit order within the log (608.2i)
```

The **rewriter acts pre-commit**: while an event is still prospective,
run the replacement fixpoint — a replaced event *never happens* (614.6),
so it triggers nothing (603.2g); the modified event occurs instead and
may itself trigger abilities (614.6); and each replacement is marked
used per event (614.5). **Triggers act post-commit**: committed events are matched
against (event, state) predicates (603.2), batch onto the stack at the
next priority grant (603.3b), and re-check intervening-if conditions on
resolution (603.4). Committed events append to the turn-keyed log with
the LKI snapshots look-back consumers will need (608.2i, 704.8).
