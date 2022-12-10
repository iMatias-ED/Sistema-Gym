from typing import List
from PySide6.QtCore import Signal, Slot
from __feature__ import snake_case, true_property

# Services 
from ..service import MovementsService

# Classes
from ...customers.classes.customer import Customer
from ....shared.classes.table_header_label import TableHeaderLabel
from ....shared.components.search_dialog import SearchDialog, SearchDialogConfig

class SearchCustomerDialog(SearchDialog):
    customer_changed = Signal(Customer)

    def __init__(self, parent, service:MovementsService):
        super(SearchCustomerDialog, self).__init__(parent)

        self.movements_service = service
        self.movements_service.data_changed.connect(self.on_data_changed) 

        self.setup_ui( SearchDialogConfig(
            "Seleccione un cliente",
            "Ingrese un nombre para buscar",
            [ 
                TableHeaderLabel("full_name", "Nombre y Apellido"), 
                TableHeaderLabel("ci", "Número de cédula") 
            ],
            self.on_select
        ))

    # Signal Slots
    @Slot()
    def on_select(self) -> None:
        self.hide()
        self.customer_changed.emit( self.data[self.table.current_row()] )

    @Slot()
    def on_data_changed(self) -> None:
        self.hide()

    @Slot(str)
    def update_table_data(self, text:str):
        self.data = self.movements_service.search_users(text)
        self.table.insert_values(self.data)
