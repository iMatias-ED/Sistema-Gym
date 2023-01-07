from PySide6.QtWidgets import QWidget, QVBoxLayout, QDialog, QLabel
from PySide6.QtCore import Qt
from __feature__ import snake_case, true_property

from typing import List

from ...classes.cash_flow_item import CashFlowItem
from .....shared.components.data_table import DataTable, TableHeaderLabel

class CashFlowDialog(QDialog):

    def __init__(self, parent: QWidget):
        super(CashFlowDialog, self).__init__(parent)
        self.object_name = "cash-flow-summary-dialog"
        self.root_layout = QVBoxLayout()
        
        self.header_labels = [
            TableHeaderLabel("user_name", "Registrado por"),
            TableHeaderLabel("amount", "Monto"),
            TableHeaderLabel("description", "Detalle"),
            TableHeaderLabel("date", "Fecha del registro"),
        ]

        self.setup_ui()

    def setup_ui(self):
        self.minimum_width = 600
        self.title = QLabel("Entradas de dinero", alignment=Qt.AlignCenter)
        
        self.table = DataTable()
        self.table.minimum_height = 300
        self.table.setup_table(self.header_labels)

        self.root_layout.add_widget(self.title)
        self.root_layout.add_widget(self.table)

        self.set_layout(self.root_layout)

    def show(self, title: str, data: List[CashFlowItem]):
        self.title.text = title
        self.table.insert_values( data )

        super().show()
