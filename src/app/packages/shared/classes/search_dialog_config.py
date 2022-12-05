from typing import List, Callable

class SearchDialogConfig:
    title: str
    input_placeholder: str
    table_headers: List[str]
    slot: Callable

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            self.__setattr__(key, value)