---
needs: [cite-xtask-parity]
---

# Port the remaining plugin runtime to standard-library Python

Remove the installed plugin's remaining dependencies on fish, rg, jq,
sha256sum, curl, xz and the sqlite3 executable. Follow jj-sensei's layout:
thin executable entry points, shared modules in `src/mtg_rules`, and Python
hook launchers. Python 3.11+ and its standard library supply the runtime;
VCS executables remain optional for VCS-specific metadata and tracked scans.

## Scope

- Port `rule`, `rule-search`, `define`, `keyword`, `mtr`, `card`, `rulings`,
  `corpus`, `lookup`, `ref`, `classify`, `underdetermined`, `health`, `version`,
  `normalize-glossary`, and `ensure-data`.
- Port the automatic bootstrap and double-bracket card hooks. Update host
  manifests and OpenCode wiring to invoke Python directly.
- Consolidate data discovery, bootstrap destination selection, glossary
  normalization and rendering in the shared package; delete runtime fish
  implementations when their callers are migrated.
- Preserve command interfaces, output contracts, data layout, hook JSON
  protocols, nonblocking failure behavior, and the persistent data-ABI marker.
  Keep startup locking, interrupted-owner recovery, staging validation and
  concurrent-session serialization. Use parameterized read-only SQLite queries.
- Update documentation and fixture copying/interpreter selection. Keep existing
  behavioral assertions. Add focused tests for bootstrap concurrency/failure,
  hook protocols, lookup edge cases and operation without external utilities.
- Development-only fish harnesses and corpus/evaluation scripts may remain;
  give them a Python data-discovery path in place of runtime `lib.fish`.

## Done when

- No installed script or hook requires the removed utilities, including
  transitive calls. An isolated PATH smoke test demonstrates that property.
- The existing shell harness, pytest, Ruff and both citation checks pass.
  Manifest hook commands point at executable Python launchers.
- CLI and hook behavior is checked against fixtures and representative local
  rules/card data. Document deliberate compatibility corrections.
- Integrate the ticket and move it to `done/` through Kata.

## Completed

All installed commands and hooks now use shared standard-library Python
modules with executable launchers. Host manifests invoke Python directly;
`lib.fish` is removed and development consumers use `data-path`. Bootstrap
retains serialization, stale/ownerless lock recovery, staged validation and
marker-last publication. SQLite queries are parameterized and read-only.

Validation: 99 pytest tests, 250 shell assertions, 16 evaluation unittests,
Ruff, and both citation checks pass (7,813 skill and 263 eval citations;
zero stale). The Python suite exercises every command and hook with only
Python on PATH, plus concurrent provisioning and failed/live/stale owners.
Seventeen representative lookups match captured pre-port stdout, stderr and
exit status exactly. Network downloads were covered with offline fixtures;
no live download was required for verification.

Deliberate compatibility changes: regex searches use Python `re`; the legacy
`git_commit` metadata key reports the jj parent ID, or null without jj.
The card hook accepts whitespace-formatted transcript JSON. Development fish
harnesses remain outside the installed runtime dependency contract.
