from __future__ import annotations

from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any

SUPPORTED_AUDIO_EXTENSIONS = {
    ".mp3",
    ".flac",
    ".ogg",
    ".oga",
    ".opus",
    ".m4a",
    ".aac",
    ".wav",
    ".aiff",
    ".aif",
}


@dataclass(slots=True)
class TrackMetadata:
    path: Path
    title: str = ""
    artist: str = ""
    album: str = ""
    album_artist: str = ""
    genre: str = ""
    year: str = ""
    track_number: str = ""
    disc_number: str = ""
    composer: str = ""
    comment: str = ""
    lyrics: str = ""
    bpm: str = ""
    artwork_mime: str = ""
    artwork_bytes: bytes = b""
    duration_seconds: float = 0.0
    bitrate: int = 0
    sample_rate: int = 0
    channels: int = 0
    dirty: bool = False
    warnings: list[str] = field(default_factory=list)

    @property
    def filename(self) -> str:
        return self.path.name

    @property
    def extension(self) -> str:
        return self.path.suffix.lower()

    def to_json_dict(self) -> dict[str, Any]:
        data = asdict(self)
        data["path"] = str(self.path)
        data.pop("artwork_bytes", None)
        data.pop("dirty", None)
        data.pop("warnings", None)
        return data

    def apply_json_dict(self, data: dict[str, Any]) -> None:
        editable = {
            "title",
            "artist",
            "album",
            "album_artist",
            "genre",
            "year",
            "track_number",
            "disc_number",
            "composer",
            "comment",
            "lyrics",
            "bpm",
        }
        for key in editable:
            if key in data:
                setattr(self, key, str(data.get(key) or ""))
        self.dirty = True
