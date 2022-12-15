from typing import List, Callable
from PySide6.QtWidgets import QDialog, QLineEdit, QPushButton, QVBoxLayout, QLabel
from PySide6.QtCore import Signal, Slot, Qt
from __feature__ import snake_case, true_property

# Classes
from .data_table import DataTable
from ..classes.search_dialog_config import SearchDialogConfig


class SearchDialog(QDialog):

    def setup_ui(self, config: SearchDialogConfig) -> None:        
        self.object_name = "search-dialog"
        self.root_layout = QVBoxLayout()
        self.minimum_width = 400 

        # Products data
        self.title    = QLabel    ( config.title, alignment=Qt.AlignCenter, object_name="title" ) 
        self.input    = QLineEdit ( placeholder_text=config.input_placeholder, object_name="search-input" )
        self.table    = self._create_table(config.table_headers)
        
        # Update table data
        self.input.textChanged.connect(self.update_table_data)

        # Add to layout
        self.root_layout.add_widget(self.title)
        self.root_layout.add_widget(self.input)
        self.root_layout.add_widget(self.table)

        # Initial data
        self.update_table_data("")

        # Button
        self.submit = QPushButton("Seleccionar", clicked=config.slot, object_name="bt-select")
        self.root_layout.add_widget(self.submit)

        self.set_layout(self.root_layout)

    def search(self): 
        self.show()

    # Signal Slots
    @Slot(str)
    def update_table_data(self, text:str):
        """This is a placeholder"""
        pass

    def search(self): 
        self.show()

    def _create_table(self, header_labels: List) -> DataTable:
        table = DataTable()
        table.setup_table(header_labels)
        return table
