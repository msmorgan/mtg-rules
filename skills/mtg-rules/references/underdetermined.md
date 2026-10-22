# Underdetermined — The Engine-Choice Registry

*Synthesized from the Comprehensive Rules effective 2026-09-25
(`data/rules/cr.json`).*

Points where the CR underdetermines semantics: a rules-correct engine must
make a choice the rules don't make for it, and that choice belongs in a
documented decision — this is the engine's ADR seed list. Admission is
adversarial: an entry is admitted only after an attempt to **refute** it
(hunting the CR for a settling rule) has failed; candidates refuted during
the hunt land in **Settled** below with the resolving cite, never silently
deleted. Distinguish these from `generalizations.md`'s "empty cells": an
empty cell is *design space* — no rule or card instantiates the
combination, so nothing poses the question yet — while an entry here is a
*semantic gap* in live rules: the rules as written already pose the
question, or an engine implementing them generically must answer it now.
Entry ids are durable (`UD-NNN` — never renumbered, never reused); cite
them from other docs. Every entry line carries its category: `assumed` =
a reference doc commits to a choice; `open` = no doc commitment yet;
`representation-only` = the CR fixes observable behavior, only the
internal representation is open — still pin it; `settled` /
`settled-by-policy` entries live in the Settled section (entries retired
before the UD rename keep their original S/U ids). Look entries up with
`scripts/underdetermined <id>` (no argument lists every entry line);
`scripts/lookup` also surfaces the entry headings.

