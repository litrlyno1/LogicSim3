from typing import Protocol, List

class Observer(Protocol):
    def onChange(self) -> None:
        ...

