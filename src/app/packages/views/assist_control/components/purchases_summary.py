from PySide6.QtWidgets import QPushButton, QWidget, QHeaderView, QDialog, QVBoxLayout, QTableWidget, QTableWidgetItem, QLabel
from __feature__ import snake_case, true_property

from typing import Callable

from .purchase_detail import PurchaseDetailDialog

from ..classes.customer_summary import CustomerSummary
from ...movements.classes.product_sold import ProductSold

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
        header_labels: list[str] = ["Fecha", "Total", "Detalles"]

        table = QTableWidget( 
            column_count=len(header_labels), 
            horizontal_header_labels=header_labels )
        table.style_sheet = "color: white;"

        table.vertical_header().visible = False
        table.horizontal_header().stretch_last_section = True
        table.horizontal_header().set_section_resize_mode(QHeaderView.Stretch)

        return table

    def show(self, data:CustomerSummary ):
        def create_action_button(text:str, on_clicked: Callable, *args)  -> QPushButton:
            button = QPushButton(text)
            button.clicked.connect( lambda: on_clicked(*args) )
            return button

        self.table.row_count = len(data.purchases)

        for row, purchase in enumerate(data.purchases):
            self.table.set_item(row, 0, QTableWidgetItem(purchase.formatted_date()))
            self.table.set_item(row, 1, QTableWidgetItem(purchase.total()))
            self.table.set_cell_widget( 
                row, 2, create_action_button("Detalles", self.show_purchase_detail, purchase ))
        super().show()

    def show_purchase_detail(self, purchase: ProductSold):
        self.detail_dialog.show(purchase)