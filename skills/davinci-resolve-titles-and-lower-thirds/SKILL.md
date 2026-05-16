---
name: davinci-resolve-titles-and-lower-thirds
description: Use when a user needs branded titles, animated lower-thirds, or a logo intro for their video — uses Resolve's Text+ node and Fusion's animation modifiers to create reusable title templates. Triggering symptoms include phrases like "add a name lower third", "animated logo intro", "title card with gradient", "save title as a template", "introduce a guest", or any DaVinci Resolve title/text question.
---

# DaVinci Resolve — branded titles and animated lower-thirds

## Overview

Build animated lower-thirds and title cards using the **Text+** node, then save them as templates that drop into any future timeline. The core principle: the basic **Text** generator is fine for static titles; for anything that needs to animate or look polished, use **Text+** which is Fusion-backed and far more powerful.

## When to use

Symptoms:
- Need to label a person in an interview ("FULL NAME / TITLE")
- Want an animated logo reveal at the start of a video
- Need a chapter divider title card with a gradient or animation
- Want to reuse the same title style across many videos
- The phrase "make it look like a real broadcast"

When NOT to use:
- You need 3D titles or particle effects — use the full Fusion 3D workflow (Advanced VFX Guide pp. 14-19).
- You only need a one-off static slide of text — the basic Text generator (Effects Library > Titles > Text) is faster.

## Quick reference

| Goal | Tool | Where it lives |
|---|---|---|
| Static caption (one line, no animation) | Basic Text generator | Effects Library > Titles > Text |
| Lower-third (name + role, animated) | **Text+** template | Effects Library > Titles > Text+ |
| Animated logo reveal | **Text+** + Follower modifier OR Fusion comp | Effects Library > Titles > Text+ |
| Reusable across projects | Save as Template | Right-click the Fusion comp > Save As Macro |

## Steps

### Build a lower-third using Text+

This is the workflow from Fusion VFX Guide pp. 140-145.

1. On the **Edit** page, position the playhead where you want the lower-third to appear.
2. Open the **Effects Library** (top-left button) > **Titles** category.
3. Drag the **Text+** template onto V2 (above your main video clip) at the playhead.
4. Select the Text+ clip in the timeline.
5. Open the **Inspector** (top right).

### Style the text

1. In the **Styled Text** field, replace `Custom Title` with the person's name in CAPS — e.g. `FULL NAME`.
2. Press **Return** to add a second line. Type their role/title — e.g. `Senior Developer Advocate`.
3. Set **Font**: pick a clean sans-serif. The Resolve PDFs use **Open Sans** at **Extrabold** weight, which is a safe default.
4. Set **Size** to around `0.1` (Text+ uses a 0-1 scale where 1 is the screen height).
5. Scroll down to **H Anchor** (horizontal anchor) and click the **Left** button so text aligns left.

### Position the text

1. Click the **Layout** tab at the top of the Inspector.
2. Adjust **Center X** and **Center Y** to position the text in the lower-third (left side). Typical values: X = `0.1`, Y = `-0.3` (negative Y is below center).
3. Or — from the overlay menu in the lower-left of the viewer, choose **Fusion Overlay** to drag the text directly in the viewer using onscreen handles.

### Add a gradient (the polished broadcast look)

1. Click the **Shading** tab in the Inspector.
2. Under **Type**, choose **Gradient**.
3. The first (white) color stop in the gradient bar sets the lower color of the gradient. Click it, then open the color swatch and pick a light teal.
4. Click the white color stop on the right end. Open the swatch and pick a pale yellow.
5. Scroll down to **Mapping Angle** and drag to `-90` so the gradient runs horizontally across each character.
6. From the **Mapping Level** menu, choose **Line** so the gradient spans the whole word, not each letter individually.

Fusion VFX Guide pp. 142-145 covers this gradient workflow with screenshots.

### Animate the lower-third (slide in from the left)

1. Position the playhead at the start of the Text+ clip.
2. Click the **Layout** tab > find **Center X**.
3. Click the small diamond next to Center X to add a keyframe at the current position.
4. Set Center X to `-1.5` (off-screen left).
5. Move the playhead forward 12 frames (about 0.5 seconds at 24 fps).
6. Set Center X back to `0.1` (your final position). A second keyframe is created automatically.
7. Resolve interpolates between the two keyframes. The lower-third slides in from the left over 12 frames.
8. To smooth the motion: right-click the Center X parameter > **Edit Spline** to open the Spline Editor and convert the keyframes to ease in/out curves.

### Save the lower-third as a template

This is what makes it reusable.

