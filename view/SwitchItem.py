from typing import List
from PySide6.QtGui import QPainter
from PySide6.QtCore import QRectF, Qt, Slot, QPointF, Signal
from PySide6.QtWidgets import QGraphicsItem, QGraphicsObject
from view.CircuitComponentItem import CircuitComponentItem
from view.settings.SwitchItem import SwitchItemSettings

class SwitchItem(CircuitComponentItem):
    """Graphical representation of a switch component on the canvas.

    This class extends CircuitComponentItem to visualize a toggleable switch,
    including its pins and state-dependent color. It also emits a signal
    when the user requests a toggle by clicking on the switch.

    Signals:
        toggleRequested (str): Emitted when the switch is clicked. Carries the switch's ID.
    """
    
    toggleRequested = Signal(str)
    
    def __init__(self, id: str, type: str, pos: QPointF, inputPinIds: List[str], outputPinIds: List[str], value: bool, settings: SwitchItemSettings = SwitchItemSettings.default()):
        """Initialize a SwitchItem.

        Args:
            id (str): Unique identifier of the switch.
            type (str): Component type string ("Switch").
            pos (QPointF): Position on the canvas.
            inputPinIds (List[str]): IDs of input pins (usually empty for a switch).
            outputPinIds (List[str]): IDs of output pins.
            value (bool): Initial state of the switch (on/off).
            settings (SwitchItemSettings, optional): Visual settings for the switch.
        """
        super().__init__(id, type, pos, inputPinIds, outputPinIds, value, settings)
        self._importSettings(settings)
    
    def _importSettings(self, settings: SwitchItemSettings):
        """Load visual settings specific to the switch."""
        super()._importSettings(settings)
        self._settings = settings
        self._onColor = settings.ON_COLOR
        self._draggingColor = settings.DRAGGING_COLOR
    
    def paint(self, painter: QPainter, option, widget=None):
        """Paint the switch rectangle with appropriate color and text.

        Args:
            painter (QPainter): Qt painter object.
            option: QStyleOptionGraphicsItem (unused).
            widget: QWidget (unused).
        """
        painter.setRenderHints(QPainter.Antialiasing)
        painter.setBrush(self._brush)
        if self._isGhost:
            # Use ghost color when dragging
            painter.setBrush(self._draggingColor)
        painter.setPen(self._pen)
        painter.drawRect(self._rect)
        painter.setFont(self._font)
        painter.setPen(self._textPen)
        painter.drawText(self._rect, Qt.AlignCenter, self._type)
    
    def updateVisuals(self, newValue: bool):
        """Update the switch's fill color based on its on/off state."""
        self._brush = self._onColor if newValue else self._color
    
    def clone(self):
        """Return a copy of this switch item for duplication purposes."""
        clone = SwitchItem(
            self._id,
            self._type,
            self.pos(),
            list(self.inputPinItems.keys()),
            list(self.outputPinItems.keys()),
            self._settings
        )
        return clone
    
    def ghost(self):
        """Return a semi-transparent 'ghost' version of this switch for dragging."""
        ghost = self.clone()
        ghost._isGhost = True
        ghost.setOpacity(0.5)
        ghost.setZValue(self.zValue() + 1)
        return ghost
    
    def mousePressEvent(self, event):
        """Handle mouse click events to emit toggleRequested signal on left click."""
        if event.button() == Qt.LeftButton:
            self.toggleRequested.emit(self._id)
        super().mousePressEvent(event)
    
    def itemChange(self, change, value):
        """Handle item changes (selection, movement, etc.)."""
        return QGraphicsObject.itemChange(self, change, value)