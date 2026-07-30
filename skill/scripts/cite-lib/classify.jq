# Resolved tokens -> stale report lines.
#   $cur[0]:  {rule: hash} for every cited rule that exists in the current CR
#   $lock[0]: the lockfile ({checksums: {rule: hash}, …})
# MALFORMED: bracketed-shaped token whose contents fail citation parsing
#   (resolve.jq status "skip" — bracketed mode only; bare-mode tokens come
#   from the scan regex, so they always parse).
# resolve.jq status "placeholder" (an ellipsis-only token, i.e. prose about the
#   citation format) yields nothing at all — it is not a citation to check.
# GONE: cited rule absent from the current CR (or an unexpandable range token).
# UNLOCKED: cited rule has no lock baseline (run bless).
# CHANGED: current text hash differs from the blessed baseline.
($cur[0]) as $C
| ($lock[0].checksums // {}) as $L
| if .status == "placeholder"
  then empty
  elif .status == "skip"
  then {tag: "MALFORMED", rule: .raw, file, line, ctx}
  elif .status == "gone"
  then {tag: "GONE", rule: .raw, file, line, ctx}
  else
    . as $t
    | .members[]
    | . as $m
    | ($C[$m]) as $c
    | ($L[$m]) as $b
    | if $c == null then {tag: "GONE", rule: $m, file: $t.file, line: $t.line, ctx: $t.ctx}
      elif $b == null then {tag: "UNLOCKED", rule: $m, file: $t.file, line: $t.line, ctx: $t.ctx}
      elif $c != $b then {tag: "CHANGED", rule: $m, file: $t.file, line: $t.line, ctx: $t.ctx}
      else empty
      end
  end
| "\(.tag)  \(.rule)  \(.file):\(.line)  \(.ctx)"
