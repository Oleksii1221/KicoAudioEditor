# -*- mode: python ; coding: utf-8 -*-

from pathlib import Path

project = Path(SPECPATH).resolve().parent
if project.name == "packaging":
    project = project.parent

a = Analysis(
    [str(project / "src" / "kae" / "app.py")],
    pathex=[str(project / "src")],
    binaries=[],
    datas=[(str(project / "src" / "kae" / "assets"), "kae/assets")],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name="KAE",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    icon=str(project / "src" / "kae" / "assets" / "icons" / "kae.ico"),
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name="KAE",
)
