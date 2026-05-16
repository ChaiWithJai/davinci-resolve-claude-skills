# Colorist Guide to DaVinci Resolve 20 — Wiki

**One-line summary**: The professional color grading PDF. Covers the Color page in depth, including primary grading, shot matching, qualifier-based secondary corrections, node trees, groups, raw/HDR, and DCP delivery. 457 pages. Fissoun, 2025.

**Use this PDF when**: a user is doing serious color work — matching shots, building a look across a timeline, refining skin tones, grading raw, or applying LUTs / color management.

## Table of contents

| Lesson | Chapter title | Purpose | Pages |
|---|---|---|---|
| Front | Interface Review | Color page layout, viewer, primaries wheels, palette panel | xx-xxv |
| — | Color Correcting a DaVinci Resolve Timeline | Intro to Part I | 1-2 |
| 1 | Balancing Footage | Open archive, project backups, grading workflow, primary grading with wheels, precision with curves, color vs log wheels | 3-43 |
| 2 | Creating Color Continuity | Shot-matching strategy, flags + filters, applying shot match, matching with stills, manual matching | 45-71 |
| 3 | Correcting and Enhancing Isolated Areas | Power Windows, sharpening with windows, fixing overcast skies, color range warping, **skin tone refinement** (Face Refinement and manual), Chroma Warper | 73-139 |
| — | Managing Nodes and Grades | Intro to Part II | 141 |
| 4 | Conforming an XML Timeline | Importing XML, syncing offline reference, conforming, maximizing dynamic range | 143-179 |
| 5 | Mastering Node Trees | Node-based compositing, **node order**, **Parallel Mixer node**, **Layer Mixer node**, External Mattes | 181-223 |
| 6 | Managing Grades Across Clips and Timelines | Working with versions, appending grades, node tree templates, **saving stills for other projects (PowerGrade)**, ColorTrace, Timelines Album | 225-259 |
| — | Optimizing the Grading Workflow | Intro to Part III | 261 |
| 7 | Using Groups | Scene Cut Detection, group creation, pre-clip / clip / post-clip group levels, automatic tracking, unifying looks, LUTs, timeline level | 263-341 |
| 8 | Adjusting Image Properties | Timeline resolutions and sizing modes, keyframes, **Noise Reduction**, **Render Cache** | 343-379 |
| 9 | Setting Up Raw Projects | Raw at project / clip level, **HDR Wheels**, render cache for raw | 381-409 |
| 10 | Delivering Projects | Lightbox, client review, render workflow, custom renders, **DCP**, advanced render settings | 411-447 |
| A | Using the DaVinci Resolve Panels | Hardware control surfaces | 449-454 |
| B | Setup and Delivery on Macs | macOS-specific notes | 455-456 |

## Chapter notes — chapters the skills draw on

### Front matter — Project backups (pp. 6-7)

**Key concepts**:
- **Live Save**: Auto-save on every change. Preferences > User > Project Save and Load > Live Save.
- **Project Backups**: Independent of Live Save. Time-based snapshots. Recommended intervals: every 10 minutes (6 per hour), hourly for 24 hours, daily for 180 days.

**Workflow**:
1. DaVinci Resolve > Preferences > User > Project Save and Load.
2. Check Live Save.
3. Check Project Backups. Set the three intervals (10 minutes / 24 hours / 180 days).
4. Browse for Backup Location — pick a folder on your **internal SSD**, not the media drive. (If the media drive dies, the backups die with it.)
5. Check Timeline Backups too — these are small `.drt` files, recoverable independently.

_Source: pp. 6-7_

### Lesson 1 — Balancing Footage (pp. 3-43)

**Key concepts**:
- **The grading workflow**: Normalize → Balance → Enhance. Always in this order.
- **Primary grading with wheels**: Each of the three wheels (Lift / Gamma / Gain) has a **center dot** (color cast) and a **master wheel** (luminance). Drag the dot to push color. Drag the master wheel slider to push luminance.
- **Reading the waveform** (pp. 12-15): The horizontal axis is screen position; the vertical axis is luminance (0 = black, 1023 = white in 10-bit). The trace should fill the range without crushing or clipping.
- **Curves vs wheels** (pp. 20-27): Curves give finer control over isolated luminance ranges. Wheels are faster for global moves. Most colorists start with wheels and refine with curves.
- **Color vs Log wheels**: Color wheels affect the whole image with smooth rolloff. Log wheels target shadow/midtone/highlight bands with hard transitions. Use Log wheels when grading log footage or HDR.

**Workflows**:

Primary grade — basic balancing:
1. Switch to Color page (Shift-6).
2. Open Scopes (right-side palette button), set to Waveform.
3. Drag Lift master wheel left until darkest area sits just above 0 (around line 64 on a 1023 scale).
4. Drag Gain master wheel until highlights peak around 75% (line 768).
5. Drag Gamma master wheel to set midtone brightness.
6. Adjust Contrast (top of Primaries palette) to ~1.1; Pivot to ~0.3 for punchier mids.

**Misconceptions to address**:
- Eyeballing on a laptop screen. The waveform is the truth source.
- Skipping normalization. Creative grades on top of broken footage stack errors.

_Source: pp. 3-43_

