from PySide6.QtWidgets import QWidget, QDialog, QVBoxLayout, QLabel
from __feature__ import snake_case, true_property

from typing import List, Union

# Components
from .purchase_detail import PurchaseDetailDialog
from ....shared.components.summary_dialog import SummaryDialog

# Classes
from ..classes.customer_summary import CustomerSummary
from ...movements.classes.product_sold import ProductSold
from ....shared.components.data_table import DevAction, DataTable, TableItem, Action
from ....shared.classes.table_header_label import TableHeaderLabel
from ....shared.classes.summary_content import SummaryContent

class PurchasesSummaryDialog(SummaryDialog):
    def __init__(self, parent: QWidget):
        super(PurchasesSummaryDialog, self).__init__(parent)
        
        self.detail_dialog = PurchaseDetailDialog(self)

        self.setup_ui( SummaryContent(
            "Compras",
            "Filtro",
            [   
                TableHeaderLabel("formatted_date", "Fecha"),
                TableHeaderLabel("total", "Total"),
                TableHeaderLabel("action", "Detalles"),
            ],
            "X Registros encontrados"
        ))

    def show(self, data:CustomerSummary ):
        actions = [ DevAction(2, "D", self.show_purchase_detail, True, "<self>") ]

        self.table.test_insert(data.purchases, actions)
        super().show()

    def show_purchase_detail(self, purchase: ProductSold):
        self.detail_dialog.show(purchase)