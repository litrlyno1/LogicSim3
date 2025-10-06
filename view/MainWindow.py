from PySide6.QtWidgets import QMainWindow
from view.settings.MainWindow import MainWindowSettings
from view.Canvas import Canvas

class MainWindow(QMainWindow):
    
    def __init__(self, settings : MainWindowSettings = MainWindowSettings.default(), canvas : Canvas = None):
        super().__init__()
        self.setWindowTitle(settings.TITLE)
        self.resize(settings.RESOLUTION)
        self._layout = settings.LAYOUT
        self._canvas = canvas or Canvas()
        self.setCentralWidget(self._canvas)