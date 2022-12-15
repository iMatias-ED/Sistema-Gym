from PySide6.QtWidgets import QFrame, QVBoxLayout, QPushButton, QLabel
from PySide6.QtCore import Signal, Slot, Qt
from __feature__ import snake_case, true_property

from datetime import datetime

# Services
from ..service import MovementsService

# Classes
from ...customers.classes.customer import Customer

class RightSidebarTools(QFrame):
    summary_requested = Signal(Customer)
    root_layout = QVBoxLayout()
    info_layout = QVBoxLayout()

    current_customer: Customer = None

    def __init__(self, service: MovementsService):
        super(RightSidebarTools, self).__init__(object_name="preview-sidebar")
        self.service = service
        self.setup_ui()

    def setup_ui(self) -> None:
        self.bt_search_customer = QPushButton("Seleccione un cliente", object_name="bt-search-customer")
        
        self.ci = QLabel(object_name="data")
        self.ruc = QLabel(object_name="data")
        
        self.bt_continue = QPushButton("Finalizar", object_name="bt-continue", clicked=self.on_continue_clicked)
        
        self.info_layout.add_widget( self.bt_search_customer )
        self.info_layout.add_widget( self.ci )
        self.info_layout.add_widget( self.ruc )
        self.info_layout.add_stretch()
        self.info_layout.add_widget( self.bt_continue )
        self.info_layout.add_spacing(42)

        self.title = QLabel('Información del cliente', object_name="title", alignment=Qt.AlignCenter)
        self.root_layout.add_widget(self.title, 10)
        self.root_layout.add_layout(self.info_layout, 90)
        
        self.set_layout(self.root_layout)

    @Slot()
    def on_continue_clicked(self):
        self.summary_requested.emit(self.current_customer)

    @Slot(Customer)
    def on_customer_changed(self, c:Customer):
        self.current_customer = c
        self.ci.text = f"CI: {c.ci}"
        self.ruc.text = f"RUC: {c.ruc}"

        self.bt_search_customer.text = c.full_name

