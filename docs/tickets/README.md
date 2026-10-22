# Tickets

A ticket's status is the folder it lives in:

| Folder | Meaning |
|---|---|
| `planned/` | Agreed work, ready to claim once its needs are done |
| `maybe/` | Speculative or design-gated; promote to `planned/` when decided |
| `wip/` | Claimed and in progress |
| `done/` | Integrated into the default line |

jj-kata's bundled folder-Kanban driver (configured in `kata.toml`) makes the
moves. `kata claim <slug>` moves a ticket into `wip/` and creates the feature
workspace `.workspaces/<slug>`. `kata integrate` folds the work into the
default line and moves the ticket to `done/`.

## Writing a ticket

The only prescribed part is the frontmatter: `needs: [slug, ...]` lists the
tickets that must reach `done/` first. The body describes an actionable change
and records the design decisions already made that bear on it. Shape and
length are otherwise free.

## The dependency graph

`needs:` lists are graph data, not a reading list. Query the graph with
`kata kanban`: `board`, `ready`, `blocked`, `order`, `graph <slug>`,
`needs <slug>` and `check`. Don't open dependency tickets to work out their
status.
