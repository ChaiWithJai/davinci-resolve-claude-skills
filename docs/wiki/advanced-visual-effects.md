# Advanced Visual Effects in DaVinci Resolve 20 — Wiki

**One-line summary**: The 3D Fusion compositing PDF. Covers 3D scene construction (cameras, lights, materials), green-screen with 3D set extensions, rainy-day compositing, 3D camera tracking, and USD (Universal Scene Description) integration. 201 pages. Allen, Scoppettuolo, 2025. Studio only.

**Use this PDF when**: a user is doing 3D VFX work — 3D logos, 3D set extensions, camera tracking a live-action plate, animated 3D particles, USD asset integration.

## Table of contents

| Lesson | Chapter title | Purpose | Pages |
|---|---|---|---|
| Front | Getting Started, Blackmagic Cloud | Setup notes | viii-xviii |
| 1 | Creating a 3D Scene | Placing elements in 3D space, navigating 3D, **3D text**, camera setup, lights, converting 3D to 2D image | 1-39 |
| 2 | Exploring a Green-Screen Workflow | Color management for VFX, noise removal, **pulling a key**, natural light spill, **3D windshield reflection** | 41-83 |
| 3 | Creating a Rainy Day | Merging 2D and 3D, sky replacement patching, magic mask, reflections, color correction in Fusion, **3D particles**, finishing | 85-127 |
| 4 | 3D Camera Tracking | Masking for tracking, preparing camera tracker, solving, refining solve, exporting scene, positioning 3D objects in tracked space, matching color and light | 129-159 |
| 5 | Compositing 3D with USD | Importing USD, surfaces with shaders, rendering USD, dragon-fly animation, matching lights to scene, flight of dragons, Z-depth in color correction, finishing | 161-199 |

## Chapter notes — chapters the skills draw on

### Lesson 1 — Creating a 3D Scene (pp. 1-39)

**Key concepts**:
- **3D space in Fusion**: Different node types — start with a **Merge3D** node, which combines 3D objects into a single 3D scene. Connect objects (shapes, text, image planes) into it.
- **3D Text** (pp. 14-19): Create the Text+ node, then a **Text3D** node, OR connect Text+ to an ImagePlane3D and extrude.
- **Camera setup** (pp. 19-26): **Camera3D** node controls perspective. Position, target, focal length, aperture.
- **Lights** (pp. 26-33): Spot, point, directional, ambient. Set color, intensity, position.
- **Renderer3D**: The node that converts a 3D scene to a 2D image for the rest of the comp.

_Source: pp. 1-39_

### Lesson 4 — 3D Camera Tracking (pp. 129-159)

**Key concepts**:
- **Camera Tracker** node: Analyzes a live-action plate to determine the camera's motion through 3D space. Output is a virtual Camera3D that matches the real-world camera.
- **Workflow**:
  1. Add Camera Tracker after the MediaIn.
  2. Press Track Forward — Resolve analyzes the plate.
  3. Press Solve — Resolve computes camera position per frame.
  4. Set Scene Reference — give Resolve the ground plane.
  5. Export Scene — generates a Camera3D you can connect to a Merge3D.

**Common pitfalls**:
- Trackers landing on moving objects (people, cars). Mask them out before tracking.
- Insufficient parallax — a locked-off camera produces a poor solve.

_Source: pp. 129-159_

### Lesson 5 — Compositing 3D with USD (pp. 161-199)

**Key concepts**:
- **USD** (Universal Scene Description): Industry-standard 3D scene format. Resolve imports `.usd` and `.usda` files via the **uShape** node or similar.
- **Z-depth** (pp. 190-196): 3D scenes export a Z-depth channel alongside RGB. Used in Color page for depth-aware grading (e.g. blur background only).

_Source: pp. 161-199_

## When to crack open the PDF

Read the actual PDF when:

- **The user has a live-action plate and needs a 3D set extension**: Lesson 4 (pp. 129-159). The Camera Tracker solve process is detailed step-by-step in the PDF.
- **The user wants 3D logo / animated 3D title**: Lesson 1 (pp. 14-19) for 3D text. The wiki summarizes only structure.
- **Particle systems**: Lesson 3 (pp. 113-127) — 3D particles for rain, snow, dust. Wiki-level summary is not enough.
- **The user pushes back that the green-screen key has rim/spill light**: Lesson 2 (pp. 67-72) "Adding Natural Light Spill" covers the integration trick that makes a composite believable.
- **The Camera Tracker solve gave bad results**: pp. 142-146 cover refining the solve — masking out tracked points on moving subjects, raising the track count, etc.
- **USD asset import is failing**: Lesson 5 (pp. 161-172).

## Author

Built by Jai Bhagat. More at chaiwithjai.com.
