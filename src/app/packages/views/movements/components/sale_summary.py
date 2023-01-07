from typing import Callable, Dict, Tuple, List
from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import QColor, QRegularExpressionValidator
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

    root_layout = QVBoxLayout()
    ONLY_NUMBERS_VALIDATOR = QRegularExpressionValidator(QRegularExpression("[0-9]*"))

    # Error Messages
    no_customer_msg = ErrorMessage("No seleccionaste un cliente", "Por favor, seleccione un cliente para continuar.")
    no_products_msg = ErrorMessage("No hay productos seleccionados", "Por favor, seleccione al menos un producto para continuar.")
    empty_values_msg = ErrorMessage("No hay datos seleccionados", "Para registrar un movimiento, debe seleccionar un cliente y al menos un producto.")

    def __init__(self, parent, service:MovementsService):
        super(SaleSummary, self).__init__(parent)

        self.movements_service = service
        self.setup_ui()

    def setup_ui(self) -> None:
        self.object_name = "sale-summary"
        self.minimum_width = 450 
        self.error_msg = ErrorDialog(self)

        self.title = QLabel("Vista previa", alignment=Qt.AlignCenter, object_name="title")

        user_layout = QHBoxLayout()
        self.customer_name = QLabel("Nombre y apellido", alignment=Qt.AlignCenter, object_name="customer-data")
        self.customer_ruc = QLabel("RUC", alignment=Qt.AlignCenter, object_name="customer-data")
        user_layout.add_widget(self.customer_name)
        user_layout.add_widget(self.customer_ruc)

        total_layout = QHBoxLayout()
        self.total_label = QLabel("Total:", object_name="value-label")
        self.total = QLabel("Gs. 0", alignment=Qt.AlignCenter, object_name="total")
        total_layout.add_widget(self.total_label)
        total_layout.add_widget(self.total)

        self.inp_amount = QLineEdit(placeholder_text="Ingrese el monto recibido", validator=self.ONLY_NUMBERS_VALIDATOR, object_name="input-amount")
        self.inp_amount.textChanged.connect(self.calculate_change)

        change_layout = QHBoxLayout()
        self.change_label = QLabel("Su vuelto es:", object_name="value-label")
        self.change = QLabel("Gs. 0", alignment=Qt.AlignCenter, object_name="change-amount")
        change_layout.add_widget(self.change_label)
        change_layout.add_widget(self.change)

        # Button
        self.submit = QPushButton("Confirmar venta", clicked=self.on_submit, object_name="bt-save")

        self.root_layout.add_widget(self.title)
        self.root_layout.add_layout(user_layout)
        self.root_layout.add_spacing(15)
        self.root_layout.add_layout(total_layout)
        self.root_layout.add_widget(self.inp_amount)
        self.root_layout.add_layout(change_layout)
        self.root_layout.add_widget(self.submit)

        self.set_layout(self.root_layout)

    @Slot(list, int)
    def set_products_collection(self, data: list[SaleItem], total: int):
        self.products = data
        self.total_value = total

        self.inp_amount.text = str(total)
        self.total.text = f"Gs. {total}"

    @Slot(Customer)
    def set_selected_customer(self, customer: Customer):
        if not isinstance(customer, Customer):
            self.error_msg.show(self.no_customer_msg)
            return

        self.customer = customer
        
        self.customer_ruc.text = customer.ruc
        self.customer_name.text = customer.full_name
        
        self.on_data_received()

    def calculate_change(self):
        if self.inp_amount.text == "":
            self.change.text = f"Gs. {self.total_value}"
            return

        value = int(self.inp_amount.text)

        self.change_value = value - self.total_value
        self.change.text = f"Gs. {self.change_value }"

        if self.change_value < 0:
            self.submit.enabled = False
        else: self.submit.enabled = True

    def on_data_received(self):        
        if len(self.products) == 0:
            self.error_msg.show(self.no_products_msg)
            return

        self.show()

    @Slot()
    def on_submit(self):
        self.hide()
        self.movements_service.save_sales(self.products, self.customer)
