"""Synthetic fixture tests; these do not validate a real Cubism MOC3 runtime."""
import json
import subprocess
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / 'scripts' / 'vtuber' / 'repack_vts.py'

def synthetic_png():
    """Build an actual 1x1 PNG; no external dependencies."""
    import struct
    import zlib
    def chunk(kind, payload):
        return struct.pack(">I", len(payload)) + kind + payload + struct.pack(">I", zlib.crc32(kind + payload) & 0xffffffff)
    ihdr = struct.pack(">IIBBBBB", 1, 1, 8, 6, 0, 0, 0)
    return b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", ihdr) + chunk(b"IDAT", zlib.compress(b"\x00\x00\x00\x00\x00")) + chunk(b"IEND", b"")



def fixture(root, bad=False):
    model = root / 'OrangeScarf'
    (model / 'OrangeScarf.2048').mkdir(parents=True)
    (model / 'animations').mkdir()
    (root / 'Source').mkdir()
    (root / 'Source' / 'original.psd').write_bytes(b'original')
    (root / 'BUILD_REPORT.txt').write_text('non-runtime report')
    (model / 'OrangeScarf.moc3').write_bytes(b'MOC3' + bytes(60))  # mock header, NOT real Cubism export
    (model / 'OrangeScarf.2048' / 'texture_00.png').write_bytes(synthetic_png())
    (model / 'OrangeScarf.physics3.json').write_text('{}')
    (model / 'animations' / 'Idle.motion3.json').write_text('{}')
    (model / 'OrangeScarf.model3.json').write_text(json.dumps({'Version': 3, 'FileReferences': {'Moc': '../Source/original.psd' if bad else 'OrangeScarf.moc3', 'Textures': ['OrangeScarf.2048/texture_00.png'], 'Physics': 'OrangeScarf.physics3.json', 'Motions': {'Idle': [{'File': 'animations/Idle.motion3.json'}]}}}))


class RepackTest(unittest.TestCase):
    def test_directory_to_runtime_zip(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / 'input'
            fixture(root)
            output = Path(tmp) / 'release.zip'
            run = subprocess.run([sys.executable, str(SCRIPT), str(root), '--output', str(output), '--folder-name', 'OrangeScarf_vts'], capture_output=True, text=True)
            self.assertEqual(run.returncode, 0, run.stderr)
            data = json.loads(run.stdout)
            self.assertEqual(data['references_checked'], 4)
            self.assertFalse(data['runtime_verified'])
            with zipfile.ZipFile(output) as z:
                names = z.namelist()
                self.assertIn('OrangeScarf_vts/OrangeScarf.model3.json', names)
                self.assertIn('OrangeScarf_vts/OrangeScarf.2048/texture_00.png', names)
                self.assertFalse(any('Source/' in n or 'BUILD_REPORT' in n for n in names))
            again = subprocess.run([sys.executable, str(SCRIPT), str(output), '--inspect'], capture_output=True, text=True)
            self.assertEqual(again.returncode, 0, again.stderr)
            overwrite = subprocess.run([sys.executable, str(SCRIPT), str(root), '--output', str(output)], capture_output=True, text=True)
            self.assertNotEqual(overwrite.returncode, 0)
            self.assertIn('refusing to overwrite', overwrite.stderr)

    def test_invalid_paths_fail_closed(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / 'input'
            fixture(root, bad=True)
            run = subprocess.run([sys.executable, str(SCRIPT), str(root), '--inspect'], capture_output=True, text=True)
            self.assertNotEqual(run.returncode, 0)
            self.assertIn('Path traversal', run.stderr)

    def test_reject_fake_moc3_and_bad_png(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / 'input'
            fixture(root)
            (root / 'OrangeScarf' / 'OrangeScarf.moc3').write_bytes(b'not actually a MOC3')
            invalid_moc = subprocess.run([sys.executable, str(SCRIPT), str(root), '--inspect'], capture_output=True, text=True)
            self.assertNotEqual(invalid_moc.returncode, 0)
            self.assertIn('Invalid MOC3 header', invalid_moc.stderr)
            (root / 'OrangeScarf' / 'OrangeScarf.moc3').write_bytes(b'MOC3' + bytes(60))
            (root / 'OrangeScarf' / 'OrangeScarf.2048' / 'texture_00.png').write_bytes(b'not a png')
            invalid_png = subprocess.run([sys.executable, str(SCRIPT), str(root), '--inspect'], capture_output=True, text=True)
            self.assertNotEqual(invalid_png.returncode, 0)
            self.assertIn('Invalid PNG signature', invalid_png.stderr)

    def test_missing_reference_fails_closed(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / 'input'
            fixture(root)
            (root / 'OrangeScarf' / 'OrangeScarf.moc3').unlink()
            run = subprocess.run([sys.executable, str(SCRIPT), str(root), '--inspect'], capture_output=True, text=True)
            self.assertNotEqual(run.returncode, 0)
            self.assertIn('Missing manifest references', run.stderr)


if __name__ == '__main__':
    unittest.main()
