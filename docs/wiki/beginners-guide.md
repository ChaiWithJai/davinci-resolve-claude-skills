# Beginner's Guide to DaVinci Resolve 20 — Wiki

**One-line summary**: The on-ramp PDF. Covers a full edit from raw media to delivered MP4 across one project, touching every page (Media, Cut, Edit, Fusion, Color, Fairlight, Deliver). 600 pages. Roberts and Hall, 2025.

**Use this PDF when**: a user is brand new to Resolve, has free Resolve (not Studio), or needs the simplest possible recipe for a single concept.

## Table of contents

| Lesson | Chapter title | Purpose | Pages |
|---|---|---|---|
| Front | Getting Started | Install, system requirements, Quick Setup wizard | xiii-xxiv |
| 1 | Editing a Rough Cut | Import, bins, timeline creation, J-K-L scrubbing, soundbite assembly, music | 1-67 |
| 2 | Finessing the Rough Cut | Trim modes, replace edit, ResolveFX (Vignette, Film Damage), Dynamic Zoom, Logo, closing titles via Fusion Titles | 69-139 |
| 3 | Audio Editing and Quick Export | Clip levels, normalize, Noise Reduction via Fairlight FX, fades/transitions, music mixing, voiceover recording, Quick Export | 141-179 |
| — | An Introduction to Color Correction | Color theory primer | 181-188 |
| 4 | Performing Primary Color Corrections | Color page interface, primary corrector, video scopes, Lift/Gamma/Gain, nodes, automatic adjustments, color management, matching cameras, channels, curves, HDR Wheels | 189-245 |
| 5 | Making Secondary Adjustments | Windows, Outside nodes, HSL Curves, Color Warper, Chroma Warper, Qualifier, Power Window + Qualifier combos, Tracker, Color Slice | 247-293 |
| 6 | Finishing and Management | Applying ResolveFX in Color, identifying ungraded clips, copying grades, working with stills, importing/exporting grades, LUTs | 295-333 |
| 7 | Project Setup and Preferences | New project, source media, Project Settings, importing media, syncing audio to video, metadata, Smart Bins, subclips, Preferences, keyboard shortcuts | 335-415 |
| — | An Introduction to Audio Post | Audio post primer | 417-423 |
| 8 | An Introduction to Fairlight | Fairlight interface, track formats, AI Dialogue Leveler, EQ, sound effects, scrollers, mixing, ducking | 425-491 |
| — | An Introduction to Visual Effects Compositing | VFX primer | 493-497 |
| 9 | An Introduction to Fusion | Fusion comp creation, interface, nodes, Merge node, Text, keyframes, quick changes from Edit page | 499-541 |
| 10 | Delivery and Media Management | Vertical timelines, reframing, Deliver page, audio standards, custom Deliver presets, save render preset, render the queue, archive project, project libraries, backup | 543-599 |

## Chapter notes — chapters the skills draw on

### Lesson 1 — Editing a Rough Cut (pp. 1-67)

**Key concepts**:
- **Soundbite-driven editing**: Build the spine of the cut from interview audio first, then layer B-roll over it.
- **Three-point editing**: Mark In/Out on the source viewer, mark a point on the timeline, press F10 (overwrite) or F9 (insert).
- **Subclips**: Resolve subclips are pointers, not copies. Editing a subclip doesn't duplicate media.

**Workflows**:
1. Import a project (or media) via File > Import Project.
2. Relink offline media via right-click bin > Change Source Folder (bulk) or right-click clip > Relink Selected Clips (one-off).
3. Create a timeline (File > New Timeline, Cmd-N). Uncheck Use Project Settings to override resolution/fps.
4. Mark In/Out on the source viewer (I/O keys), press F10 to Overwrite or F9 to Insert.

**Shortcuts**: J = reverse, K = stop, L = forward (tap L again for 2x, again for 4x). I = mark In, O = mark Out. F9 = Insert. F10 = Overwrite. F12 = Append at end.

**Common pitfalls**:
- Importing media before creating a project — Resolve indexes media into the *current* project. Always make the project first.
- Forgetting to set timeline frame rate before adding clips — changing fps after clips are added causes retiming.

_Source: pp. 1-67_

### Lesson 2 — Finessing the Rough Cut (pp. 69-139)

**Key concepts**:
- **Trim modes**: Roll (adjusts both sides of a cut), Slip (changes content without moving boundaries), Slide (moves clip in time without changing its content), Ripple (adjusts one side and shifts everything downstream).
- **Replace Edit (F11)**: Drop a new source clip into an existing timeline position, preserving duration. Different from a regular overwrite — Replace lines up the playhead point in source with the playhead point in timeline.
- **ResolveFX in Edit**: Effects like Vignette and Film Damage live in Effects Library > OpenFX > Filters. Drag onto clip, parameters appear in Inspector > Effects tab.
- **Paste Attributes**: Copy a clip (Cmd-C), select target clips, Edit > Paste Attributes (Option-V), choose which attributes (Plugins, Color Correction, Composition Mode...) to paste.
- **Dynamic Zoom**: Built-in pan/zoom on still images. Inspector > Dynamic Zoom or Viewer Overlay menu.
- **Fusion Titles**: Pre-built animated titles in Effects Library > Titles. Different from basic Text — these are Fusion macros with exposed parameters.

**Shortcuts**: F11 = Replace. Option-V = Paste Attributes. F12 = Place on Top (used for titles that need their own track).

