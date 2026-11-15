# AI-Assisted VTuber Production Research (15 November 2026)

> Scope: practical, evidence-led production of **high-quality, editable, stream-ready VTuber avatars**, especially 2D Live2D/VTube Studio, with a distinct 3D/VRM route. This is a researched workflow, **not evidence that any particular avatar was built or runtime-tested**. Source references and compatibility caveats are recorded below. Read [BUILD_PLAYBOOK.md](BUILD_PLAYBOOK.md) and [ORANGESCARF_CASE_STUDY.md](ORANGESCARF_CASE_STUDY.md) first for current project constraints.

## 1. Executive findings and correct product choice

**Quality is a pipeline property**, not a property of a single AI-generated illustration. Optimize for (1) recognizable and coherent character identity, (2) separable editable artwork / clean 3D geometry, (3) accurate deformation, (4) convincing expressions and secondary motion, (5) stable tracking, (6) usable performance, and (7) maintainable source files.

| Target | Editable working files | Export / runtime files | Rigging and use | Runtime |
| --- | --- | --- | --- | --- |
| 2D streaming avatar | Layered PSD/CLIP and **Cubism .cmo3** | .moc3, .model3.json, texture PNGs, .physics3.json, .exp3.json, .motion3.json where present | ArtMeshes, warp/rotation deformers, parameters, physics; head pose is 2.5D deformation, not full 3D | **VTube Studio** (Live2D only) |
| 3D streaming avatar | **.vroid** (VRoid), or **.blend** plus source textures | **.vrm** in the **version supported by the target** | Humanoid skeleton, skinning/weights, expressions (morph targets), eye gaze, spring bones/colliders | VRM-compatible software, e.g. Warudo; check target-specific version and tracking setup |
| Single flattened PNG | Original PNG + derivative masked layers / reconstruction | Potentially a *limited* 2.5D model | No actual hidden anatomy or separately authored parts exist | Cannot promise fully expressive premium Live2D without new artwork |

**Format trap:** VTube Studio does **not** load VRM models. VSeeFace's official manual says it supports **VRM 0.x only**, not VRM 1.0. The main VRoid Studio export documentation describes VRM 0.0 **and** 1.0 options, but the newer **dress-up feature's** separate export documentation says it exports **VRM 1.0 only**. Do not merge these distinct workflows or claim universal compatibility. Test the *exact exporter + export mode + target-app version* before committing to a pipeline.

**Recommended default for this repository:** prioritize the **2D Live2D route**, because the existing OrangeScarf evidence and established skills target VTube Studio. Use the 3D route only when the project explicitly needs true volumetric body rotation/3D motion or the target app is VRM-compatible.

## 2. What AI can do, and what it cannot establish

| Stage | Practical AI assistance | What still needs verification or human art direction |
| --- | --- | --- |
| Creative direction | Character briefs, silhouettes, style sheets, consistent palettes, expression concepts, layer maps | Consent, intellectual-property provenance, uniqueness, stable identity across angles |
| Artwork | Generate **new artwork only if authorized**; segment visible image regions (e.g. SAM 2); mask and inpaint occluded regions; optional illustration upscaling | Generated artwork may be inconsistent; segmentation does **not** recover pixels hidden behind hair/arms; reconstructing them requires artistic decisions |
| 2D setup | Draft part inventories, naming, import QA, preliminary meshes and parameter scripts, scriptable atlas/mask checks | PSD correctness, hair occlusion, eyelids/eye geometry, clean mesh triangles and depth order |
| 2D rig | Use Cubism 5's **semi-automatic face movement**; suggest keyforms, interpolate motions, find out-of-range parameter references | Cubism facial auto-generation requires correct face parts/deformers and is specifically documented for **front-facing faces**; polished diagonal views, blinking and expressive rigging require review |
| Texture | Real-ESRGAN anime model for restoration/upscaling candidates; automated alpha/mask analysis; atlas packing | Diffusion/upscaling can change eyes, linework and identity; ordinary Lanczos scaling is **not** AI reconstruction; texture memory/performance |
| Physics/motion | Generate baseline curves and config templates; validate curves/ranges/IDs automatically | Natural timing, collision, parameter ownership conflicts, tracking-vs-motion priorities |
| 3D mesh | Image-to-3D candidates (e.g. Hunyuan3D), automated UV/retopology/rig suggestions | Production topology, facial edge loops, asymmetry, weight painting, mouth/eyes, back/hidden anatomy, commercial-use permission |
| QA and packaging | Automated file inventories, structure validators, regression images/video, source hashes, failure reports | True Cubism/VTube Studio or VRM app runtime tests **must be executed**, never inferred from static checks |

