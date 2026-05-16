# Editor's Guide to DaVinci Resolve 20 — Wiki

**One-line summary**: The deep editing PDF. Covers the Edit and Cut pages in depth, multicam, AI Transcription, project organization, edit-page effects, audio editing, and the full Deliver page workflow. 619 pages. Roberts, 2025.

**Use this PDF when**: a user needs serious editing technique — trimming, multicam, transcription-driven cutting, render preset design, Smart Reframe, or media management.

## Table of contents

| Lesson | Chapter title | Purpose | Pages |
|---|---|---|---|
| Front | Getting Started | Install and Quick Setup | xii-xxi |
| 1 | Building the Rough Cut | Project setup, soundbite assembly, subclips, Insert/Append edits, B-roll, backtiming, music, logo | 1-73 |
| 2 | Refining the Rough Cut | Trim modes (roll, slip, ripple, slide), replace edits, closing titles, edit reviewing | 75-147 |
| 3 | Cutting a Dramatic Scene | Working with takes, blocking dialogue, reverse shots, Ripple Overwrite for alternate takes, Match Frame, pickups, Take Selector, split edits, dynamic trimming | 149-195 |
| 4 | Multicamera Editing | Editing multicam interviews, switching angles, flattening, music videos, real-time multicam, adjusting cuts | 197-243 |
| 5 | Project Organization | New project + settings, source media, importing, syncing audio to video, metadata, Keyword Smart Bins, Analyzing Clips for People (Studio), Custom Smart Bins, Subclips, **Power Bins** | 245-321 |
| 6 | AI Workflows | Proxy generation, **AI Transcription** (Studio), subclips with transcription, **Editing Using Transcription**, **Remove Silent Portions**, IntelliScript, AI Music Editor | 323-387 |
| 7 | Edit Page Effects | Compositing with traveling mattes, clip speed (variable speed, freeze frames), 3D Keyer FX, Transform FX, Video Collage, tiles | 389-473 |
| 8 | Audio Editing | Mixing prep, sound effects, syncing Foley, voiceover, balancing clips, **AI Dialogue Leveler**, EQ, sound effects balance, mixing music | 475-543 |
| 9 | Delivering Projects | AAF for Pro Tools, reformatting timelines for aspect ratios, **AI Smart Reframe** (Studio), vertical timeline, custom render preset, M&E bus, **subtitles from audio**, customizing Deliver presets, multi-project rendering, verifying exports, timeline media management | 545-617 |

## Chapter notes — chapters the skills draw on

### Lesson 2 — Refining the Rough Cut (pp. 75-147)

**Key concepts**:
- **Roll trim**: Adjust both sides of an edit point simultaneously. The total duration stays the same; only the cut location moves.
- **Slip trim**: Change the source content of a clip without moving its in/out points on the timeline. Useful when you want to keep duration but show a different moment.
- **Ripple trim**: Adjust one side of a cut; everything downstream shifts. Use when you want to add/remove time from a clip and have the rest of the timeline absorb the change.
- **Slide trim**: Move a clip in time without changing its content. Adjacent clips compress/expand to absorb.

**Shortcuts**: T = trim tool (cycle through ripple/roll/slip/slide). N = toggle snapping. Shift-comma / Shift-period = nudge edit by 5 frames.

_Source: pp. 75-147_

### Lesson 5 — Project Organization (pp. 245-321)

**Key concepts**:
- **Bins vs Smart Bins vs Power Bins**:
  - **Bin** = folder. Project-scoped. Holds clips.
  - **Smart Bin** = saved query. Dynamic; populates automatically based on criteria (e.g. "all clips with keyword X"). pp. 283-287, 302-308.
  - **Power Bin** = library-scoped bin. Spans projects in the same library. Perfect for reusable brand assets, music stings, animated logos. pp. 317-321.
- **Metadata** (pp. 278-282): Resolve indexes every clip's metadata (Scene, Shot, Take, Keywords, Description). Smart Bins query against this. Always tag your media upfront.
- **Syncing audio to video** (pp. 267-277): Two methods — **Waveform** (works without timecode, slower) or **Timecode** (instant if both clips have matching TC).

**Workflows**:

Setting up Power Bins:
1. View menu > Show Power Bins.
2. In the Power Bins panel, right-click > New Bin. Name it (e.g. BRAND ASSETS).
3. Drag reusable media in. Any project in the same library now sees these.

Keyword Smart Bin:
1. Select multiple clips in the Media Pool.
2. In the Inspector > Metadata tab, add a keyword (e.g. `interview`).
3. View menu > Show Smart Bins.
4. Right-click Smart Bins panel > Add Smart Bin. Filter: Keywords contains `interview`. Save.

_Source: pp. 245-321_

### Lesson 6 — AI Workflows (pp. 323-387)

