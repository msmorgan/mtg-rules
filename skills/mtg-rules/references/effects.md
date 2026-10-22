# Effects — Taxonomy, Layers, Replacement

*Synthesized from the Comprehensive Rules effective 2026-09-25
(`data/rules/cr.json`).*

How an engine models what spells, abilities, and the rules *do*. The layer
system (§4) is the heart of this doc: it is the deterministic algorithm for
computing an object's current characteristics. For the abilities that
generate these effects, see `abilities.md`; for the game state they read and
write, see `state.md`.

## 1. What an effect is (609)

An effect is something that happens in the game as a result of a spell or
ability (609.1). Resolving a spell, activated ability, or triggered ability
may create one or more **one-shot** or **continuous** effects; static
abilities create continuous effects (609.1), with one exception: statics that
make spells gain an ability as they're cast create one-shot effects (610.5,
§2). **Text itself is never an effect** (609.1) — only the resolution/static
application produces one.

- Effects apply only to permanents unless the text says otherwise or they
  clearly can apply only to objects elsewhere (609.2) — e.g. "lands become
  creatures" ignores library/graveyard cards; "spells cost more" hits the
  stack (609.2 example).
- An effect that attempts the impossible does only as much as possible
  (609.3), and any impossible part of an instruction is ignored (101.3). A
  tie has no default; the source must specify (609.5). Three operations are
  **all-or-nothing** instead, so partial completion is wrong for them:
  - **Exchange.** If the entire exchange can't be completed, no part of it
    occurs (701.12a). Exchanging control of two permanents that one player
    controls does nothing (701.12b). An exchange of life totals or other
    values can't raise the life total of a player who can't gain life or
    lower that of a player who can't lose life, and in that case the exchange
    won't happen (701.12c, 701.12g, 119.7, 119.8). Cards in different zones
    can be exchanged only if one player owns them all, but an empty zone
    doesn't stop the exchange (701.12d, 701.12f).
  - **Moving a counter.** If either the removal or the placement is
    impossible, no counter is removed or put anywhere (122.5).
  - **Fight.** If either creature has left the battlefield, is no longer a
    creature, or is an illegal target, neither fights or deals damage
    (701.14b).

  So two simultaneous "gain control" effects don't model an exchange: each
  would still do as much as possible (609.3), where the exchange does
  nothing. Switcheroo ruling `[2018-07-13]`: "If one of the target creatures
  is an illegal target when Switcheroo resolves, the exchange won't happen."
- "As though" effects treat the game as if a condition were true *only for
  that effect*, normally otherwise (609.4); spending mana "as though it were
  any color/type" changes only how a cost is paid, not the cost or what was
  actually spent (609.4b).
- Some continuous effects are **replacement** or **prevention** effects — a
  cross-cutting kind, see §6–§8 (609.6).
- Resolved-effect shields on damage from a source recheck the source's
  properties when damage would be dealt; if they no longer match, nothing is
  prevented/replaced and the shield isn't used up (609.7b). Static ones apply
  to permanents with the property and to off-battlefield sources with it
  (609.7c). A chosen source is fixed when the effect is created and may be
  any object in 609.7a's list (609.7a).

## 2. One-shot effects (610)

A one-shot effect does something **just once and has no duration** (610.1) —
dealing damage, destroying a permanent, creating a token, moving an object
between zones (610.1). Wrinkles an engine must model:

- May create a **delayed triggered ability** that acts later, not at
  resolution (610.2, → 603.7).
- "Change zones until [event]" / "phase out until [event]" is really *two*
  one-shot effects: the move now, and a **second one-shot effect created
  immediately after the event** that returns/phases-in the object
  (610.3, 610.4). For a zone change, if the event already happened (after
  the spell/ability was put on the stack / triggered but before the move),
  the object doesn't move (610.3a, 610.3b). Returned objects come back under
  owner's control unless stated (610.3c); simultaneous events make
  simultaneous returns (610.3d).
