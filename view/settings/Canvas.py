from PySide6.QtGui import QColor
from PySide6.QtCore import QRect

class CanvasSettings:
    def __init__(self,
                sceneRect : QRect,
                zoom: float,
                zoomMin : float,
                zoomMax : float,
                zoomStep : float,
                wheelNotchDelta: float,
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
        self.WHEEL_NOTCH_DATA = wheelNotchDelta
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
        zoomStep = 1.15
        wheelNotchDelta = 120
        backgroundColor = QColor("#D4D4D4")
        gridColor = QColor("#646464")
        gridDarkColor = QColor("#2A2A2A")
        gridSize = 10
        gridMajorFactor = 5
        return cls(sceneRect, zoom, zoomMin, zoomMax, zoomStep, wheelNotchDelta, backgroundColor, gridColor, gridDarkColor, gridSize, gridMajorFactor)