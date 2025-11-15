from PySide6.QtWidgets import QGraphicsObject, QGraphicsItem
from PySide6.QtCore import Qt, QPointF, Signal, QRect
from PySide6.QtGui import QPen, QPainter

from logicsimulator.view.settings.PinItem import PinItemSettings, InputPinItemSettings, OutputPinItemSettings

class PinItem(QGraphicsObject):
    """Graphical representation of a pin attached to a circuit component.

    PinItem is a base class for input and output pins displayed on a component.
    It handles selection, visual appearance, and signals for movement or selection.
    """
    parentMoved = Signal(QPointF)
    """Signal emitted when the parent component moves. Emits the new position."""

    selected = Signal(str)
    """Signal emitted when this pin is selected. Emits the pin ID."""

    def __init__(self, parentItem: "CircuitComponentItem", id: str, relativePos: QPointF, settings: PinItemSettings = PinItemSettings.default()):
        """Initialize a pin item.

        Args:
            parentItem (CircuitComponentItem): The parent component item.
            id (str): Unique identifier for this pin.
            relativePos (QPointF): Position relative to parent component.
            settings (PinItemSettings, optional): Visual appearance settings.
        """
        self._importSettings(settings)
        super().__init__()
        self._id = id
        self.setParentItem(parentItem)
        parentItem.moved.connect(lambda pos: self.parentMoved.emit(pos))
        parentItem.selected.connect(lambda val: self.setParentSelected(val))
        self._setupGraphics(relativePos)
        self.setFlags(QGraphicsObject.ItemIsSelectable)
        self._parentSelected = parentItem.isSelected()

    def _importSettings(self, settings: PinItemSettings):
        """Load visual appearance settings from a PinItemSettings object."""
        self._radius = settings.RADIUS
        self._color = settings.COLOR
        self._parentSelectedColor = settings.PARENT_SELECTED_COLOR
        self._selectedColor = settings.SELECTED_COLOR
        self._draggingColor = settings.DRAGGING_COLOR
        self._borderColor = settings.BORDER_COLOR
        self._borderWidth = settings.BORDER_WIDTH

    def _setupGraphics(self, relativePos: QPointF):
        """Initialize graphics properties and set relative position."""
        self._rect = QRect(-self._radius, -self._radius, 2*self._radius, 2*self._radius)
        self.setPos(relativePos)
        self._brush = self._color
        self._pen = QPen(self._borderColor, self._borderWidth)
        self.setZValue(1)
        self.setAcceptHoverEvents(True)
        self.setAcceptedMouseButtons(Qt.LeftButton)

    def boundingRect(self):
        """Return the bounding rectangle for this pin."""
        return self._rect

    @property
    def center(self) -> QPointF:
        """Return the scene coordinates of the pin center."""
        return self.sceneBoundingRect().center()

    @property
    def type(self) -> str:
        """Return the type of pin. Must be implemented by subclasses."""
        raise NotImplementedError("Pin subclasses must define their type")

    @property
    def id(self):
        """Return the unique ID of this pin."""
        return self._id

    def setSelected(self, value: bool) -> None:
        """Update selection state and adjust brush color.

        Args:
            value (bool): True if selected, False otherwise.
        """
        super().setSelected(value)
        if value:
            self.selected.emit(self._id)
            self._brush = self._selectedColor
        else:
            self._brush = self._parentSelectedColor if self.parentSelected else self._color
        self.update()

    @property
    def parentSelected(self) -> bool:
        """Return whether the parent component is selected."""
        return self._parentSelected

    def setParentSelected(self, value: bool):
        """Update visual color based on parent selection state."""
        self._parentSelected = value
        self._brush = self._parentSelectedColor if value else self._color
        self.update()

    def paint(self, painter: QPainter, option, widget=None):
        """Paint the pin as a colored ellipse."""
        painter.setBrush(self._brush)
        painter.setPen(self._pen)
        painter.drawEllipse(self._rect)

    def itemChange(self, change, value):
        """Override to handle selection changes."""
        if change == QGraphicsItem.ItemSelectedHasChanged:
            self.setSelected(value)
        return super().itemChange(change, value)


class InputPinItem(PinItem):
    """Graphical representation of an input pin."""

    def __init__(self, parentItem: "CircuitComponentItem", id: str, relativePos: QPointF, settings: PinItemSettings = InputPinItemSettings.default()):
        """Initialize an input pin item with default input pin settings."""
        super().__init__(parentItem, id, relativePos, settings)


class OutputPinItem(PinItem):
    """Graphical representation of an output pin."""

    def __init__(self, parentItem: "CircuitComponentItem", id: str, relativePos: QPointF, settings: PinItemSettings = OutputPinItemSettings.default()):
        """Initialize an output pin item with default output pin settings."""
        super().__init__(parentItem, id, relativePos, settings)