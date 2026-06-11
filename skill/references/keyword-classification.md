# Keyword Classification — Intrinsic / Composite / Marker

*Synthesized from the Comprehensive Rules effective 2026-04-17
(`data/rules/cr.json`). Orientation only — verify load-bearing specifics
with `scripts/rule` before citing. Run `scripts/check-citations` after CR
refreshes.*

Every keyword ability (CR 702) and keyword action (CR 701) is classified by
**what an engine has to build for it**. The full per-keyword data (all 260
rows, `how` rationale, cites, `core_referenced` flag) lives in
`../keywords-classified.json`; this doc holds the rubric, the engine
primitive basis, and the closed-class tables. The JSON is the authority for
the 212-row composite enumeration — only highlights appear below.

## Rubric (rubric_version 1)

Four classes, by what machinery the keyword forces:

- **intrinsic** — needs its own engine opcode. It changes *prospective*
  machinery (combat-damage assignment legality, lethality computation,
  priority/turn structure, the casting pipeline, native zone/status events)
  in a way no composition of statics + triggers + replacements + permissions
  + restrictions + action-sequences reproduces. Exemplars: **trample**
  (must assign lethal to blockers first, then may assign excess to the
  player — the assignment rules 510.1c–d themselves, 702.19b); **deathtouch**
  (510.1c reads any nonzero damage from the source as lethal at *assignment
  time*, 702.2c, plus the dedicated SBA 704.5h).
- **composite** — compiles to the primitive basis already in the engine.
  Exemplars: **flying** (a declare-blockers legality predicate: can't be
  blocked except by flying/reach, 702.9b); **ward** (a triggered toll:
  trigger + counter-unless-pay, 702.21a); **scry** (a look/move action
  sequence, 701.22a).
- **composite-given(P)** — decomposes *iff* the basis includes a named
  primitive `P` (recorded in the `given` field). Exemplars: **vigilance** =
  null-replacement on the "tapped because declared as an attacker" event
  *given* cause-tagged events; CR instead hardcodes the exemption in 508.1f
  (702.20b). **lifelink** = augment the damage *result* (gain that much life
  in addition) *given* the damage-result-rewrite stage; CR hardcodes it as
  120.3f (702.15b). Without `P`, these would each demand their own opcode;
  sharing `P` keeps the intrinsic set minimal.
- **marker** — no function of its own; meaning lives entirely in *other*
  rules' predicates that reference it. Type specimen: **reach** (only
  flying's blocking predicate 702.9b gives it meaning, 702.17b).

Orthogonal flag **`core_referenced`** (data in the JSON): true iff the
keyword is named in CR rules *outside* its own 70x.x section.

## Primitive basis (`given` vocabulary)

The composite-given class decomposes against exactly six primitives. Adding
any one of these to the engine collapses a cluster of would-be intrinsics
into compositions. Each cross-refs the relevant `generalizations.md`
directive/family.

| primitive | one-line definition | keywords needing it | generalizations cross-ref |
|---|---|---|---|
| `cause-tagged-events` | Events carry a tag for *what caused them* ("tapped because declared as an attacker"), so statics/replacements match on cause instead of the CR hardcoding the case. | Vigilance, Enlist | **defining home: `events.md` §3** (cause = a *(verb, agency, agent)* triple there); directive 2 (role-vs-identity parameters) |
| `damage-result-rewrite` | A stage that rewrites the *result* of a damage event (substitute or augment what damage does), not its amount — the slot CR 120.3 hardcodes. | Lifelink, Wither, Infect, Toxic | Family 11 / directive 3 (typed transform algebra: substitute/augment) |
| `progress-track` | A game-maintained monotonic value with thresholds (day/night, speed), advanced by turn-based actions or inherent triggers; statics read it. | Daybound, Nightbound, Max Speed, Start Your Engines! | Family 4 / directive 4 (one ProgressTrack type) |
| `attachment-relation` | A first-class `attached_to` edge to a legal host (object or player) with legality predicate and violation policy. | Attach | Family 5 / directive 2 (attach carries host+predicate+policy) |
| `cost-modification-hook` | A permission that edits how generic/colored mana of an already-determined total cost is paid (601.2f–h) — *neither* additional *nor* alternative cost. | Delve, Convoke, Improvise, Assist, Waterbend | **defining home: `costs.md` §4** (payment-stage substitution at the 601.2f–h lock); directive 10 (mana payment predicates) |
| `face-down-objects` | A primitive for objects existing face down (708): put/cast face down as a 2/2, secret-identity memory, special action to turn face up. | Morph, Manifest, Manifest Dread, Disguise, Cloak, Foretell, Hidden Agenda | Family 8 / directive 6 (copy/cast through the copiable-value lens, across the 708 boundary) |

