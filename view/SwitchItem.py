from typing import List

from PySide6.QtGui import QPainter
from PySide6.QtCore import QRectF, Qt, Slot, QPointF, Signal
from PySide6.QtWidgets import QGraphicsItem, QGraphicsObject
from view.CircuitComponentItem import CircuitComponentItem
from view.settings.SwitchItem import SwitchItemSettings

class SwitchItem(CircuitComponentItem):
    toggleRequested = Signal(str)
    
    def __init__(self, id: str, type:str, pos: QPointF, inputPinIds: List[str], outputPinIds: List[str], value, settings: SwitchItemSettings = SwitchItemSettings.default()):
        super().__init__(id, type, pos, inputPinIds, outputPinIds, value, settings)
        self._importSettings(settings)
    
    def _importSettings(self, settings: SwitchItemSettings):
        super()._importSettings(settings)
        self._settings = settings
        self._onColor = settings.ON_COLOR
    
    def paint(self, painter: QPainter, option, widget=None):
        painter.setRenderHints(QPainter.Antialiasing)
        painter.setBrush(self._brush)
        painter.setPen(self._pen)
        painter.drawRect(self._rect)
        painter.setFont(self._font)
        painter.setPen(self._textPen)
        painter.drawText(self._rect, Qt.AlignCenter, self._type)
    
    def updateVisuals(self, newValue: bool):
        self._brush = self._onColor if newValue else self._color
    
    def clone(self):
        clone = SwitchItem(self._id, self._type, self.pos(), list(self.inputPinItems.keys()), list(self.outputPinItems.keys()), self._settings)
        return clone
    
    def ghost(self):
        ghost = self.clone()
        ghost.setOpacity(0.5)
        ghost.setZValue(self.zValue() + 1)
        return ghost
    
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.toggleRequested.emit(self._id)
        super().mousePressEvent(event)
    
    def itemChange(self, change, value):
        return QGraphicsObject.itemChange(self, change, value)