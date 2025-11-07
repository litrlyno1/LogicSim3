from PySide6.QtWidgets import QGraphicsRectItem, QGraphicsItem
from PySide6.QtGui import QPainter, QPen, QFont, QPainterPath
from PySide6.QtCore import QRectF, Qt

from viewmodel.LogicGateVM import LogicGateVM
from view.settings.GateItem import GateItemSettings
from view.ComponentItem import ComponentItem

class GateItem(ComponentItem):
    
    def __init__(self, logicGateVM: LogicGateVM, settings: GateItemSettings = GateItemSettings.default()):
        super().__init__(logicGateVM)
        self._importSettings(settings)

        self.setPos(self._componentVM.pos)
        self.setFlags(
            QGraphicsRectItem.ItemIsSelectable |
            QGraphicsRectItem.ItemIsMovable | # we don't set the flag selectable, because we implement our own logic
            QGraphicsRectItem.ItemSendsGeometryChanges
        )
        self.setAcceptHoverEvents(True)
        self.setZValue(1)
        
        self._dragStartPos = None  #for movement tracking
        self.initPinItems()

    def _importSettings(self, settings: GateItemSettings):
        size = settings.SIZE
        self._rect = QRectF(
            -size.width() / 2,
            -size.height() / 2,
            size.width(),
            size.height()
        )
        self._font = QFont()
        self._font.setPointSize(settings.FONT_SIZE)
        self._pen = QPen(settings.BORDER_COLOR, settings.BORDER_WIDTH)
        self._textPen = QPen(settings.TEXT_COLOR)
        self._color = settings.COLOR
        self._selectedColor = settings.SELECTED_COLOR
        self._brush = self._color
    
    def boundingRect(self) -> QRectF:
        return self._rect.adjusted(-1, -1, 1, 1)
    
    def shape(self) -> QPainterPath:
        path = QPainterPath()
        path.addRect(self._rect)
        return path
    
    @property
    def rect(self) -> QRectF:
        return self._rect

    def paint(self, painter: QPainter, option, widget=None):
        painter.setRenderHints(QPainter.Antialiasing)
        painter.setBrush(self._brush)
        painter.setPen(self._pen)
        painter.drawRect(self._rect)

        painter.setFont(self._font)
        painter.setPen(self._textPen)
        gate_type = type(self._componentVM.component).__name__
        painter.drawText(self.rect, Qt.AlignCenter, gate_type)