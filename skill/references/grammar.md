# Oracle Text — Grammar for Parsing

*Synthesized from the Comprehensive Rules effective 2026-04-17
(`data/rules/cr.json`). Orientation only — verify load-bearing specifics
with `scripts/rule` before citing. Run `scripts/check-citations` after CR
refreshes.*

How to slice an Oracle-text string into abilities and recognize each one's
surface form. Terminal vocabularies live in `data/catalogs/*.json` and
`data/rules/keywords.json`; CR rules cited here govern what the forms *mean*.
Every oracle example below is real text fetched via `scripts/card` or
`scripts/corpus`. For what the abilities *do*, see `abilities.md`; for
replacement-effect semantics see `effects.md` §6.

## 1. Segmentation

MTGJSON's `text` field separates paragraphs/lines with `\n`. The default
unit is **one paragraph = one ability**, but four cases break that:

- **Comma-separated keyword line = multiple abilities.** Keyword abilities
  written on one line, separated by commas (or whitespace), are each a
  separate ability (702.1; per-keyword rules in 702 treat each as its own
  ability). Split on `, ` *within* a line only when every token resolves to
  a keyword in the catalogs.
- **Modal blocks span lines.** A `Choose …` header plus its bulleted modes
  (`•` lines) is *one* ability with multiple modes (700.2); do not split the
  bullets into separate abilities.
- **Ability-word / flavor-word prefix.** `Word — text` puts an italicized
  word before an em dash; the word has no rules meaning and is not part of
  segmentation (207.2c ability words, 207.2d flavor words). Strip the prefix,
  parse the remainder normally.
- **Reminder text is not rules text.** Italic text in parentheses summarizes
  a rule and has no game function (207.2, 207.2a). Discard it before parsing
  (but see §3 — it may be the only place a keyword's parameters are spelled
  out in plain English).

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
  `:` not inside parentheses or a `{…}` symbol.
