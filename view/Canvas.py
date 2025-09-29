from PySide6.QtWidgets import QGraphicsView
from view.settings.CanvasSettings import CanvasSettings

class Canvas(QGraphicsView):
    
    def __init__(self, settings : CanvasSettings):
        super().__init()
        