#!/usr/bin/env bash
set -euo pipefail

VERSION="${KAE_VERSION:-0.1.0}"
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
APPDIR="$ROOT/dist/linux/KAE.AppDir"

rm -rf "$APPDIR"
mkdir -p "$APPDIR/usr/app" "$APPDIR/usr/bin" "$APPDIR/usr/share/applications" "$APPDIR/usr/share/icons/hicolor/256x256/apps"

python -m venv "$APPDIR/usr/venv"
"$APPDIR/usr/venv/bin/python" -m pip install --upgrade pip
"$APPDIR/usr/venv/bin/python" -m pip install "$ROOT"
cp -R "$ROOT/src" "$APPDIR/usr/app/src"
ln -s ../venv/bin/python "$APPDIR/usr/bin/python"
cp "$ROOT/packaging/linux/AppRun" "$APPDIR/AppRun"
chmod +x "$APPDIR/AppRun"
cp "$ROOT/packaging/linux/kae.desktop" "$APPDIR/kae.desktop"
cp "$ROOT/packaging/linux/kae.desktop" "$APPDIR/usr/share/applications/kae.desktop"
cp "$ROOT/src/kae/assets/images/kae_mascot.png" "$APPDIR/kae.png"
cp "$ROOT/src/kae/assets/images/kae_mascot.png" "$APPDIR/usr/share/icons/hicolor/256x256/apps/kae.png"

APPIMAGETOOL="${APPIMAGETOOL:-appimagetool}"
"$APPIMAGETOOL" "$APPDIR" "$ROOT/dist/KAE-${VERSION}-x86_64.AppImage"
