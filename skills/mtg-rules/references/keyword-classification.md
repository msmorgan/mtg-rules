# Keyword Classification — Intrinsic / Composite / Marker

*Synthesized from the Comprehensive Rules effective 2026-09-25
(`data/rules/cr.json`).*

Every keyword ability with its own 702 entry and every keyword action
(CR 701) is classified by **what an engine has to build for it**, one row
per catalog entry. Variants defined inside a section inherit the section
row (see Keyword variants); keyword abilities the CR defines elsewhere are
listed in Keyword abilities without a 702 entry. The full per-keyword data
(all 266 rows, `how` rationale, cites, `core_referenced` flag) lives in
`../keywords-classified.json`; this doc holds the rubric, the engine
primitive basis, and the closed-class tables. The JSON is the authority for
the 222-row composite enumeration — only highlights appear below.

## Rubric (rubric_version 1)

Four classes, by what machinery the keyword forces:

- **intrinsic** — needs its own engine opcode. It changes *prospective*
  machinery (combat-damage assignment legality, lethality computation,
  priority/turn structure, the casting pipeline, native zone/status events)
  in a way no composition of statics + triggers + replacements + permissions
  + restrictions + action-sequences reproduces. Exemplars: **trample**
  (702.19a–b: a static that modifies attacking combat-damage assignment;
  lethal to every blocker before any excess may go to the player,
  planeswalker, or battle attacked, 702.19b. The baseline 510.1c confines a
  blocked creature's damage to its blockers, divided as its controller
  chooses); **deathtouch** (702.2c makes any nonzero combat damage lethal
  for excess-damage determination, read by 702.19b and restated in 120.4a,
  plus the dedicated SBA 704.5h).
- **composite** — compiles to the primitive basis already in the engine.
  Exemplars: **flying** (a declare-blockers legality predicate: can't be
  blocked except by flying/reach, 702.9b); **ward** (a triggered toll:
  trigger + counter-unless-pay, 702.21a); **scry** (a look/move action
  sequence, 701.22a).
- **composite-given(P)** — decomposes *iff* the basis includes a named
  primitive `P` (recorded in the `given` field). Exemplars: **lifelink** =
  augment the damage *result* (gain that much life in addition) *given* the
  damage-result-rewrite stage; CR hardcodes it as 120.3f (702.15b).
  **daybound** = statics reading the day/night designation (731.1) *given*
  the progress-track primitive; CR builds the designation as rule 731
  (702.145b–c).
  Without `P`, these would each demand their own opcode; sharing `P` keeps
  the intrinsic set minimal — and `P` must earn its keep (dependents
  threshold below).
- **marker** — no function of its own; meaning lives entirely in *other*
  rules' predicates that reference it. Type specimen: **reach** (only
  flying's blocking predicate 702.9b gives it meaning, 702.17b).

Orthogonal flag **`core_referenced`** (data in the JSON): true iff the
keyword is named in CR rules *outside* its own 70x.x section. The scan is
regenerable from `data/rules/cr.json`; `meta.core_referenced_rule` in the
JSON repeats this policy.

- **Scanned:** each rule's `ruleText`. Examples and the glossary are not.
- **Matched:** the keyword's printed name, case-insensitive, whole word.
  Abilities also match the plural; actions match every verb inflection
  (scries, planeswalked). A derived adjective or participle of an ability
  name (bestowed, kicked, equipped, enchanted) is not the name, so Bestow is
  false although 608.3b says "bestowed Aura spell".
- **Counts:** a mention inside another 70x section (702.17b names flying;
  701.71a names Surveil), a "See rule…" pointer that prints the keyword's
  name (608.3g names Dash, Blitz, and Warp), and token-definition text
  (111.10e names Scry; 111.10k, trample).
- **Does not count:** a pointer that gives only a rule number.
- **Homograph exclusions** (reviewed; the hit is not the keyword):
  - Dash: "long dash" in 301.3, 302.3, 303.3, 304.3, 305.5, 306.3, 307.3,
    308.2, 310.3, 311.3, 205.3b, 702.159b, 717.5, and 719.3. Only 608.3g
    remains.
  - Melee: "Grand Melee" in 801.18, 807.1, 807.2, 807.2c, 807.4, 807.5,
    901.13, and 901.14.
  - Double: "double strike", "double agenda", and "rolled doubles". 107.1b
    remains.
  - Fading, Storm, Transmute, Harness, Protection, Ward, and Flying: card
    names in 206.3a–c and 712.5c. Harness, Protection, Ward, and Flying keep
    their other hits.
  - Persist: the ordinary verb (603.2e).
  - Endure: "enduring story" (702.195a–c).
  - ∞ (Infinity): the artifact type (205.3g).
  - Shadow: "Shadows over Innistrad" (712.2a–b). 122.1b remains.
  - Search: "search for a copy" (707.1). Other hits remain.

