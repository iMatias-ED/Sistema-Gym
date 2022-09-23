from PySide6.QtCore import *
from PySide6.QtWidgets import *
from __feature__ import snake_case, true_property

from datetime import datetime, date

from ..customers.service import CustomersService
from ..customers.classes.customer import Customer

class ReportView(QFrame):
    go_back = Signal()
    customers_service = CustomersService()
    root_layout = QGridLayout()

    def __init__(self):
        super(ReportView, self).__init__()
        self.setup_ui()

    def setup_ui(self):
        self.name = QLabel("Matias Acosta", object_name="name" )
        self.status = QLabel("Habilitado", object_name="status-expired")
        self.last_pay = QLabel("i'm a button", object_name="last-pay")
        self.registered_until = QLabel("31/11/2022", object_name="registered-until")

        self.bt_go_back = QPushButton("Volver", object_name="go_back", clicked=self.emit_go_back)

        self.root_layout.add_widget(self.bt_go_back, 1, 1, alignment=Qt.AlignCenter)
        self.root_layout.add_widget(self.name, 2, 1, alignment=Qt.AlignCenter)
        self.root_layout.add_widget(self.status, 2, 2, alignment=Qt.AlignCenter)
        self.root_layout.add_widget(self.last_pay, 3, 1, alignment=Qt.AlignCenter)
        self.root_layout.add_widget(self.registered_until, 3, 2, alignment=Qt.AlignCenter)

        self.set_layout(self.root_layout)

    def load_data(self, ci: int):
        c = self.customers_service.get_by_ci_number(ci)

        self.name.text = c.full_name
        self.registered_until.text = c.access_until_date

        if self.check_access(c.access_until_date):
            self.status.text = "Habilitado"
            self.change_status_style("status-ok")
        else:
            self.status.text = "Inhabilitado"
            self.change_status_style("status-expired")

        print(self.status.object_name)

    def change_status_style(self, style: str):
        self.status.object_name = style

    def check_access(self, _date: str) -> bool:
        today = datetime.strptime(date.today().strftime('%d/%m/%Y'), '%d/%m/%Y')
        access_until = datetime.strptime( _date, '%d/%m/%Y' )
        
        return access_until >= today 

    def emit_go_back(self):
        self.go_back.emit()