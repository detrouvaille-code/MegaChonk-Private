# Mega Chonk Project Memory

Last updated: 2026-10-20 (Asia/Shanghai).
Latest released gameplay baseline: `3a3e447` on `main`.
Read current Git history before relying on that baseline; this file is not a live
deployment status feed.

## Resume Here

- Private upload verified (2026-10-20): `main` at `f0a5da5e68aab42c007b41df71da7f82c5417731` was pushed successfully to `detrouvaille-code/MegaChonk-Private`. GitHub's branch reference matched the local commit, its complete tree contained 1,539 files including the custom runtime GLB and editable Blender model, and repository visibility was confirmed private. The independent checkout was clean and tracking the new origin. The original public checkout remained at `e3a342b` with its staged/unstaged work preserved. The large Blender file produced GitHub's advisory size warning but uploaded successfully. No website was deployed.
- Separate private repository request (2026-10-20): the user chose a new private repository instead of uploading to the existing public repository. Created and confirmed private: https://github.com/detrouvaille-code/MegaChonk-Private, under the user's device-authorized `detrouvaille-code` account. Prepared `MegaChonk-Private` as an independent local copy with the original Git history through `e3a342b58fc9c8a7f7c6b6922e9a55a71e8602af` plus the latest tracked working files, including staged and unstaged Tactical Tabby work. The original checkout and its index are preserved. This copy's Pages workflow is manual-only; no new website deployment was requested. Fresh validation passed all 12 runtime syntax checks, pure adventure/condition rules, the 36-file / 39.57 MB runtime build, and the local Pages browser test (both complete models and hashes, three rooms, movement/jump, no browser errors). No gameplay or model geometry was changed during repository setup; full campaigns and physical-device checks were not repeated. Uploading this copy's `main` is authorized; the public repository is unchanged.
- Publication authorized (2026-10-19): user asked to host the saved changes in their Git repository. Inspected `main` at `e3a342b`, fetched `origin/main` at `f02c205` (zero remote-only commits); the saved food/rescue commit is included in the authorized publication. Staged the custom character sources, art candidates, mapped fur, seven-action runtime integration, local loading fix, docs and relevant test updates. No runtime geometry/physics changed during release preparation. Fresh syntax, pure adventure/condition rules and runtime packaging passed. The second full custom campaign seed 765432 passed eight meals + rescue + vacuum, 865 XP, 14 jumps / 2 bonks in 5m16s. Existing latest-fur seed 424242 and tactical/vertical/mobile/Pages checks remain separately documented. Upload/deployment evidence will be recorded after verification.
- Local visibility follow-up (2026-10-19): user confirmed the unchanged appearance was at `127.0.0.1:4173`. The current asset already contained the mapped coat. Added its SHA prefix to the GLB URL and a revision to the entry module URL so an older cached request cannot reuse the initial model/loader. The original launcher hit a failing Windows Store Python alias; it now prefers the working Python-manager installation and delegates to `tools/serve_game.py` (explicit checkout, no-store headers, browser after bind, Windows-exclusive port, safe reuse only when served HTML/JS match). An initial restricted CIM port query missed an existing server; netstat and HTTP inspection established the actual matching server, which was preserved. Only the redundant server started during diagnosis was stopped. Fresh tactical integration and the local Pages package passed: maps/normal/strand alpha retained, switching/persistence/actions/poses intact, exact versioned model hash verified, three missions/movement/jump, no browser errors. Launcher no-browser/reuse and isolated no-store/exclusive-bind checks passed. No geometry or gameplay changed, so Blender/full campaign/physical-device checks were not repeated for this loading fix. Local only; no commit/push/deployment.
- Latest character revision: remodel the playable orange cat and map the supplied illustration's coat/fur style. The local Tactical Tabby now has fuller cheeks/refined muzzle, rounder eyes, whiskers, painted copper forehead stripes, cream markings, UV-mapped undercoat/normal detail and fine skinned alpha-masked strands on thirteen surfaces. The GLB has 303,788 triangles, 106 skinned primitives, 32 bones and seven actions; 26,933,024 bytes, hash `3c84497eef98cb7e65d6c20d00224647dbd90b721b88be903c0641d6108eee27`. `tools/tactical_fur.py` and editable PNGs in `assets/models/textures/tactical-tabby/` extend the separate custom pipeline. The loader preserves embedded PBR maps/alpha cutoff and skips fine-strand shadow passes. Built-in image_gen made the tintable atlas and undercoat; exact prompts/provenance are included. This follows the reference's coat style; it is not an exact offline-groom reconstruction. New delivery copies are in parent-workspace `Your-Cat-3D/Fur-Remodel`; original deliveries/art are preserved. See [fur remodel](docs/tactical-fur-remodel.md). Saved locally on `main` at `e3a342b`; not committed, pushed or published.
- Current remodel checks: final Blender export/re-import and independent source reopen passed normalized weights, packed reference and sampled pose bounds. Actual browser textures/UVs/normal map/alpha mask, seven actions, 35 deformed poses, switching/persistence, torso-fur/gear Chonk and NPC isolation passed. Default smoke, custom vertical and complete emulated-touch/boss/retry/desktop-toggle checks passed. Short fixed-delay action/input checks now wait for real cooldown/travel; fresh browsers isolate the desktop phase. The local package passed: 36 files / 39.57 MB, both served hashes and three missions. Sampled local headless performance: 23.64 median FPS / 42.6 ms p95. Full keyboard campaign seed 424242 passed eight meals + rescue + vacuum, 865 XP (checkpoint bonus included), 13 jumps / 5 bonks, 3m24s, no room Continue needed. The driver now distinguishes combat recovery from room completion and can use the real room Continue button if nine lives are spent; initial failed attempts are recorded in the remodel notes. Physical phones/Safari/public hosting, the full condition suite and a second campaign seed were not rerun for this revision.
- Previous playable-character integration (2026-10-18): animate the supplied orange tactical cat and include it as a playable character. The start screen now offers **Tactical Tabby - your orange cat**, remembers the choice, and supports `?character=tactical-tabby`; Turkish Van remains the default. The original custom `.blend`/`.glb` are `assets/models/tactical-tabby-game-cat.*`, generated by `tools/build_tactical_game_cat.py` with the earlier shape helpers. It has 205,232 triangles, 32 bones, seven gameplay clips, eyelid/tail motion and authored body/clothing Chonk morphs. This is a stylized adaptation of the furry turnaround. Physics and controls are shared with the Van; the orange rescue NPC uses an independent Van template and never inherits tactical gear. Source, limits and verification: [playable character](docs/tactical-character.md). Delivery copies, action renders and instructions are in parent-workspace `Your-Cat-3D/Playable-Character`; earlier seated versions are preserved. Inspected baseline: `main` at `e3a342b`. Saved locally, not committed, pushed or deployed.
- Initial integration verification (2026-10-18): Blender export/re-import and independent source reopen passed normalized weights, packed reference, seven actions and sampled poses. Browser switching/persistence, all actions, 35 deformed poses, body/gear morphs and NPC isolation passed. Default Van smoke, visual/blink and desktop/emulated-touch rescue passed; custom vertical, condition and full emulated-touch suites passed. Both full keyboard campaigns completed eight meals + rescue + vacuum: seed 424242 earned 850 XP with 10 jumps/4 bonks (2m44s); seed 765432 earned 865 XP including checkpoint bonus with 11 jumps/3 bonks (2m25s). The autoplay driver now recognizes already-eaten goals and uses the actual gallery floor for descent; condition checks wait for arrival/latch/impact. The local Pages package passed: 36 runtime files / 22.20 MB, both served model hashes and all three mission layouts. Edge reported completed-model abort notices; the test accepts only exact, fully parsed and hash-verified models, reports those notices, and keeps other failures fatal. Physical phones/Safari and live hosting were not checked. Details are in the character verification document.
- Previous seated-art request: make **Tactical Tabby** less blocky. Version 2 remains in `assets/models/artist-work/tactical-tabby-soft/`, with a continuous muzzle, conforming eyes, cupped ears, padded gear and smoother plume. Its source packs `IMG_0664.jpg`; 222,432 triangles, 11 posing bones and four seated motions passed Blender/browser checks. The original 91,204-triangle version is preserved in `tactical-tabby/`; delivery copies remain in parent-workspace `Your-Cat-3D/Softer-Version`. These are separate art candidates, not the new seven-clip gameplay model. Generators overwrite their procedural outputs, so preserve manual edits separately.
- Previous completed gameplay request: level two is **Orange Cat Rescue** in the kitchen. A real skinned orange NPC waits in a cage guarded by exactly three mice. Each guard requires two Claw impacts regardless of pendant damage; bites do not count. All three defeats open the cage, the orange cat walks onto the floor, 100 XP is awarded once, and the pet door unlocks. Partial hits/kills survive deaths and regeneration; a new run resets them. The four kitchen meals are now optional energy food, leaving eight required suppers in levels one/three. The base campaign still earns 850 XP before checkpoint bonuses. Implementation and limits: [rescue verification](docs/rescue-verification.md).
- Previous rescue verification: syntax, adventure rules, rescue desktop/emulated-touch scenarios, smoke, vertical, adventure integration, mobile controls, 90 seeded layouts, and local Pages passed. Both full keyboard campaigns completed eight meals + rescue + vacuum with 865 XP: seed 424242 used 12 jumps/3 combat deaths; seed 765432 used 7 jumps/4 combat deaths. That package had 35 runtime files (12.63 MB). See the latest character verification for the expanded package and current checks.
- The prior cat-food-can change is included: `food-visual.js` supplies repeated cat-face labels, stamped lids and pull tabs for every food role and enemy food drop, with a softer halo. Green marks catnip and blue marks lean food. The playable Turkish Van and canonical `.blend`/`.glb` are unchanged; the orange NPC has independent runtime geometry/materials/skeleton. Inspected baseline is `main` at `f02c205942d048d7b8ca7c1f892e4cab15deee9e`, origin `https://github.com/desmondttm123/MegaChonk`.
- On 2026-10-18 the user requested saving both changes in a local Git checkpoint, titled `Add cat-food cans and orange-cat rescue mission`. No push or deployment was requested; consult Git history for the checkpoint hash.
- Latest released request: make a regenerating food supply available in every level and make running/jumping slim the cat. Each room now has two clearly signed +9-chonk rich bowls that return after 20 seconds without counting as supper progress. Walking still trims gradually, trotting/running burns over 2.5x as much weight at base pace, and each successful jump burns 0.45 chonk down to the existing 26 floor.
- Published gameplay as `3a3e447` through successful Pages workflow `39007873141`. The public manifest matched `3a3e447bc086ba53968bfd82a95394665a17c732` with 33 runtime files and the unchanged canonical model hash; hosted Pages verified all three levels, movement, jumping and no browser errors. Pure condition rules, condition integration (all-room supply plus an actual rich-bowl refill), smoke, 90 layouts, adventure, mobile, vertical, visual-cat, local Pages, and full campaign seeds 424242/765432 passed. The campaigns completed 12 suppers + boss with 850 XP, no deaths/bonks, 4/5 jumps, and finished near 38.92/38.62 chonk without optional food. One vertical test launched during parallel browser load timed out at startup; its isolated rerun passed. Physical phones/Safari were not tested.
- Previous released request: longer average leaps, continuous interruptible eating, meaningful energy/weight, optional point-bearing fattening snacks, starvation life loss, narrow passages, heavy pressure plates and a safe trim/refeed loop. User explicitly requested auto-push. Balance and test boundaries: [condition system](docs/condition-system.md).
- Published gameplay as `c401b65`. Pages workflow `38948118700` completed successfully and the public manifest matched `c401b650238575b5dc795247b1b7471282b20cd6`, with 33 runtime files. Hosted Pages, condition integration, mobile (including boss loss/retry/victory) and camera suites all passed without browser errors. Live sprint range was 5.276 normal versus 2.416 heavy, and 110 earned snack points survived reload. The follow-up changes only handoff evidence/captures, not runtime code.
- Required suppers are separate from optional food: +8 energy/+0.8 chonk, capped at 80 energy. Rich snacks/food drops give +10 energy/+9 chonk/+25 browser-saved points; bonus stashes give +60 points/+3 chonk. No spending UI yet. Starting condition remains 62/48. Warnings and six seconds at zero spend a life, drop the pendant and safely restore energy; room nine-life continue retains meal progress. The boss keeps its own nine-life fight.
- Every room now has optional 60-max slim entry, 64-min latched pressure plate, scratch post (-4 chonk/-1.5 energy per claw) and no-fat recovery food. Refills and occupant-safe exits prevent body-puzzle softlocks. Runtime torso morph and variable capsule radius make weight visible/physical; canonical model and open Blender scene are untouched.
- Condition pure/browser tests, smoke, 90 layouts, adventure, vertical, camera, phone layout/input, visual-cat and local Pages passed. Both full keyboard campaign seeds were repeated after final polish: 424242/765432 each completed 12 suppers + boss, 850 XP, no deaths/bonks, latest 6/4 jumps (earlier 765432 run used 5). Physical phones/Safari and human balance feedback remain outstanding. One first mobile run stalled; fresh bounded local and hosted runs passed, so do not count the stalled run as a pass. A Pages CDP large-response-body eviction was handled in the test with an explicit served-asset hash fallback; packaging/model hashes still must match.
- Previous released request: fair generated jump obstacles, a reusable vacuum boss after room three, persistent accessories, and enemies with guaranteed drops. The adventure implementation is described in [adventure system](docs/adventure-system.md).
- The third pet door now starts the vacuum encounter instead of completing the run. Claw the rear filter; front suction costs one of nine lives. Retry after nine losses resets only the fight. The boss remains winnable without equipment.
- Room-tier collars add pace and survive combat deaths; pendants add claw damage/hunger efficiency and are lost on combat death. Both persist across rooms for the current run. Optional clockwork mice warn/pounce and drop a snack or pendant on defeat. Ordinary environmental bumps remain nonlethal.
- Shared jump rules validate generated hurdles/bridge approaches and reserve takeoff/landing space. Clear objective corridors and stairs remain available to hungry/heavy cats; equipment does not bypass their jump restrictions.
- Published all adventure changes as `74b013e` on 2026-10-17 after the user authorized the push. The Pages workflow and public manifest matched; hosted Pages/mobile/camera checks and a no-equipment keyboard boss victory passed with no browser errors. The evidence follow-up changes only notes/captures, not runtime code. Details and limitations: [adventure verification](docs/adventure-verification.md). The active cat asset is unchanged.
- Adventure rules/integration, 90 generated layouts, smoke/camera, vertical/visual, expanded phone controls, and local Pages checks passed. Full campaign seeds `424242` and `765432` both finished with 12 meals, 850 XP, no deaths, and the boss defeated; a separate keyboard fight also won without any equipment. Scenario setup is explicitly distinguished from no-teleport autoplay in the verification notes.
- The previous mobile release is `39d9265` with evidence-only follow-up `3c9260e`; both deployed successfully. The mouse-spike fix is `cecfb02`. Physical Android/iPhone Safari checks remain outstanding; do not claim hardware performance from emulation.
- Multiplayer and generic extra coat variants remain deferred. The separately requested Tactical Tabby option is implemented; wait for user feedback or a new request before adding more characters or publishing it.

