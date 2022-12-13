from typing import List

# Service
from ..service import CustomersService

# Components | Classes
from ....shared.components.data_table import DataTable, Action
from ....shared.components.confirmation_message import ConfirmationDialog, ConfirmationMessage

class CustomersDataTable(DataTable):
    def __init__(self, service: CustomersService):
        super(CustomersDataTable, self).__init__()
        self.customers_service = service
        self.customers_service.data_changed.connect(self.refresh)

        self.setup_table(self.customers_service.header_labels)
        self.load_data()

    def load_data(self) -> None:
        self.customers = self.customers_service.get_all()

        actions: List[Action] = [
            Action(0, "X", self.delete_clicked, True, "src/assets/remove.png", "full_name", "id"),
            Action(1, "E", self.edit_clicked, True, "src/assets/edit.png", "id"),
        ]

        self.insert_values(self.customers, actions)

    def edit_clicked(self, customer_id: int) -> None:
        self.edit.emit(customer_id)

    def delete_clicked(self, customer_name:str, customer_id:int) -> None:
        ConfirmationDialog(self, lambda: self.delete(customer_id)).show(ConfirmationMessage(
            "¿Está seguro?",
            f'''Se eliminará el cliente "{customer_name}" y toda la información asociada.''',
            "Esta acción no se puede deshacer."
        ))

    def delete(self, customer_id: int) -> None:
        self.delete.emit(customer_id)
        self.customers_service.delete(customer_id)
