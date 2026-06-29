from __future__ import annotations

from PySide6.QtWidgets import (
    QCheckBox,
    QComboBox,
    QDialog,
    QFormLayout,
    QHBoxLayout,
    QPushButton,
    QVBoxLayout,
)

from kae.core.i18n import LANGUAGES, t
from kae.core.settings import AppSettings


class SettingsDialog(QDialog):
    def __init__(self, settings: AppSettings, parent=None) -> None:
        super().__init__(parent)
        self.setWindowTitle("KAE Settings")
        self.settings = settings
        self.language = QComboBox()
        for code, label in LANGUAGES.items():
            self.language.addItem(label, code)
        self.language.setCurrentIndex(max(0, self.language.findData(settings.language)))

        self.theme = QComboBox()
        self.theme.addItem("Sakura Candy", "sakura")
        self.theme.addItem("Night Sakura", "night")
        self.theme.setCurrentIndex(max(0, self.theme.findData(settings.theme)))

        self.autosave = QCheckBox("Autosave before switching files")
        self.autosave.setChecked(settings.autosave_on_file_switch)
        self.confirm = QCheckBox("Confirm before overwriting files")
        self.confirm.setChecked(settings.confirm_before_overwrite)
        self.recent = QCheckBox("Remember recent files")
        self.recent.setChecked(settings.remember_recent_files)
        self.compact = QCheckBox("Compact controls")
        self.compact.setChecked(settings.compact_mode)

        form = QFormLayout()
        form.addRow(t(settings.language, "language"), self.language)
        form.addRow(t(settings.language, "theme"), self.theme)
        form.addRow("", self.autosave)
        form.addRow("", self.confirm)
        form.addRow("", self.recent)
        form.addRow("", self.compact)

        cancel = QPushButton("Cancel")
        cancel.clicked.connect(self.reject)
        save = QPushButton("Save")
        save.clicked.connect(self.accept)
        buttons = QHBoxLayout()
        buttons.addStretch()
        buttons.addWidget(cancel)
        buttons.addWidget(save)

        layout = QVBoxLayout(self)
        layout.addLayout(form)
        layout.addLayout(buttons)

    def accept(self) -> None:
        self.settings.language = self.language.currentData()
        self.settings.theme = self.theme.currentData()
        self.settings.autosave_on_file_switch = self.autosave.isChecked()
        self.settings.confirm_before_overwrite = self.confirm.isChecked()
        self.settings.remember_recent_files = self.recent.isChecked()
        self.settings.compact_mode = self.compact.isChecked()
        self.settings.save()
        super().accept()
