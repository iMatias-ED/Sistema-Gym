from PySide6.QtWidgets import QHBoxLayout, QPushButton, QWidget, QHeaderView, QDialog, QVBoxLayout, QTableWidget, QTableWidgetItem, QLabel
from __feature__ import snake_case, true_property

from typing import Callable

from ...movements.classes.sale_record import SaleRecord
from ..classes.customer_summary import CustomerSummary

class PurchaseDetailDialog(QDialog):
    def __init__(self, parent: QWidget):
        super(PurchaseDetailDialog, self).__init__(parent)
        self.setup_ui()

    def setup_ui(self):
        title_layout = QHBoxLayout()
        self.title = QLabel("Fecha de compra:")
        self.date = QLabel("xx/xx/xxxx")

        title_layout.add_widget(self.title)
        title_layout.add_widget(self.date)

        self.table = self.create_table()

        self.total = QLabel("Gs. 10000")

        layout = QVBoxLayout()
        layout.add_layout(title_layout)
        layout.add_widget(self.table)
        layout.add_widget(self.total)

        self.set_layout(layout)

    def show(self, data: SaleRecord):
        self.date.text = data.formatted_date()
        self.total.text = f"Gs. {data.total()}"
        self.load_data(data)
        
        super().show()

    def load_data(self, data:SaleRecord):
        self.table.row_count = len(data.items)

        for row, product in enumerate(data.items):
            self.table.set_item(row, 0, QTableWidgetItem(product.product.name))
            self.table.set_item(row, 1, QTableWidgetItem(str(product.quantity)))
            self.table.set_item(row, 2, QTableWidgetItem(product.period))
            self.table.set_item(row, 3, QTableWidgetItem(str(product.price)))
            self.table.set_item(row, 4, QTableWidgetItem(str(product.total)))

    def create_table(self):
        header_labels: list[str] = [
            "Producto", "Cantidad", "Periodo", "Precio Unitario", "Total"]

        table = QTableWidget( 
            column_count=len(header_labels), 
            horizontal_header_labels=header_labels )
        table.style_sheet = "color: gray;"

        table.vertical_header().visible = False
        table.horizontal_header().stretch_last_section = True
        table.horizontal_header().set_section_resize_mode(QHeaderView.Stretch)

        return table