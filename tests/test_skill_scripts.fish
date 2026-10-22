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
set -g scripts $repo/skills/mtg-rules/scripts
set -g fixtures $repo/tests/fixtures

# --- plugin layout ---
t "Codex manifest names the plugin" '^mtg-rules$' \
    jq -r '.name' $repo/.codex-plugin/plugin.json
t "Codex manifest discovers the skills directory" '^\./skills/$' \
    jq -r '.skills' $repo/.codex-plugin/plugin.json
t "Codex manifest leaves hooks to conventional discovery" '^false$' \
    jq -r 'has("hooks")' $repo/.codex-plugin/plugin.json
t "Codex marketplace installs the repository root" '^url \./$' \
    jq -r '.plugins[0].source | [.source, .url] | join(" ")' $repo/.agents/plugins/marketplace.json
t "Codex marketplace has a collision-free development name" '^mtg-rules-dev$' \
    jq -r '.name' $repo/.agents/plugins/marketplace.json
t "Codex and Claude manifests have the same version" '^true$' fish -c \
    "test (jq -r .version $repo/.codex-plugin/plugin.json) = (jq -r .version $repo/.claude-plugin/plugin.json); and echo true"
t "OpenCode package manifest matches plugin name and version" '^true$' fish -c \
    "test (jq -r .name $repo/package.json) = mtg-rules; and test (jq -r .version $repo/package.json) = (jq -r .version $repo/.codex-plugin/plugin.json); and echo true"

# --- shared data discovery ---
t "lib resolves rules dir" 'data/rules$' fish -c "set -l rules_dir ($scripts/data-path --field rules); set -l data_dir ($scripts/data-path); set -l mtgjson_dir ($scripts/data-path --field mtgjson); or exit 1; echo \$rules_dir"

# --- rule ---
t "rule prints a subrule" 'concedes leaves the game' $scripts/rule 104.3a
t "rule walks rule family" '601\.2a' $scripts/rule 601.2
t "rule family excludes neighbors" '^0$' fish -c "$scripts/rule 601.2 | grep -c '^601\.3' ; true"
t "rule walks through double-lettered subrules" '704\.5aa' $scripts/rule 704.5
t "rule prints an exact double-lettered subrule" 'speed becomes 1' $scripts/rule 704.5aa
t "rule prints examples" 'Example:' $scripts/rule 702.19c
t "rule prints whole section" '120\.6' $scripts/rule 120
t_fails "rule rejects bogus number" $scripts/rule 999.9
t_fails "rule rejects garbage arg" $scripts/rule abc

# --- rule-search ---
t "rule-search finds deathtouch rules" '702\.2' $scripts/rule-search deathtouch
t "rule-search truncation notice" 'more matches' $scripts/rule-search --max 1 the
t_fails "rule-search misses garbage" $scripts/rule-search zzqqxyzzy
t_fails "rule-search rejects --max abc" $scripts/rule-search --max abc deathtouch

# --- define ---
t "define deathtouch cites 702.2" '702\.2' $scripts/define deathtouch
t "define handles multiword terms" '[Aa]ctive [Pp]layer' $scripts/define active player
t "define falls back to unofficial" unofficial $scripts/define battalion
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
t "card full-name mode excludes a matching face of another card" '^1$' fish -c \
    "$scripts/card --full-name 'Lightning Bolt' | grep -c '^# '"
t "card full-name mode rejects a lone multiface face" \
    '^card: no exact match' fish -c "$scripts/card --full-name Start 2>&1; true"
t "card combined name renders every face" '(?s)face: Start.*face: Finish' \
    $scripts/card --full-name 'Start // Finish'
t "card case-insensitive" 'Llanowar Elves' $scripts/card llanowar elves
t_fails "card bogus name" $scripts/card Zzgrokk the Unreal
t_fails "card partial name fails with suggestions" $scripts/card Llanowar El
t "card finds unsupported planes too" '[Pp]lane' $scripts/card Llanowar
t_fails "card empty name rejected" $scripts/card ''
t "card handles quoted names" 'Ach! Hans' $scripts/card '"Ach! Hans, Run!"'

set -l sqlite_card_data (mktemp -d)
mkdir -p $sqlite_card_data/rules $sqlite_card_data/mtgjson
echo '{}' >$sqlite_card_data/rules/cr.json
set -l card_db (fish -c "set -l rules_dir ($scripts/data-path --field rules); set -l data_dir ($scripts/data-path); set -l mtgjson_dir ($scripts/data-path --field mtgjson); echo \$mtgjson_dir/AllPrintings.sqlite")
ln -s $card_db $sqlite_card_data/mtgjson/AllPrintings.sqlite
t "card lookup needs only MTGJSON SQLite" '3 damage to any target' \
    env MTG_RULES_DATA=$sqlite_card_data $scripts/card Lightning Bolt
rm -rf $sqlite_card_data

# --- card_context.py UserPromptSubmit hook ---
set -g cardhook $scripts/hooks/card_context.py

function cardhookjson --argument-names prompt
    jq -nc --arg p $prompt '{session_id: "card-test", prompt: $p}' \
        | python3 $cardhook
end

function cardhookrun --argument-names prompt
    cardhookjson "$prompt" | jq -r '.hookSpecificOutput.additionalContext // empty'
end

function cardhookcount --argument-names prompt pattern
    cardhookrun "$prompt" | grep -c -- $pattern
end

t "card hook injects an exact double-bracketed card" 'Whenever an attacking creature' \
    cardhookrun 'Explain [[Brazen Cannonade]].'
t "card hook emits UserPromptSubmit additionalContext" '^UserPromptSubmit$' \
    fish -c "jq -nc --arg p '[[Brazen Cannonade]]' '{prompt:\$p}' | python3 $cardhook | jq -r .hookSpecificOutput.hookEventName"
t "card hook ignores a single-bracketed card" '^$' \
    cardhookrun 'Explain [Brazen Cannonade].'
t "card hook renders both faces of a canonical combined name" \
    '(?s)face: Start.*face: Finish' cardhookrun '[[Start // Finish]]'
t "card hook rejects a lone multiface face" '^$' cardhookrun '[[Start]]'
t "card hook ignores non-card double brackets" '^$' cardhookrun 'See [[the previous section]].'
t "card hook deduplicates repeated names case-insensitively" '^1$' \
    cardhookcount '[[Brazen Cannonade]] and [[brazen cannonade]]' '^# Brazen Cannonade$'
t "card hook survives malformed stdin" '^\{\}$' \
    fish -c "printf 'not json' | python3 $cardhook; true"
t "plugin hooks.json registers UserPromptSubmit" '^command$' \
    jq -r '.hooks.UserPromptSubmit[0].hooks[0].type' $repo/hooks/hooks.json
t "plugin hooks.json points at the card hook script" '^true$' fish -c \
    "test -x $repo/(jq -r '.hooks.UserPromptSubmit[0].hooks[0].command' $repo/hooks/hooks.json | string replace -r '.*PLUGIN_ROOT\}\}?/' '' | string trim -c '\"'); and echo true"

