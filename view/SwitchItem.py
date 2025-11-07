from PySide6.QtGui import QBrush, QColor, QPainter, QPen
from PySide6.QtCore import Qt, QRectF

from view.ComponentItem import ComponentItem

class SwitchItem(ComponentItem):

    def __init__(self, componentVM, radius=20, parent=None):
        super().__init__(componentVM=componentVM)
        self.radius = radius
        self._rect = QRectF(-self.radius, -self.radius, 2*self.radius, 2*self.radius)
        self.on = False 
        self.initPinItems()

    def boundingRect(self) -> QRectF:
        return QRectF(-self.radius, -self.radius, 2*self.radius, 2*self.radius)

    def paint(self, painter: QPainter, option, widget=None):
        painter.setRenderHint(QPainter.Antialiasing)

        self._color = QColor("green") if self.on else QColor("red")
        self._selectedColor = QColor("green")
        brush = QBrush(self._color)
        painter.setBrush(brush)

        pen = QPen(QColor("black"))
        pen.setWidth(2)
        painter.setPen(pen)

        painter.drawEllipse(self.boundingRect())

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.on = not self.on
            self._componentVM.toggle()
            self.update() 
            event.accept()
        else:
            event.ignore()