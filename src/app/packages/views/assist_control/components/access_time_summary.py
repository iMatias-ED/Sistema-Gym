from PySide6.QtWidgets import QHBoxLayout, QWidget, QDialog, QVBoxLayout, QLabel
from __feature__ import snake_case, true_property

from typing import List
from datetime import datetime

# Services
from ..service import AssistControlService

# Classes
from ...customers.classes.customer import Customer
from ....shared.components.data_table import DataTable, TableItem

class AccessTimeSummaryDialog(QDialog):
    service = AssistControlService()
    has_at_least_one_access = False

    def __init__(self, parent: QWidget):
        super(AccessTimeSummaryDialog, self).__init__(parent)
        self.setup_ui()

    def setup_ui(self):
        title_layout = QHBoxLayout()
        self.title = QLabel("Nombre")
        self.status = QLabel("Habilitado")

        title_layout.add_widget(self.title)
        title_layout.add_widget(self.status)

        self.table = self.create_table()

        layout = QVBoxLayout()
        layout.add_layout(title_layout)
        layout.add_widget(self.table)

        self.set_layout(layout)

    def show(self, data: Customer):
        self.load_data(data)
        self.status.text = str(self.has_at_least_one_access)
        
        super().show()

    def load_data(self, data:Customer):
        table_items: List[ List[TableItem] ] = []

        for info in data.access_time:
            # Check access time
            expired = datetime.now() > datetime.fromtimestamp(info.unix_time)
            if not expired: self.has_at_least_one_access = True

            # Prepare the table data
            product = self.service.get_product_by_id(info.id_product)
            table_items.append([
                TableItem( column=0, value=product.name ),
                TableItem( column=1, value=info.time ),
                TableItem( column=2, value=str(not expired) )
            ])

        self.table.insert_items(table_items)

    def create_table(self):
        table = DataTable()
        table.setup_table(
            ["Producto", "Fecha de expiración", "Cuenta con acceso"])

        return table