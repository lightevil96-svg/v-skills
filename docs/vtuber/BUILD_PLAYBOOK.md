# VTuber / Live2D Build Playbook

This playbook defines a repeatable workflow for future VTuber model projects. It separates source-art limitations from rigging defects and distinguishes static validation from runtime proof.

> **For a new AI agent:** Read [START_HERE_AGENT.md](START_HERE_AGENT.md) and the [Live2D Execution Runbook](LIVE2D_EXECUTION_RUNBOOK.md) first. This playbook is a detailed technical reference, **not** proof that any tool can produce .cmo3/.moc3 from text without an authentic Cubism authoring/export environment. See [Troubleshooting](TROUBLESHOOTING_AND_LIMITS.md) for blocked stages and [Agent Readiness Audit](AGENT_READINESS_AUDIT.md) for evidence limits.

## 1. Source asset requirements

### Preferred input

- Layered PSD, CLIP, or another editable layered source.
- Transparent, full-resolution character artwork.
- Separate head, face, eyes, mouth, hair groups, torso, arms, hands, clothing, and accessories.
- Occlusion-aware layers: front hair above face, neck below head, scarf above shirt, hands/arms with appropriate overlap.
- Existing Cubism project (.cmo3) when available.

### Fallback input

A single flattened RGBA PNG can support a constrained 2.5D rig, but it does not contain hidden pixels behind hair, face features, clothing, or limbs. Any separation requires manual reconstruction or careful image processing. Never imply that a flattened source can provide the same articulation as a properly layered illustration.

Record source dimensions, color mode, alpha extrema, visible bounds, and SHA-256 before editing.

## 2. Artwork and texture quality

1. Inspect the source at native size and at expected on-screen zoom.
2. Inspect face details separately: brows, eyes, eyelids, nose, mouth, jaw, fringe, ears.
3. Preserve the source artwork as an immutable input.
4. Use premultiplied-alpha resizing/compositing to avoid dark or colored fringes at transparent edges.
5. Use high-quality resampling for controlled size changes. Clearly distinguish Lanczos resampling from AI super-resolution: resampling increases pixel sampling density but does not create missing detail.
6. For AI upscaling, test an anime/illustration model such as Real-ESRGAN x4plus anime 6B against the original. Inspect line-art, facial identity, eye details, and alpha edges because enhancement models can hallucinate or alter fine details.
7. Do not upscale a whole atlas unnecessarily. Pack only required assets and patches. Consider GPU memory: RGBA texture memory is approximately width × height × 4 bytes before GPU-specific overhead.

## 3. Face-layer integration

This is a critical quality gate.

If eyes or mouth are animated as separate meshes, the base head texture must not still display the original eyes or mouth underneath. Otherwise blinking/opening can reveal duplicate features, ghosting, patches, or misalignment.

Recommended method for flattened artwork:
- define a precise feature mask;
- preserve fringe/occlusion pixels that should remain in front;
- reconstruct the base skin under the removed feature using nearby skin texture or inpainting;
- create separate open-eye and closed-eye patches from aligned crops;
- create a source-aligned closed-mouth patch;
- create a dedicated open-mouth patch with matching line art, cavity, teeth, and tongue;
- use feathered alpha at patch boundaries;
- map each mesh to its own atlas region;
- preview neutral, blink, and talk states before building the final MOC3.

Do not use arbitrary UV sample points from unrelated parts of the source image. A mouth cavity must not sample an eye, eyebrow, scarf, or random pixel.

## 4. Mesh and UV design

- Use denser triangulation around facial features, eyelids, mouth, hairline, and outer silhouette.
- Use moderate density on broad stable clothing/body regions.
- Check for triangles spanning transparent gaps, long slivers, and mesh islands that deform independently by accident.
- Keep face feature meshes bound to the same head-angle parameters as the head.
- Avoid applying hair physics to face/skin pixels.
- For non-square texture atlases, normalize U by atlas width and V by atlas height: U = x / width; V = 1 - y / height. Do not reuse one dimension for both axes.
- Verify all UV coordinates stay in [0,1].

## 5. Parameters, physics, and motion

### Parameters

