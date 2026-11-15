# VTube Studio Folder Structure: Hiyori vs OrangeScarf

**Status:** 2026-11-15. Based on the **user-supplied folder listings**, official VTube Studio guidance and Live2D model3 specifications. **Neither OrangeScarf ZIP nor hiyori_vts ZIP has been supplied to this workspace**; the underlying OrangeScarf model files and actual import behavior remain **NOT INSPECTED / NOT TESTED**. Do not claim the original ZIP was fixed.

> **Fresh-agent requirement:** Follow [START_HERE_AGENT.md](START_HERE_AGENT.md) and [LIVE2D_EXECUTION_RUNBOOK.md](LIVE2D_EXECUTION_RUNBOOK.md) to distinguish valid package layout from source/rig creation. The ZIP repacker now checks light-weight `.moc3`/PNG signatures, but still **cannot** establish MOC3 integrity or actual VTube Studio import.

## 1. What the comparison actually proves

| User-visible package level | OrangeScarf_V... | hiyori_vts | Diagnosis |
| --- | --- | --- | --- |
| Top-level model assets | A child directory named `OrangeScarf` | `hiyori.model3.json`, `hiyori.moc3`, texture directory and physics visible | **Different level being displayed.** A parent bundle with a nested valid model folder is not inherently broken; verify inside `OrangeScarf/` |
| Extra development material | `Source/`, `BACA_DULU.txt`, `BUILD_REPORT.txt`, `Face_Integration_Preview.png`, `verification.json` appear at outer level | No equivalent material listed | Source/build artifacts should be distributed separately from the *installable model folder* |
| Animations/expressions | Unknown inside child model folder | `animations/`, `expressions/` | Optional; presence must be confirmed against `.model3.json` references |
| `.cdi3.json` and `.vtube.json` | Unknown | Seen in Hiyori | `.cdi3.json` is **not needed** by VTS. VTS can create the `.vtube.json` sidecar on import; neither is a universal prerequisite for a first import |
| `items_pinned_to_model.json` | Unknown | Seen in Hiyori | Optional VTS state, not a core Live2D model file |

User-supplied names were copied from a mobile file view; text such as `http://hiyori.moc3` / `http://verification.json` is **not sufficient proof that `http://` is part of the actual file name**. Inspect actual ZIP entry names before making such a claim.

**Important distinction:** A ZIP with `OrangeScarf/` and `Source/` at its top level may be fine as a *development bundle*. You install the **inner OrangeScarf folder** when that folder itself contains the required files. A ZIP is a convenience; its root is not itself the model root.

## 2. Recommended outputs: two deliberately separate packages

### A. VTube Studio runtime release (only this folder goes into Live2DModels)

```text
OrangeScarf_vts/
├── OrangeScarf.model3.json              # REQUIRED index; located here
├── OrangeScarf.moc3                     # REQUIRED and referenced in model3
├── OrangeScarf.physics3.json            # if used; reference explicitly
├── OrangeScarf.2048/                    # name ONLY if model3 actually references it
│   └── texture_00.png
├── animations/                          # optional; registered .motion3.json
│   └── Idle.motion3.json
├── expressions/                         # optional; registered .exp3.json
├── OrangeScarf.cdi3.json                # optional
├── OrangeScarf.vtube.json               # optional; VTS may generate
├── items_pinned_to_model.json           # optional
└── icon.png                             # strongly recommended 512×512
```

`OrangeScarf.2048`, `texture_00.png`, filenames and optional motion file above are **illustrative placeholders**, not a verified listing of the actual OrangeScarf archive. Retain **the exact filenames referenced** by the real model manifest, even when they differ from Hiyori.

### B. Development / reproducibility bundle (NOT to be installed into Live2DModels)

```text
OrangeScarf_dev/
├── Source/                               # immutable reference, scripts, PSD, .cmo3 if present
├── BACA_DULU.txt
├── BUILD_REPORT.txt
├── Face_Integration_Preview.png
├── verification.json
└── OrangeScarf_vts.zip                  # separately validated installation archive
```

Do not add fictitious `.cmo3`/PSD source files if the original source is a flattened PNG, as recorded in the OrangeScarf case study. Do not treat `.moc3` as editable `.cmo3`.

## 3. The manifest determines the real structure, not the Hiyori naming convention

`OrangeScarf.model3.json` includes a `FileReferences` object such as:

```json
{
  "Version": 3,
  "FileReferences": {
    "Moc": "OrangeScarf.moc3",
    "Textures": ["OrangeScarf.2048/texture_00.png"],
    "Physics": "OrangeScarf.physics3.json",
    "Motions": {"Idle": [{"File": "animations/Idle.motion3.json"}]}
  }
}
```

**EXAMPLE ONLY.** Verify the real manifest before copying, moving, or renaming anything. All paths are relative to the directory of `.model3.json`; moving assets without updating those paths breaks loading. Case-sensitive paths and nonempty referenced texture files must resolve. Physics/expressions/motions are not obligatory unless the user requires those features or the manifest references them.

