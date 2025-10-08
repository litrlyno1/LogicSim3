from PySide6.QtWidgets import QMainWindow, QWidget, QHBoxLayout
from view.settings.MainWindow import MainWindowSettings
from view.Canvas import Canvas
from view.SideBar import SideBar


class MainWindow(QMainWindow):
    def __init__(self,
                settings: MainWindowSettings = MainWindowSettings.default(),
                canvas: Canvas = None,
                sidebar: SideBar = None,):
        
        super().__init__()
        self.setWindowTitle(settings.TITLE)
        self.resize(settings.RESOLUTION)

        self.container = QWidget(self)
        self._layout = QHBoxLayout(self.container)
        self.container.setLayout(self._layout)

        self.addSideBar()
        self.addCanvas()

        self.setCentralWidget(self.container)
    
    def addCanvas(self, canvas : Canvas = None):
        self._canvas = Canvas(parent = self) or canvas
        self._layout.addWidget(self._canvas)
    
    def addSideBar(self, sideBar : SideBar = None):
        self._sideBar = SideBar(parent = self) or sideBar
        self._layout.addWidget(self._sideBar)
    
    def getCanvas(self) -> Canvas:
        return self._canvas