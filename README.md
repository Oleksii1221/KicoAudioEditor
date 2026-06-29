<p align="center">
  <img src="src/kae/assets/images/kae_mascot.png" alt="KAE mascot" width="180">
</p>

<h1 align="center">KAE</h1>

<p align="center">
  A native desktop audio metadata editor with a polished sakura-night interface, embedded artwork tools, batch editing, and professional release packaging.
</p>

<p align="center">
  <a href="LICENSE"><img alt="License: MIT" src="https://img.shields.io/badge/license-MIT-ff69b4"></a>
  <img alt="Python" src="https://img.shields.io/badge/python-3.11+-2b1524">
  <img alt="UI" src="https://img.shields.io/badge/UI-PySide6-ff8ac4">
  <img alt="Platform" src="https://img.shields.io/badge/platform-Windows%20%7C%20Linux-fc5ca8">
</p>

## Overview

KAE is a desktop-first audio tag editor for people who want a fast, focused way to clean up a music library without opening a browser, running a server, or fighting a generic utility window. It edits common metadata, embedded cover artwork, lyrics, comments, technical file details, and sidecar JSON metadata in a single native interface.

The product direction is simple: reliable audio metadata workflows, a distinctive pink anime visual identity, and release artifacts that feel like a real application.

## Core Capabilities

- Edit titles, artists, albums, album artists, genres, years, track/disc numbers, composers, comments, lyrics, and BPM.
- Replace, preview, export, and remove embedded cover artwork.
- Import and export metadata as JSON for backups or external workflows.
- Batch-apply shared album, album artist, genre, and year values to selected tracks.
- Open individual files or scan entire folders recursively.
- Search and filter the loaded library.
- Save current or selected tracks with keyboard shortcuts.
- Persist recent files and application preferences.
- Switch between Sakura Candy and Night Sakura themes.
- Use Ukrainian, English, Japanese, Italian, and Spanish UI languages.
- Run as a native PySide6 desktop application with custom title bar controls.

## Supported Audio Formats

KAE uses Mutagen for metadata operations.

| Format | Metadata | Artwork |
| --- | --- | --- |
| MP3 | ID3 | Embedded APIC |
| FLAC | Vorbis comments | Embedded FLAC pictures |
| M4A / AAC | MP4 tags | Embedded cover atom |
| OGG / OPUS | Vorbis comments | Basic tag workflow |
| WAV / AIFF | Best-effort tag support | Depends on container support |

## Installation

Release builds are produced by GitHub Actions.

- Windows: `KAE-Setup-<version>.exe` installs KAE with Start Menu and optional desktop shortcuts.
- Linux universal: `KAE-<version>-x86_64.AppImage`.
- Debian / Ubuntu: `kae_<version>_amd64.deb`.
- Fedora / RHEL: `kae-<version>-1.x86_64.rpm`.
- Arch: use the provided `packaging/linux/PKGBUILD` template.

For local development:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -e ".[dev]"
python -m kae
```

## Keyboard Shortcuts

| Shortcut | Action |
| --- | --- |
| `Ctrl+O` | Open audio files |
| `Ctrl+Shift+O` | Open folder |
| `Ctrl+S` | Save current file |
| `Ctrl+Shift+S` | Save selected files |
| `Ctrl+I` | Import JSON metadata |
| `Ctrl+E` | Export JSON metadata |
| `Ctrl+Shift+C` | Change cover |
| `Ctrl+F` | Search library |
| `Ctrl+,` | Settings |

## Engineering Notes

KAE is split into testable core services and a native UI shell:

- `src/kae/core`: metadata, settings, language strings, and domain models.
- `src/kae/ui`: PySide6 windows, dialogs, title bar, and theme loading.
- `src/kae/assets`: mascot, icon, and QSS theme assets.
- `packaging`: PyInstaller, Windows installer, and Linux packaging assets.
- `site`: static product site deployed to GitHub Pages.

Development happens on `dev`. `master` is reserved for release-ready versions after explicit approval.

```powershell
git checkout dev
pytest
ruff check .
pyinstaller packaging/kae.spec --noconfirm
```

## Release Pipeline

The release workflow builds and uploads:

- Windows portable bundle
- Windows setup executable
- Linux AppImage
- Debian package
- RPM package
- Python source distribution and wheel

The Pages workflow deploys the static product site from `site/`.

## License

KAE is released under the [MIT License](LICENSE).
