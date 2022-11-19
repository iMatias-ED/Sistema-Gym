from PySide6.QtWidgets import *
from PySide6.QtCore import *
from __feature__ import snake_case, true_property

from ...shared.content_view import ContentView

# Service
from .service import MovementsService

# Componentes
from .components.table import Table
from .components.sidebar import Sidebar
from .components.add_product_by_code import AddProductByCode

from .components.summary_dialog import SummaryDialog
from .components.search_product import SearchProductDialog
from .components.search_customer import SearchCustomerDialog

class Movements(ContentView):
    service = MovementsService()
    root_layout = QHBoxLayout()
    second_layout = QVBoxLayout()

    def setup_ui(self) -> None:
        self.set_styles(__file__)

        self.table = Table(self.service)
        self.sidebar = Sidebar(self.service)
        self.code_input = AddProductByCode(self.service)

        # dialogs
        self.summary_dialog = SummaryDialog(self, self.service)
        self.search_product = SearchProductDialog(self, self.service)
        self.search_customer = SearchCustomerDialog(self, self.service)

        self.root_layout.add_layout(self.second_layout, 80)
        self.root_layout.add_widget(self.sidebar, 20)

        self.second_layout.add_widget( self.setup_title_frame(), 10 )
        self.second_layout.add_widget( self.table, 70 )
        self.second_layout.add_widget( self.code_input, 20 )

        self.set_layout(self.root_layout)
        self.__events_manager()

    def __events_manager(self) -> None:
        self.bt_search_product.clicked.connect( self.search_product.search )
                
        self.sidebar.summary_requested.connect( self.table.on_summary_requested )
        self.sidebar.summary_requested.connect( self.summary_dialog.set_selected_customer )
        self.sidebar.bt_search_customer.clicked.connect( self.search_customer.search )

        self.table.data_collected.connect( self.summary_dialog.set_products_collection )

        self.code_input.product_selected.connect( self.table.on_product_select )

        self.search_product.product_selected.connect( self.table.on_product_select )
        self.search_customer.customer_changed.connect( self.sidebar.on_customer_changed )

    def setup_title_frame(self) -> None:
        self.title = QLabel("Movimientos", alignment=Qt.AlignCenter, object_name="view-title")
        self.bt_search_product = QPushButton("B", maximum_width=50)

        layout = QHBoxLayout()
        layout.add_widget(self.bt_search_product, 10)
        layout.add_widget(self.title,  90)

        frame = QFrame()
        frame.set_layout(layout)
        return frame        


    

