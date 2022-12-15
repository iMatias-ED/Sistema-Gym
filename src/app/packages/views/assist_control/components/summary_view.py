from PySide6.QtGui import QIcon
from PySide6.QtCore import QRect, Qt, Signal, QSize
from PySide6.QtWidgets import QFrame, QVBoxLayout, QPushButton, QLabel
from __feature__ import snake_case, true_property

from datetime import datetime, date

from .access_time_summary import AccessTimeSummaryDialog
from .purchases_summary import PurchasesSummaryDialog
from ..classes.customer_summary import CustomerSummary

from ..service import AssistControlService
from ...customers.service import CustomersService

class SummaryView(QFrame):
    go_back = Signal()
    customers_service = CustomersService()
    report_service = AssistControlService()
    root_layout = QVBoxLayout()

    data: CustomerSummary

    def __init__(self):
        super(SummaryView, self).__init__()
        self.setup_ui()

    def setup_ui(self):
        self.object_name = "summary-view"

        self.name = QLabel("Nombre y Apellido", object_name="name" )
        self.my_products = QPushButton("Ver mis modalidades", object_name="summary-button",clicked=self.show_access_time_summary)
        self.my_buys = QPushButton("Ver compras realizadas", object_name="summary-button", clicked=self.show_purchases_summary)
        self.bt_continue = QPushButton("Registrar Asistencia", object_name="register-button", clicked=self.register_assistance)
        
        self.status = QLabel("Habilitado", object_name="status-ok")

        self.bt_go_back = QPushButton(self, icon=QIcon("src/assets/previous.png"), object_name="go_back", clicked=self.emit_go_back)
        self.bt_go_back.icon_size = QSize(50, 50)
        self.bt_go_back.geometry = QRect(20, 20, 50, 50)

        self.purchase_summary = PurchasesSummaryDialog(self)
        self.access_time_summary = AccessTimeSummaryDialog(self)

        self.root_layout.add_spacing(70)
        self.root_layout.add_widget(self.name, 0, Qt.AlignCenter)
        self.root_layout.add_widget(self.status, 0, Qt.AlignCenter)

        self.root_layout.add_stretch()        
        self.root_layout.add_widget(self.my_products, 0, Qt.AlignCenter)
        self.root_layout.add_widget(self.my_buys, 0, Qt.AlignCenter)
        self.root_layout.add_widget(self.bt_continue, 0, Qt.AlignCenter)
        self.root_layout.add_spacing(80)

        self.set_layout(self.root_layout)

    def register_assistance(self):
        pass

    def show_purchases_summary(self):
        self.purchase_summary.show(self.data)

    def show_access_time_summary(self):
        self.access_time_summary.show(self.data.customer)

    def load_data(self, ci: int):
        self.data = self.report_service.get_info(ci)
        self.name.text = self.data.customer.full_name
            
    def change_status_style(self, style: str):
        self.my_products.object_name = style

    def check_access(self, access_until: int) -> bool:
        today = datetime.now()
        access_until = datetime.fromtimestamp(access_until)

        print(f"{access_until} > {today}")
        
        return access_until >= today 

    def emit_go_back(self):
        self.go_back.emit()