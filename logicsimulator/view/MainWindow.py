from PySide6.QtWidgets import QMainWindow, QWidget, QHBoxLayout
from logicsimulator.view.settings.MainWindow import MainWindowSettings
from logicsimulator.view.Canvas import Canvas
from logicsimulator.view.SideBar import SideBar

class MainWindow(QMainWindow):
    """Main application window for the logic circuit simulator.

    This window contains a canvas for placing circuit components and a sidebar
    for selecting and dragging components into the canvas.
    """

    def __init__(self,
                settings: MainWindowSettings = MainWindowSettings.default(),
                canvas: Canvas = None,
                sidebar: SideBar = None):
        """Initialize the main window with optional custom settings, canvas, and sidebar.

        Args:
            settings (MainWindowSettings, optional): Settings for window title and resolution. Defaults to default settings.
            canvas (Canvas, optional): Custom canvas to embed in the window. Defaults to None.
            sidebar (SideBar, optional): Custom sidebar to embed in the window. Defaults to None.
        """
        super().__init__()

        # Configure window title and size
        self.setWindowTitle(settings.TITLE)
        self.resize(settings.RESOLUTION)

        # Create central container widget with horizontal layout
        self.container = QWidget(self)
        self._layout = QHBoxLayout(self.container)
        self.container.setLayout(self._layout)

        # Add sidebar and canvas widgets
        self.addSideBar(sidebar)
        self.addCanvas(canvas)

        # Set the container as the central widget
        self.setCentralWidget(self.container)
    
    def addCanvas(self, canvas: Canvas = None):
        """Add a canvas widget to the main window layout.

        Args:
            canvas (Canvas, optional): If provided, use this canvas; otherwise, create a new one.
        """
        # Use provided canvas or create a new Canvas
        self._canvas = canvas or Canvas(parent=self)
        self._layout.addWidget(self._canvas)
    
    def addSideBar(self, sideBar: SideBar = None):
        """Add a sidebar widget to the main window layout.

        Args:
            sideBar (SideBar, optional): If provided, use this sidebar; otherwise, create a new one.
        """
        # Use provided sidebar or create a new SideBar
        self._sideBar = sideBar or SideBar(parent=self)
        self._layout.addWidget(self._sideBar)
    
    def getCanvas(self) -> Canvas:
        """Return the canvas widget.

        Returns:
            Canvas: The canvas currently embedded in the main window.
        """
        return self._canvas