## Product Decisions

- Name: **Mega Chonk**. Single-player browser game with desktop keyboard/mouse and optional phone virtual controls.
- Default visual direction: a believable Turkish Van, mostly white with chestnut ears/tail/patches, smooth animated limbs, subtle idle life, and large dark night-adapted pupils. The user-approved Tactical Tabby is a separate selectable orange cat with black tactical gear/headset. Stray is a quality/control reference, not an asset source.
- The user rejected boxy cats and rigid frame-by-frame sprites. The active character is a real skinned GLB rendered in Three.js. More polygons alone are not the solution to anatomy, clipping, or animation problems.
- The setting is a house with furniture and vertical exploration, not a dungeon. The three missions are Living Room Zoomies, Orange Cat Rescue in the kitchen, and Attic Midnight Run.
- Levels one/three require 3/5 food cans, including one upstairs each. Level two requires rescuing the orange cat by clawing each of three cage guards twice; food there is optional. Reach each pet door after its mission. The third door leads to the vacuum boss. Base completion earns 850 XP including 100 rescue XP and the boss's 250 XP, before optional checkpoint/bonus rewards.
- Required food restores energy with little weight; optional snacks add significant chonk and saved points, not objective progress. Two rich cans per room regenerate for repeatable weight gain. Walking drains weight gradually, running does so much faster, and successful jumps have a small fixed weight burn; balanced condition is fastest. Satiety at or below 8 or chonk at or above 90 blocks jumping. Six seconds at zero loses a life with safe checkpoint energy recovery. See condition-system for tuning.
- WASD/arrows move relative to the camera; W moves away from it, showing the cat's back. Shift trots, Space jumps, Q sits, F/LMB claws, E/RMB bites. Five idle seconds trigger grooming; movement interrupts it and automatic eating immediately.
- Touch uses a left analog joystick, right-side swipe to look, action buttons, and a latched Trot toggle. Use Trot + Jump for longer jumps. Do not require pointer lock or synthesize sticky WASD keys for touch input.
- Claw and bite damage clockwork mice at animation impact time. Only rear-facing claws damage the vacuum. This is a basic combat/equipment foundation, not a finished RPG, networking, or inventory-menu system.
- Equipment is run-scoped in memory, not saved across reloads. Combat death loses the pendant, not the collar. Nine suction losses require a boss retry; ordinary room hazards do not spend boss lives.

