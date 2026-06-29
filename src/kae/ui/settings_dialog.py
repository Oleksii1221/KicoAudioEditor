from __future__ import annotations

from PySide6.QtWidgets import (
    QCheckBox,
    QComboBox,
    QDialog,
    QFormLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QVBoxLayout,
)

from kae.core.i18n import LANGUAGES, t
from kae.core.settings import AppSettings


class SettingsDialog(QDialog):
    def __init__(self, settings: AppSettings, parent=None) -> None:
        super().__init__(parent)
        self.setObjectName("SettingsDialog")
        self.settings = settings
        self.form_labels: dict[str, QLabel] = {}
        self.setWindowTitle(t(settings.language, "settings_title"))
        self.language = QComboBox()
        for code, label in LANGUAGES.items():
            self.language.addItem(label, code)
        self.language.setCurrentIndex(max(0, self.language.findData(settings.language)))
        self.language.currentIndexChanged.connect(self._refresh_language)

        self.theme = QComboBox()
        self.theme.addItem("Sakura Candy", "sakura")
        self.theme.addItem("Night Sakura", "night")
        self.theme.setCurrentIndex(max(0, self.theme.findData(settings.theme)))

        self.autosave = QCheckBox()
        self.autosave.setChecked(settings.autosave_on_file_switch)
        self.confirm = QCheckBox()
        self.confirm.setChecked(settings.confirm_before_overwrite)
        self.recent = QCheckBox()
        self.recent.setChecked(settings.remember_recent_files)
        self.compact = QCheckBox()
        self.compact.setChecked(settings.compact_mode)

        form = QFormLayout()
        form.addRow(self._form_label("language"), self.language)
        form.addRow(self._form_label("theme"), self.theme)
        form.addRow("", self.autosave)
        form.addRow("", self.confirm)
        form.addRow("", self.recent)
        form.addRow("", self.compact)

        self.cancel = QPushButton()
        self.cancel.clicked.connect(self.reject)
        self.save = QPushButton()
        self.save.clicked.connect(self.accept)
        buttons = QHBoxLayout()
        buttons.addStretch()
        buttons.addWidget(self.cancel)
        buttons.addWidget(self.save)

        layout = QVBoxLayout(self)
        layout.addLayout(form)
        layout.addLayout(buttons)
        self._refresh_language()

    def accept(self) -> None:
        self.settings.language = self.language.currentData()
        self.settings.theme = self.theme.currentData()
        self.settings.autosave_on_file_switch = self.autosave.isChecked()
        self.settings.confirm_before_overwrite = self.confirm.isChecked()
        self.settings.remember_recent_files = self.recent.isChecked()
        self.settings.compact_mode = self.compact.isChecked()
        self.settings.save()
        super().accept()

    def _form_label(self, key: str) -> QLabel:
        label = QLabel()
        self.form_labels[key] = label
        return label

    def _refresh_language(self) -> None:
        language = self.language.currentData() or self.settings.language
        self.setWindowTitle(t(language, "settings_title"))
        for key, label in self.form_labels.items():
            label.setText(t(language, key))
        self.autosave.setText(t(language, "autosave"))
        self.confirm.setText(t(language, "confirm"))
        self.recent.setText(t(language, "recent"))
        self.compact.setText(t(language, "compact"))
        self.cancel.setText(t(language, "cancel"))
        self.save.setText(t(language, "save"))
