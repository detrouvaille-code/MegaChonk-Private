# Tactical Tabby coat remodel

User-requested local model/texture revision, 2026-10-19 (Asia/Shanghai), on
`main` at `e3a342b` with the previous uncommitted playable-character work intact.
Originally prepared locally. The user authorized GitHub publication on
2026-10-19; see `MEMORY.md` for the release revision and deployment evidence.

Local loading follow-up: use
[the orange-character link](http://127.0.0.1:4173/?character=tactical-tabby&v=tactical-fur-20261019)
with the local server running. The entry module and model now carry revision
queries; the GLB revision matches its SHA256 prefix. `start-game.bat` uses
`tools/serve_game.py` to avoid the failing Windows Store Python alias, serve
fresh local files, and avoid competing local servers. The user's existing
matching server was preserved. Repeated tactical integration and the local
Pages check passed with the actual versioned GLB hash and no browser errors.
No model regeneration or gameplay changes were needed for this loading fix.
A separate fresh-browser check of that direct link selected Tactical Tabby
without using the dropdown, fetched the exact revised GLB, and verified the
coat maps on 40 runtime coat primitives with no browser errors. The delivery's
`Previews/in-game-closeup.png` is an actual game render with a temporary test
camera zoom for inspection; normal gameplay camera settings are unchanged.

The reference is the supplied golden-orange furry tactical-kitten turnaround.
The model now has fuller lower cheeks, a gently shaped brow/muzzle, rounder
eye apertures, fine whiskers, softer cream muzzle boundaries and copper
forehead marks painted across the coat. Cream paws, pale ear furnishings and
the pale tail tip retain the reference's color placement. Tactical equipment
remains attached to the same rig and uses a more matte fabric finish.

The skin uses UV-mapped directional fiber color/normal detail. Fine curved,
tapered, alpha-masked strand ribbons add actual depth and a fuzzy silhouette
on thirteen head/ear/body/leg/paw/tail surfaces. These are skinned meshes,
not Blender-only particle hair. Torso fur follows the body's Chonk shape;
the head and paws retain their size. Seven animation names, scale, movement
physics, collision capsule and controls are preserved.

The new runtime material handling retains embedded color maps, normal maps,
vertex colors, double-sided strand rendering and the alpha cutoff. This is
necessary because the previous fur override discarded artist image maps.
The canonical Turkish Van and independent orange rescue NPC keep their
existing appearance and behavior.

The final asset contains 303,788 triangles, 106 skinned render primitives,
32 bones and seven clips. The GLB is 26,933,024 bytes with SHA256
`3c84497eef98cb7e65d6c20d00224647dbd90b721b88be903c0641d6108eee27`.
The opaque coat casts the game shadow; fine subpixel strands skip the additional
shadow passes. Local headless Edge measured 23.64 median FPS and 42.6 ms p95
frame time at 1440x900. These are workstation measurements, not device guarantees.

## Sources and delivery

- Editable gameplay source: `assets/models/tactical-tabby-game-cat.blend`.
- Runtime model: matching `.glb`; all textures are embedded.
- Geometry/rig/animation pipeline: `tools/build_tactical_game_cat.py`.
- Coat/UV/strand authoring: `tools/tactical_fur.py`.
- Original shape helpers: `tools/build_tactical_tabby.py`.
- Editable textures: `assets/models/textures/tactical-tabby/`.
- Exact texture prompt and provenance: [TEXTURE-SOURCE.md](../assets/models/textures/tactical-tabby/TEXTURE-SOURCE.md).
- Actual Blender action/view renders: `assets/models/tactical-tabby-game-previews/`.
- Local delivery copies: parent workspace `Your-Cat-3D/Fur-Remodel/`, with
  animated GLB, editable Blender source, PNGs, prompts, views and an in-game image.

The tintable strand atlas and soft undercoat color map were made with the
built-in image_gen tool. Fine tangent-space normal relief is authored
deterministically by the coat script. All image dependencies are packed into Blender.
The first wide-lock draft looked coarse in close-up and was replaced by
individual fine tapered strands before the gameplay handoff.

This matches the supplied color placement and plush fur style more closely.
It is a real-time interpretation, not an exact reconstruction of the reference's
offline fur groom, unseen anatomy or studio lighting. Inspect the actual game
and Blender previews when judging the result.

The earlier seated models and original playable delivery are preserved.
Preserve manual edits before regenerating: the procedural pipeline overwrites
its own gameplay outputs. It runs in a separate background Blender process.

## Verification

The revised model passed Blender export/re-import, embedded PBR/alpha-mask
checks, and an independent reopen of the final Blender source. All vertices
have normalized weights with at most four influences. Twenty source pose
samples passed the existing floor bound; the lowest fine strand was -0.0206
units in Sit/Groom, inside the -0.025 test tolerance. This is sampled inspection,
not a claim of zero penetration at every vertex/frame.

The dedicated browser check passed both-way character switching, persistence,
all seven actions, 35 finite deformed poses, body/clothing/torso-fur Chonk,
independent rescue-NPC appearance and phone boot layouts. It explicitly checks
the actual game's coat UVs, vertex colors, undercoat/normal images, strand atlas,
double-sided rendering and alpha cutoff.

Default Turkish Van smoke, custom vertical routes and the complete emulated
touch suite passed. Touch checks include all four phone layouts, multi-pointer
input, all actions, boss loss/retry/victory, restart and desktop virtual-control
toggle back to real keyboard movement. The requested custom character is
asserted on both phone and desktop. The desktop portion uses a fresh browser
after releasing the phone's GPU context. Initial short-delay action/toggle
checks failed and were changed to await real cooldown completion and movement;
the assertions and input requirements remain intact. A first five-second
catnip-consumption wait timed out; the same boost condition passed with a
bounded 15-second wait. Initial startup attempts also timed out; only the
completed fresh run is counted as the touch-suite pass.

The runtime-only package passed under `/MegaChonk/`: 36 files / 39.57 MB,
both served-model hashes, three mission layouts, movement and jumping.
The packaged test recorded one completed-model Edge ERR_ABORTED notice after
full parse/hash verification, as described in the initial integration notes;
other errors remain fatal. All source/runtime/manifest hashes matched.

The full keyboard-driven campaign passed with seed 424242: eight meals,
orange-cat rescue and vacuum victory, 865 XP including a checkpoint bonus,
13 jumps / 5 bonks in 3m24s. No room Continue was needed in this passing run.
The driver now distinguishes combat/checkpoint recovery from a cleared room,
fixing a false first-room gate failure without changing gameplay. A separate
initial attempt exhausted nine room lives with one guard hit left; the driver
now understands the real Continue button with a three-continue safety limit.
Campaign navigation/combat use normal input; health/objective state is not
mutated to finish the run. Focused pose/vertical/touch scenarios deliberately
place the character at test starts and are separate evidence.

Changed JS/Python syntax and Git whitespace checks passed. Delivery GLB/Blender
copies match the gameplay files byte for byte. The canonical Van GLB retains
SHA256 `a2e47a69b82af295e3d30f8d2186760907e827f02c72c85ced2fa1a0bebe126d`.
Release preparation on 2026-10-19 also passed a second full custom campaign,
seed 765432: eight meals, orange-cat rescue, vacuum victory, 865 XP, 14 jumps /
2 bonks in 5m16s. Syntax, pure adventure/condition rules and runtime packaging
passed again. Physical phones/Safari remain untested. Public hosting and the
additional condition check are recorded separately when completed; earlier
results in `tactical-character.md` apply to the preceding model.
