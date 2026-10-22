# Abilities — Taxonomy

*Synthesized from the Comprehensive Rules effective 2026-09-25
(`data/rules/cr.json`).*

How an engine should classify what a card can do. The four general
categories partition every ability (113.3); the cross-cutting sub-kinds
overlay them with special timing/stack rules. Closed lists are enumerated
in full. For mapping surface card text to these categories, see
`grammar.md` section 1 (segmentation, 113.2c) and section 2 (surface forms by
ability kind).

## 1. The four kinds

Rule 113.3 names four general categories. Abilities of all four kinds can be
characteristics of objects (113.1a); a player can also have abilities,
normally only when effects grant them (113.1b). Only activated and triggered
abilities are ever objects themselves, on the stack (113.1c); static
abilities never use the stack (113.9).

- **Spell ability** (113.3a) — instructions followed while an instant or
  sorcery spell resolves. Any text on an instant/sorcery is a spell ability
  unless it's an activated, triggered, or 113.6-qualifying static ability
  (113.3a). Grammar cue: imperative sentences with no cost/colon and no
  when/whenever/at. See `grammar.md`.
- **Activated ability** (113.3b) — has a cost and an effect, written
  "[Cost]: [Effect.] [Activation instructions (if any).]" (113.3b, 602.1).
  The cost is everything before the colon (602.1a). Activate whenever you
  have priority; it goes on the stack (113.3b, 602.1c). The *only* kind of
  ability that can be activated; a bare "activate an ability" means this
  kind (602.1c).
- **Triggered ability** (113.3c) — has a trigger condition and an effect,
  written "[Trigger condition], [effect]," and includes (usually begins
  with) "when," "whenever," or "at" (113.3c). When the event occurs it goes
  on the stack the next time a player would receive priority (113.3c, 603.3).
  A very few triggered abilities put the trigger condition mid-ability, and a
  static ability can share a paragraph with triggered abilities linked to it
  (603.11; linkage 607.2h, section 2).
- **Static ability** (113.3d) — written as a statement; it's simply true,
  creating a continuous effect active while the source is in the appropriate
  zone (113.3d, 604.1). Does not use the stack and can't be countered
  (113.9, 604.1). See `effects.md`. A few statics carry a one-shot action
  instead (section 2, action-performing statics). "[This permanent] enters
  with...", "As [this permanent] enters...", "[This permanent] enters as..."
  and "[This permanent] enters tapped" are static abilities, not triggered
  ones (603.6d), and they generate replacement effects (614.1c–d). See
  `grammar.md` section 4 and `effects.md` section 6.

**Keyword abilities** (702.1) are notational shorthand. A keyword names one
or more abilities of the four kinds (702.1). Some explicitly represent
several, e.g. suspend (static + 2 triggered, 702.62a), cipher (spell +
static, 702.99a), class level bar (activated + static, 716.2). The
machine-readable list of keyword abilities lives in
`data/rules/keywords.json`; `scripts/keyword <name>` prints a keyword's
defining CR section.

## 2. Cross-cutting sub-kinds

These overlay the four kinds. Each carries special timing or stack behavior
an engine must special-case.

| Sub-kind | Defining rule | Underlies kind(s) | Recognize by |
|---|---|---|---|
| Mana ability (activated) | 605.1a | activated | no target, could add mana, not loyalty, doesn't move cards to/from a library; judged ignoring non-self replacement effects |
| Mana ability (triggered) | 605.1b | triggered | no target, triggers off a mana ability / mana added, could add mana |
| Loyalty ability | 606.2 | activated | loyalty symbol in the cost |
| Characteristic-defining (CDA) | 604.3a | static | states a defining characteristic (color/subtype/P/T) about itself |
| Linked abilities | 607.1 | activated/triggered/static | one ability refers to what another did ("the exiled cards," "the chosen color") |
| Delayed triggered | 603.7 | triggered | created by a resolving effect, a replacement effect, or an allowing static (603.7a); "when/whenever/at" not at the start |
| State trigger | 603.8 | triggered | triggers while a game *state* holds, not on an event |
| Action-performing static (engine grouping, not a CR term) | 702.131b, 702.195a, 702.145b | static | "Any time [state], [action]"; daybound/nightbound's "As it becomes night/day, ..." (not "As [this] enters", which is a replacement effect, 614.1c); one-shot, no stack |
| Intervening-"if" trigger | 603.4 | triggered | "When/Whenever/At [event], **if** [condition], [effect]" |
| Reflexive triggered | 603.12 | triggered | "When you do, ..." referring to an action taken during the same resolution |

