# mtg-rules

This repository develops the plugin in `skills/mtg-rules/`. Read its
[SKILL.md](skills/mtg-rules/SKILL.md) when changing runtime instructions,
reference synthesis, or lookup behavior; it owns source authority and the
verification workflow.

## Reference synthesis

- Verify each new or changed claim against its governing source before writing
  it. Treat rule numbers supplied in plans as hypotheses until resolved.
- Give every rules claim a dotted citation. `cite check` checks existence and
  text drift; a reader must still establish that the cited rule supports the claim.
- Before merging synthesis changes, perform a refutation pass against source
  text and official rulings; re-verify proposed corrections.
- Write closed taxonomies in full and point open vocabularies to the catalogs.
  Mark engine inferences and register CR-underdetermined choices in
  `skills/mtg-rules/references/underdetermined.md`.
- Preserve each reference's italic synthesis-date header. Split material when
  independent question branches need different passages; use sibling pointers
  to keep each derivation in one place.
- For CR refreshes, read [README.md's maintenance checklist](README.md#maintenance-post-refresh-checklist).
  For synthesis validation, read the affected probes in
  [evals/rulings-check.md](evals/rulings-check.md) and its Maintenance procedure.

## Working in this repo

- Use jj exclusively. Pushes and bookmark moves require the user's request.
- Work is tracked with jj-kata (`kata.toml`). Tickets live in `docs/tickets/`
  (see its README). Claim a ticket or start a named workspace before changing
  files; the `default` workspace is for coordination.
- Parallel implementers edit files; the coordinating agent owns jj operations,
  since snapshots include the entire working copy.
- Invoke fish scripts as executables or with `fish`, regardless of the caller's shell.
- Script changes use `tests/test_skill_scripts.fish`; eval tooling has
  `python3 -m unittest discover -s evals -p 'test_*.py'`. Before completing skill changes, run
  `fish tests/test_skill_scripts.fish` and
  `skills/mtg-rules/scripts/cite check` (both exit 0).
  Changes to validation records also require
  `skills/mtg-rules/scripts/cite --config evals/cite-config.json check`.
- Prefer the most capable model tier for synthesis/review subagents; cheap
  tiers only for mechanical fixes/wiring.