A language model's source code, a generated concept image, or a simulated preview is not an automatically editable .cmo3/.blend, a valid .moc3 or evidence of successful app import. Treat the required output medium as a hard constraint.

## 3. Preproduction / identity control

1. **Record the brief:** 2D or 3D, reference character, front/side needs, half/full body, art style, audience, intended streaming crop, target app/device, budget, permissions, commercial use and allowed design changes.
2. Freeze an **identity bible**: stable face proportions, iris color/shape, hair part, outfit features, accessories, line thickness, shadow language, palette (hex), and no-change areas. Use original source/reference image as authoritative; don't silently let generative AI reinterpret features.
3. Produce **separate reference deliverables**: neutral front, expression sheet (blink, smile, mouth open, surprise), layer/depth diagram, and optional angle/body turnaround for 3D. Generate artwork only if the user requests creation or editing.
4. Require a **deliverable contract** at the start: exact editable sources, export format/version, target tracking app, expected expressions/motions, resolution/performance budget, and QA evidence.
5. Audit provenance/licenses **before uploading** references to third-party services or publishing generated assets. Check model weights, generator TOS, brushes, fonts, commissioned art, presets, textures and accessories; don't assume “open source” equals unrestricted commercial use.

## 4. High-quality 2D Live2D route (preferred for V Skills)

### A. Asset intake and separation

- Prefer the original **layered PSD/CLIP** and **.cmo3** when supplied. Make immutable backup, file manifest and SHA-256 checksums. For Cubism PSD import, lower-level paint/line-art within an imported part needs to be prepared as a combined texture layer; preserve a separate editable material-separation PSD instead of overwriting it.
- Draw a part/depth hierarchy **before rigging**. At minimum, decide head base, neck, torso; back hair / side hair / bangs; brows; upper/lower eyelids, lashes, irises/pupils, eye whites, highlights; mouth line/cavity/teeth/tongue as needed; clothes, arms/hands and accessories according to motion requirements. Keep overlapping front/back versions where pose requires them.
- **Invisible reconstruction is mandatory** for parts newly exposed by turning the head, opening eyes/mouth, lifting hair or moving clothing. A segmentation mask from SAM 2 can select *visible* regions, and inpainting can hypothesize hidden skin/art, but neither guarantees the correct hidden character design. Review these areas frame-by-frame.
- Never double-render facial features: when eye and mouth meshes animate, remove the original eye/mouth pixels from the underlying face texture. Preserve bangs as true foreground occlusion. Build source-aligned open/closed and partial states; feather/matte cleanly.
- For **flattened PNG**, tag art changes as *reconstruction* and require explicit permission before new hidden anatomy or a redesign. Otherwise deliver a clearly limited 2.5D rig. See OrangeScarf lessons.

### B. Texture / atlas standard

