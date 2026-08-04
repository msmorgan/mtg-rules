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
t "Codex marketplace installs the repository root" '^url \./$' \
    jq -r '.plugins[0].source | [.source, .url] | join(" ")' $repo/.agents/plugins/marketplace.json
t "Codex marketplace has a collision-free development name" '^mtg-rules-dev$' \
    jq -r '.name' $repo/.agents/plugins/marketplace.json
t "Codex and Claude manifests have the same version" '^true$' fish -c \
    "test (jq -r .version $repo/.codex-plugin/plugin.json) = (jq -r .version $repo/.claude-plugin/plugin.json); and echo true"

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

# --- rulings ---
t "rulings humility has dated entries" '\[\d{4}-\d{2}-\d{2}\]' $scripts/rulings Humility
t "rulings face name resolves to full card" 'Fire // Ice' $scripts/rulings Fire
t "rulings case-insensitive" '\[\d{4}' $scripts/rulings humility
t_fails "rulings bogus card" $scripts/rulings Zzgrokk the Unreal
t_fails "rulings empty arg" $scripts/rulings ''

# --- data resolution chain ---
mkdir -p /tmp/mtg-data-test/rules; echo '{}' > /tmp/mtg-data-test/rules/cr.json
t "lib honors MTG_RULES_DATA" '/tmp/mtg-data-test/rules$' fish -c "set -x MTG_RULES_DATA /tmp/mtg-data-test; source $scripts/lib.fish; or exit 1; echo \$rules_dir"
t "lib ignores invalid MTG_RULES_DATA" 'data/rules$' fish -c "set -x MTG_RULES_DATA /nonexistent; source $scripts/lib.fish; or exit 1; echo \$rules_dir"
rm -rf /tmp/mtg-data-test

set -l codex_test_root (mktemp -d)
set -l codex_test_home $codex_test_root/home
set -l codex_test_skill $codex_test_home/plugins/cache/mtg-rules/mtg-rules/1.8.3/skills/mtg-rules
mkdir -p $codex_test_skill/scripts $codex_test_home/plugins/data/mtg-rules/data/rules
cp $scripts/lib.fish $codex_test_skill/scripts/lib.fish
echo '{}' >$codex_test_home/plugins/data/mtg-rules/data/rules/cr.json
t "lib resolves persistent Codex plugin data" 'plugins/data/mtg-rules/data/rules$' \
    env CODEX_HOME=$codex_test_home fish -c "source $codex_test_skill/scripts/lib.fish; or exit 1; echo \$rules_dir"
rm -rf $codex_test_root

# --- setup-data ---
t "setup-data shows usage" '(?i)usage' fish -c "$scripts/setup-data --help; true"
t_fails "setup-data rejects bogus flag" $scripts/setup-data --bogus

# --- keyword classification ---
t "keywords-classified.json parses" '^valid$' fish -c "jq -e . skills/mtg-rules/keywords-classified.json >/dev/null; and echo valid"
t "keyword classes are all in enum" '^0$' fish -c 'jq -r "[.keywords[].class] - [\"intrinsic\",\"composite\",\"composite-given\",\"marker\"] | length" skills/mtg-rules/keywords-classified.json'
t "keyword count covers both lists" '^263$' fish -c "jq -r '.keywords | length' skills/mtg-rules/keywords-classified.json"
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

# --- cite_context.fish PostToolUse hook ---
set -g hook $scripts/hooks/cite_context.fish
set -g hookdata $citetmp/data
set -g hookenv
set -g hookrepo (mktemp -d)      # consumer repo: cite-config.json beside a VCS marker
mkdir -p $hookrepo/.git
echo '{"format":"bracketed","lockfile":"lock.json","sources":{"globs":["*.md"]}}' > $hookrepo/cite-config.json
set -g nomarker (mktemp -d)      # config, but no VCS root
echo '{"format":"bracketed","lockfile":"lock.json","sources":{"globs":["*.md"]}}' > $nomarker/cite-config.json
set -g noconfig (mktemp -d)      # VCS root, but no config
mkdir -p $noconfig/.git

function hookrun --argument-names cwd sid tool text
    jq -nc --arg c $cwd --arg s $sid --arg t $tool --arg v $text '
        {session_id: $s, cwd: $c, tool_name: $t}
        + (if $t == "Edit" then {tool_input: {new_string: $v}}
           elif $t == "Write" then {tool_input: {content: $v}}
           else {tool_response: $v} end)' \
        | env MTG_RULES_DATA=$hookdata TMPDIR=$hookrepo $hookenv fish $hook
end

t "hook annotates an Edit in a consumer repo" 'Banding is a static' \
    hookrun $hookrepo e1 Edit '[CR#702.22a]'
t "hook emits PostToolUse additionalContext" '^PostToolUse$' \
    fish -c "jq -nc --arg c $hookrepo '{session_id:\"e2\",cwd:\$c,tool_name:\"Edit\",tool_input:{new_string:\"[CR#702.22a]\"}}' | env MTG_RULES_DATA=$hookdata TMPDIR=$hookrepo fish $hook | jq -r .hookSpecificOutput.hookEventName"
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
    fish -c "jq -nc --arg c $hookrepo '{session_id:\"e13\",cwd:\$c,tool_name:\"Edit\",tool_input:{new_string:\"[CR#702.22a]\"}}' | env MTG_RULES_DATA=$hookdata TMPDIR=$hookrepo fish $hook >/dev/null; jq -nc --arg c $hookrepo '{session_id:\"e13\",cwd:\$c,tool_name:\"Edit\",tool_input:{new_string:\"[CR#702.22a]\"}}' | env MTG_RULES_DATA=$hookdata TMPDIR=$hookrepo fish $hook"
t "hook survives malformed stdin" '^$' \
    fish -c "printf 'not json' | env MTG_RULES_DATA=$hookdata TMPDIR=$hookrepo fish $hook; true"
t "plugin hooks.json registers the PostToolUse matcher" '^Write\|Edit\|Read\|Bash$' \
    jq -r '.hooks.PostToolUse[0].matcher' $repo/hooks/hooks.json
t "plugin hooks.json points at the hook script" '^true$' fish -c \
    "test -x $repo/(jq -r '.hooks.PostToolUse[0].hooks[0].command' $repo/hooks/hooks.json | string replace -r '.*PLUGIN_ROOT\}\}?/' '' | string trim -c '\"'); and echo true"
rm -rf $hookrepo $nomarker $noconfig
rm -rf $citetmp

# --- version (conformance manifest) ---
t "version emits the plugin version" '"plugin_version": "1\.8\.3"' $scripts/version
t "version manifest parses with all four keys" '^true$' \
    fish -c "$scripts/version | jq -e 'has(\"plugin_version\") and has(\"git_commit\") and has(\"cr_effective\") and has(\"keywords_classified_sha\")'"

# --- keyword idents (machine enum spellings) ---
t "idents: all 263 records carry a string ident" '^263$' \
    jq -r '[.keywords[].ident | select(type == "string")] | length' $repo/skills/mtg-rules/keywords-classified.json
t "idents: all 263 unique" '^263$' \
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

# --- health per-doc staleness summary ---
t "health reports reference-doc sync state" 'reference docs: \d+' fish -c "$scripts/health; true"

# (tests appended by later tasks above this line)

echo
echo "$passes passed, $fails failed"
test $fails -eq 0