set -l agy_trans_tmp (mktemp -d)
echo '{"type":"USER_INPUT","content":"Explain [[Brazen Cannonade]]."}' > $agy_trans_tmp/transcript.jsonl
t "card hook injects cards via AGY transcript into injectSteps" 'Whenever an attacking creature' \
    fish -c "jq -nc --arg t $agy_trans_tmp/transcript.jsonl '{transcriptPath:\$t,invocationNum:1}' | python3 $cardhook | jq -r '.injectSteps[0].ephemeralMessage // empty'"
echo '{"type":"USER_INPUT","content":"Explain [Brazen Cannonade]."}' > $agy_trans_tmp/transcript.jsonl
t "card hook returns empty object for AGY transcript without bracketed cards" '^\{\}$' \
    fish -c "jq -nc --arg t $agy_trans_tmp/transcript.jsonl '{transcriptPath:\$t,invocationNum:1}' | python3 $cardhook"
rm -rf $agy_trans_tmp

t "agy hooks.json registers card context PreInvocation" '^command$' \
    jq -r '."mtg-rules-card-context".PreInvocation[0].type' $repo/hooks.json
t "agy hooks.json points at the card hook script" '^true$' fish -c \
    "test -x $repo/(jq -r '.\"mtg-rules-card-context\".PreInvocation[0].command' $repo/hooks.json | string replace -r '^python3 \\./' ''); and echo true"

# --- corpus ---
t "corpus finds deathtouch lines" '[Dd]eathtouch' $scripts/corpus --match deathtouch
t "corpus type filter" '.' $scripts/corpus --type Battle --match defeat
t_fails "corpus no matches" $scripts/corpus --match zzqqxyzzy
t "corpus --all reaches un-set lines" '[Gg]otcha' $scripts/corpus --all --match gotcha
t "corpus type filter is case-insensitive" '.' $scripts/corpus --type battle --match defeat
t_fails "corpus rejects invalid regex" $scripts/corpus --match '['

# --- rulings ---
t "rulings humility has dated entries" '\[\d{4}-\d{2}-\d{2}\]' $scripts/rulings Humility
t "rulings face name resolves to full card" 'Fire // Ice' $scripts/rulings Fire
t "rulings case-insensitive" '\[\d{4}' $scripts/rulings humility
t_fails "rulings bogus card" $scripts/rulings Zzgrokk the Unreal
t_fails "rulings empty arg" $scripts/rulings ''

# --- data resolution chain ---
mkdir -p /tmp/mtg-data-test/rules
echo '{}' >/tmp/mtg-data-test/rules/cr.json
t "lib honors MTG_RULES_DATA" '/tmp/mtg-data-test/rules$' fish -c "set -x MTG_RULES_DATA /tmp/mtg-data-test; set -l rules_dir ($scripts/data-path --field rules); set -l data_dir ($scripts/data-path); set -l mtgjson_dir ($scripts/data-path --field mtgjson); or exit 1; echo \$rules_dir"
t "lib ignores invalid MTG_RULES_DATA" 'data/rules$' fish -c "set -x MTG_RULES_DATA /nonexistent; set -l rules_dir ($scripts/data-path --field rules); set -l data_dir ($scripts/data-path); set -l mtgjson_dir ($scripts/data-path --field mtgjson); or exit 1; echo \$rules_dir"
rm -rf /tmp/mtg-data-test

set -l plugin_data_test (mktemp -d)
mkdir -p $plugin_data_test/rules
echo '{}' >$plugin_data_test/rules/cr.json
t "lib honors host-provided PLUGIN_DATA" "$plugin_data_test/rules\$" \
    env -u MTG_RULES_DATA PLUGIN_DATA=$plugin_data_test fish -c "set -l rules_dir ($scripts/data-path --field rules); set -l data_dir ($scripts/data-path); set -l mtgjson_dir ($scripts/data-path --field mtgjson); or exit 1; echo \$rules_dir"
rm -rf $plugin_data_test

set -l codex_test_root (mktemp -d)
set -l codex_test_home $codex_test_root/home
set -l codex_test_skill $codex_test_home/plugins/cache/mtg-rules/mtg-rules/1.10.0/skills/mtg-rules
mkdir -p $codex_test_skill/scripts $codex_test_home/plugins/data/mtg-rules/data/rules
cp $scripts/data-path $codex_test_skill/scripts/data-path
cp -r $repo/src $codex_test_skill/../../src
echo '{}' >$codex_test_home/plugins/data/mtg-rules/data/rules/cr.json
t "lib resolves persistent Codex plugin data" 'plugins/data/mtg-rules/data/rules$' \
    env -u MTG_RULES_DATA CODEX_HOME=$codex_test_home fish -c "$codex_test_skill/scripts/data-path --field rules"
rm -rf $codex_test_root

# --- setup-data ---
t "setup-data shows usage" '(?i)usage' fish -c "$scripts/setup-data --help; true"
t "setup-data cards tier includes MTGJSON SQLite" \
    '(?s)--cards.*AllPrintings\.sqlite' $scripts/setup-data --help
t "setup-data exposes the automatic runtime tier" \
    '(?s)--runtime.*AllPrintings\.sqlite' $scripts/setup-data --help
t_fails "setup-data rejects bogus flag" $scripts/setup-data --bogus

set -l glossary_tmp (mktemp)
cp $fixtures/glossary-envelope.json $glossary_tmp
t "glossary normalizer converts the whole-document API envelope" '^Active Player\|City’s Blessing$' fish -c \
    "$scripts/normalize-glossary $glossary_tmp; jq -r '[.[\"active player\"].term, .[\"city’s blessing\"].term] | join(\"|\")' $glossary_tmp"
rm -f $glossary_tmp

# --- automatic data bootstrap ---
set -l ensure $scripts/ensure-data
set -l ensure_hook $scripts/hooks/ensure_data.py
set -l ensure_tmp (mktemp -d)
set -l ensure_count $ensure_tmp/count
t "ensure-data installs the complete runtime and ABI marker" '(?s)^1.*READY$' fish -c \
    "env MTG_RULES_SETUP_DATA=$fixtures/fake_setup_data.py MTG_RULES_FAKE_SETUP_COUNT=$ensure_count $ensure --dest $ensure_tmp; cat $ensure_count; test -s $ensure_tmp/mtgjson/AllPrintings.sqlite; and test (cat $ensure_tmp/.mtg-rules-runtime-v2) = 2; and echo READY"
t "ensure-data fast path does not re-run setup" '^1$' fish -c \
    "env MTG_RULES_SETUP_DATA=$fixtures/fake_setup_data.py MTG_RULES_FAKE_SETUP_COUNT=$ensure_count $ensure --dest $ensure_tmp; cat $ensure_count"
t "fresh automatic runtime supports SQLite card lookup" '3 damage to any target' \
    env MTG_RULES_DATA=$ensure_tmp $scripts/card Lightning Bolt
t "fresh automatic runtime supports CR lookup" 'Fixture rule text' \
    env MTG_RULES_DATA=$ensure_tmp $scripts/rule 100.1
