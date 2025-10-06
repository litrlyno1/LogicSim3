from PySide6.QtWidgets import QLayout, QHBoxLayout
from PySide6.QtCore import QSize

from typing import Tuple

class MainWindowSettings():

    class LayoutSettings():
        def __init__(self,
                     type : QLayout,
                     contentsMargins : Tuple[int, int, int, int],
                     spacing : int):
            self.TYPE = type
            self.CONTENTS_MARGINS = contentsMargins
            self.SPACING = spacing
        
        @classmethod
        def default(cls):
            return cls(type = QHBoxLayout(), 
                       contentsMargins = (0, 0, 0, 0),
                       spacing = 0)

    def __init__(self, 
                 title : str, 
                 layoutSettings: LayoutSettings, 
                 resolution : QSize):
        self.TITLE = title
        self.LAYOUT = layoutSettings.TYPE
        self.LAYOUT.setContentsMargins(layoutSettings.CONTENTS_MARGINS[0], layoutSettings.CONTENTS_MARGINS[1], layoutSettings.CONTENTS_MARGINS[2], layoutSettings.CONTENTS_MARGINS[3])
        self.LAYOUT.setSpacing(layoutSettings.SPACING)
        self.RESOLUTION = resolution
    
    @classmethod
    def default(cls):
        title = "Logic Simulator"
        layoutSettings = MainWindowSettings.LayoutSettings.default()
        resolution = QSize(1200, 800)
        return cls(title,
                   layoutSettings,
                   resolution
                   )