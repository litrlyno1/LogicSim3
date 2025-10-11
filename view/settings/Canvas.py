from PySide6.QtGui import QColor
from PySide6.QtCore import QRect

class CanvasSettings:
    def __init__(self,
                sceneRect : QRect,
                zoom: float,
                zoomMin : float,
                zoomMax : float,
                zoomStep : float,
                backgroundColor: QColor,
                gridColor : QColor,
                gridDarkColor : QColor,
                gridSize: int,
                gridMajorFactor: int):
        self.SCENE_RECT = sceneRect
        self.ZOOM = zoom
        self.ZOOM_MIN = zoomMin
        self.ZOOM_MAX = zoomMax
        self.ZOOM_STEP = zoomStep
        self.BACKGROUND_COLOR = backgroundColor
        self.GRID_COLOR = gridColor
        self.GRID_DARK_COLOR = gridDarkColor
        self.GRID_SIZE = gridSize
        self.GRID_MAJOR_FACTOR = gridMajorFactor
    
    @classmethod
    def default(cls):
        sceneRect = QRect(0, 0, 2000, 2000)
        zoom = 1.0
        zoomMin = 0.5
        zoomMax = 20.0
        zoomStep = 1.1
        backgroundColor = QColor("#BABABA")
        gridColor = QColor("#575757")
        gridDarkColor = QColor("#3B3B3B")
        gridSize = 10
        gridMajorFactor = 5
        return cls(sceneRect, zoom, zoomMin, zoomMax, zoomStep, backgroundColor, gridColor, gridDarkColor, gridSize, gridMajorFactor)