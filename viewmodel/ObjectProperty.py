from PySide6.QtCore import QObject

class ObjectProperty(QObject):
    
    def __init__(self, parentId : str):
        super().__init__()
        self._parentId = parentId
    
    @property
    def parentId(self):
        return self._parentId