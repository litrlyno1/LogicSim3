from logicsimulator.model.CircuitComponent import CircuitComponent

class Bulb(CircuitComponent):
    """A circuit component representing a light bulb.

    The ``Bulb`` has one input pin and no output pins. Its value reflects the
    boolean state of its input. When the input is ``True``, the bulb is
    considered "on"; when ``False``, it is "off".
    """

    type = "Bulb"
    numInputs = 1
    numOutputs = 0

    def __init__(self):
        """Initialize the bulb and create its single input pin."""
        super().__init__()

    def _evaluate(self) -> None:
        """Evaluate the bulb's state.

        The bulb mirrors the value of its single input pin.

        Sets:
            self._value (bool): The current on/off state of the bulb.
        """
        self._value = self._inputPins[0].value