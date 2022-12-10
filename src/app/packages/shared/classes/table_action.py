from typing import Callable, Any

class Action:
    column: int
    label: str
    slot: Callable
    params: Any
    params_are_attr: bool

    def __init__(self, column: int, label: str, slot: Callable, params_are_attr: bool = True, *args):
        self.column = column
        self.label = label
        self.slot = slot
        self.params = args
        self.params_are_attr = params_are_attr