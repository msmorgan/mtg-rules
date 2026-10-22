"""Explicit, language-independent exemptions for citation-looking source text.

Markers live in //, #, --, or HTML comments. Ordinary, triple-quoted and Rust
raw strings are skipped before looking for comments, so quoted markers do not
suppress diagnostics. This is a lexical guard, not a programming-language parser.
The allow- prefix distinguishes this contract from xtask's Rust-AST exemptions.
"""

import re

# Order matters: consume complete strings before treating their contents as
# comments. Rust lifetimes aren't character literals (a closing quote is needed).
LEX = re.compile(
    r'(?P<raw>\br(?P<hashes>\#+)".*?"(?P=hashes))'
    r'|(?P<triple>""".*?"""|\'\'\'.*?\'\'\')'
    r'|(?P<string>"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\\n])*\')'
    r'|(?P<block>/\*.*?\*/)'
    r'|(?P<comment>//[^\n]*|\#[^\n]*|--[^\n]*|<!--.*?-->)',
    re.S,
)
MARKER = re.compile(
    r"cite: allow-noncompliant(?:(-line)| (begin|end))(?: -- (\S.*))?\Z"
)


def exempt_lines(text: str) -> set[int]:
    if "cite: allow-noncompliant" not in text:
        return set()
    exempt = set()
    start = None
    cursor, line = 0, 1
    for match in LEX.finditer(text):
        line += text.count("\n", cursor, match.start())
        cursor = match.start()
        if match.lastgroup != "comment":
            continue
        comment = match[0]
        prefix = "<!--" if comment.startswith("<!--") else "#" if comment.startswith("#") else comment[:2]
        body = comment[len(prefix):].removesuffix("-->" if prefix == "<!--" else "").strip()
        if not body.startswith("cite: allow-noncompliant"):
            continue
        marker = MARKER.fullmatch(body)
        if not marker or (marker[2] != "end" and not marker[3]):
            raise ValueError(f"cite: malformed noncompliance marker at line {line}; a reason is required")
        if marker[1]:
            exempt.add(line)
        else:
            # Scope delimiters must occupy their own source line.
            beginning = text.rfind("\n", 0, match.start()) + 1
            ending = text.find("\n", match.end())
            tail = text[match.end():ending if ending >= 0 else len(text)]
            if text[beginning:match.start()].strip() or tail.strip() or "\n" in comment:
                raise ValueError(f"cite: scope marker must be on its own line at line {line}")
            if marker[2] == "begin":
                if start is not None:
                    raise ValueError(f"cite: nested noncompliance scope at line {line}")
                start = line
            elif start is None:
                raise ValueError(f"cite: unmatched noncompliance end at line {line}")
            else:
                exempt.update(range(start, line + 1))
                start = None
    if start is not None:
        raise ValueError(f"cite: unclosed noncompliance scope at line {start}")
    return exempt
