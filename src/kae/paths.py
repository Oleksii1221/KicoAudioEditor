from __future__ import annotations

from importlib.resources import files
from pathlib import Path


def asset_path(*parts: str) -> Path:
    return Path(str(files("kae").joinpath("assets", *parts)))
