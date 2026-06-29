from pathlib import Path

from kae.core.metadata import discover_audio_files
from kae.core.models import TrackMetadata


def test_track_metadata_json_roundtrip_marks_editable_fields() -> None:
    track = TrackMetadata(path=Path("song.mp3"), title="Old")

    track.apply_json_dict({"title": "New", "artist": "Kico", "album": "Pink"})

    assert track.title == "New"
    assert track.artist == "Kico"
    assert track.album == "Pink"
    assert track.dirty is True


def test_discover_audio_files_filters_supported_extensions(tmp_path: Path) -> None:
    audio = tmp_path / "a.mp3"
    ignored = tmp_path / "notes.txt"
    nested = tmp_path / "nested"
    nested.mkdir()
    flac = nested / "b.flac"
    audio.write_bytes(b"")
    ignored.write_text("nope")
    flac.write_bytes(b"")

    assert discover_audio_files([tmp_path]) == [audio, flac]
