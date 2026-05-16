# Visual Effects Guide to DaVinci Resolve 20 — Wiki

**One-line summary**: The 2D Fusion compositing PDF. Covers the Fusion page for VFX work — compositing split screens, sky replacement, sign replacement, green-screen keying, plus an addendum on animated title creation with Text+. 200 pages. Allen, Gallardo, Scoppettuolo, 2025.

**Use this PDF when**: a user is doing VFX (sky replace, sign replace, green screen) or wants animated titles, lower-thirds, and logo reveals using Fusion macros.

## Table of contents

| Lesson | Chapter title | Purpose | Pages |
|---|---|---|---|
| Front | Getting Started | Install and download lesson media | ix-xx |
| 1 | Getting Started: Learning the Fusion Page | Fusion interface, combining images with nodes, adding effects, node flow, masks, secondary correction, keyframes, vignette | 1-30 |
| 2 | Compositing Split Screens | Layers from Edit page, **Tracking in Fusion**, drawing a matte, nudging, restoring camera motion | 31-57 |
| 3 | Replacing a Sky | Clip resolution, composition resolution, Darken Apply Mode, effects library, **fixing holes in a key**, embedding alpha, **tracking the sky** | 59-85 |
| 4 | Replacing Signs and Screens | **Planar Tracker**, Clone Tool, Photoshop PSD layers, mattes + images, **Planar Transform**, finalizing | 87-109 |
| 5 | Compositing Green-Screen Content | Clean plate, **Delta Keyer**, rotoscoping, lining up background, color correcting elements, sending matte to Color page | 111-137 |
| 6 | **Addendum: Creating Title Animations** | **Styling Text+ in Edit page**, moving to Fusion, background banner, revealing text with mattes, **Follower modifier**, keyframe timing, versions, **Save Template** | 139-167 |
| 7 | Addendum: Animating with Keyframes and Modifiers | Clip resolution, keyframing motion paths, auto-orienting, alpha channels, paint motion path, linking parameters, acceleration adjustments, random modifiers, motion blur | 169-191 |

## Chapter notes — chapters the skills draw on

### Lesson 1 — Learning the Fusion Page (pp. 1-30)

**Key concepts**:
- **Node-based compositing**: Each Fusion node is an image operation. Connect outputs (right side) to inputs (left side). Output is always on the right; inputs vary per node.
- **MediaIn / MediaOut**: Every Fusion comp starts with a MediaIn (the timeline clip) and ends with a MediaOut (back to the timeline).
- **Merge node** (p. 9): The compositor. Takes two inputs:
  - **Background** (orange) — the bottom layer.
  - **Foreground** (green) — the top layer, composited over BG.
  - Optional **Mask** input — restricts compositing to a region.
- **Node flow**: The horizontal direction shows processing order. Left to right.

**Workflows**:

Adding a node from the toolbar:
1. Click an existing node to select it.
2. Press Shift-Spacebar to open the Select Tool dialog.
3. Type the node name (e.g. "Blur"). Hit Enter.
4. The new node inserts after the selected one.

_Source: pp. 1-30_

### Lesson 2 — Compositing Split Screens (pp. 31-57)

**Key concepts**:
- **Tracker** node: Single-point tracker. Track a feature (corner, freckle) and use its motion to drive Position, Rotation, etc. on another node.
- **Stabilizing**: Track a feature, then invert the tracking data via Right-click Tracker > Operation > Match Move > Steady. Removes camera shake.

_Source: pp. 31-57_

### Lesson 4 — Replacing Signs and Screens (pp. 87-109)

**Key concepts**:
- **Planar Tracker** (pp. 88-93): Track a *flat surface* across frames. Far more robust than single-point tracking for screen replacements. Set Region of Interest, click Track Forward. Resolve generates a planar transform.
- **Planar Transform node**: Applies the tracked planar motion to a foreground element. Plug your replacement screen into the Planar Transform; the replacement now follows the surface.

_Source: pp. 87-109_

### Lesson 5 — Compositing Green-Screen Content (pp. 111-137)

**Key concepts**:
- **Delta Keyer** (pp. 115-119): The recommended Fusion keyer. Sample background green; tune Threshold, Tolerance, and Density.
- **Clean plate** (p. 112): A frame of the empty green-screen with no subject. Used to subtract uneven lighting before pulling the key.

