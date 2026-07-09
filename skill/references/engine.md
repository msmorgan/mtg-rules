# Engine Sketch — Pseudo-code Model and the Damage Pipeline

*Synthesized from the Comprehensive Rules effective 2026-06-19
(`data/rules/cr.json`). Orientation only — verify load-bearing specifics
with `scripts/rule` before citing. Run `scripts/cite check` after CR
refreshes.*

Read alongside `generalizations.md` — its 12 engine modeling directives prescribe which operations to model as parameterized records.

A pseudo-code rendering of the taxonomy `state.md` argues in prose, plus the
damage pipeline (CR 120) it touches only piecemeal. `state.md` is the
authority; the classes below cross-reference its sections (`see state.md §N`)
rather than re-deriving them. Characteristics are **derived** (recompute by
walking layers 1→7, `effects.md §4/§9`) — stored state is everything here.

## 1. Game-state model (pseudo-code)

```python
class Game:                                # see state.md §1, §8
    players: list[Player]                  # turn order fixed at game start (103.1)
    active_player: Player                  # whose turn it is (102.1)
    phase, step: Enum                      # five phases, ordered steps (500.1)
    priority_holder: Player|None           # may act now (117.1)
    extra_turn_queue: Stack[Turn]          # added one at a time, taken LIFO,
                                           # most-recent first; APNAP if many (500.7)
    pending_skips: Map[occurrence, int]    # "skip" = replacement (614.10);
                                           # COUNT them — two skips skip two (614.10a)
    zones: battlefield, exile, command,    # shared zones (400.1); per-player
           stack                           #   library/hand/graveyard live on Player
    stack: Stack[StackObject]              # LIFO, top resolves first (405.1, 405.2)
    continuous_effects: list[FloatingEffect]   # timestamp-ordered (613.7); see effects.md
    pending_triggers: list[StackObject]    # triggered, waiting for next priority (603.3)
    delayed_triggers: list[DelayedTrigger] # persist until their event (603.7)
    replacement_usage: per-event set       # each replacement applies once/event (614.5)
    day_night: None|DAY|NIGHT              # game designation; checked in untap (731.1, 502.2)
    monarch: Player|None                   # single-holder designation (725.1)
    initiative: Player|None                # single-holder, inherent triggers (726.1)
    planar_controller: Player|None         # controls face-up plane/phenomenon;
                                           # normally the active player (901.6)
    turn_history: TurnHistory              # event log keyed by turn (608.2i)
    dungeon_progress: Map[Player, DungeonCard|None]  # venture marker position (309.4);
                                           # None = no active dungeon
    ring_temptation_count: Map[Player, int]  # times the Ring has tempted each player;
                                           # drives which Ring abilities are active (701.54c)
    attraction_state: Map[Player, AttractionDeck]  # supplementary command-zone deck;
                                           # unlocked lights track open Attractions (717.2)
    # see designations.md for the full global-flag set (monarch, initiative, ring-bearer, etc.)
```

```python
class TurnHistory:                         # see state.md §2 "Per-turn tracked history"
    # "this turn" wording looks back in time, not at the snapshot (608.2i) —
    # an event log is REQUIRED. Examples (not exhaustive):
    spells_cast: list[(player, info)]      # storm (702.40a); day/night flip (502.2)
    lands_played: Map[Player, int]         # played vs allowed (305.2a, 305.2b)
    damage_dealt: Map[(source, recipient), int]  # bloodthirst (702.54a); commander dmg (903.10a)
    attacked_with: ...                     # look-back trigger example (608.2i)
    descended: int                         # permanent cards to graveyard this turn (700.11)
    mana_spent_on_spells: Map[Player, int] # "expend" (700.14)
    first_card_drawn: Card|None            # miracle (702.94a)
```

```python
class Player:                              # see state.md §2
    life: int                              # starts 20, variants differ (119.1);
                                           # gain/lose adjusts it (119.3); set = gain/lose diff (119.5)
    counters: Map[kind, int]               # poison (122.1f), rad (122.1i),
                                           # energy {E} (107.14), ticket {TK} (107.17a)
    library, hand, graveyard: Zone         # per-player zones (400.1); graveyard ordered (400.5)
    max_hand_size: int                     # default 7; excess discarded in cleanup (402.2, 514.1)
    speed: None|1|2|3|4                    # none until set; max 4; none counts as 0 (702.179b, 702.179e, 702.179f)
    designations: set                      # city's blessing (702.131c); monarch/initiative held on Game
    commander_tax: Map[cmdr, int]          # +{2} per prior cast from command zone (903.8)
    commander_damage: Map[cmdr, int]       # 21+ from one commander loses (903.10a)
```

