from typing import List

from PySide6.QtGui import QPainter
from PySide6.QtCore import QRectF, Qt, Slot, QPointF, Signal
from PySide6.QtWidgets import QGraphicsObject
from view.CircuitComponentItem import CircuitComponentItem
from view.settings.BulbItem import BulbItemSettings

class BulbItem(CircuitComponentItem):
    
    def __init__(self, id: str, type:str, pos: QPointF, inputPinIds: List[str], outputPinIds: List[str], value: bool, settings: BulbItemSettings = BulbItemSettings.default()):
        super().__init__(id = id, type = type, pos = pos, inputPinIds = inputPinIds, outputPinIds= outputPinIds, value=value, settings=settings)
        self._importSettings(settings)
    
    def _importSettings(self, settings: BulbItemSettings):
        super()._importSettings(settings)
        self._settings = settings
        self._onColor = settings.ON_COLOR
        self._draggingColor = settings.DRAGGING_COLOR
    
    def paint(self, painter: QPainter, option, widget=None):
        painter.setRenderHints(QPainter.Antialiasing)
        painter.setBrush(self._brush)
        if self._isGhost:
            painter.setBrush(self._draggingColor)
        painter.setPen(self._pen)
        painter.drawEllipse(self._rect)
        painter.setFont(self._font)
        painter.setPen(self._textPen)
        painter.drawText(self._rect, Qt.AlignCenter, self._type)
    
    def updateVisuals(self, newValue: bool):
        self._brush = self._onColor if newValue else self._color
    
    def clone(self):
        clone = BulbItem(self._id, self._type, self.pos(), list(self.inputPinItems.keys()), list(self.outputPinItems.keys()), self._settings)
        return clone
    
    def ghost(self):
        ghost = self.clone()
        ghost._isGhost = True
        ghost.setOpacity(0.5)
        ghost.setZValue(self.zValue() + 1)
        return ghost
    
    def itemChange(self, change, value):
        return QGraphicsObject.itemChange(self, change, value)