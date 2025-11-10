from PySide6.QtGui import QFont, QPen, QPainter
from PySide6.QtCore import Qt, Signal, QPointF, QObject, QRectF

from view.PinItem import InputPinItem, OutputPinItem
from viewmodel.CircuitComponentVM import CircuitComponentVM
from view.CircuitComponentItem import CircuitComponentItem
from view.settings.LogicGateItem import LogicGateItemSettings

from typing import List

class LogicGateItem(CircuitComponentItem):
    
    def __init__(self, id : str, type : str, pos : QPointF, inputPinIds : List[str], outputPinIds : List[str], settings: LogicGateItemSettings = LogicGateItemSettings.default()):
        super().__init__(id, type, pos, inputPinIds, outputPinIds, settings)

    def paint(self, painter: QPainter, option, widget=None):
        painter.setRenderHints(QPainter.Antialiasing)
        painter.setBrush(self._brush)
        painter.setPen(self._pen)
        painter.drawRect(self._rect)
        painter.setFont(self._font)
        painter.setPen(self._textPen)
        painter.drawText(self._rect, Qt.AlignCenter, self._type)
    
    def clone(self):
        clone = LogicGateItem(self._id, self._type, self.pos(), list(self.inputPinItems.keys()), list(self.outputPinItems.keys()), self._settings)
        return clone
    
    def ghost(self):
        ghost = self.clone()
        ghost.setOpacity(0.5)
        ghost.setZValue(self.zValue() + 1)
        return ghost