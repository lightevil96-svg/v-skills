# VTuber Failure Recovery, Limitations, and Honest Reporting

This guide is required for any production agent that encounters missing source art, tool limitations, broken rigging, invalid packages or failed target-app import. Use [START_HERE_AGENT.md](START_HERE_AGENT.md) and [LIVE2D_EXECUTION_RUNBOOK.md](LIVE2D_EXECUTION_RUNBOOK.md) as the primary procedures. Do not treat this as proof a failing user model was inspected.

## Decision tree (start here)

```text
User asks only for skill/docs?
  YES -> change authorized docs only; do NOT touch/query model files.
  NO  -> model/diagnostic task authorized?
         NO  -> identify scope and do safe read-only analysis.
         YES -> do actual file inventory + hashes. Is a source model/art present?
                NO -> report exact missing input, no invented files.
                YES -> target VTube Studio?
                       NO -> choose compatible 3D/other pipeline, never feed VRM to VTS.
                       YES -> is there genuine editable .cmo3 OR proper layer PSD?
                              YES -> can run compatible Cubism Editor authoring/export?
                                     YES -> perform full runbook, save project, export, QA.
                                     NO  -> preserve art/analysis and mark author/export NOT RUN.
                              NO  -> compiled .moc3 + model3 + textures present?
                                     YES -> inspect/repackage/runtime test only.
                                     NO  -> flattened illustration?
                                            YES -> art/occlusion plan, obtain permission for missing layers.
                                            NO  -> BLOCKED; list actual missing assets.
```

## Failure matrix: specific diagnosis and remedy

| Symptom | Likely causes to INVESTIGATE (not a diagnosis without evidence) | Evidence to collect | Safe next action |
| --- | --- | --- | --- |
| PSD won't import / parts merged | improperly prepared PSD layers, unsupported blend mode or layer masks, import constraints/version | source layer tree and Cubism error log/screenshots | preserve material PSD; prepare a separate merged-per-part import PSD following official instructions; retry in correct version |
| No .cmo3 source and only .moc3 | compiled file, source never supplied | archive inventory and exact headers | treat rig as **not natively editable**; request true .cmo3 or rebuild/retouch with approved original layers; **don't pretend conversion** |
| Only flattened PNG, requested premium X/Y head movement | no separate surfaces / hidden pixels, face underpaint absent | input image, layer count, target pose requirements | propose approved new art and layered reconstruction; or clearly cap to limited 2.5D |
| Face shows two eyes/mouths on blink | baked base face has original pixels plus dynamic overlays | render base face with overlays disabled, closed and half-closed state | remove/reconstruct base-face original feature while preserving occluding fringe; rebuild aligned patches |
| Mouth contains eyes/scarf/random pixels | wrong atlas UV, wrong sample map or incorrect texture region | atlas image overlay, mesh/UV mapping and normalized coordinates | locate texture source region and atlas dims; fix sampling, verify neutral/open/half-open states |
| Transparent black/white fringe | straight-vs-premultiplied alpha resampling or matte mismatch | close-ups on dark/light background at display size | repair alpha workflow and patch edges without changing identity |
| Hair/face/neck detached at angles | wrong parenting, bad deformer coverage or missing underpaint | X/Y 3×3 poses, hierarchy screenshot | fix transform hierarchy and occlusion; do not just hide gap with overlay |
| Blink/eyes look wrong with X/Y | independent meshes not following head deformers, incomplete diagonal forms | eye open/half/closed × 3×3 pose matrix | align parent transforms, revise keyforms/occlusion |
| Physics shakes / never settles | overlapping parameter writers, normalization/chain direction, FPS setup | input/output IDs and actual video over slow/fast turns | choose one authoritative output writer, correct range and damping, test under actual FPS |
| Facial expressions snap/stick | motion/expression parameter ownership conflict or missing return | sequence test before/after hotkey | define priority, restore defaults, test in actual runtime |
| `.model3.json` exists but VTS model absent | nested wrong folder, missing MOC3/texture, invalid references, unsupported export version, broken binary | file tree, JSON refs, real VTS log and app version | check actual model root under Live2DModels and exported SDK version; re-export via real Cubism |
| Valid JSON/package but VTS crashes | bad compiled MOC, memory-pressure textures, app incompatibility, native runtime issue | app/device/OS version, textures, logs | reduce resource usage only on test copy, re-export with supported Cubism version; test actual app |
| `.vtube.json` missing on first install | app hasn't imported/generated VTS configuration yet | actual model folder and VTS logs | let VTube Studio start and create it; don't fabricate undocumented schema |
| Texture is sharp in preview but bad on stream | face too small, poor source sampling or lossy screen capture | native and stream-cropped comparison | tune atlas/art/stream scale; AI upscaling is optional and needs identity QA |
| 3D VRM won't load in 2D VTube Studio | category mismatch | file extension + target app | use a compatible 3D program or produce a distinct genuine Live2D model |
| VRM fails in chosen 3D tracker | version 0.x/1.0 mismatch, skeleton/material/expression incompatibility | exporter version and exact app's support doc/log | pick supported VRM version and validate in real target application |
| Test script says PASS with fake files | test confirms structure only, contents never parsed by runtime | source of test fixture, checks performed | label **structural-only PASS**, not model-valid or render-tested |

