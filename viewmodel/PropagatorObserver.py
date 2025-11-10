from PySide6.QtCore import Signal, QObject

from model.Observer import Observer
from model.Propagator import Propagator

class PropagatorObserver(Observer):
    def __init__(self, parent : QObject, propagator : Propagator):
        self._parent = parent
        self._propagator = propagator
        self._propagator.attach(self)
    
    def update(self) -> None:
        print(f"self propagator: {self._propagator}")
        print(f"with value: {self._propagator.value}")
        self._parent.onValueChange(self._propagator.value)
    
    @property
    def propagator(self):
        return self._propagator