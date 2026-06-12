# cr.json (stdin) + $mem (rawfile: one rule per line) + $sec[0] (sections map)
# -> "rule<TAB>normalized text" for each member that exists.
# Normalization mirrors the Rust checker: collapse whitespace runs to single
# spaces, trim the ends. The checksum is sha256 over EXACTLY this string (no
# trailing newline) — computed by the caller, truncated to 16 hex chars.
($mem | split("\n") | map(select(length > 0)) | unique) as $ms
| . as $cr
| $ms[]
| . as $m
| ($cr[$m].ruleText? // $sec[0][$m] // null) as $t
| select($t != null)
| "\($m)\t\($t | gsub("\\s+"; " ") | gsub("^ +| +$"; ""))"
