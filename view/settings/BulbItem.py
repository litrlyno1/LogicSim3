from view.settings.CircuitComponentItem import CircuitComponentItemSettings

from PySide6.QtCore import QSize
from PySide6.QtGui import QColor

class BulbItemSettings(CircuitComponentItemSettings):
    
    def __init__(self,
                size,
                fontSize,
                textColor,
                color,
                onColor,
                selectedColor,
                draggingColor,
                borderColor,
                borderWidth):
        
        self.SIZE = size
        self.FONT_SIZE = fontSize
        self.TEXT_COLOR = textColor
        self.COLOR = color
        self.ON_COLOR = onColor
        self.SELECTED_COLOR = selectedColor
        self.BORDER_COLOR = borderColor
        self.BORDER_WIDTH = borderWidth
        self.DRAGGING_COLOR = draggingColor
    
    @classmethod
    def default(cls):
        settings = CircuitComponentItemSettings.default()
        settings.SIZE = QSize(40, 40)
        settings.COLOR = QColor(255, 170, 170)
        ON_COLOR = QColor(184, 230, 176)
        draggingColor = QColor(245, 245, 245)
        return cls(settings.SIZE, settings.FONT_SIZE, settings.TEXT_COLOR, settings.COLOR, ON_COLOR, 
                    settings.SELECTED_COLOR, draggingColor, settings.BORDER_COLOR, settings.BORDER_WIDTH)