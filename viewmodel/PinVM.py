from model.Pin import Pin
from viewmodel.PropagatorObject import PropagatorObject
from core.idGenerator import generateId
import weakref

class PinVM(PropagatorObject):
    
    def __init__(self, pin : Pin):
        self._pin = pin
        self._id = generateId(prefix = self._pin.type)
        super().__init__(id = self._id, propagator = self._pin)
    
    @property
    def pin(self):
        return self._pin
    
    @property
    def type(self):
        return self.pin.type
    
    @property
    def id(self):
        return self._id