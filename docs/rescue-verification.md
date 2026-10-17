# Orange Cat Rescue Verification

Local contribution begun on 2026-10-17 and verified on 2026-10-18 (Asia/Shanghai).
Inspected baseline: branch `main`, commit `f02c205942d048d7b8ca7c1f892e4cab15deee9e`.
The earlier cat-food-can work is included. On 2026-10-18 the user requested a
local Git checkpoint containing both changes, titled `Add cat-food cans and
orange-cat rescue mission`. No push or live deployment was requested.

## Behavior

- Level two is **Orange Cat Rescue** in the kitchen. Exactly three guard mice
  each require two successful Claw impacts, regardless of pendant damage.
  Bites cannot substitute for swipes. Two marks show each guard's remaining hits.
- All guards must be defeated before the cage gate lifts. The orange cat walks
  out, returns to Idle, grants 100 XP once, and unlocks the pet door.
- The cage has side, roof, base and moving-gate collision, plus floor support.
  The combat area, approaches and optional energy food have reserved routes.
- Partial guard damage, kills and a completed rescue survive room recovery and
  seeded regeneration. Run again resets all rescue state.
- The kitchen's four former required meals remain optional energy supplies.
  Levels one and three retain three and five required meals. Basic campaign XP
  remains 850 before optional checkpoint/bonus rewards.
- `rescue-mission.js` clones the existing skinned cat with SkeletonUtils, separate
  geometry/materials/skeleton and original runtime orange tabby colors. It uses
  the existing Idle and Walk clips. The playable Turkish Van, canonical GLB and
  Blender source, licenses and source attribution are preserved. No Blender
  export/re-import was needed for this runtime NPC.

## Verification Boundaries

`tools/rescue-test.js` places the player at individual scenario starts and grants
brief invulnerability to isolate hit counts and cage behavior. It checks desktop
and emulated touch attacks, a pendant, rejected bites, locked/open cage collision,
the independent skinned NPC, saved partial progress, release animation, reward,
exit gating and run reset. These are isolated scenarios, not played campaigns.

`tools/autoplay-test.js` uses keyboard movement, camera aiming and claw inputs to
traverse all missions and defeat the vacuum. It does not teleport to guards or
meals, alter enemy health, or force rescue completion. The driver now picks clear
claw approaches around support posts and resumes held movement after combat
recovery clears input. Upstairs planning stays on the gallery footprint and can
return to the stairs if a navigation attempt falls to the floor.

The smoke test now waits for actual grooming rather than a fixed 5.3 wall-clock
seconds. The severe-condition stair scenario has a 30-second bound and recovery
grace so it tests stair access independently of starvation. Adventure scenarios
wait for actual pickup/hit/death events, including a new death relative to the
previous count, rather than assuming a 100 ms pickup or zero earlier pounces.

## Results

| Check | Result |
| --- | --- |
| Syntax | Passed all 12 runtime modules and seven changed browser tools |
| Adventure rules | Passed two-swipe guards, rejected bites, saved damage, rescue/reset and existing equipment/boss/jump rules |
| Rescue scenarios | Passed keyboard and emulated touch, 320x568 / 568x320 / 390x844 / 844x390 HUD bounds, locked/open cage entry, solid floor and grounded freed NPC |
| Smoke / vertical | Passed model/actions/condition limits, all-room stairs, severe-condition stair access, catnip/return shelves and gallery underside |
| Adventure / mobile | Passed equipment, guard hits/loot/death, hurdles, boss armor/nine-loss retry, unequipped keyboard victory, phone layouts and simultaneous touch |
| Generation | Passed 90 layouts, protected guard approaches/optional meals/exit, deterministic replay and platform carry |
| Campaign 424242 | Eight meals, orange cat rescued, vacuum defeated, 865 XP, 12 jumps, three deaths/bonks, 2m43s |
| Campaign 765432 | Eight meals, orange cat rescued, vacuum defeated, 865 XP, seven jumps, four deaths/bonks, 2m30s |
| Local Pages | Passed `/MegaChonk/` packaging, three missions, model hash, movement/jump and no browser errors; 35 runtime files, 12.63 MB |

Both campaigns earned the 850 base XP plus a 15 XP checkpoint. They completed
before final cage-threshold and NPC foot-grounding polish; the focused rescue
scenarios and local Pages were rerun after those changes. Earlier failed runner
attempts are not counted as passes: fixed waits, a blocked claw approach, cleared
movement after death and an upstairs fall were resolved in the test drivers.

Physical Android/iOS hardware, Safari, condition integration and live hosting
were not tested in this contribution. Nothing was verified on the public host.

## Previews

- [Caged orange cat and three guards](../assets/previews/mega-chonk-orange-cat-rescue.png)
- [Freed orange cat](../assets/previews/mega-chonk-orange-cat-freed.png)
- [Touch rescue HUD](../assets/previews/mega-chonk-orange-rescue-mobile.png)