- Check at original resolution **and** target on-stream size (full-body face may occupy very few pixels).
- Compare original vs candidate upscaled patches at 100%/200%: eye outlines, lashes, mouth corners, blush, line weight, hue, alpha edges, garment motifs. Keep original when restoration changes the style.
- Use alpha-premultiplied resampling/compositing to reduce transparent edge halos; avoid arbitrary pixels from other atlas regions for UV sampling.
- For a non-square atlas, normalize **u = x/atlas_width; v = 1 - y/atlas_height** (when source image y increases downward). Assert each UV within [0,1], and test orientation.
- Rough **uncompressed RGBA** GPU payload per full texture = **width × height × 4 bytes** (plus actual GPU/renderer overhead). Example: 2048×4096 ≈ **32 MiB**; 4096×4096 ≈ **64 MiB**. Atlases are not automatically better when they waste space; benchmark device load times and memory.
- VTube Studio warns that large/multiple textures can lag or crash mobile. Do not promise “8K always best.” Pick sizes from required close-up sharpness and measured target hardware performance.
- Real-ESRGAN's `RealESRGAN_x4plus_anime_6B` is an optional **AI-upscale candidate**, not a source-of-truth replacement. Lanczos alone is resampling.

### C. Mesh, deformation, expressions

1. Auto-generate starter ArtMeshes **before** authoring keyforms; Live2D warns that regenerating meshes *after* parameter deformation can reset or disturb forms. Manually refine high-deformation edges (eyelashes, eye shapes, mouth, hair tips, cheek outline). Avoid elongated triangles, floating islands, triangles spanning transparent gaps.
2. Design explicit deformer hierarchy: high-level body → neck → head → facial subregions; separate rotation deformers for independently pivoting parts; hair/clothes physics should not deform face pixels.
3. Use Live2D standard parameter IDs when suitable: `ParamAngleX/Y/Z` (often −30..30, default 0), `ParamEyeLOpen/ROpen` (0..1, default 1), `ParamEyeBallX/Y` (−1..1), `ParamMouthOpenY` (0..1), `ParamMouthForm` (−1..1), `ParamBreath`; record any custom IDs/ranges and confirm in the actual model.
4. Cubism 5 **Auto generation of facial motion** can generate a face deformer and Angle X/Y keys after corresponding facial parts/deformers are set. Official docs explicitly limit this feature to **front-facing faces**. Use it as a baseline; tune facial perspective, eye volumes, mouth perspective, jaw/cheek shape and head-to-neck seams across the full motion range manually.
5. Generate **four-corner forms** for combined X/Y motion from established keyforms, then inspect and correct all diagonal corners. Regeneration can overwrite already sculpted corners: create a backup/take.
6. Build separate believable blink (left/right), eyelid smirk/smile, brow, eyeball gaze, mouth open/form, and several facial expressions (happy, angry/sad, surprise, thinking). Evaluate expressions *together* with blinking and talking; avoid mutually exclusive overlays in the same render stack.
7. Physics: use distinct input/output parameters and stable roots. Live2D's physics docs recommend **60 FPS** when target app is unknown, but **changing FPS changes the physical result**. This is not a guarantee of 60 FPS runtime rendering; calibrate at actual device frame pacing. Tune sway, damping, convergence and collision so hair/scarf are lively but not rubbery.
8. Live2D Motion Sync analyzes audio to generate viseme-based mouth motions **when the viseme shapes/parameter mappings are prepared**. Do not imply full speech phoneme quality when a model has only one mouth-open parameter or that an editor preview proves VTube Studio real-time feature support.

### D. Export / VTube Studio

- Preserve editable **.cmo3 + layered art**, then export the correct **.moc3** and a **.model3.json** manifest; include textures and physics, expressions and motion assets as actually referenced.
- Validate all relative paths and exact parameter IDs. A `.vtube.json` is VTube Studio-specific; VTS can create it on initial import. Configure/check tracked inputs and output parameter mapping in VTS. Default IDs simplify auto-setup; custom IDs require manual mapping.
- Confirm neutral expression, blink, talk, head turn X/Y/Z, diagonal turn, eye gaze, hair movement, expression hotkeys and return-to-idle. Test the **actual app** on **actual intended hardware**, not just an offline preview.
- Package one model directory, with tested clean extraction/import, icon, user instructions, version, rollback source and known limitations.

