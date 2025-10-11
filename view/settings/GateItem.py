from PySide6.QtCore import QSize
from PySide6.QtGui import QColor

class GateItemSettings:
    
    def __init__(self,
                size,
                fontSize,
                textColor,
                color,
                borderColor,
                borderWidth):
        
        self.SIZE = size
        self.FONT_SIZE = fontSize
        self.TEXT_COLOR = textColor
        self.COLOR = color
        self.BORDER_COLOR = borderColor
        self.BORDER_WIDTH = borderWidth
    
    @classmethod
    def default(cls):
        size = QSize(80, 50)
        fontSize = 10
        textColor = QColor(0,0,0)
        color = QColor(245, 245, 245)
        borderColor = QColor(50, 50, 50)
        borderWidth = 1.2
        return cls(size, fontSize, textColor, color, borderColor, borderWidth)