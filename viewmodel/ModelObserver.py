from PySide6.QtCore import Signal, QObject

from model.Observer import Observer
from model.LogicGate import LogicGate

class ModelObserver(Observer):
    def __init__(self, parent : QObject, gate : LogicGate):
        self._parent = parent
        self._gate = gate
        self._gate.attach(observer = self)
    
    def update(self) -> None:
        self._parent.onModelUpdate()