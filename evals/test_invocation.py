"""Offline checks of trace evidence; no paid agent runs."""

import unittest

from invocation import doc_reads, grade, script_commands


POSITIVE = {"invoke": True, "scripts": ["rule"], "docs": ["state.md"]}
NEGATIVE = {"invoke": False, "scripts": [], "docs": []}
INIT = {"type": "system", "subtype": "init", "skills": ["mtg-rules:mtg-rules"]}
FINAL = {"type": "result", "subtype": "success", "result": "Answer", "is_error": False}


def action(tool, args, error=False):
    return [
        {"type": "assistant", "message": {"content": [
            {"type": "tool_use", "id": "use", "name": tool, "input": args}]}},
        {"type": "user", "message": {"content": [
            {"type": "tool_result", "tool_use_id": "use", "is_error": error,
             "content": "Permission denied" if error else "Source text"}]}},
    ]


class EvidenceTests(unittest.TestCase):
    def trace(self):
        return [INIT] + action("Skill", {"skill": "mtg-rules:mtg-rules"}) + action(
            "Bash", {"command": "/plugin/skills/mtg-rules/scripts/rule 400.7"}) + action(
            "Read", {"file_path": "/plugin/skills/mtg-rules/references/state.md"}) + [FINAL]

    def test_successful_route(self):
        self.assertEqual(grade(POSITIVE, self.trace()), [])

    def test_claimed_use_is_not_evidence(self):
        trace = [INIT, {**FINAL, "result": "I used mtg-rules, rule, and state.md."}]
        self.assertEqual(len(grade(POSITIVE, trace)), 3)

    def test_denied_lookup_is_not_evidence(self):
        trace = self.trace()
        trace[4]["message"]["content"][0]["is_error"] = True
        self.assertEqual(grade(POSITIVE, trace), ["missing successful script: rule"])

    def test_wrong_doc_does_not_satisfy_route(self):
        trace = self.trace()
        trace[5]["message"]["content"][0]["input"]["file_path"] = "/other/state.md"
        self.assertEqual(grade(POSITIVE, trace), ["missing successful reference read: state.md"])

    def test_negative_requires_available_skill_and_completion(self):
        self.assertEqual(grade(NEGATIVE, [INIT, FINAL]), [])
        self.assertTrue(grade(NEGATIVE, [FINAL]))
        self.assertTrue(grade(NEGATIVE, [INIT]))
        self.assertTrue(grade(NEGATIVE, [INIT, {**FINAL, "is_error": True}]))

    def test_negative_rejects_even_failed_invocation(self):
        trace = [INIT] + action("Skill", {"skill": "mtg-rules"}, error=True) + [FINAL]
        self.assertEqual(grade(NEGATIVE, trace), ["unexpected MTG skill activity"])

    def test_negative_rejects_compound_script_attempt(self):
        trace = [INIT] + action("Bash", {"command": "scripts/rule 400.7; true"}) + [FINAL]
        self.assertEqual(grade(NEGATIVE, trace), ["unexpected MTG skill activity"])

    def test_reading_skill_is_a_valid_load(self):
        trace = self.trace()
        trace[1:3] = action("Read", {"file_path": "/plugin/skills/mtg-rules/SKILL.md"})
        self.assertEqual(grade(POSITIVE, trace), [])

    def test_echo_comments_and_masked_failures_are_not_lookups(self):
        for command in ["python3 -c scripts/rule 400.7", "echo /plugin/skills/mtg-rules/scripts/rule 400.7",
                        "echo 'x; scripts/rule 400.7'", "# scripts/rule 400.7",
                        "scripts/rule 400.7; true", "scripts/rule 400.7 | head"]:
            self.assertEqual(script_commands(command), set(), command)
        self.assertEqual(script_commands('python3 "/plugin/skills/mtg-rules/scripts/rule" 400.7'), {"rule"})
        self.assertEqual(script_commands('fish "/plugin/skills/mtg-rules/scripts/rule" 400.7'), {"rule"})
        self.assertEqual(script_commands("cd /plugin/skills/mtg-rules && scripts/rule 400.7"), {"rule"})


    def test_shell_reads_credit_the_named_doc(self):
        refs = "/plugin/skills/mtg-rules/references/state.md"
        for command in [f"cat {refs}", f"sed -n '1,40p' {refs}", f"head -n 30 {refs}",
                        f"tail -20 {refs}", f"less {refs}", f"grep -n 'zone' {refs}",
                        f"rg -i -e zone -e object {refs}", f"rg --glob '*.md' zone {refs}",
                        f"grep -A 3 -m 2 zone {refs}", f"grep -ne zone {refs}",
                        "cat skills/mtg-rules/references/state.md",
                        "cat ./skills/mtg-rules/references/state.md",
                        "cat references/state.md", "cat ./references/state.md",
                        "/usr/bin/cat references/state.md", "head -5 -- references/state.md",
                        "cd /plugin/skills/mtg-rules && sed -n '1,9p' references/state.md"]:
            self.assertEqual(doc_reads(command), {"state.md"}, command)
        self.assertEqual(doc_reads("cat references/state.md references/turn.md"),
                         {"state.md", "turn.md"})

    def test_ref_script_credits_the_named_doc(self):
        for command in ["/plugin/skills/mtg-rules/scripts/ref state", "scripts/ref state.md",
                        "skills/mtg-rules/scripts/ref state 'Zone changes'",
                        "./scripts/ref state.md zones", 'fish "/plugin/skills/mtg-rules/scripts/ref" state',
                        "cd /plugin/skills/mtg-rules && scripts/ref state"]:
            self.assertEqual(doc_reads(command), {"state.md"}, command)
        self.assertEqual(script_commands("scripts/ref state"), {"ref"})
        for command in ["ref state", "echo scripts/ref state", "scripts/ref", "scripts/ref --list",
                        "scripts/ref ../state", "scripts/ref references/state.md", "scripts/ref state; true"]:
            self.assertEqual(doc_reads(command), set(), command)

    def test_broad_or_unrelated_shell_reads_name_no_doc(self):
        for command in ["grep -rn zone skills/mtg-rules/references",
                        "grep -rn zone skills/mtg-rules/references/",
                        "grep -n zone skills/mtg-rules/references/*.md",
                        "rg zone skills/mtg-rules/references/", "cat references/*.md",
                        "cat skills/mtg-rules/references/s*.md", "cat references/{state,turn}.md",
                        "grep zone references/state.md references/turn.md",
                        "rg zone references/state.md references/",
                        "grep references/state.md notes.txt", "rg -g 'references/state.md' zone",
                        "cat /other/references/state.md", "cat /other/state.md", "cat state.md",
                        "cat references/sub/state.md", "cat references/state.txt",
                        "cat skills/mtg-rules/SKILL.md", "ls skills/mtg-rules/references",
                        "echo references/state.md", "# cat references/state.md",
                        "wc -l references/state.md", "cat references/state.md | head",
                        "cat references/state.md; true", "bash -c 'cat references/state.md'"]:
            self.assertEqual(doc_reads(command), set(), command)

    def test_shell_read_is_evidence_only_after_success(self):
        trace = [INIT] + action("Skill", {"skill": "mtg-rules:mtg-rules"}) + action(
            "Bash", {"command": "/plugin/skills/mtg-rules/scripts/rule 400.7"}) + action(
            "Bash", {"command": "sed -n '1,40p' references/state.md"}) + [FINAL]
        self.assertEqual(grade(POSITIVE, trace), [])
        trace[6]["message"]["content"][0]["is_error"] = True
        self.assertEqual(grade(POSITIVE, trace), ["missing successful reference read: state.md"])
        trace[6]["message"]["content"][0].update(is_error=False, content="")
        self.assertEqual(grade(POSITIVE, trace), ["missing successful reference read: state.md"])

    def test_ref_script_satisfies_doc_and_script_routes(self):
        trace = [INIT] + action("Skill", {"skill": "mtg-rules:mtg-rules"}) + action(
            "Bash", {"command": "/plugin/skills/mtg-rules/scripts/ref state 'Zone changes'"}) + [FINAL]
        self.assertEqual(grade({**POSITIVE, "scripts": ["ref"]}, trace), [])
        self.assertEqual(grade(POSITIVE, trace), ["missing successful script: rule"])
        self.assertEqual(grade({**POSITIVE, "docs": ["turn.md"]}, trace),
                         ["missing successful script: rule", "missing successful reference read: turn.md"])

    def test_directory_grep_does_not_satisfy_doc_route(self):
        trace = self.trace()
        trace[5] = action("Bash", {"command": "grep -rn zone /plugin/skills/mtg-rules/references"})[0]
        trace[6] = action("Bash", {"command": "grep -rn zone /plugin/skills/mtg-rules/references"})[1]
        self.assertEqual(grade(POSITIVE, trace), ["missing successful reference read: state.md"])

    def test_negative_rejects_shell_reference_read_attempts(self):
        for command in ["cat references/state.md", "grep zone skills/mtg-rules/references/state.md",
                        "cat references/state.md; true", "cat references/state.md | head",
                        "scripts/ref state"]:
            trace = [INIT] + action("Bash", {"command": command}, error=True) + [FINAL]
            self.assertEqual(grade(NEGATIVE, trace), ["unexpected MTG skill activity"], command)
        trace = [INIT] + action("Bash", {"command": "cat notes/state.md"}) + [FINAL]
        self.assertEqual(grade(NEGATIVE, trace), [])


if __name__ == "__main__":
    unittest.main()