## Current Technical State

| Area | Current implementation |
| --- | --- |
| Stack | Buildless JavaScript modules, locally bundled Three.js, no runtime backend |
| Gameplay | `game.js`: world construction, collisions, support surfaces, condition, progression, animation, UI |
| Camera | `camera-controls.js`: filtered input consumed per frame; `game.js`: follow camera and collision recovery |
| Touch | `touch-controls.js`: pointer capture, analog movement, look smoothing, buttons, mode/lifecycle state; `window.__megaChonk.touchSnapshot()` is a test/debug hook |
| Adventure rules | `adventure-rules.js`: run equipment/ownership, boss phase/attack/weak-point registries, health/lives/retry |
| Adventure visuals/AI | `adventure-world.js`: original procedural vacuum, optional mice and three required cage guards, pickups, loot and animation-impact interactions |
| Food visuals | `food-visual.js`: shared procedural cat-food tin, CanvasTexture cat-face labels and lid artwork; all food roles and loot |
| Rescue mission | `rescue-mission.js`: collidable kitchen cage, independent orange skinned NPC, gate/escape animation and protected approaches; guard rules/progress in `adventure-rules.js` |
| Jump planning | `jump-rules.js`: runtime pace/impulse and conservative generation envelope (38 satiety, 75 chonk, no equipment/catnip) |
| Condition | `condition-rules.js`: recipes, metabolism, workouts, body thresholds and browser-local snack points; `body-trials.js`: optional slim/weight puzzles; `cat-condition-visual.js`: Van torso morph / custom authored body-and-gear targets |
| Generation | `course-generator.js`: seeded layouts, grid routes, reserved corridors and swept obstacle envelopes |
| Character | Default `turkish-van-game-cat.glb`: 193,136 triangles, 24 skinned meshes; selectable `tactical-tabby-game-cat.glb`: 303,788 triangles, 106 skinned render primitives, 32 bones |
| Animation clips | Idle, Walk, Groom, Sit, Jump, Claw, Bite |
| House scale | Floor 46 x 42, ceiling 7.2; cat scale 0.84, mass-dependent capsule radius 0.22-0.35, height 0.76; food cans scale 0.70 |
| Vertical route | Gallery height 2.7; 18 stairs with 0.15 rise; protected launch/return shelves |
| Catnip | Optional; 18 seconds of 1.32x speed and 1.18x jump impulse; regrows after 22 seconds; cannot bypass condition limits |
| Course counts | 25/30/37 generated obstacles across the three rooms in verified layouts |
| Debug/test hooks | `window.__megaChonk`: state, navigation, snapshot, cameraSnapshot, seeded regeneration, scenario helpers |