## 5. High-quality 3D VRM route

1. **Start with a model that can actually be edited:** `.vroid` in VRoid Studio, or a Blender `.blend` scene. VRoid texture editor supports import/export of **PNG** textures. Keep master files; do not expect `.vrm` to reopen as editable `.vroid` in VRoid Studio.
2. Make consistent front/side/back concept sheets and an expression reference. Image-to-3D tools such as Hunyuan3D can supply **mesh proposals**, **not** reliably final VTuber-ready anatomy, clothing seams, skeleton, UVs or expressions. Inspect the **license** of each model and service; the Hunyuan3D-2 repository includes non-commercial license language, so do not assume commercial streaming/reuse is permitted.
3. In Blender, repair symmetry where intended, missing back geometry, normals, manifold/self-intersections where relevant, face topology around eyelids/lips/jaw, hair cards and clothing intersections. Retopologize deforming areas rather than applying raw dense generated topology as a final animated mesh.
4. Clean UV islands and texture seams; author stylized coherent albedo/materials (MToon where appropriate). Preserve irises, facial proportions and accessories across turnarounds; audit excessive polygon/texture/memory costs against the real target.
5. Build and validate humanoid bone hierarchy, rest pose, skinning/weight painting, facial blendshapes or VRM expressions (blink, happy, angry, sad, surprise, mouth shapes/visemes), look-at, spring-bone hair/clothes and colliders; check elbow/knee/neck deformation and unwanted skin penetrations.
6. Export to **the target application's supported VRM version** and inspect its model metadata/license. The current VRM 1.0 specification covers expressions, lookAt and SpringBone and recommends their evaluation order. The VRM Blender add-on supports VRM functionality; choose an app/add-on version supported by the project instead of assuming any current exporter will work.
7. Runtime test in the chosen 3D tracker, including mic-driven mouth, eye tracking, head/body motion, hands when needed, spring bones, expressions and actual stream scene. **Warudo** documents VRM model import and VRM expression handling, but do **not** infer a specific VRM version from a generic “VRM supported” statement; verify with a live import.
8. **Known mismatch:** VSeeFace documentation states VRM0-only; its model file cannot be fed VRM1 directly. Older **VRoid Studio model-editor export** documentation describes selectable VRM0/VRM1, while its **dress-up feature export** documents VRM1-only. If target requires VRM0, identify an allowed, tested VRM0 exporter/conversion path *before* production.

## 6. Process controls that make the output professional

**Versioned milestones:** `concept-approved` → `separated-art-approved` → `neutral-rig-approved` → `expression-rig-approved` → `physics-approved` → `runtime-validated` → `release`. Each gate must have artifacts and review evidence. If a gate fails, do not silently move onward.

**Suggested naming/layout:**

```text
model-name/
  originals/            # immutable source + checksum manifest
  working/              # layered PSD/CLIP, .cmo3 OR .blend/.vroid
  concepts/             # approvals and identity/style sheets
  source-scripts/       # deterministic processing/build scripts
  previews/             # poses, video clips and before-after comparisons
  reports/              # static validation, visual QA and runtime QA
  releases/vX.Y.Z/      # final app-specific extracted package
```

The directory example is a **recommended output workspace**; it does not assert that the existing OrangeScarf or V Skills repository uses this layout.

**Quality-first rules:**

