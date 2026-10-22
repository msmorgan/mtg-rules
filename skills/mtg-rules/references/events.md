# Events — The Event Ontology

*Synthesized from the Comprehensive Rules effective 2026-09-25
(`data/rules/cr.json`).*

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
ordered zones (library/graveyard/stack), `face` because a face-down
object is turned face down *before* it enters, so its own enters
abilities neither trigger nor apply (708.3; face-down characteristics
708.2a); other permanents' enters triggers match it as the face-down
permanent (603.6a, 603.6b), `cause` per §3. The CR names two kinds of
views of this one event.

**Verb-identified views** — the identity is the verb; the default
destination can be replaced and the object still counts:

| Named view | Filter on the zone change | CR |
|---|---|---|
| destroyed | only via a "destroy" effect or the lethal-damage / deathtouch SBAs (704.5g, 704.5h); any other route isn't "destroyed"; the default destination is the owner's graveyard | 701.8a, 701.8b |
| sacrificed | controller moves their own permanent from the battlefield to its owner's graveyard by default; never destruction, so regeneration can't replace it | 701.21a |
| discarded | the discard action from hand, whether as a cost, an effect, the cleanup turn-based action (703.4n, 514.1) or the special action of 116.2e; default destination the owner's graveyard (701.9a); a discard redirected elsewhere still counts (701.9c, 702.35a) | 701.9a, 701.9c, 702.35a, 703.4n, 514.1, 116.2e |
| milled | the mill action from the top of a library, also possible as a cost (701.17b); default destination the graveyard (701.17a); a card moved elsewhere instead is still milled and is found in the zone it moved to (701.17c) | 701.17a, 701.17b, 701.17c |
| drawn | library top → hand via the draw action only (121.1, 121.5). Draw replacements apply even with an empty library (121.6a, 614.11). An attempt to draw from an empty library draws nothing, so draw triggers don't fire; the attempt is recorded for the 704.5b loss check (121.4) | 121.1, 121.4, 121.5, 121.6a, 614.11 |
| countered | a spell or ability removed from the stack by a counter effect (701.6a). A countered spell goes to its owner's graveyard unless that is replaced (Dissipate exiles it); a countered ability ceases to exist; look-back per 603.10e | 701.6a, 603.10e |
| created | tokens put onto the battlefield by a create instruction (701.7a); replacement order per 701.7b and 616.1g; a resolving copy of a permanent spell is not "created" (608.3f) | 701.7a, 701.7b, 616.1g, 608.3f |
| cast | zone → stack, paying costs; "becomes cast" only after the rule 601 steps complete, when cast/put-onto-stack triggers fire | 701.5a, 601.2i |
| played (land) | onto the battlefield via the land-play special action; an effect putting a land onto the battlefield is **not** playing it | 701.18a |

**Destination-identified views** — the identity is where the object ends
up:

| Named view | Filter on the zone change | CR |
|---|---|---|
| dies | battlefield → graveyard, **any cause** | 700.4 |
| exiled | anywhere → exile | 701.13a |
| enters | → battlefield, however it got there; each event putting one or more permanents onto the battlefield is checked against all permanents' enters-triggers | 603.6a |

With Rest in Peace on the battlefield, discard, destroy and sacrifice
triggers still fire; dies triggers do not.

One note on the enters view: continuous effects that modify a
permanent's characteristics apply the moment it's on the battlefield —
it is never there unmodified — so enters-triggers are checked against
the already-modified object (603.6b).

The keyword-action list is open: the verbs above are only those whose
trigger or replacement wording matters here. The full list is
`data/rules/keywords.json` (`.keywordActions`), as `actions.md` §5 says.

The other atomic types an engine must emit (each is something CR trigger
or replacement text matches on):

- **Damage** — `{source, recipient, amount, combat?, source-flags}`;
  objects deal damage to battles, creatures, planeswalkers, players
  (120.1); it is combat damage (120.2a) or effect damage (120.2b). The
  full propose → replace → results → commit pipeline is `engine.md` §2 —
  fields only here.
