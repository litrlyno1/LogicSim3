from PySide6.QtWidgets import QGraphicsObject, QGraphicsItem
from PySide6.QtCore import Qt, Signal, QPointF, QRectF
from PySide6.QtGui import QFont, QPen

from logicsimulator.view.settings.ComponentItem import ComponentItemSettings

class ComponentItem(QGraphicsObject):
    """Graphical representation of a circuit component in the QGraphicsScene.

    ``ComponentItem`` wraps a component for rendering and interaction in the
    canvas. It handles selection, movement, and appearance based on
    settings. Signals are emitted on movement or selection changes.
    """

    #: Emitted when the item is moved. Args: new position (QPointF)
    moved = Signal(QPointF)

    #: Emitted when the item is selected or deselected. Args: is selected (bool)
    selected = Signal(bool)

    def __init__(self, id: str, type: str, pos: QPointF, isGhost: bool = False,
                 settings: ComponentItemSettings = ComponentItemSettings.default()):
        """Initialize the component item.

        Args:
            id (str): Unique identifier for the component.
            type (str): Type name of the component.
            pos (QPointF): Initial position in the scene.
            isGhost (bool, optional): If True, render as a semi-transparent ghost. Defaults to False.
            settings (ComponentItemSettings, optional): Visual settings to use. Defaults to default settings.
        """
        super().__init__()
        self._type = type
        self._id = id
        self._isGhost = isGhost

        # Enable selection and geometry change notifications
        self.setFlags(
            QGraphicsItem.ItemIsSelectable |
            QGraphicsItem.ItemSendsGeometryChanges
        )

        # Load appearance settings
        self._importSettings(settings)

        # Set initial position
        self.setPos(pos)

        # Enable hover events for interactive feedback
        self.setAcceptHoverEvents(True)

        # Render on top of most items
        self.setZValue(3)

        # Accept only left mouse button interactions
        self.setAcceptedMouseButtons(Qt.LeftButton)

    def _importSettings(self, settings: ComponentItemSettings):
        """Load and apply visual settings to the item.

        Args:
            settings (ComponentItemSettings): Settings object containing size, colors, fonts, etc.
        """
        self._settings = settings    
        size = settings.SIZE
        # Center the rectangle on the origin
        self._rect = QRectF(
            -size.width() / 2,
            -size.height() / 2,
            size.width(),
            size.height()
        )
        # Font
        self._font = QFont()
        self._fontSize = settings.FONT_SIZE
        self._font.setPointSize(self._fontSize)
        # Border
        self._borderColor = settings.BORDER_COLOR
        self._borderWidth = settings.BORDER_WIDTH
        self._pen = QPen(self._borderColor, self._borderWidth)
        # Text
        self._textColor = settings.TEXT_COLOR
        self._textPen = QPen(self._textColor)
        # Fill color
        self._color = settings.COLOR
        self._selectedColor = settings.SELECTED_COLOR
        self._brush = self._color

    @property
    def id(self) -> str:
        """str: Unique ID of the component."""
        return self._id

    @property
    def type(self) -> str:
        """str: Type name of the component."""
        return self._type

    @property
    def height(self) -> float:
        """float: Height of the component rectangle."""
        return self._rect.height()

    @property
    def width(self) -> float:
        """float: Width of the component rectangle."""
        return self._rect.width()

    def boundingRect(self) -> QRectF:
        """QRectF: Return the bounding rectangle for QGraphicsScene rendering."""
        return self._rect.adjusted(-1, -1, 1, 1)

    @property
    def rect(self) -> QRectF:
        """QRectF: Rectangle representing the component's size and position."""
        return self._rect

    def setPos(self, pos: QPointF):
        """Set the item’s position and emit the moved signal.

        Args:
            pos (QPointF): New position.
        """
        super().setPos(pos)
        self.moved.emit(pos)

    def itemChange(self, change, value):
        """Handle item state changes such as selection.

        Args:
            change: Type of change (QGraphicsItem.GraphicsItemChange)
            value: New value associated with the change

        Returns:
            The processed value to pass to the base class.
        """
        if change == QGraphicsItem.ItemSelectedChange:
            # Change the brush color when selected/deselected
            self._brush = self._selectedColor if value else self._color
            self.update()
            # Emit selection signal
            self.selected.emit(value)
        return super().itemChange(change, value)