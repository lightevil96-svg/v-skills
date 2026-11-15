# Live2D → VTube Studio: Operational Runbook for a New AI Agent

**Target:** obtain a REAL editable Live2D Cubism source and a correctly imported VTube Studio avatar. **This is not an autonomous exporter.** Cubism Editor is the principal authoring/export dependency. AI can plan, inspect assets, assist with masks/textures, generate validation reports and operate an accessible GUI **only if the tool environment allows it**. If there is no GUI, stop at the last verifiable gate. Read [START_HERE_AGENT.md](START_HERE_AGENT.md) and [the QA matrix](PRODUCTION_QA_MATRIX.md) first.

## Step 0 — Confirm the environment and input

1. Find real input paths. Record checksum for source files. Choose exact output format: Live2D for VTube Studio, NOT VRM.
2. Check available **Live2D Cubism Editor version, installed license tier and actual GUI operation**. FREE limitations may block saving/export for more complex models; use official [FREE vs PRO comparison](https://www.live2d.com/en/cubism/comparison/); do not claim output if blocked. Do not invent CLI/export API.
3. Check actual source type: layered **material-separation PSD**, Cubism **.cmo3**, flattened image, or compiled-only **.moc3**. A .moc3 cannot substitute for a full editable .cmo3 rig.
4. Record platform and intended VTube Studio runtime. Use explicit source-rights/asset-license/permission gate for reconstruction and external AI uploads.
5. If only a flattened image: produce an honest layer reconstruction *proposal*, not claims about full 3D facial depth. Inpainting can propose missing pixels but does not reveal real hidden anatomy.

**Gate A:** complete inventory + source preservation + target confirmed + authoring software availability documented.

## Step 1 — Character art and material separation

1. Establish canonical identity sheet: eyes/iris, face outline, hair part, outfit/accessories, palette, perspective and intended head range. Compare every generated derivative against it.
2. Map the required independently moving pieces (example categories, **not mandatory exact layer counts**):
   - head base/skin (without independently animated eye/mouth pixels); ears, neck;
   - each brow, upper/lower eyelid and lashes, sclera, iris/pupil/highlight; optionally upper/lower eye shadow;
   - mouth closure line, lip/shadow and the **underlying cavity/tongue/teeth** if needed;
   - back/side/front hair, bangs, individual locks for physics and proper occlusion;
   - torso, clothing overlays, separate shoulders/upper arms/forearms/hands according to intended movement;
   - scarves/accessories separated into independent physics groups where necessary.
3. Draw or explicitly approve **hidden/overlap fill** behind bang, jaw, eyes, mouth, neck and articulated joints. Never reveal transparency or a second baked-in eye behind dynamic overlay.
4. Preserve the true editable material-separation PSD. For importing into Cubism, create a **separate import PSD** with each material part's line/fill/clipping merged appropriately into one raster texture layer per part. Avoid duplicate layer names, unsupported blend-mode differences and unresolved layer masks.
5. Inspect alpha halos and occlusion over both light and dark backgrounds, at native size and actual stream crop. Reject changes to iris/line art/outfit not authorized by user.

**Gate B:** show named layer inventory, depth map, clean source and import PSD with actual visible separated materials. If AI cannot produce honest part artwork, label 'ART BLOCKED' and give exact missing parts.

Official: [Material separation](https://docs.live2d.com/en/cubism-editor-manual/divide-the-material/), [Preparing PSD for import](https://docs.live2d.com/en/cubism-editor-manual/reimport-psd/), [PSD import](https://docs.live2d.com/en/cubism-editor-manual/psd-import/).

## Step 2 — Cubism import, ArtMesh, and deformer structure

1. Open Cubism Editor Modeling Workspace; drag/drop the **import PSD**, choose **Create new model from PSD** and confirm layers become separate ArtMeshes. Save an actual model source as `<name>.cmo3` in a versioned working folder; don't overwrite baseline.
2. Inspect Parts/Deformer palettes and draw order. Correct overlapping bang, hair, neck, eyelid, eye-white, pupil, mouth cavity and clothing order. Hide individual ArtMeshes to verify proper underpaint.
3. Run starter automatic mesh generation early **before complex keyforms**, then manually refine around eyelashes, mouth, hair tips, jaw and outlines; prevent degenerate/sliver triangles and bridging transparent gaps. Avoid unnecessary high-density subdivisions on rigid clothing.
4. Build a sensible hierarchy: body/root → neck/head → facial region deformers; independent hair chains from head, limbs from shoulders, clothing from body. Use warp deformers for organic contours; rotation deformers for joints/pivots. Ensure children are inside parent warp coverage; avoid accidental double-applied transforms.
5. Save a neutral-pose checkpoint `.cmo3`. If editor lacks a needed tool or can't save because license limits, do not fake an editor file.

**Gate C:** evidence of real editor import, non-duplicated facial features, correct mesh/parent/depth order, a saved genuine editable `.cmo3`.

Official: [PSD import](https://docs.live2d.com/en/cubism-editor-manual/psd-import/), [Deformers](https://docs.live2d.com/en/cubism-editor-manual/deformer/), [Mesh editing](https://docs.live2d.com/en/cubism-editor-manual/mesh-edit/).

## Step 3 — Parameter contract and keyforms

Define parameter IDs/ranges/defaults in a table BEFORE building expressions, physics or motion. Suggested **starting conventions** (confirm exact ranges in model and app, do not hardcode to all projects):

| ID | Example min/default/max | Keyforms and visual check |
| --- | --- | --- |
| `ParamAngleX`, `ParamAngleY` | −30 / 0 / +30 | 3 keys each + all 9 X/Y combined poses |
| `ParamAngleZ` | −30 / 0 / +30 | head roll without neck tearing |
| `ParamEyeLOpen`, `ParamEyeROpen` | 0 / 1 / 1 | closed, quarter, half, three-quarter, open |
| `ParamEyeBallX`, `ParamEyeBallY` | −1 / 0 / +1 | gaze without clipping |
| `ParamMouthOpenY` | 0 / 0 / 1 | 0%, 25%, 50%, 75%, 100% |
| `ParamMouthForm` | −1 / 0 / +1 | sad/neutral/smile at multiple openness values |
| `ParamBreath` | app/model-specific | subtle breathing, no jaw/face distortions |
| hair/cloth/arm params | model-specific, unique IDs | compatible with intended physics/tracking ownership |

1. Select relevant mesh/deformer and add parameter keys in Cubism's **Parameter** palette. Edit each extreme **on the correct key**, then return to default to compare. Save frequently.
2. Angle X: adjust perceived front/side face plane, ear visibility, iris perspective and bangs. Angle Y: face up/down, eyelids, neck/jaw. Angle Z: coherent head rotation independent from fake warping.
3. Construct diagonal X/Y combinations with editor-assisted corner synthesis where appropriate, **then inspect all 9 positions** and manually correct; save checkpoint before any automatic regeneration, which may overwrite manual work.
4. Build left/right eyelid independently. Verify corners of mouth under `MouthForm` as openness changes. Do not create a mouth simply by stretching a fixed texture over the face.
5. Face-motion auto-generation in Cubism is a **starting tool** documented for front-facing faces, not a complete premium rig nor a replacement for checking diagonals.

**Gate D:** 3×3 angle proof, Z extrema, eye and mouth interpolation screenshots; every displayed state preserves identity and layer order. A single nice neutral render does NOT satisfy this gate.

Official: [Parameters](https://docs.live2d.com/en/cubism-editor-manual/parameter/), [Keyform editing](https://docs.live2d.com/en/cubism-editor-manual/edit-parameters/), [Auto facial motion](https://docs.live2d.com/en/cubism-editor-manual/face-auto-edit/).

## Step 4 — Expressions, physics, and optional motions

1. Define a parameter ownership table: camera tracking (head/eyes/mouth), expression presets (brows/cheeks/etc), idle/breathing, physics output (hair/scarf) and one-shot motions. Avoid hidden priority conflicts when multiple systems drive the same ID.
2. Configure expressions in available Cubism/Viewer workflow; ensure each preset has deliberate default restoration. Test with open/closed eye and moving mouth. Do not invent expression files with invalid structure.
3. In physics editor, tune pendulum chains, source axes, destination parameter ranges, normalization, weights and damping. Verify slow/fast turns and settling. Save/export physics **registered in the actual model manifest**.
4. If animations are required, author in Cubism animation workspace, save editable animation source `.can3`, then export `.motion3.json`; verify motion names/IDs are registered in `.model3.json` as needed. Not all rigs require every Hiyori motion/animation.
5. Lip sync can use standard open/form mouth parameters; more elaborate viseme/motion sync needs prepared shapes and explicit target-app verification. Do not claim advanced phoneme accuracy from one mouth-open value.

**Gate E:** expression × blink × mouth matrix; hair/scarf settling preview; relevant files and IDs recorded. Report uncreated optional motions plainly.

Official: [Physics](https://docs.live2d.com/en/cubism-editor-manual/physics-operation/), [Motion Sync](https://docs.live2d.com/en/cubism-editor-manual/motion-sync/).

## Step 5 — Export for runtime (actual application required)

1. In Cubism Modeling Workspace use **File → Export For Runtime → Export as .moc3 file** (labels/locations may vary by version). Select a version **supported by actual target VTube Studio**; avoid beta formats unless supported. Choose SDK export.
2. Export textures and choose to export **Physics settings file** with model export so it is properly registered in `FileReferences`. Preserve real generated `.moc3`, `.model3.json` and textured PNGs; don't invent or rename without updating refs.
3. For animations, export genuine `.motion3.json`; for expressions/pose configured in Cubism Viewer, export model settings / `.model3.json` with linked files as per official docs.
4. Check model3 JSON and all referenced asset paths. Avoid moving files out of reference-relative subfolders to superficially match another model. Filename case must agree.
5. Create a clean runtime package with one model directory; put `Source/`, reports, original PSD and `.cmo3` into a **separate development bundle**. If using the repo's repacker, read its scope and security limitations before use.
6. Re-extract and run a **static** manifest/reference inspection. Note: even a passing static test does not inspect all MOC3 binary internals or certify correct rendering.

**Gate F:** real exporter output exists; model3 resolves to a real binary and texture(s); output archive reopens and extracts cleanly; no unrelated docs in model runtime folder.

Official: [Runtime export](https://docs.live2d.com/en/cubism-editor-manual/export-moc3-motion3-files/), [VTube Studio import](https://github.com/DenchiSoft/VTubeStudio/wiki/Loading-your-own-Models).

## Step 6 — Actual VTube Studio integration

1. Place the extracted **model folder** (not the parent dev ZIP and not just JSON) under VTube Studio's `StreamingAssets/Live2DModels` via its in-app folder button; restart app after adding while running.
2. Pick model in VTS; confirm it renders and the app creates a `.vtube.json` if needed. Inspect logs if it does not load.
3. Confirm VTS parameter mapping for head XYZ, brows/eyes, eye-gaze and mouth: parameter **IDs** matter more than display names. Calibrate real webcam/phone tracker.
4. Test neutral, left/right/up/down, diagonals, Z, blink and partial blink, talking, eye-look, expressions, physics and motion return to idle.
5. Record target OS/app version, tracking device, stream crop, short video evidence and observed app performance. This is the only basis for declaring an actual runtime success.
6. If runtime not available, write **'VTube Studio: NOT RUN'** and instructions, not 'Ready/Success'.

**Gate G:** successful actual import and tracking with measured evidence. Do not claim 'stream ready' until run-through/QA results are accepted.

## Step 7 — Final handoff and limitations

Your answer must identify:
- Source and saved files (including SHA-256 when computed), which user files remain unchanged;
- Genuine editor/output artifacts versus intended/missing placeholders;
- ArtParts/mesh/parameter/expression/motion counts from actual source, if measurable;
- Exact gate status A–G, failures and visual evidence;
- Whether actual Cubism and VTube Studio GUI tests were performed;
- User-visible *one next action* for blocked items.

See [START_HERE_AGENT.md](START_HERE_AGENT.md), [TROUBLESHOOTING_AND_LIMITS.md](TROUBLESHOOTING_AND_LIMITS.md), and [PRODUCTION_QA_MATRIX.md](PRODUCTION_QA_MATRIX.md).

**Key source distinction:** this runbook is a human/GUI-operable procedure plus AI assistance; it is not a file generator capable of synthesizing a proprietary Cubism binary without an authentic exporter. Mark each unexecuted step NOT RUN.
