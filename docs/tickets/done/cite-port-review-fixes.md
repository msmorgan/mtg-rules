---
needs: []
---

# Fix the bugs found in review of the Python port

Two independent reviews of the Python port (`cite-python-port`,
`cite-xtask-parity` and `runtime-python-port`) found these five bugs. Each one
was reproduced. Fix each with a regression test in `tests/`.

1. **Interactive `cite audit --diff` has no `git` fallback**
   (`src/mtg_rules/cite.py`, around lines 423-425).
   - With a terminal on stdin, it runs `jj --no-pager diff --git` only. In a
     git-only repo it dies with "No such file or directory: 'jj'".
   - Fall back to `git -C <root> diff` the way tracked-file discovery does,
     and give a clear error when neither tool is available.
2. **The exemption lexer loses markers** (`src/mtg_rules/exemptions.py`, `LEX`).
   - A Rust lifetime pairs with a later apostrophe in the comment, which
     swallows the `//`. This line gives no exemption:

     ```
     const K: &'static str = "100.1"; // cite: allow-noncompliant-line -- parser's key
     ```

     The same line without the apostrophe works.
   - A zero-hash raw string ending in a backslash (`r"\"`) is lexed as an
     ordinary string, so it runs to the next quote in the file and swallows
     the marker on its line. Raw strings with zero hashes must be recognized.
   - The guard stays lexical, not a language parser. Pick rules that handle
     these cases without breaking the Python- and shell-style quoting the
     existing tests cover.
3. **A dotted `coverage.out_of_scope` key crashes `cite context`**
   (`src/mtg_rules/cite.py`, around lines 282-285). A key like `"103.4"`
   raises `invalid literal for int() with base 10: '103.4'`. Keys may be a
   whole section (`123`), a section range (`800..999`) or a rule prefix
   (`103.4`, which covers 103.4 and its subrules). Match all three, and never
   crash the hook on a bad key; skip it with a warning instead.
4. **`health` mislabels the data source** (`src/mtg_rules/lookups.py`, around
   line 251).
   - Data found through a host plugin data directory reports
     `via repo-relative`.
   - A trailing slash on `$MTG_RULES_DATA` misses the match.
   - Report the source that `data.discover_data` actually used. Return it from
     discovery rather than re-deriving it, so host detection stays in one place.
5. **`setup-data` shows no download progress** (`src/mtg_rules/setup_data.py`).
   The old fish script printed each URL to stderr, plus the destination. Restore
   that; it can be one stderr line per file.

## Done when

- Each bug has a failing-then-passing test.
- These pass:
  - `fish tests/test_skill_scripts.fish`
  - `uv run --extra dev pytest`
  - `uv run --extra dev ruff check .`
  - `skills/mtg-rules/scripts/cite check`
  - `skills/mtg-rules/scripts/cite --config evals/cite-config.json check`
- On deckmaste.rs, `cite --config cite-config.json list` is still byte-identical
  to `target/debug/cargo-xtask cite list`.
