from __future__ import annotations

from kae.paths import asset_path


def load_stylesheet(compact: bool = False) -> str:
    qss = asset_path("styles", "sakura.qss").read_text(encoding="utf-8")
    return qss.replace("/*DENSITY*/", "6px" if compact else "10px")
