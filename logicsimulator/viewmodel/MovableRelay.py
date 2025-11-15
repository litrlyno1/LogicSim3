from logicsimulator.viewmodel.ObjectProperty import ObjectProperty
from PySide6.QtCore import QPointF, Signal

class MovableRelay(ObjectProperty):
    """Relay object responsible for tracking and emitting movement updates.

    ``MovableRelay`` stores the position of a parent object and emits
    a signal whenever that position changes. This separates movement
    behavior from the main view-model class, allowing better decoupling.
    """

    #: Signal emitted when the object's position changes.
    #: Args:
    #:     str: The ID of the parent object.
    #:     QPointF: The new position.
    posChanged = Signal(str, QPointF)

    def __init__(self, parentId: str, pos: QPointF):
        """Initialize the relay.

        Args:
            parentId (str): The ID of the object that owns this relay.
            pos (QPointF): The initial position.
        """
        super().__init__(parentId)
        self._pos = pos

    @property
    def pos(self) -> QPointF:
        """QPointF: Current stored position of the parent object."""
        return self._pos

    @pos.setter
    def pos(self, pos: QPointF):
        """Set a new position and emit a notification signal."""
        self._pos = pos
        self.posChanged.emit(self._parentId, pos)