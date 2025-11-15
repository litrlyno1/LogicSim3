from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QSizePolicy, QLabel
from PySide6.QtGui import QDrag, QPixmap, QPainter
from PySide6.QtCore import Qt, QMimeData
from typing import List

from logicsimulator.core.registry import ComponentRegistry
from logicsimulator.view.settings.SideBar import SideBarSettings

class SideBar(QWidget):
    """Sidebar widget displaying all available components as draggable buttons.

    The sidebar allows the user to drag and drop components (logic gates, bulbs, switches)
    into the main canvas. Each component type gets a dedicated button.

    Attributes:
        gateTypes (List[str]): List of available component types to display.
    """

    def __init__(self, parent=None, gateTypes: List[str] = ComponentRegistry.getAllComponents(), settings=SideBarSettings.default()):
        """Initialize the sidebar with component buttons and visual settings.

        Args:
            parent (QWidget, optional): Parent widget. Defaults to None.
            gateTypes (List[str], optional): List of component types to display. Defaults to all registered components.
            settings (SideBarSettings, optional): Settings for sidebar appearance. Defaults to default settings.
        """
        super().__init__(parent)
        self.gateTypes = gateTypes
        self._importSettings(settings)
        self._setupGraphics()

    def _importSettings(self, settings: SideBarSettings):
        """Load visual and layout settings for the sidebar.

        Args:
            settings (SideBarSettings): Settings object with margins, width, spacing, and stylesheet.
        """
        self._width = settings.WIDTH
        self._margin = settings.MARGIN
        self._spacing = settings.SPACING
        self._header = settings.HEADER
        self._styleSheet = settings.STYLE_SHEET
        self._buttonStyleSheet = settings.BUTTON_STYLE_SHEET

    def _setupGraphics(self):
        """Create the sidebar layout and add a header and buttons for each component type."""
        self.setFixedWidth(self._width)
        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(self._margin, self._margin, self._margin, self._margin)
        layout.setSpacing(self._spacing)

        # Add header label
        header = QLabel(self._header)
        header.setAlignment(Qt.AlignCenter)
        header.setStyleSheet(self._styleSheet)
        layout.addWidget(header)

        # Add a button for each gate type
        for gateType in self.gateTypes:
            button = QPushButton(gateType)
            button.setObjectName(f"btn_{gateType.lower()}")
            button.setStyleSheet(self._buttonStyleSheet)
            # Connect button press to drag start
            button.pressed.connect(lambda gt=gateType: self.startDrag(gt))
            layout.addWidget(button)

        layout.addStretch()

    def startDrag(self, gateType: str):
        """Start a drag operation for a given component type.

        Creates a QDrag object with the component type encoded in QMimeData.

        Args:
            gateType (str): Type of the component being dragged.
        """
        drag = QDrag(self)
        mime = QMimeData()
        mime.setText(gateType)
        drag.setMimeData(mime)
        drag.exec(Qt.CopyAction)