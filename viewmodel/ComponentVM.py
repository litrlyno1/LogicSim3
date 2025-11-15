from PySide6.QtCore import QObject, QPointF, Signal

from core.idGenerator import generateId
from model.Component import Component

from viewmodel.Movable import Movable

class ComponentVM(Movable):
    """View-model representation of a circuit component.

    ``ComponentVM`` acts as the visual or interactive layer for a
    :class:`Component` model object. It assigns a unique ID, tracks the
    component's position in the UI, and exposes component metadata such as
    its type.

    It inherits from :class:`Movable`, which provides movement behavior and
    position handling for visual elements.
    """

    def __init__(self, component: Component, pos: QPointF, **kwargs):
        """Initialize a ComponentVM.

        Args:
            component (Component): The underlying logic/model component this
                view-model represents.
            pos (QPointF): Initial position of the component in the UI.
            **kwargs: Additional keyword arguments passed to ``Movable``.
        """
        self._component = component
        self._id = generateId(prefix=self.type)
        super().__init__(id=self._id, pos=pos, **kwargs)

    @property
    def type(self):
        """str: The type of the underlying component."""
        return self._component.type

    @property
    def id(self):
        """str: Unique identifier assigned to this view-model instance."""
        return self._id