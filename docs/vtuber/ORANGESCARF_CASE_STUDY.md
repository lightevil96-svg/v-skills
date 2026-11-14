# OrangeScarf VTuber Case Study

## Project identity

- Model: OrangeScarf
- Target: VTube Studio / Live2D-compatible package
- Repository knowledge home: V Skills
- Source input: one flattened RGBA PNG, 1024 × 1536
- Editable source layers: not supplied
- Cubism .cmo3 project: not supplied
- Rig class: constrained 2.5D starter rig, not a fully layered production rig

## Version history and verified findings

### v0.1 / initial package

The initial package contained a flattened character illustration and generated rig assets. The original artwork is not a layer-separated source. This is the core limitation for independent hair, arm, hand, scarf, and facial articulation.

### v0.2 / v0.3 investigations

The generated Head ArtMesh still sampled the complete head artwork, including original eyes and mouth. Separate eye and mouth meshes were drawn over it. That architecture risks duplicate facial features and patchy transitions because the base pixels remain visible.

Specific UV defects found in the v0.3 builder:
- the open-mouth cavity sampled a fixed source point near the eye region (around x=552.5, y=148.5);
- the tongue sampled a fixed source point around x=519.5, y=307.5, in the scarf region;
- eyelid skin patches used cheek samples as flat underpaint;
- the original eye/mouth pixels were not consistently removed from the base head texture.

The face issue was therefore both a layer-compositing problem and a texture-coordinate problem, not simply a low-resolution issue.

### v0.4 / face integration and texture update

The v0.4 builder applies these corrections:
- removes/reconstructs dynamic eye and mouth pixels in the derived base head texture;
- preserves the upper eyelid contour and fringe occlusion while reconstructing eye interiors from nearby cheek pixels;
- uses separate aligned open-eye and closed-eye patch crops;
- uses a source-aligned closed-mouth crop;
- uses a dedicated open-mouth patch with matching skin/line-art colors;
- no longer samples eye/scarf pixels as mouth texture;
- uses feathered alpha around facial patch boundaries;
- uses alpha-premultiplied Lanczos 2× texture resampling;
- packs the texture in a 2048 × 4096 atlas to avoid storing an unused duplicate full artwork.

### v0.4 package facts

- MOC3 version: 3
- Parameters: 11
- ArtMeshes: 8
- Mesh IDs: Body, Head, EyeL, ClosedLidL, EyeR, ClosedLidR, ClosedMouth, MouthCavity
- Texture atlas: 2048 × 4096
- Source artwork: 1024 × 1536
- Texture sampling: 2×
- Physics FPS in package: 30
- Motion files: 9 (Idle plus Blink, LookAround, Greeting, Happy, Surprised, Nod, Laugh, Thinking)
- Static validation: 227 passed, 0 failed
- Deterministic rebuild: tested; MOC3, physics, model3, VTube Studio sidecar, icon, texture, and selected motion hashes matched on a clean rebuild.

## What v0.4 does not prove

- VTube Studio/Cubism runtime was not executed in the build environment.
- 227 passing checks are static structure/asset checks, not proof of correct tracking or deformation in the app.
- The 2× Lanczos texture is higher sampling density, not AI super-resolution and does not invent new details.
- The source remains flattened. Arms, hands, scarf segments, and individual hair strands are not independent art layers.
- The model remains a 2.5D rig. It cannot provide full 3D-like rotations or hidden anatomy without additional artwork.

## Required next user-side test

Import v0.4 into VTube Studio and record 15–20 seconds while testing:
1. neutral tracking;
2. head turn left/right and up/down;
3. blink and partial blink;
4. mouth closed/open while speaking;
5. hair physics during head movement;
6. one-shot motion playback and return to neutral.

Review the video for facial seams, eye clipping, mouth alignment, hair/fringe occlusion, head/neck gaps, motion/tracking conflicts, and device performance. Update this case study only after the actual runtime evidence is reviewed.

## Reusable lessons

1. Never overlay a dynamic eye or mouth on top of an unchanged base face.
2. Do not map a feature to arbitrary UV sample points outside that feature's source region.
3. Preserve hair fringe as an occluding layer when reconstructing eyes.
4. Use separate open/closed patches with matching crop coordinates and feathered alpha.
5. Keep texture width and height separate when normalizing UVs for portrait atlases.
6. Test the ZIP after extraction, not only the working folder.
7. Rebuild deterministically and record hashes before claiming a reproducible package.
8. Report static and runtime validation separately.