1. With the Text+ clip selected, click the **Fusion** button at the bottom (or press Shift-5) to enter the Fusion page.
2. You will see one node called `Template` (or `Text1`).
3. Right-click the Text+ node > **Save As Macro**.
4. Enter a name like `DEVREL_LOWER_THIRD_v1`.
5. The macro is saved to your local templates folder and shows up in the Effects Library > Titles category for any future project.

Fusion VFX Guide pp. 163-167 covers the Save As Template workflow.

### Use it on the next video

1. New project, new video. Drag your saved template from Effects Library > Titles onto V2 above the speaker's clip.
2. Update the Styled Text in the Inspector with the new name and title.
3. Done — the same animation, gradient, and position carry over.

### Build an animated logo reveal (the merged JTBD)

For a logo intro: same Text+ tooling, slightly different recipe.

1. Add a Text+ clip and replace the text with your brand name (or use a plain Text generator for typography-only logos).
2. Alternatively, drag your logo PNG/SVG from the Media Pool onto V2 — go to the **Fusion** page to compose it with animated background elements (animated shapes, particle systems).
3. For a simple "text appears one letter at a time" reveal: in the Text+ Inspector, set the **Follower** modifier on the Styled Text parameter — see Fusion VFX Guide pp. 153-157 for the Follower modifier workflow.

The Follower walks across each character and applies an animation to that character with a configurable delay between characters. Set the delay to 2 frames per character for a typewriter feel.

## Common mistakes

- **Using the basic Text generator and then trying to animate it** -> the basic Text generator does not expose animation properties cleanly. For anything animated, start with Text+. **(This is the misconception this skill addresses head-on.)**
- **Working in the Inspector and ignoring the on-screen handles** -> the Fusion Overlay (lower-left of viewer > overlay menu > Fusion Overlay) gives you direct manipulation. Faster than typing numbers.
- **Saving the template before perfecting the animation** -> save your template only when you are happy with the timing. Each saved template is hard to update without recreating from scratch.
- **Picking ornate or thin fonts** -> they fall apart at YouTube's compression. Stick to medium-to-bold sans-serif fonts. Open Sans Extrabold (used in the Resolve PDFs) is a safe default.

## Verification

You succeeded if all of the following are true:

1. The lower-third clip on V2 plays back smoothly with the slide-in animation.
2. The gradient on the text is visible — not flat single-color.
3. The saved template appears in the Effects Library > Titles category.
4. Dragging the saved template into a fresh timeline produces the same lower-third with the same animation.
5. Updating the Styled Text on the new instance does not break the animation or gradient.

## Transfer

Now try this: build a *closing* lower-third that slides out (the reverse animation). The keyframe recipe inverts — start at `0.1` (visible) and animate to `1.5` (off-screen right). Save as `DEVREL_LOWER_THIRD_OUT_v1`. Now you have a matched pair you can drop in for the in/out moments of every guest introduction.

## Working reference

- `docs/wiki/fusion-visual-effects.md#lesson-6--creating-title-animations-addendum-pp-139-167` (Text+, gradients, animation, macros — primary)
- `docs/wiki/beginners-guide.md#lesson-2--finessing-the-rough-cut-pp-69-139` (Adding the Logo, Adding the Closing Titles — beginner-tier alt path)
- `docs/wiki/master.md#shared-glossary-terms-that-appear-across-multiple-pdfs` (Text+ / Macro glossary)
- `docs/wiki/master.md#reset-matrix--when-the-user-pushes-back-read-this` (lower-third drift row)

## When the agent's work isn't matching expectations (context-rot reset)

If the user reports gradients not appearing, the Follower modifier not animating, or the saved macro missing from Effects Library, read these PDF page ranges to reset:

- `DaVinci-Resolve-20-Fusion-Visual-Effects.pdf` pp. 139-167 (Addendum: Creating Title Animations — complete workflow)
- `DaVinci-Resolve-20-Fusion-Visual-Effects.pdf` pp. 140-145 (Styling Text in the Edit Page)
- `DaVinci-Resolve-20-Fusion-Visual-Effects.pdf` pp. 142-145 (Gradient shading — Mapping Level / Mapping Angle)
- `DaVinci-Resolve-20-Fusion-Visual-Effects.pdf` pp. 145-149 (Moving Text to the Fusion Page)
- `DaVinci-Resolve-20-Fusion-Visual-Effects.pdf` pp. 153-157 (Follower modifier — for logo reveals)
- `DaVinci-Resolve-20-Fusion-Visual-Effects.pdf` pp. 163-167 (Saving a Template / Macro)
- `DaVinci-Resolve-20_Beginners-Guide.pdf` pp. 122-130 (Adding the Logo, Adding the Closing Titles)
