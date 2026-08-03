# Semantic-audit report: each selected citation site with its claim line and
# the FULL official text of every rule it resolves to, side by side. The
# checker can only prove a cited rule exists; whether it is the rule the
# claim NAMES needs a reader — this report makes that read cheap.
#
# Input: cr.json. $toks: resolved token objects (resolve.jq output, slurped).
# $sec: cr.txt section headers. $fmt: bracketed|bare.
. as $cr
| $toks[]
| (if $fmt == "bracketed" then "[CR#\(.raw)]" else .raw end) as $tok
| if .status == "ok" then
    "\(.file):\(.line)  \($tok)",
    "  > \(.ctx)",
    (.members[] | "    \(.): \($cr[.].ruleText? // $sec[0][.] // "(not found)")"),
    ""
  else
    "\(.file):\(.line)  \($tok)  !! \(.status) — fix before auditing",
    ""
  end
