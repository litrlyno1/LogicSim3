import inspect
import importlib

class GateRegistry:
    _registry = None

    @classmethod
    def _loadGates(cls, module_path="model.Gates"):
        if cls._registry is None:
            import importlib, inspect
            gates_module = importlib.import_module(module_path)
            cls._registry = {
                name: obj
                for name, obj in vars(gates_module).items()
                if inspect.isclass(obj) and name != "LogicGate"
            }
        return cls._registry

    @classmethod
    def getAllGates(cls):
        return list(cls._loadGates().keys())
    
    @classmethod
    def getGate(cls, name : str):
        registry = cls._loadGates()
        return registry[name]