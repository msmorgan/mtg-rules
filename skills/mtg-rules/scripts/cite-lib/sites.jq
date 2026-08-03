# rg --json match events -> {file, line, ctx, refs[]} per matching line.
# $fmt: "bracketed" strips the [CR# … ] wrapper from each token; "bare" keeps it.
# $root: prefix stripped from absolute paths for display.
select(.type == "match")
| .data
| {file: (.path.text | ltrimstr($root + "/")),
   line: .line_number,
   ctx: (.lines.text | rtrimstr("\n") | gsub("^\\s+|\\s+$"; "")),
   refs: [.submatches[].match.text
          | if $fmt == "bracketed" then .[4:-1] else . end]}
