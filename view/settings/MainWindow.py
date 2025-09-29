from PySide6.QtWidgets import QLayout, QHBoxLayout
from PySide6.QtCore import QSize

class MainWindowSettings():
    def __init__(self, 
                 title : str, 
                 layout: QLayout, 
                 resolution : QSize):
        self.TITLE = title
        self.LAYOUT = layout
        self.RESOLUTION = resolution
    
    @classmethod
    def getDefault(cls):
        return cls(title = "Logic Simulator", 
                   layout = QHBoxLayout(), 
                   resolution = QSize(1200, 800)
                   )