- **Phase-out "until" differs from the zone-change case.** A permanent phased
  out "until" an event skips the untap-step phase-in (502.1); if another
  effect phases it in first, the second one-shot effect never happens, even
  if it has phased out again (610.4a). If the event already happened, it
  doesn't phase out (610.4b, 610.4c). Simultaneous second effects happen
  simultaneously (610.4d).
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
  If a single effect has parts of both kinds, the set of objects each part
  applies to is determined independently (611.2c). X is fixed once, on
  resolution (611.2d).
- **A P/T effect on a noncreature is still created (208.3a).** An effect that
  sets or modifies the power or toughness of a noncreature permanent is
  created anyway. It does nothing until that permanent becomes a creature,
  and then it applies (208.3a). Veteran Motorist's +1/+1 to a Vehicle it
  crewed "is created and will apply to the Vehicle once it becomes a
  creature" (208.3a example). This doesn't widen a locked set: "All white
  creatures get +1/+1 until end of turn" still reaches only permanents that
  were white creatures at resolution (611.2c example). In the other
  direction, counters, stickers, effects, and damage stay with an object
  whose card type changes, even when they're meaningless to the new type
  (205.1a). For whether a noncreature has P/T at all, see `queries.md` §4.
- Characteristic-setting that puts a permanent onto the battlefield and says
  it "is/has [characteristic]" applies *simultaneously* with entry;
  "becomes/gains" applies *after* it's on the battlefield (611.2e).
- **Next-spell modifiers** don't begin immediately: an effect that modifies
  the next spell a player casts (or the next that meets a condition) begins to
  apply when that player next puts an appropriate spell on the stack (611.2f,
  → `casting.md` §1).

**From a static ability (611.3):**

- **Not locked in** — applies at any moment to whatever its text currently
  indicates (611.3a), at all times the source is in the appropriate zone
  (611.3b). A creature that becomes white gains "white creatures get +1/+1"
  and loses it if it stops being white (611.3b example).
- Characteristic modifications apply **simultaneously with the permanent
  entering**, before checking ETB triggers — a "white creatures get +1/+1"
  static makes a 1/1 token enter *as* a 2/2 (611.3c).
- **Exception to the two bullets above (611.3d):** a static may allow a player
  to play a land or cast a permanent spell, or grant a permanent spell or card
  an ability that allows it to be cast. If it also grants that object an
  ability that functions only on the battlefield, that ability lasts as long
  as the granting effect states, or until the end of the game if no duration
  is stated (611.3d, exception to 611.3a-b).

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
| **4** | Type-changing (card type, subtype, supertype); set-vs-retain wording: `grammar.md` §4a |
| **5** | Color-changing effects |
| **6** | Ability add/remove, keyword counters, "can't have an ability" |
| **7** | Power/toughness-changing effects |

Layers 1 and 7 have ordered **sublayers**; layers 2–6 do not (613.2, 613.4):

| Sublayer | Scope |
|----------|-------|
| **1a** | Copy effects + merges; "as ~ enters/turned face up" that *set* P/T (613.2a) |
| **1b** | Face-down spells/permanents get characteristics per 708.2 (613.2b) |
| **7a** | P/T from **characteristic-defining abilities** (613.4a, → 604.3) |
| **7b** | Effects that **set** P/T to a specific value; "base P/T" effects (613.4b); **exchanging** a power or toughness with another value (701.12g) |
| **7c** | Effects/counters that **modify** P/T without setting it (613.4c), including **doubling** and **tripling** (701.10a, 701.11a) |
| **7d** | Effects that **switch** a creature's own P/T (613.4d). This is not an exchange (701.12g) |

Doubling power gives +X/+0, where X is the creature's power as the doubling
spell or ability resolves (701.10b); tripling uses twice that power
(701.11b). A negative value is pushed further negative: a creature with -2
power that is doubled gets -2/-0 (701.10c, 701.11c). This is an exception to
clamping negative results to zero (107.1b). The bonus is a fixed modifier, so
later changes don't rescale it. A 2/2 with a +1/+1 counter that is doubled
gets +3/+0 (6/3), and it is 5/2 if the counter is later removed (701.10b,
613.4c).

