from PySide6.QtWidgets import QHBoxLayout, QWidget, QDialog, QVBoxLayout, QLabel
from __feature__ import snake_case, true_property

from typing import List

# Components
from ....shared.components.summary_dialog import SummaryDialog
# Classes
from ...movements.classes.sale_record import SaleRecord
from ....shared.components.data_table import DataTable, TableItem
from ....shared.classes.summary_content import SummaryContent
from ....shared.classes.table_header_label import TableHeaderLabel

class PurchaseDetailDialog(SummaryDialog):
    def __init__(self, parent: QWidget):
        super(PurchaseDetailDialog, self).__init__(parent)

        self.setup_ui( SummaryContent(
                "Fecha de compra",
                "xx/xx/xxxx",
                [   
                    TableHeaderLabel("name", "Producto"),
                    TableHeaderLabel("quantity", "Cantidad"),
                    TableHeaderLabel("period", "Periodo"),
                    TableHeaderLabel("price", "Precio Unitario"),
                    TableHeaderLabel("total", "Total"),
                ],
                "X Registros encontrados"
            ))

    def show(self, data: SaleRecord):
        self.second_title.text = data.formatted_date()
        self.bottom_label.text = f"Gs. {data.total()}"
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