t "ensure-data repairs a missing runtime file" '^2$' fish -c \
    "rm $ensure_tmp/catalogs/card-names.json; env MTG_RULES_SETUP_DATA=$fixtures/fake_setup_data.py MTG_RULES_FAKE_SETUP_COUNT=$ensure_count $ensure --dest $ensure_tmp; cat $ensure_count"
rm -rf $ensure_tmp

set -l ensure_v1 (mktemp -d)
mkdir -p $ensure_v1
echo 1 >$ensure_v1/.mtg-rules-runtime-v1
set -l ensure_v1_count $ensure_v1/count
t "data ABI v1 is refreshed to normalized-glossary ABI v2" '(?s)^1.*READY$' fish -c \
    "env MTG_RULES_SETUP_DATA=$fixtures/fake_setup_data.py MTG_RULES_FAKE_SETUP_COUNT=$ensure_v1_count $ensure --dest $ensure_v1; cat $ensure_v1_count; test (cat $ensure_v1/.mtg-rules-runtime-v2) = 2; and echo READY"
rm -rf $ensure_v1

set -l ensure_concurrent (mktemp -d)
set -l concurrent_count $ensure_concurrent/count
t "ensure-data serializes concurrent first-run sessions" '^1$' bash -c \
    "env MTG_RULES_SETUP_DATA=$fixtures/fake_setup_data.py MTG_RULES_FAKE_SETUP_COUNT=$concurrent_count MTG_RULES_FAKE_SETUP_DELAY=1 python3 $ensure --dest $ensure_concurrent >/dev/null 2>&1 & env MTG_RULES_SETUP_DATA=$fixtures/fake_setup_data.py MTG_RULES_FAKE_SETUP_COUNT=$concurrent_count MTG_RULES_FAKE_SETUP_DELAY=1 python3 $ensure --dest $ensure_concurrent >/dev/null 2>&1 & wait; cat $concurrent_count"
rm -rf $ensure_concurrent

set -l ensure_stale (mktemp -d)
mkdir $ensure_stale/.mtg-rules-runtime.lock
t "ensure-data reclaims an ownerless stale lock" '^READY$' fish -c \
    "env MTG_RULES_SETUP_DATA=$fixtures/fake_setup_data.py $ensure --dest $ensure_stale; test -s $ensure_stale/.mtg-rules-runtime-v2; and echo READY"
rm -rf $ensure_stale

set -l ensure_fail (mktemp -d)
t "bootstrap hook warns but exits zero on setup failure" '(?s)non-blocking.*HOOK_OK$' fish -c \
    "printf '{}' | env PLUGIN_DATA=$ensure_fail MTG_RULES_SETUP_DATA=$fixtures/fake_setup_data.py MTG_RULES_FAKE_SETUP_FAIL=1 python3 $ensure_hook; and echo HOOK_OK"
t "agy bootstrap failure uses PreInvocation output" injectSteps fish -c \
    "printf '{\"invocationNum\":0}' | env PLUGIN_DATA=$ensure_fail MTG_RULES_SETUP_DATA=$fixtures/fake_setup_data.py MTG_RULES_FAKE_SETUP_FAIL=1 python3 $ensure_hook"
rm -rf $ensure_fail

t "Codex and Claude register SessionStart bootstrap" '^startup\|resume\|clear$' \
    jq -r '.hooks.SessionStart[0].matcher' $repo/hooks/hooks.json
t "agy registers PreInvocation bootstrap" '^command$' \
    jq -r '."mtg-rules-data".PreInvocation[0].type' $repo/hooks.json

set -l host_tmp (mktemp -d)
set -l codex_root $host_tmp/codex
set -l codex_ensure $codex_root/plugins/cache/mtg-rules/mtg-rules/1.10.0/skills/mtg-rules/scripts/ensure-data
mkdir -p (path dirname $codex_ensure)
cp $ensure $codex_ensure
cp -R $repo/src (path resolve (path dirname $codex_ensure)/../../..)/src
t "Codex path fallback provisions persistent plugin data" '^true$' fish -c \
    "env -u MTG_RULES_DATA -u PLUGIN_DATA -u CLAUDE_PLUGIN_DATA HOME=$host_tmp/home CODEX_HOME=$codex_root MTG_RULES_SETUP_DATA=$fixtures/fake_setup_data.py python3 $codex_ensure; test -s $codex_root/plugins/data/mtg-rules/data/.mtg-rules-runtime-v2; and echo true"

set -l claude_home $host_tmp/claude-home
set -l claude_ensure $claude_home/.claude/plugins/cache/mtg-rules/mtg-rules/1.10.0/skills/mtg-rules/scripts/ensure-data
mkdir -p (path dirname $claude_ensure)
cp $ensure $claude_ensure
cp -R $repo/src (path resolve (path dirname $claude_ensure)/../../..)/src
t "Claude path fallback provisions persistent plugin data" '^true$' fish -c \
    "env -u MTG_RULES_DATA -u PLUGIN_DATA -u CLAUDE_PLUGIN_DATA -u CODEX_HOME HOME=$claude_home MTG_RULES_SETUP_DATA=$fixtures/fake_setup_data.py python3 $claude_ensure; test -s $claude_home/.claude/plugins/data/mtg-rules/data/.mtg-rules-runtime-v2; and echo true"

set -l agy_home $host_tmp/agy-home
set -l agy_ensure $agy_home/.gemini/config/plugins/mtg-rules/skills/mtg-rules/scripts/ensure-data
mkdir -p (path dirname $agy_ensure)
cp $ensure $agy_ensure
cp -R $repo/src (path resolve (path dirname $agy_ensure)/../../..)/src
t "agy path fallback provisions persistent plugin data" '^true$' fish -c \
    "env -u MTG_RULES_DATA -u PLUGIN_DATA -u CLAUDE_PLUGIN_DATA -u CODEX_HOME HOME=$agy_home MTG_RULES_SETUP_DATA=$fixtures/fake_setup_data.py python3 $agy_ensure; test -s $agy_home/.gemini/config/plugins/mtg-rules/data/.mtg-rules-runtime-v2; and echo true"
rm -rf $host_tmp

# --- keyword classification ---
t "keywords-classified.json parses" '^valid$' fish -c "jq -e . skills/mtg-rules/keywords-classified.json >/dev/null; and echo valid"
t "keyword classes are all in enum" '^0$' fish -c 'jq -r "[.keywords[].class] - [\"intrinsic\",\"composite\",\"composite-given\",\"marker\"] | length" skills/mtg-rules/keywords-classified.json'
t "keyword count covers both lists" '^266$' fish -c "jq -r '.keywords | length' skills/mtg-rules/keywords-classified.json"
t "classified names exactly cover the live keyword catalogs" '^0$' fish -c \
    "set -l rules_dir ($scripts/data-path --field rules); set -l data_dir ($scripts/data-path); set -l mtgjson_dir ($scripts/data-path --field mtgjson); jq -n --slurpfile c $repo/skills/mtg-rules/keywords-classified.json --slurpfile k \$rules_dir/keywords.json '((([\$k[0].keywordAbilities[], \$k[0].keywordActions[]] - [\$c[0].keywords[].name]) + ([\$c[0].keywords[].name] - [\$k[0].keywordAbilities[], \$k[0].keywordActions[]])) | length)'"
