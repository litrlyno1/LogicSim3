from PySide6.QtGui import QColor
from PySide6.QtCore import Qt

class ConnectionItemSettings:
    def __init__(self,
                color,
                onColor,
                selectedHighlightColor,
                width):
        self.COLOR = color
        self.ON_COLOR = onColor
        self.SELECTED_HIGHLIGHT_COLOR = selectedHighlightColor
        self.WIDTH = width
    
    @classmethod
    def default(cls):
        color = Qt.black
        onColor = QColor(170, 225, 255, 200)
        selectedHighlightColor = QColor(255, 225, 170)
        width = 3
        return cls(color, onColor, selectedHighlightColor, width)