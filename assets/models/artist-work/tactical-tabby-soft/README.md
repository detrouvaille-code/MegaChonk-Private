# Tactical Tabby - softer revision

Version 2 of the seated orange cat modeled from your `IMG_0664.jpg` turnaround.

This revision has a continuous head and muzzle, smaller eyes that follow the
face, curved hollow ears with thin rims, rounded fabric pouches and shoulder
straps, painted hip stripes, and a smoother tail. Separate cone-like crown
tufts and the stacked rigid borders on the front panels were removed.

## Your files

- `tactical-tabby.blend`: editable Blender source with named parts, materials,
  posing rig, studio lights and camera. Your reference drawing is packed inside.
- `tactical-tabby.glb`: portable colored 3D model and four simple preview motions.
- `cat-preview.png`: the revised model at a three-quarter angle.
- `previews/`: front, side, back, face, browser and before/after previews.
- `start-preview.bat`: double-click to launch the local rotatable viewer with
  Python installed. Keep its terminal open while viewing.
- `source/build_tactical_tabby.py`: reproducible Blender modeling script.

Open the `.blend` in Blender, or import the `.glb` into a compatible 3D editor.
The Blender text `START HERE - Tactical Tabby` explains the posing setup.
Available motions are Idle, LookAround, TailWag and PawWave. This seated posing
rig does not include a finished walking or facial-animation system.

The original version is preserved in the neighboring `tactical-tabby` source
folder and in the original files in `Your-Cat-3D`.

## Verification

Blender 3.4.1 exported and re-imported the GLB. The editable source was separately
reopened with its packed drawing, 107 mesh parts, 11 bones, normalized weights
and finite geometry. The model has 222,432 triangles. Sampled poses in all four
motions stayed above the floor within floating-point tolerance.

Edge/Three.js loaded all four motions without browser errors. The two ear
materials produce 109 skinned render primitives from 107 source mesh parts.
View buttons, turntable and the 390x844 phone layout were checked. See
`verification.json` and `source-verification.json` for the results.

This remains a separate art candidate. The active Mega Chonk model and gameplay
have not changed. Game animation integration and gameplay tests were not part
of this revision.

## Editing and rebuilding

The `.blend` is editable. Save manual edits to a new file before rebuilding;
the script recreates its generated files. To generate a separate copy:

```
blender --background --factory-startup --python source/build_tactical_tabby.py -- --output-dir path/to/new-folder
```

The default output in the repository is `assets/models/artist-work/tactical-tabby-soft`.
It never loads or rewrites the game's canonical Turkish Van model.

The design reference was supplied by the user. Geometry was authored for this
reference without reusing a third-party model. This handoff does not change
ownership of the reference artwork. The optional viewer uses Three.js under
the MIT license included in `viewer-vendor/LICENSE`.
