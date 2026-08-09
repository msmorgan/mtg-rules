# Shared setup for mtg-rules skill scripts. Source, don't execute.
# Resolves real paths so scripts work through personal-skill symlinks.

set -l here (path resolve (status dirname))
set -g skill_dir (path dirname $here)
set -g plugin_root (path dirname (path dirname $skill_dir))
set -g plugin_manifest ""
for _manifest_candidate in \
    $plugin_root/.codex-plugin/plugin.json \
    $plugin_root/.claude-plugin/plugin.json \
    $skill_dir/.claude-plugin/plugin.json
    if test -r $_manifest_candidate
        set plugin_manifest $_manifest_candidate
        break
    end
end

# Data resolution chain — each candidate accepted iff <dir>/rules/cr.json is readable:
#   1. $MTG_RULES_DATA (if set)
#   2. the host-provided persistent plugin data directory
#   3. the current host's conventional persistent plugin data directory
#   4. plugin/repo-relative data (plugin/skills/mtg-rules -> plugin/data)
#   5. the other supported hosts' persistent plugin data directories
set -g data_dir ""
set -l _candidates

set -l _codex_root "$HOME/.codex"
if set -q CODEX_HOME; and test -n "$CODEX_HOME"
    set _codex_root (path normalize "$CODEX_HOME")
end
set -l _codex_data "$_codex_root/plugins/data/mtg-rules/data"
set -l _gemini_data "$HOME/.gemini/config/plugins/mtg-rules/data"
set -l _claude_data "$HOME/.claude/plugins/data/mtg-rules/data"

if set -q MTG_RULES_DATA
    set -a _candidates "$MTG_RULES_DATA"
end

# Codex exposes PLUGIN_DATA; Claude Code exposes CLAUDE_PLUGIN_DATA. Prefer
# either host-owned persistent location over paths inferred from an installed
# cache layout, while keeping MTG_RULES_DATA as the explicit user override.
for _data_var in PLUGIN_DATA CLAUDE_PLUGIN_DATA
    if set -q $_data_var; and test -n "$$_data_var"
        set -l _host_data $$_data_var
        if not contains -- "$_host_data" $_candidates
            set -a _candidates "$_host_data"
        end
    end
end

# Prefer the persistent data directory belonging to the host that installed
# this copy. This avoids choosing another agent's stale data when several
# clients are installed on the same machine.
if string match -q -- "$_codex_root/*" "$skill_dir"
    set -a _candidates "$_codex_data"
else if string match -q -- "$HOME/.gemini/*" "$skill_dir"
    set -a _candidates "$_gemini_data"
else if string match -q -- "$HOME/.claude/*" "$skill_dir"
    set -a _candidates "$_claude_data"
end

set -l _plugin_data (path dirname (path dirname $skill_dir))/data
set -l _legacy_data (path dirname $skill_dir)/data
for _cand in \
    $_plugin_data \
    $_legacy_data \
    $_codex_data \
    $_gemini_data \
    $_claude_data
    if not contains -- "$_cand" $_candidates
        set -a _candidates "$_cand"
    end
end

for _cand in $_candidates
    if test -r $_cand/rules/cr.json
        set data_dir $_cand
        break
    else if set -q MTG_RULES_DATA; and test "$_cand" = "$MTG_RULES_DATA"
        echo >&2 "mtg-rules: warning: MTG_RULES_DATA is set but $_cand/rules/cr.json is unreadable — trying other locations"
    end
end

if test -z "$data_dir"
    echo >&2 "mtg-rules: could not find data directory. Tried:"
    if not set -q MTG_RULES_DATA
        echo >&2 "  \$MTG_RULES_DATA is not set"
    end
    set -l _candidate_number 1
    for _cand in $_candidates
        echo >&2 "  $_candidate_number. $_cand"
        set _candidate_number (math $_candidate_number + 1)
    end
    echo >&2 "Populate plugin data with: $skill_dir/scripts/setup-data --runtime [--cards]"
    echo >&2 "For a repo checkout, you may instead run: scripts/fetch_data.fish"
    exit 1
end

set -g rules_dir $data_dir/rules
set -g catalogs_dir $data_dir/catalogs
set -g mtgjson_dir $data_dir/mtgjson
set -g derived_dir $data_dir/derived

function die
    printf '%s\n' "$argv" >&2
    exit 1
end

# ISO (YYYY-MM-DD) CR effective date from cr.txt; fails silently if absent.
function cr_effective_iso
    test -r $rules_dir/cr.txt; or return 1
    set -l line (grep -m1 'effective as of' $rules_dir/cr.txt | string trim)
    set -l m (string match -r 'effective as of ([A-Z][a-z]+) ([0-9]+), ([0-9]+)' -- $line)
    test (count $m) -eq 4; or return 1
    set -l months January February March April May June July August September October November December
    set -l mi (contains -i -- $m[2] $months)
    test -n "$mi"; or return 1
    printf '%04d-%02d-%02d\n' $m[4] $mi $m[3]
end