```python
class Zone:                                # see state.md §3
    kind: Enum                             # closed list (400.1): library, hand,
                                           #   battlefield, graveyard, stack, exile,
                                           #   command, ante
    ordered: bool                          # library/graveyard/stack ordered; others not (400.5)
    visibility: PUBLIC|HIDDEN              # library/hand hidden, rest public (400.2)
    objects: list[Object]                  # wrong-zone sends route to owner's (400.3)
```

```python
class Permanent(Object):                   # battlefield only (110.1); see state.md §6
    base: card|token_def|copy_snapshot     # layer-input for the derived getter (613.1)
    controller: Player                     # only stack/battlefield objects have one (109.4);
                                           # defaults to who it entered under (110.2)
    owner: Player                          # 108.3; token owner = creator (111.2)
    status: {tapped, flipped, face_down, phased_out}   # closed; not a characteristic (110.5)
    counters: Map[kind, int]               # +1/+1 & -1/-1 annihilate (122.3); loyalty (122.1e);
                                           #   defense (122.1g); shield/stun/finality/keyword (122.1)
    marked_damage: int                     # lethal if >= toughness (SBA); cleared in cleanup (120.6, 514.2)
    dealt_by_deathtouch_flag: bool         # dealt damage by deathtouch source since last SBA (704.5h)
    attached_to / attachments: ...         # Aura/Equip target; kept clear (400.5)
    timestamp: int                         # on entry (613.7d); renewed on attach/flip/transform
    counter_timestamps: Map[kind, int]     # each counter timestamped (613.7c)
    stickers: list[Sticker]               # markers that modify characteristics; each sticker
                                           # gets a new timestamp when placed or when the object
                                           # gets a new timestamp (123.1, 613.7k)
    controlled_since: turn_marker          # summoning sickness: continuous since last turn began (302.6)
    class_level: int                       # any permanent can have a level; level-1 default;
                                           #   not copiable (716.2b, 716.2d)
    unlocked_doors: set                    # Room: "left/right half unlocked" designations (709.5c)
    merged_components: list[card|copy]     # merged permanent = multiple components (730.2);
                                           # has only the top component's chars (730.2a); on leave,
                                           # each component goes to its own zone (730.3, 730.3c)
    linked_memory: ...                     # what the first linked ability did (607.1);
                                           # also covers secretly noted card names: a
                                           # face-down/conspiracy card with hidden agenda notes
                                           # a name on paper kept with the card (702.106b)
    casting_choices: ...                   # modes/targets/X/costs the spell was cast with (601.2c)
```

```python
class StackObject:                         # spell or ability on the stack (405.1); see state.md §4
    kind: SPELL|ACTIVATED|TRIGGERED
    characteristics|ability_text           # spells carry the card's chars; abilities only text (405.4)
    controller, source                     # ability lives independently of its source (113.7a);
                                           # trigger controlled by source's controller at trigger time (603.3a)
    targets: list[(slot, chosen)]          # target count/choices locked at cast (601.2c)
    modes, X, costs_paid                    # casting decisions
```

```python
class FloatingEffect:                      # from a resolved spell/ability; see effects.md §3
    source, timestamp                      # ordering timestamp (613.7b)
    duration                               # stated or until end of game (611.2)
    locked_set: set[Object]|None           # char/control-modifying resolution effects
                                           #   lock their affected set at start (611.2c)

class DelayedTrigger:                      # see state.md §8
    text, source, controller               # persists until its trigger event (603.7)
```

**Last known information.** When an effect needs info from an object that has
left its expected public zone, use the object's LKI (608.2h, 113.7a); the SBA
snapshot is from *before* the batch that removed it (704.8). Deathtouch /
lifelink / wither / infect on a source that changed zones are read from LKI
(702.2e, 702.15c, 702.80b, 702.90d). (See state.md §7.)

