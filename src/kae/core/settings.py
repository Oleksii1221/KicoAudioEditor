from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from pathlib import Path

APP_DIR = Path.home() / "AppData" / "Roaming" / "KAE"
SETTINGS_PATH = APP_DIR / "settings.json"


@dataclass(slots=True)
class AppSettings:
    language: str = "uk"
    theme: str = "sakura"
    autosave_on_file_switch: bool = False
    confirm_before_overwrite: bool = True
    remember_recent_files: bool = True
    compact_mode: bool = False
    recent_files: list[str] = field(default_factory=list)

    @classmethod
    def load(cls) -> AppSettings:
        if not SETTINGS_PATH.exists():
            return cls()
        data = json.loads(SETTINGS_PATH.read_text(encoding="utf-8"))
        return cls(**{key: data[key] for key in cls.__dataclass_fields__ if key in data})

    def save(self) -> None:
        APP_DIR.mkdir(parents=True, exist_ok=True)
        SETTINGS_PATH.write_text(json.dumps(asdict(self), indent=2), encoding="utf-8")

    def remember(self, paths: list[Path]) -> None:
        if not self.remember_recent_files:
            return
        existing = [str(path) for path in paths] + self.recent_files
        deduped: list[str] = []
        for item in existing:
            if item not in deduped:
                deduped.append(item)
        self.recent_files = deduped[:24]
        self.save()
