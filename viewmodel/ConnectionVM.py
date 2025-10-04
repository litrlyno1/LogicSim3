from PySide6.QtCore import Signal, QObject
from model.Observer import Observer
from model.Pin import Connection

class ConnectionVM(QObject, Observer):
    selectedChanged = Signal()
    deleted = Signal()
    
    def __init__(self, connection : Connection):
        self._connection = connection
    
    
    
    def delete(self):
        self.deleted.emit()