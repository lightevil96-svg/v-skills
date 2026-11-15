#!/usr/bin/env python3
"""Check that claimed VTuber production stages have LOCAL evidence files.

A PASS means filenames, hashes, declared gate statuses and provenance fields are
internally consistent. It does NOT validate actual Cubism authorship, MOC3
binary semantics, artistic quality, reviewer independence or app performance.
No network and no dependencies beyond Python 3.9+ standard library.

Usage:
  python scripts/vtuber/validate_release_evidence.py --init output/evidence.json
  # User/agent fills real file references, checksums and test results.
  python scripts/vtuber/validate_release_evidence.py --check output/evidence.json
"""
import argparse
import hashlib
import json
import re
import sys
from pathlib import Path

STAGES = ("KNOWLEDGE_ONLY", "CONCEPT", "ART_READY", "RIG_AUTHORED",
          "RUNTIME_EXPORTED", "APP_IMPORTED", "STREAM_READY")
GATES = ("art_review", "native_rig", "native_export", "moc_consistency",
         "vts_import", "live_tracking", "visual_acceptance")
REQUIRED = {
    "KNOWLEDGE_ONLY": (),
    "CONCEPT": ("source",),
    "ART_READY": ("source", "layered_art"),
    "RIG_AUTHORED": ("source", "layered_art", "cmo3"),
    "RUNTIME_EXPORTED": ("source", "layered_art", "cmo3", "moc3",
                         "model3", "checker_log"),
    "APP_IMPORTED": ("source", "layered_art", "cmo3", "moc3",
                     "model3", "checker_log", "app_import_recording"),
    "STREAM_READY": ("source", "layered_art", "cmo3", "moc3",
                     "model3", "checker_log", "app_import_recording",
                     "tracking_recording", "visual_review"),
}
STAGE_GATES = {
    "KNOWLEDGE_ONLY": (),
    "CONCEPT": (),
    "ART_READY": ("art_review",),
    "RIG_AUTHORED": ("art_review", "native_rig"),
    "RUNTIME_EXPORTED": ("art_review", "native_rig", "native_export", "moc_consistency"),
    "APP_IMPORTED": ("art_review", "native_rig", "native_export",
                     "moc_consistency", "vts_import"),
    "STREAM_READY": GATES,
}
EXPECTED_EXTENSIONS = {
    "layered_art": (".psd", ".psb", ".clip"),
    "cmo3": (".cmo3",),
    "moc3": (".moc3",),
    "model3": (".model3.json",),
}


def template():
    return {
        "schema_version": 1,
        "project": "UNSET",
        "production_type": "full_live2d_new_build",
        "stage_claim": "KNOWLEDGE_ONLY",
        "target_app": "VTube Studio",
        "target_app_version": "UNKNOWN",
        "art_rights_reviewed": False,
        "artifacts": {},
        "gates": {gate: "NOT_RUN" for gate in GATES},
        "reviewer": "",
        "review_notes": "",
        "provenance": {
            "cubism_version": "UNKNOWN",
            "moc_checker": "NOT_RUN",
            "vts_version": "UNKNOWN",
            "capture_device": "UNKNOWN"
        }
    }


def safe_file(root, path):
    if not isinstance(path, str) or not path.strip():
        raise ValueError("Missing artifact file path")
    if "\\" in path or "\x00" in path or re.match(r"^[A-Za-z]:", path):
        raise ValueError(f"Unsafe artifact path: {path!r}")
    item = Path(path)
    if item.is_absolute() or ".." in item.parts:
        raise ValueError(f"Absolute/traversing artifact path: {path!r}")
    target = (root / item).resolve()
    try:
        target.relative_to(root.resolve())
    except ValueError:
        raise ValueError(f"Artifact escapes evidence directory: {path!r}")
    if not target.is_file() or target.is_symlink():
        raise ValueError(f"Missing/symlink artifact file: {path}")
    if target.stat().st_size == 0:
        raise ValueError(f"Empty artifact file: {path}")
    return target


