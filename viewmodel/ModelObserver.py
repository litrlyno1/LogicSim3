from PySide6.QtCore import Signal, QObject

from model.Observer import Observer
from model.Component import Component
from model.LogicGate import LogicGate

class ModelObserver(Observer):
    def __init__(self, parent : QObject, component : Component):
        self._parent = parent
        self._propagator = component
        self._propagator.attach(observer = self)
    
    def update(self) -> None:
        self._parent.onModelUpdate()