**Mana abilities** (605.1) — two disjoint definitions:
- *Activated*: no target, *could* add mana on resolution, not a loyalty
  ability, and its cost/effect moves no card to or from a library (605.1a).
  Judge these on the ability as written: "Do not take into account
  replacement effects that may apply, other than self-replacement effects"
  (605.1a). A self-replacement effect is an effect of a resolving spell or
  ability that replaces part or all of that spell or ability's own effect; its
  text is usually part of that ability but can be a separate ability (614.15).
  So Ashnod's Altar ("Sacrifice a creature: Add {C}{C}") stays a mana ability
  when the sacrificed creature is Blightsteel Colossus, whose static
  replacement effect (not a self-replacement) shuffles it into its library
  (inference from 605.1a and 614.15; no ruling). The "could produce" test
  works the other way: it counts applicable replacement effects in any
  possible order (106.7; `mana.md` section 3).
  *Triggered*: no target, could add mana, and triggers
  off activating/resolving a mana ability or off mana being added (605.1b).
- Special behavior: neither uses the stack — each resolves immediately and
  can't be targeted, countered, or responded to (605.3b, 605.4a). An
  activated mana ability may be activated whenever priority is held *or*
  whenever a mana payment is asked for, even mid-cast/mid-resolution
  (605.3a). Once begun, it can't be activated again until it resolves
  (605.3c). Stays a mana ability even when it can't currently produce mana
  (605.2). A spell is never a mana ability (605.5b); an ability with a
  target never is (605.5a).

**Loyalty abilities** (606) — an activated ability with a loyalty symbol in
its cost (606.2); normally only planeswalkers have them (606.2). Activate
only with priority, an empty stack, during a main phase of your turn, and
only if no loyalty ability of *that permanent* was activated this turn
(606.3). The cost is putting on or removing loyalty counters as the symbol
shows (606.4); multiple add/remove costs combine into one (606.5). A
negative-cost ability needs at least that many counters present (606.6).

**Linked abilities** (607) — two abilities where one takes an action and the
other refers only to *that* action's objects/players (607.1). The second
("the exiled card," "the chosen color," etc.) ignores anything any other
ability did (607.1). Both abilities must be printed on the object (607.1).
607.1a–d extend this: an ability printed within an ability that grants it
counts as printed; either face of a nonmodal DFC counts; one ability can be
linked to itself; and a token, emblem, or permanent can be linked to the
object whose ability created it or put it onto the battlefield. If the first
ability exiled several cards, the second refers to each, and a value it reads
is the sum (607.3). A reference to an undefined linked choice does nothing
(607.5a). See `queries.md` section 3 (Stored bindings) and section 4
(undefined values). Recognize the closed list of linkage patterns in
607.2: exile-then-reference (607.2a), replacement-exile reference (607.2b),
put-onto-battlefield reference (607.2c), "choose a [value]" / "the chosen
[value]" (607.2d), noted-information reference (607.2e), choose-a-word
reference (607.2f), enters-cost reference (607.2g), static-plus-its-own-
triggers in one paragraph (607.2h), additional-cost-paid reference (607.2i),
variable-cost-paid reference (607.2j), champion (607.2k), anchor word
(607.2m), pre-game-exile-by-name reference (607.2n), pre-game CDA choice
(607.2p), and spell-cast-cost-exile reference (607.2q). An ability may
belong to more than one linked pair (607.4); an object that acquires both
abilities of a pair as part of the same effect has them linked to each other
and to no other ability (607.5). Engine: track what the first ability did so
the second can resolve (see `state.md` linked-ability tracking).

