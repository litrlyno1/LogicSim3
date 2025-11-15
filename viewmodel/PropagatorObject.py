from viewmodel.PropagatorRelay import PropagatorRelay
from model.Propagator import Propagator

class PropagatorObject:
    """Mixin that exposes propagator value-change notifications.

    ``PropagatorObject`` gives a view-model class the ability to react to
    model-side propagator updates through Qt signals. It internally creates
    a :class:`PropagatorRelay` that receives updates and emits ``valueChanged``.
    """

    def __init__(self, id: str, propagator: Propagator, **kwargs):
        """Initialize the propagator-enabled object.

        Args:
            id (str): Unique identifier of the parent object.
            propagator (Propagator): The propagator providing updates.
            **kwargs: Forwarded to the next class in the MRO.
        """
        self._propagatorRelay = PropagatorRelay(id, propagator)
        super().__init__(**kwargs)

    @property
    def valueChanged(self):
        """Signal. Emits valueChange when the propagator updates."""
        return self._propagatorRelay.valueChanged