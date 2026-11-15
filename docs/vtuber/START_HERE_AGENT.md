# START HERE — VTuber Production Agent (v1, 2026-11-15)

> **This is the mandatory entry point for a fresh AI agent.** Reading this repository does NOT provide artwork, a Cubism authoring engine, a VTube Studio installation, a webcam, or permission to change a user's model. Follow the instructions in order. If a dependency is unavailable, complete only verifiable preparatory work and report the gate as blocked / NOT RUN.

> **Read-only preflight helper:** [preflight.py](../../scripts/vtuber/preflight.py) can inventory file suffixes and detect user-supplied editor executable paths, not prove GUI/model validity. The [Real Production Validation](REAL_PRODUCTION_VALIDATION.md) protocol is mandatory before asserting stream-ready results. Cold-start comprehension requires independently recorded [evaluation cases](../../evals/agent_cases.json), not a self-assigned score.

## 0. Five-minute orientation

1. Read `skills/vtuber-model-builder/SKILL.md` first, then this page.
2. Read `docs/vtuber/LIVE2D_EXECUTION_RUNBOOK.md` if target is Live2D/VTube Studio, or `docs/vtuber/VRM_3D_EXECUTION_RUNBOOK.md` for a 3D/VRM target.
3. Read `docs/vtuber/PRODUCTION_QA_MATRIX.md`, and the model-specific case study **only if it matches the model being worked on**. OrangeScarf is a historical example, not generic input or implied permission.
4. Inspect **the actual attachments/working directory**. Never pretend a repository knowledge base contains PSD, .cmo3, or the model ZIP if it has only markdown and scripts.
5. Check the capabilities and permissions matrix below before making any change.

## 1. What completion really means

| Status to report | Required evidence | Do not call it |
| --- | --- | --- |
| **Concept** | Approved/reference artwork and style identity | Rigged model |
| **Art-ready** | Separately editable **material separation** source and flattened-per-part Cubism import PSD; visible parts and hidden overlap illustrated | Finished .cmo3 |
| **Rig-authored** | REAL editable Cubism .cmo3 saved by a compatible authoring tool, with parameter/deformer hierarchy, expression/physics examples and pose screenshots | Deployable runtime model |
| **Runtime-exported** | REAL .moc3 exported by Cubism, .model3.json and referenced texture/physics/etc files; valid static file checks | Proven VTube Studio-compatible |
| **App-imported** | Evidence the actual model folder opens inside real VTube Studio on target platform/version | Fully tested model |
| **Stream-ready** | Actual in-app tracking + blink/mouth + diagonal + expression + physics + representative stream crop/performance acceptance | Any other earlier stage |

**Never report a stronger status than evidence proves.** Unknown and not tested are not the same as passed. If no Cubism Editor or equivalent supported creation/export tool is accessible, a finished native `.cmo3`/`.moc3` is NOT an achievable deliverable in that environment by merely writing JSON/Python. Do **not** fabricate a binary. Cubism SDK/Core loads/uses exported models; it is not the native authoring interface for producing a polished editable model from scratch. A tool claiming to generate valid MOC3 must be separately validated for legal/technical compatibility; never infer it from file suffix.

## 2. User intent and scope gate

First decide what was requested:

- **Skill/docs-only:** edit only authorized skill/repository documentation. Do **not** request or modify model ZIP as a prerequisite.
- **Inspect/diagnose:** read files and report fact/inference, without overwriting originals.
- **Build/repair model:** changes to model derivatives are authorized only within the named scope; any re-design, previously unseen anatomy, external AI upload, destructive overwrite, or disclosure needs separate approval.
- **Package:** repack **a model that already exists**; do not pretend repackaging creates meshes/artwork/rigging.
- **Runtime validate:** only mark tested when the actual target application was used.

When safe progress is possible, continue with inventory, docs, validation and a bounded plan rather than stopping for nonessential preferences.

## 3. First response / handoff contract

Write a compact technical contract before editing:

```yaml
task: "<exact task>"
scope: ["<allowed files / assets>"]
do_not_touch: ["<originals / unrelated repo / unspecified model>"]
target: {format: "Live2D | VRM", app: "VTube Studio | other", app_version: "unknown", platform: "unknown"}
source: {path: "<actual discovered path | unavailable>", type: "layered-PSD | cmo3 | flattened | compiled-only | other", hash_sha256: "<value | not computed>"}
software_available: {cubism_editor: "yes | no | unknown", vtube_studio: "yes | no | unknown"}
rights: {artwork: "confirmed | unknown", external_ai_upload: "authorized | not authorized"}
deliverables: ["<named source/export/report>"]
acceptance_tests: ["<measurable evidence>"]
blocked_items: ["<reason + evidence + needed dependency>"]
```

Never fill an unknown field with an invented value or silently declare authorization.

## 4. Capability and output decision table

