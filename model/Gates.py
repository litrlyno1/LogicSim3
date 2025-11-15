from model.LogicGate import LogicGate

class AndGate(LogicGate):
    """Logic gate implementing boolean AND.

    The ``AndGate`` takes two boolean inputs and produces one boolean output,
    evaluating to ``True`` only if both inputs are ``True``.
    """

    type = "AndGate"
    numInputs = 2
    numOutputs = 1

    def __init__(self):
        """Initialize the AND gate."""
        super().__init__()

    def _evaluate(self) -> None:
        """Evaluate the AND gate output."""
        self._value = self._inputPins[0].value and self._inputPins[1].value


class OrGate(LogicGate):
    """Logic gate implementing boolean OR.

    The ``OrGate`` takes two boolean inputs and produces one boolean output,
    evaluating to ``True`` if at least one input is ``True``.
    """

    type = "OrGate"
    numInputs = 2
    numOutputs = 1

    def __init__(self):
        """Initialize the OR gate."""
        super().__init__()

    def _evaluate(self) -> None:
        """Evaluate the OR gate output."""
        self._value = self._inputPins[0].value or self._inputPins[1].value


class XorGate(LogicGate):
    """Logic gate implementing boolean XOR.

    The ``XorGate`` takes two boolean inputs and produces one boolean output,
    evaluating to ``True`` only if exactly one input is ``True``.
    """

    type = "XorGate"
    numInputs = 2
    numOutputs = 1

    def __init__(self):
        """Initialize the XOR gate."""
        super().__init__()

    def _evaluate(self) -> None:
        """Evaluate the XOR gate output."""
        self._value = (
            (not self._inputPins[0].value and self._inputPins[1].value)
            or (self._inputPins[0].value and not self._inputPins[1].value)
        )

class NotGate(LogicGate):
    """Logic gate implementing boolean NOT.

    The ``NotGate`` takes one boolean input and produces one output that is the
    logical negation of its input.
    """

    type = "NotGate"
    numInputs = 1
    numOutputs = 1

    def __init__(self):
        """Initialize the NOT gate."""
        super().__init__()

    def _evaluate(self) -> None:
        """Evaluate the NOT gate output."""
        self._value = not self._inputPins[0].value