# Lint (the Enlist-bug class): a composite-given row whose `how` never names
# its `given` primitive is exactly how a tag/rationale mismatch survives
# review. Normalized comparison: lowercase, hyphens treated as spaces.
t "lint: composite-given how names its given primitive" '^0$' \
    jq -r '[.keywords[] | select(.class=="composite-given") | (.given|ascii_downcase|gsub("-";" ")) as $g | select(((.how|ascii_downcase|gsub("-";" ")) | contains($g)) | not) | .name] | length' skills/mtg-rules/keywords-classified.json
t "lint: every given value is in meta.given_vocabulary" '^0$' \
    jq -r '([.keywords[] | select(.class=="composite-given") | .given] | unique) - (.meta.given_vocabulary | keys) | length' skills/mtg-rules/keywords-classified.json

# --- lookup/classify/health ---
t "lookup deathtouch spans rule and keyword sources" '(?s)\[rule\] 702\.2.*\[keyword\]' $scripts/lookup deathtouch
t_fails "lookup rejects invalid regex" $scripts/lookup '['
t_fails "lookup misses garbage" $scripts/lookup zzqqxyzzy
t "classify Cascade is composite" 'Cascade.*composite' $scripts/classify Cascade
t "classify Recruit is composite" 'Recruit.*composite' $scripts/classify Recruit
t "classify Storied is composite" 'Storied.*composite' $scripts/classify Storied
t_fails "classify bogus keyword" $scripts/classify zzgrok
t "cite defaults to the skill-relative config" '0 stale' $scripts/cite check
t "health reports effective date and exits 0" '(?s)effective.*HEALTH_OK' fish -c "$scripts/health; and echo HEALTH_OK"

# --- cite (fixtures copied to a tmp dir; locks are created there by bless) ---
set -l citetmp (mktemp -d)
cp -r $fixtures/cite/. $citetmp/
set -l cite $scripts/cite
set -l cdat MTG_RULES_DATA=$citetmp/data
set -l cdat2 MTG_RULES_DATA=$citetmp/data-v2
set -l cdat3 MTG_RULES_DATA=$citetmp/data-v3
set -l curlenv MTG_RULES_CITE_WIZARDS_URL=file://$citetmp/old-cr.txt

t_fails "cite check before bless demands a lock" env $cdat $cite --config $citetmp/cfg-good.json check
t "cite bless writes the lock" 'blessed 6 rules at cr_date 2026-04-17' \
    env $cdat $curlenv $cite --config $citetmp/cfg-good.json bless
t "cite lock entries are 16-hex" '"100\.1a": "[0-9a-f]{16}"' cat $citetmp/lock-good.json
t "cite lock records the wizards url" 'file://' cat $citetmp/lock-good.json
t "cite check green after bless" 'checked 6 citations against cr\.json \(eff\. 2026-04-17\); 0 stale' \
    env $cdat $cite --config $citetmp/cfg-good.json check
t "cite list expands ranges in document order (l-skip)" '704\.5k, 704\.5m, 704\.5n' \
    env $cdat $cite --config $citetmp/cfg-good.json list
t "cite list resolves leaf+section comma list" '\[CR#100\.1a,702\]  -> 100\.1a, 702' \
    env $cdat $cite --config $citetmp/cfg-good.json list
t "cite check flags MALFORMED for a bracketed-shaped token" 'MALFORMED  104\.4b-class  src/malformed\.md:1' \
    env $cdat $cite --config $citetmp/cfg-malformed.json check
t "cite check counts malformed as stale" 'checked 8 citations against cr\.json \(eff\. 2026-04-17\); 2 stale' \
    env $cdat $cite --config $citetmp/cfg-malformed.json check
t_fails "cite exits nonzero on malformed" env $cdat $cite --config $citetmp/cfg-malformed.json check
t "cite list still skips malformed tokens" '^0$' \
    fish -c "env $cdat $cite --config $citetmp/cfg-malformed.json list | grep -c xyz; true"
t "cite bless still skips malformed tokens" 'blessed 6 rules' \
    env $cdat $curlenv $cite --config $citetmp/cfg-malformed.json bless
# An ellipsis-only token is prose about the format. Asserting the count is still
# 6 (cfg-good's) proves both halves: not MALFORMED, and not counted as a cite.
t "cite check treats an ellipsis token as prose, not MALFORMED" 'checked 6 citations against cr\.json \(eff\. 2026-04-17\); 0 stale' \
    env $cdat $cite --config $citetmp/cfg-placeholder.json check
t_fails "cite show rejects an ellipsis placeholder" \
    env $cdat $cite --config $citetmp/cfg-good.json show '[CR#…]'
t "cite flags UNLOCKED for an unblessed cite" 'UNLOCKED  100\.1  src/more\.md:1' \
    env $cdat $cite --config $citetmp/cfg-unlocked.json check
t_fails "cite exits nonzero on stale" env $cdat $cite --config $citetmp/cfg-unlocked.json check
t "cite flags GONE for a vanished rule" 'GONE  999\.9z' \
    env $cdat $cite --config $citetmp/cfg-gone.json check
t "cite flags GONE for a reversed range" 'GONE  704\.5n\.\.704\.5k' \
    env $cdat $cite --config $citetmp/cfg-gone.json check
t "cite flags CHANGED on a reworded rule" 'CHANGED  702\.22a' \
    env $cdat2 $cite --config $citetmp/cfg-good.json check
t "cite checksum ignores whitespace churn" '0 stale' \
    env $cdat3 $cite --config $citetmp/cfg-good.json check
t "cite diff prints old vs new" '(?s)- Banding once was different\..*\+ Banding is a static' \
    env $cdat $cite --config $citetmp/cfg-good.json diff 702.22a
t "cite diff marks absent-in-old" '- \(absent in old version\)' \
    env $cdat $cite --config $citetmp/cfg-good.json diff 100.1a
t "cite noncompliant flags all three legacy forms" '(?s)CR 107\.3.*rule 602.*509\.1h' \
    env $cdat $cite --config $citetmp/cfg-nc.json check --list-noncompliant
t "cite noncompliant count respects exemption" '4 non-compliant' \
    env $cdat $cite --config $citetmp/cfg-nc.json check --list-noncompliant
t "cite noncompliant ignores canonical citations" '^0$' \
    fish -c "env $cdat $cite --config $citetmp/cfg-nc.json check --list-noncompliant | grep -c '702\.22a'; true"
# `\brule N` used to fire inside `--per-rule 2`, because a hyphen is a word
# boundary. The count above staying at 4 is the other half of this guard.
t "cite noncompliant ignores a --per-rule CLI flag" '^0$' \
    fish -c "env $cdat $cite --config $citetmp/cfg-nc.json check --list-noncompliant | grep -c 'per-rule'; true"
