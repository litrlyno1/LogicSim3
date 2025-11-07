from core.registry import ComponentRegistry
from model.Component import Component

class ComponentFactory:
    
    @staticmethod
    def createComponent(type : str) -> Component:
        component = ComponentRegistry.getComponent(type)()
        return component