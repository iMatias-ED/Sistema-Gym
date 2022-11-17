from typing import Callable, Dict, Tuple, List
from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import QColor
from __feature__ import snake_case, true_property

# Services 
from ..service import MovementsService

# Classes
from ...customers.classes.customer import Customer
from ..classes.selected_product_info import SelectedProductInfo

class SummaryDialog(QDialog):
    data: list[SelectedProductInfo]
    customer: Customer = None;

    root_layout = QGridLayout()

    def __init__(self, parent, service:MovementsService):
        super(SummaryDialog, self).__init__(parent)

        self.movements_service = service

        self.setup_ui()
        # self.set_window_flags(Qt.FramelessWindowHint)

    def setup_ui(self) -> None:
        self.minimum_width = 450 

        self.title    = self._create_title("Resumen", self.last_row())
        self.title    = self._create_title("Gs 100.000", self.last_row(), "monto-total")
        self.inp_name = self._create_input("Ingrese un nombre para buscar", self.last_row(), "search-input")

        # Button
        self.submit = QPushButton("Seleccionar", clicked=self.on_submit)
        self.root_layout.add_widget(self.submit, self.last_row(), 1, self.last_row(), 2)

        self.set_layout(self.root_layout)

    @Slot(Customer)
    def on_summary_requested(self, customer: Customer):
        self.customer = customer

    @Slot(list)
    def show_summary(self, data: list[SelectedProductInfo]):
        self.data = data
        self.show()

    @Slot()
    def on_submit(self):
        self.movements_service.save_sales(self.data, self.customer)

    # Widgets Creations
    def _create_title(self, text:str, row:int, obj_name:str = "") -> QLabel:
        title = QLabel(text, alignment=Qt.AlignCenter, object_name=obj_name)
        self.root_layout.add_widget(title, row, 1, row, 2)
        return title

    def last_row(self) -> int:
        return self.root_layout.row_count()

    def _create_input(self, placeholder:str, row:int, obj_name:str = "") -> QLineEdit:
        line_edit = QLineEdit( placeholder_text=placeholder, object_name=obj_name)

        self.root_layout.add_widget(line_edit, row, 1, row, 2)

        return line_edit
