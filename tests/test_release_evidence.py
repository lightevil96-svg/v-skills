"""Structural evidence tests. Never claim a genuine .cmo3/.moc3 or app test."""
import hashlib
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "vtuber" / "validate_release_evidence.py"


class EvidenceValidationTest(unittest.TestCase):
    def init(self, folder):
        record = folder / "evidence.json"
        p = subprocess.run([sys.executable, str(SCRIPT), "--init", str(record)],
                           capture_output=True, text=True)
        self.assertEqual(p.returncode, 0, p.stderr)
        return record

    def check(self, record):
        return subprocess.run([sys.executable, str(SCRIPT), "--check", str(record)],
                              capture_output=True, text=True)

    def test_knowledge_only_can_never_imply_model_completion(self):
        with tempfile.TemporaryDirectory() as temp:
            record = self.init(Path(temp))
            out = self.check(record)
            self.assertEqual(out.returncode, 0, out.stderr)
            info = json.loads(out.stdout)
            self.assertEqual(info["stage_claim"], "KNOWLEDGE_ONLY")
            self.assertFalse(info["can_infer_10_of_10_production"])
            self.assertTrue(info["NOT_verified_by_this_script"])

    def test_concept_requires_actual_hashed_artwork(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            record = self.init(root)
            obj = json.loads(record.read_text())
            obj["project"] = "synthetic-test"
            obj["art_rights_reviewed"] = True
            obj["stage_claim"] = "CONCEPT"
            art = root / "source.png"
            art.write_bytes(b"not a real PNG: hash-only fixture")
            obj["artifacts"]["source"] = {
                "path": "source.png", "sha256": hashlib.sha256(art.read_bytes()).hexdigest()
            }
            record.write_text(json.dumps(obj))
            out = self.check(record)
            self.assertEqual(out.returncode, 0, out.stderr)
            self.assertEqual(json.loads(out.stdout)["stage_claim"], "CONCEPT")
            obj["artifacts"]["source"]["sha256"] = "0" * 64
            record.write_text(json.dumps(obj))
            out = self.check(record)
            self.assertEqual(out.returncode, 2)
            self.assertIn("SHA256 mismatch", out.stderr)

    def test_stream_ready_false_claim_rejected(self):
        with tempfile.TemporaryDirectory() as temp:
            record = self.init(Path(temp))
            obj = json.loads(record.read_text())
            obj["stage_claim"] = "STREAM_READY"
            obj["project"] = "fake"
            obj["art_rights_reviewed"] = True
            record.write_text(json.dumps(obj))
            out = self.check(record)
            self.assertEqual(out.returncode, 2)
            self.assertIn("requires PASS", out.stderr)

    def test_path_traversal_rejected(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            record = self.init(root)
            obj = json.loads(record.read_text())
            obj["project"] = "fixture"
            obj["stage_claim"] = "CONCEPT"
            obj["art_rights_reviewed"] = True
            obj["artifacts"] = {"source": {"path": "../outside.png", "sha256": "0" * 64}}
            record.write_text(json.dumps(obj))
            out = self.check(record)
            self.assertEqual(out.returncode, 2)
            self.assertIn("traversing artifact path", out.stderr)

    def test_init_never_overwrites_existing_evidence(self):
        with tempfile.TemporaryDirectory() as temp:
            record = self.init(Path(temp))
            out = subprocess.run([sys.executable, str(SCRIPT), "--init", str(record)],
                                 capture_output=True, text=True)
            self.assertEqual(out.returncode, 2)
            self.assertIn("Refusing to overwrite", out.stderr)


if __name__ == "__main__":
    unittest.main()
