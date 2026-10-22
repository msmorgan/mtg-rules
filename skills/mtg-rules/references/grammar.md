# Oracle Text — Grammar for Parsing

*Synthesized from the Comprehensive Rules effective 2026-09-25
(`data/rules/cr.json`).*

How to slice an Oracle-text string into abilities and recognize each one's
surface form. Terminal vocabularies live in `data/catalogs/*.json` and
`data/rules/keywords.json`; CR rules cited here govern what the forms *mean*.
Every oracle example below is real text fetched via `scripts/card` or
`scripts/corpus`. For what the abilities *do*, see `abilities.md`; for
replacement-effect semantics see `effects.md` §6.

## 1. Segmentation

MTGJSON's `text` field separates paragraphs/lines with `\n`. The default
unit is **one paragraph = one ability** — CR rule, not formatting
convention: "each paragraph break in a card's text marks a separate
ability" (113.2c) — but these cases break that:

- **Comma-separated keyword line = multiple abilities.** Keyword abilities
  written on one line, separated by commas (or whitespace), are each a
  separate ability — 113.2c's own carve-out for "certain defined abilities
  that may be strung together on a single line". Split on `, ` *within* a
  line only when every token resolves to a keyword in the catalogs.
- **Modal blocks span lines.** A modal header (§6) plus its modes (`•`, `+
  {cost} —` or `{P}… —` lines) is *one* ability with multiple modes (700.2);
  do not split the bullets into separate abilities.
- **Anchor-word bullets are not modes.** Take `As this enchantment enters,
  choose Khans or Dragons.` followed by `• Khans — At the beginning of each of
  your main phases, add {G}{G}.` and a `• Dragons — …` bullet. This is a
  replacement effect that offers two words, plus one ability per bullet.
  "[Anchor word] — [ability]" means "As long as [anchor word] was chosen as
  this permanent entered the battlefield, this permanent has [ability]," and
  each bullet is linked to the ability that offers the choice (614.12c,
  607.2m). Emit each bullet as its own conditional static grant. It is not a
  mode (the word is chosen as the permanent enters, not while casting or
  putting an ability on the stack, 700.2a-b), and it is not an ability or
  flavor word: stripping the label would make both abilities unconditional.
  Recognize the block by bullets labeled with exactly the words that the `As …
  enters, choose A or B.` sentence offers. The sentence alone isn't enough:
  Roots of Life's `As this enchantment enters, choose Island or Swamp.` is a
  subtype choice that a later "the chosen type" reads back (607.2d). Anchor
  words are in neither `ability-words.json` nor `flavor-words.json`. Words
  attested so far (supported corpus; the set is open): Khans, Dragons, Abzan,
  Jeskai, Mardu, Sultai, Temur, Mirran, Phyrexian, Brotherhood, Enclave, NCR,
  Legion, Believe, Doubt. (14 supported cards, 28 bullet lines. 607.2m ends
  "See rule 614.12b", which is a CR cross-reference oddity.)
- **Line-initial labels.** A `Label — text` prefix does not always lack rules
  meaning. Ability words and flavor words (207.2c, 207.2d) are stripped, but
  anchor words, keyword labels, mode costs and die-result labels are rules
  text. Classify the label by §3 "Line-initial labels" before stripping
  anything.
