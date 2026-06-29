from __future__ import annotations

from pathlib import Path

from PySide6.QtCore import QByteArray, Qt
from PySide6.QtGui import QAction, QIcon, QKeySequence, QPixmap
from PySide6.QtWidgets import (
    QApplication,
    QFileDialog,
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QHeaderView,
    QLabel,
    QLineEdit,
    QListWidget,
    QListWidgetItem,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QSplitter,
    QTableWidget,
    QTableWidgetItem,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

from kae.core.i18n import t
from kae.core.metadata import (
    discover_audio_files,
    export_metadata_json,
    import_metadata_json,
    read_metadata,
    remove_artwork,
    replace_artwork,
    write_metadata,
)
from kae.core.models import TrackMetadata
from kae.core.settings import AppSettings
from kae.paths import asset_path
from kae.ui.settings_dialog import SettingsDialog
from kae.ui.theme import load_stylesheet
from kae.ui.title_bar import TitleBar


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.settings = AppSettings.load()
        self.tracks: list[TrackMetadata] = []
        self.current_index = -1
        self.fields: dict[str, QLineEdit | QTextEdit] = {}
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Window)
        self.setWindowTitle("KAE")
        self.resize(1240, 790)
        self.setWindowIcon(QIcon(str(asset_path("icons", "kae.ico"))))

        root = QWidget()
        root_layout = QVBoxLayout(root)
        root_layout.setContentsMargins(0, 0, 0, 0)
        root_layout.setSpacing(0)
        root_layout.addWidget(TitleBar(self))
        root_layout.addWidget(self._build_body(), 1)
        self.setCentralWidget(root)
        self._create_actions()
        self._apply_theme()
        self._load_recent()

    def _build_body(self) -> QWidget:
        body = QWidget()
        body.setObjectName("AppBody")
        layout = QVBoxLayout(body)
        layout.setContentsMargins(16, 12, 16, 16)

        toolbar = QHBoxLayout()
        for label, handler in [
            ("open_files", self.open_files),
            ("open_folder", self.open_folder),
            ("save", self.save_current),
            ("save_all", self.save_selected),
            ("settings", self.open_settings),
        ]:
            button = QPushButton(t(self.settings.language, label))
            button.clicked.connect(handler)
            toolbar.addWidget(button)
        self.search = QLineEdit()
        self.search.setPlaceholderText(t(self.settings.language, "search"))
        self.search.textChanged.connect(self._filter_tracks)
        toolbar.addStretch()
        toolbar.addWidget(self.search, 2)
        layout.addLayout(toolbar)

        splitter = QSplitter()
        splitter.setObjectName("MainSplitter")
        splitter.addWidget(self._build_library())
        splitter.addWidget(self._build_editor())
        splitter.setSizes([370, 870])
        layout.addWidget(splitter, 1)
        return body

    def _build_library(self) -> QWidget:
        panel = QWidget()
        panel.setObjectName("LibraryPanel")
        layout = QVBoxLayout(panel)
        self.library = QListWidget()
        self.library.currentRowChanged.connect(self._select_track)
        layout.addWidget(QLabel("Library"))
        layout.addWidget(self.library, 1)
        self.info_table = QTableWidget(4, 2)
        self.info_table.setHorizontalHeaderLabels(["Property", "Value"])
        self.info_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.info_table.verticalHeader().hide()
        self.info_table.setEditTriggers(QTableWidget.NoEditTriggers)
        layout.addWidget(self.info_table)
        return panel

    def _build_editor(self) -> QWidget:
        panel = QWidget()
        panel.setObjectName("EditorPanel")
        layout = QHBoxLayout(panel)

        cover_box = QVBoxLayout()
        self.cover = QLabel()
        self.cover.setObjectName("CoverPreview")
        self.cover.setAlignment(Qt.AlignCenter)
        self.cover.setMinimumSize(290, 290)
        self.cover.setText("KAE")
        cover_box.addWidget(self.cover)
        for label, handler in [
            ("change_cover", self.change_cover),
            ("export_cover", self.export_cover),
            ("remove_cover", self.remove_cover),
            ("import_json", self.import_json),
            ("export_json", self.export_json),
        ]:
            button = QPushButton(t(self.settings.language, label))
            button.clicked.connect(handler)
            cover_box.addWidget(button)
        cover_box.addStretch()

        form_frame = QFrame()
        form_frame.setObjectName("FormFrame")
        form = QGridLayout(form_frame)
        rows = [
            ("title", "title"),
            ("artist", "artist"),
            ("album", "album"),
            ("album_artist", "album_artist"),
            ("genre", "genre"),
            ("year", "year"),
            ("track_number", "track"),
            ("disc_number", "disc"),
            ("composer", "composer"),
            ("bpm", "bpm"),
        ]
        for row, (field, label) in enumerate(rows):
            form.addWidget(QLabel(t(self.settings.language, label)), row, 0)
            edit = QLineEdit()
            edit.textEdited.connect(self._mark_dirty)
            self.fields[field] = edit
            form.addWidget(edit, row, 1)
        form.addWidget(QLabel(t(self.settings.language, "comment")), len(rows), 0)
        comment = QTextEdit()
        comment.textChanged.connect(self._mark_dirty)
        self.fields["comment"] = comment
        form.addWidget(comment, len(rows), 1)
        form.addWidget(QLabel(t(self.settings.language, "lyrics")), len(rows) + 1, 0)
        lyrics = QTextEdit()
        lyrics.textChanged.connect(self._mark_dirty)
        self.fields["lyrics"] = lyrics
        form.addWidget(lyrics, len(rows) + 1, 1)

        batch = QPushButton(t(self.settings.language, "batch") + ": album/artist/genre/year")
        batch.clicked.connect(self.batch_apply_common_fields)
        form.addWidget(batch, len(rows) + 2, 1)

        layout.addLayout(cover_box)
        layout.addWidget(form_frame, 1)
        return panel

    def _create_actions(self) -> None:
        bindings = [
            ("Ctrl+O", self.open_files),
            ("Ctrl+Shift+O", self.open_folder),
            ("Ctrl+S", self.save_current),
            ("Ctrl+Shift+S", self.save_selected),
            ("Ctrl+I", self.import_json),
            ("Ctrl+E", self.export_json),
            ("Ctrl+Shift+C", self.change_cover),
            ("Ctrl+F", lambda: self.search.setFocus()),
            ("Ctrl+,", self.open_settings),
        ]
        for shortcut, handler in bindings:
            action = QAction(self)
            action.setShortcut(QKeySequence(shortcut))
            action.triggered.connect(handler)
            self.addAction(action)

    def open_files(self) -> None:
        paths, _ = QFileDialog.getOpenFileNames(
            self,
            "Open audio",
            "",
            "Audio (*.mp3 *.flac *.ogg *.oga *.opus *.m4a *.aac *.wav *.aiff *.aif)",
        )
        self._add_paths([Path(path) for path in paths])

    def open_folder(self) -> None:
        folder = QFileDialog.getExistingDirectory(self, "Open folder")
        if folder:
            self._add_paths([Path(folder)])

    def save_current(self) -> None:
        track = self._current_track()
        if not track:
            return
        self._pull_fields(track)
        write_metadata(track)
        self._refresh_item(self.current_index)

    def save_selected(self) -> None:
        rows = [index.row() for index in self.library.selectedIndexes()] or [self.current_index]
        for row in sorted(set(rows)):
            if 0 <= row < len(self.tracks):
                if row == self.current_index:
                    self._pull_fields(self.tracks[row])
                write_metadata(self.tracks[row])
                self._refresh_item(row)

    def change_cover(self) -> None:
        track = self._current_track()
        if not track:
            return
        path, _ = QFileDialog.getOpenFileName(self, "Cover", "", "Images (*.png *.jpg *.jpeg)")
        if path:
            replace_artwork(track, Path(path))
            self._render_cover(track)

    def export_cover(self) -> None:
        track = self._current_track()
        if not track or not track.artwork_bytes:
            return
        suffix = ".png" if track.artwork_mime == "image/png" else ".jpg"
        path, _ = QFileDialog.getSaveFileName(
            self,
            "Export cover",
            track.path.with_suffix(suffix).name,
            "Images (*.png *.jpg)",
        )
        if path:
            Path(path).write_bytes(track.artwork_bytes)

    def remove_cover(self) -> None:
        track = self._current_track()
        if track:
            remove_artwork(track)
            self._render_cover(track)

    def import_json(self) -> None:
        track = self._current_track()
        if not track:
            return
        path, _ = QFileDialog.getOpenFileName(self, "Import metadata", "", "JSON (*.json)")
        if path:
            import_metadata_json(track, Path(path))
            self._push_fields(track)

    def export_json(self) -> None:
        track = self._current_track()
        if not track:
            return
        self._pull_fields(track)
        path, _ = QFileDialog.getSaveFileName(
            self,
            "Export metadata",
            track.path.with_suffix(".json").name,
            "JSON (*.json)",
        )
        if path:
            export_metadata_json(track, Path(path))

    def batch_apply_common_fields(self) -> None:
        source = self._current_track()
        if not source:
            return
        self._pull_fields(source)
        rows = [index.row() for index in self.library.selectedIndexes()]
        for row in rows:
            track = self.tracks[row]
            for field in ["album", "album_artist", "genre", "year"]:
                setattr(track, field, getattr(source, field))
            track.dirty = True
            self._refresh_item(row)

    def open_settings(self) -> None:
        dialog = SettingsDialog(self.settings, self)
        if dialog.exec():
            self._apply_theme()

    def _add_paths(self, paths: list[Path]) -> None:
        files = discover_audio_files(paths)
        loaded: list[Path] = []
        for file in files:
            if any(track.path == file for track in self.tracks):
                continue
            try:
                track = read_metadata(file)
            except Exception as exc:
                QMessageBox.warning(self, "KAE", str(exc))
                continue
            self.tracks.append(track)
            loaded.append(file)
            item = QListWidgetItem(self._item_label(track))
            self.library.addItem(item)
        if loaded:
            self.settings.remember(loaded)
        if self.current_index == -1 and self.tracks:
            self.library.setCurrentRow(0)

    def _load_recent(self) -> None:
        recent = [Path(path) for path in self.settings.recent_files if Path(path).exists()]
        if recent:
            self._add_paths(recent[:8])

    def _select_track(self, row: int) -> None:
        if self.settings.autosave_on_file_switch and self.current_index >= 0:
            self.save_current()
        self.current_index = row
        track = self._current_track()
        if track:
            self._push_fields(track)
            self._render_cover(track)
            self._render_info(track)

    def _push_fields(self, track: TrackMetadata) -> None:
        for field, widget in self.fields.items():
            value = getattr(track, field)
            if isinstance(widget, QTextEdit):
                widget.blockSignals(True)
                widget.setPlainText(value)
                widget.blockSignals(False)
            else:
                widget.blockSignals(True)
                widget.setText(value)
                widget.blockSignals(False)

    def _pull_fields(self, track: TrackMetadata) -> None:
        for field, widget in self.fields.items():
            value = widget.toPlainText() if isinstance(widget, QTextEdit) else widget.text()
            setattr(track, field, value)
        track.dirty = True

    def _render_cover(self, track: TrackMetadata) -> None:
        pixmap = QPixmap()
        if track.artwork_bytes:
            pixmap.loadFromData(QByteArray(track.artwork_bytes))
        else:
            pixmap.load(str(asset_path("images", "kae_mascot.png")))
        self.cover.setPixmap(pixmap.scaled(290, 290, Qt.KeepAspectRatio, Qt.SmoothTransformation))

    def _render_info(self, track: TrackMetadata) -> None:
        rows = [
            ("File", track.filename),
            ("Duration", f"{track.duration_seconds:.1f}s"),
            ("Bitrate", f"{track.bitrate // 1000} kbps" if track.bitrate else "-"),
            ("Sample", f"{track.sample_rate} Hz" if track.sample_rate else "-"),
        ]
        for row, (key, value) in enumerate(rows):
            self.info_table.setItem(row, 0, QTableWidgetItem(key))
            self.info_table.setItem(row, 1, QTableWidgetItem(value))

    def _filter_tracks(self, text: str) -> None:
        needle = text.lower().strip()
        for row in range(self.library.count()):
            item = self.library.item(row)
            item.setHidden(needle not in item.text().lower())

    def _mark_dirty(self) -> None:
        track = self._current_track()
        if track:
            track.dirty = True
            self._refresh_item(self.current_index)

    def _refresh_item(self, row: int) -> None:
        if 0 <= row < len(self.tracks):
            self.library.item(row).setText(self._item_label(self.tracks[row]))

    def _item_label(self, track: TrackMetadata) -> str:
        marker = " *" if track.dirty else ""
        title = track.title or track.path.stem
        artist = f" - {track.artist}" if track.artist else ""
        return f"{title}{artist}{marker}"

    def _current_track(self) -> TrackMetadata | None:
        if 0 <= self.current_index < len(self.tracks):
            return self.tracks[self.current_index]
        return None

    def _apply_theme(self) -> None:
        QApplication.instance().setStyleSheet(load_stylesheet(self.settings.compact_mode))
