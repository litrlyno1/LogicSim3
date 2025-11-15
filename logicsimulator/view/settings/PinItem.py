from PySide6.QtGui import QColor

class PinItemSettings:
    def __init__(self,
                radius, 
                color,
                selectedColor,
                parentSelectedColor,
                borderColor,
                draggingColor,
                borderWidth):
        self.RADIUS = radius
        self.COLOR = color
        self.SELECTED_COLOR = selectedColor
        self.PARENT_SELECTED_COLOR = parentSelectedColor
        self.DRAGGING_COLOR = draggingColor
        self.BORDER_COLOR = borderColor
        self.BORDER_WIDTH = borderWidth
    
    @classmethod
    def default(cls):
        radius = 6
        color = QColor(255,255,255)
        selectedColor = QColor(170, 225, 255, 255)
        parentSelectedColor = QColor(200, 200, 200, 255)
        draggingColor = QColor(230, 230, 230)
        borderColor = QColor(0,0,0)
        borderWidth = 1
        return cls(radius, color, selectedColor, parentSelectedColor, borderColor, draggingColor, borderWidth)

class InputPinItemSettings(PinItemSettings):
    
    @staticmethod
    def default():
        return PinItemSettings.default()

class OutputPinItemSettings(PinItemSettings):
    
    @staticmethod
    def default():
        return PinItemSettings.default()