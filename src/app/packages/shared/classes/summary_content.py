from ..classes.table_header_label import TableHeaderLabel
from typing import List

class SummaryContent:
    title: str
    second_title: str
    table_content: List
    table_headers: List[TableHeaderLabel]
    bottom_label: str

    def __init__(self, title: str, second_title: str, headers: List[TableHeaderLabel], bottom_label: str):
        self.title = title
        self.second_title = second_title
        self.table_headers = headers
        self.bottom_label = bottom_label