## Primitive basis (`given` vocabulary)

The composite-given class decomposes against exactly five primitives. Adding
any one of these to the engine collapses a cluster of would-be intrinsics
into compositions. Each cross-refs the relevant `generalizations.md`
directive/family.

| primitive | one-line definition | keywords needing it | generalizations cross-ref |
|---|---|---|---|
| `damage-result-rewrite` | A stage that rewrites the *result* of a damage event (substitute or augment what damage does), not its amount — the slot CR 120.3 hardcodes. | Lifelink, Wither, Infect, Toxic | (no `generalizations.md` family; CR home 120.3 — damage results, not 614/615 replacements; reusing Family 11's transform algebra is an engine inference) |
| `progress-track` | A game-maintained value with thresholds that statics read: the game's day/night designation (731.1) or a player's speed (702.179b). Turn-based actions (703.4b, 731.2), state-based actions (702.179a), inherent triggers (702.179d), keyword rules (702.145d, 702.145g), and other effects (731.1) change it. It is not monotonic. Day and night alternate (731.2a–b), though once set the game never returns to neither (731.1), and an effect can lower speed (Spikeshell Harrier). Any bound belongs to the change, not the track. The CR caps only the inherent trigger ("if your speed is less than 4", 702.179d); Spikeshell Harrier's floor of 1 is its own text ("This effect can't reduce their speed below 1"). | Daybound, Nightbound, Max Speed, Start Your Engines! | Family 4 (speed) + Family 12 / `designations.md` (day/night); why speed is composite-given while Level Up, Venture into the Dungeon, The Ring Tempts You, and Read Ahead are plain composite: `underdetermined.md` UD-30 |
| `attachment-relation` | A first-class `attached_to` edge to a legal host (object or player) with legality predicate and violation policy. | Attach | Family 5 / directive 2 (attach carries host+predicate+policy) |
| `cost-modification-hook` | A *payment substitution* on a mana payment, with two scopes. **(a) Whole total:** it edits how the already-locked total cost is paid during 601.2g–h (imported for abilities by 602.2b) and is *neither* an additional *nor* an alternative cost (702.51b, 702.66b, 702.126b): convoke, delve, and improvise; assist changes who pays the generic part (702.132a). **(b) One component:** it attaches to one cost component and applies wherever that component is paid (701.67a–b), including an alternative cost, a resolution "unless" cost (118.12a), and ward's cost (702.21a): waterbend. | Delve, Convoke, Improvise, Assist, Waterbend | **defining home: `costs.md` §4** (payment substitution with two scopes); directive 10 (mana payment predicates) |
| `face-down-objects` | A primitive for objects existing face down (708): put/cast face down as a 2/2, secret-identity memory, special action to turn face up. Scope is exactly 708's — face-down spells and permanents (708.1); 708.5 is only a look permission (face-down cards in other zones can't be looked at). Foretell (exile, 406.3–4) and hidden agenda (command zone, 905.4a) compile to native zone machinery instead. | Morph, Manifest, Manifest Dread, Disguise, Cloak | Family 8 / directive 6 (copy/cast through the copiable-value lens, across the 708 boundary) |

### Dependents threshold (the converse of minimality)

A `given` primitive must carry **at least two keyword dependents** —
direct `given` consumers plus composite keywords whose decompositions
compile *through* a direct consumer (equip/enchant/bestow compile through
attach). A primitive whose whole ledger is a single keyword **collapses
into that keyword as intrinsic**: a sole-dependent primitive is that
keyword's private opcode under another name. Precedent:
`cause-tagged-events` — once the Enlist record was corrected to the hooks
the CR itself names (702.154b: optional cost to attack 508.1g + linked
trigger 607.2h), its only dependent was vigilance, so the primitive was
retired and vigilance reclassified intrinsic; the decomposition survives
as a documented hypothetical (`events.md` §3; `underdetermined.md` U3,
settled-by-policy).

