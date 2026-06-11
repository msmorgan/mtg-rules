# mtg-rules skill evals

Regression eval for the **skill**, not the data: each probe asks a headless
agent one of the eighteen rulings-check questions cold and grades the answer
against the citations and verdicts derived in
`skill/references/rulings-check.md`. Run after CR refreshes or reference-doc
edits to catch a skill that stopped routing, citing, or concluding correctly.
This directory deliberately lives outside `skill/` so the plugin doesn't ship it.

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
derivation, and 3-6 verdict keywords. Verify each citation appears in section
N of the doc, run `jq . evals/probes.json`, then `run_probe.fish N --dry`.
Bump `meta.cr_effective` whenever the doc's header date changes.
