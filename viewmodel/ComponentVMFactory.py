from model.ComponentFactory import ComponentFactory
from model.CircuitComponent import CircuitComponent

from viewmodel.ComponentVM import ComponentVM
from viewmodel.CircuitComponentVM import CircuitComponentVM
from viewmodel.SwitchVM import SwitchVM

from PySide6.QtCore import QPointF

vm_model = {
    "Switch" : SwitchVM
}

class ComponentVMFactory:
    
    @staticmethod
    def createComponent(type : str, pos : QPointF):
        component = ComponentFactory.createComponent(type)
        if type in vm_model:
            return vm_model[type](component, pos)
        else:
            if isinstance(component, CircuitComponent):
                return CircuitComponentVM(component, pos)
            else:
                return ComponentVM(component, pos)