- **Life loss / gain / set** — gain/lose adjusts the total (119.3);
  "set to N" *is* a gain or loss of the difference (119.5), and so are
  doubling a life total (701.10d) and exchanging it (701.12c, 701.12g).
  Because each is a gain or loss, life-gain and life-loss replacements
  and triggers apply to it (119.9, 119.10); for exchanges the CR says so
  explicitly (701.12c, 701.12g); damage to a player is normally loss
  (119.2); **paying life is loss** (119.4). Life gain is per-source:
  "whenever you gain life" means "whenever a source causes you to gain
  life," and 0 life gained is no event (119.9); simultaneous lifelink
  sources are separate gain events (702.15e).
- **Counter placed / removed** — counters go on objects *or players*
  (122.1). The transfer wordings differ in which events happen:
  - **"Put on"** includes counters an object is given as it enters
    (122.6); unless the effect names a player, the object's controller
    puts them on it (122.6a). Counters that cease to exist on a zone
    change are not "removed" (122.2).
  - **"Move"** is a removal plus a placement, all-or-nothing. If either
    half is impossible, nothing is removed or put: the same object, no
    such counter on the first object, a second object that can't have
    counters put on it, or either object out of its zone (122.5). The
    placement half is an ordinary placement, which counter triggers and
    replacements see (Simic Fluxmage [2013-01-24]). Composite guard: see
    §4 "All-or-nothing composites".
  - **"Put its counters on"** moves nothing when it comes from a
    triggered ability whose trigger condition or effect checks that the
    source left the battlefield (122.8), or from an activated ability
    that sacrificed the source as a cost (122.9). Those counters stopped
    existing with the zone change (122.2). The result is placements
    only: the same number of each kind (or of each named kind) the
    source had, read from last known information (608.2h), -1/-1
    counters included (Star Pupil [2021-04-16]). "Put the same number of
    each kind" from a source still on the battlefield (Denry Klin,
    Editor in Chief) is placements by its own wording, and the source
    keeps its counters.
  - **"When/Whenever the Nth [kind] counter is put on [it]"** is a
    threshold crossing, not a count of placements. It triggers when one
    or more counters of that kind are put on such that the object had
    fewer than N before and N or more after (122.7; Midnight Clock
    [2019-10-04]). A batch that jumps past N triggers it once; a
    placement that starts at N or more doesn't trigger it. After
    removals take the count below N, a later placement can cross again.
    Saga chapters use the same before/after edge (714.2b).
- **Double / triple / exchange** — these have no event of their own.
  Each reduces either to an event above, whose triggers and replacements
  apply, or to a continuous effect, which is no event. Doubling a life
  total is a gain or loss that leaves twice the current value (701.10d).
  Doubling counters puts that many more on, so counter replacements
  change the number (701.10e; Kalonian Hydra [2013-07-01]). Doubling
  mana adds that much more of the type (701.10f). Doubling damage is a
  replacement effect (701.10g). Doubling or tripling power and/or
  toughness is a layer-7c modification, never a set (701.10a, 701.11a,
  613.4c); it gives +X, or -X when the value is negative (701.10b,
  701.10c, 701.11b, 701.11c), one of 107.1b's exceptions to treating a
  negative result as zero. Exchange is all-or-nothing (701.12a).
  Exchanging life totals is a gain or loss on each side, and exchanging
  a life total with another number is a gain or loss for that player.
  Replacements modify these and triggers see them (701.12c, 701.12g). A
  player who can't gain (or lose) life can't be raised (or lowered) this
  way (701.12c, 701.12g), which stops the whole exchange: "neither
  player's life total will change" (Soul Conduit [2011-06-01]).
  Exchanging a power or toughness creates a layer-7b setting effect
  (701.12g, 613.4b). A creature switching its own power and toughness is
  layer 7d, not an exchange (701.12g, 613.4d). Control of two permanents
  changes simultaneously, or not at all when one player controls both
  (701.12b). Cards in two zones swap only when one player owns them all,
  and they swap even if one zone is empty (701.12d); attachments follow
  the swap (701.12e). Whole zones swap even when one is empty (701.12f).
  Text boxes swap through a text-changing effect, not an event
  (701.12h, 612.1).
