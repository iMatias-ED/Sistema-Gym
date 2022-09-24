from typing import Callable, Dict, List, Tuple
from PySide6.QtWidgets import *
from PySide6.QtCore import *
from __feature__ import snake_case, true_property

from ..service import MovementsService

class Table(QTableWidget):
    #Both emits the product_id
    edit = Signal(int)
    delete = Signal(int)

    def __init__(self, service: MovementsService):
        super(Table, self).__init__()
        self.customers_service = service
        self.customers_service.data_changed.connect( self.refresh )

        self.config_table()

    def config_table(self) -> None:
        self.column_count = len(self.customers_service.header_labels)
        self.set_horizontal_header_labels(self.customers_service.header_labels)

        self.horizontal_header().stretch_last_section = True
        self.horizontal_header().set_section_resize_mode(QHeaderView.Stretch)

        self.load_data()
        
    def load_data(self) -> None:
        self.customers = self.customers_service.get_all()
        self.row_count = len(self.customers)

        def create_button(text:str, customer_id: int, on_clicked: Callable)  -> QPushButton:
            button = QPushButton(text)
            button.clicked.connect( lambda: on_clicked(customer_id) )
            return button

        for row, customer in enumerate(self.customers):
            self.set_cell_widget(row, 0, create_button( "X", customer.id, self.delete_clicked ))
            self.set_cell_widget(row, 1, create_button( "E", customer.id, self.edit_clicked))

            self.set_item(row, 2, QTableWidgetItem(customer.full_name))
            self.set_item(row, 3, QTableWidgetItem(str(customer.ci)))
            self.set_item(row, 4, QTableWidgetItem(customer.ruc))
            self.set_item(row, 5, QTableWidgetItem(customer.invoice_to))
            self.set_item(row, 6, QTableWidgetItem(customer.phone))
            self.set_item(row, 7, QTableWidgetItem(customer.email))
            self.set_item(row, 8, QTableWidgetItem(customer.genre))
            self.set_item(row, 9, QTableWidgetItem(str(customer.access_until_date)))

    def refresh(self)  -> None:
        self.clear()
        self.config_table()

    def edit_clicked(self, customer_id:int) -> None:
        self.edit.emit(customer_id)
    
    def delete_clicked(self, customer_id:int) -> None:
        self.delete.emit(customer_id)
        self.customers_service.delete(customer_id)

    @Slot(int, bool)
    def on_filter(self, index, state) -> None:
        if state: 
            self.hide_column(index)
            return
        self.show_column(index)

    @Slot()
    def _on_data_changed(self) -> None:
        self.refresh()
