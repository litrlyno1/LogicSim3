from PySide6.QtGui import QBrush, QColor

class CanvasSettings():
    def __init__(self,
                zoom: float,
                backgroundColor: QColor,
                gridColor : QColor,
                gridDarkColor : QColor,
                gridSize: int,
                gridMajorFactor: int):
        self.ZOOM = zoom
        self.BACKGROUND_COLOR = backgroundColor
        self.GRID_COLOR = gridColor
        self.GRID_DARK_COLOR = gridDarkColor
        self.GRID_SIZE = gridSize
        self.GRID_MAJOR_FACTOR = gridMajorFactor
    
    @classmethod
    def default(cls):
        zoom = 1.0
        backgroundColor = QColor("#BABABA")
        gridColor = QColor("#575757")
        gridDarkColor = QColor("#3B3B3B")
        gridSize = 10
        gridMajorFactor = 5
        return cls(zoom, backgroundColor, gridColor, gridDarkColor, gridSize, gridMajorFactor)