t_fails "cite noncompliant exits nonzero" env $cdat $cite --config $citetmp/cfg-nc.json check --list-noncompliant
t "cite bare-mode bless" 'blessed 2 rules' \
    env $cdat $curlenv $cite --config $citetmp/cfg-bare.json bless
t "cite bare-mode check green" '0 stale' env $cdat $cite --config $citetmp/cfg-bare.json check
t "cite bare-mode flags a missing rule" 'GONE  999\.9x' \
    env $cdat $cite --config $citetmp/cfg-bare-missing.json check
t "cite show prints wrapped rule text" 'Banding is a static ability' \
    env $cdat $cite --config $citetmp/cfg-good.json show '[CR#702.22a]'
t "cite show --plain prints number-prefixed line" '^702\.22a  Banding' \
    env $cdat $cite --config $citetmp/cfg-good.json show --plain 702.22a
t "cite show resolves a section title" 'Keyword Abilities' \
    env $cdat $cite --config $citetmp/cfg-good.json show 702
t_fails "cite show rejects a malformed citation" env $cdat $cite --config $citetmp/cfg-good.json show xyz

# --- cite context (PostToolUse hook payload) ---
t "cite context prints rule text for a cited rule" 'Banding is a static' \
    fish -c "printf 'x [CR#702.22a] y' | env $cdat $cite --config $citetmp/cfg-good.json context"
t "cite context is silent when nothing is cited" '^$' \
    fish -c "printf 'no citations here' | env $cdat $cite --config $citetmp/cfg-good.json context"
t "cite context expands a range" '(?s)704\.5k.*704\.5m.*704\.5n' \
    fish -c "printf 'r [CR#704.5k..704.5n]' | env $cdat $cite --config $citetmp/cfg-good.json context"
t "cite context marks a rule absent from the lockfile" 'new to this repo' \
    fish -c "printf 'x [CR#100.1]' | env $cdat $cite --config $citetmp/cfg-good.json context"
t "cite context flags a citation the CR does not have" 'NOT FOUND IN THE CR' \
    fish -c "printf 'x [CR#999.9]' | env $cdat $cite --config $citetmp/cfg-good.json context"
t "cite context ignores an ellipsis placeholder" '^$' \
    fish -c "printf 'prose about [CR#…] tokens' | env $cdat $cite --config $citetmp/cfg-good.json context"
# An EMPTY ledger used to make NR == FNR true for the batch file too, so every
# rule was read as already-seen and the hook reported nothing on first use.
t "cite context reports through an empty ledger" '702\.22a' \
    fish -c "set -l s (mktemp); printf 'x [CR#702.22a]' | env $cdat $cite --config $citetmp/cfg-good.json context --seen \$s; rm -f \$s"
t "cite context shows a rule once per ledger" '^$' \
    fish -c "set -l s (mktemp); printf 'x [CR#702.22a]' | env $cdat $cite --config $citetmp/cfg-good.json context --seen \$s >/dev/null; printf 'x [CR#702.22a]' | env $cdat $cite --config $citetmp/cfg-good.json context --seen \$s; rm -f \$s"
t "cite context ledger records what it reported" '^702\.22a$' \
    fish -c "set -l s (mktemp); printf 'x [CR#702.22a]' | env $cdat $cite --config $citetmp/cfg-good.json context --seen \$s >/dev/null; cat \$s; rm -f \$s"
# One `cite list` surfaces every citation in the repo — uncapped that is ~53k
# tokens from a single tool call. The cap is announced, never silent.
t "cite context caps how many rules it reports" '… 2 more first-seen citations not shown' \
    fish -c "printf 'a [CR#100.1a] b [CR#702.22a] c [CR#704.5k]' | env $cdat $cite --config $citetmp/cfg-good.json context --max 1"
t "cite context --max 0 lifts the cap" '(?s)100\.1a.*702\.22a.*704\.5k' \
    fish -c "printf 'a [CR#100.1a] b [CR#702.22a] c [CR#704.5k]' | env $cdat $cite --config $citetmp/cfg-good.json context --max 0"
t "cite context ledgers only the rules it showed" '^100\.1a$' \
    fish -c "set -l s (mktemp); printf 'a [CR#100.1a] b [CR#702.22a]' | env $cdat $cite --config $citetmp/cfg-good.json context --seen \$s --max 1 >/dev/null; cat \$s; rm -f \$s"
t_fails "cite context rejects a non-numeric --max" \
    fish -c "printf 'x [CR#100.1a]' | env $cdat $cite --config $citetmp/cfg-good.json context --max abc"

# --- cite_context.py PostToolUse hook ---
set -g hook $scripts/hooks/cite_context.py
set -g hookdata $citetmp/data
set -g hookenv
set -g hookclean -u CITE_ON_READ -u CITE_ON_BASH -u CITE_CONTEXT_FULL -u CITE_CONTEXT_MAX -u CITE_CONTEXT_OFF
set -g hookrepo (mktemp -d) # consumer repo: cite-config.json beside a VCS marker
mkdir -p $hookrepo/.git
echo '{"format":"bracketed","lockfile":"lock.json","sources":{"globs":["*.md"]}}' >$hookrepo/cite-config.json
set -g nomarker (mktemp -d) # config, but no VCS root
echo '{"format":"bracketed","lockfile":"lock.json","sources":{"globs":["*.md"]}}' >$nomarker/cite-config.json
set -g noconfig (mktemp -d) # VCS root, but no config
mkdir -p $noconfig/.git

# Hook switches are isolated from the caller environment; the hook now uses Python.
function hookrun --argument-names cwd sid tool text
    jq -nc --arg c $cwd --arg s $sid --arg t $tool --arg v $text '
        {session_id: $s, cwd: $c, tool_name: $t}
        + (if $t == "Edit" then {tool_input: {new_string: $v}}
           elif $t == "Write" then {tool_input: {content: $v}}
           else {tool_response: $v} end)' \
        | env $hookclean MTG_RULES_DATA=$hookdata TMPDIR=$hookrepo $hookenv python3 $hook
end

# Bash payloads carry the command too, so the skill-call exemption can see it.
function hookbash --argument-names cwd sid command stdout
    jq -nc --arg c $cwd --arg s $sid --arg cmd $command --arg v $stdout \
        '{session_id: $s, cwd: $c, tool_name: "Bash",
          tool_input: {command: $cmd}, tool_response: {stdout: $v}}' \
        | env $hookclean MTG_RULES_DATA=$hookdata TMPDIR=$hookrepo $hookenv python3 $hook
end

t "hook annotates an Edit in a consumer repo" 'Banding is a static' \
    hookrun $hookrepo e1 Edit '[CR#702.22a]'
t "hook emits PostToolUse additionalContext" '^PostToolUse$' \
    fish -c "jq -nc --arg c $hookrepo '{session_id:\"e2\",cwd:\$c,tool_name:\"Edit\",tool_input:{new_string:\"[CR#702.22a]\"}}' | env $hookclean MTG_RULES_DATA=$hookdata TMPDIR=$hookrepo python3 $hook | jq -r .hookSpecificOutput.hookEventName"
t "hook annotates a Write" 'Banding is a static' \
    hookrun $hookrepo e3 Write '[CR#702.22a]'
