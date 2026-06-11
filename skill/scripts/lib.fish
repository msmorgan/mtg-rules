# Shared setup for mtg-rules skill scripts. Source, don't execute.
# Resolves real paths so scripts work through the ~/.claude/skills symlink.

set -l here (path resolve (status dirname))
set -g skill_dir (path dirname $here)

# Data resolution chain — each candidate accepted iff <dir>/rules/cr.json is readable:
#   1. $MTG_RULES_DATA (if set)
#   2. ~/.claude/plugins/data/mtg-rules/data
#   3. (path dirname $skill_dir)/data  (dev/repo layout)
set -g data_dir ""
set -l _candidates
if set -q MTG_RULES_DATA
    set -a _candidates $MTG_RULES_DATA
end
set -a _candidates $HOME/.claude/plugins/data/mtg-rules/data
set -a _candidates (path dirname $skill_dir)/data

for _cand in $_candidates
    if test -r $_cand/rules/cr.json
        set data_dir $_cand
        break
    end
end

if test -z "$data_dir"
    echo >&2 "mtg-rules: could not find data directory. Tried:"
    echo >&2 "  1. \$MTG_RULES_DATA = "(set -q MTG_RULES_DATA; and echo $MTG_RULES_DATA; or echo "(not set)")
    echo >&2 "  2. $HOME/.claude/plugins/data/mtg-rules/data"
    echo >&2 "  3. "(path dirname $skill_dir)/data
    echo >&2 "Populate data with: scripts/setup-data (plugin installs) or scripts/fetch_data.fish (repo checkouts)"
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
