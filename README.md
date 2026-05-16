# DaVinci Resolve Claude Skills

Claude Code skills for DaVinci Resolve 20. Built for developers, content creators, and anyone shipping demos, tutorials, talks, or podcasts.

These skills target real jobs to be done — not "click this menu." Each one solves a recognizable problem like "cut a 60-minute screen recording into a tight 8-minute demo" or "make webcam footage look broadcast-quality."

## What is in the box

Eight skills, each solving a specific job:

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

You can also reference a skill explicitly: "use the davinci-resolve-color-grade-webcam skill on this footage."

## Python automation

Three skills include Python scripts that drive Resolve through its external scripting API:

- `skills/davinci-resolve-cut-screen-recording/scripts/auto_silence_cut.py`
- `skills/davinci-resolve-export-multi-platform/scripts/multi_platform_render.py`
- `skills/davinci-resolve-troubleshooting/` (diagnostic snippets)

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
