from PySide6.QtCore import Signal, Slot
from PySide6.QtWidgets import QTableWidget, QTableWidgetItem, QPushButton, QHeaderView
from __feature__ import snake_case, true_property

from typing import Callable, Any, Union, List

# Type Classes
class TableItem:
    column: int
    value: str

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            self.__setattr__(key, value)


class Action:
    column: int
    label: str
    slot: Callable
    params: Any

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            self.__setattr__(key, value)

# Main class

class DataTable(QTableWidget):
    edit = Signal(int)
    delete = Signal(int)

    # Initial setup
    def setup_table(self, header_labels: List[str]) -> None:
        self.vertical_header().visible = False
        self.column_count = len(header_labels)
        self.set_horizontal_header_labels(header_labels)

        self.horizontal_header().stretch_last_section = True
        self.horizontal_header().set_section_resize_mode(QHeaderView.Stretch)

    # Insert one row
    def insert_item(self, data: list[ Union[TableItem, Action] ], row: int):
        for item in data:
            if (isinstance(item, TableItem)):
                self._insert_text_item(row, item)
            if (isinstance(item, Action)):
                self._insert_action_button(row, item)

    # Insert many rows
    def insert_items(self, data: list[list[Union[TableItem, Action]]]):
        self.row_count = len(data)

        for row, row_data in enumerate(data):
            for item in row_data:
                if (isinstance(item, TableItem)):
                    self._insert_text_item(row, item)
                if (isinstance(item, Action)):
                    self._insert_action_button(row, item)

    # Insert Items
    def _insert_text_item(self, row: int, item: TableItem):
        self.set_item(
            row, item.column, QTableWidgetItem(str(item.value)))

    def _insert_action_button(self, row: int, config: Action):
        self.set_cell_widget(row, config.column,
                             self._create_button(config.label, config.slot, config.params))

    # Placeholders
    def load_data(self) -> None:
        """ This is a placeholder! Configure this method in the child class """
        pass

    # Util
    def refresh(self) -> None:
        self.clear_contents()
        self.load_data()

    def _create_button(self, text: str, on_clicked: Callable, *args) -> QPushButton:
        if len(args) == 1: args = args[0]

        button = QPushButton(text)
        button.clicked.connect(lambda: on_clicked(args))
        return button

    # Slots
    @Slot(int, bool)
    def on_filter(self, index, state) -> None:
        if state:
            self.hide_column(index)
            return
        self.show_column(index)

    @Slot()
    def _on_data_changed(self) -> None:
        self.refresh()
