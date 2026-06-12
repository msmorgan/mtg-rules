# Underdetermined — The Engine-Choice Registry

*Synthesized from the Comprehensive Rules effective 2026-04-17
(`data/rules/cr.json`). Orientation only — verify load-bearing specifics
with `scripts/rule` before citing. Run `scripts/cite check` after CR
refreshes.*

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
  production and payment within one step or phase (106.4).

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

### UD-6 — One undefined value (⊥) behind seven per-case rules — category: assumed

- **CR says:** per-case handling only — undetermined number → 0 (107.2);
  undefined choice → that part does nothing (607.5a); undefined mana type
  → no mana (106.5); undefined commander color identity → that part does
  nothing, referencing costs unpayable (903.4f); undefined search quality
  → can't find (701.23c); undefined attach target → stays put (301.5e,
  303.4i); card discarded face-down into a hidden zone → *all*
  characteristics "considered to be undefined" (701.9c).
- **Open:** the general principle — what a *novel* undefined case does —
  and precedence when the coercions collide: a number computed from an
  undefined choice could read 0 (107.2) or skip that part (607.5a).
- **Docs assume:** a single ⊥ with two coercions — ⊥→0 in numeric
  position, ⊥→no-op in choice position (`queries.md` §4, §7).
- **Alternatives:** keep seven unrelated cases (no extrapolation power).
  On collisions the 903.4f precedent cuts both ways: skip-beats-zero —
  the undefined color count does nothing rather than read 0 — or the
  *printed exception proving the 107.2 default*: a dedicated rule was
  needed precisely because 107.2 would otherwise coerce to 0, so novel
  collisions default to 0 and skips exist only where printed. Pick one.

### UD-7 — Concession granularity — category: open

- **CR says:** "A player can concede the game at any time"; they leave
  immediately and lose (104.3a). Leave-game cleanup happens "as soon as
  the player leaves the game," explicitly *not* a state-based action
  (800.4a); in a two-player game the game simply ends (104.1).
- **Open:** what "at any time" means against atomic operations. CR events
  have no internal timeline: can a concession land mid-resolution,
  between replacement applications, or inside the 704.3 SBA batch — and
  what state does 800.4a's cleanup run against if it does?
- **Docs assume:** nothing — no doc commits to interruption points.
- **Alternatives:** coarse — concession takes effect at the next event
  boundary (clean atomicity; "immediately" weakened, and a player can't
  concede to deny a mid-resolution disclosure); fine — interruptible
  anywhere (honors 104.3a literally; the engine must define
  partially-applied-event semantics 800.4 never anticipated).

### UD-8 — "Random" means what distribution? — category: open

- **CR says:** dice *are* distribution-fixed: an N-sided die "must have N
  equally likely outcomes" (706.1a); substitute methods need "the same
  number of equally likely outcomes" (706.1b). Everything else isn't:
  sticker sheets are chosen "at random" (103.2d), a face-down exiled card
  may be picked "at random" (406.4), and shuffle is defined
  *epistemically* — "randomize the cards … so that no player knows their
  order" (701.24a); MTR 3.10 is the same epistemic test ("no player can
  have any information"). There is no glossary entry for "random."
- **Open:** narrower than it looks — uniformity for the "at random"
  choices and shuffle outcomes; independence across successive random
  events; and verifiability — 701.24a's no-player-knows condition
  constrains implementations beyond any distribution (a predictable PRNG
  seed violates it even with uniform outputs).
- **Docs assume:** nothing distributional — `information.md` §5 treats
  RNG only as a discloser.
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
  controller, status, and counters are clearly in — but do attachments,
  choices made for the object, and history-dependent quantities (damage
  marked, "this turn" facts) ride along? The CR never draws the line;
  consumers name fields case by case (702.2e, 702.15c, 701.44c, 701.50c,
  800.4i).
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
  un-learned" is read as 733.1's rationale; rewinds restore state, never
  views (`information.md` §5, §6). MTR 4.8 corroborates: a judge may
  reverse a decision only if the player "has not gained any information
  since taking the action" — policy already treats knowledge as
  unrevertible.
- **Alternatives:** reset views to the restored state (coherent for
  replay and AI self-play; models humans as forgetting, contradicting
  the rationale the docs read out of 733.1 and MTR 4.8).

### UD-11 — Game-state equality — category: open

- **CR says:** behavior is predicated on state *identity* in four
  places: a "loop" of mandatory actions "repeating a sequence of events
  with no way to stop" is a draw (104.4b; limited-range variants 104.4f,
  801.16 draw only the involved players), and a fragmented loop is
  detected by "the same game state being reached multiple times,"
  obligating a different choice (732.3). Yet "game state" has no
  glossary entry and no rule defines when two states are the same; MTR
  4.4 leans on the same undefined notion ("not meaningfully changing,"
  "a previous game state (or one identical in all relevant ways)").
- **Open:** the equality predicate — which components count. Zones,
  life, counters, designations, and per-object status clearly do; but
  turn/phase position (always advancing across turn-spanning loops),
  timestamps, the event log, floating mana, and revealed-knowledge
  differences must each be ruled in or out — include everything and no
  two states are ever equal, so 104.4b and 732.3 never fire.
- **Docs assume:** nothing — `outcomes.md` §3 names the mandatory-loop
  monitor but no doc defines its equality test.
- **Alternatives:** structural equality over a pinned component list
  (MTR 4.4's "identical in all relevant ways" made explicit);
  equivalence modulo declared-irrelevant components; event-sequence
  equality per 104.4b's "sequence of events" framing (detects loops
  without comparing whole states).

### UD-12 — Intra-batch event ordering — category: assumed

- **CR says:** batches are single simultaneous events — all SBAs in a
  check are performed "simultaneously as a single event" (704.3); all
  assigned combat damage is dealt simultaneously (510.2) — and every
  order-sensitive consumer is settled by its own rule, never by
  intra-batch position: simultaneous timestamps go in APNAP order
  (613.7m), the batch's triggers stack in APNAP order (603.3b), LKI for
  batch departures snapshots the pre-batch state (704.8).
- **Open:** whether intra-batch order is *observable at all*. The CR's
  answer pattern says no — but a totally ordered log invents an ordering
  the game cannot see, and any consumer that reads it (replay,
  diagnostics, a future "first"/"last" wording) bakes the invention in.
- **Docs assume:** a total order — `events.md` §7 commits
  `ordering: int` (commit order within the log, 608.2i).
- **Alternatives:** batch-scoped ordering — a batch id plus unordered
  members, so simultaneity is representable and 613.7m/603.3b/704.8
  consume their own rules, not log position; or keep the total int but
  pin that nothing rules-facing may read relative order within a batch.

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
step") and 614.1's closed replacement-effect definition, which never
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

## Maintenance

On every CR refresh:

1. **Re-run the refutation hunt per entry.** Each entry's "CR says" cites
   mark where a settling rule would appear: `scripts/rule` those numbers,
   then `scripts/rule-search` the entry's key phrases ("snow", "at
   random", "last known information", "undefined", "game state", "loop").
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
