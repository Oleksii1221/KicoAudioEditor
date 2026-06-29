from __future__ import annotations

from PySide6.QtCore import QPoint, Qt
from PySide6.QtWidgets import QHBoxLayout, QLabel, QPushButton, QWidget


class TitleBar(QWidget):
    def __init__(self, parent) -> None:
        super().__init__(parent)
        self._drag_start: QPoint | None = None
        self.title = QLabel("KAE")
        self.title.setObjectName("TitleText")

        minimize = QPushButton("−")
        minimize.setToolTip("Minimize")
        minimize.clicked.connect(parent.showMinimized)
        maximize = QPushButton("□")
        maximize.setToolTip("Maximize")
        maximize.clicked.connect(self._toggle_maximized)
        close = QPushButton("×")
        close.setToolTip("Close")
        close.setObjectName("CloseButton")
        close.clicked.connect(parent.close)

        for button in [minimize, maximize, close]:
            button.setFixedSize(34, 30)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(14, 8, 10, 6)
        layout.addWidget(self.title)
        layout.addStretch()
        layout.addWidget(minimize)
        layout.addWidget(maximize)
        layout.addWidget(close)

    def mousePressEvent(self, event) -> None:
        if event.button() == Qt.LeftButton:
            self._drag_start = event.globalPosition().toPoint()

    def mouseMoveEvent(self, event) -> None:
        if self._drag_start is None:
            return
        parent = self.window()
        delta = event.globalPosition().toPoint() - self._drag_start
        parent.move(parent.pos() + delta)
        self._drag_start = event.globalPosition().toPoint()

    def mouseReleaseEvent(self, event) -> None:
        self._drag_start = None

    def _toggle_maximized(self) -> None:
        parent = self.window()
        if parent.isMaximized():
            parent.showNormal()
        else:
            parent.showMaximized()