- **Tap / untap** — status flips; only untapped permanents can be tapped
  and vice versa (701.26a, 701.26b), so a no-op is no event. "Becomes
  tapped/untapped" fires only on the actual transition, not on entering
  in that state (603.2e).
- **Becomes-target** — happens at announcement: chosen objects/players
  become targets during casting, and becomes-target triggers fire then,
  waiting until the spell finishes being cast (601.2c). Activating an
  ability and putting a triggered ability on the stack run the same step
  (602.2b, 603.3d). Exemplar consumer: ward (702.21a). The CR states
  this event only for announcement, and rulings supply the rest. An
  object or player also becomes a target when a spell's or ability's
  target is changed to it (115.7a, 115.7b, 115.7c, 115.7d): "the new
  target is considered to be targeted ... This will trigger any effects
  which trigger on being targeted" (Deflection [2004-10-04]; Angelic Cub
  [2024-11-08]). It also becomes a target when a copy is put onto the
  stack targeting it, whether or not that target was changed (707.10,
  707.10c; Dormant Gomazoa [2010-06-15]), because the copy is a new
  spell or ability. A target left unchanged by a redirect of the *same*
  spell was already its target, and a "becomes" event fires only on the
  transition (603.2e). Cast-keyed wordings ("whenever you cast a spell
  that targets ...", heroic) never see a redirect or a copy, because
  nothing is cast (707.10; Akroan Crusader [2013-09-15]).
- **Crime** — a player commits a crime *as* they cast a spell, activate
  an ability, or put a triggered ability on the stack that targets an
  opponent; a permanent, spell, or ability an opponent controls; and/or
  a card in an opponent's graveyard (700.13). The targets that make it a
  crime are those chosen at announcement (601.2c, 602.2b, 603.3d), but
  the crime is committed when casting, activating, or putting the
  ability on the stack is finished. Costs are paid by then: a Forsaken
  Miner sacrificed to pay that spell's cost still sees the crime. It
  doesn't matter whether the spell or ability ever resolves (Forsaken
  Miner [2024-04-12]). A spell or ability commits one crime however many
  criminal targets it has. Only the initial targets count, so changing
  targets later neither commits nor undoes a crime. A copied spell or
  activated ability is neither cast nor activated (707.10), so copying
  one commits no crime. Whether putting a *copy* of a triggered ability
  on the stack counts as "puts a triggered ability on the stack" is
  unstated (UD-26; 707.10 says "A copy of an
  ability is itself an ability").
- **Attack / block declaration** — turn-based declarations (508.1,
  509.1). "Whenever [a creature] attacks" = declared as an attacker
  (508.3a). A creature put onto the battlefield attacking, or stated to
  be attacking, is *attacking* but for trigger events and effects never
  *attacked* (508.4; `turn.md` §3). Every attack and block trigger
  template, with its grain, is in *Combat-declaration triggers* below.
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
- **Transform / convert** — a permanent turns to its other face while
  staying on the battlefield (701.27a, 701.28a). This is a different
  action from turning face up or down, so turned-face-down triggers
  don't fire on a transform, and so on (701.27b, 701.28b). "Transforms
  into [an object with a quality]" matches a transform *or* a convert
  after which the permanent has that quality, whatever it was before
  (701.27e; Cult of the Waxing Moon [2016-04-08]). A bare "transforms"
  trigger also fires on a convert (Megatron, Tyrant [2022-10-14]).
  Entering the battlefield back face up (712.14a) is not transforming:
  "A non-Human creature that's put onto the battlefield transformed ...
  will not cause Cult of the Waxing Moon's ability to trigger" (Cult
  [2016-04-08]). Oracle text that wants both cases names both
  ("transforms or ... enters transformed", Corruption of Towashi).
