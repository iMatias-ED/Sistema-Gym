from typing import List, Callable
from ..classes.table_header_label import TableHeaderLabel

class SearchDialogConfig:
    title: str
    input_placeholder: str
    table_headers: List[str]
    slot: Callable

    def __init__(self, title: str, placeholder: str, headers: List[TableHeaderLabel], slot: Callable):
        self.title = title
        self.input_placeholder = placeholder
        self.table_headers = headers
        self.slot = slot