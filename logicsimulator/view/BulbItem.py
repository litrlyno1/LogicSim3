from typing import List
from PySide6.QtGui import QPainter
from PySide6.QtCore import QRectF, Qt, Slot, QPointF, Signal
from PySide6.QtWidgets import QGraphicsObject
from logicsimulator.view.CircuitComponentItem import CircuitComponentItem
from logicsimulator.view.settings.BulbItem import BulbItemSettings

class BulbItem(CircuitComponentItem):
    """Graphical representation of a Bulb component on the canvas.

    This class extends CircuitComponentItem to visualize a bulb, including its pins
    and state-dependent color (on/off). Supports cloning and ghosting for drag-and-drop.

    Methods:
        updateVisuals(newValue: bool): Updates the visual color of the bulb based on its state.
        clone(): Returns a full copy of the BulbItem.
        ghost(): Returns a semi-transparent 'ghost' version of the BulbItem.
    """
    
    def __init__(self, id: str, type:str, pos: QPointF, inputPinIds: List[str], outputPinIds: List[str], value: bool, settings: BulbItemSettings = BulbItemSettings.default()):
        """Initialize a BulbItem.

        Args:
            id (str): Unique identifier for the bulb.
            type (str): Component type string ("Bulb").
            pos (QPointF): Position on the canvas.
            inputPinIds (List[str]): List of input pin IDs.
            outputPinIds (List[str]): List of output pin IDs (usually empty for bulbs).
            value (bool): Initial state of the bulb (on/off).
            settings (BulbItemSettings, optional): Visual settings for the bulb.
        """
        super().__init__(id=id, type=type, pos=pos, inputPinIds=inputPinIds, outputPinIds=outputPinIds, value=value, settings=settings)
        self._importSettings(settings)
    
    def _importSettings(self, settings: BulbItemSettings):
        """Load visual settings specific to the bulb."""
        super()._importSettings(settings)
        self._settings = settings
        self._onColor = settings.ON_COLOR
        self._draggingColor = settings.DRAGGING_COLOR
    
    def paint(self, painter: QPainter, option, widget=None):
        """Paint the bulb as a colored ellipse with centered text.

        Args:
            painter (QPainter): Qt painter object.
            option: QStyleOptionGraphicsItem (unused).
            widget: QWidget (unused).
        """
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
        """Update the bulb's color based on its current on/off state.

        Args:
            newValue (bool): True if bulb is on, False if off.
        """
        self._brush = self._onColor if newValue else self._color
    
    def clone(self):
        """Return a copy of this bulb item for duplication purposes."""
        clone = BulbItem(
            self._id,
            self._type,
            self.pos(),
            list(self.inputPinItems.keys()),
            list(self.outputPinItems.keys()),
            self._settings
        )
        return clone
    
    def ghost(self):
        """Return a semi-transparent 'ghost' version of this bulb for dragging."""
        ghost = self.clone()
        ghost._isGhost = True
        ghost.setOpacity(0.5)
        ghost.setZValue(self.zValue() + 1)
        return ghost
    
    def itemChange(self, change, value):
        """Handle item changes (selection, movement, etc.)."""
        return QGraphicsObject.itemChange(self, change, value)