A self-linked ability both acts and refers back to what it did (607.1c).
Mimic Vat's imprint ability reads "you may exile that card. If you do, return
each other card exiled with this artifact to its owner's graveyard". It reads
cards exiled by its own earlier resolutions and by no other ability (Mimic Vat
[2011-01-01]: "choosing to exile a card this way causes the previously exiled
cards to return to their owners' graveyards"). It is also linked to the token
ability that reads "a card exiled with this artifact" (607.2a, 607.4).
Engine: a linked set is memory that persists across resolutions of a single
ability. "This way" is different: it reads only the current resolution
(`queries.md` section 3; engine inference).

**Characteristic-defining ability** (604.3) — a static ability conveying a
characteristic normally found elsewhere on the object (604.3). The closed
criteria (604.3a): it defines (1) color, subtype, power, or toughness; (2)
is printed on / granted to the token / copied/text-changed onto the object;
(3) doesn't directly affect other objects' characteristics; (4) isn't one
the object grants itself; (5) doesn't set the value only conditionally. A
CDA functions in *all* zones, outside the game, and before the game begins
(604.3, 113.6a). In the layer system, CDA-defined P/T applies in layer 7a
ahead of other P/T effects (613.4a), and CDAs apply first within layers 2–6
(613.3).

*Choice-reading CDAs.* Depending on a choice is not setting a value "only if
certain conditions are met" (criterion 5). The CR's own CDA example is Lost
Order of Jarkeld: "As this creature enters, choose an opponent" plus "power
and toughness are each equal to 1 plus the number of creatures the chosen
player controls" (208.2a). Shapeshifter's last-chosen-number P/T likewise "is
a characteristic-defining ability" (Shapeshifter [2008-08-01]). The subtype
version, "This creature is the chosen type in addition to its other types"
(Adaptive Automaton, Metallic Mimic; Thran Portal for land types), meets the
same five criteria and is a CDA on the same reading (inference; no ruling
classifies these cards). Being a CDA fixes its place in the layers: it applies
first in layer 4, or in sublayer 7a for P/T, ahead of timestamp order (613.3,
613.4a). It also can't depend on, or be depended on by, a non-CDA effect
(613.8a; `effects.md` section 4). Off the battlefield no choice has been made.
A P/T CDA then uses 0 for the number it can't determine (208.2a: Lost Order is
1/1 there; by the same rule Shapeshifter is 0/7). A subtype CDA adds nothing,
because the linked ability "refers only to a choice made as a result of the
first ability" (607.2d; inference). A choice made before the game begins is
the exception: it carries across zones (607.2p).

Removing a CDA in layer 6 doesn't undo a color or subtype it already set in
layers 4–5 (613.1d–f; Moritte of the Frost [2021-02-05]; a changeling card in
a graveyard still has all creature types, Yixlid Jailer [2021-03-19]), but
does stop a P/T CDA, which applies later in 7a (613.4a; * = 0, Yixlid Jailer
[2021-03-19]). A keyword the CR calls a CDA (changeling, 702.73a; devoid,
702.114a) but that is granted any way other than those in criterion (2) is not
settled by the CR (604.3a; UD-16).

**Delayed triggered ability** (603.7). Created during resolution of a
spell/ability, by a replacement effect, or by a static ability allowing an
action (603.7a). Contains "when/whenever/at," usually not at the start
(603.7). It won't trigger until actually created, even if its event just
happened (603.7a). Triggers only once, the next time its event occurs, unless
given a duration (603.7b). Source and controller are fixed by 603.7d–g,
depending on what created it. One that triggers on its creator's Nth
resolution in a turn is created only once (603.7h). A permanent spell's
on-stack static (dash, blitz, warp) creates its trigger as the permanent is
put onto the battlefield, during resolution (608.3g). So 603.7d fixes its
source (the spell) and its controller (the player who controlled the spell as
it resolved). Settled by 608.3g; see UD-40.

*Object binding* (603.7c). A delayed trigger that refers to a particular
object "still affects it even if the object changes characteristics." It
doesn't affect the object if, when the trigger resolves, the object is no
longer in the zone it's expected to be in. An object that left and returned is
a new object (603.7c, 400.7). Sneak Attack [2020-08-07]: "If that creature has
left the battlefield, even if it came back, you don't sacrifice it." The
referent is fixed when the trigger is created (603.7c; lock table in
`temporal.md` section 3). The creating effect can bind the new object it just
moved to a public zone (400.7j): Flickerwisp's "Return
that card to the battlefield ... at the beginning of the next end step" names
the card in exile, its expected zone. 400.7j reaches only "other parts of that
effect," so a later move by anything else is not followed (inference from
603.7c and 400.7j). The referent doesn't have to have moved. Angrath, the
Flame-Chained's "Sacrifice it at the beginning of the next end step if it has
mana value 3 or less" refers to the creature the ability targeted, and
"Whether the target creature has mana value 3 or less is checked only as the
delayed triggered ability ... resolves" (Angrath, the Flame-Chained
[2018-01-19]). Information about a referent that has left its zone comes from
its last known information (608.2h). For zone-change bindings in general, see
`queries.md` section 3.

**State trigger** (603.8) — triggers when a game *state* matches its
condition (e.g., "Whenever you have no cards in hand"), not on a discrete
event (603.8). Fires as soon as the state holds and goes on the stack at
the next opportunity; it won't trigger again until it has left the stack,
then re-triggers if its object is still in the same zone and the state still
matches (603.8). Distinct from state-based actions (603.8).

