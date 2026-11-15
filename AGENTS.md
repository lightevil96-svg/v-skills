# Agent instructions for `v-skills`

**Repository purpose:** reusable operational knowledge, prompts and QA tools for building VTuber assets. **This repository is NOT an already trained or installed Live2D authoring engine.** Follow the actual user's request and available tools; do not assume this project includes the user's source artwork, PSD, real .cmo3/.moc3, Cubism Editor or VTube Studio.

## Required cold-start sequence

1. Read [VTuber Model Builder](skills/vtuber-model-builder/SKILL.md) and [START HERE](docs/vtuber/START_HERE_AGENT.md).
2. Determine task type **before any write**: documentation/skill-only, research, diagnose, art-preparation, native model authoring, release packaging, target-runtime testing.
3. If Live2D/VTube Studio: follow [Live2D execution runbook](docs/vtuber/LIVE2D_EXECUTION_RUNBOOK.md). If VRM/3D: follow [3D/VRM runbook](docs/vtuber/VRM_3D_EXECUTION_RUNBOOK.md). Don't confuse runtime formats: VTube Studio takes Live2D, not VRM.
4. Read only the necessary additional sections of [QA matrix](docs/vtuber/PRODUCTION_QA_MATRIX.md), [failure recovery](docs/vtuber/TROUBLESHOOTING_AND_LIMITS.md), [source research](docs/vtuber/AI_PRODUCTION_RESEARCH_2026.md) and the **current specific model's** case study. Do not overconsume irrelevant documents.
5. State goal, exact target format/app, real inputs and source hashes, selected tools, measured acceptance criteria, in-scope files, permissions and stop conditions. Read-only [preflight helper](scripts/vtuber/preflight.py) is available.
6. Execute reversible, authorized work only. Keep the original art/rig immutable; make a versioned output when building.
7. Report evidence per stage. Real editable .cmo3 requires a genuine authoring workflow; .moc3 requires a real exporter; a header/ZIP/static test does **not** prove the model is valid. Validate true MOC3 with [official checker](https://docs.live2d.com/en/cubism-editor-manual/moc3-consistency-checker/) or compatible SDK and confirm actual VTube Studio import/tracking.
8. If tools, rights, layers or hardware are missing: complete safe preparatory work, mark blocked/NOT RUN and state the dependency. **Never fabricate completed model files or runtime evidence.**
9. For a documentation-only request, **do not touch user model files** or demand a model upload. For a model request, do not edit unrelated repository files.
10. Use [real production evidence protocol](docs/vtuber/REAL_PRODUCTION_VALIDATION.md) and [fresh-agent evaluation suite](evals/agent_cases.json) to determine what can honestly be claimed.

## Change-management and acceptance

- **Scope / approval:** do not invent hidden anatomy, redesign identity, upload private artwork to external AI services, purchase tools, publish or destroy originals without permission.
- **Runtime-folder structure:** model3 manifest determines exact paths. Separate installation-ready VTS folder from source PSD/.cmo3, `Source/` and reports; do not blindly copy Hiyori folder names.
- **Tests (structural only):** run `python scripts/vtuber/check_skill_links.py` and `python -m unittest discover -s tests -v`. GitHub Actions performs Python syntax, local-link and synthetic fixture tests.
- **No counterfeit completion:** don't turn tests of fake MOC headers, generated PNG previews, static package checks or human-scored agent answer forms into evidence of a working native rig.
- **Handoff:** list exact real files changed, passed/failed/NOT RUN tests, remaining blockers, app compatibility, and one next required action. For new agent readiness, 12 challenge scenarios require actual separate agent transcripts and independent review; **do not self-award 10/10**.

Primary official sources: [Cubism export](https://docs.live2d.com/en/cubism-editor-manual/export-moc3-motion3-files/), [MOC3 Consistency Checker](https://docs.live2d.com/en/cubism-editor-manual/moc3-consistency-checker/), [VTube Studio import](https://github.com/DenchiSoft/VTubeStudio/wiki/Loading-your-own-Models).
