from PySide6.QtWidgets import *
from PySide6.QtCore import *
from __feature__ import snake_case, true_property

from .service import *

class Table(QTableWidget):
    service = CustomersService()

    test_data = [
        ("Matias Acosta", "7.478.938-4", "matdj31@gmail.com", "0994633973"),
        ("Belén Franco", "1.111.111-1", "belen@gmail.com", "0972771482")
    ]

    def example(self):
        self.row_count = len(self.test_data)
        self.column_count = 6
  
        self.load_data()

        self.set_horizontal_header_labels(self.service.header_labels)

        self.horizontal_header().stretch_last_section = True
        self.horizontal_header().set_section_resize_mode(
            QHeaderView.Stretch)
        
        self.hide(1)

    def load_data(self):
        def create_edit_button(row: int):
            button = QPushButton("E")
            button.clicked.connect( lambda: self.delete_clicked(row) )
            return button
            
        def create_delete_button(row: int):
            button = QPushButton("X")
            button.clicked.connect( lambda: self.delete_clicked(row) )
            return button
        
        for row, data in enumerate(self.test_data):
            self.set_cell_widget(row, 0, create_delete_button(row))
            self.set_cell_widget(row, 1, create_edit_button(row))

            for column, item in enumerate(data):
                col = column+2
                self.set_item(row, col, QTableWidgetItem(item))

    def edit_clicked(self, row:int):
        print("editing", row)
    
    def delete_clicked(self, row:int):
        print("removing", row)