Dependents index — direct columns regenerable from the JSON:
`jq -r '[.keywords[] | select(.class=="composite-given")] | group_by(.given)[]
| "| \(.[0].given) | \(length) | \(map(.name)|sort|join(", ")) |"'
../keywords-classified.json`

| primitive | direct | keyword dependents (`given` field) | family beyond the direct rows |
|---|---|---|---|
| attachment-relation | 1 | Attach | eight composite keywords compile through attach (Bestow, Enchant, Equip, For Mirrodin!, Fortify, Job Select, Living Weapon, Reconfigure), plus native Aura attachment machinery (303.4) |
| cost-modification-hook | 5 | Assist, Convoke, Delve, Improvise, Waterbend | — |
| damage-result-rewrite | 4 | Infect, Lifelink, Toxic, Wither | — |
| face-down-objects | 5 | Cloak, Disguise, Manifest, Manifest Dread, Morph | — |
| progress-track | 4 | Daybound, Max Speed, Nightbound, Start Your Engines! | — |

## Intrinsic table (24)

These need a native opcode. 9 abilities + 15 actions. The action set *is*
the primitive event basis (cast/counter/destroy/exile/sacrifice/tap/… are
the verbs other rules hang machinery on).

| name | kind | rule | machinery it owns | cites |
|---|---|---|---|---|
| Banding | ability | 702.22 | Rewrites attacker declaration (band formation, shared blocking) and reassigns who chooses combat-damage division (702.22j/k are explicit exceptions to 510.1c/d). | 702.22c, 702.22h, 702.22j, 510.1c |
| Deathtouch | ability | 702.2 | Prospective lethality: 702.2c treats nonzero combat damage from the source as lethal when determining excess (trample 702.19b, excess-damage effects 120.4a); dedicated SBA 704.5h. | 702.2b, 702.2c, 120.4a, 704.5h |
| Double Strike | ability | 702.4 | Forces a first-strike combat-damage step *plus* a regular step (510), altering phase structure. | 702.4a, 702.4b, 510.4 |
| First Strike | ability | 702.7 | Splits combat damage into a first-strike step and a regular step (510) when present. | 702.7a, 702.7b, 510.4 |
| Trample | ability | 702.19 | Modifies prospective assignment (702.19a–b): lethal to every blocker first, then excess may go to the player, planeswalker, or battle attacked (702.19b). | 702.19a, 702.19b, 510.1c |
| Vigilance | ability | 702.20 | Dedicated rules text inside attack declaration: a "static ability that modifies the rules for the declare attackers step" (702.20a) exempting the creature from 508.1f's attack-tap (702.20b) — same justification shape as trample's 702.19a–b (dedicated text modifying 510.1c). Hypothetical decomposition: null-replacement on tap(cause: attack-declaration), retired with the sole-dependent `cause-tagged-events` primitive (dependents threshold; `events.md` §3). | 702.20a, 702.20b, 508.1f |
| Companion | ability | 702.139 | Functions outside the game + a dedicated special action (116.2g) to move the card from outside the game into hand. | 702.139a, 116.2g, 103.2b |
| Mutate | ability | 702.140 | Merges the spell into an existing permanent without it entering (702.140c, 730.2b–c); the merged permanent keeps its identity and takes the topmost component's characteristics (730.2a, 702.140e). | 702.140a, 702.140c, 730.2, 730.2b |
| Phasing | ability | 702.26 | Edits the untap step (phase out/in turn-based action) and adds the phased-out status (treated as not existing without changing zones). | 702.26a, 702.26b, 702.26d |
| Activate | action | 701.2 | Put an activated ability on the stack and pay costs (601-structured) — the native put-on-stack opcode. | 701.2a |
| Cast | action | 701.5 | The casting-pipeline event (601): take from zone, put on stack, pay costs. | 701.5a, 701.5b |
| Counter | action | 701.6 | Cancel/remove-from-stack: doesn't resolve, no effects, goes to graveyard, no cost refund. | 701.6a, 701.6b |
| Create | action | 701.7 | Instantiate tokens with token-specific replacement-ordering (701.7b) distinct from generic ETB. | 701.7a, 701.7b |
| Destroy | action | 701.8 | Battlefield→graveyard destruction event that regeneration replaces and lethal-damage/deathtouch SBAs invoke. | 701.8a, 701.8b, 701.8c |
| Discard | action | 701.9 | Hand→graveyard event with chooser/random modes and hidden-zone / illegal-cost-rewind nuances. | 701.9a, 701.9b, 701.9c |
| Exile | action | 701.13 | Primitive move into the exile zone; the basis-level relocation destination. | 701.13a |
| Play | action | 701.18 | Land-play special action (116): onto battlefield without the stack under once-per-turn/main-phase/empty-stack timing; dispatches to cast otherwise. | 701.18a, 701.18b, 116.1, 116.2 |
| Reveal | action | 701.20 | Show-to-all with revealed-state lifetime, no zone change; reordered revealed cards become new objects. | 701.20a, 701.20b, 701.20d |
| Sacrifice | action | 701.21 | Controller-only battlefield→graveyard that is *not* destruction (bypasses regeneration). | 701.21a |
| Search | action | 701.23 | Look at all cards in a zone (even hidden) + find-matching, with optional-find / search-replacement / library-searched triggers. | 701.23a, 701.23b, 701.23f |
| Shuffle | action | 701.24 | Randomize a library (excludes searched-then-found cards; fires shuffle triggers even on empty/single-card libraries). | 701.24a, 701.24b, 701.24e |
| Tap | action | 701.26 | Flip untapped→tapped status (only untapped can be tapped) — native boolean the engine tracks. | 701.26a |
| Transform | action | 701.27 | Face-flip on a DFC/DFT, distinct from turn-face-up/down, once-per-stack guard + "transformed permanent" status. | 701.27a, 701.27b, 701.27f, 701.27g |
| Untap | action | 701.26 | Flip tapped→untapped (only tapped can be untapped) — complement of Tap. | 701.26b |

