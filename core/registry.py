import inspect
import importlib

class GateRegistry:
    def __init__(self, module_path: str = "model.Gates"):
        self.module_path = module_path
        self.registry = {}
        self._loadGates()

    def _loadGates(self):
        gates_module = importlib.import_module(self.module_path)
        for name, obj in inspect.getmembers(gates_module, inspect.isclass):
            self.registry[name] = obj

    def getClass(self, name: str):
        return self.registry.get(name)

    def getAllGates(self) -> list:
        return list(self.registry.keys())

    def reload(self):
        self.registry.clear()
        self._loadGates()

