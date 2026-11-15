#!/usr/bin/env python3
"""Validate and repackage ONE Live2D model into a clean VTube Studio ZIP.

Examples:
  python scripts/vtuber/repack_vts.py OrangeScarf_V0.4.zip --output OrangeScarf_VTS.zip
  python scripts/vtuber/repack_vts.py OrangeScarf_V0.4/ --inspect

This never creates .moc3, repairs broken JSON, modifies originals, or
claims successful VTube Studio import. Requires Python >=3.9, stdlib only.
"""
import argparse
import json
import re
import stat
import struct
import zlib
import sys
import zipfile
from pathlib import Path, PurePosixPath

EXCLUDE_TOP_DIRS = {"source", "originals", "working", "source-scripts", "docs", "reports", "previews", "__macosx", ".git"}
EXCLUDE_TOP_FILES = {"baca_dulu.txt", "build_report.txt", "face_integration_preview.png", "verification.json", ".ds_store"}

# Guardrails for untrusted ZIPs. These are conservative resource limits, not VTube Studio requirements.
MAX_ENTRIES = 12000
MAX_SINGLE_FILE = 512 * 1024 * 1024
MAX_TOTAL_FILES = 2 * 1024 * 1024 * 1024
MAX_COMPRESSION_RATIO = 1000

# These are conservative defaults for packaging a VTube Studio runtime directory,
# NOT a claim that these are the only VTS-accepted file types. Unknown files are
# omitted with a warning. Source files/private data are never copied automatically.
RUNTIME_SUFFIXES = (
    ".model3.json", ".moc3", ".physics3.json", ".pose3.json", ".cdi3.json",
    ".userdata3.json", ".motion3.json", ".exp3.json", ".vtube.json",
    ".png", ".jpg", ".jpeg", ".wav", ".ogg", ".mp3", ".json",
)
NEVER_EXPORT_SUFFIXES = (
    ".psd", ".psb", ".clip", ".cmo3", ".can3", ".blend", ".vroid",
    ".zip", ".7z", ".rar", ".py", ".sh", ".bat", ".exe", ".dll", ".pem",
    ".key", ".sqlite", ".db", ".txt", ".md",
)
PRIVATE_NAME_MARKERS = ("secret", "password", "credential", "apikey", "api_key", "private_key", "id_rsa", "access_token")


def validate_file_budget(entries):
    if len(entries) > MAX_ENTRIES:
        raise PackageError(f"Too many files: {len(entries)} > {MAX_ENTRIES}")
    total = 0
    for name, size, compressed in entries:
        if size < 0 or size > MAX_SINGLE_FILE:
            raise PackageError(f"File exceeds safety size limit: {name} ({size})")
        total += size
        if total > MAX_TOTAL_FILES:
            raise PackageError("Total input size exceeds safety limit")
        if compressed is not None and size > 4 * 1024 * 1024 and size / max(1, compressed) > MAX_COMPRESSION_RATIO:
            raise PackageError(f"Suspicious compression ratio (possible ZIP bomb): {name}")



class PackageError(Exception):
    pass


def safe_path(raw):
    """Allow only relative POSIX paths; prohibit URLs, drives and traversal."""
    if not isinstance(raw, str) or not raw or "\\" in raw or "\x00" in raw:
        raise PackageError(f"Unsafe or empty path: {raw!r}")
    if raw.startswith("/") or re.match(r"^[A-Za-z][A-Za-z0-9+.-]*:", raw):
        raise PackageError(f"Absolute, drive, or URL path prohibited: {raw!r}")
    parts = [p for p in raw.split("/") if p not in ("", ".")]
    if not parts or ".." in parts:
        raise PackageError(f"Path traversal/empty path prohibited: {raw!r}")
    return "/".join(parts)


