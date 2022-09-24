from PySide6.QtWidgets import *
from PySide6.QtCore import *
from __feature__ import snake_case, true_property

from ...shared.content_view import ContentView

# Service
from .service import MovementsService

# Componentes
from .components.table import Table
from .components.sidebar import Sidebar
from .components.dialog import Dialog

from .components.search_customer import SearchCustomerDialog

class Movements(ContentView):
    service = MovementsService()
    root_layout = QHBoxLayout()
    second_layout = QVBoxLayout()

    def setup_ui(self) -> None:
        self.set_styles(__file__)

        self.table = Table(self.service)
        self.dialog = Dialog(self, self.service)
        self.sidebar = Sidebar(self.service)

        # Search dialogs
        self.search_customer = SearchCustomerDialog(self, self.service)

        self.root_layout.add_layout(self.second_layout, 80)
        self.root_layout.add_widget(self.sidebar, 20)
        self.root_layout.add_child_widget(self.dialog)

        self.second_layout.add_widget( self.setup_title_frame(), 10 )
        self.second_layout.add_widget( self.table, 90 )

        self.set_layout(self.root_layout)
        self.__events_manager()

    def __events_manager(self) -> None:
        self.bt_search_product.clicked.connect( self.dialog.create )
        
        self.table.edit.connect( self.dialog.edit )
        
        self.search_customer.customer_changed.connect( self.sidebar.on_customer_changed )
        self.sidebar.bt_search_customer.clicked.connect( self.search_customer.search )

    def setup_title_frame(self) -> None:
        self.title = QLabel("Movimientos", alignment=Qt.AlignCenter, object_name="view-title")
        self.bt_search_product = QPushButton("B", maximum_width=50)

        layout = QHBoxLayout()
        layout.add_widget(self.bt_search_product, 10)
        layout.add_widget(self.title,  90)

        frame = QFrame()
        frame.set_layout(layout)
        return frame        


    

