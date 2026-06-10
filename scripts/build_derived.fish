#!/usr/bin/env fish
# Build data/derived/cards.jsonl — one JSON object per card face — from AtomicCards.json.
# Re-run after scripts/fetch_data.fish refreshes mtgjson data.

source (status dirname)/lib/setup.fish
or exit 1

set -l out $data_dir/derived/cards.jsonl
mkdir -p $data_dir/derived

echo "build_derived: writing $out (takes ~1 minute)…" >&2
jq -c '
    .data | to_entries[] | .value[]
    | { name, face: .faceName, side, layout,
        manaCost, manaValue, type, types, supertypes, subtypes,
        text, power, toughness, loyalty, defense,
        colors, colorIdentity,
        supported: (((.legalities.vintage // "Banned") != "Banned")
                    and .layout != "reversible_card") }
' $mtgjson_dir/AtomicCards.json > $out.tmp
and mv $out.tmp $out
and echo "build_derived: "(count < $out)" face records" >&2