After layer 1 finishes, the object's characteristics *are* its **copiable
values** (613.2c, → 707.2).

**Copy exceptions** (707.9). An ability gained or a characteristic modified as
part of the copying process becomes part of the copy's copiable values, so
later copies inherit it (707.9a, 707.9b). Grist's Insect tokens are Insects
"instead of their other creature types ... These are copiable values of the
tokens that other effects may copy" (Grist, Voracious Larva `[2024-06-07]`).
An exception that doesn't copy a characteristic, retains the original values,
or provides a specific set of values for it also leaves uncopied the source's
characteristic-defining ability for that characteristic, and for color its
color indicator too (707.9d). CDAs define only colors, subtypes, power and
toughness (604.3a), so the drop reaches devoid (702.114a), changeling
(702.73a) and P/T CDAs: Quicksilver Gargantuan ("except it's 7/7") copying
Tarmogoyf is 7/7 (707.9d). Carve-out: an exception stating a card type,
supertype or subtype "in addition to its other types" keeps type-defining
CDAs, so Glasspool Mimic copying a changeling keeps changeling (707.9d).
**CR-underdetermined** (UD-24 in
`underdetermined.md`): the carve-out names only types. 707.9d doesn't say
whether "in addition to its other colors" drops a copied devoid or color
indicator, or whether a type-additive exception also exempts the same copy
effect's P/T and color exceptions.

**Within a layer/sublayer**, ordering is (in priority):

1. **CDAs first** in layers 2–6 (then everything else); layer 7 isolates
   CDAs in sublayer 7a instead (613.3, 613.4a). This is the "CDA placement"
   rule — there is no separate CDA layer; CDAs simply sort first. Among
   multiple CDAs within the same layer, the normal timestamp and dependency
   rules determine their relative order (613.7, 613.8a(c)): the timestamp part
   follows from 613.7's general rule, and CDA-to-CDA dependency comes from
   613.8a(c).
2. **Timestamp order** — earlier timestamp applies first (613.7). What gets a
   timestamp and when: an effect from a resolved spell/ability is stamped at
   creation (613.7b); an effect from a static ability shares the source
   object's timestamp, or the granting effect's, whichever is later (613.7a);
   if the granting effect is later and the object gets a new timestamp, each
   static-ability effect of that object is re-stamped too, but their relative
   order stays the same (613.7a); an object is stamped on **entering a zone**
   (613.7d); an Aura/Equipment/Fortification is **re-stamped each time it
   attaches** (613.7e); a permanent re-stamps on turning face up/down
   (613.7f) and on transform/convert (613.7g); each counter is stamped when
   placed, and if the object or player already has counters of that kind,
   each of them receives a new timestamp identical to the new counter's
   (613.7c). A sticker is stamped each time it's put on an object; it is
   re-stamped immediately after the object's own new timestamp, and again when
   the object becomes part of a merged permanent; multiple stickers keep their
   relative order as the object enters a zone or merges (613.7k). Variant
   cards: a face-up plane, phenomenon or scheme card is stamped when turned
   face up (613.7h); a face-up vanguard at the beginning of the game (613.7i);
   a conspiracy at the beginning of the game, and again when a face-down one
   turns face up (613.7j). Simultaneous timestamps resolve in APNAP order
   (613.7m); when a
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

**Layer 4: what a type change keeps (205).** Each subtype is correlated to a
card type (205.3c), and an object can't gain a subtype that doesn't
correspond to one of its types (205.3d). Two subtype lists are shared.
Creatures and kindreds share creature types (205.3m, 308.2), so a
noncreature kindred card can have creature types (Nameless Inversion is a
"Kindred Instant — Shapeshifter"). Instants and sorceries share spell types:
Adventure, Arcane, Lesson, Omen, Trap (205.3k). The wording decides whether
prior types survive:

