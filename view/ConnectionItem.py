from PySide6.QtGui import QPen, QPainterPath
from PySide6.QtWidgets import QGraphicsPathItem, QGraphicsItem, QGraphicsObject
from PySide6.QtCore import Qt, QPointF, Signal

from view.PinItem import PinItem
from view.settings.ConnectionItem import ConnectionItemSettings

class ConnectionItem(QGraphicsObject):
    removed = Signal(str)
    valueChanged = Signal(str)
    
    class CubicPath(QGraphicsPathItem):
        
        def __init__(self, start: QPointF, end: QPointF, settings: ConnectionItemSettings = ConnectionItemSettings.default()):
            super().__init__()
            self._start = start
            self._end = end
            self._importSettings(settings)
            self._setupGraphics()
        
        def _importSettings(self, settings: ConnectionItemSettings):
            self._settings = settings
            self._color = settings.COLOR
            self._selectedColor = settings.SELECTED_COLOR
            self._onColor = settings.ON_COLOR
            self._width = settings.WIDTH
        
        def _setupGraphics(self):
            self._pen = QPen(self._color, self._width)
            self._pen.setCapStyle(Qt.RoundCap)
            self.setPen(self._pen)
            self.setZValue(1)
            self._updatePath()
        
        
        def boundingRect(self):
            return super().boundingRect()
        
        @property
        def start(self):
            return self._start

        @start.setter
        def start(self, newStart: QPointF):
            self._start = newStart
            self._updatePath()

        @property
        def end(self):
            return self._end

        @end.setter
        def end(self, newEnd: QPointF):
            self._end = newEnd
            self._updatePath()

        def _updatePath(self):
            path = QPainterPath(self._start)
            dx = (self._end.x() - self._start.x()) * 0.5
            controlPoint1 = QPointF(self._start.x() + dx, self._start.y())
            controlPoint2 = QPointF(self._end.x() - dx, self._end.y())
            path.cubicTo(controlPoint1, controlPoint2, self._end)
            self.setPath(path)
        
        def clone(self):
            clone = ConnectionItem.CubicPath(self._start, self._end, self._settings)
            return clone
    
        def ghost(self):
            ghost = self.clone()
            ghost.setOpacity(0.5)
            ghost.setZValue(self.zValue() + 1)
            print(f"GhostConnection: parent: {ghost.parentItem()}, z: {ghost.zValue()}")
            return ghost
    
    def __init__(self, id: str, pinItem1: PinItem, pinItem2: PinItem, settings: ConnectionItemSettings = ConnectionItemSettings.default()):
        super().__init__()
        self._path = ConnectionItem.CubicPath(pinItem1.center, pinItem2.center, settings)
        self._path.setParentItem(self)
        pinItem1.parentMoved.connect(lambda: self.updateStart(pinItem1.center))
        pinItem2.parentMoved.connect(lambda: self.updateEnd(pinItem2.center))
        self.setFlags(
            QGraphicsItem.ItemIsSelectable |
            QGraphicsItem.ItemSendsGeometryChanges
        )
        print(self._path.start)
        print(self._path.end)
    
    def updateStart(self, pos : QPointF):
        self._path.start = pos
    
    def updateEnd(self, pos : QPointF):
        self._path.end = pos

    def boundingRect(self):
        return self._path.boundingRect()

    def paint(self, painter, option, widget=None):
        pass
    
    def shape(self):
        return self._path.shape()
    
    def itemChange(self, change, value):
        if change == QGraphicsItem.ItemSelectedHasChanged:
            self._path._pen.setColor(self._path._selectedColor) if value else self._path._pen.setBrush(self._path._color)
            self._path.setPen(self._path._pen)
            self.update()
        return super().itemChange(change, value)