- **Coin flip / die roll** — rule 705 / rule 706. A flip is heads/tails,
  or call-and-win/lose for effects that care (705.2); a roll has a
  natural result plus modifiers (706.2); an *ignored* roll "is
  considered to have never happened" — no triggers, no effects (706.6). A
  planar-die roll matches roll triggers but has no numerical result (706.7,
  901.9d; `choices.md` §4).
- **Shuffle** — randomize a library/pile so no player knows the order
  (701.24a); also an information event (`information.md`).
- **Reveal / look** — reveal shows a card to all players for a scoped
  window (701.20a); look-at is a named subset — visibility model in
  `information.md`.
- **Control change and other "becomes" deltas** — "becomes" trigger
  events (becomes attached, becomes blocked, …) fire only at the moment
  the state changes, never on persistence (603.2e); loses-control /
  opponent-gains-control triggers look back in time (603.10d).
- **Keyword-action events** — no rule says that an action which did
  nothing produces no event. The CR answers verb by verb, so an engine
  carries per-verb flags rather than one no-op rule (**engine
  inference**):
  - *Happens even if some or all of its steps were impossible*, with the
    event landing after the whole process: scry (701.22d), surveil
    (701.25d), explore (701.44b), amass (701.47b), connive (701.50f),
    the Ring tempts you (701.54d), discover (701.57b), manifest dread
    (701.62b). Also, in other wording: shuffle, even with nothing to
    shuffle in or a library of zero or one cards, and shuffle triggers
    still fire (701.24c, 701.24d, 701.24e); set in motion (701.32b); and
    exert, even on an already tapped or exerted permanent (701.43b).
  - *A zero count withholds the event:* scry 0 and surveil 0, where "no
    ... event occurs" (701.22b, 701.25c); connive 0 (701.50e); endure 0,
    where "nothing happens" (701.63b); transform or convert of a
    permanent with no other face, or into an instant or sorcery face:
    "nothing happens" (701.27c, 701.27d, 701.28c, 701.28d). The
    non-keyword siblings are gaining 0 life (119.9) and dealing 0 damage
    (120.8).
  - *All-or-nothing:* in a fight, if either creature has left the
    battlefield, stopped being a creature, or is an illegal target,
    neither fights (701.14b). Exchange (701.12a) and moving a counter
    (122.5) work the same way; see §4 "All-or-nothing composites".
  - For verbs the CR doesn't address, rulings decide case by case. For
    example, a player who proliferates while choosing nothing has still
    proliferated (Venomous Brutalizer [2023-02-04]).

