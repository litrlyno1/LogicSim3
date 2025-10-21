import inspect
import importlib

class ComponentRegistry:
    _registry = None

    @classmethod
    def _loadComponents(cls, modules = ["model.Gates", "model.Switch", "model.Bulb"]):
        
        if cls._registry is None:
            componentModule = importlib.import_module("model.Component")
            logicGateModule = importlib.import_module("model.LogicGate")
            Component = getattr(componentModule, "Component")
            LogicGate = getattr(logicGateModule, "LogicGate")

            cls._registry = {}
            for module_name in modules:
                module = importlib.import_module(module_name)
                for name, obj in vars(module).items():
                    if (
                        inspect.isclass(obj)
                        and issubclass(obj, Component)
                        and obj is not Component
                        and obj is not LogicGate
                    ):
                        cls._registry[name] = obj

        return cls._registry

    @classmethod
    def getAllComponents(cls):
        return list(cls._loadComponents().keys())
    
    @classmethod
    def getComponent(cls, name : str):
        registry = cls._loadComponents()
        return registry[name]