- **Identity:** compare face, hair and clothing to the signed-off reference, not just the generated candidate. Any unexpected redesign is a blocker.
- **Occlusion:** hair stays in front of the correct facial regions; no double eyes/lips, transparent holes, or scarf/skin sample swaps.
- **Animation:** inspect neutral + all extrema + diagonal combined poses + transition video. A keyframe screenshot alone is insufficient.
- **Physics:** stable at idle and after sharp turns; no infinite oscillation, unnatural head/neck break, or competing parameter writes.
- **Performance:** record app version, hardware, resolution/atlas layout, capture setup and measured in-app FPS/memory where available. Targets depend on device and stream use; *30 FPS minimum steady preview* and *60 FPS preferred* are proposed project targets, **not** specifications or measured OrangeScarf results.
- **Accessibility/usability:** recognizability at small stream crop, readable expressions, hotkeys explained, short installation instructions, no dependency on inaccessible private inputs.
- **Legal/privacy:** rights to original art and generated assets, service terms, licensed weights, permitted redistribution, no uploading sensitive references without authorization.

## 7. Concrete AI-agent execution policy

**Before any edits:** inspect the actual model/repo/target apps; inventory and hash inputs; identify exact request, change scope, constraints and outputs; consult existing V Skills case study. Produce a bounded plan with independent QA evidence.

**Allowed without extra permission:** reading source/repo docs, proposing a part map, local non-destructive test copies, static validators, preview generation from permitted source content, documentation updates authorized by user.

**Requires explicit permission:** inventing hidden anatomy, redesigning identity, generative alteration of source art, uploading private/source art to external AI services, purchasing APIs, publishing assets/streams, deleting or replacing originals, changing unrelated files or public repository visibility.

**Agent stopping points:** missing essential source data; source/licensing conflict; incompatible model/runtime version; destructive change required; hidden anatomy must be designed; target-app runtime inaccessible when a runtime claim is required. Report partial work and alternatives instead of fabricating success.

**Output report:** files changed, SHA-256 inputs, implementation approach, model parts/meshes/parameters/expressions/physics/motions, atlas dimensions, package layout, validation commands and pass/fail counts, preview evidence, actual app/runtime measurements, limits and next action. Separate **verified fact**, **engineering recommendation**, **hypothesis**, and **not yet tested**.

Read [PRODUCTION_QA_MATRIX.md](PRODUCTION_QA_MATRIX.md) for a reproducible test plan. See [../../prompts/VTUBER_AI_PRODUCTION_AGENT.md](../../prompts/VTUBER_AI_PRODUCTION_AGENT.md) for a reusable production prompt.

## 8. Prioritized next research/experiments for OrangeScarf (NOT completed tests)

1. Compare original 1024×1536 artwork, current 2× Lanczos derivatives, and an **AI-enhanced *copy*** of relevant face patches at matched display size. Determine whether eye and lip identity improves without hallucinations; do not replace master art.
2. Audit current overlay-to-base skin composition in **neutral, partial blink, full blink, partial talk and full talk**, including fringe occlusion, seam halos and deliberate alpha transitions.
3. Review current 11-parameter/8-ArtMesh 2.5D range versus desired motions. Document which premium-rig effects **cannot** be achieved without new layers; obtain approval for any new art.
4. Run the existing OrangeScarf runtime test in actual VTube Studio, including 15–20 seconds of face turns, blinking, speaking, idle and one-shots; capture app/device versions and actual logs. No runtime-success claim until this happens.
5. Treat performance as a measured constraint; compare the existing 2048×4096 atlas with a more tightly packed variant on the intended device instead of upscaling everything.

## 9. References and what they establish

Sources were consulted on **2026-11-15**; links are factual pointers, not blanket endorsement. Recheck version-sensitive pages before future builds.

