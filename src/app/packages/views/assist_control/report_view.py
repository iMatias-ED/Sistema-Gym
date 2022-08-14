from ctypes import alignment
from PySide6.QtCore import *
from PySide6.QtWidgets import *
from __feature__ import snake_case, true_property

from ..customers.service import *

class ReportView(QFrame):
    customers_service = CustomersService
    root_layout = QGridLayout()

    def __init__(self):
        super(ReportView, self).__init__()
        self.setup_ui()

    def setup_ui(self):
        self.name = QLabel("Matias Acosta", object_name="name" )
        self.status = QLabel("Habilitado", object_name="status")
        self.last_pay = QLabel("31/10/2022", object_name="last-pay")
        self.registered_until = QLabel("31/11/2022", object_name="registered-until")

        self.root_layout.add_widget(self.name, 1, 1, alignment=Qt.AlignCenter)
        self.root_layout.add_widget(self.status, 1, 2, alignment=Qt.AlignCenter)
        self.root_layout.add_widget(self.last_pay, 2, 1, alignment=Qt.AlignCenter)
        self.root_layout.add_widget(self.registered_until, 2, 2, alignment=Qt.AlignCenter)

        self.set_layout(self.root_layout)