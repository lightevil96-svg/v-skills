---
name: vtuber-model-builder
description: Build, repair, rig, animate, package, and validate Live2D/VTube Studio character models while preserving the user's original design and project constraints.
---

# VTuber Model Builder

## Mission

Produce a stable, visually coherent, responsive VTuber model. Treat the artwork, mesh, parameters, physics, motions, VTube Studio configuration, and package as one system. Do not optimize one layer while silently breaking another.

## Tool selection

- Use container/Python for archive inspection, image processing, code edits, mesh/UV analysis, deterministic builds, and static validation.
- Use the GitHub connector for repository inspection and authorized documentation/code updates.
- Use image generation only when the user explicitly asks for new or edited artwork. Do not use it as a substitute for editable layers, rig structures, or machine-readable model files.
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

Update the V Skills case study and playbook after meaningful new findings.