## Intrinsic table (24)

These need a native opcode. 8 abilities + 16 actions. The action set *is*
the primitive event basis (cast/counter/destroy/exile/sacrifice/tap/… are
the verbs other rules hang machinery on).

| name | kind | rule | machinery it owns | cites |
|---|---|---|---|---|
| Banding | ability | 702.22 | Rewrites attacker declaration (band formation, shared blocking) and reassigns who chooses combat-damage division (702.22j/k are explicit exceptions to 510.1c/d). | 702.22c, 702.22h, 702.22j, 510.1c |
| Deathtouch | ability | 702.2 | Prospective lethality: 510.1c treats nonzero combat damage from the source as lethal at assignment time (702.2c); dedicated SBA 704.5h. | 702.2b, 702.2c, 510.1c, 704.5h |
| Double Strike | ability | 702.4 | Forces a first-strike combat-damage step *plus* a regular step (510), altering phase structure. | 702.4a, 702.4b, 510.1 |
| First Strike | ability | 702.7 | Splits combat damage into a first-strike step and a regular step (510) when present. | 702.7a, 702.7b, 510.1 |
| Trample | ability | 702.19 | Modifies prospective assignment (510.1c–d): lethal to blockers first, then excess may go to the player/planeswalker. | 702.19a, 702.19b, 510.1c, 510.1d |
| Companion | ability | 702.139 | Functions outside the game + a dedicated special action (116.2g) to move the card from outside the game into hand. | 702.139a, 116.2g, 103.2b |
| Mutate | ability | 702.140 | Merges the spell with its target into one object represented by multiple cards (rule 730) — non-standard object machinery. | 702.140a, 702.140c, 730.2 |
| Phasing | ability | 702.26 | Edits the untap step (phase out/in turn-based action) and adds the phased-out status (treated as not existing without changing zones). | 702.26a, 702.26b, 702.26d |
| Activate | action | 701.2 | Put an activated ability on the stack and pay costs (601-structured) — the native put-on-stack opcode. | 701.2a |
| Cast | action | 701.5 | The casting-pipeline event (601): take from zone, put on stack, pay costs. | 701.5a, 701.5b |
| Convert | action | 701.28 | Face-flip primitive (follows 701.27a–f) with once-per-stack guard; can't-transform blocks it. | 701.28a, 701.28b, 701.28e, 701.28f |
| Counter | action | 701.6 | Cancel/remove-from-stack: doesn't resolve, no effects, goes to graveyard, no cost refund. | 701.6a, 701.6b |
| Create | action | 701.7 | Instantiate tokens with token-specific replacement-ordering (701.7b) distinct from generic ETB. | 701.7a, 701.7b |
| Destroy | action | 701.8 | Battlefield→graveyard destruction event that regeneration replaces and lethal-damage/deathtouch SBAs invoke. | 701.8a, 701.8b, 701.8c |
| Discard | action | 701.9 | Hand→graveyard event with chooser/random modes and hidden-zone / illegal-cost-rewind nuances. | 701.9a, 701.9b, 701.9c |
| Exile | action | 701.13 | Primitive move into the exile zone; the basis-level relocation destination. | 701.13a |
| Play | action | 701.18 | Land-play special action (116): onto battlefield without the stack under once-per-turn/main-phase/empty-stack timing; dispatches to cast otherwise. | 701.18a, 701.18b, 116.1, 116.2 |
| Reveal | action | 701.20 | Show-to-all with revealed-state lifetime, no zone change; reordered revealed cards become new objects. | 701.20a, 701.20b, 701.20d |
| Sacrifice | action | 701.21 | Controller-only battlefield→graveyard that is *not* destruction (bypasses regeneration). | 701.21a |
| Search | action | 701.23 | Look at all cards in a zone (even hidden) + find-matching, with optional-find / search-replacement / library-searched triggers. | 701.23a, 701.23b, 701.23f |
| Shuffle | action | 701.24 | Randomize a library (excludes searched-then-found cards; fires shuffle triggers even on empty/single-card libraries). | 701.24a, 701.24b, 701.24g |
| Tap | action | 701.26 | Flip untapped→tapped status (only untapped can be tapped) — native boolean the engine tracks. | 701.26a |
| Transform | action | 701.27 | Face-flip on a DFC/DFT, distinct from turn-face-up/down, once-per-stack guard + "transformed permanent" status. | 701.27a, 701.27b, 701.27f, 701.27g |
| Untap | action | 701.26 | Flip tapped→untapped (only tapped can be untapped) — complement of Tap. | 701.26b |

