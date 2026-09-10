# mtg-rules skill evals

Three instruments live here: invocation probes, answer probes, and the
corpus coverage report. Model runs are paid; offline grading and self-tests are free.

## Invocation probes

`invocation-probes.json` contains seven positive requests covering rules,
cards, policy, grammar, engine modeling, mechanic design, and classification,
plus three negative requests including Magic-themed prose editing. Their prompts
carry no skill name or instruction to look up sources.

```sh
python3 evals/invocation.py policy --dry
python3 evals/invocation.py policy --model sonnet
python3 evals/invocation.py policy --transcript /path/to/trace.jsonl
python3 evals/invocation.py 11 --answer-probe --dry
python3 -m unittest discover -s evals -p 'test_*.py'
```

Each live run starts Claude in a fresh temporary directory with this checkout
loaded via `--plugin-dir`, excluding the development `CLAUDE.md` from discovery.
Provision the runtime and corpus data first. The runner allows skill loading,
file reads, and literal calls to this checkout's lookup scripts. Permission or
data failures are evidence gaps; inspect the saved trace before diagnosing routing.
Host-level settings and other installed skills still affect the run.

The grader requires an init event advertising this skill and a successful final
result. Positive probes additionally require successful Skill/Read loading and
the configured script calls and reference reads. Negative probes reject any
attempt to load or use the MTG skill. Claims in the final prose earn no credit.
The `--answer-probe` mode uses the numbered questions from `probes.json` unchanged,
requiring card/rule lookups and the listed `frame_docs` as observable routes.

Evidence recognition covers literal script paths (optionally run with `fish`
or after `cd &&`) and explicit reference Read calls. Compound pipelines, shell
wrappers, and alternative valid routes require manual trace review. Tool success
establishes that evidence was obtained; answer correctness still needs semantic
review. A passing discovery probe is not an answer-quality verdict.

Run selected positive and negative cases after instruction changes. Each live
invocation is one paid agent run; offline tests validate the grader, not model behavior.

## Corpus coverage report (free)

`evals/coverage.fish` measures how much of the oracle-text grammar surface
the taxonomy docs account for: `coverage-config.json` maps each taxonomy
kind (keyword lines, activated/triggered/static shapes, modal bullets,
replacement markers, Gate/Toll markers, cost lines, …) to a list of
case-insensitive ERE patterns; the report prints, per kind, how many of the
distinct supported oracle lines (the same extraction as
`skills/mtg-rules/scripts/corpus`) match any of that kind's patterns, plus the union
coverage across all kinds — the headline number. Needs the cards data tier
(`derived/cards.jsonl`); no agent calls.

```sh
evals/coverage.fish               # the report
evals/coverage.fish --unmatched   # print the gap lines no kind matches
```

Honest v1: the patterns are structural proxies derived from the reference
docs, deliberately approximate; kinds overlap (the union dedups), and a
match means "this kind's surface shape accounts for the line," not "a
parser exists." "Is the taxonomy done?" becomes: drive union coverage
toward 100% by refining patterns until every gap line is either covered or
explained.

## Probe eval (paid)

Regression eval for the **skill**, not the data: each probe asks a headless
agent one of the eighteen rulings-check questions with explicit skill instructions and grades the answer
against the citations and verdicts derived in
`evals/rulings-check.md`. Run after CR refreshes or reference-doc edits to
spot missing verdict terms or citations. This test does not measure autonomous
invocation; use the invocation probes above for discovery and route evidence.
This directory lives outside the skill's runtime reference tree.

**Cost warning:** every non-`--dry` run is one full `claude -p` agent run
(skill lookups included). Spot-check single probes; don't loop all 18 casually.

## Usage

```sh
evals/run_probe.fish --selftest        # free: verify the grader itself
evals/run_probe.fish 11 --dry          # free: print the prompt for probe 11
evals/run_probe.fish 11                # paid: run probe 11 (default model: sonnet)
evals/run_probe.fish 11 --model opus   # paid: pick the model
```

If the skill's data isn't in a default location, set `MTG_RULES_DATA` so the
spawned agent's scripts can find it (it propagates through the environment):
`MTG_RULES_DATA=/path/to/data evals/run_probe.fish 11`.

## Grading rubric

- **expected_verdict_keywords** — case-insensitive substrings; **all** must appear.
- **expected_citations** — exact dotted rule numbers (`613.4` does not credit
  `613.4b`); **at least half** must appear.
- PASS = both bars met; misses are printed line by line. Transcripts are kept
  in `/tmp/mtg-probe-<id>.*.txt`.

## Adding probes

When `rulings-check.md` gains probe N: append an object to `probes.json` with
`id: N`, the cards, frame docs, a **self-contained** question (answerable
without reading rulings-check.md), the load-bearing dotted citations from the
derivation, and 3-6 verdict keywords. Verify each citation against the derivation
(following its pointer for shared worked examples), run `jq . evals/probes.json`,
then `run_probe.fish N --dry`. Validate the record with
`skills/mtg-rules/scripts/cite --config evals/cite-config.json check`.
After revalidation, bump `meta.cr_effective` with the doc's header date.
