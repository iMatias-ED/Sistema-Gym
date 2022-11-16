from typing import Callable, Dict, List, Tuple
from PySide6.QtWidgets import *
from PySide6.QtCore import *
from __feature__ import snake_case, true_property

# Services
from ..service import MovementsService

# Classes
from ..classes.product_selection import ProductSelection
from ..classes.selected_product_info import SelectedProductInfo
from ...products.classes.product import Product

class Table(QTableWidget):
    #Both emits the product_id
    edit = Signal(int)
    delete = Signal(int)
    
    collection: dict[str: SelectedProductInfo] = {}

    def __init__(self, service: MovementsService):
        super(Table, self).__init__()
        self.movements_service = service
        self.movements_service.data_changed.connect( self.refresh )

        self.config_table()

    def config_table(self) -> None:
        self.vertical_header().visible = False
        self.column_count = len(self.movements_service.header_labels)
        self.set_horizontal_header_labels(self.movements_service.header_labels)

        self.horizontal_header().stretch_last_section = True
        self.horizontal_header().set_section_resize_mode(QHeaderView.Stretch)

    def refresh(self)  -> None:
        self.clear()
        self.config_table()

    def delete_clicked(self, key:str) -> None:   
        self.hide_row(self.collection[key].row)
        del self.collection[key]
        
    def create_action_button(self, text:str, param: str, on_clicked: Callable)  -> QPushButton:
        button = QPushButton(text)
        button.clicked.connect( lambda: on_clicked(param) )
        return button

    @Slot(Product)
    def on_product_select(self, data: ProductSelection):
        key = f'{data.product.code}::{data.price.name}'
        
        if key not in self.collection:
            self.row_count += 1
            row = self.row_count - 1

            self.collection[key] = SelectedProductInfo(data, row)
            self.insert_data(data, key, row)
        else:
            info = self.collection[key]
            info.data.add(data.quantity)
            self.insert_data(info.data, key, info.row)

    def insert_data(self, data: ProductSelection, key:str, row:int):
        total = f"Gs. {data.total}"
        price = f"Gs. {data.price.price}"

        self.set_cell_widget( 
            row, 0, self.create_action_button( "X", key, self.delete_clicked ))
        
        self.set_item( row , 1, QTableWidgetItem(data.product.name) )
        self.set_item( row , 2, QTableWidgetItem(str(data.quantity)) )
        self.set_item( row , 3, QTableWidgetItem(data.price.name) )
        self.set_item( row , 4, QTableWidgetItem(price) )
        self.set_item( row , 5, QTableWidgetItem(total) )

    # def edit_clicked(self, customer_id:int) -> None:
    #     self.edit.emit(customer_id)

    # @Slot(int, bool)
    # def on_filter(self, index, state) -> None:
    #     if state: 
    #         self.hide_column(index)
    #         return
    #     self.show_column(index)

    # @Slot()
    # def _on_data_changed(self) -> None:
    #     self.refresh()
