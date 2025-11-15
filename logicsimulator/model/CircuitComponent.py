from abc import ABC, abstractmethod
from typing import List, Optional, Set

from logicsimulator.model.Component import Component
from logicsimulator.model.Propagator import Propagator
from logicsimulator.model.Pin import InputPin, OutputPin

class CircuitComponent(Component, Propagator, ABC):
    """Abstract base class for components that participate in logic circuits.

    It defines a common interface for circuit components that have a fixed number
    of input and output pins and propagate their signal (True/False) forward.

    Subclasses must implement :attr:`numInputs` and :attr:`numOutputs`, which
    determine how many :class:`InputPin` and :class:`OutputPin` objects are
    created for the component.

    Attributes:
        inputPins (Optional[List[InputPin]]): A list of all input pins, or
            ``None`` if the component has zero inputs.
        outputPins (Optional[List[OutputPin]]): A list of all output pins, or
            ``None`` if the component has zero outputs.
    """
    
    def __init__(self):
        """Initialize the component and create its input and output pins."""
        super().__init__()
        self._inputPins = self._createInputPins(self.numInputs)
        self._outputPins = self._createOutputPins(self.numOutputs)
    
    @property
    @abstractmethod
    def numInputs(self) -> int:
        """Number of input pins the component should have.

        Returns:
            int: The number of input pins.
        """
        pass
    
    @property
    @abstractmethod
    def numOutputs(self) -> int:
        """Number of output pins the component should have.

        Returns:
            int: The number of output pins.
        """
        pass
    
    def _createInputPins(self, numInputs : int) -> Optional[List[InputPin]]:
        """Create the list of input pins for the component.

        Args:
            numInputs (int): Number of input pins to create.

        Returns:
            Optional[List[InputPin]]: A list of input pins, or ``None`` if
            ``numInputs`` is zero.
        """
        if numInputs == 0:
            return None
        else:
            pins = []
            for _ in range(numInputs):
                pins.append(InputPin(parent = self))
            return pins
    
    def _createOutputPins(self, numOutputs : int) -> Optional[List[OutputPin]]:
        """Create the list of output pins for the component.

        Args:
            numOutputs (int): Number of output pins to create.

        Returns:
            Optional[List[OutputPin]]: A list of output pins, or ``None`` if
            ``numOutputs`` is zero.
        """
        if numOutputs == 0:
            return None
        else:
            pins = []
            for _ in range(numOutputs):
                pins.append(OutputPin(parent = self))
            return pins
    
    @property
    def inputPins(self):
        """Access the component's input pins.

        Returns:
            Optional[List[InputPin]]: All input pins, or ``None`` if none exist.
        """
        return self._inputPins
    
    @property
    def outputPins(self):
        """Access the component's output pins.

        Returns:
            Optional[List[OutputPin]]: All output pins, or ``None`` if none exist.
        """
        return self._outputPins
    
    def precedes(self, circuitComponent : "CircuitComponent") -> bool:
        """Determine whether this component precedes another in the propagation graph.

        This performs a depth-first search starting from ``self`` and follows all
        propagator observers to determine whether ``self`` eventually leads to
        ``circuitComponent``. Components do not precede themselves.

        Args:
            circuitComponent (CircuitComponent): The component to test reachability to.

        Returns:
            bool: ``True`` if this component precedes ``circuitComponent`` in the
            propagation graph, ``False`` otherwise.
        """
        if self == circuitComponent:
            return False
        else: 
            start = self
            end = circuitComponent
            visited : Set[Propagator] = set()
            
            def dfs(current : Propagator):
                if current == end:
                    return True
                visited.add(current)
                for observer in current._observers:
                    if isinstance(observer, CircuitComponent):
                        if observer not in visited:
                            if dfs(observer):
                                return True
                return False
            
            return dfs(start)