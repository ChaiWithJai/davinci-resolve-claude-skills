# DaVinci Resolve Claude Skills

Claude/Codex skills for DaVinci Resolve 20. Built for creators, operators, developers, and educators who need publishable video, not another pile of editing notes.

The repo is organized around real jobs to be done: cut the story, repair the audio, keep the speaker in frame, add captions people can read on a phone, source useful B-roll, and hand the result back as an editable Resolve timeline.

If you found this from Twitter: this is an open skill library for teaching AI agents professional post-production workflows with evidence, not vibes.

If you came from Jai's content: this is the operating system behind turning raw workshop footage into Instagram Reels, Shorts, and YouTube videos that explain the offer clearly and feel worth watching.

## What is in the box

Eleven skills, each solving a specific job:

| Skill | Job to be done |
|---|---|
| `davinci-resolve-setup` | Install Resolve correctly, set up media drives, configure backups before your first edit |
| `davinci-resolve-devrel-project-template` | Set up a reusable project — bins, timeline, render presets, color preset — once, reuse forever |
| `davinci-resolve-cut-screen-recording` | Turn a 60-minute screen recording into an 8-minute tight demo (kills ums, dead air, mistakes) |
| `davinci-resolve-color-grade-webcam` | Make webcam or interview footage look broadcast-quality (skin tones, exposure, balance) |
| `davinci-resolve-audio-cleanup-podcast` | Clean podcast/interview audio — denoise, de-hum, dialogue level, music duck under voice |
| `davinci-resolve-titles-and-lower-thirds` | Branded titles and animated lower-thirds without leaving Resolve |
| `davinci-resolve-export-multi-platform` | Export the same edit for YouTube (16:9), LinkedIn (square), Shorts (9:16), plus automate it |
| `davinci-resolve-troubleshooting` | Diagnose the 5 most common "why is X broken" moments |
| `davinci-resolve-computer-use-training` | Work through Blackmagic lesson homework with Computer Use, record evidence, and turn UI lessons into better production skills |
| `davinci-resolve-social-editor` | Build speaker-led social edits with semantic cuts, B-roll, captions, audio checks, and Resolve handoff |
| `social-video-folder-autocutter` | Turn a hard-drive folder into repeatable Instagram/YouTube cut briefs, B-roll plans, and eval artifacts |

See `docs/jtbd-map.md` for the mapping from jobs to skills.

## The two-layer reference model

Each skill points at two layers of reference material:

1. **Deep wikis (`docs/wiki/`)** — working summaries the agent reads as context. One per Blackmagic PDF, plus a master index. These cover chapter structure, key concepts, workflows, shortcuts, and common pitfalls. Per-chapter page ranges are listed at the end of each notes block.

2. **PDF page ranges** — the ground truth. Blackmagic publishes six free training PDFs for Resolve 20, totaling around 1,800 pages. Download them from Blackmagic and keep them locally; skills cite specific page ranges as a reset mechanism.

The flow:

- Agent reads the wiki as working memory before answering.
- If the user pushes back, the agent reads the cited PDF page range to reset its mental model — then re-answers.
- The agent does not invent technique; it summarizes what the PDFs say.

This is the core design idea. Wikis are fast context. PDFs are the truth layer when context drifts.

## Installation

### Option 1: Copy each skill directory to `~/.claude/skills/`

```bash
git clone https://github.com/ChaiWithJai/davinci-resolve-claude-skills.git
cp -R davinci-resolve-claude-skills/skills/* ~/.claude/skills/
```

Claude Code picks up skills in `~/.claude/skills/` automatically.

### Option 2: Symlink the whole skills directory

```bash
git clone https://github.com/ChaiWithJai/davinci-resolve-claude-skills.git
cd davinci-resolve-claude-skills
for skill in skills/*/; do
  name=$(basename "$skill")
  ln -s "$(pwd)/$skill" "$HOME/.claude/skills/$name"
done
```

Symlinking lets you `git pull` updates without re-copying.

### Option 3: Project-local skills

If you want the skills available only inside one repo, put them in `<repo>/.claude/skills/` instead of `~/.claude/skills/`.

## How to use

The skills auto-trigger when their description matches what you are asking for. For example:

