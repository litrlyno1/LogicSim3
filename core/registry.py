class registry:
    _registry = {}

    @classmethod
    def register(cls, name : str, gate_cls):
        cls._registry[name] = gate_cls

    @classmethod
    def getGate(cls, name : str):
        return cls._registry.get(name)

    @classmethod
    def allGates(cls):
        return list(cls._registry.keys())