# Effects — Taxonomy, Layers, Replacement

*Synthesized from the Comprehensive Rules effective 2026-08-07
(`data/rules/cr.json`). Orientation only — verify load-bearing specifics
with `scripts/rule` before citing. Run `scripts/cite check` after CR
refreshes.*

How an engine models what spells, abilities, and the rules *do*. The layer
system (§4) is the heart of this doc: it is the deterministic algorithm for
computing an object's current characteristics. For the abilities that
generate these effects, see `abilities.md`; for the game state they read and
write, see `state.md`.

## 1. What an effect is (609)

An effect is something that happens in the game as a result of a spell or
ability (609.1). Resolving a spell, activated ability, or triggered ability
may create one or more **one-shot** or **continuous** effects; static
abilities create only continuous effects (609.1). **Text itself is never an
effect** (609.1) — only the resolution/static application produces one.

- Effects apply only to permanents unless the text says otherwise or they
  clearly can apply only to objects elsewhere (609.2) — e.g. "lands become
  creatures" ignores library/graveyard cards; "spells cost more" hits the
  stack (609.2 example).
- An effect that attempts the impossible does only as much as possible
  (609.3); a tie has no default — the source must specify (609.5).
- "As though" effects treat the game as if a condition were true *only for
  that effect*, normally otherwise (609.4); spending mana "as though it were
  any color/type" changes only how a cost is paid, not the cost or what was
  actually spent (609.4b).
- Some continuous effects are **replacement** or **prevention** effects — a
  cross-cutting kind, see §6–§8 (609.6).
- Effects on damage *from a source* recheck the source's properties when
  damage would be dealt; if they no longer match, nothing is
  prevented/replaced and the shield isn't used up (609.7, 609.7b).

## 2. One-shot effects (610)

A one-shot effect does something **just once and has no duration** (610.1) —
dealing damage, destroying a permanent, creating a token, moving an object
between zones (610.1). Wrinkles an engine must model:

- May create a **delayed triggered ability** that acts later, not at
  resolution (610.2, → 603.7).
- "Change zones until [event]" / "phase out until [event]" is really *two*
  one-shot effects: the move now, and a **second one-shot effect created
  immediately after the event** that returns/phases-in the object
  (610.3, 610.4). If the event already happened (after the spell/ability was
  put on the stack / triggered but before the move), the object doesn't move
  (610.3a, 610.3b). Returned objects come back under owner's control unless
  stated (610.3c); simultaneous events make simultaneous returns (610.3d).
- A statics-granted "cast spells with [ability]" begins to apply when the
  player puts the spell on the stack (610.5, → 601.2a).

## 3. Continuous effects (611)

A continuous effect modifies characteristics, modifies control, or affects
players/the rules, for a **fixed or indefinite period** (611.1). Two
sources, with different locking behavior:

**From a resolved spell/ability (611.2):**

- Lasts as long as the spell/ability states (e.g. "until end of turn"); with
  no stated duration it lasts **until end of the game** (611.2a).
- "For as long as …" durations: if the duration never starts, or has already
  ended before the effect would first apply (and doesn't restart during
  resolution), the effect does nothing — it never starts-and-stops, and never
  lasts forever (611.2b).
- **Locked-in object set:** an effect that modifies characteristics or
  control fixes its set of affected objects when it begins; the set never
  changes afterward (611.2c). An effect that does *neither* is modifying the
  rules and *can* reach objects that weren't around at the start (611.2c).
  X is fixed once, on resolution (611.2d).
- Characteristic-setting that puts a permanent onto the battlefield and says
  it "is/has [characteristic]" applies *simultaneously* with entry;
  "becomes/gains" applies *after* it's on the battlefield (611.2e).

**From a static ability (611.3):**

- **Not locked in** — applies at any moment to whatever its text currently
  indicates (611.3a), at all times the source is in the appropriate zone
  (611.3b). A creature that becomes white gains "white creatures get +1/+1"
  and loses it if it stops being white (611.3b example).
- Characteristic modifications apply **simultaneously with the permanent
  entering**, before checking ETB triggers — a "white creatures get +1/+1"
  static makes a 1/1 token enter *as* a 2/2 (611.3c).

## 4. The layer system (613)

An object's characteristics are computed from scratch, continually and
automatically, with instantaneous results (613.1, 613.5). **Start from the
actual object** (printed card values; for tokens/copies, the values the
creating effect defined), then apply all applicable continuous effects in
this fixed layer order (613.1):

| Layer | Scope (613.1a–g) |
|-------|------------------|
| **1** | Copiable values (copy effects, merges, face-down) |
| **2** | Control-changing effects |
| **3** | Text-changing effects (see 612) |
| **4** | Type-changing (card type, subtype, supertype) |
| **5** | Color-changing effects |
| **6** | Ability add/remove, keyword counters, "can't have an ability" |
| **7** | Power/toughness-changing effects |

