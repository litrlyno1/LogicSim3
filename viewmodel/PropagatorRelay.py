from model.Propagator import Propagator

from viewmodel.PropagatorObserver import PropagatorObserver
from viewmodel.ObjectProperty import ObjectProperty

from PySide6.QtCore import QObject, Signal

class PropagatorRelay(ObjectProperty):
    valueChanged = Signal(str, bool)
    #id, value
    
    def __init__(self, parentId : str, propagator : Propagator):
        super().__init__(parentId)
        self._propagatorObserver = PropagatorObserver(self, propagator)
    
    def onValueChange(self, value : bool) -> None:
        self.valueChanged.emit(self._parentId, value)
        #print(f"Reacting to change in model. Object type: {self._propagatorObserver.propagator.type}, value: {value}")