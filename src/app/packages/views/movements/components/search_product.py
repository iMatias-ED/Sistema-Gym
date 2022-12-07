from PySide6.QtCore import Signal, Slot
from __feature__ import snake_case, true_property

# Services
from ..service import MovementsService

# Classes
from ..classes.sale_item import SaleItem
from ....shared.classes.table_header_label import TableHeaderLabel
from ....shared.components.search_dialog import SearchDialog, SearchDialogConfig

# Components
from .configure_selected_product import ConfigureSelectedProduct

class SearchProductDialog (SearchDialog):
    product_selected = Signal(SaleItem)

    def __init__(self, parent, service:MovementsService):
        super(SearchProductDialog, self).__init__(parent)

        self.movements_service = service

        self.setup_ui( SearchDialogConfig(
            "Seleccione un producto",
            "Ingrese un nombre para buscar",
            [ TableHeaderLabel("name", "Nombre del producto") ],
            self.on_product_selected
        ))
        self.quantity_dialog = ConfigureSelectedProduct(self)
        self.quantity_dialog.selected.connect(self.on_selection_finished)

    # Signal Slots
    @Slot()
    def on_product_selected(self) -> None:
        self.quantity_dialog.show(self.data[self.table.current_row()])
        
    @Slot(str)
    def update_table_data(self, text:str):
        self.data = self.movements_service.search_products(text)
        self.table.test_insert( self.data )

    @Slot(SaleItem)
    def on_selection_finished(self, data: SaleItem):
        self.product_selected.emit(data)
        self.close()

