#!/usr/bin/env fish
# Build data/derived/cards.jsonl — one JSON object per card face — from AtomicCards.json.
# Re-run after scripts/fetch_data.fish refreshes mtgjson data.
# Note: .name is the full combined card name ("Fire // Ice"); .face is the per-face name.

source (status dirname)/lib/setup.fish
or exit 1

set -l out $data_dir/derived/cards.jsonl
mkdir -p $data_dir/derived
or exit 1

echo "build_derived: writing $out (takes ~10 seconds)…" >&2
rm -f $out.tmp
# Emits ALL faces; supported=false rows (un-sets, reversibles) are retained for corpus --all.
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