Obstacles, sizes, phases, and some meal positions vary by seed. The structural
stairs/gallery/catnip jump route is intentionally authored and protected, not a
fully random building generator. Floors and collision bounds are world-space.

## Canonical Assets And Pitfalls

- Edit `tools/generate_stray_style_cat.py` to regenerate the active `assets/models/turkish-van-game-cat.blend` and `.glb`, plus `assets/models/game-cat-previews/`.
- The separate `tools/build_tactical_game_cat.py` builds only the custom Tactical Tabby. It reuses shared animation helpers, not the Van mesh or canonical generator's main routine. Both generators overwrite their outputs; preserve artist edits before regenerating. The canonical Van GLB remains unchanged (SHA256 `a2e47a69b82af295e3d30f8d2186760907e827f02c72c85ced2fa1a0bebe126d`).
- Artist instructions: [artist cat guide](docs/artist-cat-guide.md). The from-scratch generator overwrites canonical files and does not read a manually edited `.blend`. Keep artist candidates separate; an accepted manual workflow must explicitly preserve an authoritative source and repeatable export recipe/tool rather than regenerating from the old FBX. No pipeline switch has been made yet.
- Runtime `loadCat()` replaces `TurkishVan.Fur` with vertex-color/procedural-bump shading. Texture-based upgrades need a coordinated material-loader and test update; a better Blender material/render alone will not carry through unchanged.
- Blender 3.4 runs in background mode with `--factory-startup`; it must not touch the user's open Blender scene.
- The active base mesh is Jonas Dichelle's CC BY 3.0 cat at `assets/models/source/jonas-dichelle-cat/cat.fbx`. Preserve source attribution and `credits.html`; no Stray assets are included.
- POINT-domain coat/iris vertex colors avoid the Blender 3.4 CORNER export bug. Keep normalized skin weights and verify all seven clips after export/re-import.
- The face now uses larger almond apertures, round nearly black pupils, a thin amber rim, deeper sockets to avoid lower-eye clipping, and skeletal eyelid blinks.
- Earlier foreleg work raised the elbows, added scapula articulation, smoothed joint weights, reduced paw lift, and improved grooming paw-to-muzzle alignment. Avoid undoing these by switching pipelines.
- `generate_rigged_cat_v2.py`, `generate_rigged_cat_v3.py`, matching v2/v3 assets, standing CC0 assets, and sprite sheets are historical experiments, now tracked. They are not the active pipeline; do not remove them without agreement.
- `generate_sitting_cat_blender.py` and the sitting STL/OBJ are a separate printable-model task. STL has no standard material-color support; colors live in Blender/OBJ materials.
- PNG writes can hit transient Windows locks. Use `tools/capture-screenshot.js` for test captures; the active Blender generator renders to temporary PNGs and replaces completed files.