- "My screen recording is too long, help me cut it down" → triggers `davinci-resolve-cut-screen-recording`
- "How do I make my webcam look better" → triggers `davinci-resolve-color-grade-webcam`
- "The music in my podcast is drowning out the host" → triggers `davinci-resolve-audio-cleanup-podcast`
- "Export my edit for LinkedIn and YouTube" → triggers `davinci-resolve-export-multi-platform`
- "Make this folder into an Instagram Reel and YouTube cut" → triggers `social-video-folder-autocutter`
- "Fix the jump cuts, audio, captions, B-roll, and Resolve handoff" → triggers `davinci-resolve-social-editor`

You can also reference a skill explicitly: "use the davinci-resolve-color-grade-webcam skill on this footage."

## Production Standard

The current bar is not "a video exists." The bar is:

- the story is coherent enough for a stranger to understand,
- warm traffic immediately knows why the workshop matters,
- dialogue is clean and dominant on phone speakers,
- captions are burned in, timed to actual speech, and proofread,
- B-roll proves claims or covers cuts instead of decorating the frame,
- the color grade is bright, vibrant, and skin-tone safe,
- the Resolve artifact remains layered enough for a human editor to take over.

The strongest loop we learned is simple: when a cut is close, preserve the liked picture edit and fix the exact defect. For the latest Chai With Jai pass, that meant a caption-only finishing pass from word-level speech timing, followed by phone-safe still and loudness verification.

## Python automation

Several skills include Python scripts that drive Resolve through its external scripting API or prepare verified edit artifacts:

- `skills/davinci-resolve-cut-screen-recording/scripts/auto_silence_cut.py`
- `skills/davinci-resolve-export-multi-platform/scripts/multi_platform_render.py`
- `skills/davinci-resolve-computer-use-training/scripts/`
- `skills/davinci-resolve-social-editor/scripts/`
- `skills/social-video-folder-autocutter/scripts/`

To run these scripts you must enable external scripting in Resolve:

1. DaVinci Resolve > Preferences > System > General
2. Set External scripting using to **Local** (or **Network** if running remotely)
3. Click Save

Then either:

- Run from inside Resolve: Workspace > Console > Py3
- Or run from your shell:

  ```bash
  # macOS
  export RESOLVE_SCRIPT_API="/Library/Application Support/Blackmagic Design/DaVinci Resolve/Developer/Scripting"
  export RESOLVE_SCRIPT_LIB="/Applications/DaVinci Resolve/DaVinci Resolve.app/Contents/Libraries/Fusion/fusionscript.so"
  export PYTHONPATH="$PYTHONPATH:$RESOLVE_SCRIPT_API/Modules/"
  python3 skills/davinci-resolve-cut-screen-recording/scripts/auto_silence_cut.py
  ```

Resolve must be open with a project loaded. The scripts attach to the running Resolve instance via `DaVinciResolveScript.scriptapp("Resolve")`.

## Source documentation

The wikis under `docs/wiki/` summarize the six Blackmagic Design DaVinci Resolve 20 training PDFs:

- *The Beginner's Guide to DaVinci Resolve 20* (Roberts, Hall — 2025)
- *The Editor's Guide to DaVinci Resolve 20* (Roberts — 2025)
- *The Colorist Guide to DaVinci Resolve 20* (Fissoun — 2025)
- *The Fairlight Audio Guide to DaVinci Resolve 20* (Plummer — 2025)
- *The Visual Effects Guide to DaVinci Resolve 20* (Allen, Gallardo, Scoppettuolo — 2025)
- *Advanced Visual Effects in DaVinci Resolve 20* (Allen, Scoppettuolo — 2025)

Download the PDFs free from `https://www.blackmagicdesign.com/products/davinciresolve/training`.

The Python scripting API is documented in `DaVinci Resolve/Developer/Scripting/README.txt` shipped with the application installer.

## Contributing

Open issues and PRs welcome. Please:

- Cite specific PDF page numbers for any new technical claims
- Keep `description:` frontmatter focused on triggering conditions, not workflow summaries
- Add a `Verification` section to every new skill
- If you add a Python script, mark untested API calls clearly

## License

MIT. See `LICENSE`.

## About

Built by Jai Bhagat. More at chaiwithjai.com.
