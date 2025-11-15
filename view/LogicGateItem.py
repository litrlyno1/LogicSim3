from PySide6.QtGui import QPainter
from PySide6.QtCore import Qt, QPointF

from view.CircuitComponentItem import CircuitComponentItem
from view.settings.LogicGateItem import LogicGateItemSettings

from typing import List

class LogicGateItem(CircuitComponentItem):
    """Graphical representation of a logic gate in the circuit canvas.

    Extends CircuitComponentItem to provide rendering specific to logic gates,
    including visual painting of the gate rectangle, type label, and support
    for cloning and ghost previews (semi-transparent copies for drag-and-drop).
    """

    def __init__(self, id: str, type: str, pos: QPointF,
                inputPinIds: List[str], outputPinIds: List[str],
                settings: LogicGateItemSettings = LogicGateItemSettings.default()):
        """Initialize the logic gate item.

        Args:
            id (str): Unique identifier for the gate.
            type (str): Gate type (e.g., "AndGate", "OrGate").
            pos (QPointF): Initial position on the scene.
            inputPinIds (List[str]): IDs for input pins.
            outputPinIds (List[str]): IDs for output pins.
            settings (LogicGateItemSettings, optional): Visual settings for the gate.
        """
        super().__init__(id, type, pos, inputPinIds, outputPinIds, settings)

    def paint(self, painter: QPainter, option, widget=None):
        """Paint the gate rectangle and type label.

        Args:
            painter (QPainter): The painter object used for drawing.
            option: QStyleOptionGraphicsItem (unused here).
            widget: Optional widget context (unused).
        """
        painter.setRenderHints(QPainter.Antialiasing)
        # Draw background rectangle
        painter.setBrush(self._brush)
        painter.setPen(self._pen)
        painter.drawRect(self._rect)
        # Draw type label
        painter.setFont(self._font)
        painter.setPen(self._textPen)
        painter.drawText(self._rect, Qt.AlignCenter, self._type)

    def clone(self):
        """Create a full copy of this logic gate item.

        Returns:
            LogicGateItem: New instance with same ID, type, position, pins, and settings.
        """
        clone = LogicGateItem(
            self._id,
            self._type,
            self.pos(),
            list(self.inputPinItems.keys()),
            list(self.outputPinItems.keys()),
            self._settings
        )
        return clone

    def ghost(self):
        """Create a semi-transparent "ghost" copy of this logic gate for drag-and-drop.

        Returns:
            LogicGateItem: Ghost copy with 50% opacity and slightly higher Z-value.
        """
        ghost = self.clone()
        ghost.setOpacity(0.5)
        ghost.setZValue(self.zValue() + 1)
        return ghost