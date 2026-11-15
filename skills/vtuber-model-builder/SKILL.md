---
name: vtuber-model-builder
description: Build, repair, rig, animate, package, and validate Live2D/VTube Studio character models while preserving the user's original design and project constraints.
---

# VTuber Model Builder

## READ FIRST — mandatory fresh-agent start sequence

**Do not begin by generating files.** Read [START_HERE_AGENT.md](../../docs/vtuber/START_HERE_AGENT.md), then choose the [Live2D execution runbook](../../docs/vtuber/LIVE2D_EXECUTION_RUNBOOK.md) when VTube Studio is the target, or use the [3D/VRM execution runbook](../../docs/vtuber/VRM_3D_EXECUTION_RUNBOOK.md) for a compatible 3D app; read [Troubleshooting and Limitations](../../docs/vtuber/TROUBLESHOOTING_AND_LIMITS.md) on any blocker, and apply [Production QA Matrix](../../docs/vtuber/PRODUCTION_QA_MATRIX.md). The [Agent Readiness Audit](../../docs/vtuber/AGENT_READINESS_AUDIT.md) contains adversarial cold-start scenarios and unproven areas.

1. **Intent and permission:** determine whether requested output is skill/docs-only, inspection, source artwork, Cubism rig, packaging or real app test; do not act outside that stage. A docs-only request must **never** trigger edits or demands for the user's model.
2. **Current state:** inventory actual supplied files, source type, dimensions/hashes, app target, available editor/license/GUI and rights. This repo itself contains instructions and scripts; **do not pretend it contains model binaries or the user's assets**.
3. **Tool and format gate:** for Live2D, a genuine editable `.cmo3` is authored/saved by Cubism or a demonstrated compatible authoring tool; a `.moc3` must originate from a working exporter. Python manifest/ZIP scripts **cannot create real rig deformations by naming a file .moc3**. Cubism SDK consumption is not equivalent to an authoring workflow. If editor/exporter unavailable, stop at verified art/static preparation and mark native export **NOT RUN**.
4. **Stage gates:** concept → editable separated art → genuine `.cmo3`/rig → genuine exported `.moc3`/model3/textures → actual VTube Studio import → streaming tracking/QA. No stage can be promoted without its own evidence.
5. **Partial completion:** if a dependency is missing, still deliver safe, verifiable authorized work; report `DONE`, `BLOCKED`, `STATIC`, `VISUAL`, `RUNTIME NOT RUN`, and the next exact action. No guessed paths, passing tests, model scores or fake binary files.
6. **Original and environment preservation:** no destructive writes, unauthorized redesign, unseen anatomy synthesis, or external art upload. Keep identity and references canonical, development and runtime releases separate.

## Extended research and test standards

**Token-efficient reading:** always read this skill + [START HERE](../../docs/vtuber/START_HERE_AGENT.md) and **one** route-specific runbook (2D or 3D). Consult the relevant sections of [AI Production Research](../../docs/vtuber/AI_PRODUCTION_RESEARCH_2026.md), [Production QA Matrix](../../docs/vtuber/PRODUCTION_QA_MATRIX.md), [Build Playbook](../../docs/vtuber/BUILD_PLAYBOOK.md), and a model case study **only when the task needs them**. Avoid loading unrelated 3D documentation for a 2D task or OrangeScarf notes for a different character. The [AI Production Agent Prompt](../../prompts/VTUBER_AI_PRODUCTION_AGENT.md) is optional reusable orchestration, not a substitute for actual file inspection and software availability.

- Select **Live2D for VTube Studio**; VRM/3D needs a compatible 3D runtime. VRM 0.x and 1.0 support differs across applications.
- AI-assisted face generation in Cubism is **semi-automatic** and documented for front-facing source faces; manually verify diagonals, feature occlusion and expressive keyforms.
- Image segmentation and generative inpainting never automatically establish missing hidden geometry/anatomy or permission to alter the character.
- AI upscaling, AI mesh generation, exported files and static validators are candidates/partial evidence, **not proof** of visual correctness, licensing or app runtime success.
- Apply the QA matrix release gates: identity, layers, mesh/UV, parameters, pose grid, expressions, physics, package, actual target app and measured performance; explicitly mark unavailable runtime tests NOT RUN.

## Objective readiness and real-model evidence

