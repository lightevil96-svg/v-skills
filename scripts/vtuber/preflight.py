#!/usr/bin/env python3
"""Read-only VTuber input and toolchain preflight. Does not create or validate a model.

Example:
  python scripts/vtuber/preflight.py --source /path/to/project.zip --target live2d
  python scripts/vtuber/preflight.py --source ./character.psd --cubism-exe /path/to/CubismEditor

Only verifies file names and optional executable path existence, NOT license,
GUI operability, art layers, binary validity, or stream-readiness.
"""
import argparse
import hashlib
import json
import sys
import zipfile
from pathlib import Path

MAX_NAMES = 5000
KNOWN = {".psd": "psd", ".cmo3": "cmo3", ".moc3": "moc3", ".model3.json": "model3",
         ".vroid": "vroid", ".blend": "blend", ".vrm": "vrm", ".png": "png"}


def classify(name):
    lower = name.lower()
    if lower.endswith(".model3.json"):
        return "model3"
    return KNOWN.get(Path(name).suffix.lower(), "other")


def list_names(path):
    if path.is_file() and zipfile.is_zipfile(path):
        with zipfile.ZipFile(path) as z:
            names = [info.filename for info in z.infolist() if not info.is_dir()]
    elif path.is_dir():
        names = [p.relative_to(path).as_posix() for p in path.rglob("*") if p.is_file()]
    elif path.is_file():
        names = [path.name]
    else:
        raise ValueError(f"Source does not exist: {path}")
    if len(names) > MAX_NAMES:
        raise ValueError(f"Too many input files to inspect safely: {len(names)}")
    return names


def digest(path):
    if not path.is_file():
        return None
    sha = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1048576), b""):
            sha.update(chunk)
    return sha.hexdigest()


def executable_hint(value):
    if not value:
        return {"path": None, "exists": False, "executable_tested": False, "gui_tested": False}
    path = Path(value).expanduser()
    return {"path": str(path), "exists": path.is_file(), "executable_tested": False, "gui_tested": False}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--target", choices=("live2d", "vrm"), default="live2d")
    parser.add_argument("--cubism-exe")
    parser.add_argument("--vtube-exe")
    parser.add_argument("--blender-exe")
    parser.add_argument("--vroid-exe")
    args = parser.parse_args()
    names = list_names(args.source)
    found = {kind: sorted(n for n in names if classify(n) == kind)
             for kind in ("psd", "cmo3", "moc3", "model3", "vroid", "blend", "vrm", "png")}
    tools = {
        "cubism": executable_hint(args.cubism_exe), "vtube_studio": executable_hint(args.vtube_exe),
        "blender": executable_hint(args.blender_exe), "vroid_studio": executable_hint(args.vroid_exe)
    }
    warnings = []
    if args.target == "live2d":
        if not found["cmo3"] and not found["psd"]:
            warnings.append("No native .cmo3 or layered .psd found; authoring from flat art may need approved new layers.")
        if not tools["cubism"]["exists"]:
            warnings.append("Cubism Editor executable not supplied/found. Native Live2D authoring/export NOT RUN.")
        if found["model3"] and not found["moc3"]:
            warnings.append("Model manifest present without a visible .moc3; inspect missing exports.")
        if not tools["vtube_studio"]["exists"]:
            warnings.append("VTube Studio app executable not supplied/found. Real runtime test NOT RUN.")
    else:
        if not (found["blend"] or found["vroid"]):
            warnings.append("No native .blend/.vroid 3D editor source detected.")
        if not (tools["blender"]["exists"] or tools["vroid_studio"]["exists"]):
            warnings.append("No 3D editor executable supplied/found. 3D authoring/export NOT RUN.")
    report = {
        "target": args.target, "source": str(args.source),
        "source_sha256_if_file": digest(args.source), "file_count": len(names),
        "found_by_extension_only": found, "provided_executable_paths": tools,
        "source_license_verified": False, "actual_editor_operability_tested": False,
        "actual_export_verified": False, "actual_runtime_tested": False,
        "warnings": warnings, "status": "PREFLIGHT_ONLY",
    }
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (ValueError, OSError, zipfile.BadZipFile) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        sys.exit(2)
