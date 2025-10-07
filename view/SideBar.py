from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QSizePolicy, QLabel
from PySide6.QtCore import Qt
from typing import List 

from core.registry import registry


class SideBar(QWidget):
    
    def __init__(self,  parent=None, gate_types: list[str] = ("AndGate", "OrGate", "NotGate")):
        super().__init__(parent)
        self.gate_types = gate_types
        self._setup_ui()

    def _setup_ui(self):
        self.setFixedWidth(180)
        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(8, 8, 8, 8)
        layout.setSpacing(10)

        header = QLabel("Logic Gates")
        header.setAlignment(Qt.AlignCenter)
        header.setStyleSheet("font-weight: bold; font-size: 14px;")
        layout.addWidget(header)

        for gate_type in self.gate_types:
            button = QPushButton(gate_type)
            button.setObjectName(f"btn_{gate_type.lower()}")
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
            layout.addWidget(button)

        layout.addStretch()