The **VTube Studio folder** must hold the root model index and all referenced assets. Subfolders for texture/animations/expressions are fine, and the model directory itself is installed under VTube Studio's `StreamingAssets/Live2DModels/`. Use the in-app open-models-folder route rather than guessing OS-specific absolute paths.

## 4. Safe automatic packaging tool

Use **[scripts/vtuber/repack_vts.py](../../scripts/vtuber/repack_vts.py)** (Python 3.9+, standard library only).

```bash
# 1. Diagnose input without changing anything:
python scripts/vtuber/repack_vts.py "OrangeScarf_V0.4.zip" --inspect

# 2. Build a runtime-only ZIP, keeping original archive untouched:
python scripts/vtuber/repack_vts.py "OrangeScarf_V0.4.zip" \
  --output "OrangeScarf_VTS.zip" \
  --folder-name "OrangeScarf_vts"

# 3. List ZIP entries to visually verify it:
python -m zipfile -l "OrangeScarf_VTS.zip"
```

Tool behavior:
- Detects **exactly one** `.model3.json` inside source folder or ZIP and identifies that file's parent as the model root. Multiple models cause an explicit failure rather than silently choosing the wrong one.
- Validates the JSON and verifies references for MOC3, texture(s), physics when registered, expressions, motions, pose, display info and user data. **Missing assets stop the build**; no fake files are synthesized.
- Copies the model root into a ZIP with **one** `OrangeScarf_vts/` folder at top level. This makes a clear installable folder regardless of the parent build-bundle structure.
- Omits outer-level source/docs/reports automatically. Also omits well-known build folders/files if they sit within the selected model root. All other files within the model root are preserved to avoid deleting VTube Studio sidecar or custom assets.
- Rejects path traversal, absolute/URL-like paths, symlinks and duplicate/archive-collision problems; refuses to overwrite an existing output ZIP.
- Reopens the new ZIP and validates the model references again. **This is static validation only, not proof of Cubism/VTube Studio runtime loading or rig correctness.**

**Important limitations:** The script does **not** change the PNG artwork, re-rig the character, convert an invalid MOC3, create missing physics/texture files, repair incorrect parameter IDs, or guarantee that a valid-JSON model renders properly. If a manifest references assets outside the model directory using `../`, the tool **fails deliberately** instead of silently restructuring them. Fix the model source/export or obtain required missing assets separately.

## 5. End-to-end release acceptance checklist

- [ ] ZIP contains exactly **one** runtime root folder; development files do not appear beside the model.
- [ ] Root folder contains a real `.model3.json` and referenced `.moc3`, plus all referenced textures.
- [ ] Physics/expressions/motions included and referenced **if the model uses them**.
- [ ] Real filenames and case match JSON; relative paths resolve after extracting to a new directory.
- [ ] **Source files retained in development archive**, not lost when building runtime ZIP.
- [ ] Real output ZIP passes `--inspect`; note that valid JSON does not certify the MOC binary parses.
- [ ] Install extracted runtime folder directly under `StreamingAssets/Live2DModels/`; restart app if imported while running.
- [ ] Test actual tracking, blink, talk, head rotation, physics, motions and frame performance in VTube Studio. Log app/device version and failures separately.
- [ ] Mark unperformed app tests **NOT RUN**, never **PASS**.

## 6. Existing OrangeScarf evidence (must not be upgraded without a real test)

Existing case study records **v0.4: MOC3 version 3, 11 parameters, 8 ArtMeshes, 2048×4096 atlas, 9 motion files, 227 passed static checks and zero static failures**. These describe previous reported static results; **they do not show the actual source ZIP's file hierarchy and do not prove VTube Studio opened the release**. See [ORANGESCARF_CASE_STUDY.md](ORANGESCARF_CASE_STUDY.md).

## Official references (consulted 2026-11-15)

- [VTube Studio: Loading your own models](https://github.com/DenchiSoft/VTubeStudio/wiki/Loading-your-own-Models) — model folder, required primary files, optional expressions/animations, optional display info, icons.
- [VTube Studio: Getting started](https://github.com/DenchiSoft/VTubeStudio/wiki/Getting-Started) — `Live2DModels` installation, restart after import.
- [Live2D CubismSpecs: model3.json](https://github.com/Live2D/CubismSpecs/blob/master/FileFormats/model3.json.md) — FileReferences as *relative paths*.
- [Live2D file types](https://docs.live2d.com/en/cubism-editor-manual/file-type-and-extension/) — editor `.cmo3` vs runtime `.moc3`/manifest roles.

## Evidence status

**VERIFIED:** published documentation, current V Skills docs, synthetic **unit tests added** for packaging and missing-path rejection; CI status must be checked before claiming any tests passed, and GitHub docs updates. **NOT VERIFIED:** original OrangeScarf and Hiyori ZIP content, user-side installer import, texture rendering or tracking. Once the original ZIP is available, execute the script on those **actual bytes**, record file paths and hashes, and update the case study.
