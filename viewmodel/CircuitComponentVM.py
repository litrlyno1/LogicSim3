from typing import List

from PySide6.QtCore import QPointF, Signal, Slot

from model.CircuitComponent import CircuitComponent
from viewmodel.ComponentVM import ComponentVM
from viewmodel.PinVM import PinVM
from viewmodel.PropagatorObject import PropagatorObject

class CircuitComponentVM(ComponentVM, PropagatorObject):
    """View-model wrapper for a :class:`CircuitComponent`.

    ``CircuitComponentVM`` provides the UI-side representation of a circuit
    component. It manages view-model instances for all input/output pins,
    exposes component values, and integrates propagation behavior by mixing
    in :class:`PropagatorObject`.
    """

    def __init__(self, circuitComponent: CircuitComponent, pos: QPointF):
        """Initialize the view-model.

        Args:
            circuitComponent (CircuitComponent): The logic/model component
                represented by this view-model.
            pos (QPointF): Initial position of the component in the view.
        """
        super().__init__(component=circuitComponent, pos=pos, propagator=circuitComponent)
        self._createPinsVM()

    def _createPinsVM(self):
        """Create both input and output pin view-models."""
        self._createInputPinsVM()
        self._createOutputPinsVM()

    def _createInputPinsVM(self):
        """Create view-models for all input pins of the component."""
        if self._component.inputPins is not None:
            self._inputPins = {}
            for pin in self._component.inputPins:
                newPinVM = PinVM(self._id, pin)
                self._inputPins[newPinVM.id] = newPinVM
        else:
            self._inputPins = {}

    def _createOutputPinsVM(self):
        """Create view-models for all output pins of the component."""
        if self._component.outputPins is not None:
            self._outputPins = {}
            for pin in self._component.outputPins:
                newPinVM = PinVM(self._id, pin)
                self._outputPins[newPinVM.id] = newPinVM
        else:
            self._outputPins = {}

    @property
    def inputPins(self):
        """dict: Mapping of input pin IDs to their view-model instances."""
        return self._inputPins

    @property
    def inputPinIds(self) -> List[str]:
        """List[str]: IDs of all input pin view-models."""
        if self._inputPins:
            return list(self._inputPins.keys())
        else:
            return []

    @property
    def outputPins(self):
        """dict: Mapping of output pin IDs to their view-model instances."""
        return self._outputPins

    @property
    def outputPinIds(self) -> List[str]:
        """List[str]: IDs of all output pin view-models."""
        if self._outputPins:
            return list(self._outputPins.keys())
        else:
            return []

    @property
    def pins(self):
        """dict: Combined mapping of all pin IDs to their view-models."""
        return self._inputPins | self._outputPins

    @property
    def value(self):
        """bool: The logical value of the underlying component."""
        return self._component.value