class SideBarSettings:
    def __init__(self,
                width,
                margin,
                spacing,
                header,
                styleSheet,
                buttonStyleSheet):
        self.WIDTH = width
        self.MARGIN = margin
        self.SPACING = spacing
        self.HEADER = header
        self.STYLE_SHEET = styleSheet
        self.BUTTON_STYLE_SHEET = buttonStyleSheet
        
    @classmethod
    def default(cls):
        width = 180
        margin = 8
        spacing = 10
        header = "Logic Gates"
        styleSheet = "font-weight: bold; font-size: 14px;"
        buttonStyleSheet = """
                QPushButton {
                    padding: 6px;
                    border-radius: 6px;
                    background-color: #e0e0e0;
                    color: black;
                }
                QPushButton:hover {
                    background-color: #cfd8dc;
                }
            """
        return cls(width, margin, spacing, header, styleSheet, buttonStyleSheet)