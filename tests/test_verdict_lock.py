import json
import unittest

from verdict_lock import lock, show

with open("examples/gr_delivery.json", encoding="utf-8") as fh:
    DATA = json.load(fh)
V = DATA["verdict"]
S = {s["label"]: s["text"] for s in DATA["summaries"]}
PASS = {"checks": [{"name": "consent", "ok": True, "keywords": ["consent"]}], "rules_text": "ok"}


class VerdictLockTest(unittest.TestCase):
    def test_honest_summary_shown(self):
        self.assertEqual(lock(V, S["honest"]), [])

    def test_softened_summary_rejected(self):
        problems = lock(V, S["softened"])
        self.assertTrue(any("green-light" in p for p in problems))
        self.assertTrue(any("quiet_hours" in p for p in problems))

    def test_incomplete_summary_rejected(self):
        self.assertEqual(lock(V, S["incomplete"]), ["failed check not mentioned: quiet_hours"])

    def test_rejected_summary_falls_back_to_rules(self):
        text, source = show(V, S["overconfident"])
        self.assertEqual(text, V["rules_text"])
        self.assertTrue(source.startswith("rules"))

    def test_pass_verdict_cannot_invent_problems(self):
        self.assertTrue(lock(PASS, "Do not send: consent is missing"))


if __name__ == "__main__":
    unittest.main()
