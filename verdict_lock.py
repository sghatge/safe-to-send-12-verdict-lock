"""Rules decide, the model explains, and a lock makes sure the model can't overrule them.

Checks a model-written summary against the rule verdicts it is supposed to explain:
- a failed verdict may never be described as ready, fine or passed
- every failed check must be mentioned
- a passed verdict may not invent problems
If the summary breaks the lock, the rules-only text is shown instead. Standard library only.
"""
import json
import re
import sys

GREEN_LIGHT = [r"ready to (send|go)", r"good to go", r"looks? (good|fine|great)", r"all clear",
               r"no (real |major )?issues", r"\bpassed\b", r"safe to send", r"approve(d)?"]
ALARM = [r"\bfail", r"\bblock", r"must fix", r"do not send", r"\bmissing\b"]


def contains(text, patterns):
    return [p for p in patterns if re.search(p, text, re.I)]


def lock(verdict, summary):
    """Return a list of violations. Empty list = the summary may be shown."""
    problems = []
    failed = [c for c in verdict["checks"] if not c["ok"]]
    if failed:
        for p in contains(summary, GREEN_LIGHT):
            problems.append(f"green-light language on a failed verdict: /{p}/")
        for c in failed:
            if not any(k.lower() in summary.lower() for k in c["keywords"]):
                problems.append(f"failed check not mentioned: {c['name']}")
    else:
        for p in contains(summary, ALARM):
            problems.append(f"invents a problem on a passed verdict: /{p}/")
    return problems


def show(verdict, summary):
    problems = lock(verdict, summary)
    return (summary, "model") if not problems else (verdict["rules_text"], "rules (summary rejected)")


def main(path):
    with open(path, encoding="utf-8") as fh:
        data = json.load(fh)
    verdict = data["verdict"]
    for s in data["summaries"]:
        problems = lock(verdict, s["text"])
        status = "SHOWN   " if not problems else "REJECTED"
        print(f"{status} [{s['label']}] {s['text']}")
        for p in problems:
            print(f"           - {p}")
    print()


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "examples/gr_delivery.json")
