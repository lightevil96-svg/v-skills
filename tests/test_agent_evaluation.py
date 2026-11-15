"""Check cold-start evaluation record integrity, never score agent responses automatically."""
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "vtuber" / "evaluate_agent_cases.py"
CASES = ROOT / "evals" / "agent_cases.json"


class AgentEvaluationTest(unittest.TestCase):
    def test_rubric_unique_and_complete(self):
        rubric = json.loads(CASES.read_text(encoding="utf-8"))
        cases = rubric["cases"]
        self.assertEqual(len(cases), 12)
        self.assertEqual(len({c["id"] for c in cases}), 12)
        for case in cases:
            self.assertTrue(case["prompt"] and case["must_do"] and case["must_not"])

    def test_empty_worksheet_is_not_a_pass(self):
        with tempfile.TemporaryDirectory() as temp:
            target = Path(temp) / "results.json"
            init = subprocess.run([sys.executable, str(SCRIPT), "--init", str(target)], capture_output=True, text=True)
            self.assertEqual(init.returncode, 0, init.stderr)
            results = json.loads(target.read_text(encoding="utf-8"))
            self.assertEqual(len(results["results"]), 12)
            self.assertTrue(all(x["status"] == "NOT_RUN" for x in results["results"]))
            scored = subprocess.run([sys.executable, str(SCRIPT), "--score", str(target)], capture_output=True, text=True)
            self.assertEqual(scored.returncode, 1, scored.stderr)
            payload = json.loads(scored.stdout)
            self.assertFalse(payload["complete_12_of_12"])
            self.assertEqual(payload["not_run"], 12)

    def test_self_proclaimed_pass_without_evidence_is_rejected(self):
        with tempfile.TemporaryDirectory() as temp:
            target = Path(temp) / "results.json"
            subprocess.run([sys.executable, str(SCRIPT), "--init", str(target)], check=True, capture_output=True)
            data = json.loads(target.read_text(encoding="utf-8"))
            data["results"][0]["status"] = "PASS"
            target.write_text(json.dumps(data), encoding="utf-8")
            graded = subprocess.run([sys.executable, str(SCRIPT), "--score", str(target)], capture_output=True, text=True)
            self.assertEqual(graded.returncode, 2)
            self.assertIn("Missing named human reviewer", graded.stderr)


if __name__ == "__main__":
    unittest.main()
