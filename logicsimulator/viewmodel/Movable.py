from logicsimulator.viewmodel.MovableRelay import MovableRelay
from PySide6.QtCore import QPointF

class Movable:
    """Mixin that provides movement functionality to a view-model object.

    ``Movable`` wraps position handling inside a :class:`MovableRelay`,
    exposing position accessors and movement signals while keeping the
    component's main inheritance tree clean.
    """

    def __init__(self, id: str, pos: QPointF, **kwargs):
        """Initialize the movable mixin.

        Args:
            id (str): Unique identifier of the object.
            pos (QPointF): Initial position of the object.
            **kwargs: Forwarded to the next class in the MRO.
        """
        self._movableRelay = MovableRelay(id, pos)
        super().__init__(id=id, **kwargs)

    @property
    def pos(self) -> QPointF:
        """QPointF: Current position of the object."""
        return self._movableRelay.pos

    @pos.setter
    def pos(self, pos: QPointF):
        """Update the position of the object."""
        self._movableRelay.pos = pos

    @property
    def posChanged(self):
        """Signal: Emits when the object's position changes."""
        return self._movableRelay.posChanged