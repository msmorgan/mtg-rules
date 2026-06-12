# Candidate lines {file, line, text} -> wide-net non-compliant citation report.
# Canonical [CR#…] spans are blanked with a single non-word placeholder first,
# so matches can never come from inside a compliant citation (replaces the
# Rust offset arithmetic). Deliberately over-matches; a human filters.
#   $cfg[0].noncompliant_exempt: path suffixes whose files are skipped entirely
(($cfg[0].noncompliant_exempt) // []) as $E
| . as $l
| select(([$E[] | . as $sfx | $l.file | endswith($sfx)] | any) | not)
| (.text | gsub("\\[CR#[^\\]]*\\]"; "§")) as $t
| [($t | [match("CR ?[0-9]{1,3}(\\.[0-9]+[a-z]*)?"; "g")]),
   ($t | [match("\\brule [0-9]{1,3}(\\.[0-9]+[a-z]*)?"; "g")]),
   ($t | [match("\\b[0-9]{3}\\.[0-9]+[a-z]*\\b"; "g")])]
| add
| unique_by(.offset)
| .[]
| "\($l.file):\($l.line)  \"\(.string)\"  \($l.text | gsub("^\\s+|\\s+$"; ""))"