## Composite-given table (23)

Each decomposes once its `given` primitive exists; grouped by primitive.

| name | given | decomposition | cites |
|---|---|---|---|
| Vigilance | cause-tagged-events | Null-replacement on the "tapped because declared attacker" event; CR hardcodes the exemption in 508.1f. | 702.20b, 508.1f |
| Enlist | cause-tagged-events | Optional cost-to-attack hook (508.1g) tapping an eligible creature + linked trigger granting +X/+0. | 702.154a, 702.154b, 508.1g |
| Lifelink | damage-result-rewrite | Augment the damage result: controller gains that much life in addition; CR hardcodes 120.3f. | 702.15b, 120.3f |
| Toxic | damage-result-rewrite | Augment combat damage to a player with poison counters = toxic value (120.3g). | 702.164c, 120.3g |
| Wither | damage-result-rewrite | Substitute: damage to a creature becomes that many -1/-1 counters instead of being marked (120.3d). | 702.80a, 120.3d, 302.7 |
| Infect | damage-result-rewrite | Substitute: damage to a player → poison; damage to a creature → -1/-1 counters (120.3b/120.3d). | 702.90b, 702.90c, 120.3b, 120.3d |
| Daybound | progress-track | Statics reading the day/night track (rule 731): enter transformed if night, transform as night falls, can't otherwise transform. | 702.145b, 702.145c, 731.1 |
| Nightbound | progress-track | Statics on the day/night track: transform as day breaks, can't otherwise transform. | 702.145e, 702.145f, 731.1 |
| Max Speed | progress-track | Conditional static: "as long as your speed is 4, this has [ability]" — gated on the speed track. | 702.178a, 702.178b |
| Start Your Engines! | progress-track | SBA sets speed to 1 + inherent trigger raising speed when opponents lose life — initialize/advance the speed track. | 702.179a, 702.179d |
| Attach | attachment-relation | Move an Aura/Equipment/Fortification into the attached-to relation with a legal host (no-op/legality guards + new timestamp). | 701.3a, 701.3b, 701.3c |
| Delve | cost-modification-hook | Per generic mana in the total cost, may exile a graveyard card instead (neither additional nor alternative cost). | 702.66a, 702.66b |
| Convoke | cost-modification-hook | Per colored/generic mana, may tap a creature of that color (any for generic); CR: not additional/alternative (702.51b). | 702.51a, 702.51b |
| Improvise | cost-modification-hook | Per generic mana, may tap an untapped artifact instead; not additional/alternative (702.126b). | 702.126a, 702.126b |
| Assist | cost-modification-hook | Lets a chosen player pay any amount of the generic-mana component before you (601.2g–h) — pay-substitution by who pays. | 702.132a, 601.2g, 601.2h |
| Waterbend | cost-modification-hook | Pay [cost]; per generic mana in it, may tap an artifact/creature instead (701.67b scopes it to the waterbend cost). | 701.67a, 701.67b, 701.67c |
| Morph | face-down-objects | Alt-cost face-down cast (708) as a 2/2 + special action (116) to turn face up. | 702.37a, 702.37c, 702.37e, 708.2a |
| Disguise | face-down-objects | Alt-cost face-down cast (708) as a 2/2 ward {2} for {3} + special action to turn face up for the disguise cost. | 702.168a, 702.168d, 708.2a |
| Cloak | face-down-objects | Like manifest but the face-down 2/2 has ward {2}; special action (116) to turn face up. | 701.58a, 701.58b, 701.58h, 708.2a |
| Manifest | face-down-objects | Put a card onto the battlefield as a 2/2 face-down creature (708) + special action to turn it up for its mana cost. | 701.40a, 701.40b, 701.40h, 708.2a |
| Manifest Dread | face-down-objects | Look at top two, manifest one (708), graveyard the rest — built on manifest. | 701.62a, 701.62b, 701.40a, 708.2a |
| Foretell | face-down-objects | Special action (116.2h): pay {2}, exile the card face down (708) + alt foretell cost to cast it later. | 702.143a, 702.143b, 116.2h, 708.5 |
| Hidden Agenda | face-down-objects | Conspiracy enters the command zone face down (708) with a secret noted name (linked memory); special action (116.2j) flips it up. | 702.106a, 702.106c, 702.106d, 708.5 |