- For any new model task, use the **read-only** [toolchain/input preflight](../../scripts/vtuber/preflight.py) when files are available. File-extension discovery or a supplied editor executable path **does not prove** that the editor operates or that a file is a legitimate Cubism export.
- The skill has **12 cold-start behavior challenges** in [agent_cases.json](../../evals/agent_cases.json). The [review worksheet CLI](../../scripts/vtuber/evaluate_agent_cases.py) records independent evaluations, but does not judge responses semantically and cannot substitute for a new agent actually running those prompts.
- To report *stream-ready* model production, follow [Real Production Validation](../../docs/vtuber/REAL_PRODUCTION_VALIDATION.md) and use official [MOC3 Consistency Checker](https://docs.live2d.com/en/cubism-editor-manual/moc3-consistency-checker/) or SDK integrity checks on **the real exported MOC3**, plus actual VTube Studio import/tracking and user visual acceptance.
- Do not claim a **10/10 completion** based on documentation, file suffixes, code unit tests, syntax/lint success or manual self-scoring. Keep comprehension, structural CI, native authoring, runtime, and aesthetics separate. Mark every unexecuted gate NOT RUN and state the missing dependency.

## Release claim attestation (non-negotiable)

Before announcing that a real model is `ART_READY`, `RIG_AUTHORED`, `RUNTIME_EXPORTED`, `APP_IMPORTED` or `STREAM_READY`, collect and review source/editor/runtime evidence using [Real Production Validation](../../docs/vtuber/REAL_PRODUCTION_VALIDATION.md). A conservative [evidence validator](../../scripts/vtuber/validate_release_evidence.py) can check file hashes, status prerequisites and local provenance records, but **cannot independently prove a claim is true**. Do not claim 10/10, even if its JSON checks pass, until independent fresh-agent testing, a real Cubism/VRM production trial, actual app tracking and visual approval exist. When unavailable, report the maximum **verified** milestone and mark later stages `NOT_RUN`.

When packaging a real VTS model under explicit permission, use the [runtime repacker](../../scripts/vtuber/repack_vts.py) only after reviewing its **source-file and private-data exclusion policy**. Never package credential files, PSD/.cmo3, unknown binary assets or sensitive source materials into a runtime release by default; unknown file extensions require review, not silent inclusion. Report excluded files and stop on referenced forbidden assets rather than forging paths.

## Mission

Produce a stable, visually coherent, responsive VTuber model. Treat the artwork, mesh, parameters, physics, motions, VTube Studio configuration, and package as one system. Do not optimize one layer while silently breaking another.

## Mandatory VTube Studio packaging and folder structure policy

**Task-scope gate (highest priority):** If the user requests a **skill, prompt, or knowledge-base correction only**, edit **only the explicitly requested documentation/skill file(s)**. Never modify, rebuild, repackage, upload, rename, or request the actual model as a prerequisite. Explain the correct principles and provide reusable checks, but report model-file inspection, model ZIP generation, and runtime tests as **NOT RUN**. Only perform model operations if explicitly requested in a later task.

Before evaluating a user model, read [VTube Studio Folder Structure & Repack](../../docs/vtuber/VTS_FOLDER_STRUCTURE_AND_REPACK.md). Distinguish **the outer distribution/development ZIP** from **the actual installable model directory**. A bundle containing `OrangeScarf/`, `Source/` and reports is **not automatically invalid**: first inspect the content of `OrangeScarf/`; the actual folder containing `*.model3.json` defines the model root. Do not infer that missing files at the outer ZIP level are missing from the nested model.

### Expected runtime folder (illustrative, not fixed filenames)

```text
<Character_vts>/                      # this folder is placed under Live2DModels/
  <Character>.model3.json             # primary model manifest, required
  <Character>.moc3                    # compiled Live2D model referenced by manifest
  <Character>.2048/texture_00.png     # example ONLY; use the manifest's actual texture paths
  <Character>.physics3.json           # only when model uses/references it
  animations/*.motion3.json           # only when model uses/references them
  expressions/*.exp3.json             # only when model uses/references them
  <Character>.cdi3.json               # optional Cubism display-info file
  <Character>.vtube.json              # optional VTube Studio sidecar
  icon.png                            # recommended, name/format depends on application
  items_pinned_to_model.json          # optional VTube Studio state
```

The example does **not** mean every subfolder/file must exist, or that every texture atlas must be named `.2048`. Consult `FileReferences` in **the model's own** `.model3.json`; preserve exact filenames, case, nested paths and relative references. Do not fabricate missing assets to imitate another model (e.g. Hiyori), and do not blindly flatten subdirectories.

Keep **development-only** artifacts (original art, layered PSD/.cmo3, `Source/`, `BACA_DULU.txt`, `BUILD_REPORT.txt`, `Face_Integration_Preview.png`, `verification.json`, source scripts, build logs) in a **separate development bundle**, not mixed into the runtime model folder. A runtime ZIP may contain a single top-level model directory; the parent release bundle may also contain sources and reports as long as install instructions clearly identify the actual model folder.

### Validation only when package inspection/build is authorized

1. Discover all `*.model3.json` files. Require the intended model's identity to be unambiguous; do not silently choose between multiple models.
2. Parse `FileReferences`, confirm the actual relative `Moc` and every `Textures` path, and verify every referenced physics, expression, motion, sound or other asset exists with correct case; do not require optional files unless referenced or explicitly requested.
3. Check for collisions, path traversal, wrong nesting, unsupported extensions, damaged archives, and obviously irrelevant build artifacts in the runtime directory.
4. If explicitly asked for a clean release ZIP, preserve originals, package only the model directory (using [repack_vts.py](../../scripts/vtuber/repack_vts.py) **if its assumptions fit the inspected input**), and then verify the freshly extracted output. The script performs **static structural checks only**; it does not prove the MOC3 renders, check animations visually, or certify runtime compatibility.
5. **Actual VTube Studio import/tracking:** only claim success after testing in the real target app; otherwise state **NOT RUN**. Follow the existing physics, expression, motion and performance QA gates.

**Evidence boundary:** Filenames shown in a smartphone file browser (including apparent `http://` prefixes) may be display artifacts. Do not treat them as actual filenames without inspecting ZIP entries. Preserve a distinction between **user-described listing**, **inspected files**, **inferred issue**, **static validation** and **runtime test**.

## ChatGPT native image generation policy (mandatory)

When **ChatGPT** is the executing agent and the user explicitly requests or authorizes **new or edited VTuber artwork as an image deliverable** (e.g., concept art, reference sheet, expression illustration, a drawn texture or approved image edit), use **ChatGPT's built-in Generate Image capability** (the available native image-generation tool, commonly `image_gen`) as the **first and default image generator/editor**.

- **Do not use external AI image generators** (Midjourney, Leonardo AI, external Stable Diffusion/ComfyUI servers, third-party image-generation APIs/websites, etc.) as a substitute. Do not send references/artwork to outside generation services or use external accounts, paid credits or API keys. An exception requires the user's **separate, explicit authorization** and an available permitted tool; otherwise remain on the native path.
- **Do not switch silently:** if ChatGPT's native image tool is unavailable or cannot satisfy the requested image format, state the limitation and stop that image-generation step. Continue only permitted non-generative work; do not invent a finished image.
- **Do not generate unrequested images:** documentation-only work, model file inspection, rig configuration and requests for machine-readable/editable files do not alone authorize a supporting illustration. When a request spans model creation and artwork, determine whether the user actually requested or authorized the **image component** before invoking it.
- **Keep source identity and rights:** preserve originals, follow the user's reference/style requirements, compare outputs with approved design, and obtain separate approval before redesigning the character or reconstructing newly exposed hidden anatomy.
- **Respect deliverable types:** native Generate Image produces raster artwork, **not** a guaranteed layered PSD/CLIP, editable Cubism `.cmo3`, valid compiled `.moc3`, rig or animation. Layer separation, redraw/underpaint, mesh deformation, export, and VTube Studio validation remain distinct stages.
- **Non-generative processing remains permitted:** local crop/masking, alpha correction, atlas layout, resizing, UV validation and packaging of already-authorized image assets using Python/Cubism are engineering operations, not an alternative external image generator.

This policy applies specifically to ChatGPT. For an agent running outside ChatGPT, choose only a user-approved available image-generation tool and disclose the difference; never claim access to ChatGPT's native Generate Image when absent.

## Tool selection

- Use container/Python for archive inspection, image processing, code edits, mesh/UV analysis, deterministic builds, and static validation.
- Use the GitHub connector for repository inspection and authorized documentation/code updates.
- For ChatGPT, use its **native Generate Image** for user-requested/authorized artwork; never silently use outside image generators. Do not substitute raster artwork for editable layers, rig structures, or machine-readable model files.
- Use web research for current format specifications or undocumented compatibility questions. Prefer official Live2D/VTube Studio references.
- Treat the target VTube Studio/Cubism runtime as unavailable until an actual app test is performed.

## Intake and project continuity

1. Identify the exact source package and current version. Do not assume a previous ZIP or output is the latest.
2. Inventory files: artwork, PSD/CLIP layers, model3, MOC3, physics3, motion3, textures, expressions, VTube Studio sidecar, icon, source scripts, and licenses.
3. Preserve the original package. Work in a new versioned copy.
4. Record source dimensions, color mode, alpha behavior, file hashes, parameter IDs, mesh IDs, and known runtime constraints.
5. Prefer layered PSD/CLIP or a genuine Cubism project. If only a flattened PNG exists, document the resulting limits before attempting segmentation.

## Build workflow

1. **Artwork QA:** inspect resolution, transparency, edge halos, color fringing, crop boundaries, facial landmarks, and hidden/occluded anatomy.
2. **Layer plan:** define head, hair, face, eyes, mouth, body, scarf, arms, hands, and other parts only when the source supports them. Do not invent hidden anatomy.
3. **Face separation:** if eyes or mouth are separate animated meshes, remove/reconstruct those pixels in the base face first. Keep hair fringe/occlusion in the correct draw order. Use aligned, feathered patches for open/closed states.
4. **Texture atlas:** use alpha-premultiplied resizing/compositing to avoid transparent-edge halos. Keep texture dimensions explicit and normalize UVs with separate width and height for non-square atlases.
5. **Mesh:** create a denser mesh around the face, eyelids, mouth, and silhouette; use lower density in broad stable body areas. Check holes, disconnected islands, long sliver triangles, and mesh bridges.
6. **Parameters/keyforms:** define IDs, ranges, defaults, and keyforms before creating motion/physics references. Keep face parameters independent from unrelated body or hair parameters.
7. **Physics:** use plausible chain direction, stable roots, normalized inputs, correct output ranges, and a tested FPS setting. Avoid having motion files and physics compete for the same parameter unless priority is intentional.
8. **Motion:** create smooth, bounded curves for idle and user-triggered actions. Restore parameters to neutral at the end of one-shot motions.
9. **VTube Studio package:** verify relative paths, model3 references, physics, icon, sidecar configuration, and motion files. Configure hotkeys through the VTube Studio UI unless the exact configuration schema is verified.
10. **Validation:** run static checks, compare before/after previews, test deterministic rebuilds, then import into VTube Studio/Cubism on the target device.

## Non-negotiable scope controls

- Do not redesign the character or replace the artwork unless explicitly requested.
- Do not silently add new parts, effects, tracking behavior, or backend dependencies.
- Keep the original package untouched and create a rollback path.
- Never fabricate file paths, hotkey schemas, runtime results, or compatibility claims.
- Ask before destructive changes, publishing assets, or modifying unrelated repository content.
- For a skill-only request, confine writes to the requested skill documentation. Do not repair a model or alter helper scripts/test files unless specifically authorized.
- Stop and report the blocker if the source cannot support the requested movement without new artwork/layers.

## Acceptance criteria

- Facial features do not double-render between base artwork and overlays.
- Open/closed eyes and mouth states remain aligned at neutral and animated poses.
- Hair/fringe occlusion remains correct during blinking and head turns.
- Texture edges show no visible dark fringe, jagged clipping, or alpha halos at the intended display scale.
- Every UV is within [0,1] and mapped against the actual atlas width/height.
- All model3 file references resolve.
- Motion curves reference existing parameters and remain inside parameter ranges.
- Physics inputs, weights, normalization, chain direction, and output IDs are valid.
- Rebuild output is deterministic where the toolchain permits.
- Runtime success is claimed only after loading and testing in the target app.

## Evidence and reporting

For every version, report:
- exact files changed;
- original assets preserved or modified;
- mesh/parameter/texture/motion counts;
- validation checks passed/failed;
- reproducibility result;
- visual preview evidence;
- what has and has not been tested in VTube Studio/Cubism;
- remaining limitations and the next user-side test.

Record reusable lessons in the currently authorized skill/documentation scope. Update case studies, playbooks, scripts or model binaries **only when the user explicitly authorizes those files**.