**Mutate versus meld.** Both make one permanent represented by more than one card (701.42a, 702.140c), and their leave-the-battlefield rules run in parallel (712.21–712.21d for melded permanents, 730.3–730.3d for merged ones), so one multi-card representation can serve both (engine inference). That shared representation is not why Mutate is intrinsic. Meld is a zone move: both cards are put onto the battlefield as a single permanent (701.42a, 712.14c), a new object (400.7) with the combined back face's characteristics (712.8g). Mutate's own machinery is the merge, and only mutate merges (730.1). The mutating spell "doesn't enter the battlefield" (702.140c). It joins a permanent that "is the same object that it was before" (730.2b–c), which takes the topmost component's characteristics as a copiable effect (730.2a) and every component's abilities (702.140e). A primitive covering the merge would have Mutate as its sole dependent, so the dependents threshold keeps Mutate intrinsic. A melded permanent is not a merged one; 701.27g names them as two kinds.

## Composite-given table (19)

Each decomposes once its `given` primitive exists; grouped by primitive.

| name | given | decomposition | cites |
|---|---|---|---|
| Lifelink | damage-result-rewrite | Augment the damage result: controller gains that much life in addition; CR hardcodes 120.3f. | 702.15b, 120.3f |
| Toxic | damage-result-rewrite | Augment combat damage to a player with poison counters = toxic value (120.3g). | 702.164c, 120.3g |
| Wither | damage-result-rewrite | Substitute: damage to a creature becomes that many -1/-1 counters instead of being marked (120.3d). | 702.80a, 120.3d, 302.7 |
| Infect | damage-result-rewrite | Substitute: damage to a player → poison; damage to a creature → -1/-1 counters (120.3b/120.3d). | 702.90b, 702.90c, 120.3b, 120.3d |
| Daybound | progress-track | Statics reading the day/night designation (731.1), which the untap-step turn-based action (731.2) and other effects set in either direction: enter transformed if night, transform as night falls, can't otherwise transform. | 702.145b, 702.145c, 731.1, 731.2 |
| Nightbound | progress-track | Statics on the day/night track: transform as day breaks, can't otherwise transform. | 702.145e, 702.145f, 731.1 |
| Max Speed | progress-track | Conditional static: "as long as your speed is 4, this has [ability]" — gated on the speed track. | 702.178a, 702.178b |
| Start Your Engines! | progress-track | SBA sets speed to 1 + inherent trigger raising speed when opponents lose life — initialize/advance the speed track. | 702.179a, 702.179d |
| Attach | attachment-relation | Move an Aura/Equipment/Fortification into the attached-to relation with a legal host (no-op/legality guards + new timestamp). | 701.3a, 701.3b, 701.3c |
| Delve | cost-modification-hook | Per generic mana in the total cost, may exile a graveyard card instead (neither additional nor alternative cost). | 702.66a, 702.66b |
| Convoke | cost-modification-hook | Per colored/generic mana, may tap a creature of that color (any for generic); CR: not additional/alternative (702.51b). | 702.51a, 702.51b |
| Improvise | cost-modification-hook | Per generic mana, may tap an untapped artifact instead; not additional/alternative (702.126b). | 702.126a, 702.126b |
| Assist | cost-modification-hook | Lets a chosen player pay any amount of the generic-mana component before you (601.2g–h) — pay-substitution by who pays. | 702.132a, 601.2g, 601.2h |
| Waterbend | cost-modification-hook | Scope (b), per component: pay [cost]; per generic mana in it, may tap an untapped artifact or creature rather than pay that mana (701.67a), only for the waterbend cost's own generic mana (701.67b), wherever that cost is paid: casting or activating (including an alternative cost), a resolution "unless" cost (118.12a), or inside ward (702.21a). | 701.67a, 701.67b, 701.67c, 118.12a, 702.21a |
| Morph | face-down-objects | Alt-cost face-down cast (708) as a 2/2 + special action (116) to turn face up. | 702.37a, 702.37c, 702.37e, 708.2a |
| Disguise | face-down-objects | Alt-cost face-down cast (708) as a 2/2 ward {2} for {3} + special action to turn face up for the disguise cost. | 702.168a, 702.168d, 708.2a |
| Cloak | face-down-objects | Like manifest but the face-down 2/2 has ward {2}; special action (116) to turn face up. | 701.58a, 701.58b, 701.58h, 708.2a |
| Manifest | face-down-objects | Put a card onto the battlefield as a 2/2 face-down creature (708) + special action to turn it up for its mana cost. | 701.40a, 701.40b, 701.40h, 708.2a |
| Manifest Dread | face-down-objects | Look at top two, manifest one (708), graveyard the rest — built on manifest. | 701.62a, 701.62b, 701.40a, 708.2a |