t "hook is silent on an edit with no citations" '^$' \
    hookrun $hookrepo e4 Edit 'fn main() { let x = 1; }'
t "hook is silent on Read without CITE_ON_READ" '^$' \
    hookrun $hookrepo e5 Read '[CR#702.22a]'
t "hook is silent on Bash without CITE_ON_BASH" '^$' \
    hookrun $hookrepo e6 Bash '[CR#702.22a]'
set -g hookenv CITE_ON_READ=1
t "hook annotates Read under CITE_ON_READ" 'Banding is a static' \
    hookrun $hookrepo e7 Read '[CR#702.22a]'
set -g hookenv CITE_ON_BASH=1
t "hook annotates Bash under CITE_ON_BASH" 'Banding is a static' \
    hookrun $hookrepo e8 Bash '[CR#702.22a]'
set -g hookenv CITE_CONTEXT_OFF=1
t "hook is silent under CITE_CONTEXT_OFF" '^$' \
    hookrun $hookrepo e9 Edit '[CR#702.22a]'
set -g hookenv
t "hook is silent where cite-config.json is not at a VCS root" '^$' \
    hookrun $nomarker e10 Edit '[CR#702.22a]'
t "hook is silent in a repo with no cite-config.json" '^$' \
    hookrun $noconfig e11 Edit '[CR#702.22a]'
t "hook is silent in the skill's own development repo" '^$' \
    hookrun $repo e12 Edit '[CR#702.22a]'
t "hook shows a rule once per session id" '^$' \
    fish -c "jq -nc --arg c $hookrepo '{session_id:\"e13\",cwd:\$c,tool_name:\"Edit\",tool_input:{new_string:\"[CR#702.22a]\"}}' | env $hookclean MTG_RULES_DATA=$hookdata TMPDIR=$hookrepo python3 $hook >/dev/null; jq -nc --arg c $hookrepo '{session_id:\"e13\",cwd:\$c,tool_name:\"Edit\",tool_input:{new_string:\"[CR#702.22a]\"}}' | env $hookclean MTG_RULES_DATA=$hookdata TMPDIR=$hookrepo python3 $hook"
set -g hookenv CITE_ON_BASH=1
# Calls into this skill already print rule text; re-expanding it duplicates
# the output, and `cite list` alone would inject ~53k tokens.
t "hook exempts a path invocation of a skill script" '^$' \
    hookbash $hookrepo x1 'skills/mtg-rules/scripts/cite list' '[CR#702.22a] -> 702.22a'
t "hook exempts a plugin-cache invocation" '^$' \
    hookbash $hookrepo x2 '~/.claude/plugins/cache/mtg-rules/scripts/rule 702.22a' '[CR#702.22a]'
t "hook exempts a bare skill-script invocation" '^$' \
    hookbash $hookrepo x3 'cite show 702.22a' '[CR#702.22a]'
t "hook exempts a skill call after a pipe" '^$' \
    hookbash $hookrepo x4 'cat foo | rule 702.22a' '[CR#702.22a]'
t "hook still annotates unrelated Bash output" 'Banding is a static' \
    hookbash $hookrepo x5 'cargo test --workspace' 'panicked: [CR#702.22a] violated'
t "hook does not exempt a merely similar command" 'Banding is a static' \
    hookbash $hookrepo x6 'cargo build --features rules' 'note [CR#702.22a]'
t "hook exempts a bare ref invocation" '^$' \
    hookbash $hookrepo x7 'ref --cites 603.7e' '[CR#702.22a]'
t "hook does not exempt ref as a later word" 'Banding is a static' \
    hookbash $hookrepo x8 'git show ref' 'note [CR#702.22a]'
set -g hookenv
# The exempt list is hand-maintained; this fails if a script is added to
# scripts/ without being added to the hook's alternation. Whole alternatives
# only: a bare substring test is satisfied by any word containing the name
# ("ref" sits inside "references").
t "hook exempt list covers every skill script" '^$' fish -c "
    for s in (ls $scripts | grep -v '^lib.fish\$' | grep -v '^cite-lib\$' | grep -v '^hooks\$')
        grep -qE \"[(|]\"\$s\"[|)]\" $repo/src/mtg_rules/cite_hook.py; or echo \"missing: \$s\"
    end"
set -g hookenv CITE_CONTEXT_MAX=1
t "hook honors CITE_CONTEXT_MAX" 'not shown' \
    hookrun $hookrepo e14 Edit '[CR#100.1a] [CR#702.22a] [CR#704.5k]'
set -g hookenv
# Linux caps a SINGLE argv entry at 128 KB, so the payload can never ride in
# argv: `cite list` output (~700 KB) silently produced nothing until every
# stage moved to files.
set -g bigfile (mktemp)
for i in (seq 4000)
    echo "line $i filler text padding this well past the argv limit [CR#702.22a] tail"
end >$bigfile
t "hook handles a payload past the single-argument limit" 'Banding is a static' \
    fish -c "jq -nc --arg c $hookrepo --rawfile v $bigfile '{session_id:\"e15\",cwd:\$c,tool_name:\"Edit\",tool_input:{new_string:\$v}}' | env $hookclean MTG_RULES_DATA=$hookdata TMPDIR=$hookrepo python3 $hook"
rm -f $bigfile
t "hook survives malformed stdin" '^$' \
    fish -c "printf 'not json' | env $hookclean MTG_RULES_DATA=$hookdata TMPDIR=$hookrepo python3 $hook; true"
t "plugin hooks.json registers the PostToolUse matcher" '^Write\|Edit\|Read\|Bash$' \
    jq -r '.hooks.PostToolUse[0].matcher' $repo/hooks/hooks.json
t "plugin hooks.json points at the hook script" '^true$' fish -c \
    "test -x $repo/(jq -r '.hooks.PostToolUse[0].hooks[0].command' $repo/hooks/hooks.json | string replace -r '.*PLUGIN_ROOT\}\}?/' '' | string trim -c '\"'); and echo true"
rm -rf $hookrepo $nomarker $noconfig
rm -rf $citetmp

# --- version (conformance manifest) ---
t "version emits the plugin version" '"plugin_version": "1\.11\.0"' $scripts/version
t "version manifest parses with all four keys" '^true$' \
    fish -c "$scripts/version | jq -e 'has(\"plugin_version\") and has(\"git_commit\") and has(\"cr_effective\") and has(\"keywords_classified_sha\")'"

# --- keyword idents (machine enum spellings) ---
t "idents: all 266 records carry a string ident" '^266$' \
    jq -r '[.keywords[].ident | select(type == "string")] | length' $repo/skills/mtg-rules/keywords-classified.json
t "idents: all 266 unique" '^266$' \
    jq -r '[.keywords[].ident] | unique | length' $repo/skills/mtg-rules/keywords-classified.json
t "idents: all match ^[A-Z][A-Za-z0-9]*\$" '^0$' \
    jq -r '[.keywords[].ident | select(test("^[A-Z][A-Za-z0-9]*$") | not)] | length' $repo/skills/mtg-rules/keywords-classified.json
