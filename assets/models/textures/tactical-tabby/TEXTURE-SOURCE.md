# Tactical Tabby fur textures

`kitten-fur-atlas.png` and `kitten-undercoat.png` were generated with the built-in image_gen tool on
2026-10-19 for this user-approved orange-cat remodel. They provide tintable ivory
strands and undercoat detail. The model uses UV-mapped, alpha-masked skinned
hair ribbons, the generated undercoat color map and a tangent-space normal map
authored by `tools/tactical_fur.py`. The game retains the embedded maps and
alpha cutoff. No third-party animal texture was used.

The maps are embedded in the GLB and packed in the Blender source. Keep these
editable PNG sources with the generator. Old seated assets are separate.

Exact built-in generation prompt:

```text
Use case: stylized-concept
Asset type: production texture atlas for alpha-masked hair cards on a real-time 3D kitten model, NOT a picture of a cat.
Primary request: create a square 2048x2048 texture atlas with sixteen separate wispy locks of very fine soft kitten fur arranged in a precise 4 by 4 grid. Each grid cell contains one vertical narrow tapered lock of many silky individual hairs, rooted near the bottom of its cell and feathering upward to softly curved tips. Four rows of different gentle curvatures and densities. All locks fit inside their cells with clear transparent margins at each edge. Fine dense undercoat near each root, soft airy separated strands at each tip. Strand direction is from bottom to top in every cell. Short plush kitten fur, subtle natural strand variation, warm ivory/near-white overall so it can be tinted golden orange or cream by 3D vertex colors. Hairs should be clearly opaque at the root and in the body, with clean transparent gaps between loose strands toward the tips.
Composition: flat orthographic texture sheet, evenly spaced 4x4 cells, consistent scale, no perspective, no shadows on any backdrop. Real alpha transparency behind every lock. Gentle neutral even lighting only within the fibers.
Constraints: no cat face, no animal shape, no skin, no clothing, no equipment, no text, no labels, no grid lines, no borders, no gray/checkerboard background, no strong directional lighting, no black hairs. Genuine transparent background.
```

Exact built-in undercoat generation prompt:

```text
Use case: photorealistic-natural
Asset type: seamless diffuse/albedo tile for the UV-mapped skin beneath individual 3D kitten hairs, not an illustration of an animal.
Primary request: one square seamless 2048 by 2048 image filled edge-to-edge with extremely fine, dense, soft newborn kitten underfur. Neutral warm off-white/ivory fibers suitable for tinting orange in a game shader. All hairs generally flow upward, with delicate natural gentle deviations. Individual hair widths about one pixel, hair lengths about 15-65 pixels at this image scale; very dense fine strands, not broad locks, scales, wood grain, brush strokes, wool weave or fabric. Soft plush, silky baby-cat fur like a high quality realistic fluffy orange kitten render. Natural fine strand detail throughout the entire image, even uniform density right to all edges.
Lighting: very even neutral diffuse lighting, no directional baked shadows, no hotspots, no dramatic contrast; no ambient occlusion clumps. Restrained soft cream luminance variation so it remains ivory overall, not gray or brown. Tileable in both directions with no seams, no borders or empty background.
Constraints: opaque texture, no alpha, no cat face or body, no eyes, no nose, no whiskers, no equipment, no lettering or graphics, no watermarks, no checkerboard, no empty patches. This is a production texture map, flat orthographic.
```
