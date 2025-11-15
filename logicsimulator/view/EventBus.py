class EventBus:
    def __init__(self):
        self._listeners = {}

    def subscribe(self, eventName, handler):
        if eventName not in self._listeners:
            self._listeners[eventName] = []
        self._listeners[eventName].append(handler)

    def unsubscribe(self, eventName, handler):
        if eventName in self._listeners:
            self._listeners[eventName].remove(handler)
            if not self._listeners[eventName]:
                del self._listeners[eventName]

    def emit(self, eventName, **kwargs):
        for handler in self._listeners.get(eventName):
            handler(eventName, **kwargs)
    
    @property
    def listeners(self):
        return self._listeners