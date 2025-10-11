from PySide6.QtWidgets import QGraphicsWidget, QGraphicsObject
from PySide6.QtGui import QPainter, QPen, QFont
from PySide6.QtCore import QRectF, QPointF, Qt
from viewmodel.LogicGateVM import LogicGateVM

from view.settings.GateItem import GateItemSettings

class GateItem(QGraphicsWidget):
    
    def __init__(self, logicGateVM : LogicGateVM, settings : GateItemSettings = GateItemSettings.default()):
        super().__init__()
        self._logicGateVM = logicGateVM
        self._importSettings(settings)
        self.setPos(self._logicGateVM.getPos())
        self.setFlags(QGraphicsObject.ItemIsMovable | QGraphicsObject.ItemIsSelectable | QGraphicsObject.ItemSendsGeometryChanges)
        self.setAcceptHoverEvents(True)
        self.setZValue(10)

    
    def _importSettings(self, settings : GateItemSettings):
        self._size = settings.SIZE
        self._boundingRect = QRectF(-self._size.width()/2, -self._size.height()/2, self._size.width(), self._size.height())
        self._fontSize = settings.FONT_SIZE
        self._textColor = settings.TEXT_COLOR
        self._color = settings.COLOR
        self._borderColor = settings.BORDER_COLOR
        self._borderWidth = settings.BORDER_WIDTH
        self._pen = QPen(self._color, self._borderWidth)
        self._textPen = QPen(self._textColor)
        self._font = QFont()
        self._font.setPointSize(self._fontSize)
        self._borderWidth = settings.BORDER_WIDTH
    
    def getPos(self):
        return(self._logicGateVM.getPos())
    
    def boundingRect(self) -> QRectF:
        return self._boundingRect
    
    def paint(self, painter : QPainter, option, widget = None):
        painter.setRenderHints(QPainter.Antialiasing)
        painter.setBrush(self._color)
        painter.setPen(self._pen)
        painter.drawRect(self._boundingRect)

        painter.setFont(self._font)
        painter.setPen(self._textPen)
        print(f"Gate Item type: {self._logicGateVM.getGateType()}")
        painter.drawText(self._boundingRect, Qt.AlignCenter, self._logicGateVM.getGateType())