**Combat-declaration triggers.** The CR lists attack-trigger (508.3a,
508.3b, 508.3c, 508.3d, 508.3e, 508.3f) and block-trigger (509.3a,
509.3b, 509.3c, 509.3d, 509.3e, 509.3f, 509.3g) templates. Each one
slices the single declaration at its own grain (700.1). Other
declaration-keyed forms ("attacks alone", 506.5, 506.6, and the counted
forms of 509.3e) are covered below. A counted subject ("one or more
creatures you control attack") makes any of them once per declaration
(603.2c, 700.1).

| Template | Fires | Also fires | Never fires | CR |
|---|---|---|---|---|
| "Whenever [a creature] attacks [a player, planeswalker, or battle]" | per creature declared as an attacker (attacking that player or permanent) | — | for a creature put onto the battlefield attacking | 508.3a |
| "Whenever [a player, planeswalker, or battle] is attacked" | once, if one or more creatures are declared attacking it | — | for a creature put onto the battlefield attacking it | 508.3b |
| "Whenever [a player] attacks with [a creature]" | when a creature that player controls is declared as an attacker | — | for a creature put onto the battlefield attacking (508.4) | 508.3c |
| "Whenever [a player] attacks" | once, if one or more creatures that player controls are declared as attackers | — | for a creature put onto the battlefield attacking (508.4) | 508.3d |
| "Whenever [a player] attacks [another player]" | once, if one or more of the first player's creatures are declared attacking the second player | — | for a creature put onto the battlefield attacking, or one attacking a planeswalker or battle | 508.3e |
| "Whenever [a creature] attacks and isn't blocked" | in the declare blockers step, if no creatures are declared as blockers for it | for a creature never declared as an attacker (it entered attacking) | if it was blocked and then all its blockers were removed from combat | 508.3f, 509.3g |
| "Whenever [a creature] blocks" | once per combat for that creature, however many creatures it blocks | when an effect makes it a blocker while it isn't blocking | for a creature put onto the battlefield blocking | 509.3a |
| "Whenever [a creature] blocks a creature" | per attacking creature it blocks | when an effect makes it block an attacker it wasn't already blocking | for a creature put onto the battlefield blocking | 509.3b |
| "Whenever [a creature] becomes blocked" | once per combat for that creature, however many creatures block it | when it is blocked by an effect, or by a creature put onto the battlefield blocking, if it was unblocked then | — | 509.3c |
| "Whenever [a creature] becomes blocked by a creature" | per creature that blocks it | when an effect makes a creature that wasn't blocking it block it, or a creature is put onto the battlefield blocking it | when it becomes blocked by an effect rather than a creature | 509.3d |

508.4's "never 'attacked'" covers every attack template except "attacks
and isn't blocked", which fires for a creature that entered attacking
(509.3g). A quality named in a block template is read when the creature
blocks or becomes blocked, never later (509.3f). A counted block
template ("blocked by two or more creatures") is checked when blockers
are declared, and effects that add or remove blockers can also make it
trigger (509.3e). Keyword exemplars: rampage and afflict trigger on
"becomes blocked" (702.23a, 702.130a), and bushido on "blocks or becomes
blocked" (702.45a). These generally fire once per combat (509.3a,
509.3c). Flanking (702.25a) and the Ring's third ability (701.54c) fire
per blocker.

**Engine inference:** record one declaration fact per (blocker,
attacker) pair, then deduplicate per ability on the template's key: the
blocker for "blocks", the attacker for "becomes blocked", and the pair
for "blocks a creature" and "becomes blocked by a creature". Using one
key for every watcher drops triggers: keyed on the attacker, a second
creature double-blocking that attacker loses its own "blocks" trigger.

**"Alone": event vs state.** A creature *attacks alone* (*blocks alone*)
if it's the only creature declared as an attacker (blocker) during the
declare attackers (blockers) step. It *is attacking alone* (*is blocking
alone*) while it's attacking (blocking) and no other creature is (506.5).
"Attacks a player alone" and "is attacking a player alone" are the
per-defender versions: no other creature is declared attacking *that
player* (506.6). Such a creature can still be accompanied by creatures
attacking planeswalkers, battles or (in multiplayer) other players. Both
readings are fixed at declaration (506.5, 506.6), so creatures put onto
the battlefield attacking never count (508.4). Exalted keys on the
declaration (702.83a, 702.83b) and has no intervening "if" (603.4), so
creatures that enter attacking later "won't affect exalted abilities
that have already triggered or resolved", and it doesn't trigger when
several creatures attack and all but one are removed from combat
(Emissary of Soulfire [2024-06-07]; Noble Hierarch [2020-08-07]). Under
shared team turns the team makes one combined attack (805.10b), so
"alone" counts the whole team's declared attackers, and only the lone
attacker's controller gets exalted triggers. **Engine inference:**
compiling "attacks alone" as an intervening "if" over the current
attacker count is wrong: 603.4 rechecks on resolution, so tokens
entering attacking (Hero of Bladehold) would make a correctly triggered
exalted do nothing. **"Had to attack"** also reads the declaration: true
iff one or more effects required that creature to attack when attackers
were declared that combat, not merely that it had no other legal attack
(506.7).

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
regeneration never touch (701.21a). Dies is a destination view;
destroyed and sacrificed are verb views whose default destination is the
graveyard.

**Tap causes** — the cleanest demonstration that one event type needs a
cause field:

