from PySide6.QtGui import QPen, QPainterPath
from PySide6.QtWidgets import QGraphicsPathItem, QGraphicsItem, QGraphicsObject
from PySide6.QtCore import Qt, QPointF, Signal

from logicsimulator.view.PinItem import PinItem
from logicsimulator.view.settings.ConnectionItem import ConnectionItemSettings

class ConnectionItem(QGraphicsObject):
    """Represents a visual connection (wire) between two pins in the GUI.

    This item manages a cubic Bézier path that visually connects two PinItems.
    Supports selection highlighting and ghosting.
    """
    
    removed = Signal(str)      # Emitted when this connection is removed
    valueChanged = Signal(str) # Emitted when the logical value of the connection changes

    class CubicPath(QGraphicsPathItem):
        """Internal class representing the cubic Bézier path for the connection."""

        def __init__(self, start: QPointF, end: QPointF, settings: ConnectionItemSettings = ConnectionItemSettings.default()):
            """Initialize the cubic path with start and end points."""
            super().__init__()
            self._start = start
            self._end = end
            self._importSettings(settings)
            self._setupGraphics()
        
        def _importSettings(self, settings: ConnectionItemSettings):
            """Load visual settings such as color, width, and selection color."""
            self._settings = settings
            self._color = settings.COLOR
            self._selectedColor = settings.SELECTED_COLOR
            self._onColor = settings.ON_COLOR
            self._width = settings.WIDTH
        
        def _setupGraphics(self):
            """Configure the QPen and initial path."""
            self._pen = QPen(self._color, self._width)
            self._pen.setCapStyle(Qt.RoundCap)
            self.setPen(self._pen)
            self.setZValue(1)
            self._updatePath()
        
        @property
        def start(self):
            return self._start

        @start.setter
        def start(self, newStart: QPointF):
            """Update start point and recompute the path."""
            self._start = newStart
            self._updatePath()

        @property
        def end(self):
            return self._end

        @end.setter
        def end(self, newEnd: QPointF):
            """Update end point and recompute the path."""
            self._end = newEnd
            self._updatePath()

        def _updatePath(self):
            """Compute the cubic Bézier path between start and end points."""
            path = QPainterPath(self._start)
            dx = (self._end.x() - self._start.x()) * 0.5
            controlPoint1 = QPointF(self._start.x() + dx, self._start.y())
            controlPoint2 = QPointF(self._end.x() - dx, self._end.y())
            path.cubicTo(controlPoint1, controlPoint2, self._end)
            self.setPath(path)
        
        def clone(self):
            """Return a copy of this path."""
            clone = ConnectionItem.CubicPath(self._start, self._end, self._settings)
            return clone
    
        def ghost(self):
            """Return a semi-transparent ghost version of this path."""
            ghost = self.clone()
            ghost.setOpacity(0.5)
            ghost.setZValue(self.zValue() + 1)
            return ghost
    
    def __init__(self, id: str, pinItem1: PinItem, pinItem2: PinItem, settings: ConnectionItemSettings = ConnectionItemSettings.default()):
        """Initialize a connection between two PinItems."""
        super().__init__()
        self._id = id
        self._path = ConnectionItem.CubicPath(pinItem1.center, pinItem2.center, settings)
        self._path.setParentItem(self)

        # Update path if parent pins move
        pinItem1.parentMoved.connect(lambda: self.updateStart(pinItem1.center))
        pinItem2.parentMoved.connect(lambda: self.updateEnd(pinItem2.center))

        # Enable selection and geometry notifications
        self.setFlags(
            QGraphicsItem.ItemIsSelectable |
            QGraphicsItem.ItemSendsGeometryChanges
        )
    
    @property
    def id(self):
        return self._id
    
    def updateStart(self, pos: QPointF):
        """Update the start point of the path."""
        self._path.start = pos
    
    def updateEnd(self, pos: QPointF):
        """Update the end point of the path."""
        self._path.end = pos

    def boundingRect(self):
        """Return the bounding rectangle of the path for rendering."""
        return self._path.boundingRect()

    def paint(self, painter, option, widget=None):
        """No custom painting needed; the CubicPath handles drawing."""
        pass
    
    def shape(self):
        """Return the QPainterPath representing the connection shape for interaction."""
        return self._path.shape()
    
    def itemChange(self, change, value):
        """Handle selection changes to update path color."""
        if change == QGraphicsItem.ItemSelectedHasChanged:
            if value:
                self._path._pen.setColor(self._path._selectedColor)
            else:
                self._path._pen.setBrush(self._path._color)
            self._path.setPen(self._path._pen)
            self.update()
        return super().itemChange(change, value)