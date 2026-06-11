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

# --- mtr ---
t "mtr list shows top sections" 'Tournament Fundamentals' $scripts/mtr --list
t "mtr 1.7 is Head Judge" 'Head Judge' $scripts/mtr 1.7
t "mtr search finds sideboard sections" '[Ss]ideboard' $scripts/mtr --search sideboard
t_fails "mtr bogus section" $scripts/mtr 99.9
t_fails "mtr rejects list with positional" $scripts/mtr --list 1.7

# --- card ---
t "card lightning bolt oracle text" '3 damage to any target' $scripts/card Lightning Bolt
t "card face lookup resolves full name" 'Fire // Ice' $scripts/card Fire
t "card case-insensitive" 'Llanowar Elves' $scripts/card llanowar elves
t_fails "card bogus name" $scripts/card Zzgrokk the Unreal
t_fails "card partial name fails with suggestions" $scripts/card Llanowar El
t "card finds unsupported planes too" '[Pp]lane' $scripts/card Llanowar
t_fails "card empty name rejected" $scripts/card ''
t "card handles quoted names" 'Ach! Hans' $scripts/card '"Ach! Hans, Run!"'

# --- corpus ---
t "corpus finds deathtouch lines" '[Dd]eathtouch' $scripts/corpus --match deathtouch
t "corpus type filter" '.' $scripts/corpus --type Battle --match defeat
t_fails "corpus no matches" $scripts/corpus --match zzqqxyzzy
t "corpus --all reaches un-set lines" '[Gg]otcha' $scripts/corpus --all --match gotcha
t "corpus type filter is case-insensitive" '.' $scripts/corpus --type battle --match defeat
t_fails "corpus rejects invalid regex" $scripts/corpus --match '['

# --- check-citations ---
t "check-citations passes good fixture" 'citations OK|cited rules exist' $scripts/check-citations $fixtures/cite-good.md
t_fails "check-citations fails bad fixture" $scripts/check-citations $fixtures/cite-bad.md
t "check-citations names the missing rules" '999\.99' fish -c "$scripts/check-citations $fixtures/cite-bad.md 2>&1; true"

# --- rulings ---
t "rulings humility has dated entries" '\[\d{4}-\d{2}-\d{2}\]' $scripts/rulings Humility
t "rulings face name resolves to full card" 'Fire // Ice' $scripts/rulings Fire
t "rulings case-insensitive" '\[\d{4}' $scripts/rulings humility
t_fails "rulings bogus card" $scripts/rulings Zzgrokk the Unreal
t_fails "rulings empty arg" $scripts/rulings ''

# (tests appended by later tasks above this line)

echo
echo "$passes passed, $fails failed"
test $fails -eq 0
