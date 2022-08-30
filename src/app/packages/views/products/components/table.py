from typing import Callable, Dict, List, Tuple
from PySide6.QtWidgets import *
from PySide6.QtCore import *
from __feature__ import snake_case, true_property

from ..service import ProductsService

class Table(QTableWidget):
    #Both emits the product_id
    edit = Signal(int)
    delete = Signal(int)

    def __init__(self, service: ProductsService):
        super(Table, self).__init__()
        self.service = service
        self.service.data_changed.connect( self.refresh )

        self.config_table()

    def config_table(self) -> None:
        self.column_count = len(self.service.header_labels)
        self.set_horizontal_header_labels(self.service.header_labels)

        self.horizontal_header().stretch_last_section = True
        self.horizontal_header().set_section_resize_mode(QHeaderView.Stretch)

        self.load_data()
        
    def load_data(self) -> None:
        self.products = self.service.get_all()
        self.row_count = len(self.products)

        def create_button(text:str, product_id: int, on_clicked: Callable)  -> QPushButton:
            button = QPushButton(text)
            button.clicked.connect( lambda: on_clicked(product_id) )
            return button

        for row, product in enumerate(self.products):
            self.set_cell_widget(row, 0, create_button( "X", product.id, self.delete_clicked ))
            self.set_cell_widget(row, 1, create_button( "E", product.id, self.edit_clicked))

            self.set_item(row, 2, QTableWidgetItem(product.code))
            self.set_item(row, 3, QTableWidgetItem(product.name))

            # Prices
            prices = self.service.get_prices( product.id )
            for column, price in enumerate(prices):
                #[0] -> period; [1] -> price
                column = column + 4
                self.set_item(row, column, QTableWidgetItem( str(price[1]) ))

    def refresh(self)  -> None:
        self.clear()
        self.config_table()

    def edit_clicked(self, product_id:int) -> None:
        self.edit.emit(product_id)
    
    def delete_clicked(self, product_id:int) -> None:
        self.delete.emit(product_id)
        self.service.delete(product_id)

    @Slot(int, bool)
    def on_filter(self, index, state) -> None:
        if state: 
            self.hide_column(index)
            return
        self.show_column(index)

    @Slot()
    def _on_data_changed(self) -> None:
        self.refresh()
