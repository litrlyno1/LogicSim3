from abc import ABC, abstractmethod

class Component(ABC):
    """Base class for all components.

    This abstract class defines the required interface for any component. All components must define their own `type` property.

    Attributes:
        type (str): A read-only property that must be implemented by subclasses
            to return the component's type name.
    """
    
    @property
    @abstractmethod
    def type(self) -> str:
        """Return the component type

        Returns:
            str: The type of the component.
        """        
        pass