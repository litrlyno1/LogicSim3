from PySide6.QtCore import Signal, QObject

from model.Pin import Connection
from ModelObserver import ModelObserver
from Deletable import Deletable
from Selectable import Selectable

class ConnectionVM(QObject):
    selectedChanged = Signal()
    deleted = Signal()
    
    def __init__(self, connection : Connection):
        super().__init__()
        self._connection = connection
        self._connection.attach(self)

    def getConnection(self):
        return self._connection