Layers 1 and 7 have ordered **sublayers**; layers 2–6 do not (613.2, 613.4):

| Sublayer | Scope |
|----------|-------|
| **1a** | Copy effects + merges; "as ~ enters/turned face up" that *set* P/T (613.2a) |
| **1b** | Face-down spells/permanents get characteristics per 708.2 (613.2b) |
| **7a** | P/T from **characteristic-defining abilities** (613.4a, → 604.3) |
| **7b** | Effects that **set** P/T to a specific value; "base P/T" effects (613.4b) |
| **7c** | Effects/counters that **modify** P/T (don't set) (613.4c) |
| **7d** | Effects that **switch** P/T (613.4d) |

After layer 1 finishes, the object's characteristics *are* its **copiable
values** (613.2c, → 707.2).

**Within a layer/sublayer**, ordering is (in priority):

1. **CDAs first** in layers 2–6 (then everything else); layer 7 isolates
   CDAs in sublayer 7a instead (613.3, 613.4a). This is the "CDA placement"
   rule — there is no separate CDA layer; CDAs simply sort first. Among
   multiple CDAs within the same layer, the normal timestamp and dependency
   rules (613.7, 613.8) determine their relative order (613.3).
2. **Timestamp order** — earlier timestamp applies first (613.7). What gets a
   timestamp and when: an effect from a resolved spell/ability is stamped at
   creation (613.7b); an effect from a static ability shares the source
   object's timestamp, or the granting effect's, whichever is later (613.7a);
   an object is stamped on **entering a zone** (613.7d); an Aura/Equipment/
   Fortification is **re-stamped each time it attaches** (613.7e); a permanent
   re-stamps on turning face up/down (613.7f) and on transform/convert
   (613.7g); each counter (613.7c) and sticker (613.7k) is stamped when
   placed. Simultaneous timestamps resolve in APNAP order (613.7m); when a
   resolved spell/ability puts an object onto the battlefield and sets its
   characteristics (see 611.2e), the continuous effect from that object's
   **own static ability** receives an earlier relative timestamp than the
   simultaneous resolved-effect (613.7n).
3. **Dependency overrides timestamps** (613.8). Effect A *depends on* B when:
   they apply in the same (sub)layer; applying B would change A's text/
   existence/what-it-applies-to/what-it-does; and they aren't split across
   CDA/non-CDA status (613.8a). A dependent effect waits until just after
   everything it depends on has applied; simultaneous dependents go in
   timestamp order; a **dependency loop** falls back to pure timestamp order
   (613.8b). Order is re-evaluated after each application (613.8c).

**Applied in order, results carry forward:** if one effect spans multiple
(sub)layers, each part applies in its proper place but **to the same locked
set of objects** throughout, even if its source is removed mid-process
(613.6). One effect can override another, and a later result can change
whether/how a still-pending effect applies (613.9; 7/7→7/9→5/8 example in
613.5). Effects on **players** apply (timestamp order) after object
characteristics are determined (613.10); effects on **game rules** apply
last of all, costs per 601.2f then timestamp order (613.11).

## 5. Text-changing effects (612)

Layer-3 anchor. A text-changing effect changes words/symbols on an object —
usually its rules text and type line (612.1). It changes only words used *in
the correct way* (a color word as a color, a creature type as a type), and
never a card **name**, even if the name contains such a word (612.2). It
cannot touch *granted* abilities, since granting/removing abilities doesn't
change text (612.3); but it *can* change a token's defined subtypes/rules
text (612.4) and a token-maker's creature-type-as-name words (612.2a).

## 6. Replacement effects (614)

Continuous effects that watch for an event that *would* happen and
completely or partially replace it with a different event — "shields" around
what they affect (614.1). **They never use the stack** (they are continuous
effects, not abilities that resolve). Recognition markers:

- **"instead"** (614.1a); **"skip"** (614.1b — = "instead of doing X, do
  nothing"; 614.10).
- ETB modifiers: **"~ enters with …"**, **"as ~ enters …"**, **"~ enters
  as …"** (614.1c), and continuous **"~ enters …" / "[objects] enter …"**
  (614.1d).
- **"as ~ is turned face up …"** (614.1e).

Behavior:

- Must exist **before** the event — they can't go back in time (614.4); a
  destroyed-then-regenerated creature must have regen up first (614.4
  example).
- **Apply at most once per event:** a replacement effect gets one opportunity
  per event and any modified events that replace it; it never invokes itself
  repeatedly (614.5) — double-damage twice is ×4, not infinite (614.5
  example). (Engine bookkeeping for this is noted in `state.md` §8.)
- A replaced event **never happens**; the modified event occurs and may
  itself trigger abilities; impossible instructions in it are ignored
  (614.6). If the event would never happen anyway, the replacement does
  nothing (614.7); a 0-damage source deals none, so damage-increasing
  replacements have nothing to replace (614.7a).
- **Regeneration is a destruction-replacement** ("the next time ~ would be
  destroyed this turn, instead remove damage, tap it, remove from combat") —
  "instead" is implicit; damage-dealt triggers still fire (614.8, → 701.19).
- **Self-replacement effects** are *not* continuous: a resolving spell/
  ability replaces part of its **own** effect; they are applied **before**
  other replacement effects (614.15).
- **Token/counter doublers (614.16):** replacement effects keyed on "if an
  effect would create one or more tokens" or "would put one or more counters
  on a permanent" (e.g. Doubling Season) apply to tokens/counters produced
  by a resolving spell or ability **and** to tokens/counters produced by
  another replacement or prevention effect, even if the original event being
  modified was not itself an effect (614.16).
- **Damage redirection (614.9):** redirecting damage from one battle,
  creature, planeswalker, or player to another is itself a **replacement
  effect**; if the new target is no longer on the battlefield (or is no
  longer a battle/creature/planeswalker) when the redirect would occur, the
  effect does nothing (614.9).
- **Draw replacements (614.11):** effects that replace card draws apply even
  when the affected player's library is empty; within a sequence of draws,
  all replacement actions are completed before the sequence resumes
  (614.11a); if the effect would have the player perform an additional action
  on the drawn card and the draw is replaced, that additional action is not
  performed on cards drawn by the replacement (614.11b).
- **ETB replacements:** check the permanent's characteristics *as it would
  exist on the battlefield*, accounting for replacements already applied
  (per 616.1), the permanent's own statics, and existing continuous effects
  (614.12). Required choices are made before it enters (614.12a); an ETB
  modifier may move other objects too (614.13), but not objects entering
  alongside it (614.13a) and not the same object twice (614.13b).
- "Can't"/skip-style effects aren't replacements but follow similar rules
  (614.17); a "can't" event can only be replaced by a self-replacement
  effect (614.17c).

## 7. Prevention effects (615)

Continuous "shields" that watch a **damage** event and completely/partially
prevent the damage (615.1); marker word **"prevent"** (615.1a). Like
replacements they apply as events happen, can't go back in time, and last
until used up or expired (615.1, 615.3, 615.4).

- A "prevent the next N damage" shield prevents 1 per point; each prevented
  point reduces the shield by 1; multiple simultaneous sources let the
  player/controller choose which the shield eats; once at 0, the rest is
  dealt normally — only the amount matters, not the number of sources
  (615.7). "Next time [source] would deal damage" prevents one whole
  instance regardless of size (615.8).
- **"Can't be prevented":** prevention effects still *apply* (so their
  additional effects happen) but prevent no damage, and existing shields
  aren't reduced (615.12); a prevention effect applies to a particular
  unpreventable event just once (615.12a).
- Triggers that fire "when damage is prevented" fire once per prevention
  application that prevents some damage across simultaneous events (615.13).

## 8. Ordering multiple replacement/prevention effects (616)

When two or more replacement and/or prevention effects would modify how an
event affects an object/player, the **affected object's controller (or its
owner if it has no controller), or the affected player, chooses** which to
apply (616.1). Simultaneous cross-player choices go in APNAP order (616.1).
One effect can *become* applicable because another already modified the event
(616.2).

**The 616.1 priority sequence (load-bearing — verified verbatim):** at each
step, if any applicable effect matches the category, one of *that* category
**must** be chosen; otherwise fall through to the next step:

| Step | Category that must be chosen if any apply |
|------|-------------------------------------------|
| **616.1a** | **Self-replacement** effects (614.15) |
| **616.1b** | Effects modifying **under whose control** an object enters |
| **616.1c** | Effects making an object **enter as a copy** of another |
| **616.1d** | Effects making a card **enter with its back face up** (transform/convert) |
| **616.1e** | **Any** remaining applicable effect may be chosen |
| **616.1f** | Repeat the whole process (only now-applicable effects) until none remain |

Plus: an effect applying to an event *contained within* another can't be
chosen until the outer one has (616.1g) — e.g. Doubling Season (token
creation) applies before the entering tokens' own ETB choices (616.1g
example).

## 9. Engine note

Two distinct mechanisms; do not conflate them.

**Characteristics (layers).** To read any characteristic, **recompute from
scratch**: take the object's base values, then walk layers 1→7 (sublayers
1a→1b, 7a→7d), and within each (sub)layer apply CDAs first, then sort the
rest by timestamp, then let the dependency graph reorder — results of each
layer carry into the next (613.1, 613.3, 613.7, 613.8). No mutation of stored
characteristics; the layer pass *is* the getter. After layer 1 you also have
the object's copiable values (613.2c) — cache these for copy/clone effects.

