from PySide6.QtGui import QPen, QPainterPath
from PySide6.QtWidgets import QGraphicsPathItem, QGraphicsItem, QGraphicsObject
from PySide6.QtCore import Qt, QPointF, Signal

from view.PinItem import PinItem
from view.settings.ConnectionItem import ConnectionItemSettings

class ConnectionItem(QGraphicsObject):
    selected = Signal(str)
    removed = Signal(str)
    valueChanged = Signal(str)
    
    class CubicPath(QGraphicsPathItem):
        
        def __init__(self, start: QPointF, end: QPointF, settings: ConnectionItemSettings = ConnectionItemSettings.default()):
            super().__init__()
            self._start = start
            self._end = end
            self._importSettings(settings)
        
        def _importSettings(self, settings: ConnectionItemSettings):
            self._color = settings.COLOR
            self._onColor = settings.ON_COLOR
            self._selectedHighlightColor = settings.SELECTED_HIGHLIGHT_COLOR
            self._width = settings.WIDTH
        
        def _setupGraphics(self):
            pen = QPen(self._color, self._width)
            pen.setCapStyle(Qt.RoundCap)
            self.setPen(pen)
            self.update()
        
        @property
        def start(self):
            return self._start
        
        @start.setter
        def start(self, newStart: QPointF):
            self._start = newStart
            self.update()
        
        @property
        def end(self):
            return self._end
        
        @end.setter
        def end(self, newEnd: QPointF):
            self._end = newEnd
            self.update()
        
        def update(self):
            path = QPainterPath(self._start)
            dx = (self._end.x() - self._start.x()) * 0,5
            controlPoint1 = QPointF(self._start.x() + dx, self._start.y())
            controlPoint2 = QPointF(self._end.x() - dx, self._end.y())
            path.cubicTo(controlPoint1, controlPoint2, self._end)
            self.setPath(path)
    
    def __init__(self, id: str, pinItem1: PinItem, pinItem2: PinItem, settings: ConnectionItemSettings = ConnectionItemSettings.default()):
        super().__init__()
        self._path = ConnectionItem.CubicPath(pinItem1.center, pinItem2.center, settings)
        pinItem1.parentMoved.connect(lambda: self.updateStart(pinItem1.center))
        pinItem2.parentMoved.connect(lambda: self.updateEnd(pinItem2.center))
    
    def updateStart(self, pos : QPointF):
        self._path.start = pos
    
    def updateEnd(self, pos : QPointF):
        self._path.end = pos