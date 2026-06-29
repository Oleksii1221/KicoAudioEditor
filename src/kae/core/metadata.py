from __future__ import annotations

import json
from io import BytesIO
from pathlib import Path
from typing import Any

from mutagen import File
from mutagen.flac import FLAC, Picture
from mutagen.id3 import (
    APIC,
    COMM,
    ID3,
    TALB,
    TBPM,
    TCOM,
    TCON,
    TDRC,
    TIT2,
    TPE1,
    TPE2,
    TPOS,
    TRCK,
    USLT,
)
from mutagen.mp4 import MP4, MP4Cover
from mutagen.oggvorbis import OggVorbis
from PIL import Image

from kae.core.models import SUPPORTED_AUDIO_EXTENSIONS, TrackMetadata

TEXT_TAGS: dict[str, tuple[str, ...]] = {
    "title": ("title", "\xa9nam"),
    "artist": ("artist", "\xa9ART"),
    "album": ("album", "\xa9alb"),
    "album_artist": ("albumartist", "aART"),
    "genre": ("genre", "\xa9gen"),
    "year": ("date", "year", "\xa9day"),
    "track_number": ("tracknumber", "trkn"),
    "disc_number": ("discnumber", "disk"),
    "composer": ("composer", "\xa9wrt"),
    "comment": ("comment", "\xa9cmt"),
    "lyrics": ("lyrics", "\xa9lyr"),
    "bpm": ("bpm", "tmpo"),
}


class MetadataError(RuntimeError):
    pass


def discover_audio_files(paths: list[Path]) -> list[Path]:
    results: list[Path] = []
    for path in paths:
        if path.is_dir():
            results.extend(
                child
                for child in path.rglob("*")
                if child.is_file() and child.suffix.lower() in SUPPORTED_AUDIO_EXTENSIONS
            )
        elif path.is_file() and path.suffix.lower() in SUPPORTED_AUDIO_EXTENSIONS:
            results.append(path)
    return sorted(set(results), key=lambda item: str(item).lower())


def read_metadata(path: Path) -> TrackMetadata:
    audio = File(path, easy=False)
    if audio is None:
        raise MetadataError(f"Unsupported or unreadable audio file: {path}")

    easy = File(path, easy=True)
    track = TrackMetadata(path=path)
    for field, keys in TEXT_TAGS.items():
        value = _first_text_value(easy, audio, keys)
        setattr(track, field, value)

    info = getattr(audio, "info", None)
    if info:
        track.duration_seconds = float(getattr(info, "length", 0) or 0)
        track.bitrate = int(getattr(info, "bitrate", 0) or 0)
        track.sample_rate = int(getattr(info, "sample_rate", 0) or 0)
        track.channels = int(getattr(info, "channels", 0) or 0)

    artwork = extract_artwork(path)
    if artwork:
        track.artwork_mime, track.artwork_bytes = artwork
    return track


def write_metadata(track: TrackMetadata) -> None:
    suffix = track.path.suffix.lower()
    if suffix == ".mp3":
        _write_mp3(track)
    elif suffix == ".flac":
        _write_flac(track)
    elif suffix in {".m4a", ".aac"}:
        _write_mp4(track)
    else:
        _write_easy(track)
    track.dirty = False


def extract_artwork(path: Path) -> tuple[str, bytes] | None:
    suffix = path.suffix.lower()
    audio = File(path, easy=False)
    if audio is None:
        return None
    if suffix == ".mp3":
        tags = ID3(path)
        for frame in tags.values():
            if isinstance(frame, APIC):
                return frame.mime, bytes(frame.data)
    if suffix == ".flac" and isinstance(audio, FLAC) and audio.pictures:
        picture = audio.pictures[0]
        return picture.mime, bytes(picture.data)
    if suffix in {".m4a", ".aac"} and isinstance(audio, MP4):
        covers = audio.tags.get("covr") if audio.tags else None
        if covers:
            cover = covers[0]
            mime = "image/png" if cover.imageformat == MP4Cover.FORMAT_PNG else "image/jpeg"
            return mime, bytes(cover)
    return None


def replace_artwork(track: TrackMetadata, image_path: Path) -> None:
    track.artwork_bytes, track.artwork_mime = _normalize_cover_image(image_path)
    track.dirty = True


def remove_artwork(track: TrackMetadata) -> None:
    track.artwork_bytes = b""
    track.artwork_mime = ""
    track.dirty = True