class InputFiles:
    def __init__(self, path):
        self.path = path
        self.zip = None
        self.items = {}
        if path.is_file() and zipfile.is_zipfile(path):
            self.zip = zipfile.ZipFile(path)
            for info in self.zip.infolist():
                name = safe_path(info.filename.rstrip("/"))
                if info.is_dir():
                    continue
                mode = (info.external_attr >> 16) & 0xFFFF
                if stat.S_ISLNK(mode):
                    raise PackageError(f"Symlinks in ZIP are prohibited: {name}")
                if name in self.items:
                    raise PackageError(f"Duplicate filename in ZIP: {name}")
                self.items[name] = info
        elif path.is_dir():
            for item in path.rglob("*"):
                if item.is_symlink():
                    raise PackageError(f"Symlinks in model folder are prohibited: {item}")
                if item.is_file():
                    self.items[safe_path(item.relative_to(path).as_posix())] = item
        else:
            raise PackageError("Input must be a folder or an existing ZIP")
        if not self.items:
            raise PackageError("Input contains no files")
        if self.zip:
            budgets = [(name, item.file_size, item.compress_size) for name, item in self.items.items()]
        else:
            budgets = [(name, item.stat().st_size, None) for name, item in self.items.items()]
        validate_file_budget(budgets)

    def read(self, name):
        item = self.items[name]
        return self.zip.read(item) if self.zip else item.read_bytes()

    def close(self):
        if self.zip:
            self.zip.close()


def refs_in_manifest(data):
    if not isinstance(data, dict) or not isinstance(data.get("FileReferences"), dict):
        raise PackageError("Invalid .model3.json: missing FileReferences object")
    r = data["FileReferences"]
    moc = r.get("Moc")
    textures = r.get("Textures")
    if not isinstance(moc, str) or not isinstance(textures, list) or not textures:
        raise PackageError(".model3.json requires FileReferences.Moc and nonempty Textures")
    refs = [("Moc", moc)]
    for item in textures:
        refs.append(("Textures", item))
    for key in ("Physics", "Pose", "DisplayInfo", "UserData", "MotionSync"):
        if key in r:
            refs.append((key, r[key]))
    if "Expressions" in r:
        if not isinstance(r["Expressions"], list):
            raise PackageError("Expressions must be an array")
        for e in r["Expressions"]:
            if not isinstance(e, dict) or "File" not in e:
                raise PackageError("Expression missing File")
            refs.append(("Expressions", e["File"]))
    if "Motions" in r:
        if not isinstance(r["Motions"], dict):
            raise PackageError("Motions must be an object")
        for group, motions in r["Motions"].items():
            if not isinstance(motions, list):
                raise PackageError(f"Motion group {group} is not an array")
            for m in motions:
                if not isinstance(m, dict) or "File" not in m:
                    raise PackageError(f"Motion group {group} entry missing File")
                refs.append((f"Motions/{group}", m["File"]))
                if "Sound" in m:
                    refs.append((f"Motions/{group}/Sound", m["Sound"]))
    return [(kind, safe_path(value)) for kind, value in refs]


def export_policy(relative_path):
    """Return (include, reason) for a nonreferenced runtime-root file."""
    parts = relative_path.lower().split("/")
    if any(p.startswith(".") or p in EXCLUDE_TOP_DIRS for p in parts):
        return False, "hidden/source directory"
    if any(marker in p for p in parts for marker in PRIVATE_NAME_MARKERS):
        return False, "possible private or credential file"
    if any(relative_path.lower().endswith(suffix) for suffix in NEVER_EXPORT_SUFFIXES):
        return False, "development/non-runtime extension"
    if any(relative_path.lower().endswith(suffix) for suffix in RUNTIME_SUFFIXES):
        return True, "recognized runtime asset"
    return False, "unknown extension (review manually)"