## Triaging order for reproducibility

1. **Reproduce** with actual input and record tool/app/OS versions, exact error, minimal offending pose, file checksum.
2. **Separate evidence tiers:** file inventory → JSON syntax/reference verification → PNG/binary file inspection → static mesh/UV/parameter QA → visual screenshots → Cubism preview → actual VTS runtime.
3. Isolate the smallest suspected cause; keep before/after screenshot and changed-file list.
4. Repair **only** authorized derivatives; keep original and provide rollback. Do not upload private art to any external generative service without permission.
5. Re-run both the failed test and the immediately affected neighboring tests (e.g. mouth fix requires eyes/bangs and X/Y checks).
6. Report exact pass/fail/NOT RUN; do not convert "file opens" into "streaming quality proven".

## Real boundaries of an AI agent

**Knowledge and text-writing access:** can create plans, code proposals, QA, repo documentation; cannot itself operate the user's installed Cubism Editor without an app/computer interaction tool.

**General-purpose image generation:** produces rendered pixels, **not** layered PSD with validated part names/hidden surfaces, Cubism deformer/keyforms, a .cmo3 model or valid MOC3 exporter. Creating a static concept cannot meet a request for a functional Live2D rig.

**Local Python/image code:** can crop, mask, composite, inspect ZIP and validate manifest paths. It cannot **automatically guarantee** visually correct anatomy, matching eyes or realistic mouth motion from a single flat picture.

**Cubism Editor GUI available:** can make authoring operations (depending on available interaction, license, and installed version); AI must still check actual saved project and generated runtime outputs.

**VTube Studio absent:** cannot certify runtime import, real face tracking, app hotkeys, GPU performance or voice lip-sync. Mark those as NOT RUN.

**Commercial distribution:** do not assume model assets, AI model weights, source art or third-party presets are commercially redistributable. Review applicable licenses and get authorization.

## If work cannot be finished

Produce a **partial deliverable with proof**. Example:

```text
STATUS: BLOCKED AT G2 — RIG AUTHORING
INPUT VERIFIED: face.png, 1024×1536, sha256 ...
DONE: source inventory, approved visible layer plan, underpaint issue list, static part preview
NOT RUN: Cubism import and .cmo3 save (Cubism Editor unavailable)
NOT RUN: real .moc3 export / VTube Studio import
NEEDED: compatible Cubism Editor access and/or user-approved missing eye/jaw artwork
NEXT ACTION: open prepared import PSD in Cubism, save .cmo3, capture angle/eyelid proof
```

A transparent, useful partial result is superior to invented complete models or fabricated test counts.

## Official documentation

- [Live2D file types](https://docs.live2d.com/en/cubism-editor-manual/file-type-and-extension/)
- [Live2D export for runtime](https://docs.live2d.com/en/cubism-editor-manual/export-moc3-motion3-files/)
- [Live2D PSD preparation](https://docs.live2d.com/en/cubism-editor-manual/reimport-psd/)
- [Live2D PSD import](https://docs.live2d.com/en/cubism-editor-manual/psd-import/)
- [VTube Studio loading models](https://github.com/DenchiSoft/VTubeStudio/wiki/Loading-your-own-Models)
- [Cubism FREE/PRO comparison](https://www.live2d.com/en/cubism/comparison/)

**Applies as of 2026-11-15.** This is researched guidance; no specific OrangeScarf or Hiyori binary was tested for this document.
