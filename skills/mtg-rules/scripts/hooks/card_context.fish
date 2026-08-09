#!/usr/bin/env fish
# UserPromptSubmit hook — inject exact card lookups for [[Card Name]] tokens.
# Invalid double-bracketed text is ignored, and hook failures never block the prompt.

set -l payload (cat)
set -l prompt (printf '%s' "$payload" | jq -r '.prompt // empty' 2>/dev/null)
test -n "$prompt"; or exit 0

set -l names (printf '%s' "$prompt" | jq -Rrs '
    scan("\\\\[\\\\[([^][\\\\r\\\\n]+)\\\\]\\\\]")
    | .[0]
' 2>/dev/null)
test (count $names) -gt 0; or exit 0

set -l card (path resolve (status dirname)/../card)
test -x $card; or exit 0

set -l seen
set -l cards
for name in $names
    set -l key (string lower -- $name)
    contains -- $key $seen; and continue
    set -a seen $key

    set -l rendered ($card --full-name "$name" 2>/dev/null | string collect)
    test -n "$rendered"; and set -a cards "$rendered"
end

test (count $cards) -gt 0; or exit 0

begin
    printf '%s\n\n' 'Authoritative card data resolved from double-bracketed names in the user prompt:'
    for rendered in $cards
        printf '%s\n\n' "$rendered"
    end
end | jq -Rs '{
    hookSpecificOutput: {
        hookEventName: "UserPromptSubmit",
        additionalContext: .
    }
}' 2>/dev/null

exit 0
