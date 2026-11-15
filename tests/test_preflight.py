"""Preflight tests check honest file/tool detection, not app operation."""
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "vtuber" / "preflight.py"


class PreflightTest(unittest.TestCase):
    def test_flat_png_never_claims_native_rig(self):
        with tempfile.TemporaryDirectory() as temp:
            image = Path(temp) / "character.png"
            image.write_bytes(b"test only")
            p = subprocess.run([sys.executable, str(SCRIPT), "--source", str(image)], capture_output=True, text=True)
            self.assertEqual(p.returncode, 0, p.stderr)
            obj = json.loads(p.stdout)
            self.assertEqual(obj["status"], "PREFLIGHT_ONLY")
            self.assertEqual(obj["found_by_extension_only"]["png"], ["character.png"])
            self.assertFalse(obj["actual_export_verified"])
            self.assertFalse(obj["actual_runtime_tested"])
            self.assertTrue(any("Cubism" in w for w in obj["warnings"]))

    def test_source_file_extension_does_not_prove_editor_success(self):
        with tempfile.TemporaryDirectory() as temp:
            project = Path(temp) / "character.cmo3"
            project.write_bytes(b"fake")
            p = subprocess.run([sys.executable, str(SCRIPT), "--source", str(project)], capture_output=True, text=True)
            self.assertEqual(p.returncode, 0)
            obj = json.loads(p.stdout)
            self.assertEqual(obj["found_by_extension_only"]["cmo3"], ["character.cmo3"])
            self.assertFalse(obj["actual_editor_operability_tested"])
            self.assertFalse(obj["actual_export_verified"])

    def test_missing_source_fails(self):
        with tempfile.TemporaryDirectory() as temp:
            missing = Path(temp) / "missing.psd"
            p = subprocess.run([sys.executable, str(SCRIPT), "--source", str(missing)], capture_output=True, text=True)
            self.assertEqual(p.returncode, 2)
            self.assertIn("Source does not exist", p.stderr)


if __name__ == "__main__":
    unittest.main()