| Inputs & tools actually available | Legitimate next action | Highest defensible status without more access |
| --- | --- | --- |
| **Only this repository** | Review knowledge, create scoped runbook/script, identify target tool and requirements | **Instructions prepared** (not a VTuber model) |
| Only flattened PNG + Python | Audit pixels; optionally segment visible regions; prepare approved derivative art/PSD candidates, QA reports | Concept/art preparation, **not production-grade rig** |
| Proper layered PSD + **Cubism Editor GUI accessible** | Execute [Live2D runbook](LIVE2D_EXECUTION_RUNBOOK.md), save genuine .cmo3, export real .moc3 | Rig-authored, then runtime-exported once verified |
| Real .cmo3 and compatible Cubism Editor | Continue rigging, physics, motions, export, static checks | Runtime-exported after real export |
| .moc3 + model3 + textures, **no .cmo3** | Inspect/repackage; configure VTube Studio; possible runtime use | App-imported / stream-ready only if in-app tests performed; **not natively editable rig** |
| .model3.json without .moc3 or referenced textures | Report missing dependencies; no fake exports | **Blocked** |
| Valid package + no VTube Studio available | Structural tests and close-up previews if a real renderer is available; user-side import protocol | Runtime-exported; runtime **NOT RUN** |
| Blender/VRoid plus approved 3D source | Run 3D pipeline; determine VRM target version and licensing | 3D exported, then app-tested if verified |

**Critical source distinctions:** .cmo3 is editable Cubism modeling source; .can3 animation source; .moc3 is compiled runtime model; .model3.json is a reference manifest; a PSD alone is not an authored rig. VRM is not a Live2D/VTube Studio substitute.

## 5. Core workflow and gates

| Gate | Required work | Evidence to advance | Fail behavior |
| --- | --- | --- | --- |
| G0: INPUT | inventory and hash originals; verify target and rights | real file list and permission | **BLOCKED** when essential input/rights absent |
| G1: ART | identity guide, layer map, occlusion/underpaint, Cubism-ready PSD | inspection at native + stream crop; source preserved | iterate approved artwork; flattened art cannot invent correct hidden parts |
| G2: RIG | import PSD, real ArtMeshes/deformers, parameter keyforms and combinations | genuine .cmo3 saved + 3×3 angles, eye/mouth pose previews | mark rig authoring **NOT RUN** if no GUI/tool |
| G3: DYNAMICS | expressions, lip-open/form, physics and optional actions | actual Cubism previews, input/output IDs and timing | report failed combination, do not hide |
| G4: EXPORT | export from real Cubism, model3 manifest, textures; clean package | real MOC3 + existing relative refs; static checks | report invalid/missing files |
| G5: APP | import in real VTube Studio and map tracking | real app import / setup evidence | mark **NOT RUN** if app unavailable |
| G6: STREAM | test tracker, blink, talk, expressions, physics, stream-scale and performance | screenshots/video/logs, user acceptance if required | keep status as App-imported or below |

**Quality rule:** no arbitrary scores such as “100% premium” without actual reference comparison and runtime evidence. G0–G4 cannot be promoted to G5 by a successful Python unit test. See [QA matrix](PRODUCTION_QA_MATRIX.md) and [failure diagnostics](TROUBLESHOOTING_AND_LIMITS.md).

## 6. Output deliverables (2D)

Deliver **two separated packages** only if the underlying source actually exists:

```text
<name>_development_vN/
  originals/                  # untouched + checksum manifest
  <name>_material_separation.psd  # if actually produced
  <name>_import.psd               # if actually produced
  <name>.cmo3                     # only if saved by Cubism / verified compatible authoring tool
  build-notes.md
  test-evidence/
<name>_vts_vN/
  <name>.model3.json           # actual exported filenames
  <name>.moc3
  <texture-subfolder>/...      # exact manifest paths
  [other manifest-linked files]
  [optional vts sidecar / icon]
```

The paths above are an output **contract**, not a claim files exist. Never create empty fake files to fill the template. Repackager [script](../../scripts/vtuber/repack_vts.py) is for existing valid model asset sets; it is NOT a rig constructor. Release ZIP should contain one discoverable model folder; development source and reports stay outside VTS install root.

## 7. Verification and stop rule

Deliver a final report with separate sections for `INSPECTED`, `CREATED`, `STATIC PASS/FAIL/NOT RUN`, `VISUAL PASS/FAIL/NOT RUN`, `RUNTIME PASS/FAIL/NOT RUN`, `BLOCKERS`, and `NEXT ACTION`. Use real file paths and screenshots, never guessed names. Stop only the blocked action, not all safe permitted work; state precisely what outside tool/artwork is required. If user asks to update skills only, stop at skill documentation and do not seek model files.

## 8. Primary authoritative references

- [Live2D file formats](https://docs.live2d.com/en/cubism-editor-manual/file-type-and-extension/)
- [Live2D exporting runtime files](https://docs.live2d.com/en/cubism-editor-manual/export-moc3-motion3-files/)
- [Live2D preparing PSDs](https://docs.live2d.com/en/cubism-editor-manual/reimport-psd/) and [PSD import](https://docs.live2d.com/en/cubism-editor-manual/psd-import/)
- [VTube Studio model import](https://github.com/DenchiSoft/VTubeStudio/wiki/Loading-your-own-Models)
- [Cubism FREE vs PRO limitations](https://www.live2d.com/en/cubism/comparison/)
- [Prompt-master agentic patterns](https://github.com/nidhinjs/prompt-master)

**Last reviewed:** 2026-11-15. Recheck current tool versions before future use.
