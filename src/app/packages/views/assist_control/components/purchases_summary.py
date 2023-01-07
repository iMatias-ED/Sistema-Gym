from PySide6.QtWidgets import QWidget
from PySide6.QtCore import QDate
from __feature__ import snake_case, true_property

from typing import List
from ...movements.classes.sale_record import SaleRecord

# Components
from .purchase_detail import PurchaseDetailDialog
from ....shared.components.summary_dialog import SummaryDialog

# Services
from ..service import AssistControlService

# Classes
from ..classes.customer_summary import CustomerSummary
from ...movements.classes.product_sold import ProductSold
from ....shared.components.data_table import Action
from ....shared.classes.table_header_label import TableHeaderLabel
from ....shared.classes.summary_content import SummaryContent

class PurchasesSummaryDialog(SummaryDialog):

    def __init__(self, parent: QWidget):
        super(PurchasesSummaryDialog, self).__init__(parent)

        self.customer_id: int;
        self.service = AssistControlService()

        self.detail_dialog = PurchaseDetailDialog(self)

        self.setup_ui( SummaryContent(
            "Compras",
            "<date_picker>",
            [   
                TableHeaderLabel("date", "Fecha"),
                TableHeaderLabel("total", "Total"),
                TableHeaderLabel("action", "Detalles"),
            ],
            "X Registros encontrados"
        ))

    def show(self, data:CustomerSummary ):
        self.customer_id = data.customer.id
        self.date_picker.clear()
        self.insert_table_values(data.purchases)
        super().show()

    def insert_table_values(self, data: List[SaleRecord]):
        actions = [ Action(2, "D", self.show_purchase_detail, True, "src/assets/plus.png", "<self>") ]

        if len(data) == 1: pluralize = "registro encontrado"
        else: pluralize = "registros encontrados"

        self.bottom_label.text = f"{len(data)} {pluralize}."
        self.table.insert_values(data, actions)
        
    def show_purchase_detail(self, purchase: ProductSold):
        self.detail_dialog.show(purchase)

    def on_date_changed(self, date: QDate):
        date = date.to_string("dd/MM/yyyy")
        new_purchases = self.service.get_purchases(self.customer_id, date)

        self.table.clear_contents()
        self.insert_table_values(new_purchases)
