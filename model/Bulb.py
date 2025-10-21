from model.Propagator import Propagator
from model.Component import Component

class Bulb(Component, Propagator):
    type = "Bulb"
    
    def getOutput(self):
        return self._value