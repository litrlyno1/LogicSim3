from PySide6.QtWidgets import QGraphicsView
from PySide6.QtCore import Signal

from view.settings.CanvasSettings import CanvasSettings

class Canvas(QGraphicsView):
    
    def __init__(self, settings : CanvasSettings):
        super().__init()
        self.gatePlaced = Signal(str, QPointF, str)               
        self.gateSelected = Signal(str)                           
        self.connectionStarted = Signal(str)                     
        self.connectionPreview = Signal(QPointF)                  
        self.connectionCompleted = Signal(str, str)               
        self.itemMoved = Signal(str, QPointF)