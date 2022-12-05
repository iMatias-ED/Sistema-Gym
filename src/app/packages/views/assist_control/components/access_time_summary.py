from PySide6.QtWidgets import QHBoxLayout, QWidget, QDialog, QVBoxLayout, QLabel
from __feature__ import snake_case, true_property

from typing import List
from datetime import datetime

# Services
from ..service import AssistControlService

# Components
from ....shared.components.summary_dialog import SummaryDialog

# Classes
from ...customers.classes.customer import Customer
from ....shared.components.data_table import DataTable, TableItem
from ....shared.classes.summary_content import SummaryContent

class AccessTimeSummaryDialog(SummaryDialog):
    service = AssistControlService()
    has_at_least_one_access = False

    def __init__(self, parent: QWidget):
        super(AccessTimeSummaryDialog, self).__init__(parent)
        self.setup_ui( SummaryContent(
                title="Nombre",
                second_title="...",
                table_headers=["Producto", "Fecha de expiración", "Cuenta con acceso"],
                bottom_label="Status"
            ))

    def show(self, data: Customer):
        self.load_data(data)
        self.has_at_least_one_access = False;
        self.bottom_label.text = str(self.has_at_least_one_access)
        
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