### Lesson 2 — Creating Color Continuity (pp. 45-71)

**Key concepts**:
- **Shot matching strategy**: Pick a hero clip. Match the rest to it. Use flags to track which clips have been matched.
- **Applying Shot Match** (p. 52): Right-click target clip > Shot Match To This Clip. Resolve runs a one-shot auto-match. Works best when both clips have similar exposure to start.
- **Matching with stills** (p. 54): Save a still from the hero clip to the Gallery. Right-click the still > Apply Grade. Then refine.
- **Manual matching** (p. 61): Side-by-side viewer mode + waveform comparison. Adjust wheels on target clip to match the trace of the hero.

_Source: pp. 45-71_

### Lesson 3 — Correcting and Enhancing Isolated Areas (pp. 73-139)

**Key concepts**:
- **Power Windows**: Spatial masks. Linear, Circle, Polygon, Curve, Gradient. Add via the Window palette. Combine with Qualifier for "this color AND this region."
- **Qualifier**: Color/luminance selection. Three modes — HSL (default, most common), RGB, LUM. Eyedropper on the viewer, then refine with Hue/Sat/Luminance range sliders.
- **Skin tone refinement — Face Refinement** (pp. 118-128, Studio): AI-powered face detector. Color page > Effects Library > ResolveFX Color > Face Refinement. One click, detects face, exposes parameters for skin smoothing, eye brightening, lip enhancement.
- **Skin tone refinement — Manual** (pp. 129-138, Free): HSL Qualifier + Power Window combo. Qualifier picks skin color; Power Window restricts to the face region; primary controls inside the qualifier branch warm skin and add saturation.

**Workflows**:

Manual skin-tone refinement (free Resolve):
1. Add a serial node after your primary balance.
2. In the Qualifier palette, click the eyedropper, click skin in the viewer.
3. Refine Hue/Sat/Lum ranges. Toggle Highlight (top of viewer) to see the matte.
4. In the Window palette, add a Linear or Circle window around the face.
5. Switch back to Primaries. Push Gain color wheel slightly toward orange. Bump Saturation to ~60.

**Misconceptions to address**:
- Cranking saturation to 70+. Skin tones go orange and fake. Stay ≤ 60.
- Forgetting to disable the Highlight matte preview. Press the Highlight button (top of viewer) to toggle off before continuing to grade.

_Source: pp. 73-139_

### Lesson 5 — Mastering Node Trees (pp. 181-223)

**Key concepts**:
- **Node order matters** (p. 183): Sharpening before noise reduction amplifies noise. Noise reduction before sharpening preserves detail. Always sharpen *after* NR.
- **Parallel Mixer node** (p. 198): Combine multiple parallel branches with equal weight. Useful when two color decisions affect different parts of the image and you don't want one to dominate.
- **Layer Mixer node** (p. 205): Like Photoshop layers. Each input is a layer; the top input has a blend mode applied. Used to overlay color effects.
- **Outside node**: Inverse of a Power Window. Grade everything *outside* the masked region.

_Source: pp. 181-223_

### Lesson 6 — Managing Grades Across Clips and Timelines (pp. 225-259)

**Key concepts**:
- **Versions**: Each clip can hold multiple grade versions (V1, V2...). Right-click clip > Local Versions > New Version.
- **Saving stills for PowerGrade** (pp. 246-250): Right-click in the Gallery panel > Add to PowerGrade. The still saves the full node tree, persistent across projects. Apply to a new clip via right-click still > Apply Grade.
- **ColorTrace** (p. 251): Migrate grades from a previous version of the timeline (when you've re-conformed from new media).
- **Timelines Album** (p. 256): Grades stored at the timeline level (not clip level), copyable across timelines.

_Source: pp. 225-259_

### Lesson 8 — Adjusting Image Properties (pp. 343-379)

**Key concepts**:
- **Noise Reduction** (p. 362): Color page > Motion Effects palette > Noise Reduction section. Temporal NR (uses neighboring frames) and Spatial NR (within one frame). Defaults: Temporal Threshold 25, Spatial Threshold 25.
- **Render Cache** (pp. 369-377): Resolve pre-renders complex nodes to disk for real-time playback. Smart cache (auto) vs User cache (manual). Set per-clip via Playback menu > Render Cache.

_Source: pp. 343-379_

## When to crack open the PDF

Read the actual PDF when:

- **The user is grading log or raw footage**: Lesson 9 (pp. 381-409) covers raw-at-clip-level vs raw-at-project-level, plus HDR Wheels — different math than standard primaries.
- **The user is conforming from an XML/AAF**: Lesson 4 (pp. 143-179) is the conform reference.
- **The user is grading a feature with Groups**: Lesson 7 (pp. 263-341) is the only place this workflow is documented in depth.
- **The user pushes back that "the skin tones still look orange"**: Re-read pp. 118-138 — there's a complete diagnostic in the chapter about why over-saturated skin happens and the precise qualifier-plus-window fix.
- **DCP delivery for cinema**: pp. 431-447.
- **Render Cache decisions**: pp. 369-377 — important when playback is stuttering on the Color page specifically (not the Edit page).
- **The user wants ColorTrace to migrate grades**: p. 251.

## Author

Built by Jai Bhagat. More at chaiwithjai.com.
