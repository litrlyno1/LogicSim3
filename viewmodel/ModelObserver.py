from PySide6.QtCore import Signal

from model.Observer import Observer
from model.Propagator import Propagator

class ModelObserver(Observer):
    modelUpdated = Signal()
    
    def __init__():
        super().__init__()
    
    def update(self):
        self.modelUpdated.emit()
