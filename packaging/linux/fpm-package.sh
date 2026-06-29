#!/usr/bin/env bash
set -euo pipefail

VERSION="${KAE_VERSION:-0.1.0}"
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
STAGE="$ROOT/dist/linux/package-root"

rm -rf "$STAGE"
mkdir -p "$STAGE/opt/kae" "$STAGE/usr/bin" "$STAGE/usr/share/applications" "$STAGE/usr/share/icons/hicolor/256x256/apps"

python -m venv "$STAGE/opt/kae/venv"
"$STAGE/opt/kae/venv/bin/python" -m pip install --upgrade pip
"$STAGE/opt/kae/venv/bin/python" -m pip install "$ROOT"
cp -R "$ROOT/src" "$STAGE/opt/kae/src"
cat > "$STAGE/usr/bin/kae" <<'EOF'
#!/usr/bin/env bash
export PYTHONPATH="/opt/kae/src:${PYTHONPATH:-}"
exec /opt/kae/venv/bin/python -m kae "$@"
EOF
chmod +x "$STAGE/usr/bin/kae"
cp "$ROOT/packaging/linux/kae.desktop" "$STAGE/usr/share/applications/kae.desktop"
cp "$ROOT/src/kae/assets/images/kae_mascot.png" "$STAGE/usr/share/icons/hicolor/256x256/apps/kae.png"

mkdir -p "$ROOT/dist/packages"
fpm -s dir -t deb -n kae -v "$VERSION" --license MIT --description "KAE audio metadata editor" -C "$STAGE" -p "$ROOT/dist/packages/kae_${VERSION}_amd64.deb" .
fpm -s dir -t rpm -n kae -v "$VERSION" --license MIT --description "KAE audio metadata editor" -C "$STAGE" -p "$ROOT/dist/packages/kae-${VERSION}-1.x86_64.rpm" .