## Marker (1)

| name | rule | how | cites |
|---|---|---|---|
| Reach | 702.17 | No function of its own; meaning lives entirely in flying's blocking predicate (702.9b), which lets reach creatures block fliers. | 702.17b, 702.9b |

## Composite highlights

The full 222-row composite enumeration lives in
`../keywords-classified.json`. Fifteen instructive ones:

| name | rule | decomposition | cites |
|---|---|---|---|
| Flying | 702.9 | Declare-blockers legality predicate: can't be blocked except by flying/reach creatures. | 702.9b |
| Ward | 702.21 | Triggered toll: on becoming the target of an opponent's spell/ability, counter unless they pay the cost. | 702.21a |
| Scry | 701.22 | Look at top N, distribute between top and bottom (any order); scry-0 no-op; APNAP simultaneity. | 701.22a, 701.22b, 701.22c |
| Convert | 701.28 | Composite over Transform: the face-flip under another name. 701.27a–f apply to it "just as they apply to transforming" (701.28a), so the once-per-stack guard counts either action (701.27f, 701.28e), "can't transform" stops it (701.28f), and "transforms into" triggers see it (701.27e). Official rulings (Transformers cards, 2022-10-14) go further: "Any triggered ability of another card that triggers whenever a permanent transforms will also trigger whenever a permanent converts," and a "transform" instruction converts a card with convert. Every other rule that names convert treats it the same as transform (e.g. 712.9, 712.10, 712.11a, 712.14a, 712.18, 712.20, 730.2i, 613.7g). Engine inference: a name tag on the Transform event is enough, because no rule or Oracle text needs a convert-only event. | 701.28a, 701.28b, 701.28e, 701.28f, 701.27e |
| Haste | 702.10 | Lifts the 302.6/508.1a summoning-sickness restrictions (may attack + use {T}/{Q} abilities). | 702.10b, 702.10c, 302.6 |
| Flash | 702.8 | Timing permission: "play any time you could cast an instant" — a static editing when the cast/play action is legal. | 702.8a |
| Cycling | 702.29 | Activated ability from hand: "[Cost], Discard this card: Draw a card." | 702.29a |
| Kicker | 702.33 | Optional additional cost at cast + a "was kicked" memory linked abilities read. | 702.33a, 702.33d, 702.33e |
| Regenerate | 701.19 | CR itself defines it as a destruction-*replacement* (614.8): next destroy → remove marked damage, tap, remove from combat. Replacements are in the basis. | 701.19a, 701.19b, 614.8 |
| Indestructible | 702.12 | A static "can't be destroyed" (614.17 "can't" reading): nulls the destroy action for this permanent and exempts it from the lethal-damage SBA (704.5g) — a static rule-mod, not its own prospective machinery. | 702.12a, 702.12b, 704.5g, 614.17 |
| Goad | 701.15 | Applies the "goaded" designation = attack requirement (must attack if able) + direction restriction (a player other than the goader). | 701.15a, 701.15b, 701.15c |
| Proliferate | 701.34 | Choose any number of permanents/players with a counter, give each one more of each kind it has (2HG poison sharing). | 701.34a, 701.34b |
| Protection | 702.16 | Bundle of restrictions/prevention: can't be targeted/enchanted/equipped/fortified (with SBA detach), damage prevented, can't be blocked — all by qualified sources. | 702.16b, 702.16c, 702.16d, 702.16e, 702.16f |
| Recruit | 701.70 | Draw, discard, then conditionally create a 1/1 white Human Soldier creature token if the discarded card was nonland. | 701.70a |
| Storied | 702.195 | Threshold-gated static that grants a permanent player marker, then reapplies continuous effects before checking trigger conditions. | 702.195a, 702.195b, 702.195c |