## Marker (1)

| name | rule | how | cites |
|---|---|---|---|
| Reach | 702.17 | No function of its own; meaning lives entirely in flying's blocking predicate (702.9b), which lets reach creatures block fliers. | 702.17b, 702.9b |

## Composite highlights

The full 212-row composite enumeration lives in
`../keywords-classified.json`. Twelve instructive ones:

| name | rule | decomposition | cites |
|---|---|---|---|
| Flying | 702.9 | Declare-blockers legality predicate: can't be blocked except by flying/reach creatures. | 702.9b |
| Ward | 702.21 | Triggered toll: on becoming the target of an opponent's spell/ability, counter unless they pay the cost. | 702.21a |
| Scry | 701.22 | Look at top N, distribute between top and bottom (any order); scry-0 no-op; APNAP simultaneity. | 701.22a, 701.22b, 701.22c |
| Haste | 702.10 | Lifts the 302.6/508.1a summoning-sickness restrictions (may attack + use {T}/{Q} abilities). | 702.10b, 702.10c, 302.6 |
| Flash | 702.8 | Timing permission: "play any time you could cast an instant" — a static editing when the cast/play action is legal. | 702.8a |
| Cycling | 702.29 | Activated ability from hand: "[Cost], Discard this card: Draw a card." | 702.29a |
| Kicker | 702.33 | Optional additional cost at cast + a "was kicked" memory linked abilities read. | 702.33a, 702.33d, 702.33e |
| Regenerate | 701.19 | CR itself defines it as a destruction-*replacement* (614.8): next destroy → remove marked damage, tap, remove from combat. Replacements are in the basis. | 701.19a, 701.19b, 614.8 |
| Indestructible | 702.12 | A static "can't be destroyed" (614.17 "can't" reading): nulls the destroy action for this permanent and exempts it from the lethal-damage SBA (704.5g) — a static rule-mod, not its own prospective machinery. | 702.12a, 702.12b, 704.5g, 614.17 |
| Goad | 701.15 | Applies the "goaded" designation = attack requirement (must attack if able) + direction restriction (a player other than the goader). | 701.15a, 701.15b, 701.15c |
| Proliferate | 701.34 | Choose any number of permanents/players with a counter, give each one more of each kind it has (2HG poison sharing). | 701.34a, 701.34b |
| Protection | 702.16 | Bundle of restrictions/prevention: can't be targeted/enchanted/equipped (with SBA detach), damage prevented, can't be blocked — all by qualified sources. | 702.16b, 702.16c, 702.16e, 702.16f |

## Counts

| class | count |
|---|---|
| intrinsic | 24 (8 ability, 16 action) |
| composite | 212 (165 ability, 47 action) |
| composite-given | 23 |
| marker | 1 |
| **total** | **260** (192 ability, 68 action) |

`core_referenced` (named in CR outside its own 70x section): **64** of 260
rows are true, 196 false. Per row in the JSON. The 16 intrinsic actions and
several intrinsic abilities (deathtouch→510.1c/704.5h, trample→510.1, etc.)
are core-referenced; most composite *abilities* are self-contained.

## Maintenance

After a CR refresh, any newly printed keyword lands **unclassified** —
classify it against `rubric_version` (try to decompose to statics + triggers
+ replacements + permissions/restrictions + action-sequences + the six
`given` primitives before declaring it intrinsic). Then **re-verify the
intrinsic set is minimal**: attack each intrinsic with a decomposition
attempt; if a new primitive would collapse several into composite-given,
add the primitive to the `given` vocabulary rather than minting intrinsics.
Run `scripts/check-citations` (it now also guards the JSON's cites) and
`fish tests/test_skill_scripts.fish` after edits.
