#!/usr/bin/env fish
# run_probe.fish — run and grade ONE rulings-check probe against a headless agent.
#
#   evals/run_probe.fish <probe-id> [--model sonnet] [--dry] [--selftest]
#
# COSTS MONEY when run for real: each probe is one `claude -p` agent run.
# Use --dry to preview the prompt, --selftest to exercise the grader for free.
# See evals/README.md for the rubric.

set -l evals_dir (path resolve (status dirname))
set -l probes_json $evals_dir/probes.json

argparse 'm/model=' 'dry' 'selftest' 'h/help' -- $argv
or exit 2

if set -q _flag_help
    echo "usage: run_probe.fish <probe-id> [--model <m>] [--dry] [--selftest]"
    echo "  --model <m>  claude model alias (default: sonnet)"
    echo "  --dry        print the prompt that would be sent; do not invoke claude"
    echo "  --selftest   grade canned answers for probe 1 to verify the grader; no claude run"
    exit 0
end

set -l model sonnet
set -q _flag_model; and set model $_flag_model

command -q jq; or begin
    echo >&2 "run_probe: jq not found on PATH"
    exit 1
end
test -r $probes_json; or begin
    echo >&2 "run_probe: $probes_json not found or unreadable"
    exit 1
end

# --selftest always grades against probe 1; otherwise an id is required.
if set -q _flag_selftest
    set -g probe_id 1
else
    if test (count $argv) -ne 1
        echo >&2 "usage: run_probe.fish <probe-id> [--model <m>] [--dry] [--selftest]"
        exit 2
    end
    set -g probe_id $argv[1]
end
string match -rq '^\d+$' -- $probe_id; or begin
    echo >&2 "run_probe: probe id must be a positive integer, got '$probe_id'"
    exit 2
end

set -l n_match (jq --argjson id $probe_id '[.probes[] | select(.id == $id)] | length' $probes_json)
if test "$n_match" != 1
    echo >&2 "run_probe: no probe with id $probe_id in $probes_json"
    exit 2
end

set -g citations (jq -r --argjson id $probe_id '.probes[] | select(.id == $id) | .expected_citations[]' $probes_json)
set -g keywords (jq -r --argjson id $probe_id '.probes[] | select(.id == $id) | .expected_verdict_keywords[]' $probes_json)
set -l question (jq -r --argjson id $probe_id '.probes[] | select(.id == $id) | .question' $probes_json)

# Grade $argv[1] (the full answer text) against global $citations / $keywords.
# PASS = every keyword present (case-insensitive substring) AND at least half
# the citations present (exact dotted number, not a longer rule like 613.4b
# when 613.4 is expected). Returns 0 on PASS.
function grade
    set -l answer $argv[1]
    set -l cit_total (count $citations)
    set -l cit_found 0
    set -l cit_missed
    for c in $citations
        if string match -rq -- (string escape --style=regex -- $c)'(?![0-9a-z])' $answer
            set cit_found (math $cit_found + 1)
        else
            set -a cit_missed $c
        end
    end
    set -l kw_total (count $keywords)
    set -l kw_missed
    for k in $keywords
        string match -riq -- (string escape --style=regex -- $k) $answer
        or set -a kw_missed $k
    end
    set -l kw_found (math $kw_total - (count $kw_missed))

    for c in $cit_missed
        echo "  missing citation: $c"
    end
    for k in $kw_missed
        echo "  missing keyword:  $k"
    end
    if test (count $kw_missed) -eq 0; and test (math "$cit_found * 2") -ge $cit_total
        echo "PASS: probe $probe_id — $cit_found/$cit_total citations, $kw_found/$kw_total keywords"
        return 0
    end
    echo "FAIL: probe $probe_id — $cit_found/$cit_total citations, $kw_found/$kw_total keywords (need all keywords + >=half citations)"
    return 1
end

if set -q _flag_selftest
    set -l good "Both Humility and Opalescence set base power and toughness, which applies in sublayer 7b (613.4b). Opalescence's type-change is layer 4 and Humility's ability removal is layer 6, but per 613.6 each effect keeps applying in later layers even after its source loses the ability. Within sublayer 7b the effects apply in timestamp order (613.7), so the later one applies last and wins: with Humility entering last, every creature — including Humility itself, animated by Opalescence — ends up 1/1 with no abilities. With the timestamps reversed, they'd all be set by Opalescence afterward instead."
    set -l bad "Opalescence just makes Humility a 4/4 creature; the order they entered doesn't matter."
    echo "== selftest 1/2: canned GOOD answer for probe 1 (expect PASS)"
    grade "$good"
    set -l good_st $status
    echo "== selftest 2/2: canned BAD answer for probe 1 (expect FAIL)"
    grade "$bad"
    set -l bad_st $status
    if test $good_st -eq 0; and test $bad_st -ne 0
        echo "selftest OK: grader passed the good answer and failed the bad one"
        exit 0
    end
    echo >&2 "selftest FAILED: good=$good_st (want 0), bad=$bad_st (want nonzero)"
    exit 1
end

set -l prompt "$question

Answer using the mtg-rules skill to verify every claim against the Comprehensive Rules — do not answer from memory. Cite the specific dotted rule numbers (like 601.2f) that decide each point, and finish with a clear verdict."

if set -q _flag_dry
    echo "-- probe $probe_id prompt (model: $model; not invoking claude) --"
    printf '%s\n' $prompt
    exit 0
end

command -q claude; or begin
    echo >&2 "run_probe: 'claude' CLI not found on PATH — cannot run the probe (use --dry to preview)"
    exit 1
end

echo "running probe $probe_id via claude -p (model: $model) — one paid agent run..."
set -l transcript (mktemp /tmp/mtg-probe-$probe_id.XXXXXX.txt)
claude -p "$prompt" --model $model >$transcript 2>&1
set -l claude_st $status
if test $claude_st -ne 0
    echo >&2 "run_probe: claude exited $claude_st — transcript kept at $transcript"
    exit 1
end
echo "transcript: $transcript"
echo
grade "$(cat $transcript)"
