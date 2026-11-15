# VTuber Production Quality Gates and Evidence Matrix

Applies to AI-assisted 2D Live2D/VTube Studio and 3D/VRM pipelines. This is a **reusable test specification**, not a report that a particular model passed. Pair with [AI_PRODUCTION_RESEARCH_2026.md](AI_PRODUCTION_RESEARCH_2026.md), [BUILD_PLAYBOOK.md](BUILD_PLAYBOOK.md), and the active project's case study.

> **Tool result boundary:** repository unit tests can only validate their implemented checks. In particular, valid JSON and correct PNG/MOC magic bytes do **not** establish valid model geometry or importability. For real compiled models use available [Cubism SDK integrity checks](https://docs.live2d.com/en/cubism-sdk-manual/moc3-consistency/) and then the actual target app. See [START_HERE_AGENT.md](START_HERE_AGENT.md) for stage statuses and [LIVE2D_EXECUTION_RUNBOOK.md](LIVE2D_EXECUTION_RUNBOOK.md) for hands-on steps.

> **Real binary requirement:** checking `.moc3` magic bytes, a PNG CRC, and JSON file references is necessary but not sufficient for model validity. Before certifying an export, run the official [MOC3 Consistency Checker](https://docs.live2d.com/en/cubism-editor-manual/moc3-consistency-checker/) or supported Cubism Core integrity check, and record the result for the actual export. See [REAL_PRODUCTION_VALIDATION.md](REAL_PRODUCTION_VALIDATION.md). Treat this check as a distinct gate from tracking/visual tests.

## Gate 0 — Intake / permissions / reproducibility

- [ ] Target format, **exact target runtime/version**, platform (PC/mobile) and target crop are stated.
- [ ] Original artwork/project is immutable, with filenames, dimensions, file sizes, SHA-256 and backed-up version.
- [ ] User authorized any **new visual design** or hidden-anatomy reconstruction; commercial license / model weights / asset provenance reviewed where applicable.
- [ ] Separate **editor sources**, **generated derivatives**, **runtime exports**, **preview evidence**.
- [ ] Actual installed software and available tools confirmed; runtime access not assumed.
- [ ] Model budget stated (atlas/polygons/number of textures/device). No fabricated device benchmarks.

**STOP** if source rights/identity, project scope, or target version is unresolved.

## Gate 1 — Identity and artwork

| ID | Test | Evidence | Pass condition |
| --- | --- | --- | --- |
| A01 | Compare face/hair/garment identity against *approved reference* | Original and candidate aligned images at native scale | No unapproved color, shape, costume, iris or hairstyle changes |
| A02 | Layer completeness and order (2D) | Layer tree + neutral overlay preview | All *required* independently moving parts exist; holes behind eyelids/mouth/head/hair are reconstructed with approval |
| A03 | Head feature underpaint (2D) | Base head only, then overlays on/off | No original eyes/mouth duplicated under animated meshes |
| A04 | Alpha edge QA (2D) | Light/dark background previews at 100%, 200%, target stream crop | No visually significant halos, jagged seams, accidental transparent leaks |
| A05 | Artwork and atlas proportion | Pixel bounds + UV atlas overlay | No stretched sample regions, incorrect width/height UV normalizations or wrong-source mouth pixels |
| A06 | Face readability in stream scene | Target crop screenshot | Expression and mouth states can be distinguished at intended size |

**Special fallback:** if only a flattened PNG exists, record absent layers and cap the accepted motion requirements accordingly. Never label this a fully layered premium production model without new art.

## Gate 2A — 2D ArtMeshes, parameter/keyform coverage

| ID | Test | Evidence | Pass condition |
| --- | --- | --- | --- |
| R01 | Mesh topology | Mesh preview per component + validator | No unintended slivers, disconnected islands, transparent-gap bridges; enough topology at eyelids, lips, hair edges |
| R02 | Parameter contract | All IDs, minimum/default/maximum and consumers | Unique intended IDs; every physics/motion/expression reference resolves and values stay in allowed ranges |
| R03 | UV and atlas | Atlas metadata + numerical UV check | Each UV in [0,1], correct non-square denominator, expected source region and orientation |
| R04 | Angle X/Y/Z extremes | Images for min/default/max | Face identity preserved, no forehead/neck seams, clipping, texture stretches or implausible perspective |
| R05 | X/Y diagonal corners | **3×3 pose grid** across min/zero/max combinations | No edge fractures, wrong draw order or interpolation discontinuities at diagonals |
| R06 | Eyes | Both eyes open, 25%, 50%, 75%, shut, independent blink | No double eye, iris leak, unwanted eyelash jump, hair covering suddenly disappears |
| R07 | Mouth | Closed, 25%, 50%, 75%, open, smile/frown+talk combinations | No patch seams, incorrect sampled content, jaw snapping or mouth cavitation |
| R08 | Expressions | Preview each and combinations with blink/talk | Distinct, readable, controlled parameter interaction; return neutral with no stuck value |
| R09 | Physics/secondary motion | Simulated slow and quick turns + idle; runtime video | Stable damping; hair/scarf respond naturally; do not distort face or continue oscillating unbounded |
| R10 | Motion ownership | Parameter writer map: tracker / physics / idle / action / expressions | No undocumented ownership conflict; one-shot motions return control to tracker |

**Notes:** automatic ArtMesh is a *starting point*, and official Cubism recommends manual eyelash/mouth refinement. Facial auto-generation is semi-automatic and front-face constrained. Motion/physics visual QA is not validated by JSON syntax alone.

## Gate 2B — 3D geometry, rig and VRM (only when 3D chosen)

| ID | Test | Evidence | Pass condition |
| --- | --- | --- | --- |
| D01 | Geometry/topology | Front/side/back wireframes, normals report | Stable, deformation-friendly face joints and complete intended rear surfaces; no crucial missing body parts |
| D02 | Skin weights | Pose screenshots: shoulder, elbow, knee, neck, finger where present | No severe collapse, unexpected influence or persistent skin/clothing penetration |
| D03 | UV/materials | UV view and textured turntable | No broken islands, obvious texture seam/color mismatch, or wrong MToon/material behavior in target app |
| D04 | Humanoid / rest pose | Skeleton report + calibration screenshot | Required bones mapped, expected scale and correct T/rest pose |
| D05 | Expressions / lip-sync / gaze | Full blendshape/expression tests, eye look-around | Symmetric blink, distinct expressions and mouth states, no corrupt morphs |
| D06 | SpringBone/collision | Quick head turns, hair/cloth collision test | No runaway oscillation or clipping through face/body |
| D07 | VRM version and license metadata | Exporter+runtime versions, spec metadata report | Compatible target VRM 0.x/1.0 and authorized model use; **do not** assume VSeeFace can load VRM1 |

## Gate 3 — Export / static validation

- [ ] Live2D: `.model3.json` syntax and links to existing `.moc3`, PNG textures, physics/expressions/motions; exact case-sensitive paths after ZIP extraction.
- [ ] Live2D: MOC3 parser/version compatibility with target app where testable; parameter and ArtMesh counts in manifest; no orphaned or unsafe paths.
- [ ] Live2D: motion segment time ranges, curves, fade metadata and parameter references; physics group names/IDs, outputs, weights, norms, FPS.
- [ ] 3D: VRM version supported by **specific** runtime; glTF/VRM validates; humanoid/expression metadata present; springBone and license fields appropriate.
- [ ] Asset count and atlas/texture memory documented. Report *measured* sizes, not a marketing “4K/8K” label.
- [ ] Deterministic clean rebuild from source and scripts where technically feasible; compare exported file hashes. Where non-determinism is expected, document which outputs differ and why.
- [ ] Validate release ZIP after **fresh extraction** to a different directory, not only the workspace.

**Static validation is not visual or runtime proof.**

## Gate 4 — Visual regression and actual app testing

### Minimum 2D pose capture set

```
neutral
AngleX = {min, 0, max} x AngleY = {min, 0, max}    # 9 combinations
AngleZ = {min, 0, max} at neutral XY
eyeL/eyeR = {0, .25, .5, .75, 1}
mouthOpen = {0, .25, .5, .75, 1}
mouthForm = {min, 0, max} with mouthOpen={0,.5,1}
gaze = left/right/up/down/neutral
all selected expression hotkeys with neutral/blink/talk
hair/scarf motion at rest, slow turn, rapid turn, settle
```

**Visual evidence:** a contact sheet and short before/after clip at the target stream crop. Attach each failure screenshot to an issue or report with a pose/parameter label. Manual visual inspection is required even if image-diff scripts run.

### Minimum runtime recording protocol

1. Record runtime name/version, OS, device/CPU/GPU, camera/tracker, project/export version, scene resolution and relevant settings.
2. Import freshly extracted release package into **the requested app**. Capture success/failure/logs.
3. Record **at least 15–20 seconds** of neutral, slow and fast left/right and up/down head motion, blink and partial blink, talking with mouth closed/open, hair sway and one-shot expression/action returning to neutral. Extend if testing full-body tracking or many expressions.
4. Examine normal, exaggerated and combined expressions at close-up and target stream size. Note tracker latency or calibration differences.
5. Record **observed in-app FPS** under representative streaming load if visible (and relevant CPU/GPU/memory) rather than guessing. Set project-specific target; a hypothetical 30 steady / 60 preferred is not a universal spec.
6. Confirm idle/action/physics are coherent during simultaneous tracking and that hotkeys do not break parameter ownership.
7. Mark unexecuted tests as **NOT RUN**, not PASS.

## Gate 5 — Release acceptance / severity

| Severity | Examples | Release handling |
| --- | --- | --- |
| **Blocker** | Broken import, missing texture, wrong VRM version, source rights issue, severe face double-render, package cannot load | Do not release as ready |
| **Major** | Consistent head/neck gap, mouth/eye clipping, broken physics/parameter, unreadable expressions | Fix and repeat affected tests before “high quality” claim |
| **Minor** | Small non-central seam at rare extreme, subtle timing tweak, optional expression polish | Log explicitly; decide with requester |
| **Not tested** | Target app absent, no webcam, no phone, device benchmarks unavailable | State exact limitation and user-side test steps; never label as passed |

**Suggested internal rating (not a sourced industry standard):** identity 20%; source/layer quality 20%; deformation/expression 25%; physics/motion 10%; runtime integration 15%; package/reproducibility 10%. Treat any blocker as a hard fail irrespective of score. This score is an optional review aid, **never a substitute for the detailed acceptance tests**.

## Reusable report template

```yaml
project: "<name>"
version: "<version>"
date_utc: "<ISO-8601>"
route: "live2d | vrm"
target_application: "<app + version>"
editable_sources: ["..."]
source_sha256: {"path": "hash"}
changes: ["..."]
source_licensed_for_proposed_use: "yes | no | unknown"
artifact_files: ["..."]
counts:
  meshes: null
  parameters: null
  expressions: null
  physics_groups: null
  motions: null
  textures: null
tests:
  static: {passed: 0, failed: 0, not_run: 0, evidence: "path"}
  visual: {passed: 0, failed: 0, not_run: 0, evidence: "path"}
  runtime: {passed: 0, failed: 0, not_run: 0, evidence: "path"}
environment: {os: null, app: null, gpu: null, tracker: null, observed_fps: null}
blockers: []
known_limitations: []
next_required_test: "<one concrete test>"
```

Counts in this template are **placeholders**; never publish a report retaining zeros that falsely imply executed tests.

## Official technical sources

- [Live2D import PSD](https://docs.live2d.com/en/cubism-editor-manual/psd-import/)
- [Live2D automatic mesh](https://docs.live2d.com/en/cubism-editor-manual/mesh-edit/)
- [Live2D facial motion auto-generation](https://docs.live2d.com/en/cubism-editor-manual/face-auto-edit/)
- [Live2D standard parameters](https://docs.live2d.com/en/cubism-editor-manual/standard-parameter-list/)
- [Live2D physics](https://docs.live2d.com/en/cubism-editor-manual/physics-operation/)
- [VTube Studio loading models](https://github.com/DenchiSoft/VTubeStudio/wiki/Loading-your-own-Models)
- [VRM 1.0 specification](https://github.com/vrm-c/vrm-specification/blob/master/specification/VRMC_vrm-1.0/README.md)
- [VRM license metadata](https://github.com/vrm-c/vrm-specification/blob/master/specification/VRMC_vrm-1.0/meta.md)