Define each parameter's ID, min/max, default, and keyform values before writing motion or physics files. Motion and physics references must match exact parameter IDs.

### Physics

- Establish a stable root and a consistent chain direction.
- Normalize input weights to 100% where required by the format.
- Ensure physics normalization ranges fit inside the parameter min/max.
- Keep physics output parameters distinct from motion-driven parameters unless a priority interaction is intentional.
- Test fixed FPS versus app-matched FPS on the target device.

### Motion

Recommended baseline:
- Idle loop with subtle breathing/head movement.
- Blink or eye action.
- Look around.
- Greeting.
- Happy.
- Surprised.
- Nod.
- Laugh.
- Thinking.

Use smooth curves, bounded values, and neutral return points. Avoid continuous action motions competing with tracking or physics.

## 6. VTube Studio packaging

Verify:
- model3 points to the correct MOC3, texture, physics, expressions, and motion files;
- all referenced paths exist relative to the model folder;
- VTube Studio sidecar and icon are present;
- model folder nesting is correct;
- motion files are registered in the model3 manifest.

Create user hotkeys through the VTube Studio UI unless a current, exact hotkey schema has been verified. Do not invent undocumented JSON.

### Runtime-folder vs development-bundle separation (mandatory)

Do not confuse the **outer distribution ZIP** with the actual VTube Studio **model folder**. A parent bundle containing `OrangeScarf/`, `Source/` and reports is not inherently invalid if `OrangeScarf/` contains a complete model, but only the inner model folder belongs under VTube Studio's `StreamingAssets/Live2DModels/`. Do not put `Source/`, `BUILD_REPORT.txt`, preview images, or verification reports beside the runtime model files in an installable model folder.

The installable folder must have one `*.model3.json` and its real referenced `*.moc3` and texture assets; any referenced physics, expressions, motions, and other files must resolve **relative to model3**. Do not force Hiyori's naming or folder depth onto a different model. `.cdi3.json` and `.vtube.json` are not universal prerequisites for first import; icon is recommended; VTube Studio pinned-item files are optional.

Before release, use [VTS Folder Structure and Repack Guide](VTS_FOLDER_STRUCTURE_AND_REPACK.md) and run:

```bash
python scripts/vtuber/repack_vts.py 'INPUT.zip' --inspect
python scripts/vtuber/repack_vts.py 'INPUT.zip' --output 'MODEL_VTS.zip' --folder-name 'MODEL_vts'
python -m unittest discover -s tests -v
```

The output must be a **new** ZIP containing one model-root folder (not a mixed development bundle). Static checks are not proof of actual VTube Studio import.

## 7. Validation ladder

### Static validation

- MOC3 parses and has expected version.
- Expected parameter and ArtMesh counts match.
- UVs are in range.
- Texture dimensions match the UV normalization.
- Face patch regions are present and non-empty.
- Model3 and VTube Studio references resolve.
- Motion curve IDs, values, times, and metadata are valid.
- Physics input/output IDs, weights, normalization, and chain direction are valid.
- Source artwork hash is unchanged when preservation is required.
- Deterministic rebuild hashes match.

### Visual validation

Inspect:
- neutral face;
- both eyes open;
- both eyes closed;
- partial blink;
- mouth closed;
- mouth open;
- head yaw/pitch/roll;
- hair sway;
- neck/head seam;
- full-body edges at target zoom.

### Runtime validation

Import into VTube Studio and test actual tracking, physics, motion playback, hotkeys, frame pacing, and device performance. Static checks and offline previews are not runtime proof.

## 8. Release and documentation

- Version packages instead of overwriting prior builds.
- Include install instructions, source scripts, requirements, build report, validation report, and previews.
- Record known limitations.
- Keep a case study for each model in V Skills.
- Do not claim a defect is fixed until the corresponding preview or runtime test supports that claim.

## References

- Live2D Cubism specifications: https://github.com/Live2D/CubismSpecs
- Real-ESRGAN model zoo: https://github.com/xinntao/Real-ESRGAN/blob/master/docs/model_zoo.md
- VTube Studio: https://github.com/DenchiSoft/VTubeStudio
- OrangeScarf case study: ./ORANGESCARF_CASE_STUDY.md
