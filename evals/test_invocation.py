"""Offline checks of trace evidence; no paid agent runs."""

import unittest

from invocation import grade, script_commands


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
        for command in ["echo /plugin/skills/mtg-rules/scripts/rule 400.7",
                        "echo 'x; scripts/rule 400.7'", "# scripts/rule 400.7",
                        "scripts/rule 400.7; true", "scripts/rule 400.7 | head"]:
            self.assertEqual(script_commands(command), set(), command)
        self.assertEqual(script_commands('fish "/plugin/skills/mtg-rules/scripts/rule" 400.7'), {"rule"})
        self.assertEqual(script_commands("cd /plugin/skills/mtg-rules && scripts/rule 400.7"), {"rule"})


if __name__ == "__main__":
    unittest.main()