**Action-performing statics** (engine grouping, not a CR term). Some static
abilities carry a one-shot action, which 113.3d's "create continuous effects"
does not describe. The keyword cases are: ascend on a permanent, "Any time you
control ten or more permanents and you don't have the city's blessing, you get
the city's blessing for the rest of the game" (702.131b); storied, the same
shape for an enduring story (702.195a); and daybound's "As it becomes night,
if this permanent is front face up, transform it," mirrored by nightbound
(702.145b, 702.145e). The rules add companions: a daybound permanent front
face up at night, or a nightbound one back face up during the day, is
transformed: "This happens immediately and isn't a state-based action"
(702.145c, 702.145f). Any time a player controls a daybound permanent and it's
neither day nor night, it becomes day (702.145d); a nightbound permanent does
the same for night only if no daybound permanent is on the battlefield
(702.145g). The CR doesn't say whether these two are state-based actions.
These abilities don't use the stack and aren't triggers: "Ascend on a
permanent isn't a triggered ability and doesn't use the stack" (Wayward
Swordtooth [2018-01-19]; storied: Balin, Loremaster [2026-06-29]). They act
before state-based actions: if your tenth permanent enters and one leaves to
the legend rule or 0 toughness, "you get the city's blessing before it leaves
the battlefield" (same rulings). They also act mid-resolution: if Ocelot
Pride's token is your tenth permanent, "you'll get the city's blessing before
the ability would check to see if you have the city's blessing" (Ocelot Pride
[2024-06-07]). The result outlives the source ("for the rest of the game").
Gaining the designation reapplies continuous effects before trigger conditions
are checked (702.131d, 702.195c). Engine (inference): evaluate these after
every state change, separately from state triggers (603.8, which go on the
stack) and from state-based actions (704.3, checked only when a player would
receive priority). Some similar always-checked rules are state-based actions
instead: start your engines! sets a player's speed to 1, "This is a
state-based action" (702.179a, 704.5aa), and so is space sculptor's "Any time"
sector assignment (702.158c, 704.5u). Designation details are in
`designations.md`.

**Intervening-"if" trigger** (603.4) — "When/Whenever/At [event], **if**
[condition], [effect]" (603.4). The condition is checked when the event
occurs (no trigger if false) *and again* on resolution (removed from the
stack if false then), mirroring the legal-target check (603.4). This rule
applies only to an "if" immediately following the trigger condition;
elsewhere "if" has its plain meaning (603.4).

