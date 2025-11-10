from typing import List

from PySide6.QtCore import QPointF, Signal, Slot

from model.CircuitComponent import CircuitComponent
from viewmodel.ComponentVM import ComponentVM
from viewmodel.PinVM import PinVM
from viewmodel.PropagatorObject import PropagatorObject

class CircuitComponentVM(ComponentVM, PropagatorObject):
    
    def __init__(self, circuitComponent : CircuitComponent, pos : QPointF):
        super().__init__(component = circuitComponent, pos = pos, propagator = circuitComponent)
        self._createPinsVM()
    
    def _createPinsVM(self):
        self._createInputPinsVM()
        self._createOutputPinsVM()
    
    def _createInputPinsVM(self):
        if not self._component.inputPins is None:
            self._inputPins = {}
            for pin in self._component.inputPins:
                newPinVM = PinVM(self._id, pin)
                self._inputPins[newPinVM.id] = newPinVM
        else:
            self._inputPins = {}
        
    def _createOutputPinsVM(self):
        if not self._component.outputPins is None:
            self._outputPins = {}
            for pin in self._component.outputPins:
                newPinVM = PinVM(self._id, pin)
                self._outputPins[newPinVM.id] = newPinVM
        else:
            self._outputPins = {}
    
    @property
    def inputPins(self):
        return self._inputPins
    
    @property
    def inputPinIds(self) -> List[str]:
        if self._inputPins:
            return list(self._inputPins.keys())
        else:
            return []
    
    @property
    def outputPins(self):
        return self._outputPins
    
    @property
    def outputPinIds(self) -> List[str]:
        if self._outputPins:
            return list(self._outputPins.keys())
        else:
            return []
    
    @property
    def pins(self):
        return self._inputPins | self._outputPins
    
    @property
    def value(self):
        return self._component.value