### Official Live2D documentation
- [Material separation](https://docs.live2d.com/en/cubism-editor-manual/divide-the-material/) — part separation is necessary; detail influences rig potential.
- [Import PSDs](https://docs.live2d.com/en/cubism-editor-manual/psd-import/) and [PSD preparation](https://docs.live2d.com/en/cubism-editor-manual/reimport-psd/) — correctly layered import vs preserved source.
- [Automatic mesh generator](https://docs.live2d.com/en/cubism-editor-manual/mesh-edit/) and [manual mesh editing](https://docs.live2d.com/en/cubism-editor-manual/mesh-edit-manual/) — auto then manual cleanup, avoid auto mesh changes after deformation.
- [Standard parameters](https://docs.live2d.com/en/cubism-editor-manual/standard-parameter-list/) and [parameters](https://docs.live2d.com/en/cubism-editor-manual/parameter/) — IDs/defaults and keyform semantics.
- [Auto generation of facial motion](https://docs.live2d.com/en/cubism-editor-manual/face-auto-edit/) — semi-auto, required parts/deformers, front-facing-only limitation.
- [Four corner generation](https://docs.live2d.com/en/cubism-editor-manual/synthesize-corners/) — XY diagonal form synthesis and overwrite risk.
- [Physics](https://docs.live2d.com/en/cubism-editor-manual/physics-operation/) and [physics setup](https://docs.live2d.com/en/cubism-editor-manual/physical-operation-setting/) — FPS, inputs/outputs and pendulums.
- [Motion Sync](https://docs.live2d.com/en/cubism-editor-manual/motion-sync/) — visemes and prepared shapes/parameters.
- [File types](https://docs.live2d.com/en/cubism-editor-manual/file-type-and-extension/) — editor and runtime export distinctions.

### Official tracking / 3D specifications
- [VTube Studio: supported model types](https://github.com/DenchiSoft/VTubeStudio/wiki/Models), [loading your own models](https://github.com/DenchiSoft/VTubeStudio/wiki/Loading-your-own-Models) and [getting started](https://github.com/DenchiSoft/VTubeStudio/wiki/Getting-Started) — 2D only, manifest, mobile texture caution, calibration and mapping.
- [VRM 1.0 core spec](https://github.com/vrm-c/vrm-specification/blob/master/specification/VRMC_vrm-1.0/README.md), [lookAt](https://github.com/vrm-c/vrm-specification/blob/master/specification/VRMC_vrm-1.0/lookAt.md), [springBone](https://github.com/vrm-c/vrm-specification/blob/master/specification/VRMC_springBone-1.0/README.md), [meta/license fields](https://github.com/vrm-c/vrm-specification/blob/master/specification/VRMC_vrm-1.0/meta.md) — 3D behavior/rights.
- [VRoid Studio normal export](https://vroid.pixiv.help/hc/en-us/articles/15760756822297-I-want-to-learn-more-about-the-VRM-export-feature) **vs** [dress-up-only export](https://vroid.pixiv.help/hc/en-us/articles/39513600013721-Q-Can-I-export-in-VRM-0-x-format) — *different* VRM version capabilities.
- [VSeeFace official manual](https://github.com/emilianavt/VSeeFaceManual/blob/master/README.md) — documented VRM0-only limitation.
- [Warudo character documentation](https://new-docs.warudo.app/docs/assets/character) — VRM character import, expressions and motion-tracking setup.
- [VRM Add-on for Blender](https://github.com/saturday06/VRM-Addon-for-Blender) — model-import/export tool; check version.

### AI-assistance tools (verify per-model licenses)
- [Meta SAM 2](https://github.com/facebookresearch/sam2) — promptable segmentation, not recovery of unseen pixels.
- [Real-ESRGAN anime model](https://github.com/xinntao/Real-ESRGAN/blob/master/docs/model_zoo.md) — illustration-oriented x4 upscaling candidates.
- [Tencent Hunyuan3D-2](https://github.com/Tencent-Hunyuan/Hunyuan3D-2) and [setup.py license notice](https://github.com/Tencent-Hunyuan/Hunyuan3D-2/blob/main/setup.py) — AI mesh/texture research; **review non-commercial restriction and version/license terms before use**.

---

**Evidence boundary:** This file reports researched capabilities and recommended processes. It neither changes the OrangeScarf model nor certifies any asset, plugin, generated 3D mesh or tracking runtime as validated.