_Source: pp. 111-137_

### Lesson 6 — Creating Title Animations (Addendum, pp. 139-167)

**This is the chapter that powers the titles-and-lower-thirds skill.**

**Key concepts**:
- **Text+** (pp. 140-145): A Fusion-backed text generator that lives in the Effects Library on the Edit page. Drag onto a timeline track to add. Inspector exposes:
  - **Styled Text**: the actual text content. Multi-line is supported (press Return).
  - **Font / Size / Color / Tracking / Line Spacing**: typographic controls.
  - **Layout tab**: Position (Center X / Y), Rotation, Scale.
  - **Shading tab**: Fill type — Solid, Gradient, Image, Outline.
  - **Settings tab**: misc.

- **Gradient shading** (pp. 142-145):
  - Shading tab > Type: Gradient.
  - Color stops on the gradient bar: leftmost stop sets one end of the gradient, rightmost the other. Click a stop, open the color swatch, pick a color.
  - Mapping Angle: -90 makes the gradient run horizontally.
  - Mapping Level: Line spans the gradient across each line of text; Word spans each word; Character spans each character.

- **Animating Center X** (pp. 145-149):
  - Position playhead at start of clip.
  - Inspector > Layout tab > click the diamond next to Center X to add a keyframe.
  - Set Center X to off-screen value (e.g. -1.5).
  - Move playhead forward (e.g. 12 frames at 24 fps = 0.5 sec).
  - Set Center X to final value (e.g. 0.1). A second keyframe is created automatically.

- **Follower modifier** (pp. 153-157): Walks across each character and applies an animation with a configurable delay between characters. Perfect for typewriter-style reveals and logo word-builds.
  - Right-click the Styled Text parameter > Follower > Position (or other animation type).
  - Modifier panel opens. Set Delay between characters (e.g. 2 frames per char).

- **Save as Template / Macro** (pp. 163-167):
  - Fusion page > right-click the Text+ node > Save As Macro.
  - Enter a name. Macro is saved to local templates folder.
  - Macro now appears in Effects Library > Titles for any project.

**Misconceptions to address**:
- "Use the basic Text generator and animate it." Basic Text generator doesn't expose animation properties cleanly. Use Text+ for anything animated.
- Saving the macro too early — once saved, edits require recreating from scratch.

_Source: pp. 139-167_

### Lesson 7 — Keyframes and Modifiers (Addendum, pp. 169-191)

**Key concepts**:
- **Keyframing motion paths** (p. 171): Right-click any parameter > Animate. Resolve adds the parameter to a curve modifier; drag the playhead and adjust to add keyframes.
- **Spline Editor**: Right-click a keyframed parameter > Edit Spline. Edit interpolation curves (linear → smoothed → ease in/out).
- **Random modifier** (p. 187): Adds wobble/jitter to a parameter automatically.

_Source: pp. 169-191_

## When to crack open the PDF

Read the actual PDF when:

- **The user wants 3D titles, particles, or 3D logos**: Not in this PDF — see `advanced-visual-effects.md` instead.
- **Sky replacement with subject hair / fine detail**: pp. 74-83 walk through "Fixing Holes in a Key" specifically. The wiki summary skips this.
- **Sign / screen replacement with perspective**: Lesson 4 (pp. 87-109) — the planar tracker behavior on warped surfaces is documented per-step in the PDF.
- **Pulling a green-screen key on hair / soft edges**: Lesson 5 (pp. 111-137). The Delta Keyer rotoscope fallbacks (auxiliary mattes) are PDF-only detail.
- **The user pushes back on a Text+ gradient not rendering**: pp. 142-145 covers the Mapping Level distinction (Line vs Word vs Character) that often causes the visible-vs-not gradient confusion.
- **The user's saved macro doesn't appear in Effects Library**: pp. 163-167 covers the macro save path and how to refresh the library.
- **Follower modifier won't trigger**: pp. 153-157 — specific gotcha is that Follower must be added to the *Styled Text* parameter, not Layout or Shading.

## Author

Built by Jai Bhagat. More at chaiwithjai.com.
