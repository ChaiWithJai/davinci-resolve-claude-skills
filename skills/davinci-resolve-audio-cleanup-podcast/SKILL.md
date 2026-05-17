---
name: davinci-resolve-audio-cleanup-podcast
description: Use when a user has podcast, interview, or talking-head audio that needs cleanup — denoise, de-hum, level dialogue, and duck music under voice. Triggering symptoms include phrases like "podcast audio is noisy", "background hum in interview", "music too loud under voice", "level out my voiceover", "fix my podcast", or any DaVinci Resolve Fairlight audio cleanup question.
---

# DaVinci Resolve — clean podcast and interview audio

## Overview

The four-step podcast audio cleanup chain: **EQ out rumble -> kill any hum -> denoise -> level -> duck music**. Done in this order. The principle: address frequency problems before dynamic problems. EQ is surgical; noise reduction is destructive. Use the surgical tool first so the destructive tool has less to do.

## When to use

Symptoms:
- Recording has background hum (electrical 50/60 Hz interference)
- Air conditioning, refrigerator, or traffic noise floor under dialogue
- Voice levels vary from clip to clip (loud intros, quiet thoughtful moments)
- Music score drowns out the host when they start talking
- Sibilance ("ess" sounds) too harsh

When NOT to use:
- Multi-mic interview where you need to gate each mic separately — that needs the Track-level Dynamics workflow per mic (Fairlight Audio Post pp. 373-375).
- Audio is destroyed (clipped, severe wind noise, water damage) — there is a limit to what cleanup can do. Re-record if possible.
- You need surround/Atmos mixing — different chapter (Fairlight Audio Post pp. 643+).

## Quick reference — the cleanup chain in order

### Phase -1 — source audit before cleanup

Before applying effects, audit every candidate audio source. Do not assume the named lav/boom file is best. Check:

- duration matches picture
- silence percentage
- integrated LUFS
- true peak
- clipping risk
- audible room tone/hum
- whether the track is actually silent

For multi-camera workshop folders, keep the selected dialogue on `A1`, the processed dialogue on `A2`, music/ambience on `A3`, and SFX/bumpers on `A4`. If the external mic peaks near `0 dBFS`, preserve it as source but create a processed duplicate with conservative limiting/leveling before delivery.

| Step | Tool | When to use | Where |
|---|---|---|---|
| 1. EQ rumble | **Clip EQ** (Inspector > Equalizer) | Always — every dialogue clip has sub-100Hz garbage | Inspector panel, audio clip selected |
| 2. De-Hummer | **Fairlight FX > De-Hummer** | Power line buzz (50 Hz Europe, 60 Hz US) | Drag from Effects Library onto clip |
| 3. Gate the noise floor | **Mixer > Dynamics > Gate** | Air conditioner / room tone audible between sentences | Mixer track dynamics panel |
| 4. Noise Reduction | **Fairlight FX > Noise Reduction** | Stubborn broadband noise that survives steps 1-3 | Drag from Effects Library onto clip or track |
| 5. AI Dialogue Leveler | **Inspector > AI Dialogue Leveler** (Studio) or manual keyframes | Voice gets loud/quiet within a sentence | Inspector Track FX section |
| 6. Ducker | **Track FX > Ducker** | Music too loud under dialogue | Inspector on the music track |

## Steps

### Phase 0 — Switch to Fairlight, set up your monitoring

1. Press **Shift-7** to switch to the Fairlight page.
2. Open the Mixer (Toolbar > Mixer button).
3. Put on headphones. You will hear problems on headphones that you will miss on laptop speakers.

### Step 1 — Clip EQ: cut everything below 80 Hz (always)

This is non-negotiable. Every voice recording has rumble, HVAC, traffic, and breath plosives under 80 Hz that contribute nothing to intelligibility but eat up headroom.

1. Select a dialogue clip in the timeline.
2. Open the **Inspector** (top right of the interface, then Audio tab).
3. Scroll down to **Equalizer**. Turn it ON (the radio button next to "Equalizer").
4. By default, Bands 2-5 are enabled. Set **Band 2** to **Low Shelf** (the first icon in the Band Filter Type dropdown).
5. Drag the Band 2 handle in the graph **down to -70 dB** and **right until the shelf reaches the 80-100 Hz line**.
6. Repeat for every dialogue clip — or **copy attributes** from this clip to all others (Cmd-C on the clip, select others, Edit > Paste Attributes, check Equalizer only, Apply).