def select_model(files):
    model_indexes = sorted(n for n in files.items if n.endswith(".model3.json"))
    if len(model_indexes) != 1:
        raise PackageError(f"Expected exactly one .model3.json, found {len(model_indexes)}: {model_indexes}")
    index = model_indexes[0]
    root = index.rsplit("/", 1)[0] + "/" if "/" in index else ""
    try:
        manifest = json.loads(files.read(index).decode("utf-8-sig"))
    except (ValueError, UnicodeError) as exc:
        raise PackageError(f"Invalid JSON in {index}: {exc}") from exc
    refs = refs_in_manifest(manifest)
    missing = [(kind, ref) for kind, ref in refs if root + ref not in files.items]
    if missing:
        raise PackageError("Missing manifest references (paths are case-sensitive): " + json.dumps(missing, ensure_ascii=False))
    # Detect collisions on ALL files within the candidate model root, even if
    # filtered later (Windows/macOS often have case-insensitive file systems).
    root_files = [name[len(root):] for name in sorted(files.items) if name.startswith(root)]
    duplicates = {}
    for rel in root_files:
        lower = rel.lower()
        if lower in duplicates:
            raise PackageError(f"Case-insensitive path collision: {duplicates[lower]} vs {rel}")
        duplicates[lower] = rel

    selected = {}
    excluded = []
    warnings = []
    required = {ref for kind, ref in refs}
    required.add(index[len(root):])
    for fullname in sorted(files.items):
        if not fullname.startswith(root):
            continue
        rel = fullname[len(root):]
        top = rel.split("/", 1)[0].lower()
        if not rel or top in EXCLUDE_TOP_DIRS or top in EXCLUDE_TOP_FILES:
            if rel in required:
                raise PackageError(f"Referenced runtime asset is under development-only path: {rel}")
            excluded.append(fullname)
            continue
        allowed, reason = export_policy(rel)
        if not allowed:
            if rel in required:
                raise PackageError(f"Referenced runtime asset violates release policy: {rel} ({reason})")
            excluded.append(fullname)
            warnings.append(f"Excluded {rel}: {reason}")
            continue
        selected[rel] = fullname
    for kind, ref in refs:
        if ref not in selected:
            raise PackageError(f"Referenced {kind} file is excluded from runtime: {ref}")
    if index[len(root):] not in selected:
        raise PackageError("Main model3 file was excluded")
    if "Physics" not in manifest["FileReferences"]:
        warnings.append("Physics is not registered; model may have no physics")
    return index, root, refs, selected, excluded, warnings



def inspect_png_container(data, ref):
    """Check PNG signature, chunk boundaries/CRCs, IHDR, IDAT and IEND.

    This is NOT a complete PNG pixel decoder nor evidence of visual quality.
    """
    signature = b"\x89PNG\r\n\x1a\n"
    if not data.startswith(signature):
        raise PackageError(f"Invalid PNG signature: {ref}")
    offset, width, height, seen_ihdr, seen_idat, seen_iend = 8, None, None, False, False, False
    while offset < len(data):
        if offset + 12 > len(data):
            raise PackageError(f"Truncated PNG chunk header: {ref}")
        chunk_length = struct.unpack(">I", data[offset:offset + 4])[0]
        chunk_type = data[offset + 4:offset + 8]
        end = offset + 12 + chunk_length
        if chunk_length > MAX_SINGLE_FILE or end > len(data):
            raise PackageError(f"Truncated/oversized PNG chunk: {ref}")
        payload = data[offset + 8:offset + 8 + chunk_length]
        stored_crc = struct.unpack(">I", data[offset + 8 + chunk_length:end])[0]
        actual_crc = zlib.crc32(chunk_type + payload) & 0xffffffff
        if stored_crc != actual_crc:
            raise PackageError(f"PNG CRC mismatch: {ref}")
        if not seen_ihdr:
            if chunk_type != b"IHDR" or chunk_length != 13:
                raise PackageError(f"PNG must start with a 13-byte IHDR: {ref}")
            width, height = struct.unpack(">II", payload[:8])
            if not 1 <= width <= 32768 or not 1 <= height <= 32768:
                raise PackageError(f"Invalid PNG dimensions: {ref} ({width}x{height})")
            seen_ihdr = True
        elif chunk_type == b"IHDR":
            raise PackageError(f"Multiple PNG IHDR chunks: {ref}")
        if chunk_type == b"IDAT":
            seen_idat = True
        if chunk_type == b"IEND":
            if chunk_length != 0:
                raise PackageError(f"Invalid PNG IEND: {ref}")
            seen_iend = True
            if end != len(data):
                raise PackageError(f"Trailing bytes after PNG IEND: {ref}")
            break
        offset = end
    if not (seen_ihdr and seen_idat and seen_iend):
        raise PackageError(f"Missing PNG IHDR, IDAT or IEND: {ref}")
    return width, height


