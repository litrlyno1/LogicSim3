from typing import Literal
from model.CircuitComponent import CircuitComponent

class Switch(CircuitComponent):
    """A circuit component representing a boolean switch.

    The ``Switch`` has no input pins and a single output pin. Its value is
    manually toggled by the user rather than computed from other components.
    When toggled, the switch propagates its updated value through the circuit.
    """

    type = "Switch"
    numInputs = 0
    numOutputs = 1

    def __init__(self):
        """Initialize the switch with its default value (False)."""
        super().__init__()

    def toggle(self) -> None:
        """Toggle the switch's boolean state and propagate the change.

        The switch alternates between ``True`` (on) and ``False`` (off) each time
        this method is called. After updating its value, the switch notifies
        downstream components by invoking :meth:`update`.
        """
        self._value = not self._value
        self.update()

    def _evaluate(self) -> None:
        """Evaluation hook for the switch.

        The switch's value is controlled manually via :meth:`toggle`, so this
        method does nothing.
        """
        pass