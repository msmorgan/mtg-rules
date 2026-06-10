#!/usr/bin/env fish
# Test harness for mtg-rules skill scripts.
#   t <desc> <regex> <command…>        — assert stdout matches regex
#   t_fails <desc> <command…>          — assert non-zero exit

set -g passes 0
set -g fails 0

function t
    set -l desc $argv[1]
    set -l expect $argv[2]
    set -l out ($argv[3..] 2>/dev/null | string collect)
    if string match -rq -- $expect "$out"
        set passes (math $passes + 1)
    else
        set fails (math $fails + 1)
        echo "FAIL: $desc"
        echo "  expected match: $expect"
        echo "  got: "(string sub -l 200 -- "$out")
    end
end

function t_fails
    set -l desc $argv[1]
    if $argv[2..] >/dev/null 2>&1
        set fails (math $fails + 1)
        echo "FAIL: $desc (expected non-zero exit)"
    else
        set passes (math $passes + 1)
    end
end

set -g repo (path resolve (status dirname)/..)
set -g scripts $repo/skill/scripts
set -g fixtures $repo/tests/fixtures

# --- lib.fish ---
t "lib resolves rules dir" 'data/rules$' fish -c "source $scripts/lib.fish; or exit 1; echo \$rules_dir"

# --- rule ---
t "rule prints a subrule" 'concedes leaves the game' $scripts/rule 104.3a
t "rule walks rule family" '601\.2a' $scripts/rule 601.2
t "rule family excludes neighbors" '^0$' fish -c "$scripts/rule 601.2 | grep -c '^601\.3' ; true"
t "rule prints examples" 'Example:' $scripts/rule 702.19c
t "rule prints whole section" '120\.6' $scripts/rule 120
t_fails "rule rejects bogus number" $scripts/rule 999.9
t_fails "rule rejects garbage arg" $scripts/rule abc

# (tests appended by later tasks above this line)

echo
echo "$passes passed, $fails failed"
test $fails -eq 0
