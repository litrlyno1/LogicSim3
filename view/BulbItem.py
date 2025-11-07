from PySide6.QtGui import QBrush, QColor, QPainter, QPen
from PySide6.QtCore import QRectF, Qt, Slot

from view.ComponentItem import ComponentItem
from viewmodel.CircuitComponentVM import ComponentVM

class BulbItem(ComponentItem):
    
    def __init__(self, componentVM):
        super().__init__(componentVM=componentVM)
        self._componentVM.modelUpdated.connect(self.updateView)
        self._rect = QRectF(
            -80 / 2,
            -50 / 2,
            80,
            50
        )
        self.initPinItems()
        self._value = False
    
    def boundingRect(self):
        return self._rect

    def paint(self, painter: QPainter, option, widget=None):
        painter.setRenderHint(QPainter.Antialiasing)
        self._color = QColor("blue")
        self._onColor = QColor("red")
        self._selectedColor = QColor("gray")
        brush = QBrush(self._color) if self._value == False else QBrush(self._onColor)
        painter.setBrush(brush)

        pen = QPen(QColor("black"))
        pen.setWidth(2)
        painter.setPen(pen)

        painter.drawRect(self._rect)
    
    @Slot(bool)
    def updateView(self, value : bool):
        self._value = value
        self.update()