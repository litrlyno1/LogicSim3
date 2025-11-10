from view.settings.CircuitComponentItem import CircuitComponentItemSettings

from PySide6.QtCore import QSize
from PySide6.QtGui import QColor

class SwitchItemSettings(CircuitComponentItemSettings):
    
    def __init__(self,
                size,
                fontSize,
                textColor,
                color,
                onColor,
                selectedColor,
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
    
    @classmethod
    def default(cls):
        settings = CircuitComponentItemSettings.default()
        settings.SIZE = QSize(50, 50)
        settings.COLOR = QColor(255, 170, 170)
        ON_COLOR = QColor(184, 230, 176)
        return cls(settings.SIZE, settings.FONT_SIZE, settings.TEXT_COLOR, settings.COLOR, ON_COLOR, 
                    settings.SELECTED_COLOR, settings.BORDER_COLOR, settings.BORDER_WIDTH)