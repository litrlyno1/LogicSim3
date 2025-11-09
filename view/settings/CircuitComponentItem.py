from view.settings.ComponentItem import ComponentItemSettings

class CircuitComponentItemSettings(ComponentItemSettings):
    
    def __init__(self,
                size,
                fontSize,
                textColor,
                color,
                selectedColor,
                borderColor,
                borderWidth):

        super().__init__(size,
                fontSize,
                textColor,
                color,
                selectedColor,
                borderColor,
                borderWidth)
    
    @classmethod
    def default(cls):
        return ComponentItemSettings.default()