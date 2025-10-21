from PySide6.QtCore import Signal, QObject

from model.Observer import Observer
from model.Propagator import Propagator
from model.LogicGate import LogicGate

class ModelObserver(Observer):
    def __init__(self, parent : QObject, propagator : Propagator):
        self._parent = parent
        self._propagator = propagator
        self._propagator.attach(observer = self)
    
    def update(self) -> None:
        self._parent.onModelUpdate()