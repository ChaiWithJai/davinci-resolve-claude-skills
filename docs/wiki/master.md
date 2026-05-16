# DaVinci Resolve 20 — Master Wiki

The agent's working memory for DaVinci Resolve 20. Six PDFs from Blackmagic Design are the ground truth; the per-PDF wikis in this directory are working summaries. This master wiki tells you which PDF to crack when, and how to reset the model when your output drifts from what the user expects.

## How to use this wiki

1. **Start here** when you don't know which PDF holds the answer. The cross-PDF index below maps Resolve features and question types to the right PDF.
2. **Open the per-PDF wiki** for a chapter-level summary. Page ranges at the end of each notes block point back to the PDF for deep reads.
3. **Read the PDF directly** when the wiki is wrong, incomplete, or when the user pushes back on your technique. PDFs are ground truth.

The wikis are working summaries — not full transcripts. When precision matters (specific knob values, exact menu paths, the order of two adjacent steps), go to the PDF page range.

## Cross-PDF index — which PDF for which question?

| Question / feature | PDF | Per-PDF wiki |
|---|---|---|
| Install, system requirements, preferences | Beginner's Guide | `beginners-guide.md` |
| Cut/Edit page basics, J-K-L, In/Out, trim modes | Beginner's Guide | `beginners-guide.md` |
| AI Transcription, Remove Silent Portions | Editor's Guide | `editors-guide.md` |
| Multicam editing | Editor's Guide | `editors-guide.md` |
| Smart Bins, Power Bins, project organization | Editor's Guide | `editors-guide.md` |
| Proxies, Blackmagic Disk Speed Test | Editor's Guide | `editors-guide.md` |
| Delivery, render presets, AI Smart Reframe, subtitles | Editor's Guide | `editors-guide.md` |
| Audio sync (waveform / timecode) | Editor's Guide | `editors-guide.md` |
| Color page interface, scopes | Colorist Guide | `colorist-guide.md` |
| Primary grading (Lift / Gamma / Gain) | Colorist Guide | `colorist-guide.md` |
| Nodes, node order, Outside / Layer / Parallel mixers | Colorist Guide | `colorist-guide.md` |
| Qualifier, Power Windows, skin-tone refinement | Colorist Guide | `colorist-guide.md` |
| Shot matching, color management, LUTs | Colorist Guide | `colorist-guide.md` |
| HDR Wheels, raw, ACES | Colorist Guide | `colorist-guide.md` |
| Fairlight interface, tracks, mixer | Fairlight Audio Post | `fairlight-audio-post.md` |
| Clip EQ, De-Hummer, Noise Reduction, Gate | Fairlight Audio Post | `fairlight-audio-post.md` |
| AI Dialogue Leveler | Fairlight Audio Post | `fairlight-audio-post.md` |
| Ducker, music ducking, busses | Fairlight Audio Post | `fairlight-audio-post.md` |
| Loudness (LUFS, dBTP), delivery | Fairlight Audio Post | `fairlight-audio-post.md` |
| Voice-over, ADR, Foley | Fairlight Audio Post | `fairlight-audio-post.md` |
| Fusion interface, nodes, Merge node | Fusion Visual Effects | `fusion-visual-effects.md` |
| Text+, gradients, animated titles, lower-thirds | Fusion Visual Effects | `fusion-visual-effects.md` |
| Save As Macro / Template | Fusion Visual Effects | `fusion-visual-effects.md` |
| Tracker, planar tracking, sky replace | Fusion Visual Effects | `fusion-visual-effects.md` |
| Green screen / Delta Keyer | Fusion Visual Effects | `fusion-visual-effects.md` |
| 3D scenes, 3D text, lights, cameras | Advanced Visual Effects | `advanced-visual-effects.md` |
| 3D camera tracking | Advanced Visual Effects | `advanced-visual-effects.md` |
| USD, 3D particles, depth | Advanced Visual Effects | `advanced-visual-effects.md` |

## Shared glossary (terms that appear across multiple PDFs)

