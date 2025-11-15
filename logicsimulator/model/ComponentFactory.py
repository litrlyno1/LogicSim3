from logicsimulator.core.registry import ComponentRegistry
from logicsimulator.model.Component import Component

class ComponentFactory:
    """Factory class for creating component instances.

    ``ComponentFactory`` provides a simple interface for constructing
    :class:`Component` objects based on their registered type names.
    It relies on :class:`ComponentRegistry` to look up the appropriate constructor.
    """

    @staticmethod
    def createComponent(type: str) -> Component:
        """Create a component instance by its type name.

        This method looks up the registered constructor for the given
        ``type`` in :class:`ComponentRegistry` and returns a new instance.

        Args:
            type (str): The unique type identifier of the component to create.

        Returns:
            Component: A newly constructed component of the requested type.

        Raises:
            KeyError: If no component with the given type is registered.
        """
        component = ComponentRegistry.getComponent(type)()
        return component