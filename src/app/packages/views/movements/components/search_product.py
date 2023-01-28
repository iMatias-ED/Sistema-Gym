from PySide6.QtCore import Signal, Slot
from __feature__ import snake_case, true_property

from typing import Union

# Services
from ..service import MovementsService

# Classes
from ..classes.sale_item import SaleItem
from ...products.classes.product import Product
from ....shared.classes.table_header_label import TableHeaderLabel
from ....shared.components.search_dialog import SearchDialog, SearchDialogConfig

# Components
from .configure_selected_product import ConfigureSelectedProduct

class SearchProductDialog (SearchDialog):
    product_selected = Signal(Product)
    selection_finished = Signal(SaleItem)

    def __init__(self, parent, service:MovementsService):
        super(SearchProductDialog, self).__init__(parent)

        self.movements_service = service
        self.request_only_product = False

        self.setup_ui( SearchDialogConfig(
            "Seleccione un producto",
            "Ingrese un nombre para buscar",
            [ TableHeaderLabel("name", "Nombre del producto") ],
            self.on_product_selected
        ))
        self.quantity_dialog = ConfigureSelectedProduct(self)
        self.quantity_dialog.selected.connect(self.on_selection_finished)

    # @Override
    def search(self, request_only_product: bool = False): 
        self.request_only_product = request_only_product
        self.show()

    # Signal Slots
    @Slot()
    def on_product_selected(self) -> None:
        product = self.data[self.table.current_row()]

        if self.request_only_product:
            self.product_selected.emit(product)
            self.close()
        else: self.quantity_dialog.show(product)
        
    @Slot(str)
    def update_table_data(self, text:str):
        self.data = self.movements_service.search_products(text)
        self.table.insert_values( self.data )

    @Slot(SaleItem)
    def on_selection_finished(self, data: SaleItem):
        self.selection_finished.emit(data)
        self.close()

