from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QSizePolicy, QLabel
from PySide6.QtGui import QDrag, QPixmap, QPainter
from PySide6.QtCore import Qt, QMimeData
from typing import List

from core.registry import ComponentRegistry
from view.settings.SideBar import SideBarSettings

class SideBar(QWidget):
    
    def __init__(self,  parent=None, gateTypes: list[str] = ComponentRegistry.getAllComponents(), settings = SideBarSettings.default()):
        super().__init__(parent)
        self.gateTypes = gateTypes
        self._importSettings(settings)
        self._setupGraphics()

    def _importSettings(self, settings):
        self._width = settings.WIDTH
        self._margin = settings.MARGIN
        self._spacing = settings.SPACING
        self._header = settings.HEADER
        self._styleSheet = settings.STYLE_SHEET
        self._buttonStyleSheet = settings.BUTTON_STYLE_SHEET

    def _setupGraphics(self):
        self.setFixedWidth(self._width)
        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(self._margin, self._margin, self._margin, self._margin)
        layout.setSpacing(self._spacing)
        header = QLabel(self._header)
        header.setAlignment(Qt.AlignCenter)
        header.setStyleSheet(self._styleSheet)
        layout.addWidget(header)
        for gateType in self.gateTypes:
            button = QPushButton(gateType)
            button.setObjectName(f"btn_{gateType.lower()}")
            button.setStyleSheet(self._buttonStyleSheet)
            button.pressed.connect(lambda gt = gateType: self.startDrag(gt))
            layout.addWidget(button)
        layout.addStretch()
    
    def startDrag(self, gateType: str):
        drag = QDrag(self)
        mime = QMimeData()
        mime.setText(gateType)
        drag.setMimeData(mime)
        drag.exec(Qt.CopyAction)