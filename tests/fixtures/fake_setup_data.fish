#!/usr/bin/env fish

argparse dest= runtime -- $argv; or exit 2
set -q _flag_dest; or exit 2
set -q _flag_runtime; or exit 2

if set -q MTG_RULES_FAKE_SETUP_FAIL
    echo >&2 "fake setup failure"
    exit 1
end

if set -q MTG_RULES_FAKE_SETUP_DELAY
    sleep $MTG_RULES_FAKE_SETUP_DELAY
end

if set -q MTG_RULES_FAKE_SETUP_COUNT
    set -l count 0
    test -r $MTG_RULES_FAKE_SETUP_COUNT; and set count (cat $MTG_RULES_FAKE_SETUP_COUNT)
    math $count + 1 >$MTG_RULES_FAKE_SETUP_COUNT
end

mkdir -p $_flag_dest/rules $_flag_dest/catalogs $_flag_dest/mtgjson
echo 'Magic: The Gathering Comprehensive Rules' >$_flag_dest/rules/cr.txt
echo '{"100.1":{"ruleNumber":"100.1","examples":null,"ruleText":"Fixture rule text.","fragment":"1","navigation":{"previousRule":null,"nextRule":null}}}' >$_flag_dest/rules/cr.json
for file in keywords.json unofficial-glossary.json mtr.json
    echo '{}' >$_flag_dest/rules/$file
end
echo '{"fixture":{"term":"Fixture","definition":"Fixture glossary entry."}}' >$_flag_dest/rules/glossary.json
for catalog in \
    card-names artist-names word-bank supertypes card-types artifact-types \
    battle-types creature-types enchantment-types land-types planeswalker-types \
    spell-types powers toughnesses loyalties keyword-abilities keyword-actions \
    ability-words flavor-words watermarks
    echo '{"object":"catalog","data":[]}' >$_flag_dest/catalogs/$catalog.json
end
sqlite3 $_flag_dest/mtgjson/AllPrintings.sqlite \
    "CREATE TABLE cards(name TEXT, faceName TEXT, layout TEXT, manaCost TEXT, type TEXT, text TEXT, power TEXT, toughness TEXT, loyalty TEXT, defense TEXT, side TEXT); INSERT INTO cards VALUES ('Lightning Bolt', NULL, 'normal', '{R}', 'Instant', 'Lightning Bolt deals 3 damage to any target.', NULL, NULL, NULL, NULL, NULL);"