## 2. The damage pipeline (CR 120)

Any object can deal damage (120.2) to a battle, creature, planeswalker, or
player (120.1); damage can't be dealt to anything else (120.1a). Damage is
combat (each attacker/blocker deals its power, 120.2a) or effect-based (120.2b).

**A. Propose the event.** Form `{source, recipient, amount}` per recipient
(combat damage is one simultaneous batch, 510.2). A source dealing 0 deals
nothing — no triggers, nothing to replace (120.8). The "source" can be chosen
even after it left its zone (120.7, 609.7).

**B. Replacement / prevention / redirection fixpoint.** Run the
event-modification fixpoint from `effects.md §8–9`: collect every applicable
replacement (614) and prevention (615) effect; the affected object's
controller/owner or the affected player chooses one per the 616.1a–f order
(self-replacement first), APNAP across players; apply it; mark it used for this
event (614.5, 615.12a); re-collect (some only just became applicable, 616.2)
until none apply (614.6). Ordering details:

- **Excess-redirection effects go first** (120.4a): if an effect says excess
  damage to a permanent is dealt elsewhere, compute excess (over lethal /
  loyalty / defense, counting marked damage and simultaneous sources; deathtouch
  makes anything > 1 excess, 702.2c) and rewrite the event.
- **Then damage is dealt as modified** by replacement/prevention (120.4b); a
  prevention "shield" reduces the amount 1-per-point (615.7), redirection moves
  it to another battle/creature/planeswalker/player (614.9). Abilities that
  trigger on damage being dealt trigger now and wait (120.4b).
- "Can't be prevented" damage still *applies* prevention effects (for their
  riders) but prevents nothing and doesn't drain shields (615.12, 615.12a).

**C. Process results per recipient** (120.4c — "as modified by replacement
effects that interact with the results," e.g. life-loss/counter doublers). Each
recipient resolves to the 120.3 letters (every letter verified against CR 120):

| Recipient + source property | Result | CR |
|---|---|---|
| Player, source without infect | player loses that much life | 120.3a |
| Player, source with infect | controller gives player that many poison counters | 120.3b |
| Planeswalker | remove that many loyalty counters | 120.3c |
| Creature, source with wither and/or infect | controller puts that many -1/-1 counters on it | 120.3d |
| Creature, source with neither | mark that much damage on it | 120.3e |
| Battle | remove that many defense counters | 120.3h |
| (any) source with lifelink | controller gains that much life, in addition; multiple simultaneous lifelink sources produce **separate** life-gain events, so "whenever you gain life" triggers count per source (120.3f, 702.15e) |
| Player, combat damage from a creature with toxic | give poison = total toxic value, in addition | 120.3g |

Life loss/gain then adjusts the life total (119.3); damage to a player
*normally* is loss (119.2), but infect routes to poison instead (702.90b).
Marked damage persists till cleanup and is lethal at >= toughness (120.6).
Wither/infect to a creature are -1/-1 counters, never marked damage
(702.80a, 702.90c). The `dealt_by_deathtouch_flag` is what the deathtouch SBA
later reads (702.2b, 704.5h) — deathtouch is a *flag at deal time*, not a result.

**D. The damage event occurs** (120.4d). Only now do the results (life change,
counters, marked damage) actually happen — the whole of A–C built up a modified
event that fires atomically here. Combat damage is dealt simultaneously as one
event (120.2a via 510.2). See the two worked examples in CR 120.4d (Boon
Reflection / wither+lifelink, and Awe Strike / Worship).

**After.** Damage does not destroy (120.5); destruction is an SBA. So the
priority handshake (below) runs the SBA fixpoint — lethal marked damage (704.5g),
the deathtouch flag (704.5h), 0-loyalty planeswalkers (704.5i), 0-defense
battles (704.5v) — and only then do the damage triggers from step B reach the
stack. Excess-damage trigger conditions read the amount over lethal/loyalty/
defense computed at deal time (120.10).

## 3. The main loop

Between `take_turn` / turn-based actions and resolution, the engine runs the
priority→act/pass→resolve cycle and the SBA+trigger fixpoint at every priority
grant (117.5, 704.3, 603.3b). Do not duplicate it here — **see actions.md §6**
(and the SBA list in actions.md §3, turn-based actions in §2).
