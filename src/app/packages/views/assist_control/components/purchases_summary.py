from PySide6.QtWidgets import QWidget, QDialog, QVBoxLayout, QLabel
from __feature__ import snake_case, true_property

from typing import List, Union

# Components
from .purchase_detail import PurchaseDetailDialog

# Classes
from ..classes.customer_summary import CustomerSummary
from ...movements.classes.product_sold import ProductSold
from ....shared.components.data_table import DataTable, TableItem, Action

class PurchasesSummaryDialog(QDialog):
    def __init__(self, parent: QWidget):
        super(PurchasesSummaryDialog, self).__init__(parent)
        self.setup_ui()
    
    def setup_ui(self):
        self.title = QLabel("Titulo")
        self.table = self.create_table()
        self.detail_dialog = PurchaseDetailDialog(self)

        layout = QVBoxLayout()
        layout.add_widget(self.title)
        layout.add_widget(self.table)
        self.set_layout(layout)

    def create_table(self):
        table = DataTable()
        table.setup_table(["Fecha", "Total", "Detalles"])
        return table

    def show(self, data:CustomerSummary ):
        table_items: List[ List[ Union[TableItem, Action] ] ] = []

        for purchase in data.purchases:
            table_items.append( [
                TableItem( column=0, value=purchase.formatted_date() ),
                TableItem( column=1, value=purchase.total() ),
                Action   ( column=2, label="D", 
                    slot=self.show_purchase_detail, params=purchase)
            ])

        self.table.insert_items(table_items)
        super().show()

    def show_purchase_detail(self, purchase: ProductSold):
        self.detail_dialog.show(purchase)