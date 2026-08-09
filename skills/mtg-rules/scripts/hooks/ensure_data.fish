#!/usr/bin/env fish
# Cross-host wrapper: setup failures warn but never fail the agent lifecycle.

set -l payload (cat | string collect)
set -l ensure (path dirname (path resolve (status dirname)))/ensure-data

if fish --no-config $ensure
    # agy requires a JSON object from PreInvocation; Codex and Claude accept it.
    echo '{}'
    exit 0
end

if string match -q '*"invocationNum"*' -- $payload
    echo '{"injectSteps":[{"ephemeralMessage":"mtg-rules could not provision its local rules and SQLite card data. Hooks will remain non-blocking; run skills/mtg-rules/scripts/setup-data --runtime to retry."}]}'
else
    echo '{"continue":true,"systemMessage":"mtg-rules could not provision its local rules and SQLite card data. Hooks will remain non-blocking; run skills/mtg-rules/scripts/setup-data --runtime to retry."}'
end
exit 0
