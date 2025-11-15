from logicsimulator.model.ComponentFactory import ComponentFactory
from logicsimulator.model.CircuitComponent import CircuitComponent

from logicsimulator.viewmodel.ComponentVM import ComponentVM
from logicsimulator.viewmodel.CircuitComponentVM import CircuitComponentVM
from logicsimulator.viewmodel.SwitchVM import SwitchVM

from PySide6.QtCore import QPointF

# Mapping of component type names to their corresponding view-model classes
vm_model = {
    "Switch": SwitchVM
}

class ComponentVMFactory:
    """Factory class for creating view-model instances of components.

    ``ComponentVMFactory`` generates the appropriate view-model wrapper
    for a given component type and initial position. It leverages the
    underlying :class:`ComponentFactory` to create the model object first,
    then selects the correct view-model class based on type.
    """

    @staticmethod
    def createComponent(type: str, pos: QPointF):
        """Create a component and its corresponding view-model.

        Args:
            type (str): The type name of the component to create.
            pos (QPointF): Initial position of the view-model in the UI.

        Returns:
            ComponentVM: A view-model instance corresponding to the created
                component.

        Behavior:
            - If the type is registered in ``vm_model``, use the mapped
            specialized view-model class.
            - If the component is a :class:`CircuitComponent` but not in
            ``vm_model``, return a generic :class:`CircuitComponentVM`.
            - Otherwise, return a generic :class:`ComponentVM`.
        """
        component = ComponentFactory.createComponent(type)
        if type in vm_model:
            return vm_model[type](component, pos)
        else:
            if isinstance(component, CircuitComponent):
                return CircuitComponentVM(component, pos)
            else:
                return ComponentVM(component, pos)