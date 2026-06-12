# Sites jsonl -> one token per citation occurrence, with resolved members.
#   $keys[0]: cr.json keys in document order (leaves)
#   $idx[0]:  {rule: position} over those keys
# status: "ok" (members[] expanded), "skip" (malformed — `check` reports these
# as MALFORMED via classify.jq; list/bless still ignore them), "gone" (a range
# endpoint is not a leaf in the current CR, or the range is reversed).
def valid_one: test("^[0-9]{1,3}(\\.[0-9]+[a-z]*)?$");
def parse_part:
  if contains("..") then
    split("..") as $ab
    | if ($ab | length) == 2 and ($ab[0] | valid_one) and ($ab[1] | valid_one)
      then {range: $ab}
      else {bad: true}
      end
  elif valid_one then {one: .}
  else {bad: true}
  end;

($keys[0]) as $K
| ($idx[0]) as $I
| . as $s
| $s.refs[]
| . as $raw
| ($raw | split(",") | map(parse_part)) as $pp
| {file: $s.file, line: $s.line, ctx: $s.ctx, raw: $raw}
  + (if ($pp | length) == 0 or any($pp[]; .bad == true) then {status: "skip"}
     else
       ([$pp[]
         | if has("one") then [.one]
           else
             ($I[.range[0]]) as $a
             | ($I[.range[1]]) as $b
             | if $a == null or $b == null or $a > $b then null
               else $K[$a:$b + 1]
               end
           end]) as $chunks
       | if any($chunks[]; . == null) then {status: "gone"}
         else {status: "ok", members: ($chunks | add)}
         end
     end)
