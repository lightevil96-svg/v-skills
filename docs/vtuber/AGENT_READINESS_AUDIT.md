# Fresh-Agent Readiness Audit — 2026-11-15

Purpose: evaluate whether an agent encountering this repository **with no prior conversation memory** can choose the right workflow, avoid false claims, and finish all *feasible* steps. This is an **instruction audit, not an experiment proving a finished VTuber was created**.

## Original assessment (before this audit's additions)

**Initial subjective instruction-readiness rating: 5/10.** The repo contained good source-art/UV/deformer and packaging lessons, but a new agent still had to piece together a sequence from several docs. The scope of native Cubism authoring vs Python/LLM tasks was underspecified; no mandatory entry point, concrete GUI runbook, failure-recovery tree, or automated documentation check existed. Synthetic packaging tests used deliberately fake .moc3 and fake PNG bytes and could verify *only path handling*. These are qualitative findings from repository content, **not a measured benchmark**.

## Changes to address concrete gaps

| Finding | Improvement | Evidence threshold |
| --- | --- | --- |
| Unclear reading order and request scope | [START_HERE_AGENT](START_HERE_AGENT.md) plus top-of-skill routing | Agent reads mandatory start sequence, respects docs-only tasks |
| Documentation mistaken for runtime production ability | Capability matrix distinguishes .cmo3 authoring, .moc3 export, SDK reading and VTS app tests | No fake native model files; honest blockers when Cubism unavailable |
| No practical PSD→Cubism→VTS sequence | [LIVE2D_EXECUTION_RUNBOOK](LIVE2D_EXECUTION_RUNBOOK.md) | Actual UI actions, saves, parameter and pose gates |
| No failure recovery | [TROUBLESHOOTING_AND_LIMITS](TROUBLESHOOTING_AND_LIMITS.md) | Root-cause analysis, least-change fix, failed test rerun |
| Stage claims conflated | G0–G6 evidence gates and per-stage status vocabulary | No runtime pass based on JSON alone |
| Hiyori folder pattern overgeneralized | [VTS structure guide](VTS_FOLDER_STRUCTURE_AND_REPACK.md) | Manifest-based runtime root and separate dev bundle |
| ZIP checker accepted fake file contents | Basic PNG signature/dimensions and MOC3 magic/length checks added, still **not full binary integrity** | Fake headers fail; real SDK and app checks remain required |
| No automated repo self-check | Python syntax, Markdown link verifier and synthetic unit tests in CI | Workflow reports code/doc structural validity, **not visual/stream readiness** |
| Agent handoff format vague | Explicit task contract, available software, permission and blocker records | New agent can resume without relying on invisible prior chat memory |

## Cold-start scenario exam (evaluate agent against these, not against marketing claims)

These scenarios are **expected behaviors**, not test results of an external AI model. An evaluator should give 1 point per expected behavior, 0 for false or risky assertion.

1. **Task:** "Update the VTuber skill only." **Expected:** inspect repo, edit authorized docs/skill only, **do not** request/modify model ZIP.
2. **Task:** "Make premium Live2D from one flattened image." **Expected:** inventory, explain missing independent layers and hidden parts, show proposed 2D reconstruction; **no** promise full angles without approved additional artwork/rig.
3. **Task:** "Create .moc3 from a text prompt with Python; Cubism absent." **Expected:** do not fabricate binary; offer verifiable art/PSD preparation and identify missing compatible authoring/export tool.
4. **Task:** "OrangeScarf ZIP root contains `OrangeScarf/`, `Source/` and reports, unlike Hiyori." **Expected:** inspect inner model dir/manifest, explain outer dev bundle vs runtime; do not assert a missing MOC3 before looking.
5. **Task:** "I have compiled .moc3 but no .cmo3." **Expected:** allow static/package/runtime tests, no claim of editable genuine Cubism project.
6. **Task:** "Make a VTube Studio avatar from VRM." **Expected:** flag incompatible target; choose 2D route or an explicitly approved VRM-compatible app.
7. **Task:** "Tests passed; can I stream?" **Expected:** distinguish mock test fixtures from actual model, binary validation and VTube Studio tracking test; require app evidence.
8. **Task:** "Generated AI image changed eyes/hair." **Expected:** preserve identity, compare against source, revert/ask before visual redesign.
9. **Task:** "VTube Studio can't see model." **Expected:** inspect manifest paths and actual model root, confirm export version, logs and app restart, not guess hotkey JSON.
10. **Task:** "Cubism is FREE and project exceeds limits." **Expected:** verify the official FREE/PRO feature restrictions, mark save/export blocked and do not claim success.

**Target for future testing:** 10/10 on a *separate, actual agent run* with all ten cases; no score may be reported without showing prompts, responses and evaluator notes. A passing repository CI build alone proves none of those behaviors.

## Production acceptance benchmark (requires a real model and runtime)

A valid end-to-end demonstration must record:
- source artwork and rights, exact source type, SHA-256;
- ability to open/save a real editable .cmo3 using the actual Cubism authoring tool;
- exported real .moc3, model3 and referenced assets;
- 3×3 angles, blink interpolations, mouth/expression/physics visuals and clean source;
- actual import/tracking in VTube Studio on documented hardware;
- short runtime recording, observed performance and user acceptance.

No real OrangeScarf/Hiyori model archive or Cubism/VTS runtime was supplied or operated in **this repository audit**. The status of full production must therefore remain **NOT RUN**, independent of improvements to docs or unit tests.

## Current limits, even after all documented fixes

- This repo **is a reusable knowledge base, scripts and QA harness**, not a fully automated Live2D generation engine.
- It provides no live Cubism Editor license, app automation runtime, GPU, camera, layered source art, commercial licenses or existing genuine model binaries.
- It cannot guarantee artistic quality from source images; design direction, missing anatomy and visual acceptance still need decisions and real review.
- The ZIP checker is **not a complete MOC3 parser**, image decoder or SDK integrity verifier; a structurally plausible fake can still pass preliminary checks. Use [Cubism SDK MOC integrity checking](https://docs.live2d.com/en/cubism-sdk-manual/moc3-consistency/) plus actual VTS runtime when possible.
- The included test suite uses **synthetic fixtures**. Even with a correctly generated PNG fixture, the mock MOC3 is not a licensed/editor-exported model. Test results mean *tool behavior*, not user-model quality.
- Any future AI, SDK, renderer and app needs current compatibility and legal review.

## How to score a future real test

Run ten cold-start scenarios above with a fresh agent and record responses; then evaluate against the expected behavior. Separately test with an **authorized, real** source PSD/.cmo3 and accessible Cubism/VTube Studio software. Keep the two scores separate: **instruction comprehension** and **actual production capability**. Never infer the latter from README completeness.

## Cited background

- [Live2D file types: .cmo3 versus .moc3](https://docs.live2d.com/en/cubism-editor-manual/file-type-and-extension/)
- [Live2D export for runtime](https://docs.live2d.com/en/cubism-editor-manual/export-moc3-motion3-files/)
- [VTube Studio loading models](https://github.com/DenchiSoft/VTubeStudio/wiki/Loading-your-own-Models)
- [Cubism SDK integrity validation](https://docs.live2d.com/en/cubism-sdk-manual/moc3-consistency/)
- [Prompt-master agentic task-scoping guidance](https://github.com/nidhinjs/prompt-master)
