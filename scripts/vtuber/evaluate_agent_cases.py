#!/usr/bin/env python3
"""Record independent, human-reviewed cold-start agent results.

This script verifies evidence records, NOT semantic correctness. Never use this
script or a 12/12 worksheet as proof that Cubism/VTube Studio production worked.
Run:
  python scripts/vtuber/evaluate_agent_cases.py --init evals/agent_results.json
  # Run each prompt with a fresh agent, save real response transcripts, then
  # fill reviewer/status/evidence_note/response_file per case.
  python scripts/vtuber/evaluate_agent_cases.py --score evals/agent_results.json
"""
import argparse
import json
import sys
from pathlib import Path


def cases_path():
    return Path(__file__).resolve().parents[2] / "evals" / "agent_cases.json"


def get_cases():
    data = json.loads(cases_path().read_text(encoding="utf-8"))
    if data.get("schema_version") != 1:
        raise ValueError("Unsupported evaluation schema version")
    cases = data.get("cases")
    if not isinstance(cases, list) or len(cases) < 10:
        raise ValueError("Expected at least ten cold-start scenarios")
    ids = [c["id"] for c in cases]
    if len(set(ids)) != len(ids):
        raise ValueError("Duplicate scenario IDs")
    for c in cases:
        if not all(isinstance(c.get(k), str) and c[k].strip() for k in ("prompt", "must_do", "must_not")):
            raise ValueError(f"Incomplete rubric scenario: {c['id']}")
    return cases


def write_template(path, cases):
    if path.exists():
        raise ValueError(f"Refusing to overwrite existing results: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    data = {
        "schema_version": 1,
        "evaluation_notice": "Requires a DIFFERENT agent for each cold-start prompt and independent HUMAN reviewer; not automated response grading.",
        "model_id": "",
        "run_date": "",
        "results": [
            {
                "id": c["id"],
                "status": "NOT_RUN",
                "reviewer": "",
                "response_file": "",
                "evidence_note": "",
            }
            for c in cases
        ],
    }
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def score(path, cases):
    obj = json.loads(path.read_text(encoding="utf-8"))
    if obj.get("schema_version") != 1:
        raise ValueError("Invalid results schema")
    runs = obj.get("results", [])
    ids = [c["id"] for c in cases]
    run_ids = [r.get("id") for r in runs]
    if len(runs) != len(cases) or len(set(run_ids)) != len(run_ids) or set(run_ids) != set(ids):
        raise ValueError("Results must contain each scenario ID exactly once")
    passed = 0
    failed = 0
    not_run = 0
    for r in runs:
        status = r.get("status")
        if status not in ("PASS", "FAIL", "NOT_RUN"):
            raise ValueError(f"Invalid status {status!r} for {r['id']}")
        if status == "NOT_RUN":
            not_run += 1
            continue
        reviewer = r.get("reviewer", "")
        note = r.get("evidence_note", "")
        response = r.get("response_file", "")
        if not isinstance(reviewer, str) or len(reviewer.strip()) < 2:
            raise ValueError(f"Missing named human reviewer for {r['id']}")
        if not isinstance(note, str) or len(note.strip()) < 30:
            raise ValueError(f"Missing substantive evaluation note for {r['id']}")
        if not isinstance(response, str) or not response.strip():
            raise ValueError(f"Missing response transcript path for {r['id']}")
        source = (path.parent / response).resolve()
        if not source.is_file() or source.stat().st_size < 20:
            raise ValueError(f"Actual response transcript file required for {r['id']}: {response}")
        if status == "PASS":
            passed += 1
        else:
            failed += 1
    result = {
        "rubric_scenarios": len(cases), "human_reviewed_pass": passed,
        "human_reviewed_fail": failed, "not_run": not_run,
        "complete_12_of_12": passed == len(cases) and failed == 0 and not_run == 0,
        "meaning": "Human-reviewed agent instruction comprehension ONLY; NOT model-production quality or independent AI grader verification.",
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["complete_12_of_12"] else 1


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    group = ap.add_mutually_exclusive_group(required=True)
    group.add_argument("--init", type=Path)
    group.add_argument("--score", type=Path)
    args = ap.parse_args()
    cases = get_cases()
    if args.init:
        write_template(args.init, cases)
        print(f"Created blank evaluation worksheet ({len(cases)} NOT_RUN): {args.init}")
        return 0
    return score(args.score, cases)


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (ValueError, OSError, KeyError, json.JSONDecodeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        sys.exit(2)
