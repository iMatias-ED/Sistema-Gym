from PySide6.QtCore import Signal, Slot
from __feature__ import snake_case, true_property

from typing import Dict

# Services
from ..service import MovementsService

# Components
from .configure_selected_product import ConfigureSelectedProduct

# Classes
from ..classes.sale_item import SaleItem
from ...products.classes.product import Product
from ....shared.components.data_table import SubValue, Action, DataTable

class TableSaleItem:
    row: int
    item: SaleItem

    def __init__(self, data: SaleItem, row:int):
        self.row = row
        self.item = data

    def __str__(self):
        return f"{self.row}:{self.item}"     

class SaleItemsTable(DataTable):
    total_changed = Signal(int)
    data_collected = Signal(list, int)
    collection: Dict[str, TableSaleItem] = {}

    current_key: str

    def __init__(self, service: MovementsService):
        super(SaleItemsTable, self).__init__()
        self.total = 0
        self.movements_service = service
        self.movements_service.data_changed.connect( self.refresh )

        self.edit_dialog = ConfigureSelectedProduct(self)
        self.edit_dialog.selected.connect( self.on_product_edited )

        self.setup_table(self.movements_service.header_labels)

    def refresh(self) -> None:
        self.clear_contents()
        self.collection.clear()

    def remove_product(self, key:str) -> None: 
        sale_item = self.collection[key].item

        self.total -= sale_item.price.price * sale_item.quantity 
        self.total_changed.emit(self.total)

        self.hide_row(self.collection[key].row)
        del self.collection[key]

    def edit_clicked(self, product: Product, key:str, quantity: int, period: str):
        self.current_key = key
        self.edit_dialog.show(product, quantity, period)

    @Slot(SaleItem)
    def on_product_edited(self, data: SaleItem):
        self.remove_product(self.current_key)
        self.on_product_select(data)

    @Slot(SaleItem)
    def on_product_select(self, data: SaleItem) -> None:
        key = f'{data.product.code}::{data.price.name}'

        if key not in self.collection:
            self.row_count += 1
            row = self.row_count - 1

            self.collection[key] = TableSaleItem(data, row)
            self.insert_data(data, key, row)
        else:
            info = self.collection[key]
            info.item.add(data.quantity)
            self.insert_data(info.item, key, info.row)

        self.total += data.price.price * data.quantity
        self.total_changed.emit(self.total)

    @Slot()
    def on_summary_requested(self) -> None:
        self.data_collected.emit( 
            [ data.item for data in list(self.collection.values())],
            self.total 
        )

    def insert_data(self, data: SaleItem, key:str, row:int) -> None:
        actions = [
            Action(0, "X", self.remove_product, False, "src/assets/remove.png", key),
            Action(1, "E", self.edit_clicked, False, "src/assets/edit.png",
                data.product, key, data.quantity, data.price.name )
        ]
        sub_values = {
            "product": [SubValue("product_name", "name", False)],
            "price"  : [
                SubValue("period", "name", False),
                SubValue("price", "price", False)
            ],
        }
        self.insert_value(data, row, actions, sub_values)

