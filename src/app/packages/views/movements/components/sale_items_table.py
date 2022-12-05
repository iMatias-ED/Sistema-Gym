from PySide6.QtCore import Signal, Slot
from __feature__ import snake_case, true_property

from typing import Tuple

# Services
from ..service import MovementsService

# Components
from .configure_selected_product import ConfigureSelectedProduct

# Classes
from ..classes.sale_item import SaleItem
from ....shared.components.data_table import DataTable, Action, TableItem

class TableSaleItem:
    row: int
    item: SaleItem

    def __init__(self, data: SaleItem, row:int):
        self.row = row
        self.item = data

    def __str__(self):
        return f"{self.row}:{self.item}"     

class SaleItemsTable(DataTable):
    data_collected = Signal(list)
    collection: dict[str: TableSaleItem] = {}

    current_key: str

    def __init__(self, service: MovementsService):
        super(SaleItemsTable, self).__init__()
        self.movements_service = service
        self.movements_service.data_changed.connect( self.refresh )

        self.edit_dialog = ConfigureSelectedProduct(self)
        self.edit_dialog.selected.connect( self.on_product_edited )

        self.setup_table(self.movements_service.header_labels)

    def refresh(self) -> None:
        self.clear_contents()
        self.collection.clear()

    def remove_product(self, key:str) -> None:   
        self.hide_row(self.collection[key].row)
        del self.collection[key]

    # def edit_clicked(self, product: Product, key:str, quantity: int, period: str):
    def edit_clicked(self, data: Tuple):
        product, key, quantity, period = data
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

    @Slot()
    def on_summary_requested(self) -> None:
        self.data_collected.emit( 
            [ data.item for data in list(self.collection.values())] 
        )

    def insert_data(self, data: SaleItem, key:str, row:int) -> None:
        total = f"Gs. {data.total}"
        price = f"Gs. {data.price.price}"

        self.insert_item([
            Action(column=0, label="X", slot=self.remove_product, params=key),
            Action(column=1, label="E", slot=self.edit_clicked, 
                params=(data.product, key, data.quantity, data.price.name) ),
            TableItem( column=2, value=data.product.name ),
            TableItem( column=3, value=data.quantity ),
            TableItem( column=4, value=data.price.name ),
            TableItem( column=5, value=price ),
            TableItem( column=6, value=total )
        ], row)
