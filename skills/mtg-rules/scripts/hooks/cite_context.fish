#!/usr/bin/env fish
# PostToolUse hook — inject the official CR text for citations a tool call
# surfaced for the first time this session.
#
# Only active in repos that *consume* the skill: a repo qualifies when its VCS
# root holds a cite-config.json. deckmaste.rs does; the mtg-rules repo keeps
# its config under skills/mtg-rules/, so the skill's own development repo is
# excluded automatically and no path is ever hardcoded.
#
# Write/Edit are on by default — those are the moments a claim gets committed
# to the tree, and an edit cites a handful of rules, not hundreds. Read and
# Bash are opt-in because they inject per-file, not per-delta: a Read of
# deckmaste_engine/src/step/mod.rs carries 127 citations (~10k tokens).
#
# Env:
#   CITE_ON_READ=1       also annotate Read (whole-file: every rule it covers)
#   CITE_ON_BASH=1       also annotate Bash stdout
#   CITE_CONTEXT_FULL=1  never clip already-locked rules
#   CITE_CONTEXT_OFF=1   disable entirely
#
# Always exits 0 — a hook that fails must never break the tool call.

set -q CITE_CONTEXT_OFF; and exit 0

set -l payload (cat | string collect)
test -n "$payload"; or exit 0

set -l tool (printf '%s' $payload | jq -r '.tool_name // ""' 2>/dev/null)
set -l cwd (printf '%s' $payload | jq -r '.cwd // ""' 2>/dev/null)
set -l sid (printf '%s' $payload | jq -r '.session_id // "nosession"' 2>/dev/null)
test -n "$tool"; or exit 0

# --- gate on tool, cheapest check first ---
set -l selector
switch $tool
    case Write
        set selector '.tool_input.content // ""'
    case Edit
        set selector '.tool_input.new_string // ""'
    case Read
        set -q CITE_ON_READ; or exit 0
        set selector 'if (.tool_response | type) == "string" then .tool_response else (.tool_response.file.content? // .tool_response.content? // "") end'
    case Bash
        set -q CITE_ON_BASH; or exit 0
        set selector 'if (.tool_response | type) == "string" then .tool_response else (.tool_response.stdout? // "") end'
    case '*'
        exit 0
end

# --- gate on repo: cite-config.json beside a VCS marker ---
set -l root ""
set -l d (path resolve -- (test -n "$cwd"; and echo $cwd; or pwd))
while test -n "$d" -a "$d" != /
    if test -f $d/cite-config.json
        if test -d $d/.jj -o -d $d/.git -o -f $d/.git
            set root $d
            break
        end
    end
    set d (path dirname -- $d)
end
test -n "$root"; or exit 0

set -l text (printf '%s' $payload | jq -r "$selector" 2>/dev/null | string collect)
test -n "$text"; or exit 0

# --- gate on content: skip the cite invocation when there is nothing to find ---
if not string match -q '*[CR#*' -- "$text"
    grep -q '"format"[[:space:]]*:[[:space:]]*"bare"' $root/cite-config.json 2>/dev/null; or exit 0
    string match -rq '[1-9][0-9]{2}\.[0-9]+' -- "$text"; or exit 0
end

set -l cite (path resolve -- (status dirname)/../cite)
test -x $cite; or exit 0

# Session ledger: one rule per line, so a rule is shown once per session.
set -l tmp /tmp
set -q TMPDIR; and test -d "$TMPDIR"; and set tmp $TMPDIR
set -l ledger_dir $tmp/mtg-rules-cite
mkdir -p $ledger_dir 2>/dev/null; or exit 0
set -l ledger $ledger_dir/(string replace -ra '[^A-Za-z0-9._-]' '_' -- $sid).seen

set -l opts --seen $ledger
set -q CITE_CONTEXT_FULL; and set -a opts --full

set -l out (printf '%s' $text | $cite --config $root/cite-config.json context $opts 2>/dev/null | string collect)
test -n "$out"; or exit 0

jq -nc --arg c "$out" \
    '{hookSpecificOutput: {hookEventName: "PostToolUse", additionalContext: $c}}'
exit 0
