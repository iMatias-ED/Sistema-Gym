from PySide6.QtWidgets import *
from PySide6.QtCore import *
from __feature__ import snake_case, true_property

from ..service import MovementsService
from ..classes.customer import Customer

class Sidebar(QFrame):
    root_layout = QVBoxLayout()
    info_layout = QVBoxLayout()

    def __init__(self, service: MovementsService):
        super(Sidebar, self).__init__(object_name="sidebar")
        self.service = service
        self.setup_ui()

    def setup_ui(self) -> None:
        self.bt_search_customer = QPushButton("Nombre usuario", object_name="search-button")
        self.ci = QLabel("Número de Cédula")
        self.bt_continue = QPushButton("Finalizar", object_name="bt-continue")

        self.info_layout.add_widget( self.bt_search_customer )
        self.info_layout.add_widget( self.ci )
        self.info_layout.add_stretch()
        self.info_layout.add_widget( self.bt_continue )

        self.title = QLabel('Cliente', object_name="view-title", alignment=Qt.AlignCenter)
        self.root_layout.add_widget(self.title, 10)
        self.root_layout.add_layout(self.info_layout, 90)
        
        self.set_layout(self.root_layout)

    @Slot(Customer)
    def on_customer_changed(self, c:Customer):
        self.ci.text = str(c.ci)
        self.bt_search_customer.text = c.full_name

