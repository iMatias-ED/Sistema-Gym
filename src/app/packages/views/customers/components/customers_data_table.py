from typing import List

# Service
from ..service import CustomersService

# Components | Classes
from ....shared.components.data_table import DataTable, DevAction, TableItem, Action


class CustomersDataTable(DataTable):
    def __init__(self, service: CustomersService):
        super(CustomersDataTable, self).__init__()
        self.customers_service = service
        self.customers_service.data_changed.connect(self.refresh)

        self.setup_dev(self.customers_service.header_labels2)
        self.load_data()

    def load_data(self) -> None:
        self.customers = self.customers_service.get_all()

        actions: List[DevAction] = [
            DevAction(0, "X", self.delete_clicked, True, "id"),
            DevAction(1, "E", self.edit_clicked, True, "id"),
        ]

        self.test_insert(self.customers, actions)

    def edit_clicked(self, customer_id: int) -> None:
        self.edit.emit(customer_id)

    def delete_clicked(self, customer_id: int) -> None:
        self.delete.emit(customer_id)
        self.customers_service.delete(customer_id)