Fairlight Audio Post pp. 368-372 walks through this with the same EQ controls.

### Step 2 — De-Hummer for any electrical hum

If you hear a constant tone behind the voice — usually a low buzz at 50 Hz or 60 Hz from poor cable shielding or a ground loop — use the De-Hummer.

1. Open the **Effects Library** (top-left button on Fairlight page).
2. Under **Audio FX > Fairlight FX**, find **De-Hummer**.
3. Drag De-Hummer onto the affected clip in the timeline.
4. In the De-Hummer window, click **60 Hz** (or 50 Hz if you are in Europe / Asia / Africa).
5. Drag the **Amount** knob right until the hum disappears. Typical setting: `-20 to -30 dB`.
6. Adjust the **Slope** knob slightly right if you still hear harmonics (multiples of 60 Hz — 120, 180, 240).
7. Click the **Bypass** switch at the top to A/B compare. The Bypass switch is red when the filter is on.

Fairlight Audio Post pp. 376-380 covers this exactly. The trick is that the De-Hummer is a *notch filter* — it removes specific frequencies without affecting nearby ones, unlike EQ.

### Step 3 — Gate the noise floor (track-level dynamics)

If there is a low-level hiss, computer fan, or AC noise that is *audible between sentences but masked when the voice is playing*, a gate kills it.

1. In the **Mixer**, find the dialogue track's channel strip.
2. Double-click the **Dynamics** section to open the Dynamics panel.
3. Click the **Gate** button to enable.
4. Start with these settings:
   - **Threshold**: -35 dB (default)
   - **Range**: -18 dB (start conservative)
   - **Attack**: 1.4 ms
   - **Hold**: 0 ms
   - **Release**: 93 ms
5. Play back the track. The Gain Reduction meter should activate only between sentences (when no voice). If the gate cuts off the start of words, raise the threshold (less negative). If it cuts off breaths or quiet sentence endings, lower the range.

The exact starting values come from Fairlight Audio Post pp. 373-375.

### Step 4 — Noise Reduction (when steps 1-3 are not enough)

Some recordings have broadband noise (general "hisssss") that EQ cannot remove and the gate would chop up too aggressively. Use the Fairlight FX Noise Reduction.

1. From the Effects Library > **Audio FX > Fairlight FX**, drag **Noise Reduction** onto the affected clip.
2. The Noise Reduction panel opens. You have two modes:
   - **Manual** (default) — you "teach" the plug-in what the noise sounds like
   - **Auto Speech Mode** — algorithm separates speech from noise automatically
3. **For Auto Speech Mode**: just enable it. Adjust the **Dry/Wet** slider (default 80%). Lower it if voices start sounding "underwater."
4. **For Manual mode**:
   a. Find a section of the clip with *only noise* (silent gap, ideally at the start before anyone speaks).
   b. Click **Learn** to enable noise-profile capture.
   c. Play the noise-only section.
   d. Click **Learn** again to stop. The plug-in has now "learned" the noise.
   e. Play back the full clip — noise should drop dramatically.

Fairlight Audio Post pp. 381-383 covers both modes. Studio version only — free Resolve does not have the Noise Reduction plug-in. Free users: use a more aggressive Clip EQ (step 1) combined with the Gate (step 3).

### Step 5 — AI Dialogue Leveler (Studio) or manual keyframes (Free)

Voices have natural dynamic range — a person gets quieter as they finish a sentence. The leveler evens this out.

**Studio approach** (one click):

1. Select the dialogue clip.
2. In the Inspector > **Track FX** section, enable **AI Dialogue Leveler**.
3. That is it. Adjust the strength slider if it sounds too "compressed."

**Free Resolve approach** (manual keyframes):

1. In the Edit page, Option-click (Mac) / Alt-click (Windows) the volume bar in an audio clip to add keyframes.
2. Add a keyframe before a quiet section, another keyframe after.
3. Drag the volume bar between keyframes up (typically +3 to +6 dB) to boost the quiet section.

Beginner's Guide pp. 150-153 covers the manual keyframe workflow with screenshots.

### Step 6 — Duck the music under dialogue

If you have music underneath voice and the music swallows the voice, use the Ducker.

