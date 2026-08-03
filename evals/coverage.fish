#!/usr/bin/env fish
# coverage.fish — corpus coverage report: per taxonomy kind, the % of
# distinct supported oracle-text lines matched by that kind's patterns
# (evals/coverage-config.json), plus union coverage across all kinds.
# Turns "is the taxonomy done?" into a number. Free: local grep only,
# no agent calls. Needs the cards data tier (derived/cards.jsonl).
#
#   evals/coverage.fish               # the report
#   evals/coverage.fish --unmatched   # print the lines no kind matches (gap hunting)

set -l evals_dir (path resolve (status dirname))
source $evals_dir/../skills/mtg-rules/scripts/lib.fish; or exit 1

argparse 'u/unmatched' 'h/help' -- $argv; or exit 2
if set -q _flag_help
    echo "usage: coverage.fish [--unmatched]"
    echo "  --unmatched  print the distinct supported oracle lines matched by no kind"
    exit 0
end

set -l cfg $evals_dir/coverage-config.json
test -r $cfg; or die "coverage: $cfg missing"
jq -e . $cfg >/dev/null 2>&1; or die "coverage: $cfg is not valid JSON"
set -l idx $derived_dir/cards.jsonl
test -f $idx; or die "coverage: $derived_dir/cards.jsonl missing — cards tier; run scripts/build_derived.fish (repo) or setup-data --cards (plugin)"

set -g work (mktemp -d)
function _coverage_cleanup --on-event fish_exit
    test -n "$work"; and rm -rf $work
end

# Corpus: distinct supported oracle lines — same extraction as scripts/corpus.
jq -r 'select(.supported) | .text // empty | split("\n")[] | select(length > 0)' $idx \
    | sort -u >$work/lines.txt
set -l total (count <$work/lines.txt)
test $total -gt 0; or die "coverage: empty corpus"

touch $work/union-all.txt
set -l report
for kind in (jq -r '.kinds | keys_unsorted[]' $cfg)
    jq -r --arg k $kind '.kinds[$k].patterns[]' $cfg >$work/pat.txt
    grep -iE -f $work/pat.txt $work/lines.txt >$work/matched.txt
    set -l n (count <$work/matched.txt)
    set -a report (printf '  %-22s %6d  %5.1f%%' $kind $n (math "100 * $n / $total"))
    cat $work/matched.txt >>$work/union-all.txt
end
sort -u $work/union-all.txt >$work/union.txt
set -l matched (count <$work/union.txt)

if set -q _flag_unmatched
    comm -23 $work/lines.txt $work/union.txt
    exit 0
end

echo "corpus coverage — $total distinct supported oracle lines ("(path basename $cfg)")"
printf '%s\n' $report
printf 'union coverage: %d / %d lines (%.1f%%)\n' $matched $total (math "100 * $matched / $total")
echo "(kinds overlap; union is the headline. --unmatched prints the gap lines.)"