## Recent Changes

| Commit | Handoff significance |
| --- | --- |
| `71899df` | Animated runtime cat, upstairs routes, catnip, attribution, runtime-only GitHub Pages deployment |
| `f5dc901` | Nearly doubled floor area; cat 37% smaller; protected seeded courses; larger dark night eyes |
| `cecfb02` | Mouse-spike filtering, frame-based smoothing/rate limits, capture/focus guards, camera collision recovery |
| `ef96e40` | Check-in of older experimental assets/tools; active gameplay remains the above version |
| `ee37670` | Repository contributor instructions, persistent memory, setup/test/release handoff |
| `a7a626d` | Artist instructions covering manual/source ownership, rig/material/export constraints, and delivery |
| `39d9265` | Mobile joystick/look/actions, responsive phone layouts, lifecycle cleanup, automated touch verification; deployed and tested live |
| `3c9260e` | Successful live mobile/camera/Pages verification evidence and refreshed captures; same runtime as `39d9265` |
| `74b013e` | Vacuum finale, equipment/death/loot, clockwork enemies, shared fair-jump planning, combat tests and contributor guidance; deployed and checked live |
| `c401b65` | Longer jumps, continuous eating, appetite/weight balance, snack wallet, starvation lives, optional slim/weight trials and runtime body morph; deployed and checked live |

