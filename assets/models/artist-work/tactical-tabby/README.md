# Your Tactical Tabby 3D character

Modeled from your supplied `IMG_0664.jpg` front, side and back drawing.

- **tactical-tabby.blend** — editable Blender source, separate named parts,
  materials, a posing skeleton, studio lighting and camera. The reference image
  is packed into the file. Open the `START HERE - Tactical Tabby` text in Blender
  for animation/posing notes.
- **tactical-tabby.glb** — portable 3D model with its colors, skeleton and four
  simple preview motions: Idle, LookAround, TailWag and PawWave. No separate
  texture files are required.
- **previews/** — actual Blender renders from front, side, back and three-quarter
  views, a face close-up, and a browser preview.
- **reference.jpg** — your supplied drawing, retained for comparing the model.
- **preview.html** and **viewer-vendor/** — local interactive viewer. Drag to
  rotate, scroll/pinch to zoom, choose a motion, or use the turntable button.
- **source/build_tactical_tabby.py** — the reproducible Blender modeling script.

## Open the 3D model

Open the `.blend` in Blender, or import the `.glb` into a compatible 3D editor.
The head, ears, jaw, front legs, haunches and tail have posing bones. Gear moves
with the appropriate body part. The rig is intended for this seated design;
it is not a finished walking or facial-animation rig.

To use the interactive viewer, double-click **start-preview.bat** on Windows
with Python installed. Keep its terminal open while viewing. You can also run
`python preview.py` from this folder. Everything is served on your own computer;
the viewer does not upload the model.

## Scope and verification

The source was built with Blender 3.4.1. The model has 91,204 triangles, 156
separately editable skinned meshes, one skeleton with 11 bones, and four motions.
The GLB was re-imported into Blender and loaded in the Three.js viewer in Edge.
All four animation clips loaded, and sampled animated bone transforms were
finite. Front/side/rear views were visually reviewed. See `verification.json`.

This is a separate character art candidate. It has not replaced the playable
Mega Chonk cat. Walking, jumping, grooming and combat clips, collision/camera
fitting, optimization and gameplay checks would be part of game integration.

## Editing and rebuilding

The `.blend` is the editable source. Save your hand edits to a new copy; running
the generator again recreates the generated files and would overwrite such edits.
For a separate generated copy, run Blender in a new background process:

```
blender --background --factory-startup --python source/build_tactical_tabby.py -- --output-dir path/to/new-folder
```

The current game's canonical Turkish Van files and generator remain separate.

## Source and credits

The character design reference was supplied by the user. This model's geometry
was authored for that reference; no existing game-cat mesh or third-party model
was reused. This handoff does not assign or change ownership of the supplied
artwork. The optional viewer uses Three.js, under the MIT license included in
`viewer-vendor/LICENSE`.
