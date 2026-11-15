# V Skills

A reusable knowledge base of agent skills, technical playbooks, prompts, and verified project lessons.

## VTuber / Live2D

- [VTuber Model Builder Skill](skills/vtuber-model-builder/SKILL.md): reusable operating instructions for building, repairing, and validating Live2D/VTube Studio models.
- [AI-Assisted Production Research (2026)](docs/vtuber/AI_PRODUCTION_RESEARCH_2026.md): sourced 2D/3D production routes, AI assistance boundaries, editing and compatibility constraints, licenses, and OrangeScarf experiments.
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