_Source: pp. 69-139_

### Lesson 3 — Audio Editing and Quick Export (pp. 141-179)

**Key concepts**:
- **Normalize Clip Levels**: Right-click clip > Normalize Audio Levels. Sets gain so peaks hit a target dBFS (default -3). Useful first pass before EQ.
- **Volume keyframes**: Option-click (Mac) / Alt-click (Windows) the volume rubber-band on an audio clip to add a keyframe. Drag between keyframes to dip or boost.
- **Noise Reduction via Fairlight FX**: Drag from Effects Library > Audio FX > Fairlight FX onto a clip. Auto Speech Mode just works; Manual mode requires a noise-only sample.
- **Quick Export**: Edit page > top-right cloud icon. Opens a one-click export dialog with pre-built presets (H.264 Master, YouTube, Vimeo).

**Workflows for fading and music ducking (free Resolve users)**:
1. Click an audio clip's edge to grab the small fade handle. Drag inward to create a fade.
2. For music to duck under voiceover: add volume keyframes on the music clip — one before the VO starts (full volume), one after VO starts (lower volume, e.g. -10 dB), one before VO ends (still low), one after VO ends (back to full).

_Source: pp. 141-179_

### Lesson 4 — Performing Primary Color Corrections (pp. 189-245)

**Key concepts**:
- **Color page is node-based**: Each grade is a node. Nodes connect serially by default (output of node 1 feeds input of node 2).
- **Video scopes**: Waveform (luminance + color), Vectorscope (hue and saturation), Histogram, Parade. The waveform is the workhorse for normalization.
- **Lift / Gamma / Gain**: Three master wheels under each color wheel. Lift = shadows. Gamma = midtones. Gain = highlights. Each color wheel has both a center dot (color cast) and a master wheel (luminance).
- **Color management**: Project Settings > Color Management. DaVinci YRGB is the default; DaVinci Wide Gamut Intermediate is the modern recommended pipeline for mixed-source projects.

**Workflows**:
1. Switch to Color page (Shift-6).
2. Open Scopes from the right-side palette button.
3. Drag Lift master wheel until shadows sit just above 0 on the scope.
4. Drag Gain master wheel until highlights sit around 75% on the scope.
5. Adjust Gamma to lift or lower midtones.

**Misconceptions to address**:
- Adjusting by eye on a laptop screen. Laptops are uncalibrated; read the waveform.
- Cranking saturation past 60 — skin tones go orange.

_Source: pp. 189-245_

### Lesson 8 — An Introduction to Fairlight (pp. 425-491)

**Key concepts**:
- **Track formats**: Mono, Stereo, 5.1, etc. Set per-track via the track header context menu. Don't put a mono mic on a stereo track without conversion.
- **AI Dialogue Leveler** (p. 442): Studio-only one-click voice leveler. Inspector > Track FX.
- **Mixer**: Toolbar > Mixer button. Per-track fader, dynamics (Gate / Compressor / Expander / Limiter), EQ, FX inserts.
- **Ducker** (pp. 479-490): Lower a music track automatically when a dialogue track is loud. Inspector > Track FX > Ducker on the music track, set Source to the dialogue track.

_Source: pp. 425-491_

### Lesson 9 — An Introduction to Fusion (pp. 499-541)

**Key concepts**:
- **Node-based compositing**: Each Fusion node is an image operation. Connect outputs to inputs.
- **Merge node** (p. 509): Composite a foreground over a background. Background = orange input, Foreground = green input.
- **Text node**: Create text in Fusion. More powerful than the Edit page's Text+ for animation, less convenient for simple captions.
- **Keyframes** (p. 517): Right-click any parameter > Animate (or use the diamond next to it in the Inspector). Resolve interpolates between keyframes.

_Source: pp. 499-541_

### Lesson 10 — Delivery and Media Management (pp. 543-599)

**Key concepts**:
- **Vertical timelines** (p. 545): Create a 1080x1920 timeline alongside your 1920x1080 master. Use AI Smart Reframe (Studio) or manual Position keyframes to track subjects.
- **Render presets** (p. 577): Configure Deliver settings once, save as preset, reuse forever. Saved per user, available across projects.
- **Audio standards** (p. 571): YouTube = -14 LUFS, Streaming = -16 LUFS, Broadcast = -23 LUFS. Set under Audio tab > Audio Normalization > Optimize to standard.
- **Project archive** (p. 592): Bundles project + media into a .dra file for portability.

_Source: pp. 543-599_

## When to crack open the PDF

Read the actual PDF when:

- **The user is on free Resolve, not Studio**: Many shortcuts here assume Studio features (AI Transcription, Smart Reframe, Noise Reduction). The Beginner's Guide's pp. 142-158 explicitly covers Manual keyframes and Fairlight FX for free users — this is the fallback the user actually has.
- **The user wants the simplest possible recipe**: This PDF assumes nothing. If your skill output reads as too advanced, recipe-walk-through this PDF for the matching chapter.
- **The user is asking about Quick Export**: pp. 174-179 cover Quick Export specifically; the Editor's Guide doesn't.
- **The user pushes back on a color/audio recipe**: Read pp. 189-245 (color) or pp. 425-491 (audio) — these are the gentle, screenshot-rich versions that confirm the order of steps.

## Author

Built by Jai Bhagat. More at chaiwithjai.com.