1. Select the **MUSIC** track (or the music clip).
2. In the Inspector > **Track FX** section, enable **Ducker**.
3. In the Ducker controls:
   - **Source 1** dropdown: set to your dialogue track (e.g. DIALOGUE).
   - **Duck Level**: start at **2.7** dB (the default — a subtle duck).
   - If you have multiple dialogue tracks (host + guest), click the **+** to add Source 2 and Source 3.
4. Play back. Watch the Ducker Graph — when dialogue plays, the music level dips automatically.
5. If the duck is too dramatic, lower Duck Level. If you cannot hear the voice over music, raise Duck Level.

Fairlight Audio Post pp. 552-558 covers Ducker in depth, including the warning that **Duck Level > 5 dB sounds amateurish** because the audience perceives the dip.

## Common mistakes

- **Applying Noise Reduction first, then EQ** -> wrong order. EQ out the obvious frequencies first so the Noise Reduction has less to remove and is less destructive. **(This is the misconception this skill addresses head-on.)** Fairlight Audio Post p. 368-372 establishes EQ before p. 381-383 noise reduction for this reason.
- **Setting the Gate threshold too high** -> it cuts off the start of each word. Listen carefully and back the threshold off.
- **Cranking the Ducker Duck Level above 5 dB** -> the audience hears the level swing and it feels artificial. Stay subtle.
- **Forgetting that the Bypass switch is RED when ACTIVE** -> the convention is inverted from what you might expect. Red = filter is engaged.
- **Trying to fix wind noise** -> the Fairlight FX cannot meaningfully fix wind. Re-record or use iZotope RX externally.

## Verification

You succeeded if all of the following are true:

1. Listening on headphones at moderate volume, you cannot hear hum, hiss, or AC noise between sentences.
2. The loudness meter (top right of Fairlight) reads between -16 and -20 LUFS over the entire timeline (this is podcast-standard loudness).
3. Voice clips peak at around -9 dBFS to -3 dBFS but never clip (red).
4. Music plays at full volume when there is no voice, ducks audibly but smoothly when voice starts, returns to full when voice ends.
5. Bypassing the Clip EQ on the dialogue clip makes the audio sound noticeably "boomier" and worse — the EQ is doing something audible.

## Transfer

Now try this on a 3-person podcast where each person has their own mic (so three separate dialogue tracks). The cleanup chain is the same per track, but the Ducker setup changes: in the music track's Ducker, add Source 1, 2, and 3 pointing at each of the three dialogue tracks. The music will duck when *any* of the three is speaking. If two people talk over each other, the duck does not stack — you get the same -2.7 dB dip whether one or three voices are active.

## Working reference

- `docs/wiki/fairlight-audio-post.md#lesson-6--audio-repairs-pp-367-415` (full cleanup chain — primary)
- `docs/wiki/fairlight-audio-post.md#lesson-9--mixing-and-sweetening-pp-535-612` (Ducker setup)
- `docs/wiki/beginners-guide.md#lesson-3--audio-editing-and-quick-export-pp-141-179` (free Resolve fallback — manual keyframes + Fairlight FX)
- `docs/wiki/editors-guide.md#lesson-8--audio-editing-pp-475-543` (AI Dialogue Leveler reference)
- `docs/wiki/master.md#reset-matrix--when-the-user-pushes-back-read-this` (audio symptom rows — hum, hiss, ducker)

## When the agent's work isn't matching expectations (context-rot reset)

If the user reports remaining hum, hiss, robotic ducking, or that the chain order was different, read these PDF page ranges to reset:

- `DaVinci-Resolve-20-Fairlight-Audio-Post.pdf` pp. 368-372 (Clip EQ for low-frequency reduction)
- `DaVinci-Resolve-20-Fairlight-Audio-Post.pdf` pp. 373-375 (Dynamics Gate, gating low-level noise)
- `DaVinci-Resolve-20-Fairlight-Audio-Post.pdf` pp. 376-380 (De-Hummer for power line hum)
- `DaVinci-Resolve-20-Fairlight-Audio-Post.pdf` pp. 381-389 (Noise Reduction — manual and Auto Speech Mode)
- `DaVinci-Resolve-20-Fairlight-Audio-Post.pdf` pp. 552-558 (Ducker — Duck Level cap at 5 dB)
- `DaVinci-Resolve-20_Beginners-Guide.pdf` pp. 142-158 (manual keyframes + Fairlight FX for free Resolve)
- `DaVinci-Resolve-20-Editors-Guide.pdf` p. 514 (AI Dialogue Leveler one-click voice leveling)
