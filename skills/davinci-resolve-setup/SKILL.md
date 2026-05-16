---
name: davinci-resolve-setup
description: Use when a user is installing DaVinci Resolve for the first time, switching machines, configuring a media drive for video editing, or asking about backup/proxy settings. Triggering symptoms include phrases like "just installed Resolve", "set up DaVinci Resolve", "drop frames during playback", "where should my media live", "how do I configure backups", or any DaVinci Resolve installation/preferences question.
---

# DaVinci Resolve — first-time setup for content creators

## Overview

One-time configuration for DaVinci Resolve 20 so it does not bite you later. Three things matter: the install source, the media drive, and the backup settings. Everything else can be configured per-project.

## When to use

Symptoms:
- Just downloaded DaVinci Resolve and want to know what to configure first
- Bought a new external drive and need to point Resolve at it
- Playback drops frames or shows a red GPU indicator
- Want to enable automatic project backups before doing real work

When NOT to use:
- Resolve is already running fine and you have an existing project — skip to `davinci-resolve-devrel-project-template`.
- You only need to enable Python scripting — that is a one-liner in Preferences > System > General (set External scripting to Local).

## Quick reference

| Decision | Right answer | Why |
|---|---|---|
| Install source | blackmagicdesign.com, NOT Mac App Store | App Store version sandboxes the file system |
| Free vs Studio | Free is fine for 99% of DevRel | Studio adds noise reduction, AI Smart Reframe, neural engine features |
| Media drive | Fastest external SSD you have | Read >500 MB/s minimum for 4K |
| Backup interval | 10 minutes / 24 hours / 180 days | Survives editor crash, daily mistake, six-month regret |
| Render cache location | Internal SSD, not media drive | Reduces read/write contention |

## Steps

### 1. Install from blackmagicdesign.com (not the App Store)

1. Open a browser, go to `https://www.blackmagicdesign.com/products/davinciresolve`.
2. Click Download.
3. Choose your OS (macOS, Windows, Linux). On macOS, do **not** install via the Mac App Store — it sandboxes the filesystem and breaks several workflows like the Blackmagic Proxy Generator.
4. Run the installer. Restart if prompted.

### 2. Test your media drive speed before you commit to it

1. Download **Blackmagic Disk Speed Test** (free, separate app). On macOS it is on the App Store. On Windows it is included with the Desktop Video installer.
2. Run it pointed at the drive you plan to use for media.
3. Look at the "Will It Work?" table. Confirm green checkmarks for the codecs and resolutions you actually shoot (typically H.265 at 1080p/4K, or Blackmagic RAW if you shoot on a Blackmagic camera).
4. If the drive cannot sustain reads above ~500 MB/s for your codec at your resolution, you will get dropped-frame playback. Buy a faster drive or generate proxies (covered in `davinci-resolve-devrel-project-template`).

### 3. First launch — set the media folders

1. Launch DaVinci Resolve. Skip the welcome screen.
2. Click **DaVinci Resolve > Preferences** (macOS) or **DaVinci Resolve > Preferences** (Windows).
3. Switch to the **System** tab at the top.
4. Click **Media Storage** in the left sidebar.
5. Click the **+** button and add your media drive. This tells Resolve where to look for media by default.
6. Click **Save**.

### 4. Enable Live Save and project backups

This is the single most important step. Resolve does NOT save by default, and you will lose work.

1. **DaVinci Resolve > Preferences > User > Project Save and Load**.
2. Confirm **Live Save** is checked. This auto-saves on every change.
3. Check **Project backups**.
4. Set the intervals:
   - Backups every **10** minutes (6 backups per hour)
   - Hourly backups for the past **24** hours
   - Daily backups for the past **180** days (six months)
5. Click **Browse** for **Backup location** and pick a folder on your internal SSD (not the media drive — you want backups in a different place than your media in case the media drive dies).
6. Check **Timeline backups** too (this backs up `.drt` files which are smaller and recoverable independently).
7. Click **Save**.

These intervals are loosely based on the Colorist Guide's project backup recommendations.

### 5. Set the working folders for the project media cache

1. **DaVinci Resolve > Project Settings** (or **File > Project Settings**, or press Shift-9).
2. **Master Settings** > scroll to **Working Folders**.
3. Set:
   - **Cache files location** — internal SSD (fast)
   - **Proxy generation location** — internal SSD or media drive (your call)
   - **Project media location** — typically same as Cache files, on your internal SSD
4. Save.

### 6. Enable external scripting (optional, but you will want it later)

1. **DaVinci Resolve > Preferences > System > General**.
2. Set **External scripting using** to **Local**.
3. Save. Restart Resolve.

This lets you run Python scripts against Resolve from your terminal — used by `davinci-resolve-cut-screen-recording` and `davinci-resolve-export-multi-platform`.

## Common mistakes

- **Installed via Mac App Store** -> uninstall and reinstall from blackmagicdesign.com. The App Store version cannot reach external drives reliably and the Blackmagic Proxy Generator is missing.
- **Media drive is USB 2.0** -> you will not be able to play back even 1080p H.264 reliably. Move to USB 3 / Thunderbolt / NVMe.
- **Backup location set to the media drive** -> backups die with the media drive. Use the internal SSD.
- **Live Save unchecked** -> you will lose hours of work the first time Resolve crashes.

## Verification

You succeeded if all of the following are true:

1. Resolve launches without complaining about a missing license or installer signature.
2. You can drag a video file from your media drive into the Media Pool without Resolve marking it offline.
3. The frame-rate indicator at the top of the source viewer stays **green** during playback (not red).
4. The path under DaVinci Resolve > Preferences > User > Project Save and Load > Backup location shows a folder on your internal SSD.
5. You can find `.drp` files (project backups) appearing in the backup folder after 10 minutes of editing.

## Transfer

Now try this: import a clip from a *different* drive than the one you configured. Resolve should still find it (since the file lives at an absolute path). Then disconnect that drive and reopen the project — note how Resolve flags those clips as offline and offers **Relink** in the Media Pool. That is the workflow you will use the first time a colleague hands you a project file without media.

## Working reference

- `docs/wiki/beginners-guide.md` (install, system requirements, Quick Setup)
- `docs/wiki/colorist-guide.md#front-matter--project-backups-pp-6-7` (Live Save and project backups, primary)
- `docs/wiki/editors-guide.md#lesson-6--ai-workflows-pp-323-387` (Disk Speed Test, proxies)
- `docs/wiki/master.md#reset-matrix--when-the-user-pushes-back-read-this` (cross-cutting symptom map)

## When the agent's work isn't matching expectations (context-rot reset)

If the user pushes back on a recommendation (install path, backup interval, drive speed, scripting toggle), read these PDF page ranges to reset:

- `DaVinci-Resolve-20_Beginners-Guide.pdf` pp. xiv-xxiv (Getting Started, system requirements, download instructions)
- `DaVinci-Resolve-20-Editors-Guide.pdf` pp. xii-xxiv (Getting Started — Editor's perspective on initial setup)
- `DaVinci-Resolve-20-Editors-Guide.pdf` pp. 324-337 (Generating Proxy Files; Blackmagic Disk Speed Test; drive speed considerations)
- `DaVinci-Resolve-20-Colorist-Guide.pdf` pp. 6-7 (Setting Up Project Backups, Live Save settings)
