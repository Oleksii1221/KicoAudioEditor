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

QLineEdit,
QTextEdit,
QListWidget,
QTableWidget,
QComboBox {
  background: rgba(31, 12, 26, 0.92);
  color: #fff4fa;
  border-color: #ff74b7;
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
