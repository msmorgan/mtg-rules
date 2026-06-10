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

# --- rule-search ---
t "rule-search finds deathtouch rules" '702\.2' $scripts/rule-search deathtouch
t "rule-search truncation notice" 'more matches' $scripts/rule-search --max 1 'the'
t_fails "rule-search misses garbage" $scripts/rule-search 'zzqqxyzzy'
t_fails "rule-search rejects --max abc" $scripts/rule-search --max abc deathtouch

# --- define ---
t "define deathtouch cites 702.2" '702\.2' $scripts/define deathtouch
t "define handles multiword terms" '[Aa]ctive [Pp]layer' $scripts/define active player
t "define falls back to unofficial" 'unofficial' $scripts/define battalion
t_fails "define misses garbage" $scripts/define zzgrok

t "define normalizes apostrophe input" '[Cc]ity.s [Bb]lessing' $scripts/define "city's blessing"
t "define reaches curly-quoted keys" '[Ii]ntervening' $scripts/define 'intervening "if" clause'
t_fails "define near-match still exits 1" $scripts/define strike

# --- keyword ---
t "keyword trample → 702.19" '702\.19' $scripts/keyword trample
t "keyword scry → 701.22 (action)" '701\.22' $scripts/keyword scry
t "keyword multiword" '702\.7.*[Ff]irst [Ss]trike' $scripts/keyword first strike
t_fails "keyword bogus" $scripts/keyword zzgrok
t "keyword tap → 701.26 (glossary fallback)" '701\.26' $scripts/keyword tap

# (tests appended by later tasks above this line)

echo
echo "$passes passed, $fails failed"
test $fails -eq 0