Mouse regression details: old code directly applied every `movementX/Y` event;
an oversized sample rotated yaw by -28.2 radians. A small furniture-corner orbit
also switched the requested camera distance from about 1.25 to 3.38 units.
The fix rejects invalid/oversized deltas, guards lock/focus changes, clears queues,
reduces sensitivity, limits rotation speed, and eases collision-distance recovery.
Do not put direct raw-delta angle updates back into `setupInput()`.

Other regressions to preserve: capsule depenetration when leaving a platform,
gallery underside sweeps, walkable stairs even when jumping is blocked, movement
interrupting food/grooming, and destination-floor planning in the autoplay bot.

## Recorded Verification

The table below records earlier implementation sessions. Current mobile-input
checks are in [mobile verification](docs/mobile-controls-verification.md); latest
adventure checks/autoplay are in [adventure verification](docs/adventure-verification.md).
Re-run relevant tests after changing behavior; do not treat historical results as
evidence for an untested checkout.

| Check | Last recorded result |
| --- | --- |
| Blender export/re-import | 193,136 triangles, 24 skinned meshes, one armature, seven clips |
| Gameplay smoke | Passed model loading, orientation, action states, grooming/eating interruption, condition limits, levels |
| Visual inspection | Four angles and 19 sampled poses; no sampled floor penetration; night eyes/blinks checked; approximately 59.9 FPS locally |
| Generation | 90 layouts (30 seeds x three rooms), deterministic replay, obstacle clearance, reachable lower objectives/stairs/exits; moving-platform carry checked |
| Full autoplay `424242` | 12 meals, 600 XP, 8 jumps, 0 bumps, about 2m 34s after scale/generation changes |
| Full autoplay `765432` | 12 meals, 600 XP, 7 jumps, 0 bumps, about 2m 33s with final eye export |
| Vertical challenges | Stairs in every room, hungry/heavy stair access, normal vs boosted leap, three return shelves, boost expiry, underside collision |
| Camera regression at `cecfb02` | Local and live pass: native/small motion, invalid samples, input bursts, focus recovery, three capture cycles, 30/60/144 FPS input consistency, furniture-corner recovery |
| Pages at `cecfb02` | Live revision and model hash confirmed; three rooms, movement/jump, no browser errors; 26 runtime files, about 12.45 MB |