## Keyword variants

The JSON has one row per keyword in the CR's keyword-ability and keyword-action lists; a variant the CR defines inside its base's subsection has no row and is classified with its base. That inheritance is a rubric convention, not a CR rule: a variant takes its base row's class and `given` (trample over planeswalkers is intrinsic with trample; megamorph is face-down-objects with morph). The sibling keyword abilities that share the partner section (partner-[text], partner with, choose a Background, and Doctor's companion; 702.124a, 702.124h–m) likewise take that section's row. Whether an effect that names the base finds the variant is settled rule by rule. One rule covers grants: an effect that grants a list of keywords via "the same is true for" grants "each appropriate variant and variable of that keyword" (702.1c). Below are all the forms the CR calls a variant, a special form, or a kind of its base:

| form | base | what references to the base see | cites |
|---|---|---|---|
| typecycling | cycling | It is cycling. Cycle triggers, cycling prohibitions, cycling-cost changes, and "a card with cycling" all reach it. | 702.29e, 702.29f |
| hexproof from [quality] | hexproof | It is hexproof. Losing hexproof loses it, "as though it didn't have hexproof" reaches it, and "a card with hexproof" finds it. | 702.11d, 702.11e |
| multikicker | kicker | "A multikicker cost is a kicker cost"; the spell may be kicked multiple times. | 702.33c, 702.33d |
| sticker kicker | kicker | It "represents a kicker ability" plus an additional cost if kicked. | 702.33h |
| megamorph | morph | "A megamorph cost is a morph cost." | 702.37b |
| connive N | connive | A permanent "connives" after either process. | 701.50d, 701.50f |
| bands with other | banding | Lost when banding is lost, but a creature with only bands with other is "without banding" for band formation. | 702.22b, 702.22c |
| partner-[text], partner with [name], choose a Background, Doctor's companion | partner | Distinct, and never combined. An unqualified "partner" means partner, partner-[text] and partner with [name] only. | 702.124a, 702.124f, 702.124n |
| equip planeswalker | equip | "a variant" only | 702.6e |
| protection from everything; protection from [a player] | protection | "a variant" only | 702.16j, 702.16k |
| trample over planeswalkers | trample | Named alongside trample where the CR wants both (702.19d), distinguished from it in 702.19f, and counted separately for redundancy (702.19g; Thrasta ruling: both "can both apply"). Whether "trample" references find it is unstated. | 702.19c, 702.19d, 702.19f, 702.19g |
| commander ninjutsu | ninjutsu | "a variant" only | 702.49d |
| bloodthirst X | bloodthirst | "a variant" only | 702.54b |
| devour [quality] | devour | "a variant" only | 702.82c |
| double agenda | hidden agenda | "a variant" only | 702.106f |
| emerge from [quality] | emerge | "a variant" only | 702.119b |
| venture into [quality] | venture into the dungeon | "a variant" only. Dungeon cards enter the game only through "the venture into the dungeon keyword action" (309.2, 309.2d), which implies that this variant counts as one (inference). | 701.49d, 309.2, 309.2d |

