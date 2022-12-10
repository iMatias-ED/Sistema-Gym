from PySide6.QtWidgets import QWidget
from __feature__ import snake_case, true_property

# Components
from .purchase_detail import PurchaseDetailDialog
from ....shared.components.summary_dialog import SummaryDialog

# Classes
from ..classes.customer_summary import CustomerSummary
from ...movements.classes.product_sold import ProductSold
from ....shared.components.data_table import Action
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
        actions = [ Action(2, "D", self.show_purchase_detail, True, "<self>") ]

        self.table.insert_values(data.purchases, actions)
        super().show()

    def show_purchase_detail(self, purchase: ProductSold):
        self.detail_dialog.show(purchase)