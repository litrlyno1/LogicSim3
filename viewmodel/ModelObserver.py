from PySide6.QtCore import Signal

from model.Observer import Observer
from model.Propagator import Propagator

class ModelObserver(Observer):
    modelUpdated = Signal()
    
    def update(self) -> None:
        self.modelUpdated.emit()
