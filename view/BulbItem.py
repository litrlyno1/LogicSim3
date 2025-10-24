from PySide6.QtGui import QBrush, QColor, QPainter, QPen
from PySide6.QtCore import QRectF, Qt

from view.ComponentItem import ComponentItem
from viewmodel.ComponentVM import ComponentVM

class BulbItem(ComponentItem):
    
    def __init__(self, componentVM):
        super().__init__(componentVM=componentVM)
        self._rect = QRectF(
            -80 / 2,
            -50 / 2,
            80,
            50
        )
    
    def boundingRect(self):
        return self._rect

    def paint(self, painter: QPainter, option, widget=None):
        painter.setRenderHint(QPainter.Antialiasing)

        color = QColor("blue")
        brush = QBrush(color)
        painter.setBrush(brush)

        pen = QPen(QColor("black"))
        pen.setWidth(2)
        painter.setPen(pen)

        painter.drawRect(self._rect)