from PySide6.QtWidgets import QHBoxLayout, QWidget, QDialog, QVBoxLayout, QLabel
from __feature__ import snake_case, true_property

from typing import List

# Classes
from ...movements.classes.sale_record import SaleRecord
from ....shared.components.data_table import DataTable, TableItem

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

        self.total = QLabel("Gs. X")

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
        table_items: List[ List[TableItem] ] = []

        for sale in data.items:
            table_items.append([
                TableItem( column=0, value=sale.product.name ),
                TableItem( column=1, value=sale.quantity ),
                TableItem( column=2, value=sale.period ),
                TableItem( column=3, value=sale.price ),
                TableItem( column=4, value=sale.total ),
            ])
        self.table.insert_items(table_items)

    def create_table(self):
        table = DataTable()
        table.setup_table(["Producto", "Cantidad", "Periodo", "Precio Unitario", "Total"])
        return table