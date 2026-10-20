# Playable Tactical Tabby

Implemented locally from `main` baseline `e3a342b` on 2026-10-18 (Asia/Shanghai).
This contribution is not a commit, push or public deployment.

This document records the initial 2026-10-18 integration and its verification.
The 2026-10-19 geometry/texture revision and current asset metrics are in
[Tactical Tabby coat remodel](tactical-fur-remodel.md).

## Player behavior

The start screen offers Turkish Van and **Tactical Tabby - your orange cat**.
The choice is saved in this browser and can be changed before starting a run.
The Turkish Van remains the default; `?character=tactical-tabby` opens the custom
character directly. Both use the same collision, camera, movement, nutrition,
jump and combat rules. The vest/headset are cosmetic, while collar/pendant
pickups retain their existing effects.

The custom cat has interpolated Idle, Walk, Sit, Groom, Jump, Claw and Bite
clips, with an eating loop derived from Bite. The rig has articulated front and
hind legs, paw targets, head/jaw/ears, eyelid blinks and six tail bones. Authored
Chonk shapes enlarge its torso and gear together. The head and paws retain their
size. The character choice persists across run restarts.

The rescue NPC always comes from a separately cached Turkish Van template,
recolored orange. Its geometry/materials/skeleton remain independent, and it
never acquires the tactical player's gear. Exactly three guards, two successful
claws each, saved partial damage, gate opening and rescue XP remain intact.

## Assets and authorship

- `assets/models/tactical-tabby-game-cat.blend`: editable gameplay source.
- `assets/models/tactical-tabby-game-cat.glb`: portable runtime model and clips.
- `assets/models/tactical-tabby-game-previews/`: actual Blender action/view renders
  plus export and independently reopened-source verification JSONs.
- `tools/build_tactical_game_cat.py`: original geometry assembly, skin weights,
  32-bone rig, animations and clothing/body morphs.
- `tools/build_tactical_tabby.py`: original character shape/gear helpers.
- `tools/tactical_fur.py`: later UV coat mapping and fine skinned fur strands.
- `tools/generate_stray_style_cat.py`: shared IK and action-authoring helpers;
  its main generator and Turkish Van mesh are not used for the custom model.
- `../Your-Cat-3D/Playable-Character/`: local delivery copies of the GLB and
  Blender source, action/view renders, in-game preview and launch instructions.

The initial asset had 205,232 triangles, 109 source skinned mesh parts and 111
render primitives (the ears use two materials), with seven named clips.
The original user sketch is packed in the Blender source. The later furry
turnaround was used as an additional visual reference. This is a stylized
browser-game adaptation with short opaque mesh fibers and surface shading;
it does not reproduce the reference's individual fur strands or render quality.

The first and softened seated candidates remain in `artist-work/` and the
earlier delivery folders. Neither is the gameplay file. Preserve manual edits
to all Blender sources; regenerating creates a new procedural output rather
than reading an edited Blender project. Use a separate process with
`--background --factory-startup`, never the user's open scene.

## Verification

Blender export/re-import and independent `.blend` reopen passed. The source has
normalized weights with at most four influences, a packed reference, seven
actions and finite geometry. Twenty sampled Idle/Walk/Sit/Groom poses passed
the floor-bound checks. Early sitting/haunch/tail penetration was corrected in
the authored poses, then re-exported and checked.

The dedicated browser character test passed switching both ways, saved choice,
seven actions, 35 sampled poses, body/clothing chonk, room-two NPC isolation,
viewports 320x568 / 568x320 / 390x844 / 844x390 and no browser errors. Small-phone
boot spacing was tightened after the full touch suite caught the credits footer.

Default Turkish Van smoke, visual/blink and desktop/emulated-touch rescue
scenarios passed. Custom vertical, condition and emulated-touch suites passed.
Condition navigation and impact checks now wait for actual arrival/latch/hit
events instead of fixed short delays; nutrition and physical-gate assertions
were retained. The custom condition check measured sprint-jump ranges of 5.151
at normal weight and 2.340 at heavy weight, and retained 110 saved snack points.

Both full keyboard campaigns completed eight meals, the orange-cat rescue and
the vacuum boss. Seed 424242 earned 850 XP with 10 jumps / 4 bonks in 2m44s.
Seed 765432 earned 865 XP including a checkpoint bonus, with 11 jumps / 3 bonks
in 2m25s. The driver now stops routing toward already-consumed food and descends
from the actual gallery height, fixing a false failure after FISH was eaten.
No gameplay rules were changed for these driver corrections.

The local Pages package passed all three mission layouts, custom-character
loading/movement/jumping and served-model hash checks: 36 runtime files,
22.20 MB. The unchanged Van hash is
`a2e47a69b82af295e3d30f8d2186760907e827f02c72c85ced2fa1a0bebe126d`;
the custom GLB hash is
`aec2c26f62acfc36cfedfa9e29bc634d872211469d585f67e0a4099fdfe2fe6b`.
Initial Pages runs failed on Edge `net::ERR_ABORTED` transfer events even
though each affected model had fully loaded. The final check records those
events as explicit notices only for the two exact model URLs after checking
their complete expected mesh/triangle/clip counts and served bytes against
both the build manifest and local source. Every other resource failure and
all console/page errors remain fatal. The final run passed with two such
notices and no console/page errors; default-character smoke also passed.

Changed JavaScript/Python syntax and Git whitespace checks passed. Delivery
copies match the gameplay GLB and Blender source byte for byte. Original and
softened seated assets, the canonical Van, attribution and runtime physics
are preserved. This work is saved in local files; it has not been committed,
pushed or published.

Physical Android/iOS/Safari devices and the public website are not checked in
this contribution. Source-reopen/pose tests and dedicated scenarios place the
character at test starts; full campaign runs use keyboard movement/combat.