def export_metadata_json(track: TrackMetadata, destination: Path) -> None:
    destination.write_text(
        json.dumps(track.to_json_dict(), ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


def import_metadata_json(track: TrackMetadata, source: Path) -> None:
    track.apply_json_dict(json.loads(source.read_text(encoding="utf-8")))


def _first_text_value(easy: Any, audio: Any, keys: tuple[str, ...]) -> str:
    for key in keys:
        source = easy.tags if easy and easy.tags and key in easy.tags else None
        if source:
            return _normalize_value(source.get(key))
        if audio.tags and key in audio.tags:
            return _normalize_value(audio.tags.get(key))
    return ""


def _normalize_value(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, list | tuple):
        if not value:
            return ""
        if isinstance(value[0], tuple):
            return "/".join(str(part) for part in value[0] if part)
        return str(value[0])
    text = getattr(value, "text", None)
    if isinstance(text, list) and text:
        return str(text[0])
    return str(value)


def _write_easy(track: TrackMetadata) -> None:
    audio = File(track.path, easy=True)
    if audio is None:
        raise MetadataError(f"Unsupported audio file: {track.path}")
    if audio.tags is None:
        audio.add_tags()
    mapping = {
        "title": track.title,
        "artist": track.artist,
        "album": track.album,
        "albumartist": track.album_artist,
        "genre": track.genre,
        "date": track.year,
        "tracknumber": track.track_number,
        "discnumber": track.disc_number,
        "composer": track.composer,
        "comment": track.comment,
        "lyrics": track.lyrics,
        "bpm": track.bpm,
    }
    for key, value in mapping.items():
        if value:
            audio[key] = [value]
        elif key in audio:
            del audio[key]
    audio.save()


def _write_mp3(track: TrackMetadata) -> None:
    tags = ID3(track.path) if track.path.exists() else ID3()
    frame_ids = [
        "TIT2",
        "TPE1",
        "TALB",
        "TPE2",
        "TCON",
        "TDRC",
        "TDRL",
        "TRCK",
        "TPOS",
        "TCOM",
        "COMM",
        "USLT",
        "TBPM",
    ]
    for frame_id in frame_ids:
        tags.delall(frame_id)
    _add_text(tags, TIT2, track.title)
    _add_text(tags, TPE1, track.artist)
    _add_text(tags, TALB, track.album)
    _add_text(tags, TPE2, track.album_artist)
    _add_text(tags, TCON, track.genre)
    _add_text(tags, TDRC, track.year)
    _add_text(tags, TRCK, track.track_number)
    _add_text(tags, TPOS, track.disc_number)
    _add_text(tags, TCOM, track.composer)
    _add_text(tags, TBPM, track.bpm)
    if track.comment:
        tags.add(COMM(encoding=3, lang="eng", desc="", text=track.comment))
    if track.lyrics:
        tags.add(USLT(encoding=3, lang="eng", desc="", text=track.lyrics))
    tags.delall("APIC")
    if track.artwork_bytes:
        tags.add(
            APIC(
                encoding=3,
                mime=track.artwork_mime or "image/jpeg",
                type=3,
                desc="Cover",
                data=track.artwork_bytes,
            )
        )
    tags.save(track.path)


def _write_flac(track: TrackMetadata) -> None:
    audio = FLAC(track.path)
    _set_vorbis(audio, track)
    audio.clear_pictures()
    if track.artwork_bytes:
        picture = Picture()
        picture.type = 3
        picture.mime = track.artwork_mime or "image/jpeg"
        picture.desc = "Cover"
        picture.data = track.artwork_bytes
        audio.add_picture(picture)
    audio.save()


def _write_mp4(track: TrackMetadata) -> None:
    audio = MP4(track.path)
    if audio.tags is None:
        audio.add_tags()
    values: dict[str, Any] = {
        "\xa9nam": track.title,
        "\xa9ART": track.artist,
        "\xa9alb": track.album,
        "aART": track.album_artist,
        "\xa9gen": track.genre,
        "\xa9day": track.year,
        "\xa9wrt": track.composer,
        "\xa9cmt": track.comment,
        "\xa9lyr": track.lyrics,
    }
    for key, value in values.items():
        if value:
            audio.tags[key] = [value]
        else:
            audio.tags.pop(key, None)
    _set_mp4_pair(audio, "trkn", track.track_number)
    _set_mp4_pair(audio, "disk", track.disc_number)
    if track.bpm:
        audio.tags["tmpo"] = [int(track.bpm)] if track.bpm.isdigit() else [0]
    else:
        audio.tags.pop("tmpo", None)
    if track.artwork_bytes:
        fmt = MP4Cover.FORMAT_PNG if track.artwork_mime == "image/png" else MP4Cover.FORMAT_JPEG
        audio.tags["covr"] = [MP4Cover(track.artwork_bytes, imageformat=fmt)]
    else:
        audio.tags.pop("covr", None)
    audio.save()


def _set_vorbis(audio: OggVorbis | FLAC, track: TrackMetadata) -> None:
    mapping = {
        "title": track.title,
        "artist": track.artist,
        "album": track.album,
        "albumartist": track.album_artist,
        "genre": track.genre,
        "date": track.year,
        "tracknumber": track.track_number,
        "discnumber": track.disc_number,
        "composer": track.composer,
        "comment": track.comment,
        "lyrics": track.lyrics,
        "bpm": track.bpm,
    }
    for key, value in mapping.items():
        if value:
            audio[key] = value
        elif key in audio:
            del audio[key]


def _add_text(tags: ID3, frame_type: type, value: str) -> None:
    if value:
        tags.add(frame_type(encoding=3, text=value))


def _set_mp4_pair(audio: MP4, key: str, value: str) -> None:
    if not value:
        audio.tags.pop(key, None)
        return
    first = value.split("/", maxsplit=1)[0]
    audio.tags[key] = [(int(first), 0)] if first.isdigit() else [(0, 0)]


def _mime_from_image_path(path: Path) -> str:
    return "image/png" if path.suffix.lower() == ".png" else "image/jpeg"


def _normalize_cover_image(path: Path) -> tuple[bytes, str]:
    with Image.open(path) as image:
        if image.mode not in {"RGB", "RGBA"}:
            image = image.convert("RGBA")
        buffer = BytesIO()
        image.save(buffer, format="PNG")
        return buffer.getvalue(), "image/png"
