---
name: social-video-folder-autocutter
description: Plan repeatable hard-drive folder-to-video pipelines for speaker-led multicam content, including 9:16 Reels/Shorts up to 3 minutes at 1.1x talking speed and 16:9 long-form 3-7 minute cuts, with Resolve handoff, Editframe asset generation, audio/caption gates, and narrative beat planning.
---

# Social Video Folder Autocutter

Use this before editing when the user wants a repeatable pipeline from a folder of camera/audio files into social or long-form cuts.

## Output Profiles

- **Vertical social:** `1080x1920`, 9:16, up to 3 minutes, default 1.1x speed for speaker-led sections, Netflix-style captions, source layers preserved in Resolve.
- **Horizontal long-form:** `1920x1080`, 16:9, 3-7 minutes, default normal speed, lower thirds/captions optional, source layers preserved in Resolve.

## Required Pipeline

1. Scan the folder:
   - run the DaVinci skill `probe_media.py`;
   - run `audio_quality_audit.py`;
   - identify camera ISOs, HQ audio, intro/bumper, brand files, old renders, and existing Resolve exports.
2. Make a story plan:
   - hook/agenda,
   - body beats,
   - recap/CTA,
   - rejected or risky segments.
3. Build edit decisions:
   - source file, in/out, angle, reason, transition, crop, audio source, caption text.
   - reject word-boundary-only cuts.
4. Build a B-roll coverage plan:
   - assign B-roll only where it proves a claim, establishes the event world, covers a jump cut, compresses time, or gives the audience an emotional/visual release.
   - tag every B-roll candidate as `wide`, `medium`, `close-up`, `insert/detail`, `environment`, `screen/product`, or `human moment`.
   - prefer wide/medium/close-up sequences over isolated filler shots.
   - require source page/licensing metadata for stock footage and store it with the manifest.
   - reject low-opacity overlays over faces unless the user explicitly asks for texture; default to full-opacity cutaways or designed picture-in-picture.
   - On warm-traffic educational reels, use B-roll sparingly as proof/coverage. Keep the speaker on screen for trust-building beats, and reserve stock inserts for claims about work, learning, planning, community, or tool use.
   - If the speaker is physically demonstrating a concept, prioritize that performance over generic B-roll. Use the board/prop as a quick visual aid, not a long replacement for the speaker.
   - Reject static whiteboard/slide replacements longer than `3s-5s` unless the user explicitly asks for a screen-recording style lesson. For Instagram, the speaker should remain visible across spoken educational beats.
   - Keep B-roll source URLs/license notes in the plan, and keep raw B-roll sources disabled on a separate Resolve track for HITL replacement.
   - Use Coverr as the default free B-roll source when the project lacks enough native visual evidence. Store search query, source URL, creator/source attribution, license URL, download path, and rejection reason for any candidate not used.
   - Coverr licensing/API notes must be recorded with the manifest: free downloads require attribution credit unless the account/license says otherwise; API usage requires clickable Coverr attribution; do not use Coverr assets for AI training/datasets or to build a competing stock/video service.
   - For Chai With Jai workshop promos, default search intents should include: `small business owner`, `entrepreneur workshop`, `business planning`, `whiteboard`, `team collaboration`, `laptop work`, `coffee meeting`, `Jersey City`, `AI technology`, `coding`, `marketing campaign`, and `community event`.
   - Prefer Coverr clips that can function as visual evidence for a spoken claim. Reject generic city lights, abstract technology, slow lifestyle filler, or anything with identifiable brands/trademarks unless the usage is clearly safe.
5. Generate review artifacts:
   - low-res proxy or stills for critic review,
   - audio ranking JSON,
   - caption preview,
   - Resolve/FCPXML/EDL plan.
6. Build the real handoff:
   - Resolve layered timeline for final editing,
   - original repair audio disabled,
   - clean dialogue and music separated,
   - graphics/captions/B-roll on separate tracks,
   - timeline audit passes.

## Winning Instagram Reels Loop

Use this loop when a prior cut is close and the user says it is nearly postable:

1. **Preserve the liked picture cut.** Do not re-edit the spine unless the user asks. Export or locate a picture spine without burned captions when possible.
2. **Caption from actual speech timing.** Extract dialogue from the liked cut, run Whisper word-level transcription, and build short burned-in phrase captions. Correct only high-confidence domain terms such as names, event titles, dates, and obvious ASR artifacts.
3. **Keep caption text spoken-first.** Do not replace spoken captions with topic cards. Topic cards may remain as a separate top lane, but the lower caption lane must match what the speaker says.
4. **Verify phone-safe stills.** Inspect opening, mid-body, B-roll/whiteboard, CTA, and closing frames. Captions must avoid the speaker's mouth/chin and Instagram's bottom UI region.
5. **Verify audio.** Target `-14` to `-16 LUFS` integrated, true peak below `-1 dBTP`, with music ducked under speech.
6. **Only then hillclimb B-roll.** Add B-roll where it solves a specific edit problem: jump cut coverage, proof of a claim, visual explanation, location/event context, or emotional reset.

## Required Output Artifacts For Repeat Use

For each folder cut, create or update:

- `story_plan.md`
- `edit_decisions.csv` or `.json`
- `broll_plan.json`
- `broll_asset_manifest.json`
- `caption_chunks.txt`
- `captions.ass` or Resolve caption track
- `verification_report.json`
- Resolve timeline or handoff report

## Editframe Role

Use Editframe in parallel for motion assets, not as the primary NLE when the user expects Resolve source layers.

Good uses:

- animated branded bumpers,
- Netflix-style/word-highlight caption assets,
- lower thirds,
- waveform/title cards,
- social-safe graphic overlays,
- fast HTML/React review proxies.

Avoid using Editframe as the only deliverable for source-camera editing unless the user explicitly wants a rendered web-video output. Editframe renders can be imported back into Resolve as V3/V4 graphics or bumper layers.

## Handoff Contract

Never call the job done unless these artifacts exist:

- media manifest,
- story plan,
- edit decisions,
- audio quality audit,
- caption artifact or burned-in review,
- layered Resolve timeline or interchange file,
- timeline audit report.

## Useful Command

```bash
python3 skills/social-video-folder-autocutter/scripts/create_folder_cut_brief.py \
  /path/to/project-folder --out /path/to/project-folder/output/folder_cut_brief.json
```

Then use `davinci-resolve-social-editor` for the Resolve build.
