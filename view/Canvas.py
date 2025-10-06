from PySide6.QtWidgets import QGraphicsView
from PySide6.QtCore import Signal, QPointF

from view.settings.Canvas import CanvasSettings

class Canvas(QGraphicsView):
    
    def __init__(self, settings : CanvasSettings):
        super().__init()
        self.gatePlaced = Signal(str, QPointF, str)               
        self.gateSelected = Signal(str)                           
        self.connectionStarted = Signal(str)                     
        self.connectionPreview = Signal(QPointF)                  
        self.connectionCompleted = Signal(str, str)               
        self.itemMoved = Signal(str, QPointF)
    
    @classmethod
    def createDefault(cls):
        return cls(settings = )