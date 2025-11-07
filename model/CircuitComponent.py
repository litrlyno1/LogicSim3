from abc import ABC, abstractmethod
from typing import List, Optional, Set

from model.Component import Component
from model.Propagator import Propagator
from model.Pin import InputPin, OutputPin, Pin

class CircuitComponent(Component, Propagator, ABC):
    
    def __init__(self):
        super().__init__()
        self._inputPins = self._createInputPins(self.numInputs)
        self._outputPins = self._createOutputPins(self.numOutputs)
    
    @property
    @abstractmethod
    def numInputs(self) -> int:
        pass
    
    @property
    @abstractmethod
    def numOutputs(self) -> int:
        pass
    
    def _createInputPins(self, numInputs : int) -> Optional[List[InputPin]]:
        if numInputs == 0:
            return None
        else:
            pins = []
            for _ in range(numInputs):
                pins.append(InputPin(parent = self))
            return pins
    
    def _createOutputPins(self, numOutputs : int) -> Optional[List[OutputPin]]:
        if numOutputs == 0:
            return None
        else:
            pins = []
            for _ in range(numOutputs):
                pins.append(OutputPin(parent = self))
            return pins
    
    @property
    def inputPins(self):
        return self._inputPins
    
    @property
    def outputPins(self):
        return self._outputPins
    
    def precedes(self, circuitComponent : "CircuitComponent") -> bool:
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