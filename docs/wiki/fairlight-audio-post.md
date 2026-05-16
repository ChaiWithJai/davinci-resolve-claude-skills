# Fairlight Audio Post Guide to DaVinci Resolve 20 — Wiki

**One-line summary**: The audio post-production PDF. Covers building soundtracks, dialogue editing, sound design, recording (VO/ADR/Foley), mixing, repair, and final delivery from the Fairlight page. 727 pages. Plummer, 2025.

**Use this PDF when**: a user is doing serious audio — podcast cleanup, dialogue repair, ducking music, mixing to broadcast loudness, recording voiceover or ADR, or working with busses.

## Table of contents

| Lesson | Chapter title | Purpose | Pages |
|---|---|---|---|
| Front | Getting Started | Install and Quick Setup | xi-xxv |
| 1 | Building a Soundtrack | Empty project, importing audio, clip volumes, manual tracks, trimming, markers, balancing | 1-79 |
| 2 | Editing Dialogue Tracks | Multichannel prep, checkerboard editing, mono channels, voiceover takes, audio track layers, patchwork edit, **AI Speech-to-Text** | 81-159 |
| 3 | Editing Sound Effects and Music | Markers, Focus Mode, snapping, **Sound Library**, sync points, scrollers, beat editing, nested timelines, crossfades, podcast music, **Music Remixer** | 161-244 |
| 4 | Recording Voiceover, ADR, and the Foley Sampler | Microphone setup, patching tracks, consecutive takes, track-layer recording, **ADR session**, recording ADR cues, importing cue lists, oscillator, Foley Sampler | 247-310 |
| 5 | Balancing Clips and Panning Tracks | Dialogue clip levels, auto-leveling, panoramic placement, pan tracking | 313-364 |
| 6 | Audio Repairs with Native Processing and Plug-Ins | Finding the problem, **gating low-level noise**, **Clip EQ**, **De-Hummer**, **Noise Reduction**, processor-intensive plugins, Track FX, click removal, time stretching | 367-415 |
| 7 | Using Fairlight FX and Processing for Creative Sound Design | Keyboard shortcuts, altering dialogue, futzing (PA system simulation), saving presets, modulation, pitch/time, doubling | 417-472 |
| 8 | Simplifying the Mix with Groups, Busses, and Nested Timelines | Multichannel link groups, track groups, busses, auxiliary echo bus, nested timelines, **timeline template** | 475-533 |
| 9 | Mixing and Sweetening the Soundtrack | Reference tracks, initial track/submix levels, **Ducker**, fader automation, compression, sidechain auto-ducking, EQ, AI Processing | 535-612 |
| 10 | Finishing and Delivering Tracks | **Loudness monitoring**, bouncing mixes, exporting stems, exporting files, stereo/5.1 in Deliver | 615-640 |
| 11 | Exploring Immersive Audio Integration | Ambisonics, Dolby Atmos basics | 643-724 |

## Chapter notes — chapters the skills draw on

### Lesson 1 — Building a Soundtrack (pp. 1-79)

**Key concepts**:
- **Track formats** (pp. 19-30): Mono, Stereo, 5.1, 7.1, etc. Set when creating the track. Mismatched formats (mono mic on stereo track without conversion) cause channel-1-only playback issues.
- **Clip volume** (p. 11): Inspector > Volume slider, OR drag the rubber-band on the audio clip. Per-clip gain.
- **Markers** (pp. 31-37): Press M to add. Color-coded. Useful for spotting cues during dialogue edit.

**Workflows**:
- Switch to Fairlight (Shift-7). The Mixer is at Toolbar > Mixer button.
- Always put on headphones — problems audible on phones are missed on laptop speakers.

_Source: pp. 1-79_

### Lesson 2 — Editing Dialogue Tracks (pp. 81-159)

**Key concepts**:
- **Checkerboard editing** (p. 106): Place each speaker on alternating tracks (A1 = Host, A2 = Guest). Makes it easy to apply per-speaker EQ and ducking.
- **Audio Track Layers** (pp. 136-148): Stack overlapping takes on layered "layers" within one track. Move clips between layers to A/B compare takes without losing alternates.
- **AI Speech-to-Text** (p. 153, Studio): In Fairlight, right-click clip > Audio Transcription. Same engine as the Editor's Guide AI Transcription but with audio-track focus.

_Source: pp. 81-159_

### Lesson 6 — Audio Repairs (pp. 367-415)

**This is the chapter that powers the audio cleanup skill.**

**Key concepts and order — surgical before destructive**:
1. **Clip EQ** (pp. 376-383): Surgical. Cut specific frequencies without affecting nearby ones. Use first.
2. **De-Hummer**: Notch filter for power line hum (50 Hz Europe, 60 Hz US). Targets the fundamental + harmonics.
3. **Gate** (pp. 373-375): Cuts audio below a threshold. Removes noise floor between sentences.
4. **Noise Reduction** (pp. 381-389): Destructive. Reduces broadband noise but artifacts speech if pushed. Use last.

**Clip EQ workflow** (pp. 368-372):
1. Select dialogue clip in timeline.
2. Inspector > Audio tab > Equalizer. Turn ON.
3. Band 2 → set to Low Shelf (first icon in filter type dropdown).
4. Drag Band 2 handle in the graph: down to -70 dB, right until shelf reaches 80-100 Hz.
5. To apply to all dialogue clips: Cmd-C the clip, select others, Edit > Paste Attributes, check Equalizer only, Apply.

