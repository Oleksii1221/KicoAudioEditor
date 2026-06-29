# KAE

KAE is a native desktop audio metadata editor with a polished pink anime visual style. It edits track titles, artists, albums, genres, years, comments, lyrics, track numbers, and embedded cover artwork without any web server or browser wrapper.

## Features

- Native PySide6 desktop interface with a custom title bar.
- Edit metadata for MP3, FLAC, OGG, M4A, AAC, WAV, and AIFF where tags are supported.
- Replace, export, remove, and preview embedded cover artwork.
- Import and export sidecar JSON metadata.
- Batch-apply album, album artist, genre, and year to selected files.
- Recent files, autosave preference, language selection, theme mode, and density settings.
- Keyboard shortcuts for opening files/folders, saving, artwork actions, settings, and search.
- MIT licensed.

## Quick Start

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

## Development Workflow

Development happens on `dev`. `master` is reserved for release-ready versions only after explicit release approval.

```powershell
git checkout dev
pytest
ruff check .
```

## Packaging

The project is ready for PyInstaller packaging:

```powershell
pyinstaller packaging/kae.spec
```

The generated Windows executable uses the project icon and bundles the app assets.