| Wording | Card types | Subtypes |
|---|---|---|
| Sets card type ("is a ... creature", "becomes a 2/2 creature") | replaced, except that instant and sorcery are always retained (205.1a) | a subtype correlated with a removed card type is also removed while that type is gone, unless a remaining card type also has it (205.1a) |
| Sets subtypes | unchanged; removing a subtype never changes card types (205.1a) | replaces only subtypes in the same set: creature, land, artifact, enchantment, planeswalker, or spell types (205.1a). Setting a basic land type also removes the land's rules-text abilities and grants that type's mana ability (305.7) |
| "in addition to its other types", "still a [type]" | all retained (205.1b) | all retained (205.1b) |
| "becomes an artifact creature" | all retained (205.1b) | all retained (205.1b) |
| "becomes a [creature types] artifact creature" | all retained (205.1b) | creature types replaced; other subtypes retained (205.1b) |

Supertypes are independent: changing card types or subtypes never changes
them (205.4b). A permanent that loses every permanent type stays on the
battlefield and is still a permanent (110.4c). March of the Machines ruling
`[2004-12-01]`: "If a noncreature artifact is also another card type, such as
enchantment or land, it will retain those types in addition to being an
artifact creature." Witness Protection sets "a green and white Citizen
creature"; its ruling `[2024-11-08]` says: "If the enchanted creature had any
subtypes other than creature types, such as Equipment, Vehicle, or Shrine, it
loses those as well." Haunted Plate Mail "becomes a 4/4 Spirit artifact
creature that's no longer an Equipment". It states that removal because the
205.1b form would otherwise keep Equipment. For a worked land-type set, see
Blood Moon + Urborg in §10.

## 5. Text-changing effects (612)

Layer-3 anchor (613.1c). A text-changing effect changes words or symbols on
an object, usually its rules text and type line (612.1). Granted abilities
aren't text, so a text change can't modify them (612.3). A token's defined
subtypes and rules text are text, so it can change them (612.4). The CR names
these operations:

| Operation | Example | Rule |
|---|---|---|
| Replace a word used in its rules sense: a color word, a land type, or a creature type | Mind Bend, Artificial Evolution; Swirl the Mists changes every color word to one chosen word | 612.2 |
| Exchange rules text: each object's becomes the other's previous rules text | Exchange of Words | 612.5, 701.12h |
| Full text: text box and type line, plus name, mana cost, color indicator, and P/T | Volrath's Shapeshifter | 612.6 |
| Have all names of nonlegendary creature cards | Spy Kit | 612.7 |
| Set the name; the object loses every other name | Witness Protection | 612.8 |
| Add a word to the name | name sticker | 612.9, 123.6 |
| Append the spliced card's rules text, leaving the spell's own text unchanged | splice | 612.10, 702.47c |
| Replace "target" with "each" | overload | 702.96a, 702.96c |
| Remove all text in square brackets | cleave | 702.148a, 702.148b |

**Names.** A change to a color word or subtype can't alter a card name, even
one that contains that word (612.2). Text that makes a token can be changed,
though, because its creature types also serve as the token's name (612.2a).
Other text-changing effects *do* change names in layer 3 (612.6-612.9). To
find the name of an object with name stickers, start from its copiable
values, then apply each name sticker and each other text-changing effect in
timestamp order (123.6c); otherwise layer-3 effects follow the usual
timestamp and dependency order (613.7, 613.8). For example, a Witness
Protection with a later timestamp than a sticker leaves that sticker's word
out of the name (123.6c example). Copy effects and face-down status set the
name earlier, in layer 1 (613.2a, 613.2b; 707.2, 708.2a).

**Word replacement.** Rulings `[2004-10-04]` on Artificial Evolution and Mind
Bend (the last two bullets are Artificial Evolution's only):

- The words are chosen on resolution.
- "It can't change a word to the same word."
- It changes only text printed on the card (or set on a token when it was
  created, or by a copy effect): "It will not change any effects that are on
  the permanent." *(Artificial Evolution only: a creature type set by an
  effect is untouched.)*
- "Changing the text of a spell will not allow you to change the targets of
  the spell because the targets were chosen when the spell was cast."
  *(Artificial Evolution only.)*

## 6. Replacement effects (614)