t "ident spot checks (First Strike, For Mirrodin!, ∞)" '^FirstStrike ForMirrodin Infinity$' \
    jq -r '[.keywords[] | select(.name == "First Strike" or .name == "For Mirrodin!" or .name == "∞ (Infinity)") | .ident] | join(" ")' $repo/skills/mtg-rules/keywords-classified.json
t "classify prints the ident" 'ident: FirstStrike' $scripts/classify first strike

# --- underdetermined (durable UD ids) ---
t "underdetermined lists entry lines with categories" 'UD-7 — Concession granularity — category: open' $scripts/underdetermined
t "underdetermined prints an entry by id" '(?s)UD-12.*Intra-batch.*704\.3' $scripts/underdetermined UD-12
t "underdetermined resolves a bare number" 'Concession granularity' $scripts/underdetermined 7
t "underdetermined retired ids still resolve" '(?s)U3.*settled-by-policy' $scripts/underdetermined U3
t_fails "underdetermined bogus id" $scripts/underdetermined UD-999
t_fails "underdetermined garbage arg" $scripts/underdetermined xyz

# --- health reference-doc summary and keyword warning ---
t "health summarizes reference-doc sync on one line" \
    'reference docs: \d+/\d+ synthesized from CR \d{4}-\d{2}-\d{2} \(live \d{4}-\d{2}-\d{2}\); verify map claims against the cited rules' \
    fish -c "$scripts/health; true"
t "health no longer prints per-doc warn lines" '^0$' \
    fish -c "$scripts/health | grep -c 'no synthesis-date header\|re-sync'; true"

# A throwaway skill tree around the real data: health's skill_dir is its own
# location, so a copy of the scripts reads the fixture references and
# keywords-classified.json instead of the real ones.
set -l real_data (fish -c "set -l rules_dir ($scripts/data-path --field rules); set -l data_dir ($scripts/data-path); set -l mtgjson_dir ($scripts/data-path --field mtgjson); echo \$data_dir")
set -l live_iso (fish -c "set -l rules_dir ($scripts/data-path --field rules); set -l data_dir ($scripts/data-path); set -l mtgjson_dir ($scripts/data-path --field mtgjson); $scripts/data-path --field effective")
set -l htree (mktemp -d)
set -l hskill $htree/skills/mtg-rules
mkdir -p $hskill/scripts $hskill/references
cp $scripts/health $scripts/cite $hskill/scripts/
cp -r $repo/src $htree/
echo '{"format":"bare","lockfile":"cr-citations.lock","sources":{"globs":["references/*.md"]}}' >$hskill/cite-config.json
printf '# A\n\n*Synthesized from the Comprehensive Rules effective %s.*\n' $live_iso >$hskill/references/a.md
printf '# B\n\n*Synthesized from the Comprehensive Rules effective 2020-01-01.*\n' >$hskill/references/b.md
printf '# C\n\nNo header date here.\n' >$hskill/references/c.md
# the 702.2 (Deathtouch) row removed; every other keyword stays classified
jq '.keywords |= map(select(.rule != "702.2"))' $repo/skills/mtg-rules/keywords-classified.json >$hskill/keywords-classified.json
t "health counts docs in sync with the live CR" \
    "reference docs: 1/3 synthesized from CR $live_iso \\(live $live_iso\\); verify map claims" \
    fish -c "env MTG_RULES_DATA=$real_data $hskill/scripts/health; true"
t "health names lagging and undated docs compactly" \
    'lagging or undated \(warning only\): b\.md \(2020-01-01\), c\.md \(no date\)' \
    fish -c "env MTG_RULES_DATA=$real_data $hskill/scripts/health; true"
t "health warns about a keyword heading with no classified row" \
    'warn: 1 CR keyword heading\(s\) with no row in keywords-classified\.json: 702\.2 Deathtouch' \
    fish -c "env MTG_RULES_DATA=$real_data $hskill/scripts/health; true"
rm -rf $htree

# Every 701.N keyword action and 702.N keyword ability heading (x.1 is the
# section introduction) has a keywords-classified row. Empty output = pass; a
# failure prints the unclassified headings.
function unclassified_keywords --argument-names rules_dir
    jq -r --slurpfile kc $repo/skills/mtg-rules/keywords-classified.json '
        ($kc[0].keywords | map(.rule)) as $have
        | to_entries[]
        | select((.key | test("^70[12][.][0-9]+$")) and (.key | test("^70[12][.]1$") | not))
        | select(.key | IN($have[]) | not)
        | .key + " " + .value.ruleText' $rules_dir/cr.json
end
t "every 701/702 keyword section has a keywords-classified row" '^$' \
    unclassified_keywords (path dirname $real_data/rules/cr.json)

# --- define prints the first referenced rule ---
t "define prints the rule a glossary entry points at" '(?s)See rule 700\.4\..*\n→ 700\.4\. The term dies means' $scripts/define dies
t "define follows the first of several referenced rules" '(?s)See rules 613\.2, 707\.2.*\n→ 613\.2\. Within layer 1' $scripts/define copiable values
t "define points at rule for the rest of a long rule" '\(scripts/rule 613\.2 for the rest\)' $scripts/define copiable values
t "define clips a very long rule" '→ 120\.4a .*…\n  \(scripts/rule 120\.4a for the rest\)' $scripts/define lethal damage
t "define skips a bare section reference" '^0$' \
    fish -c "$scripts/define 'basic land type' | grep -c '→'; true"
t "define adds no rule line to an unofficial entry" '^0$' \
    fish -c "$scripts/define battalion | grep -c '→'; true"

# --- ref (section reader for the reference docs) ---
# Fixture skill tree: ref resolves references/ from its own location and reads
# `cite list` from the sibling cite, so a copy sees only the fixture docs. Rule
# data still comes from the real CR, which the range expansion needs.
set -l rtree (mktemp -d)
set -l rskill $rtree/skills/mtg-rules
mkdir -p $rskill/scripts $rskill/references
cp $scripts/ref $scripts/cite $rskill/scripts/
cp -r $repo/src $rtree/
echo '{"format":"bare","lockfile":"cr-citations.lock","sources":{"globs":["references/*.md"]}}' >$rskill/cite-config.json
printf '%s\n' \
    '# Fixture — Cites' '' \
    '*Synthesized from the Comprehensive Rules effective 2026-01-01.*' '' \
    '## 1. Delayed triggers' '' \
    'Source and controller per 603.7d–h.' \
    'Duration is 603.7a.' '' \
    '## 2. Costs (118)' '' \
    'Plain text about priority 117.1 and costs.' '' \
    '### 2.1 Nested' '' \
    'Cites 510.1c-d here. Whenever a thing happens.' '' \
    '```' '## 3. Not a heading' '```' '' \
    '## 4. Tail' '' \
    'Final words with no citations.' >$rskill/references/fixture.md
printf '%s\n' '# Fixture — No Date' '' 'Text without a synthesis header.' '' '## 1. Only section' '' 'Body.' >$rskill/references/nodate.md
set -g rref env MTG_RULES_DATA=$real_data $rskill/scripts/ref

