from typing import Callable, Any

class Action:
    column: int
    label: str
    slot: Callable
    params: Any
    icon_path: str
    params_are_attr: bool

    def __init__(self, column: int, label: str, slot: Callable, params_are_attr: bool = True, icon_path: str = None, *args):
        self.column = column
        self.label = label
        self.slot = slot
        self.params = args
        self.icon_path = icon_path
        self.params_are_attr = params_are_attr