**Events (replacement/prevention pipeline).** Model each game event as a
proposed event, then run a **fixpoint**: collect every applicable
replacement/prevention effect; let the affected controller/owner/player pick
per the 616.1a–f order (self-replacement first); apply the chosen one, mark
that effect as **used for this event** so it can't fire again (614.5,
615.12a); re-collect applicable effects (some only became applicable now,
616.2) and repeat until none apply; then perform the final modified event
(614.6). Inner events created mid-replacement are their own sub-pipelines but
gated by 616.1g.

## 10. Worked stacks

Two canonical layer puzzles, derived by the §4 algorithm and confirmed
against WotC's own rulings. Quotes verbatim with `[date]` attribution.

### Humility + Opalescence (timestamp order decides P/T)

Oracle: **Humility** "All creatures lose all abilities and have base power
and toughness 1/1." **Opalescence** "Each other non-Aura enchantment is a
creature in addition to its other types and has base power and base toughness
each equal to its mana value." Both are statics; both are {2}{W}{W} (mana
value 4). They touch three layers: **L4** type (Opalescence only), **L6**
ability removal (Humility only), **L7b** base-P/T *set* (both — "base P/T"
sets land in 7b per 613.4b). 613.6 is the crux: once an effect starts
applying it keeps applying to its locked object set **in every later layer
even after L6 strips the source's ability**. So Humility's 7b set survives
Humility losing its own ability, and likewise Opalescence's.

