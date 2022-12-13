from PySide6.QtWidgets import QFrame, QVBoxLayout, QLabel, QCheckBox
from PySide6.QtCore import Signal, Qt
from __feature__ import snake_case, true_property

from typing import List


class TableColumnsFilter(QFrame):
    filter_event = Signal(int, bool)

    def __init__(self, header_labels: List[str]):
        super(TableColumnsFilter, self).__init__()
        self.setup_ui(header_labels)

    def setup_ui(self, header_labels: List[str]) -> None:
        self.root_layout = QVBoxLayout()
        self.checkbox_layout = QVBoxLayout()

        for index, label in enumerate(header_labels):
            self.create_checkbox(label, index)
        self.checkbox_layout.add_stretch()

        self.title = QLabel('Filtrar datos', object_name="columns-filter-title", alignment=Qt.AlignCenter)
        self.root_layout.add_widget(self.title, 10)
        self.root_layout.add_spacing(10)
        self.root_layout.add_layout(self.checkbox_layout, 90)
        
        self.set_layout(self.root_layout)

    def create_checkbox(self, label:str, index: int) -> None:
        checkbox = QCheckBox(label)
        checkbox.stateChanged.connect( lambda: self.__on_filter(index, checkbox.checked) )
        self.checkbox_layout.add_widget(checkbox)
        
    def __on_filter(self, index: int, state: bool) -> None:
        self.filter_event.emit(index, state)