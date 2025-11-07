from PySide6.QtGui import QPen, QPainterPath
from PySide6.QtWidgets import QGraphicsPathItem, QGraphicsItem
from PySide6.QtCore import Qt, QPointF

from view import PinItem

class ConnectionItem(QGraphicsPathItem):
    def __init__(self, pinItem1 : PinItem, pinItem2 : PinItem):
        super().__init__()
        self._pinItem1 = pinItem1
        self._pinItem2 = pinItem2
        self._addToPins()
        
        pen = QPen(Qt.black, 3)
        pen.setCapStyle(Qt.RoundCap)
        self.setPen(pen)

        self.update_path()
    
    def _addToPins(self):
        self._pinItem1.addConnectionItem(self)
        self._pinItem2.addConnectionItem(self)

    def update_path(self):
        start = self._pinItem1.sceneBoundingRect().center()
        end = self._pinItem2.sceneBoundingRect().center()
        self.setPath(ConnectionItem.createPath(start, end))

    @staticmethod
    def createPath(start: QPointF, end: QPointF) -> QPainterPath:
        path = QPainterPath(start)
        dx = (end.x() - start.x()) * 0.5 
        ctrl1 = QPointF(start.x() + dx, start.y())
        ctrl2 = QPointF(end.x() - dx, end.y())

        path.cubicTo(ctrl1, ctrl2, end)
        return path
    
    @staticmethod
    def isViablePinPair(pin1 : PinItem, pin2 : PinItem) -> bool:
        if pin1.getParentComponent() == pin2.getParentComponent():
            print("Pin pair not viable: same parent gate")
            return False
        elif pin1.getType == pin2.getType:
            print("Pin pair not viable: same type")
            return False
        else:
            print("Pin pair viable")
            return True