Trace both timestamp orders (earlier timestamp applies first within 7b,
613.7):

| (sub)layer | Opalescence earlier | Humility earlier |
|---|---|---|
| **L4** type | Humility becomes a creature-enchantment (Opal.) | same |
| **L6** abilities | Humility (and other enchantments) lose all abilities (Hum.) | same |
| **L7b** set | Opal. → 4/4, then Hum. → **1/1** | Hum. → 1/1, then Opal. → **4/4** |
| **final** | creatures **1/1**, no abilities | enchantment-creatures **4/4**, no abilities |

Ruling `[2009-10-01]`: "The type-changing effect applies at layer 4, but the
rest happens in the applicable layers. The rest of it will apply even if the
permanent loses its ability before it's finished applying… [Opalescence
earlier] Layer 7b: Humility becomes 4/4 and Worship becomes 4/4.
(Opalescence). Humility becomes 1/1 and Worship becomes 1/1 (Humility). But
if Humility entered before Opalescence… Layer 7b: Humility becomes 1/1 and
Worship becomes 1/1 (Humility). Humility becomes 4/4 and Worship becomes 4/4
(Opalescence)." Final state = last 7b set to apply = **1/1 vs 4/4**. MATCH.

### Blood Moon + Urborg (dependency beats timestamp)

Oracle: **Blood Moon** "Nonbasic lands are Mountains." **Urborg, Tomb of
Yawgmoth** "Each land is a Swamp in addition to its other land types." Both
are type-changing statics in **L4**, neither a CDA — so 613.8a (a) same
(sub)layer and (c) CDA-parity are both met; the dependency turns on (b).
Blood Moon *sets* a nonbasic land's subtype to the basic type Mountain, which
by **305.7** strips all abilities generated from that land's rules text **in
L4 as part of the set** (not waiting for L6). Urborg is itself a nonbasic
land, so applying Blood Moon to it removes Urborg's "Each land is a Swamp"
ability — changing the **existence** of Urborg's effect. That satisfies
613.8a(b): **Urborg depends on Blood Moon.** The reverse fails: Urborg merely
*adds* Swamp to lands' types; it changes neither which lands are nonbasic nor
Blood Moon's text/what-it-does — so **Blood Moon does not depend on Urborg.**

Dependency is one-directional, so timestamps are irrelevant (613.8): the
independent effect (Blood Moon) applies first; reevaluating afterward
(613.8c), Urborg's effect no longer exists and contributes nothing. **Final
state: every nonbasic land is a Mountain with "{T}: Add {R}" and no Swamp
type; names/supertypes unchanged (Blood Moon ruling `[2020-08-07]`).**

Ruling `[2021-03-19]`: "If an effect such as that of Magus of the Moon causes
Urborg to lose its abilities by setting it to a basic land type not in
addition to its other types, it won't turn lands into Swamps, no matter in
what order those effects started to apply." (Magus of the Moon = Blood Moon's
effect on a creature.) MATCH.
