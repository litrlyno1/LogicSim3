from PySide6.QtWidgets import QGraphicsEllipseItem
from PySide6.QtGui import QBrush, QColor
from PySide6.QtCore import QRectF

from view.ComponentItem import ComponentItem

class BulbItem(QGraphicsEllipseItem):
    def __init__(self, radius=20, parent=None):
        super().__init__(QRectF(-radius, -radius, 2*radius, 2*radius), parent)
        self._on = False
        self._radius = radius
        self._off_color = QColor("gray")
        self._on_color = QColor("yellow")
        self.setBrush(QBrush(self._off_color))
        self.setZValue(-1)  

    def setState(self, state: bool):
        self._on = state
        color = self._on_color if state else self._off_color
        self.setBrush(QBrush(color))

    def isOn(self) -> bool:
        return self._on