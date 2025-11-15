from logicsimulator.viewmodel.CircuitComponentVM import CircuitComponentVM
from logicsimulator.viewmodel.Toggleable import Toggleable

from PySide6.QtCore import QPointF

class SwitchVM(CircuitComponentVM, Toggleable):
    """View-model representation of a Switch component.

    ``SwitchVM`` acts as the UI-side wrapper for a model‐side
    :class:`Switch` circuit component. It exposes toggle behavior to the
    view layer through the :class:`Toggleable` interface, and inherits
    pin/view-model behavior from :class:`CircuitComponentVM`.
    """

    type = "Switch"

    def __init__(self, circuitComponent: "Switch", pos: QPointF):
        """Initialize the Switch view-model.

        Args:
            circuitComponent (Switch): The underlying switch logic component.
            pos (QPointF): Initial position of the view-model element.
        """
        super().__init__(circuitComponent, pos)

    def toggle(self):
        """Toggle the underlying switch component.

        This calls the model's ``toggle`` method, which updates the
        component's internal value and triggers propagation.
        """
        self._component.toggle()