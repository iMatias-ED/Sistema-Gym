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
    status_text: str

    def __init__(self, name: str, date: str, has_access: bool):
        self.product_name = name
        self.date = date
        self.has_access = has_access

        if has_access: self.status_text = "Si"
        else: self.status_text = "No"

class AccessTimeSummaryDialog(SummaryDialog):
    service = AssistControlService()
    has_at_least_one_access = False

    def __init__(self, parent: QWidget):
        super(AccessTimeSummaryDialog, self).__init__(parent)
        self.setup_ui( SummaryContent(
                "Matías Acosta",
                "",
                [   TableHeaderLabel("product_name", "Producto"),
                    TableHeaderLabel("date", "Fecha de expiracion"),
                    TableHeaderLabel("status_text", "Cuenta con Acceso")],
                "Habilitado"
            ))

    def show(self, data: Customer):
        self.load_data(data)

        if self.has_at_least_one_access: 
            status = "Habilitado"
            self.bottom_label.style_sheet = "color: #1DBF53" 
        else: 
            status = "No habilitado"
            self.bottom_label.style_sheet = "color: #F20600" 
        
        self.bottom_label.text = status
        
        self.has_at_least_one_access = False;
        super().show()

    def load_data(self, data:Customer):
        table_items: List[ TableItem ] = []

        for info in data.access_time:
            # Check access time
            expired = datetime.now() > info.expiration_as_date()
            if not expired: self.has_at_least_one_access = True

            # Prepare the table data
            product = self.service.get_product_by_id(info.id_product)
            table_items.append(TableItem(product.name, info.access_until_date, not expired))
        
        self.table.insert_values(table_items)