- **Triggered** — `"[When/Whenever/At] [trigger condition], [effect].
  [Instructions (if any).]"` (113.3c, 603.1). Begins with **When**,
  **Whenever**, or **At**. Trailing instructions (target limits, "can't be
  countered") function on the stack and are not the effect (603.1a).
  - **Intervening "if"** — `"When/Whenever/At [event], if [condition],
    [effect]."` The condition is checked twice: on trigger and again on
    resolution (603.4). Only an "if" *immediately after* the trigger
    condition is intervening; "if" elsewhere is plain English (603.4).
  - **Reflexive** — `"… When you do, …"` / `"… When [something happens]
    this way, …"`: a triggered ability created mid-resolution that triggers
    on whether an earlier action in the same resolution happened (603.12).
    Real: Sorin's `"[+1]: You may sacrifice a Vampire. When you do, Sorin
    deals 3 damage to any target and you gain 3 life."`
- **Static** — declarative statement that is "simply true" (113.3d); no
  cost, no trigger word, no colon. e.g. Questing Beast's
  `"… can't be blocked by creatures with power 2 or less."`
- **Spell ability** — imperative instructions on an instant/sorcery,
  followed as the spell resolves; any text on an instant/sorcery is a spell
  ability unless it is activated, triggered, or a qualifying static (113.3a).
  e.g. Fire's `"Fire deals 2 damage divided as you choose among one or two
  targets."`

## 3. Keyword grammar

Two terminal vocabularies: **keyword abilities** (702) in
`data/catalogs/keyword-abilities.json` (220 entries) and
`data/rules/keywords.json`; **keyword actions** (701) in
`keyword-actions.json` (74 entries, e.g. Scry, Exile, Sacrifice, Mill).
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
- **Landwalk family** — `<Type>walk`: `Forestwalk`, `Islandwalk`,
  `Mountainwalk`, `Swampwalk`, `Plainswalk`, `Desertwalk`, plus the
  generic/qualified `Landwalk`, `Legendary landwalk`, `Nonbasic landwalk`,
  and granted forms like `snow landwalk of the chosen type` (all listed in
  `keyword-abilities.json`).
- **Stacked keywords with mixed punctuation:** `Ward {1}, haste` and
  `Protection from black; flanking (…)` show that `, ` and `; ` both
  delimit keyword abilities on a line.

When `scripts/define`/`scripts/keyword` lacks a parameterized form, the
keyword's **reminder text** in parens usually states the parameter in plain
English — e.g. `Ward {2} (Whenever this … becomes the target of a spell or
ability an opponent controls, counter it unless that player pays {2}.)`.

**Ability words vs flavor words** — both italic, both prefix `Word — text`,
both have no rules meaning (207.2c, 207.2d). Differ only in scope: an
**ability word** is a fixed closed list tying together similar cards
(`ability-words.json`, 69 entries: landfall, metalcraft, delirium, …); a
**flavor word** is bespoke per card (`flavor-words.json`, 549 entries, mostly
Universes Beyond — "Fire", "Teleport", "Exterminate!"). To classify a
prefix, look it up: ability-word list → ability word; else flavor word.
Neither affects parsing beyond stripping the prefix.

## 4. Replacement-effect tense markers

Replacement effects are continuous, never use the stack (614.1; effects.md
§6). Recognize them by surface markers — they are *not* triggered abilities
even though some resemble triggers:

- **"… would …, … instead"** (614.1a) — the dominant form. Real:
  `"… if that creature would deal combat damage to one of your opponents,
  it deals triple that damage to that player instead."` Also
  `"If that spell would be put into your graveyard, exile it instead."`
- **"skip"** (614.1b) — replaces a step/phase/turn with nothing. Real:
  `"You skip your next turn."`, `"You skip your next untap step."`
- **ETB modifiers** (614.1c): `"~ enters with …"`, `"As ~ enters …"`,
  `"~ enters as …"`. Real: `"As Alhammarret enters, each opponent reveals
  their hand…"`; `"… that creature enters with that many additional +1/+1
  counters on it."`
- **Continuous "~ enters …" / "[objects] enter …"** (614.1d); **"as ~ is
  turned face up …"** (614.1e).

Caution: `"As [an additional cost to cast] …"` is a casting/cost clause, not
a replacement effect — disambiguate `As ~ enters` (614.1c) from `As an
additional cost …` by what follows "As".

## 5. Reference grammar

How text names the objects and players it acts on:

- **Self-reference.** Modern Oracle text names the source by full card name
  (`"Questing Beast can't be blocked …"`, `"Sorin deals 3 damage …"`) or by
  `"this <type>"` (`"this creature deals 2 damage …"`, `"this permanent"`,
  `"this land"`). Both denote the source object; bind them to it.
- **Pronoun binding.** `"it"` / `"that creature"` / `"that player"` /
  `"those creatures"` refer back to a previously named object or player in
  the same ability. Questing Beast: `"… it deals that much damage to target
  planeswalker **that player** controls"` — `it` = Questing Beast, `that
  player` = the opponent dealt damage.
- **`target [something]`** (115.1) — the *only* word that makes a spell or
  ability targeted (115.10a; `"you"` never indicates a target, 115.10b).
  Targets are objects and/or players chosen as the spell/ability goes on the
  stack and can't change except by an effect that says so (115.1). Only
  permanents are legal unless the text says otherwise (115.2). The same
  `target` instance can't pick one object twice; distinct `target` instances
  can share an object (115.3).
- **`any target`** (115.4) — a damage shorthand expanding to **any creature,
  player, planeswalker, or battle** (115.4). Variants `another target`,
  `two targets` behave likewise; noncreature artifacts and spells can't be
  chosen (115.4).
- **Quantifiers:** `"each [player/creature]"` (untargeted, all qualifying),
  `"up to one/two/N target …"` (may choose fewer, even zero — 115.6),
  `"another target …"` (excludes the source). Real: `"Chandra deals 1
  damage to up to one target player or planeswalker."`
- **APNAP note for parsers:** turn-order (APNAP) resolution of simultaneous
  choices is an *engine-runtime* concern, not a parsing concern — the
  grammar only needs to capture *who chooses* (`"you"`, `"target player"`,
  `"each player"`), not the order.

## 6. Numbers, variables, choices

- **Variables.** `X` is a value defined elsewhere in the same text
  (`"where X is …"`, `"X is the number of …"`) or by the cost paid; `*` (CDA)
  is a self-referential count. Real: `"Target opponent skips their next X
  turns, where X is the number of coins that came up heads."`
- **Modal headers** (700.2) — a `Choose …` line followed by `•`-bulleted
  modes. Corpus forms: `Choose one —`, `Choose two —`, `Choose one or
  both —`, `Choose one or more —`. Conditional upgrades exist:
  `"Choose one. If this spell was kicked, choose any number instead."` Pick
  count is part of casting/putting-on-stack (700.2a–b); a mode with no legal
  target can't be chosen (700.2a).
- **Escalate** is the additive cost for extra modes — `Escalate {1} (Pay
  this cost for each mode chosen beyond the first.)` — not itself a mode.
- **Division** — `"[N] damage divided as you choose among one[, two,] or
  [more] targets"`: the player announces the split when targets are declared
  (601.2d, cross-ref 115.7f) and each chosen target must get ≥ 1 (601.2d).
  Real (Fire): `"Fire deals 2 damage divided as you choose among one or two
  targets."`

## 7. Parser starter checklist

1. Split `text` on `\n` into candidate paragraphs/lines.
2. For each line, extract and set aside reminder text — italic `(…)` —
   keeping it as a parameter hint (207.2a); it is not rules text.
3. Detect an ability-word / flavor-word prefix (`Word — …`); strip it,
   classify via `ability-words.json` vs `flavor-words.json` (207.2c/d).
4. If the line is a `Choose …` header, consume following `•` lines as its
   modes — emit one modal ability, not many (700.2).
5. If every comma/semicolon-delimited token on the line is a catalog
   keyword, emit one keyword ability per token (702.1); else treat the line
   as a single ability.
6. Classify the single ability by surface form: top-level `:` → activated
   (602.1); leading When/Whenever/At → triggered (603.1); imperative on an
   instant/sorcery → spell ability (113.3a); otherwise declarative → static
   (113.3d).
7. For triggered abilities, test for intervening "if" right after the
   trigger (603.4) and for reflexive "When you do" sub-triggers (603.12).
8. Resolve keyword tokens against `keyword-abilities.json` /
   `keyword-actions.json` / `keywords.json`; parse trailing parameters
   (cost `{…}`, `from <quality>`, `<type>walk`, `Enchant <object>`).
9. Tag replacement effects by marker — "would … instead" / "skip" /
   "enters with" / "as ~ enters" (614.1) — so they are not mis-filed as
   triggers.
10. Bind references: source name / "this <type>" → source; pronouns → last
    matching antecedent; `target …` and `any target` → choosers and legal
    sets (115); X/division → variable and split bindings.
