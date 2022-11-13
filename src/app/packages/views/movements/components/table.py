from typing import Callable, Dict, List, Tuple
from PySide6.QtWidgets import *
from PySide6.QtCore import *
from __feature__ import snake_case, true_property

from ..service import MovementsService
from ..classes.selection import Selection
from ...products.classes.product import Product

class Table(QTableWidget):
    #Both emits the product_id
    edit = Signal(int)
    delete = Signal(int)

    def __init__(self, service: MovementsService):
        super(Table, self).__init__()
        self.movements_service = service
        self.movements_service.data_changed.connect( self.refresh )

        self.config_table()

    def config_table(self) -> None:
        self.column_count = len(self.movements_service.header_labels)
        self.set_horizontal_header_labels(self.movements_service.header_labels)

        self.horizontal_header().stretch_last_section = True
        self.horizontal_header().set_section_resize_mode(QHeaderView.Stretch)

    def refresh(self)  -> None:
        self.clear()
        self.config_table()

    def delete_clicked(self, row_index:int) -> None:
        self.remove_row(row_index)

    def create_action_button(self, text:str, product_id: int, on_clicked: Callable)  -> QPushButton:
        button = QPushButton(text)
        button.clicked.connect( lambda: on_clicked(product_id) )
        return button

    @Slot(Product)
    def on_product_select(self, data: Selection):
        self.row_count += 1
        total = f"Gs. {data.total}"
        price = f"Gs. {data.price.price}"
        
        row = self.row_count - 1
        self.set_cell_widget( row, 0, self.create_action_button( "X", row, self.delete_clicked ))
        
        self.set_item( row , 1, QTableWidgetItem(data.product.name) )
        self.set_item( row , 2, QTableWidgetItem(data.quantity) )
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
