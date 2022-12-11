from typing import Callable, Dict, Tuple, List
from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import QColor
from __feature__ import snake_case, true_property

# Services 
from ..service import MovementsService

# Components
from ....shared.components.error_message import ErrorDialog

# Classes
from ..classes.sale_item import SaleItem
from ...customers.classes.customer import Customer
from ....shared.classes.error_message import ErrorMessage

class SaleSummary(QDialog):
    products: list[SaleItem]
    customer: Customer = None;

    root_layout = QGridLayout()

    # Error Messages
    no_customer_msg = ErrorMessage("No seleccionaste un cliente", "Por favor, seleccione un cliente para continuar.")
    no_products_msg = ErrorMessage("No hay productos seleccionados", "Por favor, seleccione al menos un producto para continuar.")
    empty_values_msg = ErrorMessage("No hay datos seleccionados", "Para registrar un movimiento, debe seleccionar un cliente y al menos un producto.")

    def __init__(self, parent, service:MovementsService):
        super(SaleSummary, self).__init__(parent)

        self.movements_service = service
        self.setup_ui()

    def setup_ui(self) -> None:
        self.minimum_width = 450 
        self.error_msg = ErrorDialog(self)

        self.title    = self._create_title("Resumen", self.last_row())
        self.title    = self._create_title("Gs 100.000", self.last_row(), "monto-total")
        self.inp_name = self._create_input("Ingrese un nombre para buscar", self.last_row(), "search-input")

        # Button
        self.submit = QPushButton("Seleccionar", clicked=self.on_submit)
        self.root_layout.add_widget(self.submit, self.last_row(), 1, self.last_row(), 2)

        self.set_layout(self.root_layout)

    @Slot(list)
    def set_products_collection(self, data: list[SaleItem]):
        self.products = data

    @Slot(Customer)
    def set_selected_customer(self, customer: Customer):
        self.customer = customer
        self.on_data_received()

    def on_data_received(self):
        if self.customer is None and len(self.products) == 0:
            self.error_msg.show(self.empty_values_msg)
            return
        
        if self.customer is None:
            self.error_msg.show(self.no_customer_msg)
            return
            
        if len(self.products) == 0:
            self.error_msg.show(self.no_products_msg)
            return

        self.show()

    @Slot()
    def on_submit(self):
        self.hide()
        self.movements_service.save_sales(self.products, self.customer)

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