t "ref lists docs with title and synthesis date" 'fixture +Fixture — Cites +\[2026-01-01\]' $rref
t "ref lists docs without a date too" 'nodate +Fixture — No Date +\[no date\]' $rref
t "ref lists a doc's sections with sizes (unique prefix resolves)" \
    '(?s)§1\. Delayed triggers \(\d+ lines\).*§2\. Costs \(118\).*§2\.1 Nested' $rref fix
t "ref section list ignores headings inside code fences" '^0$' \
    fish -c "env MTG_RULES_DATA=$real_data $rskill/scripts/ref fixture | grep -c 'Not a heading'; true"
t "ref prints a section under a map banner" \
    '(?s)^\[map\] fixture §2\. Costs \(118\) .*synthesized from CR 2026-01-01\. A map, not a source: cite the CR rules.*\n## 2\. Costs \(118\)\n.*Plain text about priority' \
    $rref fixture 2
t "ref section stops at the next peer heading" '^0$' \
    fish -c "env MTG_RULES_DATA=$real_data $rskill/scripts/ref fixture 2 | grep -c 'Final words'; true"
t "ref section includes its nested subsection text" 'Whenever a thing happens' $rref fixture 2
t "ref resolves a section by dotted number" '(?s)^\[map\] fixture §2\.1 Nested.*Whenever a thing' $rref fixture 2.1
t "ref resolves a section by heading text, case-insensitively" 'Plain text about priority' $rref fixture COSTS
t "ref accepts the listing's own section label" 'Plain text about priority' $rref fixture '§2. Costs (118)'
t "ref banner tolerates a doc without a date" '(?s)^\[map\] nodate §1\. Only section .*no synthesis date\. A map, not a source: cite the CR rules.*\nBody\.' $rref nodate 1
t_fails "ref rejects an unknown doc" $rref nosuchdoc
t_fails "ref rejects an unknown section" $rref fixture 99
t_fails "ref rejects unknown heading text" $rref fixture zzqqxyzzy
t_fails "ref rejects an unknown option" $rref --bogus
t "ref unknown doc prints usage" '(?s)usage: ref.*--cites' fish -c "env MTG_RULES_DATA=$real_data $rskill/scripts/ref nosuchdoc 2>&1; true"
t "ref --cites finds a section whose prose range covers the rule (603.7d–h ∋ 603.7e)" \
    '\[map\] fixture §1\. Delayed triggers \(1 line\)' $rref --cites 603.7e
t "ref --cites on a rule counts its lettered subrules" '\[map\] fixture §1\. Delayed triggers \(2 lines\)' $rref --cites 603.7
t "ref --cites reads an ASCII-hyphen range (510.1c-d ∋ 510.1d)" '\[map\] fixture §2\.1 Nested \(1 line\)' $rref --cites 510.1d
t "ref --cites reports the enclosing subsection, not only the peer section" '^0$' \
    fish -c "env MTG_RULES_DATA=$real_data $rskill/scripts/ref --cites 510.1d | grep -c 'fixture §2\\. '; true"
t_fails "ref --cites misses a rule outside the range (603.7c)" $rref --cites 603.7c
t_fails "ref --cites rejects a non-rule argument" $rref --cites abc
t "ref --grep is case-insensitive" '\[map\] fixture §2\.1 Nested \(1 line\)' $rref --grep WHENEVER
t "ref --grep keeps the pattern as written (\\D is not lowercased to \\d)" \
    '\[map\] fixture §2\. Costs \(118\) \(1 line\)' $rref --grep 'about \D+ 117'
t_fails "ref --grep rejects an invalid regex" $rref --grep '['
t_fails "ref --grep misses garbage" $rref --grep zzqqxyzzy

# lookup [map] tier and rule footer, against the same fixture tree.
cp $scripts/lookup $scripts/rule $rskill/scripts/
printf '%s\n' '# Fixture — Many' '' '*Synthesized from the Comprehensive Rules effective 2026-01-01.*' '' \
    '## 1. Alpha' 'qzvmarker here' 'qzvmarker again' '## 2. Beta' 'qzvmarker' '## 3. Gamma' 'qzvmarker' \
    '## 4. Delta' 'qzvmarker' '## 5. Eps' 'qzvmarker' '## 6. Zeta' 'qzvmarker' '## 7. Eta' 'qzvmarker' >$rskill/references/many.md
set -g rlook env MTG_RULES_DATA=$real_data $rskill/scripts/lookup
set -g rrule env MTG_RULES_DATA=$real_data $rskill/scripts/rule
t "lookup [map] tier finds a body hit with a drill-down command" \
    '\[map\] fixture §2\. Costs \(118\)  \(ref fixture .2.\)' $rlook 'about priority'
t "lookup [map] prints one line per section" '^1$' \
    fish -c "env MTG_RULES_DATA=$real_data $rskill/scripts/lookup 'qzvmarker' | grep -c '§1\\. Alpha'"
t "lookup [map] caps at 6 lines and names ref --grep for the rest" \
    "\\[map\\] \\(\\+1 more — ref --grep 'qzvmarker'\\)" $rlook qzvmarker
t "lookup [map] shows exactly 6 section lines when capped" '^7$' \
    fish -c "env MTG_RULES_DATA=$real_data $rskill/scripts/lookup 'qzvmarker' | grep -c '^\\[map\\]'"
t "rule footer names the map sections citing the rule" \
    '\nmaps: fixture §1 \(ref <doc> <n> to read\)' $rrule 603.7e
t "rule footer is silent when no map cites the rule" '^0$' \
    fish -c "env MTG_RULES_DATA=$real_data $rskill/scripts/rule 104.3a | grep -c '^maps:'; true"
t "rule footer is skipped for a whole section" '^0$' \
    fish -c "env MTG_RULES_DATA=$real_data $rskill/scripts/rule 603 | grep -c '^maps:'; true"
rm -rf $rtree

# Real docs: every references/*.md lists sections and prints its first one.
function ref_every_doc
    for f in $repo/skills/mtg-rules/references/*.md
        set -l d (path basename -E $f)
        set -l secs ($scripts/ref $d 2>/dev/null | string match -rg '^ +§(.+) \(\d+ lines\)$')
        test (count $secs) -gt 0; or begin; echo "no sections: $d"; continue; end
        set -l out ($scripts/ref $d "$secs[1]" 2>/dev/null | string collect)
        string match -rq "^\[map\] $d §" -- "$out"; or echo "no banner: $d"
    end
end
t "ref works on every reference doc" '^$' ref_every_doc
t "ref reads a numbered subsection of oracle-style" '(?s)^\[map\] oracle-style §12\. .*\n#+ 12\. ' $scripts/ref oracle-style 12
t "ref --cites works on the real reference docs" '\[map\] \S+ §' $scripts/ref --cites 603.7e
t "ref --grep works on the real reference docs" '\[map\] \S+ §' $scripts/ref --grep 'delayed trigger'

# (tests appended by later tasks above this line)

echo
echo "$passes passed, $fails failed"
test $fails -eq 0