| Cause of becoming tapped | CR hook |
|---|---|
| Cost payment — {T} in an activation cost | 107.5 |
| Attack declaration — explicitly **not** a cost; "attacking simply causes creatures to become tapped" | 508.1f |
| Crewing — "crews a Vehicle" = tapped to pay a crew cost; "can't crew" restricts exactly that cause | 702.122b, 702.122d |
| Convoke payment — tapped while paying a spell's total cost | 702.51a |
| Tapped for mana — tap as cost payment of a mana ability (106.12, 107.5); the separate mana-production event at resolution is what 106.12a/b match | 106.12, 107.5, 106.12a, 106.12b |
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

- **Discard**: cost vs effect vs the cleanup turn-based discard (703.4n)
  vs the Circling Vultures special action (116.2e). Most discard
  triggers are cause-agnostic, but a cost discard that is replaced into
  a hidden zone unrevealed, where the cost names a characteristic, is an
  illegal payment (701.9c).
- **Damage**: combat (120.2a) vs spell/ability effect (120.2b) — "combat
  damage" triggers filter on this tag.
- **Life loss**: from damage (119.2), from paying (119.4), from an effect
  (119.3); gain is always source-attributed (119.9).
- **Event vs state**: "attacks" fires only on the declaration cause —
  put-onto-the-battlefield-attacking creatures never "attacked" (508.3a,
  508.4), except under "attacks and isn't blocked", which fires for them
  too (509.3g); a land put onto the battlefield by an effect was never
  "played" (701.18a); cast vs other arrivals on the stack (601.2i);
  "attacks alone" (declaration) vs "is attacking alone" (state) is the
  combat instance (506.5; §2).

Settled vocabulary — a cause is a *(verb, agency, agent)* triple: the
**verb tag** is the named view performed (destroy, sacrifice, discard,
mill, exile, play, cast, crew, …: the intrinsic keyword actions of
`keyword-classification.md`); the **agency tag** is the machinery that
demanded it, from the list below; and the **agent** is the causing
object plus its controller — nullable, since turn-based and state-based
actions have neither. The agent coordinate is what oracle text reads when
it asks *who did it*: Karmic Justice's "whenever a spell or ability an
opponent controls destroys a noncreature permanent you control"
predicates on agent kind and agent controller; the whole "when a spell or
ability an opponent controls causes you to discard this card" family does
the same over discard events; and "destroyed this way" / "removed this
way" is agent-*identity* equality — match exactly the events whose agent
is this very spell or ability. Every CR distinction above is a predicate
over one or more coordinates. What cause tags do *not* carry is event
ancestry: "dies from combat damage"-style filters join a death event to
an earlier damage event, which is the §5 log/look-back's job, not a
cause tag's.

