from PySide6.QtCore import *
from PySide6.QtWidgets import *
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
    root_layout = QGridLayout()

    data: CustomerSummary

    def __init__(self):
        super(SummaryView, self).__init__()
        self.setup_ui()

    def setup_ui(self):
        self.name = QLabel("Matias Acosta", object_name="name" )
        self.status = QPushButton("Status", object_name="status-expired",
            clicked=self.show_access_time_summary)
        self.last_pay = QPushButton("Purchases Summary", object_name="bt-purchases-summary", clicked=self.show_purchases_summary)
        self.registered_until = QLabel("xx/xx/xxxx", object_name="registered-until")

        self.bt_go_back = QPushButton("Volver", object_name="go_back", clicked=self.emit_go_back)

        self.purchase_summary = PurchasesSummaryDialog(self)
        self.access_time_summary = AccessTimeSummaryDialog(self)

        self.root_layout.add_widget(self.bt_go_back, 1, 1, alignment=Qt.AlignCenter)
        self.root_layout.add_widget(self.name, 2, 1, alignment=Qt.AlignCenter)
        self.root_layout.add_widget(self.status, 2, 2, alignment=Qt.AlignCenter)
        self.root_layout.add_widget(self.last_pay, 3, 1, alignment=Qt.AlignCenter)
        self.root_layout.add_widget(self.registered_until, 3, 2, alignment=Qt.AlignCenter)

        self.set_layout(self.root_layout)

    def show_purchases_summary(self):
        self.purchase_summary.show(self.data)

    def show_access_time_summary(self):
        self.access_time_summary.show(self.data.customer)

    def load_data(self, ci: int):
        self.data = self.report_service.get_info(ci)

        self.name.text = self.data.customer.full_name
        self.registered_until.text = self.data.customer.access_until_date

        # for access_time in self.data.customer.access_time:
        #     product = self.report_service.get_product_by_id(access_time.id_product)
            
    def change_status_style(self, style: str):
        self.status.object_name = style

    def check_access(self, access_until: int) -> bool:
        today = datetime.now()
        access_until = datetime.fromtimestamp(access_until)

        print(f"{access_until} > {today}")
        
        return access_until >= today 

    def emit_go_back(self):
        self.go_back.emit()