**Reflexive triggered ability** (603.12) — created by a resolving spell/
ability that lets/instructs a player to act, triggering "when [a player]
[does/doesn't]" or "when [something happens] this way" (603.12). It follows
the delayed-trigger rules but is checked *immediately* after creation,
triggering on whether the event occurred earlier during the *same*
resolution (603.12). Normally triggers once per occurrence, but a
"pay this cost any number of times" / "when you pay one or more times"
pairing triggers it only once (603.12a).

## 3. Where abilities function

Default (113.6): abilities of an instant/sorcery spell function only while
it's on the stack; abilities of all other objects function only while on
the battlefield. The full list of exceptions (113.6a–p):

- 113.6a — characteristic-defining abilities function everywhere, even
  outside the game and before it begins.
- 113.6b — an ability stating which zones it functions in functions only
  from those zones.
- 113.6c — an ability stating which zones it *doesn't* function in functions
  everywhere else, even outside/before the game.
- 113.6d — an alternative-cost / cost-modifying ability for that object
  functions on the stack.
- 113.6e — an ability restricting/modifying how *that* object can be
  played/cast functions in any zone it could be played/cast from and on the
  stack; one that *grants another ability* doing so functions only on the
  stack.
- 113.6f — an ability restricting/modifying *what zones* that object can be
  played/cast from functions everywhere, even outside the game.
- 113.6g — "can't be countered" / "can't be copied" functions on the stack.
- 113.6h — an ability modifying how that object enters the battlefield
  functions as it enters (see 614.12).
- 113.6i — "counters can't be put on this" functions as it enters *and*
  while on the battlefield.
- 113.6j — an activated ability whose cost can't be paid on the battlefield
  functions from any zone where its cost can be paid.
- 113.6k — a trigger condition that can't trigger from the battlefield
  functions in all zones it can trigger from; other conditions of the same
  ability may function in different zones.
- 113.6m — an ability that moves its object out of a particular zone
  functions only in that zone (with stated exceptions for being put there
  first, or an Aura's enchanted permanent leaving). The same holds if the
  ability's effect creates a delayed triggered ability whose effect moves the
  object out of that zone.
- 113.6n — a deck-construction-modifying ability functions before the game
  begins.
- 113.6p — abilities of emblems, plane, vanguard, scheme, and conspiracy
  cards function in the command zone.

(Static-ability variants are restated by 604.5 for the stack and 604.6 for
play-from-hand wording.)

Look-back triggers (603.10a–g) are evaluated against the abilities that
existed, and objects as they appeared, immediately before the event. So a
leaves-the-battlefield trigger such as "when this creature dies" triggers from
the battlefield (603.6c, 603.10a). A self-referential "When [this card] is put
into a graveyard from anywhere" trigger is never a leaves-the-battlefield
ability (603.6c). It triggers from the graveyard even when the card came from
the battlefield (113.6k; Yixlid Jailer [2021-03-19]). A "from anywhere"
trigger that watches other cards functions where its object normally does
(113.6). See `events.md` section 6 (look-back triggers).

## 4. Abilities as objects vs as properties

An ability is normally a *property* — a characteristic an object has that
lets it affect the game (113.1a), or, for a player, something granted by an
effect that changes how the game affects them (113.1b). But an activated or
triggered ability *on the stack* is itself an **object** (113.1c).

Once activated or triggered, an ability on the stack exists **independently
of its source** — destroying or removing the source afterward doesn't affect
the ability (113.7a). Some abilities make the *source* do something rather
than acting directly; such an ability checks source information when it's
put on the stack (if needed then) or otherwise on resolution, and falls
back to the source's last known information if the source has left its
expected zone — the source can still perform the action even if it no longer
exists (113.7a). Static abilities can't use last known information (604.7).
The source of an ability is the object that generated it (113.7); its
controller is set by 113.8 (delayed triggers: 603.7d–g; 113.7 and 113.8 say
d–f, but 603.7g also applies; for dash/blitz/warp see 608.3g, settled in
UD-40). Abilities on
the stack aren't spells and can't be countered by spell-only
counters, though "counter target ability" effects work; static abilities
never use the stack and can't be countered at all (113.9).

## 5. Granted and lost abilities

Effects can add or remove abilities: an adding effect says the object
"gains" or "has" the ability, a removing effect says it "loses" it (113.10).
Removing an ability removes *all* instances of it (113.10b); adding an
activated ability may include activation instructions that become part of it
(113.10a). These changes are continuous effects applied in **layer 6**
(ability-adding, keyword counters, ability-removing, and "can't have")
(613.1f); generally the most recent add/remove of the same ability prevails,
subject to dependency (113.10c, 613.3). See `effects.md` for the layer
system.

**Keyword counters** give one instance of the keyword per counter. Each
counter "causes that object to gain that keyword" (122.1b), and "A creature
with multiple exalted counters will have that many instances of exalted"
(Emissary of Soulfire [2024-06-07]). Each instance functions independently.
Whether extra instances do anything depends on the keyword's own rule
(113.2c). Of the fifteen keyword-counter keywords (122.1b), thirteen say
multiple instances are redundant: flying (702.9c), first strike (702.7d),
double strike (702.4e), deathtouch (702.2f), haste (702.10d), hexproof
(702.11h), indestructible (702.12c), lifelink (702.15f), menace (702.111c),
reach (702.17c), shadow (702.28c), trample (702.19g), and vigilance (702.20c).
Exalted and decayed have no such rule and include triggered abilities
(702.83a, 702.147a), so each instance triggers. Two exalted counters give a
creature attacking alone +2/+2 (Akrasan Squire [2008-10-01]: "+1/+1 for each
of your exalted abilities"). Two decayed instances create two end-of-combat
sacrifices, and the second finds nothing (inference; 113.2c, 603.7c). Engine:
store keyword-counter grants as a count per keyword, not a flag. "Loses
[keyword]" removes every instance (113.10b).

"Can't have" effects (113.11) go further: the object loses the ability if it
has it, and no effect or keyword counter can add it — a continuous effect
that would add it simply doesn't apply that part (113.11). Note "loses all
abilities" / "all creatures lose all abilities" applies the moment a
permanent is on the battlefield, so it can strip an enters-the-battlefield
trigger before it would fire (603.6b).

An effect that sets a characteristic ("[permanent] is [value]") or states a
quality ("[creature] can't be blocked") is not a granted ability, so removing
the affected object's abilities doesn't end it (113.12). This holds whatever
generated the effect, including another object's static ability or a resolved
spell or ability. Such an effect is an ordinary layer effect in timestamp
order, not a CDA, unless it meets 604.3a. The same words printed on the object
itself are its own static ability (113.2a), and "loses all abilities" removes
them. That ends a quality such as "can't be blocked", but it doesn't undo a
type or color the ability already set in layers 4–5 (613.1 order; see the CDA
paragraph).
