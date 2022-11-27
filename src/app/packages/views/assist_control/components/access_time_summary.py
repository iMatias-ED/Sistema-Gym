from PySide6.QtWidgets import QHBoxLayout, QPushButton, QWidget, QHeaderView, QDialog, QVBoxLayout, QTableWidget, QTableWidgetItem, QLabel
from __feature__ import snake_case, true_property

from typing import Callable
from datetime import datetime

from ..service import AssistControlService

from ...movements.classes.purchase import Purchase
from ...customers.classes.customer import Customer
from ..classes.customer_summary import CustomerSummary

class AccessTimeSummaryDialog(QDialog):

    service = AssistControlService()
    has_at_least_one_access = False

    def __init__(self, parent: QWidget):
        super(AccessTimeSummaryDialog, self).__init__(parent)
        self.setup_ui()

    def setup_ui(self):
        title_layout = QHBoxLayout()
        self.title = QLabel("Nombre")
        self.status = QLabel("Habílitado")

        title_layout.add_widget(self.title)
        title_layout.add_widget(self.status)

        self.table = self.create_table()

        layout = QVBoxLayout()
        layout.add_layout(title_layout)
        layout.add_widget(self.table)

        self.set_layout(layout)

    def show(self, data: Customer):
        self.load_data(data)
        self.status.text = str(self.has_at_least_one_access)
        
        super().show()

    def load_data(self, data:Customer):
        self.table.row_count = len(data.access_time)

        for row, info in enumerate(data.access_time):
            product = self.service.get_product_by_id(info.id_product)
            expired = datetime.now() > datetime.fromtimestamp(info.unix_time)

            self.table.set_item(row, 0, QTableWidgetItem(product.name))
            self.table.set_item(row, 1, QTableWidgetItem(info.time))
            self.table.set_item(row, 2, QTableWidgetItem(str(not expired)))

            if not self.has_at_least_one_access:
                self.has_at_least_one_access = not expired

    def create_table(self):
        header_labels: list[str] = [
            "Producto", "Fecha de expiración", "Cuenta con acceso"]

        table = QTableWidget( 
            column_count=len(header_labels), 
            horizontal_header_labels=header_labels )
        table.style_sheet = "color: gray;"

        table.vertical_header().visible = False
        table.horizontal_header().stretch_last_section = True
        table.horizontal_header().set_section_resize_mode(QHeaderView.Stretch)

        return table

    def check_access(self, access_until: int) -> bool:
        today = datetime.now()
        access_until = datetime.fromtimestamp(access_until)
                
        return access_until >= today 