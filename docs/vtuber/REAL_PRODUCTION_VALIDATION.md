# Real-model proof protocol — from "well documented" to actually stream-ready

**Read [START HERE](START_HERE_AGENT.md).** This is an evidence collection procedure, not a claim that the repository contains a finished VTuber or that this audit ran native applications.

## Why 10/10 cannot be awarded by writing more markdown

A model-production skill is demonstrated on **previously unseen artwork** in a real environment. A polished instruction set may remove ambiguity, but a full-quality claim requires: 1) genuinely editable source art, 2) a compatible authoring application, 3) real compiled export, 4) runtime integration and 5) visual quality assessment at target streaming scale. This repository currently contains **none** of the user's art, proprietary native editor/runtime binaries, or new end-to-end demonstration evidence. All tests in CI are Python/Markdown/synthetic fixtures.

The **claim ladder is strict**:

1. **Knowledge ready:** documented task routing, target tools and acceptance matrix.
2. **Art ready:** real, authorized, editable separated parts; hidden regions approved; PSD import tested.
3. **Rig authored:** authentic `.cmo3` saved by Cubism, verified deformers and parameter extremes.
4. **Compiled:** genuine exported `.moc3`, manifest and textures, integrity tested with official checker/SDK.
5. **App imported:** fresh extracted model folder loaded in real VTube Studio, confirmed by log/video.
6. **Stream ready:** tracker, blinking, mouth, expressions, physics, mixed poses, performance, and final visual acceptance.

No script can promote an artifact from (1) to (3) by changing an extension.

## Required external tools and permissions

| Dependency | Acquisition / requirement | Proof it actually works |
| --- | --- | --- |
| Editable source art and rights | Commissioned/original PSD/CLIP, .cmo3, or a user-authorized reconstruction from flat image | Inspected layer tree + identity agreement, file hashes |
| Live2D Cubism Editor GUI (modeling/export) | Obtain authorized supported build/license from [Live2D](https://www.live2d.com/en/cubism/) and check [FREE/PRO limitations](https://www.live2d.com/en/cubism/comparison/) | Screenshot of actual editor importing PSD, saving native .cmo3 and exporting MOC3 |
| MOC3 integrity test | [Official MOC3 Consistency Checker](https://docs.live2d.com/en/cubism-editor-manual/moc3-consistency-checker/) or Cubism Core `csmHasMocConsistency` ([docs](https://docs.live2d.com/en/cubism-sdk-manual/moc3-consistency/)) | Logged checker result for **the actual exported binary**, version/size/hash recorded |
| VTube Studio | Obtain actual app from [official VTube Studio guide](https://github.com/DenchiSoft/VTubeStudio/wiki/Loading-your-own-Models) | App version, import video/log, tracker/expressions working |
| Camera/tracker and stream scene | Working device and user-approved tracking setup | Tracker calibration and practical stream-scale capture |
| AI assistance (optional) | Text/code tools or legally permitted local segmentation/upscaling | Original-vs-candidate preview; no unauthorized data upload |

If you only have GitHub/text/Python, you can **prepare** but cannot certify native rig/export/tracking. Do not automate external application interaction without a real supported computer interface.

## Reproducible trial using a real model

- **1. Fresh task:** give a new agent a brand-new authorized character source and a target app/hardware brief; **do not** give private prior chat context.
- **2. Inspect and plan:** record real source paths, hashes, permissions, tool availability; classify 2D vs VRM.
- **3. Art gate:** produce genuine layer map, material-separated source, import PSD, and before/after visual evidence. Stop if missing hidden art is unapproved.
- **4. Rig gate:** operate actual Cubism Editor, save native .cmo3, capture 3×3 AngleX/Y, eye open/partial/closed, mouth open/form, hair and neck seam evidence. If Cubism cannot run, mark not run.
- **5. Export gate:** export compiled MOC3/textures/manifests with real app. Use official [MOC3 consistency checker](https://docs.live2d.com/en/cubism-editor-manual/moc3-consistency-checker/) and [SDK integrity verification](https://docs.live2d.com/en/cubism-sdk-manual/moc3-consistency/). Use this repo's repacker **only** for safe structural packaging, never as binary validator.
- **6. App gate:** extract the runtime folder to VTube Studio's actual Live2DModels directory. Import and record logs/app version.
- **7. Tracking gate:** record neutral, X/Y/Z head turn including diagonals, independent blink, voice mouth, expressions while speaking, hair physics, one-shots, and FPS in a representative streaming scene. Screen-capture at least 15–20 seconds; include failed poses if any.
- **8. Release gate:** hand off separate editable source and runtime package, report actual file hashes, tracked bugs and limitations. Require user visual approval, no severe artifacts, no unresolved blockers.

For each gate use the [QA matrix](PRODUCTION_QA_MATRIX.md). A pass on a synthetic fixture or header/PNG CRC check **never** substitutes for items 4–7.

## Evidence form (copy into a project-specific file; do not fill with guesses)

```yaml
character: NOT_SET
source_artifact: NOT_SET
source_rights: UNKNOWN
source_sha256: NOT_COMPUTED
model_editor: {name: "Live2D Cubism", version: UNKNOWN, native_cmo3_saved: NOT_RUN}
moc3_export: {real_export: NOT_RUN, actual_filename: UNKNOWN, sha256: NOT_COMPUTED}
moc3_integrity: {tool: "MOC3 Consistency Checker / Cubism SDK", result: NOT_RUN, log_path: UNKNOWN}
manifest: {references_verified: NOT_RUN, zip_fresh_extraction_checked: NOT_RUN}
visual: {pose_grid: NOT_RUN, blink: NOT_RUN, mouth: NOT_RUN, physics: NOT_RUN, screenshots: []}
runtime: {app: "VTube Studio", app_version: UNKNOWN, import: NOT_RUN, tracking: NOT_RUN, video: UNKNOWN, observed_fps: UNKNOWN}
user_acceptance: NOT_RUN
blockers: []
final_stage: KNOWLEDGE_ONLY
```

**Do not convert UNKNOWN to PASS or zero into success.** A genuine 10/10 project-quality claim is not possible until independent reviewers have inspected the actual results.

## Validation failure response

If a test fails, save a failure artifact and root-cause note, fix only the authorized derivative, repeat the test and adjacent impacted poses, and only then update status. On missing permissions/software, deliver a useful partial result and an exact next action.

**Official references:** [Cubism runtime export](https://docs.live2d.com/en/cubism-editor-manual/export-moc3-motion3-files/), [MOC3 checker](https://docs.live2d.com/en/cubism-editor-manual/moc3-consistency-checker/), [SDK integrity check](https://docs.live2d.com/en/cubism-sdk-manual/moc3-consistency/), [VTube Studio import](https://github.com/DenchiSoft/VTubeStudio/wiki/Loading-your-own-Models).