- **Reminder text is not rules text.** Reminder text is italic text in
  parentheses that summarizes a rule and has no game function (207.2, 207.2a).
  It may sit on its own line when it applies to an aspect of the card other
  than an ability (207.2a). MTGJSON's `text` carries no italics, so the
  parentheses are the only marker. Discard reminder text before parsing (but
  see §3: it may be the only place a keyword's parameters are spelled out in
  plain English). Short glosses count as reminder text too: `You get {E}{E}
  (two energy counters).`, `You get {TK} (a ticket counter).` A few mid-line
  parentheticals restate a rule default rather than explain a keyword.
  Discarding them is safe only if the engine implements that default:
  - `(as long as this creature is on the battlefield)` (Warbringer,
    Alhammarret; 113.6 — for Warbringer the engine must also not treat it as a
    113.6d–e self-cost ability: "Warbringer's first ability doesn't affect
    Warbringer itself", ruling 2015-02-25);
  - `(if it's still on the battlefield)` (Gideon's Sacrifice; 614.9);
  - `(even if this card isn't on the battlefield)` (Mistform Ultimus; 113.6a);
  - Eluge's `costs {U} (or {1}) less` (118.7b–c; ruling 2024-07-26);
  - `return it to the battlefield (front face up)` on the back faces of
    double-faced cards (712.14).

  A parser that reproduces text must keep them. Flag an unrecognized mid-line
  parenthetical for review instead of dropping it silently (**engine
  inference**).
- **Quoted abilities are abilities of their own.** A quoted span after
  `has`/`have`/`gains`/`gain` (113.1a, 113.10), after `loses`, or after `with`
  in a token or emblem description is a complete ability, often one item in a
  list. Parse it recursively as its own paragraph (activated, triggered, or
  static), and classify the host line by its unquoted text only. In the
  supported corpus, 382 lines have a `:` only inside quotes, such as
  `Enchanted creature has "{1}, Discard a card: Untap this creature."`, which
  is a static grant, not an activated ability. Another 382 have
  When/Whenever/At only inside quotes, such as `[0]: Create a 1/1 red Devil
  creature token with "When this token dies, it deals 1 damage to any
  target."`, which is a loyalty ability. Activation instructions inside the
  quotes belong to the granted ability (113.10a). Inside the quote, `this
  [type]` means the object that has the ability, while a card name naming the
  granting source means that one source object (201.5a, Gutter Grime example).
  A quote nested inside a quote uses single quotation marks (the next nesting
  level): `You get an emblem with "Swamps you control have '{T}: Add
  {B}{B}{B}{B}.'"`. Not every quoted span is an ability: quotes also mention
  wording (`loses all "bands with other" abilities`, `The "legend rule"
  doesn't apply …`) or name a cost (`an additional "Sacrifice a Swamp"`). When
  a quoted ability ends its host sentence, the period inside the closing quote
  ends both. No CR rule mentions quotation marks; this is Oracle layout
  (corpus).
- **Square brackets are cleave text**, unless they enclose a loyalty symbol
  (§2). Cleave means "If this spell's cleave cost was paid, change its text by
  removing all text found within square brackets in the spell's rules text"
  (702.148a), and that is a text-changing effect (702.148b). Keep the
  bracketed spans and build both readings. Choose between them by whether the
  cleave alternative cost was chosen. When it was, targets are chosen under
  the shorter text (601.2c: "a spell may require alternative targets only if
  an alternative or additional cost was chosen for it"). Ruling
  `[2021-11-19]`: a spell cast for its cleave cost "doesn't have any of the
  text in square brackets while it's on the stack." Real: `Return target
  nonland permanent [you control] to its owner's hand.` (Alchemist's
  Retrieval); `Search your library for a [basic land] card, [reveal it,] put
  it into your hand, then shuffle.` (Dig Up). The supported corpus has 12 such
  lines, all on cleave cards.
- **Keyword em-dash templates, anchor words and striated-box markers are not
  ability words.** Cards with a striated text box prefix their abilities with
  structural markers that *look* like the `Word — text` form but are keyword
  abilities, not ability/flavor words:
  - **Saga chapters** — a line `^[IVX]+(?:, [IVX]+)* — ` (Roman-numeral
    chapter symbol; may carry a second `Word — ` flavor-word prefix after it,
    e.g. `I — Aerial Blast — …`) is a chapter ability = a **triggered**
    ability (714.2; `{rN}—[Effect]` = "When … lore counters … became at
    least N, [effect]", 714.2b; `{rN1}, {rN2}—` = both, 714.2c). Do **not**
    treat the numeral as an ability word.
  - **Class level bars**, **Leveler bands** and **Station bands** open their
    own bands — see §2.
- **A die roll and its results table form one ability.** The CR says "An
  instruction to roll one or more dice, any instructions to modify that roll
  printed in the same paragraph, any additional instructions based on the
  result of the roll, and the associated results table are all part of one
  ability" (706.3b; `underdetermined.md` S1). Each row means "If the result
  was in this range, [effect]" (706.3a). The rows follow the line that rolls
  the die, and that line keeps any label prefix it has (`Psionic Spells — When
  this creature enters, choose target instant or sorcery card in your
  graveyard, then roll a d20.`). Row forms:
  - bar rows: `N | `, `N1—N2 | ` and `N+ | ` (706.3a), plus `N or less | `,
    which 706.3a does not list (`9 or less | Put those cards into your hand,
    then shuffle.`, Druid of the Emerald Grove). Pattern: `^\d+([—–-]\d+|\+)?
    \| `;
  - six-sided-die lists: `N — ` and `N or M — ` (`5 — Destroy it.`, Six-Sided
    Die; `1 or 2 — [+2], then create two 1/1 green Squirrel creature tokens.
    …`, Comet, Stellar Pup), sometimes bulleted (`• 2 — menace`, Celebr-8000).
    Patterns: `^\d+( or \d+)? — `, `^• \d+ — `.

  Range glyphs vary: 706.3a prints an en dash (`N1–N2`), but MTGJSON stores an
  em dash (`1—9 | You may put that card on top of your library.`, Aberrant
  Mind Sorcerer) or an ASCII hyphen (`1-9 | Each player draws a card.`,
  Mathise, Surge Channeler). Match `[—–-]`. A row can carry its own flavor
  word (`1 | Trapped! — You lose 3 life.`, Treasure Chest); strip it before
  parsing the effect. Never split the rows into separate abilities, and never
  strip `N — ` as a flavor word. An `N+ | ` row below a `Station` line is a
  station striation, not a result (§2).

### Worked example — Questing Beast

Raw `text` (4 `\n`-separated lines), classified by §2 rules:

```
Vigilance, deathtouch, haste                                    ← keyword line
Questing Beast can't be blocked by creatures with power 2 or less.   ← static
Combat damage that would be dealt by creatures you control
  can't be prevented.                                           ← static
Whenever Questing Beast deals combat damage to an opponent, it
  deals that much damage to target planeswalker that player controls. ← triggered
```

Line 1 is a comma-separated keyword line → **3 keyword abilities**
(vigilance, deathtouch, haste). Lines 2–3 are declarative sentences →
**2 static abilities** (113.3d). Line 4 begins with "Whenever" →
**1 triggered ability** (113.3c). Total: 3 keyword + 2 static + 1 triggered.

## 2. Surface forms by ability kind

Four categories (113.3). Classify a paragraph by its surface shape:

- **Activated** — `"[Cost]: [Effect.] [Activation instructions (if any).]"`
  (113.3b, 602.1). The cost is everything *before* the colon (602.1a). Text
  after the colon that restricts/permits activation ("Activate only as a
  sorcery", "Activate only once each turn") is an **activation instruction**,
  not part of the effect, and appears last (602.1b). Marker: a top-level
  `:` that is not inside parentheses, `{…}` symbols or double-quoted spans. Do
  not treat a top-level apostrophe as a quote.
  - **Loyalty abilities** — `[<cost>]: [effect]` where the bracketed cost is
    `+N`, `0`, `−N` or `−X` are planeswalker loyalty abilities, a special kind
    of **activated** ability (606.1; an activated ability with a loyalty
    symbol in its cost, 606.2). Real: `[+1]: Add {R}. …`, `[0]: …`,
    `[−10]: …`.
    CRITICAL: the minus in these corpus lines is **U+2212 MINUS SIGN** (UTF-8
    `e2 88 92`), *not* ASCII hyphen `-` — a regex matching `\[-N\]` finds
    **zero** corpus lines; match `\[(\+|−)?([0-9]+|X)\]:` (or the literal
    `−`).
    Loyalty symbols also appear away from the start of a line:
    - variable costs: `[−X]: Chandra deals X damage to each creature.`
      (Chandra, Flamecaller; the value of X is chosen on activation, 107.3a);
    - cost modifiers: `Planeswalkers' loyalty abilities you activate cost an
      additional [+1] to activate.` (Carth the Lion). 107.7: "Loyalty symbols
      may also appear in abilities that modify loyalty costs";
    - instructions inside an effect: `3 — [−1], then return …` (Comet, Stellar
      Pup). `[+N]`/`[−N]` mean put or remove N loyalty counters (107.7);
    - quoted granted abilities: `Planeswalkers you control have "[−10]: …"`
      (Avatar of Burgeoning Echoes).

    Only a symbol followed by `:` at the start of a line or of a quoted
    ability opens a loyalty ability (606.2). 107.7 itself writes `[-N]` with a
    hyphen, and P/T changes use the ASCII hyphen-minus (`-1/-1`; no supported
    line has U+2212 before a slash). A regex keyed to one minus glyph misses
    the other, so accept both; the corpus itself has 0 lines starting `[-`.
- **Triggered** — `"[When/Whenever/At] [trigger condition], [effect].
  [Instructions (if any).]"` (113.3c, 603.1). Begins with **When**,
  **Whenever**, or **At**. Trailing instructions (target limits, "can't be
  countered") function on the stack and are not the effect (603.1a).
  - **Several trigger conditions** (603.1b, 113.6k): `At the beginning of your
    upkeep and whenever you cast a black spell, put a charge counter on this
    artifact.` One triggered ability can have several trigger conditions, each
    with its own introducer or sharing one. It is one ability (113.2c), not
    two, and it triggers once each time any listed event occurs (603.2c).
    Real: `When this creature enters and whenever it attacks while saddled,
    create a 3/3 green Elephant creature token.` (Autarch Mammoth); `When you
    cycle this card and when this creature dies, you may create a 1/1 white
    Soldier creature token.` (Bant Sojourners); `… or when they attack you or
    a planeswalker you control, sacrifice this Aura.` (Tenuous Truce); a
    shared introducer: `Whenever Eluge enters or attacks`, and 113.6k's own
    example `When this creature enters or the creature it haunts dies, …`
    (Absolver Thrull). Each condition can function from a different zone
    (113.6k; `abilities.md` §3). A second trigger word (`and when`, `and
    whenever`, `and at the beginning`, `or when`) always opens a new
    condition. `or` joining two event clauses is also two conditions. Never
    split before `and at least`: `Whenever Arthur and at least one other
    creature attack, …` is one condition with a compound subject. A parser
    that reads only the first introducer folds the second condition into the
    first event. 603.1b also allows an instruction that asks whether "all" of
    the conditions happened during a period; that checks the events
    themselves, whether or not the ability triggered on them. Delayed triggers
    created inside an effect (`Until end of turn, whenever …`) are covered in
    `abilities.md` §2 (603.7).
  - **Trigger words later in the paragraph**: a When/Whenever/At clause that
    doesn't open its paragraph is usually a delayed triggered ability that the
    effect creates, inside the same ability. This covers clauses after another
    sentence, after an activation-cost colon, after a loyalty cost, or inside
    a Saga chapter's effect. Per 603.7, a delayed trigger contains "when,"
    "whenever," or "at," "although that word won't usually begin the ability."
    Real: `{1}, {T}: When you next cast an instant or sorcery spell with mana
    value less than or equal to Loki's power this turn, copy that spell.`;
    `[−2]: When you next cast a creature spell this turn, search your library
    …`; `II, III — Whenever you cast a spell this turn, put a +1/+1 counter on
    target creature you control.` It triggers once unless it has a stated
    duration such as "this turn" (603.7b). `When you do` and `When … this way`
    are reflexive triggers (603.12). Not delayed: a second trigger condition
    joined to the opening one by `and`/`or` (603.1b; see **Several trigger
    conditions**), and a trigger word right after any structural prefix — a
    stripped ability/flavor word, a keyword dash prefix (`Max speed — `, `∞ —
    `, `Solved — `), an anchor-word bullet, or a station threshold `N+ | ` —
    which opens the ability that prefix carries (`Landfall — Whenever …`, `10+ |
    Whenever you attack, …`). Semantics are in `abilities.md` §2.
  - **Intervening "if"** — `"When/Whenever/At [event], if [condition],
    [effect]."` The condition is checked twice: on trigger and again on
    resolution (603.4). Only an "if" *immediately after* the trigger
    condition is intervening; "if" elsewhere is plain English (603.4).
  - **`This ability triggers only if [condition]`** restricts triggering only.
    It is checked when the event happens and is not an intervening "if":
    603.4's recheck on resolution "only applies to an 'if' that immediately
    follows a trigger condition." Real (Quakebringer): `At the beginning of
    your upkeep, Quakebringer deals 2 damage to each opponent. This ability
    triggers only if Quakebringer is on the battlefield or if Quakebringer is
    in your graveyard and you control a Giant.` `Solved — [triggered ability]`
    expands to this wording (702.169c), while `To solve — [condition]` expands
    to an intervening if (719.3a). The Case rulings `[2024-02-02]` say only of
    the latter that "'To solve' abilities will check for their condition
    twice: once when the ability would trigger, and once when it resolves."
  - **Reflexive** — `"… When you do, …"` / `"… When [something happens]
    this way, …"`: a triggered ability created mid-resolution that triggers
    on whether an earlier action in the same resolution happened (603.12).
    Real: Sorin's `"[+1]: You may sacrifice a Vampire. When you do, Sorin
    deals 3 damage to any target and you gain 3 life."`
  - **`If you do` is not reflexive.** `X. If you do, Y` is a condition inside
    a single resolution (608.2c). It creates no new triggered ability, gives
    no chance to respond between X and Y, and any `target` in Y was chosen
    when the whole spell or ability was put on the stack (601.2c, 115.1).
    Example: `[−1]: You may sacrifice an artifact. If you do, destroy target
    artifact or creature.` (Daretti, Ingenious Iconoclast). `X. When you do,
    Y` creates a reflexive triggered ability. That ability uses the stack and
    chooses its targets as it is put there (603.12, 603.3d, 115.1d).
    Heart-Piercer Manticore ruling `[2017-04-18]`: its trigger "goes on the
    stack without a target. While that ability is resolving, you may sacrifice
    a creature. If you do, a second ability triggers and you pick a target …
    This is different from other abilities that say 'If you do . . .' in that
    players may cast spells and activate abilities before a creature is
    sacrificed and then again after the creature is sacrificed but before
    damage is dealt." The supported corpus has 1,169 distinct `. If you do, `
    lines and 297 `. When you do, ` lines.
  - **`After …` is not a trigger word.** Triggered abilities use "when,"
    "whenever" or "at" (603.1, 113.3c). `After you roll a die, you may pay 1
    life. If you do, increase or decrease the result by 1. Do this only once
    each turn.` (Night Shift of the Living Dead; also Xenosquirrels) is a
    static ability, by elimination from 113.3's four categories, that offers
    an optional die-roll modifier with a cost. 706.2 says "Modifiers may also
    come from other sources", and 706.2a says they "may be optional and/or
    have associated costs." The modifier applies before the result is final,
    so the rolling ability's results table uses the shifted number (706.2,
    706.3a). When several modifiers apply, 706.2b orders them. Ruling
    `[2022-10-07]`: "you do get to see all the results before deciding whether
    to use it." Night Shift's `Do this only once each turn` borrows 603.2h's
    wording for triggered abilities. Read it as a once-per-turn limit on use:
    a separate ruling `[2022-10-07]` says that paying the life on a planar-die
    roll, whose result can't be altered, "would still 'use up' the ability for
    the turn." The other supported `After …` lines add phases (`After this
    main phase, there are two additional combat phases.`, Full Throttle;
    500.8).
- **Static** — declarative statement that is "simply true" (113.3d); no
  cost, no trigger word, no colon. e.g. Questing Beast's
  `"… can't be blocked by creatures with power 2 or less."`
- **Spell ability** — imperative instructions on an instant/sorcery,
  followed as the spell resolves; any text on an instant/sorcery is a spell
  ability unless it is activated, triggered, or a qualifying static (113.3a).
  e.g. Fire's `"Fire deals 2 damage divided as you choose among one or two
  targets."`

**Band-opening lines (striated boxes).** Some lines are *headers* that open a
band; the lines beneath them (until the next band header) belong to that band:

- **Class level bar** — `{cost}: Level N` is a keyword ability representing
  **both** an activated ability (the level-up: `Activate only … as a sorcery`,
  only from level N−1) **and** a static ability (716.2/716.2a). Lines printed
  in the same box section after the bar are that level's **static** text
  (716.2). The top box section (before any bar) is always-on, parsed normally
  (716.3). Real (Monk Class): `{W}{U}: Level 2` then
  `When this Class becomes level 2, return up to one target …` (a triggered
  ability gained at level 2).
- **Leveler band** — `^LEVEL <N>-<M>` or `^LEVEL <N>+` is a keyword ability
  (level symbol) representing a **static** ability (711.2). The P/T line and
  any ability lines under it, until the next band, belong to that band
  (711.2a "N1-N2": active while N1≤counters≤N2; 711.2b "N3+": active while
  counters≥N3). The level-up activated ability sits *above* the first band and
  is always active (711.4). Real (Kargan Dragonlord): `LEVEL 4-7` / `4/4` /
  `Flying`, then `LEVEL 8+` / `8/8` / `Flying, trample`.
- **Station band** — on a card with the `Station` keyword (702.184a), `^\d+\+
  \| ` opens a band. A station symbol `{N+}` represents a static ability
  (721.2): "As long as this permanent has N or more charge counters on it, it
  has [abilities]" (721.2a). That line and the unmarked lines after it, up to
  the next `N+ | ` line or the end of the text, are one band. *Engine
  inference from the MTGJSON layout (UD-34):* Oracle text
  carries `N+ | ` only on the first line of a striation, so the extent of a
  band is inferred; on every supported station card, ordinary abilities come
  before the `Station` line and the first row comes directly after it. If the
  striation has a P/T box, the permanent is also "a creature with base power
  and toughness [P/T] in addition to its other types" (721.2b); the box is not
  in `text`, but the station reminder names it (`It's an artifact creature at
  8+.`), and the card's `power`/`toughness` belongs to the highest threshold
  (all 25 supported station cards with P/T match). Station cards have no P/T
  off the battlefield (721.2c). The striations have no other game significance
  (721.3). The `Station` keyword line and any ability not preceded by a
  station symbol are treated normally (721.4). Real (Entropic Battlecruiser):
  `1+ | Whenever an opponent discards a card, they lose 3 life.` / `8+ |
  Flying, deathtouch` / `Whenever this Spacecraft attacks, each opponent
  discards a card. …`. The same `N+ | ` shape is a die-roll row (§1); a
  `Station` line above it or a roll instruction above it tells them apart.

## 3. Keyword grammar

Terminal vocabularies, in order of authority:

- `data/rules/keywords.json` (CR 701, 702, 207.2c) decides membership for
  keyword abilities, keyword actions (e.g. Scry, Exile, Sacrifice, Mill) and
  ability words.
- For type vocabularies, CR 205.3 outranks the type catalogs.
  `artifact-types.json` lags 205.3g (it lacks Heartwood, Lander, Mutagen and
  Vibranium, and adds Terminus), so defer to the CR.
- The Scryfall catalogs (`keyword-abilities.json`, `keyword-actions.json`,
  `ability-words.json`, `flavor-words.json`) are surface supplements. They
  hold the variant stems the comma-split guard needs (Forestwalk/Islandwalk,
  typecycling forms, `Hexproof from`, `Partner with`, `Nonbasic landwalk`).
  Their known gaps and extras are of three kinds: CR keywords the catalog
  lacks (some actions and abilities), entries the CR does not list (ability
  words absent from 207.2c; a keyword ability filed as an ability word), and
  malformed entries (an empty-string entry in `keyword-actions.json`: drop
  it).
- Normalize before matching: case, curly and straight apostrophes
  (`keywords.json` uses `’`) and the `∞ (Infinity)` label.

Forms seen in the corpus:

- **Bare keyword:** `Flying`, `Trample`, `Vigilance`.
- **Comma-separated list** (one line, many abilities — §1): `Vigilance,
  deathtouch, haste`.
- **Keyword + cost** (mana or composite): `Ward {2}`, `Buyback {2}{B}{B}`,
  `Escalate {1}{W}`. Composite costs use `—`: `Ward—{2}, Pay 2 life.`
- **Keyword + quality/parameter:** `Protection from black`,
  `Protection from black and from red`, `Enchant artifact`,
  `Enchant artifact or creature you control`, `Enchant artifact, creature,
  or planeswalker`.
- **Keyword + variable definition:** `Mobilize X, where X is the number of
  creature cards in your graveyard.`, `Firebending X, where X is this
  creature's power.` This is one keyword ability whose number is X (702.181a
  "Mobilize N", 702.189a "Firebending N"); the trailing `, where X is …`
  defines X for that ability (107.3). A granted keyword can carry the same
  definition, and its value is reevaluated continuously (702.1b: "This
  creature has echo {X}, where X is your life total."). The comma before
  `where` is not a keyword delimiter. In a token-creation clause such as
  `Create an X/X black Demon creature token with flying, where X is the number
  of cards in your hand.`, the supplement defines that clause's X (the token's
  power and toughness), not a keyword parameter. Keyword actions take the same
  supplement in sentences (`Scry X, where X is …`, `Amass Zombies X, where X
  is …`).
- **Landwalk family** — `<Type>walk`: `Forestwalk`, `Islandwalk`,
  `Mountainwalk`, `Swampwalk`, `Plainswalk`, `Desertwalk`, plus the
  generic/qualified `Landwalk`, `Legendary landwalk`, `Nonbasic landwalk` —
  all in `keyword-abilities.json`. Granted/ad-hoc forms ("…has landwalk of
  the chosen type") are *not* discrete catalog entries; parse them as the
  stem `Landwalk` plus a qualifier from the surrounding text.
- **Prose-parameter keywords.** Some keywords take a parameter that the
  comma-split guard's stripping list doesn't cover, and the catalogs list only
  the bare stem or nothing at all. The keyword's 702 written form governs the
  shape:
  - `Equip [quality] [cost]` (`Equip legendary creature {1}`, `Equip Elf {2}`,
    `Equip commander {2}`; 702.6c) and `Equip planeswalker [cost]` (702.6e);
  - `Emerge from [quality] [cost]` (`Emerge from artifact {5}{B}{B}`,
    702.119b);
  - `Splice onto [quality] [cost]` (`Splice onto Arcane {1}{R}`, 702.47a);
  - `Craft with [materials] [cost]` (`Craft with artifact {1}{U}`, 702.167a);
  - `Devour [quality] N` (`Devour artifact 1`, 702.82c);
  - `bands with other [quality]` (702.22b–c; the supported corpus has only
    quoted grants);
  - `Sticker kicker [cost]` (702.33h);
  - `Partner—[text]` for exactly Character select, Father & son, Friends
    forever, and Survivors (702.124i); the catalog has `Partner` and, as a
    separate legacy entry, `Friends forever`, but not the dashed forms.

  Two families are open in the CR, and the catalogs hold only attested
  members. `[Type]cycling [cost]` takes any card type, subtype, supertype, or
  combination (`Basic landcycling {1}{B}`, `Artifact landcycling {2}`;
  702.29e). `[type]walk` includes qualified forms such as `Snow swampwalk` and
  `artifact landwalk` (702.14a, 702.14c), and the catalog lacks `Snow
  swampwalk`. Parse these as stem + parameter, not by exact catalog match.
- **Stacked keywords with mixed punctuation:** `Ward {1}, haste` and
  `Protection from black; flanking (…)` show that `, ` and `; ` both
  delimit keyword abilities on a line.

**Comma-split guard (§1 split test, precisely).** Before splitting a line on
`, ` / `; `, test each candidate token by **stripping its trailing parameters**
— mana/composite cost (`{…}`, `—{…}`), `from <quality>`, `<type>` after
`Enchant`, bare numbers, a `, where X is …` supplement — then matching the
remaining **stem** against the catalogs. Stems may be multi-word, so match
longest-first: `First strike`, `Double strike`, `Partner with`,
`Hexproof from`, `Living weapon`. Split the
line into keyword abilities **only if every** token's stem resolves; if any
token fails, treat the whole line as one ability. Note that the catalog stores
some qualified forms as their own entries (`Hexproof from`, `Nonbasic
landwalk`) while others keep the qualifier as a parameter on the bare stem
(`Protection` + `from black`), so strip-then-match must try both. A `, where X
is …` supplement belongs to the keyword token before it. Don't count it as a
separate token, so it can't fail the line.

Punctuation cues (supported corpus):
- Apart from `Kicker [cost 1] and/or [cost 2]`, which means two kicker
  abilities (702.33b; 18 supported lines), a keyword line never joins keywords
  with `and` or `or`. A token beginning `and ` or `or ` belongs to a
  coordinated parameter (`Enchant artifact, creature, or planeswalker`;
  `Hexproof from artifacts, creatures, and enchantments`) or to prose.
- A top-level `;` (outside parentheses and quotes) occurs only on keyword
  lines. All 31 such lines end in reminder text (`Trample; haste; shroud
  (…)`).
- Reminder text does not require semicolons: `Flying, vigilance (Attacking
  doesn't cause this creature to tap.)` uses commas.

**Keyword lines vs keyword mentions.** A keyword line is a stem plus its
CR-written parameter (and reminder text), and nothing else. A keyword name
anywhere else is a *mention*: it refers to that keyword's ability, cost, or
derived state rather than adding a keyword ability to the host card. A grant
(`gains flashback until end of turn`) gives an instance of that ability to the
object it names (113.10). The CR defines these mention shapes:
- `with [keyword]` / `that has [keyword]` means with a [keyword] ability
  (702.1d), including variants that the keyword's own rules fold in: "Any
  effect that looks for a card with cycling will find a card with typecycling"
  (702.29f).
- `[keyword] cost` means only that keyword's variable costs (702.1a): `The
  flashback cost is equal to its mana cost.` This includes line-opening forms
  such as `Equip costs you pay cost {1} less.`, `Dash costs you pay cost {2}
  less …`, and `Equip abilities you activate cost {1} less to activate.` A
  capital letter at the start of a line doesn't make it a keyword line, so
  require the stem to be followed only by its parameter.
- `The same is true for [keywords]` grants every variant and variable of each
  listed keyword (702.1c); see §5. 15 supported lines list keywords; the other
  9 `the same is true for` lines extend a rule to other objects and are not
  keyword mentions.
- Derived forms are defined in each keyword's own subrules: `convoked`
  (702.51c), `it devoured` (702.82b), `evolves` (702.100b), `if tribute wasn't
  paid` (702.104b), `kicked with its [A] kicker` (702.33f), `the gift was
  promised` (702.174k), and the designations `monstrous` (701.37b) and
  `saddled` (702.171b). This vocabulary is open; look each form up in its
  keyword's 701/702 entry.

When `scripts/define`/`scripts/keyword` lacks a parameterized form, the
keyword's **reminder text** in parens usually states the parameter in plain
English — e.g. `Ward {2} (Whenever this … becomes the target of a spell or
ability an opponent controls, counter it unless that player pays {2}.)`.

**Line-initial labels (`Label — text`).** A label before a spaced em dash at
the start of a line (after any `• ` or `+ `) is a mixed slot; the dash does
not set a category. An **ability word** ties together cards with similar
functionality (207.2c, closed list); a **flavor word** is tailored to the one
ability it appears with (207.2d, not listed in the CR). Only these two are
without rules meaning, so only they are stripped. Every other label is rules
text. Test in this order:
1. **Striated-box marker:** Saga chapter numerals (§1).
2. **Die-result label:** `N — `, `N or M — ` and `• N — ` rows of a results
   table (§1; 706.3a).
3. **Mode row:** Spree `+ {cost} — `, Tiered `• Flavor — {cost} — `, pawprint
   `{P}… — ` (§6; 700.2h, 700.2i).
4. **Anchor word:** `• A — [ability]` under `As this … enters, choose A or B.`
   (§1; 614.12c, 607.2m). Require the bullets.
5. **Keyword label:** the label is a keyword whose CR definition takes this
   shape. The full set is Boast (702.142a), Exhaust (702.177a), Forecast
   (702.57a), Max speed (702.178a), Power-up (702.193a), Solved (702.169b-d),
   To solve (719.3a), Visit (702.159a; Attractions, none in the supported
   corpus), ∞ (702.186b) and Companion. 702.139a writes
   `Companion—[Condition]` without spaces, but all 10 Oracle lines print
   `Companion — `. Cards also print `Prototype {cost} — P/T` (702.160a,
   718.2). Parse each by its own rule. Boast, Exhaust, Power-up and Forecast
   restrict the following activated ability; Max speed, Solved, ∞ and Visit
   condition the following ability; To solve is a condition (719.3a);
   Companion's tail is a deck-building condition, not an ability. Later text
   refers to these abilities by name (`Whenever you activate an exhaust
   ability, …`, Adrenaline Jockey; boast abilities, 702.142b). Match the label
   after case-folding and normalizing `∞ (Infinity)`;
   `data/rules/keywords.json` spells it that way and "Max Speed" with a
   capital. `keyword-abilities.json` has no entry for `To solve`, `∞` or
   `Visit`, and `keywords.json` has none for `To solve` or `∞`, so match those
   literally. A keyword with an unspaced dash (`Suspend 4—{U}`, `Awaken N—`,
   `Impending N—`, `Reinforce N—`, `Partner—Friends forever`, `Ward—{2}, Pay 2
   life.`) starts a keyword line, not a label (§3 forms above).
6. **Ability word:** match `keywords.json` abilityWords (the 207.2c list),
   case-folded, treating `’` and `'` as equal and keeping any trailing number
   (`descend 4`, `descend 8`; Oracle prints `Tempting offer —` and `Tempting
   Offer —`). `ability-words.json` over-includes entries absent from 207.2c,
   such as `Corrupted` (24 supported `Corrupted —` lines) and `Will of the
   Planeswalkers` (1 supported line), and words that appear only on
   unsupported cards (actualize, covercast, hero's reward, kinfall, landship,
   legacy, seek out, strange new worlds, underdog). It stores bare `Descend`
   where cards print `Descend 4 —`, and lists `Start your engines!`, which is
   a keyword ability (702.179a). Printed `Corrupted —` and `Will of the
   Planeswalkers —` still get stripped as non-rules labels.
7. **Flavor word:** anything else (207.2d). `flavor-words.json` is incomplete
   (`The Minstrel's Ballad —`, `Hero's Sundering —` are missing), so treat
   this step as the fallback, not as a lookup. Flavor words also label modal
   bullets (`• Archery — This spell deals 5 damage to target creature with
   flying.`) and die rows (`1 | Trapped! — You lose 3 life.`).

Strip only (6) and (7); an ability word or flavor word affects parsing only by
being stripped. A dash in the middle of a line is not a label: in `[A player]
faces a villainous choice — [option A], or [option B]`, the dash introduces a
keyword action's options (701.55a).

## 4. Replacement-effect tense markers

Replacement effects are continuous, never use the stack (614.1; effects.md
§6). Recognize them by surface markers — they are *not* triggered abilities
even though some resemble triggers:

- **"… would …, … instead"** (614.1a) — the dominant form. Real:
  `"… if that creature would deal combat damage to one of your opponents,
  it deals triple that damage to that player instead."` Also
  `"If that spell would be put into your graveyard, exile it instead."`
- **Bare `instead` (no `would`) inside a spell's or ability's own text.** `If
  [condition], [alternative] instead.` replaces part of that same spell's or
  ability's effect. That makes it a **self-replacement effect**: it is not a
  continuous effect, and it applies before other replacement effects (614.15,
  616.1a). This applies only to text that resolves (a spell ability, or an
  activated or triggered ability's effect). Bare `If …, … instead` in a static
  ability (`If a land is tapped for mana, it produces {B} instead of any other
  type and amount.`, Contamination) is an ordinary continuous replacement
  effect (614.1a). Self-replacement text can also be a separate ability,
  particularly after an ability word (614.15). Real (Fight with Fire): `Fight
  with Fire deals 5 damage to target creature. If this spell was kicked, it
  deals 10 damage divided as you choose among any number of targets instead.`
  When the condition is a cost choice, the alternative's targets are chosen
  during casting: "a spell may require alternative targets only if an
  alternative or additional cost was chosen for it" (601.2c). Rulings
  `[2018-04-27]`: "If Fight with Fire is kicked, it can target creatures,
  players, and planeswalkers," and "You choose how many targets Fight with
  Fire has and how the damage is divided as you put the spell onto the stack."
  A mode-count upgrade such as `Choose one. If this spell was kicked, choose
  any number instead.` changes a choice made during casting instead (§6;
  700.2a).
- **"skip"** (614.1b, 614.10) — every effect that makes a player skip an
  event, step, phase or turn is a replacement effect; "Skip [something]" means
  "Instead of doing [something], do nothing" (614.10). The parsing distinction
  is how the effect is created, not whether it is a replacement. A **static
  ability** creates it continuously: `"Skip your draw step."` (Necropotence),
  `"Players skip their untap steps."`, `"If a player would draw a card, that
  player skips that draw instead."` A **resolving spell or ability** creates a
  continuous replacement effect on resolution (611.2): `"Draw four cards. You
  skip your next turn."` (Meditate), `"Target opponent skips their next X
  turns …"` (Ral Zarek, Guest Lecturer). It waits for the next occurrence
  (614.10, 614.10a) and is not a one-shot effect (610.1). Only reminder-text
  "skip" (`"Skipped chapters don't trigger."`) is not rules text.
- **ETB modifiers** (614.1c): `"~ enters with …"`, `"As ~ enters …"`,
  `"~ enters as …"`. Real: `"As Alhammarret enters, each opponent reveals
  their hand…"`; `"… that creature enters with that many additional +1/+1
  counters on it."`
- **Continuous "~ enters …" / "[objects] enter …"** (614.1d); **"as ~ is
  turned face up …"** (614.1e).

Caution: `"As [an additional cost to cast] …"` is a casting/cost clause, not
a replacement effect — disambiguate `As ~ enters` (614.1c) from `As an
additional cost …` by what follows "As".

Deontic markers are the *other* layer (choice-legality, not event-edit):
`"can't … except"`, `"only as a sorcery"`, `"as though"`, `"… if able"`,
`"unless … pays"` parse into the May/Cant/Must/toll algebra in
`deontics.md`, not into replacement effects. 614.17 is the rule for `can't`
("These effects aren't replacement effects"); it does not cover `as though`,
`if able` or `unless … pays`.

## 4a. Type-change markers (layer 4)

Type-changing effects apply in layer 4 (613.1d; layer mechanics:
`effects.md`). The wording decides what the object keeps:

- **Plain set:** `becomes a [type]` or `is a [type]` with no retention phrase.
  In most such cases "the new card type(s) replaces any existing card types"
  (205.1a), except that an object keeps the instant or sorcery type. New
  subtypes replace existing subtypes from the same set (creature, land,
  artifact, enchantment, planeswalker or spell types). Removing a card type
  also removes its correlated subtypes, unless they are subtypes of a type the
  object still has (205.1a). Supertypes do not change (205.4b). Setting a land
  to a basic land type also removes the abilities its rules text gives it
  (305.7).
- **Retention phrases:** `in addition to its other types` and `still a [type,
  supertype, or subtype]` both keep "all the object's prior card types,
  supertypes, and subtypes" (205.1b). So `It's still a land.` and `… in
  addition to its other types` have the same rules effect. 205.1b names them
  only as "phrases such as" these, and Oracle also uses `is also a`: `Tajuru
  Paragon is also a Cleric, Rogue, Warrior, and Wizard.` Its ruling
  `[2020-09-25]` calls this "The ability that adds creature types". Living
  metal's reminder, `this Vehicle is also a creature`, paraphrases 702.161a's
  "in addition to its other types".
- **`becomes an artifact creature`** keeps "all of its prior card types and
  subtypes" (205.1b). Real (crew reminder): `This Vehicle becomes an artifact
  creature until end of turn.`
- **`becomes a [creature types] artifact creature`** keeps prior card types
  and subtypes "other than creature types, but replace[s] any existing
  creature types" (205.1b). Real (Gruul War Plow): `{1}{R}{G}: This artifact
  becomes a 4/4 Juggernaut artifact creature until end of turn.`

## 5. Reference grammar

How text names the objects and players it acts on. For how Oracle text phrases
names, pronouns, `this`/`that`, carrier words, determiners and targets, see
`oracle-style.md` Part II (sections 5-7).

- **Self-reference.** Oracle text names the source in one of three ways: by
  its full card name (`"Questing Beast can't be blocked …"`), by a shortened
  name (`"Sorin deals 3 damage …"` on Sorin, Imperious Bloodlord), or by
  `"this <type>"` (`"this creature deals 2 damage …"`, `"this permanent"`,
  `"this land"`; 700.7). A shortened name is "treated as though [it] used the
  card's full name" (201.5c), and a self-name means only that particular
  object (201.5). Outside quoted grants (next bullet), bind all three forms to
  the source. Shortening does not depend on a comma: `When Acererak enters, …`
  (Acererak the Archlich), `{2}{U}{U}: Return Arcanis to its owner's hand.`
  (Arcanis the Omnipotent) and `[−2]: Ajani deals 3 damage to any target and
  you gain 3 life.` (Ajani Vengeant) all shorten names without one. Some comma
  names are printed in full (`{T}: Hansk, Slayer Zealot deals 2 damage to
  target creature.`). Accept the full name and each shortened form a card
  prints for itself. Under 201.5c a shortened name refers to the card it is
  printed on, so do not let one card's short forms resolve as names in other
  cards' text. The same word can also be a planeswalker type (205.3j): `if you
  control an Ajani planeswalker` (Ajani's Comrade) tests a subtype, and a type
  use comes before a type noun. An alternate name from a secondary title bar
  refers to the Oracle name (201.6).
- **Inside a quoted granted ability, the two forms point to different
  objects.** `"this <type>"` names the object that has the granted ability.
  The granting card's name names the granter: "the name refers only to the
  specific object which is that first ability's source" (201.5a). Blazing
  Torch: `Equipped creature has "{T}, Sacrifice Blazing Torch: Blazing Torch
  deals 2 damage to any target."` Its ruling `[2009-10-01]` says: "The source
  of the damage is Blazing Torch, not the equipped creature. However, the
  equipped creature's ability is what targets the permanent or player."
  Archery Training: `Enchanted creature has "{T}: This creature deals X damage
  to target attacking or blocking creature, where X is the number of arrow
  counters on Archery Training."` Here the creature deals the damage, and
  "each granted ability counts the counters on the Archery Training that
  granted that ability" (ruling `[2004-10-04]`). The CR's own templating works
  the same way: Sorcerer Role grants `'Whenever this creature attacks, scry
  1.'` to the enchanted creature (111.10n). No rule defines `this <type>`
  directly, so this binding rests on that templating and on the rulings. For
  name changes and gained abilities, see 201.5b (an ability gained by a
  differently named object reads the old name as the new object) and
  `queries.md` §3.
- **Pronoun binding.** `"it"` / `"that creature"` / `"that player"` / `"those
  creatures"` refer back to an object or player named earlier in the same
  ability, including from a delayed or reflexive trigger the ability creates.
  Questing Beast: `"… it deals that much damage to target planeswalker **that
  player** controls"` — `it` = Questing Beast, `that player` = the opponent
  dealt damage. The CR has no anaphora rule beyond reading the whole text
  (608.2c). Plain recency (the nearest matching antecedent) is wrong, because
  rulings bind several pronouns past a nearer match. Filter the candidates,
  then take the most recently introduced one left. Read recency by clause: the
  nearest clause that introduces a candidate left wins, and within it the
  subject beats the object, which beats an oblique:
  1. **It isn't another argument of the pronoun's own verb.** In Feral
     Contest's `Put a +1/+1 counter on target creature you control. Another
     target creature blocks it this turn if able.`, `it` is the first target:
     the second target "will have to block the first targeted creature"
     (ruling 2010-03-01). In Time to Feed's `Target creature you control
     fights that creature.`, `that creature` is the opponent's creature chosen
     earlier (ruling 2013-09-15). In Case of the Gateway Express's `choose
     target creature you don't control. Each creature you control deals 1
     damage to that creature.`, `that creature` is the chosen target, not one
     of the creatures that deal the damage (no ruling covers this shape; it
     reads like Time to Feed). A possessor or a prepositional host (`put a
     +1/+1 counter on it`) isn't such an argument.
  2. **It isn't what another anaphoric expression in the same sentence took**
     (a pronoun, or a `that`/`the` description). In Kalitas's `create a black
     Vampire creature token. Its power is equal to that creature's power`,
     `its` is the token and `that creature` is the destroyed creature (ruling
     2009-10-01). In Ram Through's `If the creature you control has trample,
     excess damage is dealt to that creature's controller instead.`, `the
     creature you control` re-mentions the first target, so `that creature` is
     the second target, the creature you don't control (ruling 2020-04-17).
     In Twinflame's `create a token that's a copy of that creature, except it
     has haste`, `that creature` takes the copied creature, so `it` is the
     token (ruling 2014-04-26: a copy of the token has haste).
  3. **It can fill the word's slot in its current zone.** "Card" in rules text
     never means a permanent or a spell (glossary, "Card"), so in Bioplasm's
     `exile the top card of your library. If it's a creature card, …`, `it` is
     the exiled card. A bare type word means a battlefield permanent (109.2),
     and an object that changed zones is a new object (400.7). So in Vampiric
     Embrace's `Whenever a creature dealt damage by enchanted creature this
     turn dies, put a +1/+1 counter on that creature.`, `that creature` is the
     enchanted creature, not the one that died (the card's original Urza's
     Saga-set printing read "put a +1/+1 counter on enchanted creature."). The
     exception is when a 400.7 exception lets the effect find the moved object
     (400.7j): Scythe of the Wretched's `return that card to the battlefield …
     Attach this Equipment to that creature`; its ruling says the Scythe
     "won't move onto it" if the returned card isn't a creature. The verb's
     own rule can narrow the slot by kind: `sacrifice it` needs a permanent
     (701.21a). State-dependent requirements (whether the object is untapped,
     701.26a, or who controls it) never rebind a pronoun; they only make the
     action do nothing.
     - **Head nouns follow the zone of what they refer to** (109.2, 109.2a).
       After an effect moves an object off the battlefield, Oracle calls the
       new object `that card` or `the exiled card`. Example: `Exile target
       creature. Return that card to the battlefield under its owner's control
       at the beginning of the next end step.` (Turn to Mist); the effect can
       find that card (400.7j). When the effect then acts on the object in its
       new zone, Oracle switches to `that card` (no supported line exiles a
       creature and then returns `that creature` or `that permanent`). A
       demonstrative that keeps the type word after the move reads that
       permanent's last known information (608.2h) when the predicate asks
       about past state: `Destroy target creature. If that creature was a
       Human, …` (Death's Caress). Filter 3 applies instead when the action
       needs a permanent (`put a +1/+1 counter on that creature`). Saw in
       Half: `Destroy target creature. If that creature dies this way, its
       controller creates two tokens that are copies of that creature, except
       their power is half that creature's power …`. Ruling `[2025-09-19]`:
       "Use the power and toughness of the creature from when it was last on
       the battlefield." Binding semantics: `queries.md` §3.

  Recency counts introductions (target and indefinite noun phrases), not
  re-mentions. If two same-kind candidates still survive, report ambiguity
  rather than guess. Never re-filter a candidate by the noun's quality: a
  stored reference survives losing it (700.7; `queries.md` §3,
  *Self-reference*). This procedure is an **engine inference** checked
  against the rulings above, not a CR rule (UD-32), so
  treat it as a heuristic: a few sentences of the same shape still resolve
  differently and need card-specific bindings. `queries.md` §3 points here.
- **Disjunctive player anaphor.** After a target that may be a player or a
  permanent (`any target`, `target player or planeswalker`, `target opponent
  or planeswalker`), Oracle names the affected player with a disjunction keyed
  on the target's kind: `that player or that planeswalker's controller`, `that
  player or that permanent's controller`, or `that permanent's controller or
  that player` (24 supported lines). It means the target itself if the target
  is a player, and otherwise that permanent's controller (109.4). In Rhystic
  Lightning's `deals 4 damage to any target unless that permanent's controller
  or that player pays {2}`, the disjunction names one payer for the toll
  (118.12a). For Chain Lightning's `Then that player or that permanent's
  controller may pay {R}{R}`, "the targeted player or the controller of the
  targeted permanent may copy it" (ruling 2022-12-08).
- **Attachment hosts.** `enchanted [object or player]`, `equipped creature`,
  and `fortified land` refer to whatever the ability's permanent is attached
  to, even if that permanent isn't an Aura, Equipment, or Fortification
  (303.4m, 301.5f; 301.6 applies 301.5a–f to Fortifications and lands). Bind
  them through the source's attachment, not by searching for an antecedent;
  they need no earlier mention. Real: `"Enchanted creature gets +4/+2."` (Boon
  Satyr, which is an Aura only while bestowed, 702.103b), `"This creature and
  enchanted creature each get +1/+1 …"` (Eidolon of Countless Battles), and
  granted text such as `have "Equipped creature gets +2/+0"` (Armed with
  Proof). If the permanent is attached to nothing, the reference finds nothing
  (engine inference from 303.4m's "whatever … that permanent is attached to";
  Spellweaver Volute's 2007-05-01 ruling agrees: when the Volute is enchanting
  nothing, its ability will "identify the 'enchanted card' as 'nothing,' so no
  copy is created"). If the source has left the battlefield, read its host
  from last known information (113.7a, 608.2h). Spellweaver Volute's ruling
  (2007-05-01) says the ability "will check its last existence on the
  battlefield and identify the 'enchanted card'".
  - **The host need not be a permanent.** An Aura enchants an object or a
    player (303.4b). Player hosts appear as `"enchanted player"` and
    `"enchanted opponent"` (702.5d). Card hosts in graveyards appear as
    `"Return enchanted creature card to the battlefield …"` (Animate Dead) and
    `"copy the enchanted instant card"` (Spellweaver Volute). A head
    containing `card` doesn't take 109.2's battlefield default, and the Volute
    ruling says "The enchanted card won't be on the battlefield."
  - **Host reference or predicate?** The host reading has a bare singular
    head, sometimes after `the` (`"the enchanted creature's toughness"`,
    Ironclaw Curse). The participle is a predicate instead when it follows a
    determiner or quantifier (`an`, `each`, `another`, `target`), when the
    head is plural, or when a control phrase follows. The predicate means "has
    an Aura attached" (303.4b) or "has an Equipment attached" (301.5a). Under
    the CR a plural is never a host, because an Aura or Equipment attaches to
    only one thing (303.4d, 301.5c). The only exception is unsupported:
    Soulmates ("Enchant two creatures") prints "Enchanted creatures each get
    +1/+1 …". Real predicates: `"Destroy target enchanted creature."`,
    `"Equipped creatures you control get +1/+1."` and `"Whenever an equipped
    creature you control dies, draw a card."`. Stone Haven Outfitter's ruling
    (2016-01-22) says these "refer to any creatures you control with Equipment
    attached to them … They aren't bonuses applied solely to the creature
    Stone Haven Outfitter is attached to." `target` used as a verb doesn't
    count as a determiner: `"Aura spells you cast that target enchanted
    creature cost {3} less to cast."` on Strong Back, an Aura, is a host
    reference.
- **`target [something]`** (115.1) is the word in a spell's or ability's own
  text that makes it targeted; `any target`, `another target` and `N targets`
  are forms of it (115.4). Otherwise only a keyword's rule creates a target:
  "Unless that object or player is identified by the word 'target' in the text
  of that spell or ability, or the rule for that keyword ability, it's not a
  target" (115.10a, 115.1e). `"you"` never indicates a target (115.10b). Some
  keyword rules create targets when the word `target` is absent from the
  card's rules text; the list is open ("such as", 115.1e):
  - an Aura spell targets what its enchant ability names (115.1b, 303.4a,
    702.5a);
  - a bestowed spell becomes an Aura spell and must target (702.103b);
  - a mutating creature spell "targets a non-Human creature with the same
    owner as this spell" (702.140a);
  - a keyword whose definition contains `target` targets through that
    definition (115.1e; equip: "Attach this permanent to target creature you
    control", 702.6a; modular, 702.43a);
  - awaken's spell ability on an instant or sorcery (702.113a).

  Targets are objects and/or players chosen as the spell/ability goes on the
  stack and can't change except by an effect that says so (115.1). Only
  permanents are legal unless the text says otherwise (115.2). The same
  `target` instance can't pick one object twice; distinct `target` instances
  can share an object (115.3).
  - **Scope of "target" on an instant/sorcery** — an *activated or triggered*
    ability **of** an instant/sorcery card that uses `target` makes that
    ability targeted, but the spell itself is **not** targeted (115.1a). Only
    a `target` in the card's spell ability targets the spell, whether printed
    or supplied by a keyword's rule.
  - **`choose target …` still targets.** The targets are declared as the spell
    or ability is put on the stack (115.1, 601.2c), not chosen during
    resolution; the verb `choose` doesn't change that. Joust: `Choose target
    creature you control and target creature you don't control. …` Ruling
    `[2019-10-04]`: "You can't cast Joust unless you choose both a creature
    you control and a creature you don't control as targets." There is also a
    per-player form: `For each player, choose up to one target creature card
    in that player's graveyard.` (Afterlife from the Loam). Without `target`,
    a `choose a/an …` in a resolving spell's or ability's effect is made
    during resolution (608.2d). `As … enters, choose …` (614.12) and modal
    headers (700.2a–b) are not resolution-time choices. About 200 supported
    lines use `choose [up to N] target`.
- **Retargeting phrases are four different rules** (115.7):
  - `change the target(s)`: each target can change only to another legal
    target, and if they can't all change, none do (115.7a; `Change the target
    of target spell or ability with a single target.`);
  - `change a target`: only one target may change (115.7b);
  - `change any targets`: any number may change (115.7c);
  - `choose new targets`: any target may stay, even an illegal one, but each
    new target must be legal and must not make an unchanged target illegal
    (115.7d). Copies with new targets follow 707.10c, which has the same
    leave-unchanged and new-must-be-legal rules but no clause about unchanged
    targets becoming illegal.

  In every case only the final target set is checked for legality (115.7e),
  and the original division of damage or counters stays (115.7f). Supported
  corpus counts: `change the target` 17, `change a target` 2, `change any
  targets` 1, `choose new targets` 204, `choose a new target` 17.
- **`any target`** (115.4) — a damage shorthand expanding to **any creature,
  player, planeswalker, or battle** (115.4). Variants `another target`,
  `two targets` behave likewise; noncreature artifacts and spells can't be
  chosen (115.4).
- **Older templates in current Oracle text.** Accept these alongside the
  modern forms.
  - `enters` and `enters the battlefield` mean the same thing and parse the
    same (603.6a). `oracle-style.md`'s "Enters and dies" says where each form
    appears.
  - `target creature or player` is **not** `any target`. Firesong and
    Sunspeaker's `deals 3 damage to target creature or player` "can't target a
    planeswalker or battle" (ruling 2023-04-14), while `any target` admits
    creatures, players, planeswalkers, and battles (115.4).
- **Quantifiers:** `"each [player/creature]"` (untargeted, all qualifying),
  `"up to one/two/N target …"` (may choose fewer, even zero — 115.6). Real:
  `"Chandra deals 1 damage to up to one target player or planeswalker."`
- **`another` / `other`** excludes an *anchor*, and the anchor is not always
  the source. With `target`, it overrides 115.3, which otherwise lets separate
  `target` words pick the same object. No CR rule defines the anchor (115.4
  only lists `another target` as a shorthand), so which mention anchors is an
  engine inference (UD-31). The anchor rule, its
  evidence and the cards that rulings settle are in `queries.md` §2. Definite
  `the other [N]` is a different construction: it picks the other member of a
  pair.
- **`The same is true for [list]`** repeats the preceding sentence once for
  each listed item, putting the item in place of the matching term everywhere
  that term occurs.
  - Keywords: Concerted Effort, `At the beginning of each upkeep, creatures
    you control gain flying until end of turn if a creature you control has
    flying. The same is true for fear, first strike, double strike, landwalk,
    protection, trample, and vigilance.` A listed keyword with variants or
    variables grants "each appropriate variant and variable" (702.1c:
    Concerted Effort grants each landwalk and protection ability). 15
    supported lines list keywords.
  - Object classes: Ward of Bones, `Each opponent who controls more creatures
    than you can't cast creature spells. The same is true for artifacts and
    enchantments.` Its ruling `[2008-08-01]` spells this out as "Each opponent
    who controls more artifacts than you can't play artifact cards."
  - Domains: Biotransference, `Creatures you control are artifacts in addition
    to their other types. The same is true for creature spells you control and
    creature cards you own that aren't on the battlefield.`

  *Engine reading:* each copy keeps the original sentence's condition and
  duration. 24 supported lines use the phrase; the 9 non-keyword ones are not
  keyword mentions.
- **Type words.** Take card types, supertypes and subtypes from MTGJSON's
  `types`, `supertypes` and `subtypes` arrays rather than splitting the `type`
  string. If you must split it:
  - supertypes come directly before card types (205.4a);
  - subtypes follow a long dash (205.3b), and "Each word after the dash is a
    separate subtype";
  - for creatures, the one two-word type is `Time Lord` (205.3m);
  - for planes, "all words after the dash are, collectively, a single subtype"
    (205.3b, 205.3n).

  Each subtype correlates with its own card type (205.3c: `Land Creature —
  Forest Dryad`). In rules text, match subtypes longest-first against the
  subtype lists in 205.3g–205.3m (or the `data/catalogs/*-types.json` files,
  whose apostrophes match Oracle's ASCII `'` rather than the CR's `’`),
  because each listed word or two-word phrase is one subtype (205.3b). Time
  Lord is the only two-word creature type (205.3m), and some subtypes contain
  a hyphen or an apostrophe (Assembly-Worker and C'tan in 205.3m; the land
  types Power-Plant and Urza's in 205.3i). So `Spend this mana only to cast a
  Time Lord or Alien spell` (Gallifrey Council Chamber) names the subtypes
  Time Lord and Alien. A choice of subtype is exactly one existing subtype of
  the required kind (205.3e: "'Merfolk' or 'Wizard' is acceptable, but
  'Merfolk Wizard' is not"). Normalize apostrophes (`C'tan`, `Shi'ar`,
  `Urza's` in the catalogs and Oracle; `C’tan` in the CR) before matching
  against CR text.
- **Coordination scope in noun phrases.** A card type is either a bare noun or
  a premodifier, and the carrier noun fixes the domain: a bare type means a
  permanent on the battlefield, "card" plus a zone means a card there, and
  "spell" means a spell on the stack (109.2, 109.2a, 109.2b). Coordinated
  premodifiers share the final carrier: `instant or sorcery spell` is an
  (instant or sorcery) spell, and `artifact or creature card` is a card that
  is either. Splitting it as [instant] or [sorcery spell] would pair a
  battlefield permanent with a spell. Oracle repeats the carrier when the
  alternatives differ in modifiers or type category (`a basic land card or
  Gate card`, `an artifact creature card or Vehicle card`) and never writes `X
  or X card` (corpus). Juxtaposed types intersect (`artifact creature`), and
  plural `and` names separate collections (`artifact and creature cards`).
  `and/or` is covered in the next bullet.

  Counter kinds follow the same pattern under the head `counter`. A numeric
  kind (122.1a) or a keyword kind (122.1b) stands alone as a modifier of the
  shared head (`your choice of a +1/+1, first strike, or vigilance counter`;
  `put a flying, lifelink, or +1/+1 counter on it`). After `a counter from
  among`, the kinds are bare (`a counter from among first strike, vigilance,
  deathtouch, and lifelink`). Coordinating kinds with `and` under one
  `counter` head is unattested (corpus).

  A trailing controller or owner clause under one determiner covers the whole
  coordination (`a creature or planeswalker you control`). When each conjunct
  has its own determiner, the clause belongs only to its own noun phrase
  (`deals 1 damage to that player or a planeswalker that player controls`).
  These are corpus regularities and an **engine inference**, not CR rules.
- **`and/or` is a third coordinator**, distinct from both `and` and `or`. Over
  zones, it lets the player pick which listed zones to search. For Dark
  Supplicant's `Search your graveyard, hand, and/or library for a card named
  Scion of Darkness`, "You can choose which and how many of the three zones …
  you want to search" and "You only shuffle your library if you choose to
  search it" (rulings 2004-10-04). For Arachnus Spinner's `Search your
  graveyard and/or library for a card named Arachnus Web`, "You may search
  both … but you can find a maximum of one card named Arachnus Web" (ruling
  2017-03-14). Plain `and` searches every listed zone, as in Splinter's
  "Search its controller's graveyard, hand, and library" (701.23b example).
  Between noun phrases that each have their own determiner, `and/or` allows
  either or both (`You may put a creature card and/or a land card from among
  them into your hand`). Inside one noun phrase or quality, it is an inclusive
  `or`, and an object that qualifies both ways counts once. Aatchik's `for
  each artifact and/or creature card in your graveyard` counts an artifact
  creature card "only once" (ruling 2025-02-07), and so does All That
  Glitters' `for each artifact and/or enchantment you control` (ruling
  2019-10-04). Fear's reminder text uses the same form: `artifact creatures
  and/or black creatures`. 510 supported corpus lines contain `and/or`.
- **Token-creation noun phrases.** The creating effect defines the token's
  characteristics and its name (111.3, 111.4). There are four surfaces:
  - A description with no name, such as `Create a 1/1 red Goblin creature
    token.` The token is named for its subtypes plus "Token" ("Goblin Token",
    111.4).
  - A trailing name: `Create a colorless artifact token named Etherium Cell
    with "{T}, Sacrifice this token: Add one mana of any color."`
  - An appositive name for a legendary token: `Create Urami, a legendary 5/5
    black Demon Spirit creature token with flying.` "Create [name], a …"
    creates a token with the listed characteristics and that name (111.9). The
    name is lexical data from the card, and the subtypes stay subtypes:
    Minsc's Boo has the subtype Hamster and the name Boo (111.4 example). All
    41 supported appositive lines are legendary.
  - A predefined token noun, which brings its 111.10 definition; the creating
    effect may modify or add to it (111.10). The list is closed: Treasure,
    Food, Gold, Walker, Shard, Clue, Blood, Powerstone, Incubator, Cursed
    Role, Monster Role, Royal Role, Sorcerer Role, Virtuous Role, Wicked Role,
    Young Hero Role, Map, Junk, Lander, Mutagen, Vibranium, and Heartwood
    (111.10a–x). Most are named for their subtype plus "Token". The
    exceptions: a Walker is a 2/2 black Zombie named Walker (111.10d), a Role
    token is named for its role ("Cursed", 111.10j; "Young Hero", 111.10r),
    and an Incubator's back face is named Phyrexian Token (111.10i).

  Changing a token's name later doesn't change its subtypes, and vice versa
  (111.4).
- **APNAP note for parsers:** turn-order (APNAP) resolution of simultaneous
  choices is an *engine-runtime* concern, not a parsing concern — the
  grammar only needs to capture *who chooses* (`"you"`, `"target player"`,
  `"each player"`), not the order.

## 6. Numbers, variables, choices

- **Variables.** `X` is a value defined elsewhere in the same text
  (`"where X is …"`, `"X is the number of …"`) or by the cost paid; `*` (CDA)
  is a self-referential count. Real: `"Target opponent skips their next X
  turns, where X is the number of coins that came up heads."`
- **Symbol quantities.** Oracle text writes a count of a unit symbol in one of
  two ways: a run of glyphs, or a quantity before one glyph. Parse both as the
  same count. Each glyph is one unit: one energy counter (107.14), one
  colorless mana (107.4c), or mana of its color (107.4a).
  - Glyph run: `"{T}, Pay {E}{E}{E}{E}{E}: …"` (Dynavolt Tower), `"Add
    {R}{R}{R}{R}{R}{R}{R}."` (Geosurge).
  - Quantity before one glyph: `"Pay six {E}, Sacrifice this enchantment: …"`
    (Era of Innovation), `"{T}, Pay fifty {E}: …"` (Aetherflux Conduit), `"Add
    seven {R}."` (Irencrag Feat), `"You get X {E} …"` (Wrath of the Skies),
    and the keyword cost `"Madness—Pay six {C}."` (Emrakul, the World Anew;
    702.35a). The CR uses this form too: "Firebending N" means "… add N {R}"
    (702.189a).
  - The glyph as a unit noun: `"that many {E}"`, `"that much {R}"` (Raphael,
    Ninja Destroyer), `"one or more {E}"`, `"any amount of {E}"`, and `"for
    each {E} paid this way"`. Comparisons put small spelled numbers before
    `{E}` too: `"four or more {E}"` (Izzet Generatorium).

  The size of each form is a corpus convention, not a CR rule. Energy prints
  runs of one to five glyphs and spells out six or more (`six`, `eight`,
  `fifty`). No supported line has a run of six or more `{E}`. Mana prints both
  forms above five, so don't use a five/six boundary to validate text. `X {R}`
  (X red mana) is not `{X}{R}` (the generic-mana variable plus one red,
  107.4b).
- **Modal headers** (700.2) are "instructions for a player to choose a number
  of" the options in a bulleted list; each option is a mode. The header and
  its bullets are one ability. A header need not start the line and may be its
  own line, end a triggered or activated line, name another chooser, or be a
  sentence.
  - Own line: `Choose one —`, `Choose two —`, `Choose one or both —`, `Choose
    one or more —`.
  - After a trigger or cost prefix: `At the beginning of your end step, choose
    one —` (Abiding Grace), `When Venser enters, choose one —`, `{1}{G}, {T}:
    Choose one —`.
  - Another chooser: `An opponent chooses one —` (Fatal Lore), `Target
    opponent chooses one —` (Truth or Dare). That player chooses where the
    controller normally would (700.2e).
  - Sentence headers: `Choose three. You may choose the same mode more than
    once.` (Brokers Confluence; 700.2d), `Choose one. If you control a
    commander as you cast this spell, you may choose both instead.` (Akroma's
    Will), `Choose one. If this spell was kicked, choose any number instead.`,
    `Whenever this creature attacks or dies, choose one or more. Each mode
    must target a different player.`
  - Counts include `one`, `two`, `three`, `four`, `five`, `X`, `one or both`,
    `one or more`, `up to one`, `up to two`, `up to four`, `up to X, where X
    is …`, `up to that many` and `any number`. Modifiers include `at random`
    and `that hasn't been chosen [this turn]`. The set is open; query
    `scripts/corpus --match` for it.
  - Recognition: find runs of mode lines (`• `, `+ {cost} — `, `{P}… — `) and
    attach each run to the nearest preceding non-mode line of the same
    ability. That line is the header when it contains a `choose <count>` /
    `chooses <count>` clause anywhere, whether the line ends in `—` (spaced or
    not), ends a sentence, or is coordinated (`choose one and Glorfindel gets
    +1/+1 until end of turn`); a `Spree` or `Tiered` keyword line also
    qualifies, even with a shared-effect line between it and the modes
    (Vincent's Limit Break). A `Choose …` line with no bullets is not a header
    (`Choose a Background` is a keyword, 702.124k; `Choose a card name.` is an
    instruction).
  - Exclusions: bullets under `As … enters, choose A or B.` are anchor-word
    abilities (§1), and bullets after a roll instruction are results-table
    rows (§1). Neither is a mode.
  - Modes are chosen while casting or activating (700.2a), or as a triggered
    ability is put on the stack (700.2b). A mode with no legal target can't be
    chosen (700.2a).
- **Pawprint modes** (700.2i) — a variant where modes are weighted by
  pawprint symbols (`{P}`) instead of bullets. Header:
  `Choose up to N {P} worth of modes` (real: `"Choose up to five {P} worth of
  modes. You may choose the same mode more than once."`); mode lines are
  `^{P}+ — ` (real: `{P} — Draw a card.`, `{P}{P} — Exile target nonland
  permanent. …`). The chosen modes' pawprints must total ≤ N (700.2i). Consume
  the `{P}…—` lines as the header's modes, same as `•` lines.
- **Escalate** is the additive cost for extra modes — `Escalate {1} (Pay
  this cost for each mode chosen beyond the first.)` — not itself a mode.
- **Costed modes** (700.2h): a cost listed before a mode's effect is an
  additional cost paid if that mode is chosen. **Spree**: header line `Spree
  (Choose one or more additional costs.)`, modes `+ {1} — [effect]`; Spree
  means "Choose one or more modes. As an additional cost to cast this spell,
  pay the costs associated with those modes" (702.172a), and the plus signs
  "do not have additional rules meaning" (702.172b). **Tiered**: header line
  `Tiered (Choose one additional cost.)`, modes `• [label] — {cost} —
  [effect]` (`• Fira — {2} — Fire Magic deals 2 damage to each creature.`);
  Tiered means "Choose one. As an additional cost to cast this spell, pay the
  cost associated with that mode" (702.183a). Parse the `{cost}` as that
  mode's additional cost. The Tiered label is read as a flavor word (an
  inference; 207.2d speaks of abilities, not modes). No supported line puts a
  cost directly after a bullet. The CR fixes the semantics; the `+` and `•`
  layouts are Oracle templating.
- **Division** — `"[N] damage divided as you choose among one[, two,] or
  [more] targets"`: the player announces the split when targets are declared
  (601.2d, cross-ref 115.7f) and each chosen target must get ≥ 1 (601.2d).
  Real (Fire): `"Fire deals 2 damage divided as you choose among one or two
  targets."`
- **Dice** (706). The roll instruction names the die kind and count (706.1).
  It is written either `dN` (`Roll a d20.`, `{1}, {T}: Roll a d4 and create a
  number of Treasure tokens equal to the result.`) or as an N-sided die with N
  spelled out (`Roll a six-sided die.`, `Roll X six-sided dice, where X is
  …`). Any positive N is legal and means N equally likely outcomes numbered 1
  to N (706.1a); the supported corpus attests d4, d6, d8, d10, d12, d20, and
  six-sided. The plural of `dN` is unchanged (`Roll two d10 and choose one
  result.`; no `d6s`). Results tables span lines but stay inside the roll's
  ability (706.3b); row forms are in §1.

## 7. Parser starter checklist

1. Split `text` on `\n` into candidate paragraphs/lines.
2. For each line, extract and set aside reminder text — italic `(…)` — keeping
   it as a parameter hint (207.2a); it is not rules text. Flag an unrecognized
   mid-line parenthetical for review instead of dropping it (§1). Also mask
   double-quoted spans, so steps 3–8 see only unquoted text, and parse each
   quoted ability recursively (§1).
3. Recognize band and table markers *before* treating any `Word — ` as an
   ability word: `^[IVX]+(?:, [IVX]+)* — ` = Saga chapter → triggered (714.2);
   `{cost}: Level N` = Class level bar (716.2); `^LEVEL N-M` / `^LEVEL N+` =
   Leveler band (711.2); `^N+ | ` after a `Station` line = Station band
   (721.2). For Class, Leveler and Station, open a band and bind the following
   P/T and ability lines (until the next band) to it (716.2, 711.2, 721.2).
   The result rows that follow a die-roll line (`N | `, `N—M | `, `N+ | `, `N
   or less | `, `N — `, `N or M — `, `• N — `) belong to that ability
   (706.3b).
4. Otherwise classify any `Label — ` prefix in §3's order (die result, mode
   row, anchor word, keyword label, ability word, flavor word). Strip only
   ability words and flavor words (207.2c, 207.2d).
5. If the line is a modal header, consume the following `•`, `+ {cost} —` or
   `{P}…—` lines as its modes and emit one modal ability (700.2, 700.2h,
   700.2i). A modal header (§6) is a `choose <count>` / `chooses <count>`
   clause anywhere in the line (ending in `—`, ending a sentence, or
   coordinated, as in `choose one and …`), or a `Spree`, `Tiered` or pawprint
   header. Bullets under `As … enters, choose A or B.` are anchor-word
   abilities (§1), not modes; bullets after a roll are results rows.
6. Comma-split guard: split on `, `/`; ` only if **every** token, after
   stripping trailing params (`{…}`, `from …`, numbers, a `, where X is …`
   supplement), has a stem resolving in the catalogs (longest-match for
   multi-word stems); emit one keyword ability per token (113.2c). Else treat
   the line as a single ability.
7. Classify the single ability by surface form, testing unquoted text only
   (step 2): top-level `:` → activated (602.1; `\[(\+|−)?([0-9]+|X)\]:` at the
   start of a line or quoted ability → loyalty, 606.2; the corpus minus is
   U+2212, not `-`, but accept both); leading When/Whenever/At → triggered
   (603.1; split coordinated conditions per §2); imperative on an
   instant/sorcery → spell ability (113.3a); otherwise declarative → static
   (113.3d). A When/Whenever/At later in the paragraph is a delayed (603.7) or
   reflexive (603.12) trigger inside this ability, except a second trigger
   condition joined by `and`/`or` (603.1b) and a trigger word right after a
   structural prefix (a stripped ability/flavor word, a keyword dash prefix
   such as `Max speed — `, `∞ — `, `Solved — `, an anchor-word bullet, or a
   station threshold `N+ | `), which opens the ability that prefix carries
   (§2).
8. For triggered abilities, test for an intervening "if" right after the
   trigger condition (603.4). `This ability triggers only if` is not one (§2).
   Test also for reflexive `When you do` sub-triggers (603.12); `If you do` is
   not reflexive (§2).
9. Resolve keyword tokens against `keyword-abilities.json` /
   `keyword-actions.json` / `keywords.json`; parse trailing parameters (cost
   `{…}`, `from <quality>`, `<type>walk`, `Enchant <object>`). A keyword name
   outside a keyword line is a mention, not a new instance (§3).
10. Tag replacement effects by marker — "would … instead" / any "skip" in
    rules text (static or resolving; reminder-text "skip" is not rules text,
    614.1b, 614.10) / "enters with" / "as ~ enters" (614.1) — so they are not
    mis-filed as triggers. Bare `If …, … instead` in the text of a *resolving*
    spell or ability (a spell ability, or an activated or triggered ability's
    effect) is a self-replacement effect (614.15). Bare `If …, … instead` in a
    *static* ability is an ordinary continuous replacement effect (614.1a).
11. Bind references: full or shortened self-name and `this <type>` → source,
    except inside a quoted granted ability, where `this <type>` → the object
    that has the ability and the card name → the granter (§5; 201.5a, 201.5c);
    attachment participle + bare singular head → the source's host (§5);
    pronouns → the antecedent left after §5's filters, by clause and role
    (not plain recency; engine inference, 608.2c); `target …` and `any target`
    → choosers and legal sets (115; a `target` in an activated/triggered
    ability of an instant/sorcery targets that ability, not the spell —
    115.1a); resolve keyword-implied targets from the 702 rule (e.g. `Enchant
    <quality>` → Aura spell target; 115.1b, 115.1e); `another`/`other` →
    anchor exclusion (§5); X/division → variable and split bindings.
12. Per `generalizations.md`'s conclusion (directive 12): the generalized
    mechanics need parameterized semantic targets, not new syntax — the one
    production worth adding preemptively is a triggered-ability instruction
    tail mirroring 602.5d–e ("Resolve this ability only as a sorcery"),
    for Family 3's timing-restricted trigger pattern.

The checklist's parse targets — predicates, counts, values, bindings —
have their semantics specified in `queries.md`, the grammar↔engine
contract.
