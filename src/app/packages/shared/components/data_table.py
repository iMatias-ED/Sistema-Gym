from PySide6.QtCore import Signal, Slot, Qt, QSize
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QTableView, QTableWidget, QTableWidgetItem, QPushButton, QHeaderView
from __feature__ import snake_case, true_property

from typing import Callable, Any, Union, List, Iterable, Dict

# Type Classes
from ..classes.table_header_label import TableHeaderLabel
from ..classes.table_sub_value import SubValue
from ..classes.table_action import Action

# Main class
class DataTable(QTableWidget):
    edit = Signal(int)
    delete = Signal(int)

    header_labels: List[TableHeaderLabel]

    # Dev
    def setup_table(self, header_labels: List[TableHeaderLabel]):
        self.header_labels = header_labels
        self.vertical_header().visible = False
        self.column_count = len(header_labels)
        self.set_horizontal_header_labels([h.label for h in header_labels])

        self.horizontal_header().stretch_last_section = True
        self.horizontal_header().set_section_resize_mode(QHeaderView.Stretch)
        
        # self.focus_policy = Qt.NoFocus
        self.vertical_header().default_section_size = 40
        self.selection_behavior = QTableView.SelectRows

    def insert_values(self, row_items: List[Any], actions: List[Action] = [], sub_values: Dict[str, List[SubValue]] = {} ):
        self.row_count = len(row_items)

        for row, row_item in enumerate(row_items): 
            for key, value in row_item.__dict__.items():
                index = self.get_index(key)
                
                if key in sub_values: 
                    sub_item = getattr(row_item, key)

                    if isinstance(sub_item, Iterable):
                        for item in sub_item:
                            self._manage_sub_values(key, item, row, sub_values, True)
                    else: 
                        self._manage_sub_values(key, row_item, row, sub_values)

                if index == None: continue
                else: self._insert_text_item(value, row, index)

                for action in actions:
                    self._insert_action_button(action, row_item, row)

    def insert_value(self, row_item: Any, row: int, actions: List[Action] = [], sub_values: Dict[str, List[SubValue]] = {} ):

        for key, value in row_item.__dict__.items():
            if key in sub_values:
                self._manage_sub_values(key, row_item, row, sub_values)
                continue
            
            index = self.get_index(key)
            if index == None: continue
        
            value = getattr(row_item, key)
            self._insert_text_item(value, row, index)

            for action in actions:
                self._insert_action_button(action, row_item, row)

    def _manage_sub_values(self, key: str, row_item: Any, row: int, sub_values: Dict[str, SubValue], use_row_item_as_attr: bool = False) -> str:
        for sub_value in sub_values[key]:
            if use_row_item_as_attr: attr = row_item
            else: attr = getattr(row_item, key)
        
            if sub_value.is_column_name_an_attr:
                index = self.get_index( getattr(attr, sub_value.column_name_attr))
            else: 
                index = self.get_index(sub_value.column_name_attr)

            value = getattr(attr, sub_value.value_attr)
            self._insert_text_item(value, row, index)

    def _insert_text_item(self, value, row, column):
        self.set_item(row, column, QTableWidgetItem(str(value)))

    def _insert_action_button(self, config: Action, item: Any, row: int):
        params = []

        for param in config.params:
            if not config.params_are_attr:
                params.append(param)
                continue

            if param == "<self>": params.append(item)
            else: params.append(getattr(item, param))

        self.set_cell_widget( row, config.column,
            self._create_action_button(config, config.slot, *params))

    def _create_action_button(self, config: Action, on_clicked: Callable, *args) -> QPushButton:
        button = QPushButton(config.label, clicked=lambda: on_clicked(*args))
        if config.icon_path:
            button.text = ""
            button.icon = QIcon(config.icon_path)
            button.icon_size = QSize(25, 25)
        
        return button

    def get_index(self, key: str) -> Union[int, None]:
        result = None

        for index, header in enumerate(self.header_labels):
            if header.column_name == key: result=index
        return result

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