def inspect_asset_signatures(files, root, refs):
    """Basic MOC header and PNG container checks, NOT MOC binary integrity or runtime."""
    checked = []
    for kind, ref in refs:
        if kind not in ("Moc", "Textures"):
            continue
        data = files.read(root + ref)
        if kind == "Moc":
            if len(data) < 64 or data[:4] != b"MOC3":
                raise PackageError(f"Invalid MOC3 header/size: {ref}; full Cubism integrity NOT checked")
            checked.append({"kind": "MOC3_header_only", "path": ref, "bytes": len(data)})
        elif kind == "Textures":
            width, height = inspect_png_container(data, ref)
            checked.append({"kind": "PNG_container_crc_only", "path": ref, "width": width, "height": height})
    return checked


def run():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("input", type=Path, help="Folder or ZIP containing exactly one Live2D model")
    ap.add_argument("--inspect", action="store_true", help="Inspect and validate references; do not generate ZIP")
    ap.add_argument("--output", type=Path, help="New ZIP file path for a clean runtime-only model")
    ap.add_argument("--folder-name", help="Name of the model folder inside output ZIP (default: source model folder + _vts)")
    args = ap.parse_args()
    if not args.inspect and args.output is None:
        ap.error("Choose --inspect or --output OUT.zip")
    if args.inspect and args.output:
        ap.error("--inspect and --output cannot be used together")
    files = InputFiles(args.input)
    try:
        index, root, refs, selected, excluded, warnings = select_model(files)
        header_checks = inspect_asset_signatures(files, root, refs)
        name = args.folder_name or ((root.rstrip("/").split("/")[-1] if root else PurePosixPath(index).name.split(".model3.json")[0]) + "_vts")
        if not re.fullmatch(r"[A-Za-z0-9_.-]+", name) or name in (".", ".."):
            raise PackageError("--folder-name must be simple ASCII filename without slashes")
        result = {"model_index": index, "root_in_input": root or ".", "model_folder_for_release": name, "runtime_files": len(selected), "references_checked": len(refs), "excluded_build_files": excluded, "warnings": warnings, "runtime_verified": False, "asset_header_checks": header_checks, "binary_integrity_verified": False}
        if args.output:
            if args.output.suffix.lower() != ".zip":
                raise PackageError("Output must end in .zip")
            if args.output.exists():
                raise PackageError("Output already exists; refusing to overwrite")
            if args.input.resolve() == args.output.resolve():
                raise PackageError("Output cannot be the source")
            args.output.parent.mkdir(parents=True, exist_ok=True)
            try:
                with zipfile.ZipFile(args.output, "x", compression=zipfile.ZIP_DEFLATED, compresslevel=6) as z:
                    for rel, source_path in selected.items():
                        z.writestr(f"{name}/{rel}", files.read(source_path))
                # Reopen output and independently check its manifest references.
                out = InputFiles(args.output)
                try:
                    _, _, out_refs, out_selected, _, _ = select_model(out)
                    inspect_asset_signatures(out, f"{name}/", out_refs)
                    if len(out_refs) != len(refs) or len(out_selected) != len(selected):
                        raise PackageError("Output ZIP verification count mismatch")
                finally:
                    out.close()
            except Exception:
                args.output.unlink(missing_ok=True)
                raise
            result["output_zip"] = str(args.output)
        print(json.dumps(result, indent=2, ensure_ascii=False))
    finally:
        files.close()


if __name__ == "__main__":
    try:
        run()
    except (PackageError, OSError, zipfile.BadZipFile) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        sys.exit(2)