**Consumer convention** (the two-way feedback loop's skeleton): this
registry records *what the CR underdetermines*, engine-agnostically — it
never picks for you. A consumer repo records *which option it chose* in
its own ADRs, keyed by UD id (e.g. "ADR-012: UD-7 — concession lands at
event boundaries"). When a CR refresh settles an entry, the UD id is the
join key telling each consumer which ADR to revisit.

## Registry

### UD-1 — Snow-ness evaluation timing for banked mana — category: assumed

- **CR says:** {S} in a cost is payable with "one mana of any type
  produced by a snow source" (107.4h); the source of mana is the
  producing spell, or the source of the producing ability (106.3); snow
  is a supertype a permanent has or lacks (205.4g); pools empty at each
  step/phase end (106.4); and the pool durably tracks producers — mana
  Drain Power moves keeps "which permanents, spells, and/or abilities
  produced that mana" unchanged (106.13).
- **Open:** *when* snow-ness is evaluated — at add-time or at pay-time.
  107.4h's past tense ("produced by") never fixes the reading.
- **Docs assume:** snapshot at add-time — the unit carries its source's
  characteristics as of production (`mana.md` §2, §6).
- **Alternatives:** pay-time re-evaluation through a live source pointer —
  needs LKI for departed sources, lets a supertype change retroactively
  corrupt banked payments, though 106.13 shows the pool already carries
  the producer pointer. Observable only when snow-ness changes between
  production and payment within one step or phase (106.4). Live
  witnesses: Arcum's Weathervane and Thermal Flux can change a source's
  snow-ness while its mana is in the pool; no official ruling decides the
  case.

### UD-4 — Cast-from-stack object identity — category: assumed

- **CR says:** casting moves the card "from where it is to the stack"
  (601.2a); an object changing zones becomes a new object, with a closed
  exception list (400.7) that never contemplates a same-zone move; the
  one mechanism that casts mid-resolution makes a *copy* "in the same
  zone the object is in" and casts that (707.12).
- **Open:** for an object already on the stack, whether the cast's "move"
  is a zone change (new object per 400.7), a no-op (same object), and
  whether zone-change triggers see anything. The engine's generic cast
  operation must answer this even while no permission instantiates the
  stack-source cell (that cell is `generalizations.md` §1 design space;
  the identity question is not).
- **Docs assume:** launder through a copy, following 707.12's own dodge
  (`generalizations.md` §1 danger note).
- **Alternatives:** same-object no-op (preserves references; invents a
  cast that never moved); new-object-in-place (consistent with 400.7's
  spirit; needs invented semantics for "moves from a zone to itself").

### UD-6 — One undefined value (⊥) behind per-case rules — category: assumed

- **CR says:** per-case handling only — undetermined number → 0 (107.2);
  a P/T characteristic-defining ability's undetermined number → 0, "including
  inside a calculation" (208.2a, Lost Order of Jarkeld off the battlefield:
  "1 plus 0, so it's 1/1"); a gained ability's undefined X → 0 (107.3j);
  further ⊥→0 cases are a creature with no power or toughness value (208.5),
  a player with no speed (702.179f), and a Saga with no chapter abilities
  (714.2d); undefined choice → that part does nothing (607.5a); information
  about an illegal target → that part "won't happen" (608.2b); undefined mana
  type → no mana (106.5); undefined commander color identity → that part does
  nothing, referencing costs unpayable (903.4f; the cost-position outcome
  reads the same in Prototype Portal [2011-01-01]: "the value of {X} is
  undefined and can't be paid"); undefined search quality → can't find
  (701.23c); undefined attach target → an Aura stays put (from the stack it
  goes to the graveyard; a token isn't created) (303.4i), Equipment enters
  unattached, token too (301.5e; Fortifications follow, 301.6); a meld back
  face referenced outside a melded permanent "fails to determine its
  characteristics", with no stated coercion (712.4b); card discarded
  face-down into a hidden zone → *all* characteristics "considered to be
  undefined" (701.9c).
- **Open:** the general principle — what a *novel* undefined case does.
  Printed resolutions run both ways by context. A P/T CDA whose input choice
  was never made reads 0 (208.2a: "there won't be a chosen player. Its power
  and toughness will each be equal to 1 plus 0, so it's 1/1"; Sutured Ghoul
  [2011-09-22] agrees: if the CDA "can't be applied … then use 0"). This is
  not 607.5a's case, which covers only a gained ability whose linked choice
  is missing. A gained ability's undefined X reads 0 (107.3j), but its
  undefined linked choice is skipped (607.5a). Information about an illegal
  target is skipped (608.2b). Color-identity references are skipped and costs
  using them are unpayable (903.4f). What stays open is the general rule for
  a novel collision outside these contexts, including the 607.5a-scoped one
  (a gained CDA computing a number from an undefined linked choice, e.g. a
  copy effect giving a Lost Order-style CDA). UD-13
  carries a printed-card instance (a Sanctuary Blade with no color chosen).
- **Docs assume:** a single ⊥ with three outcomes — ⊥→0 in numeric
  position, ⊥→no-op in choice position, and ⊥→part-does-not-happen for
  illegal-target information (608.2b) (`queries.md` §4, §7). These leave
  out the cost-position "unpayable" outcome (903.4f).
- **Alternatives:** keep the per-case rules unrelated (no extrapolation
  power). On collisions, weigh 208.2a/107.3j (zero) against
  607.5a/608.2b/903.4f (skip or unpayable). Zero by default: 903.4f needed a
  dedicated rule precisely because 107.2 would otherwise coerce to 0, so
  skips exist only where printed, and the Lost Order example favors 0 in
  numeric position. Skip by default: 607.5a, 608.2b and 903.4f all skip, but
  a skip reading plus 208.5 would give 0/0 where 208.2a prints 1/1. Pick one.

### UD-7 — Concession granularity — category: open

- **CR says:** "A player can concede the game at any time"; they leave
  immediately and lose (104.3a), even when controlled by another player
  (405.6g, 723.6). Concession doesn't use the stack (405.6g), happens
  immediately, and a controlling player can't block it (723.6). Leave-game
  cleanup happens "as soon as the player leaves the game," explicitly *not*
  a state-based action (800.4a). In a two-player game the remaining player
  wins immediately, overriding can't-win effects (104.2a), and the game ends
  (104.1). 800.4 applies only to multiplayer games, and it defines
  continuation after a departure: the leaver's non-card stack objects cease
  to exist and priority passes to the next player in turn order (800.4a);
  nothing can change to the leaver's control or be put onto the battlefield
  or stack under it (800.4b); a cost the leaver must pay "is not paid"
  (800.4f); another player makes the choices the leaver was required to make
  (800.4g, 800.4h); the turn "continues to its completion without an active
  player" (800.4j). A resolving spell or ability that leaves the stack "will
  continue to resolve fully" (608.2m).
- **Open:** narrower than "at any time" suggests: (1) a concession inside
  one atomic event, i.e. between replacement applications (616.1) or within
  the 704.3 SBA batch, and what state 800.4a's cleanup runs against if so;
  (2) who follows a resolving object's instructions when its controller is
  the leaver. 608.2c has the controller follow the instructions, and 800.4g
  reassigns only choices. 800.4h's next-player rule is the likely route, but
  that is an inference.
- **Docs assume:** nothing — no doc commits to interruption points.
- **Alternatives:** coarse — concession takes effect at the next event
  boundary (clean atomicity; "immediately" weakened, and a player can't
  concede to deny a mid-resolution disclosure); fine — interruptible
  anywhere (honors 104.3a literally). Mid-resolution departure is already
  defined by 608.2m and 800.4f–j, so the fine reading needs the engine to
  define only the two unaddressed pieces: interruption inside a single event
  and the departed-controller decider.

### UD-8 — "Random" means what distribution? — category: open

- **CR says:** dice and coins are distribution-fixed: an N-sided die "must
  have N equally likely outcomes" (706.1a); substitute methods for dice need
  "the same number of equally likely outcomes" (706.1b); a coin needs "equal
  likelihood that either side lands face up", and substitutes need "two
  possible outcomes of equal likelihood" (705.1). Everything else isn't:
  sticker sheets are chosen "at random" (103.2d), a face-down exiled card
  may be picked "at random" (406.4), and shuffle is defined
  *epistemically* — "randomize the cards … so that no player knows their
  order" (701.24a); MTR 3.10 is the same epistemic test ("no player can
  have any information"). Other unfixed random selections: decks put "in a
  random order" (103.3), "one random card" for ante (407.2), random discard
  (701.9b), the subgame's first player (729.2), random seating and
  first-player choices in team variants (806.3, 807.3, 808.4, 809.4), and
  "any mutually agreeable method" for the starting player (103.1). There is
  no glossary entry for "random."
- **Open:** narrower than it looks — uniformity for the "at random"
  choices and shuffle outcomes; independence across successive random
  events, which is also unfixed (705.1 and 706.1a fix only per-trial
  likelihood); and verifiability — 701.24a's no-player-knows condition
  constrains implementations beyond any distribution (a predictable PRNG
  seed violates it even with uniform outputs).
- **Docs assume:** nothing distributional — `information.md` §5 treats
  RNG only as a discloser. `choices.md` §4 does commit to one implementation
  constraint: the RNG is seedable for replay, and its seeds must stay
  unknowable to players during the game to satisfy 701.24a (engine
  inference). That covers verifiability only, so the entry stays `open`.
- **Alternatives:** uniform and independent (the universal tabletop
  convention; anything else is defensible under 701.24a's letter and
  indefensible in practice). Digital engines additionally need a
  verifiability story (committed seeds vs. trusted server) the CR cannot
  see.

### UD-9 — Extent of a last-known-information snapshot — category: open

- **CR says:** more than it first appears. LKI "captures that object's
  last existence in that zone" (glossary, cross-referencing 113.7a,
  608.2b, 608.2h, 800.4h — departed players included); 608.2h adds that
  the object acts "as it exists—or as it most recently existed" — the
  record is *the object*, not a field list. Timing is settled: read once
  when the effect is applied (608.2h), look-backs exempt (608.2i),
  SBA-batch departures snapshot pre-batch (704.8), statics never use LKI
  (604.7).
- **Open:** only the *boundary* of the record. Characteristics,
  controller, status, and counters are clearly in. Combat designations
  are in as well, though they are neither characteristics nor status
  (110.5) and leaving the battlefield removes a creature from combat
  (506.4). Ninjutsu's creature enters attacking "the same player,
  planeswalker, or battle as the creature that was returned" for its
  cost (702.49c). A defending player is read from what a creature "was
  attacking before it was removed from combat" (508.5). Oracle text asks
  after a death or bounce whether "it was attacking" (Garna, Bloodfist of
  Keld; Desculpting Blast) or "attacking or blocking alone" (Thijarian
  Witness). Do attachments, choices made for the object, and
  history-dependent quantities (damage marked, "this turn" facts) ride
  along? The CR never draws the line; consumers name fields case by case
  (702.2e, 702.15c, 701.44c, 701.50b, 702.49c, 800.4i).
- **Docs assume:** mechanism only — LKI is a snapshot read from the event
  log (`events.md` §5, §7); no doc commits to an extent.
- **Alternatives:** snapshot the full object record at every log commit
  (matches the glossary's "last existence" framing; heavy); per-consumer
  minimal fields (light — but 608.2h's whole-object language obligates
  *observational equivalence* with the full record: one missed field is
  a silent wrong answer the day a new consumer appears).

### UD-10 — Knowledge across rewinds and game boundaries — category: assumed

- **CR says:** reversing an illegal action may not reverse
  library-touching actions (733.1) — exactly the cases where reversal
  would leave a player knowing cards the restored state calls hidden —
  and revealed cards that get shuffled or reordered become new objects
  (701.20d). Nothing addresses knowledge after a *legal* reversal of a
  non-library disclosure (an illegally cast spell returns to a hand
  everyone has now seen, 733.1). The gap recurs at game boundaries: a
  restart carries every card into the new game (727.2), a subgame is
  built from the main game's libraries (729.2) and reports back only its
  result (729.1b) — no rule un-knows what players saw of either game.
- **Open:** the CR has no knowledge state, so an engine with per-player
  information sets must decide whether rewinds — or restarts, or subgame
  entry/exit — shrink them.
- **Docs assume:** knowledge is monotone — "knowledge can't be
  un-learned" is read as 733.1's rationale (`information.md` §5). "Rewinds
  restore state, never views" is this registry's extrapolation from §5, not
  something a doc states: `information.md` §6's
  `PlayerView = project(GameState, player)` model, read literally, would
  rewind views along with state. MTR 4.8 corroborates: a judge may
  reverse a decision only if the player "has not gained any information
  since taking the action" — policy already treats knowledge as
  unrevertible.
- **Alternatives:** reset views to the restored state (coherent for
  replay and AI self-play; models humans as forgetting, contradicting
  the rationale the docs read out of 733.1 and MTR 4.8).

### UD-11 — Game-state equality — category: open

- **CR says:** loops are defined by repetition, of "a sequence of events
  with no way to stop" (104.4b, 104.4f, 801.16) or of "a set of actions
  could be repeated indefinitely" (732.1b), with the mandatory-loop draw
  restated in 732.4. A loop of mandatory actions is a draw (104.4b;
  limited-range variants 104.4f, 801.16 draw only the involved players).
  Only 732.3 predicates on reaching "the same game state": a fragmented loop
  is detected by "the same game state being reached multiple times,"
  obligating a different choice. Yet "game state" has no glossary entry and
  no rule defines when two states are the same; MTR 4.4 leans on the same
  undefined notion ("not meaningfully changing," "a previous game state (or
  one identical in all relevant ways)"). 732.3's example calls the state
  returned only after stipulating that "nothing in the game cares how many
  times an ability has been activated", and despite the new continuous
  effects (with later timestamps) the activations created. That is evidence
  that equality is judged by relevant, observable components, matching MTR
  4.4's "identical in all relevant ways". It is an example in the informal
  shortcut rules (732.1a, 732.1c), not a definition.
- **Open:** the equality predicate — which components count. Zones,
  life, counters, designations, and per-object status clearly do; but
  turn/phase position (always advancing across turn-spanning loops),
  timestamps, the event log, floating mana, and revealed-knowledge
  differences must each be ruled in or out — include everything and no
  two states are ever equal, so 732.3 never fires and any state-recurrence
  detector for 104.4b loops misses them.
- **Docs assume:** nothing — `outcomes.md` §3 names the mandatory-loop
  monitor but no doc defines its equality test.
- **Alternatives:** structural equality over a pinned component list
  (MTR 4.4's "identical in all relevant ways" made explicit);
  equivalence modulo declared-irrelevant components (the 732.3 example
  supports this reading; how an engine computes "cares", meaning which
  predicates read which components, stays open); event-sequence
  equality per 104.4b's "sequence of events" framing (detects loops
  without comparing whole states).

### UD-12 — Intra-batch event ordering — category: assumed

- **CR says:** batches are single simultaneous events — all SBAs in a
  check are performed "simultaneously as a single event" (704.3); all
  assigned combat damage is dealt simultaneously (510.2) — and every
  order-sensitive consumer is settled by its own rule, never by
  intra-batch position: simultaneous timestamps go in APNAP order
  (613.7m), the batch's triggers stack in two APNAP passes (603.3b), LKI for
  batch departures snapshots the pre-batch state (704.8).
- **Open:** whether intra-batch order is *observable at all*. The CR's
  answer pattern says no — but a totally ordered log invents an ordering
  the game cannot see, and any consumer that reads it (replay,
  diagnostics, a future "first"/"last" wording) bakes the invention in.
- **Docs assume:** a total order — `events.md` §7 commits
  `ordering: int` (commit order within the log), marked there as an
  engine choice.
- **Alternatives:** batch-scoped ordering — a batch id plus unordered
  members, so simultaneity is representable and 613.7m/603.3b/704.8
  consume their own rules, not log position; or keep the total int but
  pin that nothing rules-facing may read relative order within a batch.

### UD-13 — "As [this Equipment] becomes attached" choices — category: open

- **CR says:** the CR defines its "As [event]" forms one event at a
  time. "As [this permanent] enters" is a replacement effect (614.1c) and
  a static ability "whose effect occurs as part of the event that puts the
  permanent onto the battlefield" (603.6d). "As [this permanent] is turned
  face up" is a replacement effect (614.1e) that is "applied while that
  permanent is being turned face up, not afterward" (708.11). "As [this
  permanent] transforms" is applied "while that permanent is transforming
  or converting" (712.20). No rule covers "As this Equipment becomes
  attached to a creature, choose …" (Sanctuary Blade, Psychic Paper,
  Dinosaur Headdress). Killer Cosplay's "Whenever this Equipment becomes
  attached" is an ordinary trigger (603.2e) and is not one of them. Some
  edges are fixed. Attaching to the object it's already attached to
  "does nothing" (701.3b), so no new choice is made (Sanctuary Blade
  [2020-04-17]). Each new attachment gets a new timestamp (613.7e). A
  Sanctuary Blade attached with no color chosen "doesn't grant a
  protection ability", not even protection from colorless (Sanctuary
  Blade [2020-04-17]). That matches 607.5a's undefined choice, but
  607.5a speaks only of an object that gains the ability, so a printed
  card with no choice is a novel UD-6 case.
- **Open:** how the choice is classified and when it happens. It could
  be a replacement effect on the attach event (extending 614.1c and
  614.1e), a static ability whose effect is part of that event
  (extending 603.6d, 708.11, and 712.20), or a trigger. The trigger
  reading contradicts the "As" convention and opens a priority window in
  which the creature is equipped without the new choice. It is also open
  which events count as becoming attached. Rulings count an Aura entering
  attached for "becomes attached" triggers (Brood Keeper [2014-07-18];
  Siona, Captain of the Pyleas [2020-01-24]). Danitha, Benalia's Hope can
  put Sanctuary Blade onto the battlefield attached, and no ruling says
  whether a color is chosen then.
- **Docs assume:** nothing; no reference doc covers the wording.
- **Alternatives:** an event rider applied while the Equipment becomes
  attached, so the choice lands with the attachment and its new
  timestamp, with no window. This is the nearest analogue of 708.11 and
  712.20. Or a replacement effect, which also brings 616.1 ordering and
  614.5's one-application rule to the attach event; no printed card was
  found that makes it differ from the rider. Separately, pin whether
  entering attached makes the choice. Sharing one becomes-attached event
  with the trigger rulings means it does.

### UD-14 — "Doesn't untap during [an] untap step": can't, replacement, or selection — category: open

- **CR says:** in the untap step, "the active player determines which
  permanents they control will untap … effects can keep one or more of a
  player's permanents from untapping" (502.3). No rule classifies the
  printed "doesn't untap during … untap step" effects (Mana Vault; Frost
  Titan's "It doesn't untap during its controller's next untap step") or
  exert, where "you choose to have it not untap during your next untap
  step" (701.43a). "Can't" effects "aren't replacement effects" (614.17),
  but this wording never says "can't". The wording uses none of 614.1a–e's
  replacement markers ("instead", "skip", the "enters" forms, "As … is
  turned face up"). Those markers are not exhaustive: regeneration is a
  replacement effect whose "instead" "doesn't appear on the card but is
  implicit in the definition of regeneration" (614.8). But no rule
  supplies such a definition for "doesn't untap", either way.
  502.3's "keep … from untapping" does not decide it either, because a
  stun counter's effect "stops the permanent from untapping" and is a
  replacement effect: "If a permanent with a stun counter on it would
  become untapped, instead remove a stun counter from it" (122.1d).
- **Open:** the classification. It is observable on a tapped permanent
  that has both a stun counter and a doesn't-untap effect. As a can't
  effect, the untap can't happen, the stun replacement can't modify it
  (614.17c), and the counter stays. As a constraint on 502.3's selection,
  the permanent is never chosen to untap, so no untap would happen and
  the counter stays. As a replacement effect, its controller orders the
  two (616.1). Applying the stun counter first removes the counter while
  the permanent stays tapped; applying doesn't-untap first keeps the
  counter. No ruling settles it; every stun-counter ruling was checked.
- **Docs assume:** nothing; no reference doc classifies the wording or
  cites 502.3 for it.
- **Alternatives:** can't (614.17) or a 502.3 selection constraint,
  which agree unless something else tries to untap the permanent during
  that same untap step (none found). The counter persists, matching
  502.3's framing of effects acting on the active player's choice of what
  untaps. Or a replacement effect, which lets the controller spend a stun
  counter during an untap step in which the permanent stays tapped
  anyway.

### UD-15 — Tally weight of repeated and attacker-side combat requirements — category: assumed

- **CR says:** a declaration is illegal if it obeys fewer requirements
  than "the maximum possible number of requirements that could be obeyed
  without disobeying any restrictions" (508.1d, 509.1c), and 509.1c's
  requirements are "effects that say a creature must block". Duplicate
  weight is fixed only for goad. Goading by several players "creates
  additional combat requirements" (701.15c), and the same player goading
  again "doesn't create additional combat requirements" (701.15d).
- **Open:** (a) whether identical requirement effects from different
  sources (two Lures on one attacker; two "must be blocked" effects on one
  attacker) count once or twice when they compete with another
  requirement; (b) how an attacker-side "[X] must be blocked if able",
  which sits outside 509.1c's per-creature parenthetical, enters the tally.
- **Rulings constrain:** "must be blocked" obliges the defender to "assign
  at least one blocker to it", and repeating it "provides no additional
  benefit" (Loathsome Catoblepas). One blocker satisfies several instances
  (Slayer's Cleaver).
- **Docs assume:** `deontics.md` §4 scores "must be blocked" as one
  set-level unit (obeyed iff at least one blocker), which settles (b) as an
  engine inference from rulings, and makes no commitment on (a) duplicates.
- **Alternatives:** scoring an attacker-side "must be blocked" as one
  set-level unit (obeyed iff at least one blocker), the inference the
  rulings above support for (b). For (a), multiset counting, the literal
  "number of requirements", which lets a repeated "must be blocked"
  outweigh a competing per-creature requirement, against the Catoblepas
  ruling's "no additional benefit". Or dedupe every wording into a set, which
  goes beyond 701.15c–d: those key goad by goading player, so different
  goaders still add requirements (`generalizations.md` §9 states "keyed by
  (source-player, constraint) pairs, deduplicated — a set, not a multiset"
  generally, but its only support is goad's 701.15c–d; read it as
  goad-scoped until this entry is settled, or scope that note to goad).

### UD-16 — Keyword-defined CDA granted outside 604.3a(2) — category: open

- **CR says:** changeling and devoid are each "a characteristic-defining
  ability" (702.73a, 702.114a), but 604.3a(2) accepts only printing, the
  token-creating effect, a copy effect, or a text-changing effect as the
  source of a CDA.
- **Open:** whether a keyword-defined CDA granted any other way is a CDA
  (applied first in its layer, functioning in all zones) or an ordinary
  continuous effect, and whether a layer-6 grant's layer-4/5 effect applies
  at all.
- **Docs assume:** nothing — `abilities.md` §2 flags the case as unsettled
  and commits to no answer.
- **Alternatives:** treat the granted keyword as a CDA; or treat it as an
  ordinary continuous effect in timestamp order. Either way the engine must
  also decide whether a grant made in layer 6 can still set the layer-4/5
  characteristics that changeling or devoid define.
- **Admitted because:** a generic keyword-grant engine must answer it. No
  supported card poses it. Only the playtest cards Everyone's an Impostor
  (reminder: "we know this doesn't actually work") and Slivdrazi Monstrosity
  do.

### UD-17 — Does a replaced SBA count as "performed" for 704.3's repeat? — category: open

- **CR says:** all applicable SBAs in a check are performed "simultaneously
  as a single event"; "if any state-based actions are performed as a result
  of a check, the check is repeated; otherwise" waiting triggers go on the
  stack and the check repeats, until a check performs none (704.3; 117.5:
  "until no state-based actions are performed"). Some conditions hold with
  nothing performed: an indestructible creature with lethal damage (702.12b,
  704.5g), a player at 0 life who can't lose (101.2). A replaced event "never
  happens" and "a modified event occurs instead" (614.6); one replacement
  replaces all same-result SBAs (704.7).
- **Open:** whether an SBA whose event is replaced or modified counts as
  "performed." Neither 614.6 nor 704.3 says. Observable effects: (a) whether
  the re-check runs before the modified event's triggers go on the stack
  (counts-as-performed: re-check first; not-performed: triggers first, then
  re-check); (b) termination: under counts-as-performed, a replacement that
  leaves the condition standing and doesn't consume its own source repeats
  forever; under not-performed the loop stops.
- **Docs assume:** nothing — `actions.md` §3 states the loop is keyed on SBAs
  performed and flags this question without committing to a reading.
- **Alternatives:** counts-as-performed (the replaced SBA still drives the
  repeat); not-performed (only unmodified SBA events drive it). Rulings
  evidence, not CR: Lich's Mirror [2008-10-01] says that if you control but
  don't own it and would lose again, it "has its effect again ... and
  again," an involuntary loop ending in a draw, which fits the
  counts-as-performed reading for game-loss replacements.

### UD-18 — Timing of day/night initialization — category: assumed

- **CR says:** "Any time a player controls a permanent with daybound, if it's
  neither day nor night, it becomes day" (702.145d); nightbound is the same
  with "there are no permanents with daybound on the battlefield, it becomes
  night" (702.145g). The mismatch transforms (702.145c, 702.145f) use the same
  "Any time" wording and add "This happens immediately and isn't a
  state-based action." The initialization rules carry no such sentence, and
  704.5 doesn't list them.
- **Open:** whether initialization is also immediate (it can happen
  mid-resolution, before the rest of the effect that put the permanent on the
  battlefield finishes) or waits for the next 704.3 check or priority
  boundary. The CR neither says "immediately" nor classifies it as an SBA.
- **Docs assume:** immediate, like the mismatch transforms, inferred from the
  shared "Any time" wording (`actions.md` §3, "Immediate rule actions").
- **Alternatives:** applied at the next state check (the "Any time" read as a
  standing state rule). Observable when a later instruction in the same
  resolution, or a trigger from the same entry, reads whether it is day or
  night.

### UD-19 — When an OR-branch cost's branch is chosen — category: assumed

- **CR says:** the controller of a spell or ability "announces their
  intentions to pay any or all of" its additional costs as described in
  601.2b (118.8a); a multi-way mana symbol's payment choice is made as the
  controller proposes the spell or ability (118.13a, 601.2b); keyword
  costs with choices pick at 601.2b and pay at 601.2h (702.48b, 702.119c,
  702.180b); 601.2f computes the total cost from a cost already chosen;
  cumulative upkeep makes each choice separately per age counter (702.24a).
- **Open:** when the branch of an additional cost written as an OR ("As an
  additional cost to cast this spell, forage or pay {B}") is chosen. No
  rule names that step for a bare OR-cost.
- **Docs assume:** the branch is announced at 601.2b as part of announcing
  intentions to pay additional costs, and paid at 601.2h (`costs.md` §2).
  The choice is read off the analogs: 601.2f needs the branch to compute the
  total, so 601.2f is the latest possible point, and 118.8a plus the keyword
  analogs place the choice at 601.2b.
- **Alternatives:** choose the branch at 601.2f while totalling, or at
  601.2h at payment. Observable only if something between 601.2b and
  601.2f/h reacts to the branch (targets or text that depend on it); no
  supported-corpus card does today.

### UD-20 — Is a target choice a "choice that may change the spell's qualities"? — category: assumed

- **CR says:** 601.3b lets a player begin casting as though a spell had flash if a choice in the proposal "may cause that spell's qualities to change" and that choice could make the granting effect apply (bestow's alternative cost making an Aura is its example). 601.3c covers paying a required alternative or additional cost. 601.3d is present-tense: a spell that has flash only if certain conditions are met may begin to be cast "if those conditions are met", and 601.6a lets that flash persist if the conditions later stop being met. Targets are chosen during the proposal (601.2c), and 601.6 re-checks legality after the proposal.
- **Open:** whether a target choice counts as a choice that "may cause … qualities to change" under 601.3b. This matters for "You may cast this spell as though it had flash if it targets …" (Flash Photography, Timely Ward) and "… if X is 3 or less" (Silver Scrutiny; X is a 601.2b announcement, which is closer to 601.3b's text). The CR never calls a target a quality. Under 601.3d's present tense alone, a condition that depends on a not-yet-chosen target is not yet met when the player begins to cast.
- **Docs assume:** the existential reading. Conditions that only a proposal choice can satisfy (X, targets) are evaluated under 601.3b, and the chosen completion must still satisfy the condition at the post-proposal recheck (601.2e, 601.6). 601.6a persistence does not cover these cases (`deontics.md` §5, marked *Engine inference*).
- **Alternatives:** present-tense only (a target-dependent flash condition can never begin a cast, so such cards would be uncastable at instant speed; contradicts the cards' evident intent); existential for X but not targets (follows 601.3b's "variable cost" example class literally; needs a rule for why targets differ).

### UD-21 — Duplicate goad instances from one player — category: open

- **CR says:** a creature can be goaded by multiple players, each adding
  requirements (701.15c); if the same player goads it again, that "has no
  effect" and adds no requirements (701.15d). The goad action lasts "until the
  next turn of the controller of that spell or ability" (701.15a); other
  effects that say a permanent is goaded set their own durations (611.2a,
  611.3a), and a static goad applies as long as the static does (Baeloth
  Barrityl ruling 2022-06-10).
- **Open:** whether "has no effect" covers one player's instances with
  different durations, such as a static goad plus a goad action from the same
  player. If the later instance is a no-op, the creature stops being goaded
  when the earlier one ends. If the later instance exists, it must add no
  requirements while both apply (701.15d), and the creature stays goaded after
  the earlier one ends.
- **Docs assume:** nothing on the collapse question. `designations.md` Goaded
  and `state.md` §6 model per-goader instances, each with its own duration, and
  no extra requirements from a duplicate; that pins the "instance exists, adds
  nothing" reading only for requirements.
- **Alternatives:** collapse duplicates (one instance per goading player, the
  earlier one's expiry ends the goad); keep every instance (each expires on its
  own clock, requirements deduplicated by (goader, requirement) pair).

### UD-22 — Which plane each planar controller controls — category: open

- **CR says:** normally one planar controller controls the face-up plane or
  phenomenon (311.5, 312.4, 901.6). In Grand Melee Planechase each player who
  will start with a turn marker sets a starting plane, "Each of them is a
  planar controller" (901.14a), and several planes may be face up at once
  (901.14). A leaving turn-marker holder ceases to be a planar controller and
  their planes go to the bottom of their owners' decks, with no planeswalk
  (901.14b). Turn markers can be passed (807.4c, 807.4d). Planeswalking moves
  every face-up plane away (701.31b, 901.11c).
- **Open:** which face-up plane each planar controller controls; who controls
  a plane while its passed turn marker waits to start a turn; and what remains
  after one planar controller planeswalks, since planeswalking moves every
  face-up plane away.
- **Docs assume:** the representation shape only — a face-up plane →
  planar-controller map, not a single player reference (`designations.md`
  Planar controller; `state.md` §2). No doc picks the mapping rule.
- **Alternatives:** one controller reference per face-up plane, fixed when the
  plane is set (901.14a); derive controller from the plane's owner or the
  marker holder; treat planeswalking as moving all planes and recompute the
  map from the turn markers.

### UD-23 — Protector repair while the battle is attacked — category: open

- **CR says:** a battle's protector is chosen as it enters (310.9a); 310.11
  limits the repair of a missing or ineligible protector to "a battle that
  isn't being attacked"; 704.5x repairs a protector-less battle only when no
  creatures are attacking it; 704.5y repairs an ineligible protector with no
  such condition. A change of protector removes the battle from combat
  (506.4); eligibility depends on battle type (310.9a, 310.12a).
- **Open:** whether 704.5y's repair runs immediately for an attacked battle
  (704.5y as written) or waits until the battle isn't attacked (310.11). A
  control change already removes the battle from combat (506.4), so the two
  texts differ only when eligibility changes mid-attack without one. Example:
  an attacked Siege loses its battle type, which leaves only its controller
  eligible (310.9a).
- **Docs assume:** nothing — `designations.md` Protector and
  `generalizations.md` Family 10 flag that the sources disagree and commit to
  no reading.
- **Alternatives:** follow 704.5y literally (repair immediately, which removes
  the battle from combat); follow 310.11 (defer all repair until the battle
  isn't attacked, leaving the ineligible protector in place for the rest of
  the attack).

### UD-24 — Additive copy exceptions under 707.9d — category: open

- **CR says:** a copy exception that doesn't copy, retains, or provides
  values for a characteristic leaves uncopied the source's
  characteristic-defining ability for it, and for color its color
  indicator (707.9d); the carve-out: "This rule does not apply to copy
  effects with exceptions that state the object is a certain card type,
  supertype, and/or subtype 'in addition to its other types.' In those
  cases, any characteristic-defining ability that defines card type,
  supertype, and/or subtype is copied" (707.9d).
- **Open:** (a) does an additive color exception ("a 1/1 red Balloon
  creature in addition to its other colors and types", The Jolly Balloon
  Man) provide values for color? Read literally it does, so a copied devoid
  (702.114a) and color indicator drop, and "its other colors" then come from
  the mana cost alone. (b) Does a type-additive exception exempt the whole
  copy effect ("This rule does not apply") or only type CDAs ("In those
  cases")? That decides whether Ratadrabik of Urborg's "2/2" drops a copied
  P/T CDA. Rulings lean toward reading these as 707.9b modifications
  without reaching CDAs. Ratadrabik of Urborg `[2022-09-09]`: "Except for
  power and toughness, the token copies only what was printed ... and adds
  the color black and the creature type Zombie". Lazotep Convert
  `[2023-04-14]`: "it keeps its other colors and types as part of its copy
  effect". Neither names a characteristic-defining ability or color
  indicator, and The Jolly Balloon Man's rulings are silent, so neither
  question is settled.
- **Docs assume:** nothing; `effects.md` §4 flags it.
- **Alternatives:** treat additive exceptions as 707.9b modifications (CDAs
  and indicator copied, values unioned); or apply 707.9d literally to every
  exception except the type-defining CDAs.

### UD-25 — Agency tags for rules-procedure moves — category: representation-only

- **CR says:** special actions "are not to be confused with turn-based
  actions and state-based actions" (116.1); twelve exist (116.2), and
  one of them, Circling Vultures' discard, is a discard that "is a special
  action" (116.2e); playing a land is a special action (701.18a). An
  object whose targets are all illegal "doesn't resolve" (608.2b, 608.3b),
  while one that resolves makes a final move: an instant or sorcery goes to
  the graveyard (608.2n), a permanent spell enters (608.3a) or, if it
  can't, goes to the graveyard (608.3e). The two cases are observable
  apart: rebound has no effect when all targets are illegal (Staggershock
  [2010-06-15]), and resolution-only replacements and triggers match the
  resolution move only (702.27a, 702.88a, 702.55a). Casting moves the card
  to the stack (601.2a); the game-start procedure moves cards (103.5,
  103.6a); objects leaving with their owner is "not a state-based action"
  (800.4a). Mana tapping is the activation of a mana ability (106.12), and
  106.12a/b match the production at resolution.
- **Open:** the tag names, or whether these procedure moves carry an
  agency at all. The CR fixes the behavior (which moves can be told apart)
  but never names a tag. The relation to U2's nullable agent (nullable vs
  a synthetic "game rules" agent) is part of the same question.
- **Docs assume:** the nine-tag list in `events.md` §3: `cost-payment`,
  `attack-declaration`, `effect-instruction`, `turn-based-action`,
  `state-based-action`, `mana-ability-resolution` (the mana-production
  event only), `special-action`, `resolution`, `failed-resolution`. The
  list is declared non-exhaustive for casting's move to the stack,
  game-start moves and leaving the game with the owner.
- **Alternatives:** a single `rules-procedure` tag, workable only if it
  still carries the resolve/fail distinction; no agency (null agent) for
  procedure moves, with the distinction carried on the event instead;
  separate tags for game-start and leaving-the-game moves instead of
  leaving them outside the list.

### UD-26 — Crime from a copy of a triggered ability — category: open

- **CR says:** a player commits a crime as they cast a spell, activate an
  ability, or put a triggered ability on the stack and that spell or
  ability targets an opponent, an opponent's permanent, spell or ability,
  or a card in an opponent's graveyard (700.13). To copy a spell or
  ability is to put a copy of it onto the stack; "a copy of a spell isn't
  cast and a copy of an activated ability isn't activated" (707.10). 707.10
  says nothing about triggering for a copied triggered ability, only that
  a copy of an ability is itself an ability.
- **Open:** whether putting a *copy* of a triggered ability on the stack
  counts as "puts a triggered ability on the stack" for 700.13. Copied
  spells and copied activated abilities are settled (no crime), but the
  triggered-ability case is not.
- **Docs assume:** nothing — `events.md` §2 "Crime" states the question and
  commits to neither reading.
- **Alternatives:** count it (the copy is an ability put on the stack, and
  the targets are chosen or copied as for any triggered ability); don't
  count it (the copy is put on the stack by the copying effect, not by the
  trigger procedure that 700.13's "puts a triggered ability on the stack"
  describes). Observable only with an effect that copies a triggered
  ability that targets an opponent's objects, and a crime trigger or
  payoff.

### UD-27 — Mana produced by a hybrid Phyrexian symbol — category: assumed

- **CR says:** a produced Phyrexian mana symbol adds "one mana of the color
  of that symbol" (106.9); a hybrid Phyrexian symbol "is both of its
  component colors" (107.4f; the glossary's two-way and three-way hybrid
  Phyrexian entries split it into component colors), so "the color of that
  symbol" is not a single color; an effect that would produce mana of an
  undefined type produces none (106.5), which a literal reading of 106.9
  would trigger here; 106.8 names only colored and generic hybrid halves.
  The cost-side analog is equally silent: 118.7f does not settle how a
  hybrid Phyrexian symbol behaves under cost reduction.
- **Open:** how many mana, and of which color(s), an effect adds when it
  adds a hybrid Phyrexian symbol such as {G/W/P} (reachable via Elemental
  Resonance on Ajani, Sleeper Agent).
- **Docs assume:** the player chooses one of the symbol's component colors
  and one mana of that color is added (`mana.md` §3 table). This follows
  Elemental Resonance's reminder text (no game function, 207.2) and Charmed
  Pendant's ruling [2005-11-01], "you get one of either color mana, not
  both". Attested by Elemental Resonance + Ajani, Sleeper Agent.
- **Alternatives:** no mana (the literal 106.5 undefined-type reading of
  106.9); both component colors (107.4f's "both of its component colors"
  read as a production of two mana, which the Charmed Pendant ruling
  contradicts); engine-assigned color (no rule gives the engine the choice).

### UD-28 — Do looked-at cards that a library effect reorders become new objects? — category: assumed

- **CR says:** "If cards in a player's library are shuffled or otherwise
  reordered, any revealed cards that are reordered stop being revealed and
  become new objects" (701.20d). "Looking at a card follows the same rules as
  revealing a card, except that the card is shown only to the specified
  player" (701.20e), and a reveal lasts as long as the effect needs it
  (701.20a). Scry, surveil and fateseal each look at the top N cards and then
  put some on the bottom or rearrange or keep the rest on top (701.22a,
  701.25a, 701.29a).
- **Open:** two points the text does not settle. (1) Whether 701.20d's
  "revealed cards" reaches looked-at cards at all, since 701.20e borrows the
  reveal rules but 701.20d names only revealed cards. (2) If it does, whether
  a looked-at card counts as "reordered" when it ends where it started, or
  when its order relative to the other cards is unchanged (scry 1 kept on
  top). No official ruling addresses either point.
- **Docs assume:** point (1) yes, as an engine inference from reading 701.20e
  and 701.20d together: looked-at cards that a library effect moves or
  rearranges become new objects (`information.md` §5). Point (2): no
  commitment.
- **Alternatives:** (a) any repositioning of a looked-at card makes a new
  object, including a card kept in place (simplest rule; every scry
  invalidates references to the cards it looked at). (b) only a changed
  position or changed relative order counts (matches "reordered" literally;
  needs a before/after comparison per effect). (c) looks never trigger
  701.20d, so a scry keeps the object's identity (needs 701.20e's "same
  rules" to exclude 701.20d). Observable through anything tracking the object
  across the reorder: "this card" references, 400.7 look-backs, and effects
  that referred to a card the player just looked at.

### UD-29 — Do references to a base keyword find its "variant of" forms? — category: open

- **CR says:** Ten forms are only "a variant of" their base (701.49d, 702.6e, 702.16j, 702.16k, 702.19c, 702.49d, 702.54b, 702.82c, 702.106f, 702.119b). The CR settles matching fully for typecycling, hexproof from, sticker kicker and the partner abilities (702.29f, 702.11e, 702.33h, 702.124n), and partially for multikicker and megamorph (cost identity, 702.33c, 702.37b), bands with other (loss and band formation, 702.22b-c) and connive N (701.50f). It settles grants only when an effect grants a list via "the same is true for" (702.1c). It says nothing about matching for the ten "variant of" forms; for trample over planeswalkers, 702.19d/f/g lean toward distinctness.
- **Open:** whether a reference to the base finds the variant. Printed pairs pose it: Silver-Fur Master / Yuriko, the Tiger's Shadow; equip-cost reducers / Luxior, Giada's Gift; Archetype of Aggression / Thrasta, Tempest's Roar; Keen-Eared Sentry / the initiative's "ventures into Undercity" (726.2). No official ruling addresses these pairs.
- **Docs assume:** nothing — `keyword-classification.md` (Keyword variants) states the gap and commits to no matching rule.
- **Alternatives:** the variant is the base for every reference, it is never the base, or it is the base per reference kind (cost changes, loss, prohibitions).

### UD-30 — Which counted-state mechanics share the `progress-track` primitive? — category: assumed

- **CR says:** day and night are "designations that the game itself can have" (731.1) and move in both directions: day becomes night under 731.2a, night becomes day under 731.2b, and "other effects can also make it day or night" (731.1); once set, the game never returns to neither (731.1). A player's speed is set by a rule or effect (702.179b), raised by an inherent trigger only while it is less than 4 (702.179d), and lowered by effects (Spikeshell Harrier: "This effect can't reduce their speed below 1"). Neither is monotonic, the CR gives neither a range, and it names no mechanism that day/night, speed and the other progressions share. Level Up (702.87), Venture into the Dungeon (701.49), The Ring Tempts You (701.54) and Read Ahead (702.155) are also positions in an advancing progression (Family 4 of `generalizations.md`), but the CR does not group them with day/night. Ascend, Storied and Renown are plain composite with `given: null`.
- **Open:** where the primitive's boundary lies: a game-maintained value with thresholds that statics read, whatever its representation (a scalar or a designation), or only a monotonic counter. Speed is a number a static reads (Max Speed 702.178; Start Your Engines! 702.179), and day/night is a designation statics read (Daybound and Nightbound, 702.145); the other four keywords compile to counters, designations or zone state. 731.1 calls day and night "designations", yet other designations are plain composite. No official ruling decides the boundary.
- **Docs assume:** option (a), the wider non-monotonic reading: one `progress-track` primitive covering the day/night designation and speed. Daybound, Nightbound, Max Speed and Start Your Engines! are composite-given(`progress-track`); Level Up, Venture into the Dungeon, The Ring Tempts You and Read Ahead stay plain composite (`keyword-classification.md` Primitive basis; `generalizations.md` §4).
- **Alternatives:** (b) treat day/night as a plain designation, so Daybound and Nightbound become plain composite (composite-given 19 to 17, composite 222 to 224; the Counts table, dependents index and JSON all change) and `progress-track` keeps Max Speed and Start Your Engines! (two dependents, still at the threshold). (c) widen the primitive to every Family 4 instance, making Level Up, Venture, the Ring and Read Ahead composite-given. Or mint a separate designation primitive (rejected during review).

### UD-31 — What "another" / "other" excludes — category: assumed

- **CR says:** nothing general. The CR lists "another target" only as a
  shorthand among the damage-target forms (115.4), and uses "another"/"other"
  as ordinary English in its own prose (701.14a, 702.134c, 121.2c). A single
  `target` word can't pick one object twice, but separate `target` words can
  (115.3), and "any other target" constrains only the final target set (115.7e
  example). Keyword definitions spell the exclusion out when it matters
  (champion, 702.72a; soulbond, 702.95a; backup, 702.165a; station, 702.184a;
  reconfigure, 702.151a; support, 701.41a).
- **Open:** which referent a printed `another [noun]` / `other [noun]`
  contrasts with, and how a generic parser distinguishes definite `the other
  [N]` (pair complement) from bare `other`. Rulings settle single cards whose
  mention comes earlier in the same sentence (Ulvenwald Tracker, Farrel's
  Mantle, Selvala, Pit Fight, Domri Rade: the first target or the enchanted
  creature, not the source). No ruling covers a later mention in the same
  sentence (Inquisitor's Flail's "If another creature would deal combat damage
  to equipped creature") or a mention in an earlier sentence (Bond of
  Passion).
- **Docs assume:** the anchor is a same-kind mention earlier in the same
  ability, which may be in an earlier sentence (Bond of Passion's "any other
  target"), or later in the same sentence (cataphoric: Inquisitor's Flail's
  second ability), whose kind and types fit the head (a mention fits only if
  the head could select it, 115.4). With neither, it is the source, or "you" for a player head
  (`queries.md` §2, `grammar.md` §5). Engine inference from English grammar.
- **Alternatives:** always the source (contradicted by the Tracker and
  Farrel's Mantle rulings); "requires an earlier target" (contradicted by
  702.151a and 701.41a); the nearest earlier mention only (leaves the Flail on
  the source default, which excludes nothing; fails Bond of Passion-shaped
  earlier-sentence mentions); a per-card anchor table.

### UD-32 — Antecedent of "it" / "that [noun]" — category: assumed

- **CR says:** the only hook is 608.2c: the whole text is read and the rules
  of English apply, and later text can change the meaning of earlier text;
  linking is identity-based (607.1). No rule says which earlier object or
  player a pronoun or `that [noun]` refers to. Rulings bind individual cards
  (Feral Contest 2010-03-01, Kalitas 2009-10-01, Ram Through 2020-04-17), and a
  type word names a battlefield permanent (109.2) while an object that changed
  zones is a new object (400.7, with the 400.7j find exception).
- **Open:** the procedure that picks the antecedent when several candidates
  exist. Plain recency contradicts those rulings (Feral Contest, Kalitas,
  Twinflame, Ram Through).
- **Docs assume:** `grammar.md` §5 is the single home of the procedure
  (`queries.md` §3 points to it). Filter the candidates, then take the most
  recently introduced one left. Filter 1: drop a candidate that is another
  argument of the pronoun's own verb. Filter 2: drop what another anaphoric
  expression in the same sentence already took. Filter 3: drop a candidate
  that can't fill the word's slot in its current zone. Tie-break: read recency
  by clause; the nearest clause that introduces a candidate wins, and within
  it the subject beats the object, which beats an oblique. Recency counts
  introductions (target and indefinite noun phrases), not re-mentions. If two
  same-kind candidates still survive, report ambiguity rather than guess. A
  few sentences of the same shape still need card-specific bindings.
- **Alternatives:** recency only; subject, then object, then oblique; report
  ambiguity and require a card-specific binding whenever two candidates
  survive; per-card annotation.

### UD-33 — Same-effect tracking into hidden zones — category: assumed

- **CR says:** the 400.7 exceptions that let an effect find a moved object are public-only (400.7e, 400.7j, 400.7k; 701.17c); 608.2h gives LKI for an object moved from a public to a hidden zone; 701.9c leaves an unrevealed hidden-zone discard's characteristics undefined; 121.6c and 614.11b presuppose additional actions on a card after it's drawn. The hidden-zone reach of 603.6e and 903.3e is specific to Aura triggers and commanders.
- **Open:** whether and how an effect finds a card it moved into a hand ("Draw a card and reveal it. If it isn't a land card, discard it."; Instrument of the Bards).
- **Docs assume:** `queries.md` §3: tracked for the rest of the effect.
- **Alternatives:** no tracking (breaks the printed "reveal it, then act on it" lines); tracking only for revealed cards.

### UD-34 — Extent of a station band in MTGJSON text — category: assumed

- **CR says:** a station symbol represents a static ability, and "any
  abilities printed within the same text box striation as a station symbol
  are part of its static ability" (721.2); `{N+}[abilities]` means "as long as
  this permanent has N or more charge counters on it, it has [abilities]"
  (721.2a); a striation with a P/T box adds base power and toughness (721.2b).
  The striations have no other game significance (721.3).
- **Open:** MTGJSON's `text` flattens the striations and carries `N+ | ` only
  on the first line of each one, so which following lines belong to the band
  is not in the data. The P/T box is not in `text` either.
- **Docs assume:** a band is the `N+ | ` line plus the unmarked lines after
  it, up to the next `N+ | ` line or the end of the text; the card's
  `power`/`toughness` belongs to the highest threshold (`grammar.md` §2).
  Every supported station card fits (ordinary abilities precede the `Station`
  line; the first row follows it).
- **Alternatives:** the marked line only (loses the unmarked abilities that
  follow the last band on 10 supported cards); take the striation boundaries
  from a layout-bearing data source instead of inferring them.

### UD-35 — Once-per-turn trigger and replacement templates — category: assumed

- **CR says:** the general once-per-turn rules are 602.5b-c (activation
  restrictions, with keyword instances in forecast 702.57b and boast 702.142a),
  603.2h ("Do this only once each turn"), and the ability text quoted in
  702.179d. No rule defines the ordinal-within-turn trigger or replacement
  wordings ("the first time each turn", "your second card each turn"), nor the
  generic "This ability triggers only once each turn" cap that 702.179d uses
  without defining it.
- **Open:** whether the ordinal wordings are event-history tests or
  per-ability counts, and whether the cap counts triggerings or actions.
- **Docs assume:** the official rulings' reading (`temporal.md` §4): ordinal
  wordings test the turn's event log, so an earlier matching event uses up
  "first" even before the source was present, and declining the replacement
  form uses it up. The cap counts the ability's own triggerings whether or not
  they resolve (Elvish Warmaster [2021-02-05]).
- **Alternatives:** a per-ability flag, which diverges when the first event
  precedes the source or the ability's function, or when the replacement is
  declined.

### UD-36 — Echo window with no earlier upkeep — category: assumed

- **CR says:** 702.30a anchors on "your last upkeep", and no rule supplies a
  referent when the player has had no earlier upkeep (for example, a
  flashed-in echo permanent before the second player's first upkeep).
- **Open:** what "your last upkeep" refers to in that case.
- **Docs assume:** the window runs from the game's start (`temporal.md` §2).
- **Alternatives:** the condition is false, so echo is dodged.

### UD-37 — "Only after [combat point]" when the point is skipped — category: open

- **CR says:** a spell may state it can be cast "only [before/after] [a particular point in the combat phase]" (506.8), and 506.8g extends this to abilities. Skipped points get rules in only two cases. "Only before [point]" closes when the declare attackers step ends if the declare blockers and combat damage steps are skipped, or when the precombat main phase ends if the relevant combat phase is skipped (506.8e; skip condition 508.8). "Only during combat after blockers are declared" can't be cast in a combat phase whose declare blockers step is skipped (506.8f). With several combat phases, a before/after restriction refers to the turn's first combat phase unless it also says "during combat" or "during a certain player's combat phase" (506.8c-d).
- **Open:** "only after [point]" when that point is skipped. Glyph of Reincarnation ("Cast this spell only after combat.") in a turn whose combat phase is skipped is the printed instance. 506.8e covers only "only before", and 506.8f only the "during combat after blockers are declared" form. Whether the point counts as never reached, as reached where the skipped phase or step would have fallen, or as vacuous, the CR doesn't say.
- **Docs assume:** nothing. `turn.md` §3 states the gap and commits to no reading.
- **Alternatives:** never castable that turn, since the point never occurs and "after" never begins. Castable from where the skipped point would have fallen (for example after the precombat main phase ends), which extends 506.8e's fallback for "before". Castable at any time, treating the restriction as vacuous. Observable only in turns where the relevant combat phase or step is skipped.

### UD-38 — Is an attacked battle still "attacked" after combat is ended early? — category: open

- **CR says:** the normal end of combat step removes all creatures, battles and planeswalkers from combat (511.3). The end-the-turn and end-the-combat-phase procedures remove only creatures and planeswalkers (724.1d, 724.2d). Several rules key on whether a battle "is being attacked". 310.11 defers the protector-repair state-based action for "a battle that isn't being attacked". 310.9d and 506.4e also refer to "a battle that's being attacked". 704.5x instead keys on whether "attacking creatures are currently attacking that battle", and none remain after an early end (508.1k).
- **Open:** whether a battle that was being attacked still counts as "being attacked" once 724.1d or 724.2d has removed its attackers from combat, given that those rules omit battles from the removal. This is observable chiefly through 310.11's "a battle that isn't being attacked", and likewise through 310.9d and 506.4e.
- **Docs assume:** nothing. `turn.md` §6 flags the gap.
- **Alternatives:** derive "being attacked" from the attacking creatures present, so an early end behaves like 511.3 and the battle stops being attacked. Or store it as a state set at declaration and cleared only by 511.3, so after an early end the battle stays attacked with no attackers, and 310.11's repair keeps deferring while 704.5x can already fire.

### UD-39 — APNAP order and "the active player" with concurrent turns — category: open

- **CR says:** the active player is the player whose turn it is (102.1), and APNAP order (101.4) and the trigger-ordering process (603.3b) are built on one active player. In Grand Melee each turn marker represents an active player's turn (807.4), so several players are active at once; each turn marker has its own stack (807.5). A player gets priority for a stack only if its turn marker, or an object on it, is within their range of influence (807.5a). A player with priority for several stacks says which stack a new spell or ability goes on, with fixed placement for triggers caused by a stack object, copies, and targeting (807.5b). 805.9 (shared team turns) and 101.4e (starting the game) do not reach several concurrent active players.
- **Open:** how APNAP order and "the active player" resolve when several players are active players at once. For example, which active player goes first when several simultaneous triggers need ordering, or what an effect that says "the active player" refers to.
- **Docs assume:** nothing. `variants.md` flags it at the Grand Melee rows (state.md 807.4, events.md batching, choices.md APNAP).
- **Alternatives:** the active player of the turn marker whose stack holds the resolving object, or onto which the triggers go (807.5b); otherwise an active player among the choosers goes first, then the rest in turn order.

## Settled

Former candidates refuted by a specific rule — or, where the CR fixes
behavior but not representation, pinned by a recorded project policy
(`settled-by-policy`) — kept with the resolving cite or policy so the
question isn't re-litigated. Entries retired before the UD rename keep
their original ids (S1, U2, U3, U5); entries retired from the registry
keep their UD ids.

### S1 — Oracle paragraph segmentation — category: settled

(candidate: `grammar.md` §1's one-paragraph-one-ability unit is mere
formatting practice). Settled by
**113.2c**: "each paragraph break in a card's text marks a separate
ability," with the strung-on-one-line keyword carve-out (each keyword
still its own ability; 113.2c with rule 702's per-keyword rules), modal
bullets as one ability (700.2), rules-inert ability words (207.2c), and
an explicit multi-line-one-ability statement for dice — roll
instruction, same-paragraph modifiers, result-contingent instructions,
and results table "are all part of one ability" (706.3b). Only the data
encoding (MTGJSON `\n` ↔ paragraph break) and parsing heuristics remain
conventional — corpus-format properties, not CR semantics.

### U2 — Agent attribution for rules-performed events — category: settled

(retired; was: does SBA destruction for lethal damage attribute the
damage's source as the destroying agent?). Settled by **120.5**:
"likewise, the source of that damage doesn't destroy it," and the
rule's own example closes
it — "Neither Lightning Bolt nor the damage dealt by Lightning Bolt
destroyed that creature." Karmic Justice-style "a spell or ability an
opponent controls destroys" predicates never see lethal-damage or
deathtouch SBA kills (704.5g, 704.5h); TBA/SBA events carry no agent
(703.2, 704.2) — `events.md` §3's agent=None commitment and log-join
treatment of dies-from-damage wordings were already CR-correct.
Residue — nullable field vs. synthetic "game rules" agent — is
`representation-only`: behavior fixed, pin it (docs keep nullable).

### U3 — Vigilance: procedure carve-out vs. cause-tagged replacement — category: settled-by-policy

(retired, `settled-by-policy`; was `representation-only`: the CR fixes
behavior — attack-taps aren't a cost, "attacking simply causes
creatures to become tapped," 508.1f, and "attacking doesn't cause
creatures with vigilance to tap," 702.20b — leaving only the engine
representation open: null replacement on
tap(cause: attack-declaration) vs. hardcoding in the declare-attackers
procedure). No CR rule settles it; the **dependents threshold**
(`keyword-classification.md`, Primitive basis) settles it as project
policy: with the Enlist record corrected to its CR-named hooks
(702.154b), `cause-tagged-events` held exactly one keyword dependent,
so the primitive was retired and vigilance classified **intrinsic** —
the procedure carve-out reading, mirroring 702.20a's own framing ("a
static ability that modifies the rules for the declare attackers
step") and 614.1's functional replacement-effect definition, which never
admits the exemption. The cause-tagged null replacement is kept as the
documented alternative (`events.md` §3 — the hypothetical
decomposition). Reopens as a *new* UD-number if a printed card makes
the divergence observable (a tap-rewrite that must order against the
exemption, 616.1, 614.5) or a second cause-tag consumer re-mints the
primitive.

### U5 — Base semantics of "can't lose" / "can't win" — category: settled

(retired; was: does "can't lose" gate the outcome while the condition
holds, or cancel each loss event?). Settled by **101.2 + 704.3 + per-SBA
wording**: a "can't" takes precedence only while applicable (101.2 —
precedence, not consumption); the SBA loop re-checks every condition
at each would-get-priority, consuming nothing (704.3); so survival
past the effect's end is decided by each SBA's own predicate. 704.5a
and 704.5c are standing state predicates ("has 0 or less life," "has
ten or more poison counters") — still true at the first check after
the effect ends, the loss fires then. 704.5b is a *windowed event*
predicate ("attempted to draw … since the last time state-based
actions were checked") — the window lapses at the next check: no
retroactive empty-draw loss once can't-lose ends. Rulings corroborate
(`scripts/rulings`): Abyssal Persecutor [2017-11-17] — an opponent at
0 or less life when it leaves the battlefield "will lose the game as
a state-based action"; Phyrexian Unlife [2011-06-01] says the same of
its own controller. `outcomes.md` §2 carries the split.

### UD-40 — Source and controller of dash, blitz, and warp delayed triggers — category: settled

(candidate: dash, blitz, and warp each represent "two static abilities
that function while the card … is on the stack, one of which may create a
delayed triggered ability" (702.109a, 702.152a, 702.185a). That creator
seems to fit none of 603.7a's three paths, and 603.7g covers only a static
that "allows a player to take an action and creates a delayed triggered
ability if that player does so", a pair the keyword splits across two
statics, leaving source and controller to the engine.) Settled by
**608.3g**: when the resolving object "has a static ability that functions
on the stack and creates a delayed triggered ability, that delayed
triggered ability is created as that permanent is put onto the
battlefield", and the rule names dash, blitz, and warp. Creation therefore
happens during the spell's resolution, 603.7a's first path, so **603.7d**
applies: the source is the spell, and the controller is "the player who
controlled that spell as it resolved." The 603.7f–g analogues give the same
answer, because the object with the static is that spell and its controller
at the moment of creation is the controller the permanent enters under
(608.3a, 608.3c). Nothing is created at casting. A countered dash spell
leaves no delayed trigger. If Aethersnatch ("Gain control of target
spell") takes a blitz spell, its new controller controls the end-step
trigger and sacrifices the permanent, which only its controller may do
(701.21a). Rebound is a different case: its static is a replacement
("instead of putting it into your graveyard as it resolves", 702.88a), so
603.7f governs. The hunt misses 608.3g because the CR's cross-references
for delayed-trigger source and controller point only to "rules 603.7d–f"
(113.7, 113.8, 603.3a, 109.4b).

### UD-41 — Scope of the 603.2h once-per-turn flag — category: settled

(candidate: the CR text of 603.2h leaves open what the "only once each turn"
flag is keyed to, and whether instances already on the stack still do
anything once the action is taken). Settled by official rulings, not by a
CR rule: 603.2h counts the action "its source's controller has … taken" that
turn, and the rulings key it to the ability on its source, not to the
controller alone or to each triggered instance (Nykthos Paragon [2021-06-18]
"refers only to the ability it is attached to, not other instances of the same
ability"; Riveteers Ascendancy [2022-04-29]), let declining a "may" leave it
free to trigger (Legolas, Counter of Kills), and make instances already on the
stack do nothing once the action is taken (Calix, Guided by Fate [2023-05-12];
Spider-Verse [2025-09-19]). The resolution-time gate is not in 603.2h. Reopens
under a new UD-number if a CR refresh rewrites 603.2h.

## Maintenance

On every CR refresh:

1. **Re-run the refutation hunt per entry.** Each entry's "CR says" cites
   mark where a settling rule would appear: `scripts/rule` those numbers,
   then `scripts/rule-search` the entry's key phrases. Give each new entry
   its own line here. The CR writes "can't" with U+2019, so an ASCII
   apostrophe matches nothing; use a regex dot.
   - UD-1: "snow"
   - UD-4: "same zone", "from the stack"
   - UD-6: "undefined", "can.t be determined", "no value", "fails to
     determine"
   - UD-7: "concede", "leaves the game"
   - UD-8: "at random", "equally likely", "equal likelihood"
   - UD-9: "last known information"
   - UD-10: "reverse", "restart", "subgame"
   - UD-11: "game state", "loop"
   - UD-12: "simultaneous", "single event"
   - UD-13: "becomes attached"
   - UD-14: "untap step"
   - UD-15: "must be blocked", "combat
     requirement"
   - UD-16: "characteristic-defining ability"
   - UD-17: "state-based actions are performed"
   - UD-18: "neither day nor night"
   - UD-19: "additional cost", "intentions to pay"
   - UD-20: "qualities to change",
     "as though it had flash"
   - UD-21: "goaded", "has no effect"
   - UD-22: "planar controller"
   - UD-23: "protector", "being attacked"
   - UD-24: "in addition to its other"
   - UD-25: "special action", "doesn.t resolve"
   - UD-26: "commit a crime", "copy of an ability"
   - UD-27: "Phyrexian mana symbol"
   - UD-28: "otherwise reordered", "revealed cards"
   - UD-29: "a variant of"
   - UD-30: "designations that the game itself can
     have", "speed"
   - UD-31: "another target", "any other target"
   - UD-32: "rules of English"
   - UD-33: "reveal it", "hidden zone"
   - UD-34: "striation"
   - UD-35: "only once each turn", "each turn"
   - UD-36: "your last upkeep"
   - UD-37: "only before", "only after"
   - UD-38: "being attacked"
   - UD-39: "active player", "turn marker"
   - UD-41 (settled by rulings): "only once each turn"
2. A new rule that settles an entry **moves it to Settled** with the
   resolving cite — never delete; the ID stays, retired.
3. New entries take the next UD-number; never renumber, never reuse.
4. If a "Docs assume" doc changes its commitment, flip the status
   (`assumed` ↔ `open`) in the same change; `representation-only` retires
   when a printed card makes the divergence observable — or when a
   recorded project policy pins the representation (mark the retirement
   `settled-by-policy`; if the question later becomes observable, it
   reopens under a new UD-number).
5. `scripts/cite check` (this doc is covered by its source globs) must
   exit 0.
