from PySide6.QtWidgets import QGraphicsView, QGraphicsScene, QGraphicsRectItem
from PySide6.QtCore import Signal, QPointF, Qt
from PySide6.QtGui import QWheelEvent, QMouseEvent, QPainter, QPen, QColor, QBrush

from view.settings.Canvas import CanvasSettings

class Canvas(QGraphicsView):
    
    def __init__(self, settings : CanvasSettings = CanvasSettings.default()):
        super().__init__()
        self._scene = QGraphicsScene(self)
        self._zoom = settings.ZOOM
        self._backgroundColor = settings.BACKGROUND_COLOR
        self._gridColor = settings.GRID_COLOR
        self._gridDarkColor = settings.GRID_COLOR
        self._gridSize = settings.GRID_SIZE
        self._gridMajorFactor = settings.GRID_MAJOR_FACTOR
        self.setScene(self._scene)
        self.setViewportUpdateMode(QGraphicsView.FullViewportUpdate)
        self.setRenderHints(QPainter.Antialiasing | QPainter.SmoothPixmapTransform)
        self.setDragMode(QGraphicsView.DragMode.RubberBandDrag)
        self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)
        self.setResizeAnchor(QGraphicsView.AnchorUnderMouse)
        self.setBackgroundBrush(QBrush(self._backgroundColor))

        self._panning = False
        self._lastPanPos = None
        self.update()
        
    def importSettings(self, settings: CanvasSettings):
        pass
        #todo
    
    def drawBackground(self, painter: QPainter, rect):
        super().drawBackground(painter, rect)
        left = int(rect.left()) - (int(rect.left()) % self._gridSize)
        top = int(rect.top()) - (int(rect.top()) % self._gridSize)

        painter.setPen(QPen(self._gridColor, 0))
        x = left
        while x < rect.right():
            painter.drawLine(x, rect.top(), x, rect.bottom())
            x += self._gridSize

        y = top
        while y < rect.bottom():
            painter.drawLine(rect.left(), y, rect.right(), y)
            y += self._gridSize

        major = self._gridSize * self._gridMajorFactor
        painter.setPen(QPen(self._gridDarkColor, 0))
        x = int(rect.left()) - (int(rect.left()) % major)
        while x < rect.right():
            painter.drawLine(x, rect.top(), x, rect.bottom())
            x += major
        y = int(rect.top()) - (int(rect.top()) % major)
        while y < rect.bottom():
            painter.drawLine(rect.left(), y, rect.right(), y)
            y += major