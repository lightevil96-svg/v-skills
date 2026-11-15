# V Skills

A reusable knowledge base of agent skills, technical playbooks, prompts, and verified project lessons.

## AI agent: start here

**New AI agent? Read [START_HERE_AGENT.md](docs/vtuber/START_HERE_AGENT.md) first.** Then use the [step-by-step Live2D runbook](docs/vtuber/LIVE2D_EXECUTION_RUNBOOK.md) or [3D/VRM runbook](docs/vtuber/VRM_3D_EXECUTION_RUNBOOK.md), [troubleshooting and limitations](docs/vtuber/TROUBLESHOOTING_AND_LIMITS.md), [QA matrix](docs/vtuber/PRODUCTION_QA_MATRIX.md) and [cold-start audit](docs/vtuber/AGENT_READINESS_AUDIT.md). The root skill is [VTuber Model Builder](skills/vtuber-model-builder/SKILL.md).

**Honest promise:** This repo is a knowledge base, prompts and structural packaging checks, **not a one-click professional Live2D authoring engine**. It does not supply a genuine .cmo3, .moc3, layered art, Cubism Editor or real VTube Studio runtime. To finish a high-quality working model the agent needs the actual source artwork, a compatible Cubism authoring/export environment, and in-app testing. Unit tests with synthetic fixtures do NOT certify a real model. For skill-only requests, no model edits should be performed.

### Tooling / self-check

```bash
python -m compileall -q scripts/vtuber tests
python scripts/vtuber/check_skill_links.py
python -m unittest discover -s tests -v
# The following only inspects an actual user-supplied existing Live2D model:
python scripts/vtuber/repack_vts.py INPUT.zip --inspect
```

A passing test means repository Python/link/packaging behavior, **not** the proprietary MOC3's full correctness or VTube Studio compatibility. Use [Cubism SDK consistency verification](https://docs.live2d.com/en/cubism-sdk-manual/moc3-consistency/) and real in-app evidence when possible.

## VTuber / Live2D

- [VTuber Model Builder Skill](skills/vtuber-model-builder/SKILL.md): reusable operating instructions for building, repairing, and validating Live2D/VTube Studio models.
- [AI-Assisted Production Research (2026)](docs/vtuber/AI_PRODUCTION_RESEARCH_2026.md): sourced 2D/3D production routes, AI assistance boundaries, editing and compatibility constraints, licenses, and OrangeScarf experiments.
- [VTube Studio Folder Structure & Repack Guide](docs/vtuber/VTS_FOLDER_STRUCTURE_AND_REPACK.md): OrangeScarf-vs-Hiyori file-level comparison, separate runtime/development bundles, and exact packaging requirements.
- [Safe Runtime ZIP Repacker](scripts/vtuber/repack_vts.py): checks model3 referenced files and emits a clean one-model VTS ZIP (unit tests: [tests/test_repack_vts.py](tests/test_repack_vts.py)).
- [Production QA Matrix](docs/vtuber/PRODUCTION_QA_MATRIX.md): measurable quality gates, pose grids, static validation, target-app runtime evidence, and release decisions.
- [AI Production Agent Prompt](prompts/VTUBER_AI_PRODUCTION_AGENT.md): end-to-end prompt with scope, permissions, tools, format compatibility and stopping rules.
- [Build Playbook](docs/vtuber/BUILD_PLAYBOOK.md): repeatable workflow, quality gates, asset requirements, rigging, physics, motion, and packaging.
- [OrangeScarf Case Study](docs/vtuber/ORANGESCARF_CASE_STUDY.md): verified findings, root causes, fixes, constraints, and next tests from OrangeScarf v0.1-v0.4.
- [Reusable Agent Prompt](prompts/VTUBER_MODEL_AGENT.md): scoped prompt template for future VTuber model work.

## Working principles

1. Preserve original assets and make versioned backups before changing a model.
2. Distinguish source facts, inferred diagnoses, static validation, and actual runtime results.
3. Never claim VTube Studio/Cubism runtime success unless tested in the target application.
4. Keep base artwork and animated overlays from drawing the same facial feature twice.
5. Verify UVs, texture dimensions, file references, motion parameter IDs, physics ranges, and reproducible builds.
6. Record new bugs, fixes, constraints, and test evidence in this repository after each VTuber project.

## Current reference project

OrangeScarf is the first documented model. Its source is a flattened RGBA illustration, so the current rig is a constrained 2.5D model rather than a fully layered Cubism production model.
