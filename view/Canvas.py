from PySide6.QtWidgets import QGraphicsView, QGraphicsScene, QGraphicsRectItem
from PySide6.QtCore import Signal, QPointF, Qt
from PySide6.QtGui import QWheelEvent, QMouseEvent, QPainter, QPen, QColor

from view.settings.Canvas import CanvasSettings

class Canvas(QGraphicsView):
    
    def __init__(self, settings : CanvasSettings = CanvasSettings.default):
        super().__init__()
        self._scene = QGraphicsScene(self)
        self.setScene(self._scene)

        self.setRenderHints(self.renderHints() | 
                    QPainter.Antialiasing |
                    QPainter.SmoothPixmapTransform)
        self.setDragMode(QGraphicsView.NoDrag)
        self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)
        self.setResizeAnchor(QGraphicsView.AnchorUnderMouse)

        self._last_pan_point = None
        self._zoom = 1.0
        self._draw_grid(50, QColor("#cccccc"))

    def _draw_grid(self, step=50, color=QColor("#cccccc")):
        pen = QPen(color)
        for x in range(-2000, 2000, step):
            self._scene.addLine(x, -2000, x, 2000, pen)
        for y in range(-2000, 2000, step):
            self._scene.addLine(-2000, y, 2000, y, pen)