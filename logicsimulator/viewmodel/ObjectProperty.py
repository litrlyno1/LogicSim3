from PySide6.QtCore import QObject

class ObjectProperty(QObject):
    """Base class for properties associated with a parent view-model object.

    ``ObjectProperty`` stores the ID of its parent object so that related
    UI elements or view-model components can reference their owner.
    """

    def __init__(self, parentId: str):
        """Initialize the property.

        Args:
            parentId (str): The ID of the parent object this property belongs to.
        """
        super().__init__()
        self._parentId = parentId

    @property
    def parentId(self) -> str:
        """str: The ID of the parent object."""
        return self._parentId