**Key concepts**:
- **Proxy generation** (pp. 324-340): Use built-in proxy generation (right-click clip > Generate Proxy Media) OR the separate **Blackmagic Proxy Generator** app for batch jobs. H.264 Half-Res 1080p is a sane default.
- **Disk Speed Test** (p. 326): Free tool from Blackmagic. Run it on your media drive. The "Will It Work?" table shows green/red checkmarks for codec+resolution combos. If your codec is red, generate proxies.
- **AI Transcription** (Studio only, pp. 341-361): Right-click a clip > Audio Transcription > Transcribe With Speaker Detection. Resolve generates a word-level transcript.
- **Editing Using Transcription** (pp. 352-358): Click a word in the transcription panel — the source viewer jumps to that timecode. Drag through words to set In/Out automatically. F12 to Append, Shift-F12 to Insert.
- **Remove Silent Portions** (p. 358): On the timeline mode of the Transcription panel, Options menu (...) > Remove Silent Portions. Ripple-deletes silent ranges.

**Workflows**:

Full AI Transcription cut:
1. Right-click clip > Audio Transcription > Transcribe With Speaker Detection.
2. Wait ~1 min per 10 min of audio.
3. Click a word — source viewer jumps there. Drag through words to set In/Out.
4. Press F12 (Append) to add the marked range to timeline end.
5. After assembling the rough cut, click the Timeline button in the Transcription panel to switch from clip-mode to timeline-mode.
6. Options menu (...) > Remove Silent Portions.

**Misconceptions to address**:
- "I should cut on the Edit page like Premiere." Transcription-driven cutting is the fastest path for any single long recording.
- Trusting transcription accuracy — always proofread. Brand names, acronyms, and technical terms come back garbled.

_Source: pp. 323-387_

### Lesson 8 — Audio Editing (pp. 475-543)

**Key concepts**:
- **AI Dialogue Leveler** (p. 514, Studio): Inspector > Track FX > AI Dialogue Leveler. One click, evens out clip-to-clip dynamic range.
- **Track EQ** (pp. 524-533): Mixer > double-click EQ section of a track strip. Six bands. Use to cut sub-100 Hz rumble on dialogue tracks.

_Source: pp. 475-543_

### Lesson 9 — Delivering Projects (pp. 545-617)

**Key concepts**:
- **Reformatting for aspect ratios** (pp. 553-568): Duplicate timeline, change Timeline Resolution, then either use AI Smart Reframe (Studio) or manually keyframe Position.
- **AI Smart Reframe** (Studio, pp. 569-575): Select clips on the reframed timeline > Right-click > Smart Reframe. Choose Object of Interest: Auto. If the AI picks the wrong subject, switch to Reference Point mode and manually click the subject.
- **Custom Render Preset** (pp. 577-580): Configure Deliver settings, click Options menu (...) at top of Render Settings > Save As New Preset. Check "Add to Quick Export" to make it available from the Edit page cloud icon.
- **Audio Normalization standards** (p. 571): Under Audio tab > Audio Normalization > Optimize to standard. YouTube = -14 LUFS / -1.0 dBTP. Streaming = -16 LUFS. Broadcast = -23 LUFS.
- **Subtitles from audio** (pp. 586-590): Timeline menu > AI Tools > Create Subtitles from Audio. Configure max characters per line (42 is standard), single vs double line, language. Resolve creates a Subtitle track on the timeline. Right-click track > Export Subtitles > SRT.

**Workflows**:

Save a multi-platform render preset chain:
1. Press Shift-8 (Deliver page).
2. Click H.264 Master in Render Settings.
3. Configure: File Name = `%timeline_name`, Resolution = Timeline Resolution, Video codec = H.264, Audio codec = AAC at 320 Kb/s, Audio Normalization = Optimize to standard = YouTube.
4. Options menu (...) > Save As New Preset > name `DEVREL_YOUTUBE_1080`. Check Add to Quick Export.
5. Repeat for LinkedIn (1080x1080, audio = Streaming) and Shorts (1080x1920, audio = Streaming).

Subtitle export:
1. Timeline menu > AI Tools > Create Subtitles from Audio.
2. Set Maximum = 42 characters per line, Lines = Single, Gap Between Subtitles = 0 frames.
3. Click Create.
4. Playback, double-click any subtitle clip to fix transcription errors.
5. Right-click Subtitle track > Export Subtitles > SRT.

**Misconceptions to address**:
- "Manually keyframe Position for vertical exports." Use Smart Reframe or at least per-clip Reframe button.
- "Render the same edit three times in three Resolve windows." Resolve renders serially; just queue all three and click Render All.

_Source: pp. 545-617_

## When to crack open the PDF

Read the actual PDF when:

- **The user is editing dialogue / dramatic scenes**: Read Lesson 3 (pp. 149-195) for take selectors, dynamic trimming, and ripple overwrite. These workflows are not in any other PDF.
- **The user has a multi-camera shoot**: Lesson 4 (pp. 197-243) is the complete multicam reference.
- **The user pushes back on transcription-driven cuts**: pp. 341-361 walk through the workflow step-by-step with screenshots. Read it before re-suggesting.
- **The user's render output is wrong**: pp. 597-617 (Customizing Deliver Presets, Verifying the Exported Files) explains the verification workflow and naming convention restrictions.
- **The user needs Smart Reframe to follow a different subject**: pp. 572-575 cover the Reference Point fallback specifically.
- **The user wants subtitles**: pp. 586-590. The skill workflow is condensed but this is where the per-language and per-format options are explained.
- **Multi-project rendering**: pp. 602-607 covers the unusual "render across projects in one queue" workflow.

## Author

Built by Jai Bhagat. More at chaiwithjai.com.