Continuous effects that watch for an event that *would* happen and
completely or partially replace it with a different event — "shields" around
what they affect (614.1). **They never use the stack** (they are continuous
effects, not abilities that resolve). Recognition markers:

- **"instead"** (614.1a); **"skip"** (614.1b — = "instead of doing X, do
  nothing"; 614.10). Skip *is* a replacement effect (614.1b, 614.10). Once a
  step, phase, or turn has started it can no longer be skipped; the skip
  waits for the next occurrence (614.10). Scheduled things and skip counting
  (two skip-next effects skip the next two occurrences): `temporal.md` §2 and
  `state.md` §8 (614.10a). An effect that skips a step, phase, or turn and
  then takes another action makes that action the first thing that happens
  in the next step, phase, or turn that actually occurs (614.10b).
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
  example). (Engine bookkeeping for this is noted in `state.md` §8.) (Except
  the two CR-stated exceptions to 614.5, which may apply more than once to
  the same event: an Attraction's command-zone replacement, 717.6, and the
  commander command-zone replacement, 903.9b.)
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
  effect**; if either permanent (the original or the new recipient) is no
  longer on the battlefield (or is no longer a battle/creature/planeswalker)
  when the redirect would occur, or if damage would be redirected to or from
  a player who has left the game, the effect does nothing (614.9).
- **Draw replacements (614.11):** effects that replace card draws apply even
  when the affected player's library is empty; within a sequence of draws,
  all replacement actions are completed before the sequence resumes
  (614.11a); if the effect would have the player perform an additional action
  on the drawn card and the draw is replaced, that additional action is not
  performed on cards drawn by the replacement (614.11b).
- **ETB replacements:** check the permanent's characteristics *as it would
  exist on the battlefield*, accounting for replacements already applied
  (per 616.1), the permanent's own statics, and existing continuous effects
  (614.12). An ETB replacement may come from the permanent itself only if it
  affects only that permanent, not a general subset that includes it; Orb of
  Dreams ("Permanents enter tapped") doesn't affect itself, so it enters
  untapped (614.12). Required choices are made before it enters (614.12a);
  when several choice-requiring ETB replacements modify permanents entering
  simultaneously, no choice may make their combined costs unpayable
  (614.12b). An anchor-word choice ("[Anchor word] — [ability]") means "as
  long as that word was chosen as this permanent entered, it has [ability]"
  (614.12c). An ETB modifier may move other objects too (614.13), but not
  objects entering alongside it (614.13a) and not the same object twice
  (614.13b). A card entering the battlefield from a library is excluded from
  a mill/exile-from-the-top replacement applied while it enters, even though
  it's still in the library as the effect is applied (614.13c).
- "Can't" effects aren't replacement effects but follow similar rules
  (614.17): they must exist before the event (614.17a), a player can't choose
  to pay a cost that includes an event that can't happen (614.17b), and such
  an event can be replaced only by a self-replacement effect (614.17c). A
  "can't enter" effect is checked like an ETB replacement (614.17d, cf.
  614.12). (Skip *is* a replacement effect: 614.1b, 614.10.)

## 7. Prevention effects (615)

Continuous "shields" that watch a **damage** event and completely/partially
prevent the damage (615.1); marker word **"prevent"** (615.1a). Like
replacements they apply as events happen, can't go back in time, and last
until used up or expired (615.1, 615.3, 615.4).

- A "prevent the next N damage" shield from a resolved spell/ability
  prevents 1 per point; each prevented point reduces the shield by 1;
  multiple simultaneous sources let the player/controller choose which the
  shield eats; once at 0, the rest is dealt normally — only the amount
  matters, not the number of sources (615.7). "Next time [source] would deal
  damage" from a resolved spell/ability prevents one whole instance
  regardless of size (615.8). A static "prevent N of that damage" isn't
  consumed; it prevents N in each applicable damage event (615.10).
