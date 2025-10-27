from __future__ import annotations
from model.Propagator import Propagator
from model.Component import Component
from model.HasPins import HasPins

class LogicGate(Component, HasPins, Propagator):

    def __init__(self, numInputs: int, numOutputs: int):
        super().__init__(numInputs, numOutputs)