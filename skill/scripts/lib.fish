# Shared setup for mtg-rules skill scripts. Source, don't execute.
# Resolves real paths so scripts work through the ~/.claude/skills symlink.

set -l here (path resolve (status dirname))
set -g skill_dir (path dirname $here)
set -g repo_dir (path dirname $skill_dir)
set -g data_dir $repo_dir/data
set -g rules_dir $data_dir/rules
set -g catalogs_dir $data_dir/catalogs
set -g mtgjson_dir $data_dir/mtgjson
set -g derived_dir $data_dir/derived

if not test -r $rules_dir/cr.json
    echo >&2 "mtg-rules: missing $rules_dir/cr.json — run scripts/fetch_data.fish"
    exit 1
end

function die
    printf '%s\n' "$argv" >&2
    exit 1
end