- **Damage-amount forms are sorted by marker word, not by whether they raise
  or lower damage.**
  - *Prevention* ("prevent", 615.1a): all of it; the next N, which is a
    shield (615.7; untargeted sets get one shield per creature, 615.11); N of
    each applicable event, from a static ability (615.10); all but N; half,
    rounded up or down; the next instance from a source, whatever its size
    (615.8).
  - *Replacement* ("instead", 614.1a): double (701.10g) or triple; half,
    rounded down; that much plus or minus N; a set amount, usually above a
    threshold. Divine Presence: "If a source would deal 4 or more damage to a
    permanent or player, that source deals 3 damage to that permanent or
    player instead."

  The halving and set-amount forms reduce damage but are **not** prevention.
  "Can't be prevented" doesn't stop them (615.12 governs prevention effects
  only), and they don't fire "when damage is prevented" triggers (615.13).
  Divine Presence ruling `[2004-10-04]`: "This is not preventing damage since
  it does not use the word 'prevent'. It is a replacement." Ghosts of the
  Innocent ruling `[2005-10-01]`: "This isn't a damage prevention effect. If
  Excruciator ... would deal 7 damage to a permanent or player, it deals 3
  damage instead." Unstable Footing ruling `[2009-10-01]`: "Effects that
  replace or redirect damage without using the word 'prevent' are not
  affected by Unstable Footing." The affected player, or the affected
  object's controller, orders both kinds together (616.1). These forms come
  from the corpus; the CR doesn't list them. Check `scripts/corpus` before
  rejecting a wording that isn't listed here.
- **Prevention with an added effect (615.5).** Some prevention effects add an
  effect that may refer to the amount prevented ("The source's controller
  draws cards equal to the damage prevented this way"). The prevention
  happens when the original event would have, and the added effect happens
  immediately afterward. It doesn't use the stack, unlike a "when damage is
  prevented" trigger (615.13). An added effect that deals damage creates new
  damage from its own source; it is not a redirection. Comeuppance ruling
  `[2014-11-07]`: "Comeuppance is the source of the new damage ... The new
  damage is not combat damage, even if the prevented damage was."
- **"Can't be prevented":** prevention effects still *apply* (so their
  additional effects happen) but prevent no damage, and existing shields
  aren't reduced (615.12); a prevention effect applies to a particular
  unpreventable event just once (615.12a). An added effect measured by the
  damage that *would* be dealt still uses that full amount. Gatta and Luzzu
  ruling `[2025-06-06]`: "you still put that many +1/+1 counters on it".
  Angel of Suffering ruling `[2022-04-29]`: "you'll still mill twice that many
  cards". Unstable Footing's ruling `[2009-10-01]` says added effects "that
  don't depend on the amount of damage prevented" still work. An added effect
  keyed to "damage prevented this way" counts 0. Phyrexian Hydra ruling
  `[2011-06-01]`: "If damage dealt to Phyrexian Hydra can't be prevented ...
  it will be dealt as normal and won't cause Phyrexian Hydra to put -1/-1
  counters on itself."
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
615.12a) (except the two CR-stated exceptions to 614.5, which may apply more
than once to the same event: an Attraction's command-zone replacement, 717.6,
and the commander command-zone replacement, 903.9b); re-collect applicable
effects (some only became applicable now, 616.2) and repeat until none apply;
then perform the final modified event (614.6). Engine choice: run events
nested inside the proposed event as sub-pipelines; 616.1g bars choosing an
effect on the contained event until the outer event's effect has been chosen.

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
Humility losing its own ability. Opalescence says "Each other non-Aura
enchantment", so it never animates itself and Humility never strips it. The
two-Opalescence case is ruling `[2006-02-01]`: in the order Opalescence,
Humility, Opalescence, the second Opalescence is 1/1 while Humility and the
first Opalescence are 4/4.

Trace both timestamp orders (earlier timestamp applies first within 7b,
613.7):

| (sub)layer | Opalescence earlier | Humility earlier |
|---|---|---|
| **L4** type | Humility becomes a creature-enchantment (Opal.) | same |
| **L6** abilities | Humility (and other animated enchantments, but not Opalescence itself) lose all abilities (Hum.) | same |
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
