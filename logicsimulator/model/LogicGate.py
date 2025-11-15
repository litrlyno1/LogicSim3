from logicsimulator.model.CircuitComponent import CircuitComponent

class LogicGate(CircuitComponent):
    """Base class for all logic gates in the circuit system.

    ``LogicGate`` extends :class:`CircuitComponent` and serves as the abstract
    parent class for specific boolean logic gates such as AND, OR, XOR, and NOT.
    It provides no additional behavior beyond what ``CircuitComponent`` defines,
    but acts as a semantic grouping for all gate-type components.
    """

    def __init__(self):
        """Initialize the logic gate and create its input/output pins."""
        super().__init__()