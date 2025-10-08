import inspect
import importlib

class CommandRegistry:
    _registry = None

    @classmethod
    def _loadCommands(cls, module_path="viewmodel.command.Commands"):
        if cls._registry is None:
            import importlib, inspect
            gates_module = importlib.import_module(module_path)
            cls._registry = {
                name: obj
                for name, obj in vars(gates_module).items()
                if inspect.isclass(obj) and name != "Command"
            }
        return cls._registry

    @classmethod
    def getAllCommands(cls):
        return list(cls._loadCommands().keys())
    
    @classmethod
    def getCommand(cls, name : str):
        registry = cls._loadCommands()
        return registry[name]