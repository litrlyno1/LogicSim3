from PySide6.QtGui import QColor
from PySide6.QtCore import Qt

class ConnectionItemSettings:
    def __init__(self,
                color,
                onColor,
                selectedColor,
                width):
        self.COLOR = color
        self.ON_COLOR = onColor
        self.SELECTED_COLOR = selectedColor
        self.WIDTH = width
    
    @classmethod
    def default(cls):
        color = Qt.black
        onColor = QColor(170, 225, 255, 200)
        selectedColor = QColor(214, 88, 56)
        width = 6
        return cls(color, onColor, selectedColor, width)