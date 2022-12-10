from PySide6.QtWidgets import QWidget
from __feature__ import snake_case, true_property

from typing import List
from datetime import datetime

# Services
from ..service import AssistControlService

# Components
from ....shared.components.summary_dialog import SummaryDialog

# Classes
from ...customers.classes.customer import Customer
from ....shared.classes.summary_content import SummaryContent
from ....shared.classes.table_header_label import TableHeaderLabel

class TableItem:
    product_name: str
    date: str
    has_access: bool

    def __init__(self, name: str, date: str, has_access: bool):
        self.product_name = name
        self.date = date
        self.has_access = has_access

class AccessTimeSummaryDialog(SummaryDialog):
    service = AssistControlService()
    has_at_least_one_access = False

    def __init__(self, parent: QWidget):
        super(AccessTimeSummaryDialog, self).__init__(parent)
        self.setup_ui( SummaryContent(
                "Nombre",
                "...",
                [   TableHeaderLabel("product_name", "Producto"),
                    TableHeaderLabel("date", "Fecha de expiracion"),
                    TableHeaderLabel("has_access", "Cuenta con Acceso")],
                "Status"
            ))

    def show(self, data: Customer):
        self.load_data(data)
        self.has_at_least_one_access = False;
        self.bottom_label.text = str(self.has_at_least_one_access)
        
        super().show()

    def load_data(self, data:Customer):
        table_items: List[ TableItem ] = []

        for info in data.access_time:
            # Check access time
            expired = datetime.now() > datetime.fromtimestamp(info.unix_time)
            if not expired: self.has_at_least_one_access = True

            # Prepare the table data
            product = self.service.get_product_by_id(info.id_product)
            table_items.append(TableItem(product.name, info.time, not expired))
        
        self.table.insert_values(table_items)
