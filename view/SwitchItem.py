from PySide6.QtWidgets import QGraphicsEllipseItem, QGraphicsSceneMouseEvent
from PySide6.QtGui import QBrush, QColor
from PySide6.QtCore import Qt, QRectF

from view.ComponentItem import ComponentItem

class SwitchItem(QGraphicsEllipseItem):
    def __init__(self, radius=20, parent=None):
        super().__init__(QRectF(-radius, -radius, 2*radius, 2*radius), parent)
        self.state = False
        self.setBrush(QBrush(QColor("gray")))
        self.setFlag(self.ItemIsSelectable)
        self.setAcceptHoverEvents(True)
        self.setCursor(Qt.PointingHandCursor)

    def mousePressEvent(self, event: QGraphicsSceneMouseEvent):
        self.toggle()
        super().mousePressEvent(event)

    def toggle(self):
        self.state = not self.state
        color = "green" if self.state else "gray"
        self.setBrush(QBrush(QColor(color)))

    def isOn(self):
        return self.state
