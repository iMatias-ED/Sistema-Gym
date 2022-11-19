from typing import Callable
from PySide6.QtWidgets import *
from PySide6.QtCore import *
from __feature__ import snake_case, true_property

# Services
from ..service import MovementsService

# Components
from ..components.select_product_quantity import SelectProductQuantityDialog

# Classes
from ..classes.product_selection import ProductSelection
from ..classes.selected_product_info import SelectedProductInfo
from ...products.classes.product import Product

class Table(QTableWidget):
    data_collected = Signal(list)
    collection: dict[str: SelectedProductInfo] = {}

    current_key: str

    def __init__(self, service: MovementsService):
        super(Table, self).__init__()
        self.movements_service = service
        self.movements_service.data_changed.connect( self.refresh )

        self.edit_dialog = SelectProductQuantityDialog(self)
        self.edit_dialog.selected.connect( self.on_product_edited )

        self.config_table()

    def config_table(self) -> None:
        self.vertical_header().visible = False
        self.column_count = len(self.movements_service.header_labels)
        self.set_horizontal_header_labels(self.movements_service.header_labels)

        self.horizontal_header().stretch_last_section = True
        self.horizontal_header().set_section_resize_mode(QHeaderView.Stretch)

    def refresh(self) -> None:
        self.clear_contents()
        self.collection.clear()

    def remove_product(self, key:str) -> None:   
        self.hide_row(self.collection[key].row)
        del self.collection[key]

    def edit_clicked(self, product: Product, key:str, quantity: int, period: str):
        self.current_key = key
        self.edit_dialog.show(product, quantity, period)

    @Slot(ProductSelection)
    def on_product_edited(self, data: ProductSelection):
        self.remove_product(self.current_key)
        self.on_product_select(data)

    @Slot(ProductSelection)
    def on_product_select(self, data: ProductSelection) -> None:
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

    @Slot()
    def on_summary_requested(self) -> None:
        self.data_collected.emit( list(self.collection.values()) )

    # Utils
    def create_action_button(self, text:str, on_clicked: Callable, *args)  -> QPushButton:
        button = QPushButton(text)
        button.clicked.connect( lambda: on_clicked(*args) )
        return button

    def insert_data(self, data: ProductSelection, key:str, row:int) -> None:
        total = f"Gs. {data.total}"
        price = f"Gs. {data.price.price}"

        self.set_cell_widget( 
            row, 0, self.create_action_button( "X", self.remove_product, key, ))
        self.set_cell_widget( 
            row, 1, self.create_action_button( "E", self.edit_clicked, data.product, key, data.quantity, data.price.name ))
        
        self.set_item( row , 2, QTableWidgetItem(data.product.name) )
        self.set_item( row , 3, QTableWidgetItem(str(data.quantity)) )
        self.set_item( row , 4, QTableWidgetItem(data.price.name) )
        self.set_item( row , 5, QTableWidgetItem(price) )
        self.set_item( row , 6, QTableWidgetItem(total) )        