- **Bin** — a folder in the Media Pool. Project-scoped. Holds clips, timelines, and other bins. Editor's Guide ch. 5.
- **Smart Bin** — a dynamic query over the Media Pool (e.g. "all clips with keyword interview"). Not a folder; a saved filter. Editor's Guide pp. 283-287, 302-308.
- **Power Bin** — a library-scoped bin that spans projects. Used for brand assets, music stings, reusable graphics. Editor's Guide pp. 317-321.
- **Clip / Track / Timeline** — Clip = a single piece of media on a track. Track = a horizontal lane (V1, V2, A1, A2...). Timeline = the assembled edit; multiple timelines can live in one project.
- **Page** — Resolve has seven pages: Media, Cut, Edit, Fusion, Color, Fairlight, Deliver. Switch with Shift-3 through Shift-8 (or click the tabs at the bottom). The Media page is Shift-2.
- **Node** — a unit in the Color page (and in Fusion). On the Color page, a node is a grading step; nodes connect serially or in parallel. In Fusion, a node is an image-processing operation (Merge, Blur, Transform, etc.).
- **Qualifier** — Color-page tool that isolates a color or luminance range (HSL most common). Combined with a Power Window for spatial isolation. Colorist Guide ch. 3.
- **Power Window** — a shape (linear, circle, polygon, gradient) that masks a grade to a region of the frame.
- **OFX** — Open FX, the plugin standard Resolve uses for ResolveFX and third-party effects. Available on the Color, Edit, and Fusion pages.
- **Inspector** — the right-hand panel on the Edit, Fusion, Color, and Fairlight pages. Holds clip attributes, FX parameters, transform controls.
- **PowerGrade** — a saved grade still in the Color page Gallery that persists across projects. Apply to a new clip via Apply Grade. Colorist Guide pp. 246-250.
- **Text+** — a Fusion-backed text generator on the Edit page. More animatable than the basic Text generator. Fusion VFX pp. 140-145.
- **Macro** — a Fusion node group saved as a single reusable tool. Lives in Effects Library after saving. Fusion VFX pp. 163-167.
- **Render preset** — a saved set of Deliver page settings. Editor's Guide pp. 577-580.
- **AI Smart Reframe** — Studio-only feature that adds Position keyframes to follow a subject when changing aspect ratio. Editor's Guide pp. 569-575.
- **LUFS** — Loudness Units relative to Full Scale. Broadcast/streaming loudness target. YouTube uses -14 LUFS; streaming generic uses -16 LUFS. Fairlight Audio Post pp. 616-624.
- **dBTP** — Decibels True Peak. Hard ceiling for delivery (-1.0 dBTP for YouTube).
- **Live Save** — auto-save on every change. Enable in Preferences > User > Project Save and Load.
- **Project backups** — separate from Live Save. Time-based snapshots (every 10 min / hourly / daily). Colorist Guide pp. 6-7.
- **Proxy** — a lower-resolution stand-in clip. Generated by Resolve or by the separate Blackmagic Proxy Generator app. Editor's Guide pp. 324-340.

## Reset matrix — when the user pushes back, read this

The single most important table in this wiki. If the user disputes your output, find the symptom and read the cited PDF pages to reset your mental model before responding again.

| User symptom / pushback | What's probably wrong | PDF + pages to re-read |
|---|---|---|
| "Skin tones look orange / green / red" | Skipped Node 2 balance, or qualifier matte includes background | Colorist Guide pp. 16-19, 118-138 |
| "The color doesn't match the reference" | Used eyeballed grade instead of scope-based; missed shot match | Colorist Guide pp. 11-19, 46-71 |
| "Audio drifts out of sync over time" | Frame rate mismatch between clip and timeline, or sample rate mismatch | Editor's Guide pp. 267-277 |
| "Render queue completed but the file is missing / 0 bytes" | Invalid character in filename, or output folder permissions | Editor's Guide pp. 597-617 |
| "Red playback indicator / dropped frames" | Drive too slow, not GPU. Diagnose with Disk Speed Test first | Editor's Guide pp. 324-340 |
| "Hum / hiss won't go away after Noise Reduction" | Wrong tool order. EQ + De-Hummer first; NR is destructive and last | Fairlight Audio Post pp. 368-383 |
| "Music drowns out the voice" / "Ducker sounds robotic" | Duck level set above 5 dB, or source dialogue track not assigned | Fairlight Audio Post pp. 552-558 |
| "AI Transcription cut the wrong word / kept the ums" | Transcription edits at word boundaries but breaths fall between words | Editor's Guide pp. 352-360 |
| "Lower-third looks janky / doesn't animate smoothly" | Used basic Text generator instead of Text+; or no spline smoothing | Fusion VFX pp. 140-167 |
| "AI Smart Reframe lost the subject mid-clip" | Auto failed; need Reference Point override | Editor's Guide pp. 569-575 |
| "My captions/subtitles have wrong technical terms" | Always proofread AI Transcription; use Search + Replace | Editor's Guide pp. 341-361 |
| "Project moved to new machine, all clips offline" | Use Change Source Folder, not Re-import | Editor's Guide pp. 336-340 |
| "Mac App Store version is missing features / can't reach drive" | Sandboxed install. Reinstall from blackmagicdesign.com | Beginner's Guide p. xv |
| "Free Resolve doesn't have Noise Reduction / Smart Reframe / AI Transcription" | These are Studio-only. Free has manual fallbacks | per-feature notes in each PDF |
| "Project crashes during render" | GPU auto-select, hardware decode bug, or out-of-memory | Editor's Guide pp. 597-617; Colorist Guide pp. 362-379 |
| "Fusion comp won't render in the timeline" | Resolution mismatch between comp and timeline, or missing input | Fusion VFX pp. 60-69 |
| "Background hum at exactly 60 Hz" | De-Hummer notch filter, not EQ | Fairlight Audio Post pp. 376-383 |

## Page-number convention

Page numbers in this wiki match the **PDF page numbers as printed in the book**, which are typically what the PDF reader displays as well. Front matter uses roman numerals (i, ii, xiv). Body pages use arabic (1, 2, 3...).

When a page reference like "pp. 246-310" appears, that is the chapter's printed page range, suitable for pasting into a PDF reader's go-to-page dialog.

## Author

Built by Jai Bhagat. More at chaiwithjai.com.
