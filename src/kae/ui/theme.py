from __future__ import annotations

from kae.paths import asset_path

NIGHT_OVERRIDES = """
#AppBody {
  background: qlineargradient(
    x1:0,
    y1:0,
    x2:1,
    y2:1,
    stop:0 #271124,
    stop:0.55 #58163d,
    stop:1 #c52b78
  );
}

TitleBar {
  background: #170914;
  border-bottom: 1px solid #ff69ad;
}

#LibraryPanel,
#EditorPanel {
  background: rgba(42, 12, 33, 0.82);
  border: 1px solid rgba(255, 115, 184, 0.65);
}

#FormFrame {
  background: rgba(255, 188, 220, 0.10);
}

QLabel {
  color: #fff2f9;
}

QPushButton {
  background: rgba(49, 18, 39, 0.94);
  color: #fff4fa;
  border-color: #ff74b7;
}

QPushButton:hover {
  background: rgba(92, 25, 65, 0.96);
  border-color: #ff9bce;
}

QPushButton:pressed {
  background: #8f1f5f;
}

TitleBar QPushButton {
  background: #fff7fb;
  color: #34182a;
  border: 0;
}

#CloseButton {
  background: #fa4f94;
  color: white;
}

QLineEdit,
QTextEdit,
QListWidget,
QTableWidget,
QComboBox {
  background: rgba(31, 12, 26, 0.92);
  color: #fff4fa;
  border-color: #ff74b7;
}

QComboBox::drop-down {
  border-left: 1px solid #ff74b7;
  background: rgba(255, 116, 183, 0.16);
}

QCheckBox {
  color: #fff2f9;
  spacing: 8px;
}

QCheckBox::indicator {
  width: 15px;
  height: 15px;
  border-radius: 3px;
  border: 1px solid #ff83be;
  background: rgba(31, 12, 26, 0.92);
}

QCheckBox::indicator:checked {
  background: #ff5ca8;
}

QDialog#SettingsDialog {
  background: #26101f;
}

QDialog#SettingsDialog QLabel {
  color: #fff2f9;
}

QDialog#SettingsDialog QCheckBox {
  color: #fff2f9;
}

QDialog#SettingsDialog QPushButton {
  background: rgba(255, 247, 251, 0.96);
  color: #34182a;
}

#CoverPreview {
  background: #21101c;
  color: #ff93c9;
}
"""


def load_stylesheet(compact: bool = False, theme: str = "sakura") -> str:
    qss = asset_path("styles", "sakura.qss").read_text(encoding="utf-8")
    qss = qss.replace("/*DENSITY*/", "6px" if compact else "10px")
    if theme == "night":
        qss += NIGHT_OVERRIDES
    return qss
