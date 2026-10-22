#!/usr/bin/env fish

source (status dirname)/lib/setup.fish
or return

function fetch_mtgjson
    set wanted_files \
        Meta.json \
        CompiledList.json \
        EnumValues.json \
        Keywords.json \
        CardTypes.json \
        SetList.json \
        AllPrintings.json \
        AtomicCards.json \
        AllSetFiles.tar \
        AllPrintings.sqlite

    mtgjson download $wanted_files
end

# Shared refresh retains the previous CR edition for citation diffs and also
# downloads the base catalogs. Card downloads above remain the repo's full tier.
fetch_mtgjson
set -l setup_data (path resolve (status dirname))/../skills/mtg-rules/scripts/setup-data
$setup_data --dest $data_dir