Full autoplay uses actual keyboard navigation without teleporting to meals.
Isolated vertical/platform tests place the cat at scenario starts. Sampled mesh
inspection is not an exhaustive intersection test, and local FPS is not a promise
for every device. Full autoplay was not rerun for the later mouse-only fix;
camera, smoke, and Pages checks were run instead.

Detailed evidence: [cat verification](docs/cat-upgrade-verification.md) and
[camera verification](docs/camera-controls-verification.md).
The old [asset brief](docs/cat-asset-brief.md) contains early triangle/clip targets;
those are not the current runtime specification.

## Hosting And Release

- Repository: https://github.com/desmondttm123/MegaChonk (the account ends in `123`).
- Live game: https://desmondttm123.github.io/MegaChonk/.
- The original public repository deploys on `main` pushes. This separate private copy has a manual-only `.github/workflows/pages.yml`; Pages is not enabled as part of creating the repository.
- `python tools/build_pages.py` follows actual module imports and packages only runtime assets/licenses into ignored `dist/`, with revision/hash metadata.
- Do not upload the whole repo as the website: Blender/FBX/STL, experiments, sprite sheets, and test captures are not required at runtime.
- CI checks module syntax and builds/deploys; it does not run the Playwright regression suite. Confirm the workflow and live build manifest when verifying a release.
- Runtime revision `39d9265cb67a4a3453ee00f544b922a523910f09` passed hosted mobile/camera/Pages checks on 2026-10-16. The evidence-only follow-up `3c9260e62025a55bf204a28bf35843ff7e12ced8` also deployed successfully, with the public manifest and unchanged runtime hashes checked. [Final release workflow](https://github.com/desmondttm123/MegaChonk/actions/runs/38854555719).
- Adventure runtime `74b013e4b0e12fd427dded7984909fe6741b095b` was verified live on 2026-10-17 after [workflow 38943348005](https://github.com/desmondttm123/MegaChonk/actions/runs/38943348005) succeeded. Hosted Pages, mobile controls including boss retry/finishing claw, and desktop camera suites passed. A fresh, isolated boss start was won by keyboard without equipment: eight attack inputs, nine lives left, about 14 seconds, no browser errors. The full campaign was verified locally, not replayed on the host.
- The adventure release has 30 runtime files, approximately 12.51 MB, with the unchanged canonical model hash. CI syntax and pure adventure-rule checks succeeded; browser tests were run separately, not by CI. Later notes/capture-only commits retain the tested runtime; inspect current history/manifest for the latest deployment ID.

## Deferred Or Limited

- Multiplayer/two-browser interaction was discussed and explicitly postponed. No networking implementation exists.
- Generic tuxedo/calico/orange coat variants remain deferred. The separately requested Tactical Tabby character selector is implemented locally; this does not authorize more variants or publication.
- Phone controls are implemented and tested with browser-dispatched multi-touch in Windows Edge/Chromium emulation. Actual Android/iOS hardware and Safari behavior/performance still require manual verification; desktop browser test launchers still assume Windows Edge.
- The game remains a stylized prototype, not production AAA quality. Continue improving anatomy/animation and environment quality only against a concrete request.
- The adventure contribution is released. New bosses, more levels, saved inventories, and additional enemy types are not automatically approved next tasks. Physical-phone playtesting and user feedback remain useful follow-up.

## Updating This Handoff

Keep this file current when contributing. Record the latest request, actual
changes, tests/seeds, limitations, deployment evidence, and exact next approved
step. Remove superseded current-state facts; do not turn memory into a transcript.
