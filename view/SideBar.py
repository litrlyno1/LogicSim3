from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QSizePolicy, QLabel
from PySide6.QtGui import QDrag, QPixmap, QPainter
from PySide6.QtCore import Qt, QMimeData
from typing import List

from core.registry import GateRegistry

class SideBar(QWidget):
    
    def __init__(self,  parent=None, gateTypes: list[str] = GateRegistry.getAllGates()):
        super().__init__(parent)
        self.gateTypes = gateTypes
        self._setupUi()

    def _setupUi(self):
        self.setFixedWidth(180)
        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(8, 8, 8, 8)
        layout.setSpacing(10)

        header = QLabel("Logic Gates")
        header.setAlignment(Qt.AlignCenter)
        header.setStyleSheet("font-weight: bold; font-size: 14px;")
        layout.addWidget(header)

        for gateType in self.gateTypes:
            button = QPushButton(gateType)
            button.setObjectName(f"btn_{gateType.lower()}")
            button.setStyleSheet("""
                QPushButton {
                    padding: 6px;
                    border-radius: 6px;
                    background-color: #e0e0e0;
                }
                QPushButton:hover {
                    background-color: #cfd8dc;
                }
            """)
            button.pressed.connect(lambda gt = gateType: self.startDrag(gt))
            layout.addWidget(button)

        layout.addStretch()
    
    def startDrag(self, gateType: str):
        drag = QDrag(self)
        mime = QMimeData()
        mime.setText(gateType)
        drag.setMimeData(mime)
        print("Starting drag for:", mime.text())
        drag.exec(Qt.CopyAction)