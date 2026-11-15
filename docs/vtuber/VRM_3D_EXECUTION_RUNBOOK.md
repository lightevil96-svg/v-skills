# 3D VTuber / VRM Execution Runbook (2026-11-15)

**Read [START_HERE_AGENT.md](START_HERE_AGENT.md) first.** This route is for an explicitly chosen VRM-compatible **3D target**, **not VTube Studio** (which takes Live2D .moc3). An image-to-3D render, static mesh or .vrm extension alone does not establish a tracking-ready character. Follow the same honest stage/evidence gates and [QA matrix](PRODUCTION_QA_MATRIX.md).

## 0. Capability and version preflight

1. Identify target app **before** creating the 3D character; record exact supported VRM **0.x vs 1.0** versions and tracking features.
2. Identify whether edit source is `.vroid` or `.blend`, and verify that VRoid Studio or Blender with compatible [VRM add-on](https://vrm-addon-for-blender.info/en-us/) can actually be operated. A `.vrm` is not a native editable `.vroid`; preserve sources separately.
3. Confirm rights for original character art, outfits, hair presets, textures, AI geometry services and export/distribution.
4. Choose export path carefully: VRoid Studio **model editor** documentation offers VRM0/VRM1 selection; its separate **dress-up feature** exports VRM1-only. Official VSeeFace docs still say VRM0-only. **Don't choose a VRM1-only route if VSeeFace is the required app.**

**Gate 0:** confirmed source license, actual software and compatible export target.

## 1. Concept and geometry

1. Define one identity sheet (front/side/back and expressions), consistent stylized proportions, eye scale/color, hair and clothing references. For 3D the back of head/clothes must exist; image-to-3D often approximates unseen surfaces.
2. Choose **VRoid Studio** for a character within its editable preset workflow, or **Blender** for custom geometry. If user only supplies AI 2D images, do not claim these already constitute a textured, rigged 3D character.
3. For AI-generated meshes, treat as **unverified base proposals**: check holes, normals, duplicate faces, topology, inside-out mesh, nonmanifold defects when relevant, missing back geometry, intersecting clothes and eyes/teeth/hair.
4. Retopologize deforming areas (eyelids, mouth, jaw, shoulders, elbows, knees) so skeleton and expressions can work without tears. Keep separate construction meshes as justified by actual deformation.
5. Create UV maps, texture/materials and style consistency at stream crop. Verify adequate polygon budget and real target device performance rather than assuming high poly/large textures equal quality.

**Gate 1:** mesh turntable + wireframe front/side/back + UV/material screenshots from actual application, source file saved.

## 2. Skeleton, facial expressions, gaze, secondary motion

1. Set a valid humanoid bone structure/rest pose and skinning weights. Verify the target VRM version's required humanoid bone IDs; fix wrist, knees, shoulder twist and neck deformation across representative poses.
2. Author facial morphs/VRM expressions for blink, smile/happy, sad/angry/surprised, and vowel/lip-sync shapes appropriate to tracker. Don't claim expressions merely because names appear; inspect resulting mesh with combinations.
3. Configure look-at as bone or expression-based gaze according to target runtime. Confirm iris position and not clipping through face when looking left/right/up/down.
4. Set hair/clothes spring bone chains and colliders. Test fast head rotation, side look, recoil/settling; avoid body/face penetrations, runaway oscillation.
5. Review VRM1 expression overrides for blink/mouth/look-at and the runtime update order. Save actual editable VRoid/Blender project, not just a VRM export.

**Gate 2:** actual deformation and mixed expression tests, clean rigging, no missing bones/morphs, evidence that springbones operate in intended renderer.

## 3. Genuine VRM export and target integration

1. Export using **an actually installed and working exporter**; choose exact VRM version supported by the tracking app and include required metadata/license fields, humanoid and expression data. A renamed GLB/JSON is not a valid VRM model.
2. Fresh import into a separately installed VRM runtime; record exact app/exporter version and any warnings. Do not infer compatibility from “supports VRM” when version is unspecified.
3. Connect tracker/camera and test head/torso (if supported), blink, gaze, lip-sync, expressions, spring bones, hotkeys and representative streaming performance.
4. Save project source, genuine `.vrm` output, texture/license metadata, contact sheet/short video, versioned package and report in separate source/runtime folders.

**Gate 3:** real export file exists and has been read by target app. **Gate 4:** tracked actual runtime test passes (not just a successful file import).

## 4. Common blockers / honest fallbacks

- **Only a single front image:** propose editable geometry reconstruction and known/unseen body anatomy for approval; cannot guarantee a high-fidelity volumetric avatar.
- **AI mesh without proper rig/morphs:** deliver an explicit **3D candidate**, NOT a finished VTuber.
- **Blender/VRoid unavailable:** deliver approved plans, texture candidates and QA notes only; mark native export **NOT RUN**.
- **VRM0-only app + VRM1-only exporter:** choose a supported VRM0 export path with rights; otherwise stop incompatible export rather than forge metadata.
- **Only exported `.vrm`:** a 3D runtime model may be importable, but it is not the same as a source VRoid project.
- **Runtime missing:** stage stays exported; face tracking/hair performance **NOT RUN**.
- **License or consent unknown:** do not publish/source-share or upload to external AI services.

## 5. Acceptance checklist

- [ ] Source preserved, authorized, and editable `.vroid` or `.blend` actually exists
- [ ] Face/hair/outfit match approved front/side/back concept
- [ ] Geometry and UVs checked, deformation joints retopologized as needed
- [ ] Humanoid skeleton/skin weights visibly tested across limb/neck poses
- [ ] Eyes, mouth/visemes, emotion blendshapes/VRM expressions checked individually and combined
- [ ] Look-at and springbones tested with target renderer, minimal clipping
- [ ] Export is genuine and in the **target's supported VRM version**
- [ ] License metadata and third-party assets verified
- [ ] Target tracking app import and actual tracker/video/performance evidence
- [ ] Final model/demo status reported as `DONE`, `BLOCKED` or `NOT RUN` per gate

## Official references

- [VRoid: .vroid versus .vrm](https://vroid.pixiv.help/hc/en-us/articles/23731198070809-About-file-formats-used-by-VRoid-Studio)
- [VRoid model-editor export options](https://vroid.pixiv.help/hc/en-us/articles/15760756822297-I-want-to-learn-more-about-the-VRM-export-feature)
- [VRoid dress-up feature export: VRM1 only](https://vroid.pixiv.help/hc/en-us/articles/38726063278233-How-do-I-export-a-model-as-VRM)
- [VSeeFace manual: VRM0 only](https://github.com/emilianavt/VSeeFaceManual/blob/master/README.md)
- [VRM 1.0 specification](https://github.com/vrm-c/vrm-specification/blob/master/specification/VRMC_vrm-1.0/README.md)
- [VRM add-on for Blender](https://vrm-addon-for-blender.info/en-us/)
- [VRM expression spec](https://github.com/vrm-c/vrm-specification/blob/master/specification/VRMC_vrm-1.0/expressions.md)

This is a **workflow**, not a claim any .vroid/.blend/.vrm was produced or tested in this audit.