For the "a variant" only rows, the CR doesn't say whether an effect that names the base finds the variant, and current Oracle text poses the question: "Ninjutsu abilities you activate cost {1} less to activate" against commander ninjutsu; "Equip abilities you activate cost {1} less to activate" against equip planeswalker; "lose trample and can't have or gain trample" against trample over planeswalkers; and "can't venture into the dungeon more than once each turn" against venturing into Undercity. Each is an engine choice; see `underdetermined.md` UD-29.

## Keyword abilities without a 702 entry

The CR calls five frame-printed forms keyword abilities but gives none of them its own 702 entry, and the JSON has no rows for them. Each composes from the basis. The class column is this doc's classification, not the CR's.

| form | CR | represents | class |
|---|---|---|---|
| level symbol (`LEVEL N1-N2`, `LEVEL N3+`) | 711.2, 107.8 | A static: base P/T and abilities while the number of level counters is in range (711.2a–b). | composite |
| chapter symbol (`I -`) | 714.2, 107.15 | A triggered chapter ability: when lore counters are put on and the count was below N and became at least N (714.2b). | composite |
| class level bar (`{cost}: Level N`) | 716.2, 107.16 | An activated ability (level becomes N; only at level N-1, as a sorcery) and a static (abilities while level is N or greater) (716.2a). | composite |
| station symbol (`N+ \|`) | 702.184b, 721.2 | A static: abilities, and creature with base P/T where one is printed, while there are N or more charge counters (721.2a–b). | composite |
| to solve (`To solve -`) | 719.3, 719.3a | A triggered ability: at your end step, if [condition] holds and the Case is unsolved, it becomes solved (719.3a; the solved designation is 719.3b). | composite |

The abilities that accompany them have their own rows: Level Up (702.87), Station (702.184), Solved (702.169).

## Counts

| class | count |
|---|---|
| intrinsic | 24 (9 ability, 15 action) |
| composite | 222 (171 ability, 51 action) |
| composite-given | 19 (14 ability, 5 action) |
| marker | 1 |
| **total** | **266** (195 ability, 71 action) |

`core_referenced` (named in CR outside its own 70x section, by the scan policy
above): **94** of 266 rows are true, 172 false. Per row in the JSON. All 24
intrinsic rows and the marker are core-referenced (deathtouch→120.4a/701.8b/704.5h;
trample→122.1b/111.10k), as are 12 of the 19 composite-given rows; 57 of the
222 composite rows are, so most composite rows are self-contained.

## Maintenance

After a CR refresh, any newly printed keyword lands **unclassified** —
classify it against `rubric_version` (try to decompose to statics + triggers
+ replacements + permissions/restrictions + action-sequences + the five
`given` primitives before declaring it intrinsic). Then **re-verify the
intrinsic set is minimal**: attack each intrinsic with a decomposition
attempt; if a new primitive would collapse several into composite-given,
add the primitive to the `given` vocabulary rather than minting intrinsics.
Apply the dependents threshold in reverse, too: a primitive left holding a
single keyword and no recorded family beyond it collapses back into its
keyword as intrinsic (precedent: cause-tagged-events → vigilance), and the
dependents index above is regenerated from the JSON in the same change.
Run `scripts/cite check` (it now also guards the JSON's cites) and
`fish tests/test_skill_scripts.fish` after edits (the harness lints that
every composite-given `how` names its `given` primitive).

A new keyword also touches these per-keyword update points: in the JSON,
`meta.generated_from` and the record count inside `meta.ident_rule`; in
`tests/test_skill_scripts.fish`, the record-count pins (`keyword count covers
both lists`, `idents: all N records carry a string ident`, `idents: all N
unique`); and in this doc the header date, the intro's row and composite
counts, the table headings, the Counts table, and the `core_referenced`
line. Regenerate that line by re-running the `core_referenced` scan for every
row, not just the new one: a new keyword can flip older rows by naming them
(701.71a, Empower Jace, names Surveil).
