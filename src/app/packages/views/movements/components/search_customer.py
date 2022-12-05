from typing import List
from PySide6.QtWidgets import QDialog, QLineEdit, QPushButton, QVBoxLayout, QLabel
from PySide6.QtCore import Signal, Slot, Qt
from __feature__ import snake_case, true_property

# Services 
from ..service import MovementsService

# Classes
from ...customers.classes.customer import Customer
from ....shared.components.data_table import TableItem
from ....shared.components.search_dialog import SearchDialog, SearchDialogConfig

class SearchCustomerDialog(SearchDialog):
    customer_changed = Signal(Customer)

    def __init__(self, parent, service:MovementsService):
        super(SearchCustomerDialog, self).__init__(parent)

        self.movements_service = service
        self.movements_service.data_changed.connect(self.on_data_changed) 

        self.setup_ui( SearchDialogConfig(
            title="Seleccione un cliente",
            input_placeholder="Ingrese un nombre para buscar",
            table_headers=["Nombre y Apellido", "Número de cédula"],
            slot=self.on_select
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
        table_items: List[ List[TableItem] ] = []

        for customer in self.data:
            table_items.append([
                TableItem(column=0, value=customer.full_name),
                TableItem(column=1, value=customer.ci)
            ])
        self.table.insert_items(table_items)