def verify_artifacts(root, artifacts, required):
    if not isinstance(artifacts, dict):
        raise ValueError("artifacts must be an object")
    missing = [name for name in required if name not in artifacts]
    if missing:
        raise ValueError("Missing artifacts for claimed stage: " + ", ".join(missing))
    verified = []
    for label, meta in artifacts.items():
        if not isinstance(meta, dict):
            raise ValueError(f"Artifact {label} must contain path and sha256")
        file_path = meta.get("path")
        target = safe_file(root, file_path)
        if label in EXPECTED_EXTENSIONS and not str(file_path).lower().endswith(EXPECTED_EXTENSIONS[label]):
            raise ValueError(f"Artifact {label} has wrong extension: {file_path}")
        expected = meta.get("sha256")
        if not isinstance(expected, str) or not re.fullmatch(r"[0-9a-f]{64}", expected):
            raise ValueError(f"Artifact {label} missing 64-char lowercase SHA256")
        digest = hashlib.sha256()
        with target.open("rb") as stream:
            for chunk in iter(lambda: stream.read(1024 * 1024), b""):
                digest.update(chunk)
        if digest.hexdigest() != expected:
            raise ValueError(f"SHA256 mismatch for {label}: {file_path}")
        verified.append(label)
    return verified


def validate(path):
    data = json.loads(path.read_text(encoding="utf-8"))
    if data.get("schema_version") != 1 or data.get("production_type") != "full_live2d_new_build":
        raise ValueError("Unsupported schema or production_type")
    stage = data.get("stage_claim")
    if stage not in STAGES:
        raise ValueError(f"Unknown stage_claim: {stage}")
    gates = data.get("gates")
    if not isinstance(gates, dict) or set(gates) != set(GATES):
        raise ValueError("All seven gate statuses are required")
    if any(status not in ("PASS", "FAIL", "NOT_RUN") for status in gates.values()):
        raise ValueError("Gate status must be PASS, FAIL or NOT_RUN")
    if stage != "KNOWLEDGE_ONLY":
        if not data.get("art_rights_reviewed"):
            raise ValueError("Cannot claim production stage without reviewed artwork rights")
        if not isinstance(data.get("project"), str) or data["project"] in ("", "UNSET"):
            raise ValueError("Set the actual project name")
    for gate in STAGE_GATES[stage]:
        if gates[gate] != "PASS":
            raise ValueError(f"Claimed {stage} requires PASS for gate {gate}")
    if any(gates[gate] == "FAIL" for gate in STAGE_GATES[stage]):
        raise ValueError("Claimed stage has failed prerequisite")
    verified = verify_artifacts(path.parent, data.get("artifacts"), REQUIRED[stage])
    if stage in ("RUNTIME_EXPORTED", "APP_IMPORTED", "STREAM_READY"):
        if not data.get("provenance", {}).get("cubism_version") or data["provenance"]["cubism_version"] == "UNKNOWN":
            raise ValueError("Actual Cubism version required for runtime-exported claim")
        if data["provenance"].get("moc_checker") in (None, "", "NOT_RUN"):
            raise ValueError("Actual consistency checker identity/version required")
    if stage in ("APP_IMPORTED", "STREAM_READY"):
        if data.get("target_app") != "VTube Studio" or data.get("target_app_version") in (None, "", "UNKNOWN"):
            raise ValueError("Actual VTube Studio runtime and version required")
    if stage == "STREAM_READY":
        if not isinstance(data.get("reviewer"), str) or len(data["reviewer"].strip()) < 2:
            raise ValueError("Human visual reviewer name required")
        if not isinstance(data.get("review_notes"), str) or len(data["review_notes"].strip()) < 30:
            raise ValueError("Substantive visual review notes required")
        if data.get("provenance", {}).get("capture_device") in (None, "", "UNKNOWN"):
            raise ValueError("Tracking capture device required")
    return {
        "stage_claim": stage,
        "structural_evidence_check": "PASS",
        "artifact_hashes_verified": verified,
        "claimed_gates": {k: v for k, v in gates.items() if v == "PASS"},
        "NOT_verified_by_this_script": [
            "genuine Cubism native authoring/export",
            "MOC3 binary consistency",
            "app video authenticity and actual tracking",
            "aesthetic quality or human-reviewer independence",
        ],
        "can_infer_10_of_10_production": False,
    }


def main():
    p = argparse.ArgumentParser(description=__doc__)
    g = p.add_mutually_exclusive_group(required=True)
    g.add_argument("--init", type=Path)
    g.add_argument("--check", type=Path)
    args = p.parse_args()
    if args.init:
        if args.init.exists():
            raise ValueError("Refusing to overwrite evidence file")
        args.init.parent.mkdir(parents=True, exist_ok=True)
        args.init.write_text(json.dumps(template(), indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        print(f"Created blank evidence template: {args.init}")
        return 0
    print(json.dumps(validate(args.check), indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (ValueError, OSError, json.JSONDecodeError) as err:
        print(f"ERROR: {err}", file=sys.stderr)
        sys.exit(2)