**De-Hummer workflow** (pp. 376-380):
1. Effects Library > Audio FX > Fairlight FX > De-Hummer. Drag onto clip.
2. Click 60 Hz (US) or 50 Hz (Europe).
3. Drag Amount knob right until hum disappears. Typical: -20 to -30 dB.
4. Adjust Slope if harmonics (120, 180 Hz) remain.

**Gate workflow** (pp. 373-375):
1. In the Mixer, find dialogue track strip.
2. Double-click Dynamics section to open Dynamics panel.
3. Click Gate to enable. Starting values:
   - Threshold: -35 dB
   - Range: -18 dB
   - Attack: 1.4 ms
   - Hold: 0 ms
   - Release: 93 ms
4. Gain Reduction meter should activate only between sentences.

**Noise Reduction workflow** (pp. 381-389):
1. Effects Library > Audio FX > Fairlight FX > Noise Reduction (Studio only). Drag onto clip.
2. Two modes: **Auto Speech Mode** (one-click, recommended) or **Manual** (teach noise profile from a silent section).
3. Adjust Dry/Wet slider — lower it if voice sounds "underwater."

**Misconceptions to address — CRITICAL**:
- **Wrong order**: Applying Noise Reduction *before* EQ. NR is destructive. EQ out the obvious problems first so NR has less to remove. Order must be: Clip EQ → De-Hummer → Gate → Noise Reduction → Leveler.
- **Bypass switch is RED when ACTIVE**, not the other way around. Resolve's convention is inverted from many DAWs.
- **Trying to fix wind noise**: Fairlight FX cannot meaningfully fix wind. Re-record or use iZotope RX externally.

_Source: pp. 367-415_

### Lesson 8 — Busses and Nested Timelines (pp. 475-533)

**Key concepts**:
- **Bus** = a routing destination that combines multiple tracks. Three types:
  - **Main bus** = final output (your stereo / 5.1 / Atmos mix).
  - **Sub bus / submix** = group multiple tracks for shared processing (e.g. all dialogue tracks → DIALOGUE bus).
  - **Auxiliary bus** = parallel processing (e.g. reverb send).
- **Timeline configuration preset** (pp. 525-532): Save your entire Fairlight track + bus + naming structure as a preset. Apply to any new timeline.

**Saving a Fairlight timeline preset**:
1. Fairlight menu > Presets Library.
2. Filter by Fairlight Configuration Presets.
3. Save New > Create New. Name it. Save.

_Source: pp. 475-533_

### Lesson 9 — Mixing and Sweetening (pp. 535-612)

**Key concepts**:
- **Ducker** (pp. 552-558): On a music track, lower volume automatically when a source dialogue track is active.
  - Source 1 = primary dialogue track. Add Source 2, 3 if multi-host.
  - Duck Level default 2.7 dB. **Above 5 dB sounds amateurish** — audience perceives the dip.
- **Compression** (pp. 572-577): Mixer > Dynamics > Compressor. Smooths dynamic range. Common starting point for dialogue: Threshold -20 dB, Ratio 3:1, Attack 10 ms, Release 100 ms.
- **Sidechain auto-ducking** (p. 578): An alternative to the Ducker. Compressor with a sidechain input from another track.

**Workflows**:

Ducker setup (music ducking under dialogue):
1. Select MUSIC track.
2. Inspector > Track FX > Ducker. Enable.
3. Source 1 = DIALOGUE track. (Add Source 2, 3 for multi-host.)
4. Duck Level = 2.7 dB (subtle). Cap at 5 dB.

_Source: pp. 535-612_

### Lesson 10 — Loudness and Delivery (pp. 615-640)

**Key concepts**:
- **Loudness monitoring** (pp. 616-623): Loudness meter in Fairlight reads LUFS (integrated and short-term), LRA (Loudness Range), and dBTP (True Peak).
- **Loudness targets**:
  - YouTube: -14 LUFS, -1.0 dBTP
  - Streaming (generic / podcast): -16 LUFS, -1.0 dBTP
  - Broadcast: -23 LUFS (EBU R128), -1.0 dBTP
- **Bouncing mixes** (pp. 624-631): Render the main bus to a file (WAV, MP3) directly from Fairlight without going to Deliver. Or use Deliver for more codec options.

_Source: pp. 615-640_

## When to crack open the PDF

Read the actual PDF when:

- **The user is recording voiceover or ADR**: Lesson 4 (pp. 247-310). The ADR workflow specifically requires PDF-level detail; the wiki summary will not give you correct cue management or session setup.
- **The user has a multi-mic podcast with bleed between mics**: pp. 373-375 (Gate) plus Lesson 2 checkerboard editing (pp. 81-159) — combined approach is in the PDF, not summarized in the wiki.
- **The user wants surround or Dolby Atmos**: Lesson 11 (pp. 643-724) is the only place this is documented.
- **The user's loudness reading is way off**: pp. 616-623 explains how each LUFS measurement is computed (integrated vs short-term vs LRA) — needed to diagnose meter discrepancies.
- **Creative sound design — pitch shifting, modulation, doubling**: Lesson 7 (pp. 417-472). Wiki does not summarize these.
- **The user pushes back on cleanup order**: pp. 367-415 is the canonical sequence. Re-read before re-suggesting a different order.

## Author

Built by Jai Bhagat. More at chaiwithjai.com.