Agency tags: `cost-payment` | `attack-declaration` | `effect-instruction`
| `turn-based-action` | `state-based-action` | `mana-ability-resolution`
| `special-action` | `resolution` | `failed-resolution`.
`mana-ability-resolution` tags only the mana-production event (see the
tap table above), never the tap. `special-action` covers the twelve
player actions that skip the stack (116.1, 116.2): the land play that
alone makes a land "played" (116.2a, 701.18a), turning a face-down
creature face up (116.2b), the suspend, foretell and plot exiles
(116.2f, 116.2h, 116.2k), Circling Vultures' discard (116.2e), and the
unlock cost (116.2m). `resolution` covers moves the resolution procedure
makes for an object that resolves: an instant or sorcery's final move to
the graveyard (608.2n), a resolving permanent spell entering (608.3a),
and one that can't enter (608.3e). `failed-resolution` covers removing
an object that doesn't resolve: a triggered ability whose intervening
"if" is false (608.2a), or a spell or ability whose targets are all
illegal (608.2b, 608.3b). Keep the two distinct: resolution-only
replacements and triggers (702.27a, 702.88a, 702.55a) match the
`resolution` move only, never a `failed-resolution` move or a counter
(verb `counter`, 701.6a, usually agency `effect-instruction`); the
window table is in `casting.md` §6. The list is not exhaustive: other
rules procedures move objects too, namely casting's move to the stack
(601.2a), game-start mulligans and opening-hand moves (103.5, 103.6a),
and objects leaving the game with their owner, which "is not a
state-based action" (800.4a). The CR fixes the behavior but not the tag,
so this is representation-only; those cases are registered as
UD-25 in `underdetermined.md`.

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
- **Simultaneous by default, sequential by exception.** An instruction
  acting on several players or objects is processed simultaneously
  unless it can't be, and then per player or object: APNAP order first,
  then the resolving spell's controller orders a player's own objects
  relative to each other and to that player (608.2f; multi-step
  multi-player actions: 608.2e). "Mill three" moves all three cards at
  once (608.2f; 701.17a defines mill but not its timing). Sidisi, Brood
  Tyrant ruling [2014-09-20]: such an instruction "moves all the cards at
  the same time", so a "one or more" watcher triggers once. The CR's
  explicit one-at-a-time rules are:
  - draw: individual draws, the active player's before each other
    player's in turn order (121.2, 121.2c; number-changing replacements
    under "Contained events" below); draws produced by a replacement or
    prevention effect, after any unreplaced part of the event (121.7);
  - setting schemes in motion (701.32c);
  - manifesting or cloaking several cards from a library (701.40e,
    701.58e);
  - facing a villainous choice, per player in APNAP order, "an exception
    to rule 608.2e" (701.55d; repeated faces of one choice, 701.55c);
  - several permanents exploring or conniving, one at a time (701.44d,
    701.50c);
  - extra turns, added one at a time and in APNAP order across players
    (500.7).

  (Set from CR searches for "one at a time", "individual" and "process
  is repeated"; the CR declares no closed list.) Drawing (121) and
  dealing damage (120) are game concepts, not 701 keyword actions, and
  moving library cards to hand without the word "draw" is not a draw
  (121.5).
- **Once per event.** A replacement effect gets one opportunity to affect
  an event and the modified events that replace it (614.5); across the
  replacements modifying how permanents enter the battlefield, the same
  object can't be chosen to change zones twice (614.13b).
- **Contained events.** One replacement may apply to an event and another
  to an event *contained within* it — the outer one must be chosen first
  (616.1g: token creation contains entering the battlefield, so Doubling
  Season applies before per-token as-enters choices). Draw N is N
  individual draw events, but effects modifying "the number of cards
  drawn" apply before any individual draw (121.2, 121.2a).
- **Trigger batching.** Triggered abilities waiting since the last
  priority grant go on the stack in two passes (603.3b). First, in APNAP
  order, each player puts their triggers whose condition is not another
  ability triggering, in any order. Second, in APNAP order, each player
  puts the remaining triggers (those that trigger on an ability
  triggering, e.g. Historian's Boon). SBAs are then rechecked and the
  process repeats (603.3b, 704.3). Events commit first, triggers batch
  after.
- **All-or-nothing composites.** Against the default that an effect does
  as much as it can (609.3), three actions happen whole or not at all:
  moving a counter (122.5) and the keyword actions fight and exchange
  (701.14, 701.12).
  - *Move a counter*: remove it from one object and put it on a second.
    If either half is impossible (the same object twice, no such counter
    on the first, a second object that can't have counters, or either
    object out of its zone), no counter is removed or put (122.5).
  - *Fight*: each creature deals damage equal to its power to the other
    (701.14a). If either creature has left the battlefield or stopped
    being a creature, or either is an illegal target of the resolving
    spell or ability, neither fights or deals damage (701.14b). The
    battlefield test reads current state, so a departed untargeted
    fighter doesn't fight on the last known information 608.2h would
    otherwise supply: "If Affectionate Indrik is no longer on the
    battlefield, the target creature won't deal or be dealt damage"
    (Affectionate Indrik [2018-10-05]). A creature that fights itself
    deals itself twice its power (701.14c); fight damage isn't combat
    damage (701.14d).
  - *Exchange*: if the entire exchange can't be completed, no part of it
    occurs (701.12a); exchanging control of two permanents with the same
    controller does nothing (701.12b).

  **Engine inference:** evaluate the whole guard before emitting any
  constituent event, then commit the constituents as one batch.

## 5. History and look-back

Events are the log. Effects that say "this turn" look back in time at
previous game states and actions, not at the current snapshot (608.2i) —
an engine therefore keeps an event log keyed by turn (`state.md` §2
enumerates the kinds; `engine.md` renders it as `TurnHistory`). When an
effect needs information about an object no longer in its expected public
zone, it uses **last known information** (608.2h, 113.7a) — LKI is a
snapshot read from the log. LKI as a log snapshot is an engine
mechanism; its extent is open (UD-9). Timing matters: a permanent that
leaves via a state-based action takes its LKI from *before any of that
batch's SBAs were performed*, not mid-batch (704.8).

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
  is defined at 603.6c, which also rules one shape out of it: an ability
  that triggers when a card is put into a zone "from anywhere" is never a
  leaves-the-battlefield ability, even when the card came from the
  battlefield (603.6c). So 603.10a's leaves-the-battlefield look-back
  doesn't apply to it. It uses the normal after-the-event check unless
  another 603.10 class covers it, such as a visible object put into a
  hand or library (603.10a). "Loses the game" triggers match a player
  losing *or leaving* the game for any reason, except leaving as the
  result of a draw (603.9).

  Within one simultaneous event, the looked-back world is the pre-event
  board. Every object leaving in that event still has its abilities for
  every *other* member's departure. An artifact destroyed along with two
  creatures triggers twice on "whenever a creature dies" (603.10a's
  example), and a dying Blood Artist triggers for each creature that
  dies with it (Blood Artist [2016-06-08]). **Engine inference:** a scan
  that checks each fact against the post-event board plus only that
  fact's own leaving object misses these triggers. Take the whole
  batch's leavers as watchers for their look-back (603.10a) abilities
  only. Their other abilities, including "from anywhere" ones (603.6c),
  keep the normal after-event check.
- **Visibility gate**: if the object with the trigger is at no time
  visible to all players, it doesn't trigger (603.2f).
- **"Whenever X or Y"** is a pattern union: one ability whose text
  defines a disjunctive event pattern (700.1); it still triggers once
  per matching event occurrence (603.2c).
- **Trigger multipliers** (Panharmonicon, Naban, Katara): an effect may
  state that a triggered ability triggers additional times (603.2d). It
  matches a triggered ability by its source ("a triggered ability of
  [object]"), optionally filtered by the event that caused the trigger
  ("If [event] causes a triggered ability of [object] to trigger").
  Determine how many times the ability triggers, then trigger it that
  many times. The instances are not copies; modes and targets are chosen
  for each as it is put on the stack (Panharmonicon [2021-03-19]). A
  multiplier doesn't apply to itself or to other multipliers, so they
  add: two Nabans or Panharmonicons give three triggers, not four
  (603.2d). A multiplier on "a triggered ability of [object]" covers only
  abilities that object has, not delayed (603.7) or reflexive (603.12)
  abilities they create (603.2d). It never reaches replacement effects
  such as "enters with" or "as [this] enters" (614.1c; Panharmonicon
  [2021-03-19]).
- State triggers (603.8), delayed (603.7) and reflexive (603.12)
  triggers: `abilities.md`.
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
    ordering: int         # engine choice: total commit order (UD-12);
                          # members of a simultaneous batch (704.3, 510.2)
                          # get an order the CR never assigns, and whether
                          # that order is observable is open (UD-12)
```

The **rewriter acts pre-commit**: while an event is still prospective,
run the replacement fixpoint — a replaced event *never happens* (614.6),
so it triggers nothing (603.2g); the modified event occurs instead and
may itself trigger abilities (614.6); and each replacement is marked
used per event (614.5). **Triggers act post-commit**: committed events are matched
against (event, state) predicates (603.2), batch onto the stack in two
passes at the next priority grant (603.3b), and re-check intervening-if
conditions on resolution (603.4). Committed events append to the
turn-keyed log with the LKI snapshots look-back consumers will need
(608.2i, 704.8).
