from PySide6.QtCore import QOBject, Signal

class Selectable(QObject):
    
    def __init__(self):
        super().__init__()
    
    def select(self):
        if 