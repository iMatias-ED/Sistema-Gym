from PySide6.QtWidgets import *
from PySide6.QtCore import *
from __feature__ import snake_case, true_property

from ...shared.content_view import ContentView

# Service
from .service import MovementsService

# Componentes
from .components.sale_items_table import SaleItemsTable
from .components.right_sidebar import RightSidebarTools
from .components.add_product_by_code import AddProductByCode

from .components.sale_summary import SaleSummary
from .components.search_product import SearchProductDialog
from .components.search_customer import SearchCustomerDialog
from .components.register_movement import RegisterMovementDialog

class Movements(ContentView):
    service = MovementsService()
    root_layout = QHBoxLayout()
    second_layout = QVBoxLayout()

    def setup_ui(self) -> None:
        self.set_styles(__file__)

        self.table = SaleItemsTable(self.service)
        self.sidebar = RightSidebarTools(self.service)
        self.code_input = AddProductByCode(self.service)

        # dialogs
        self.summary_dialog = SaleSummary(self, self.service)
        self.search_product = SearchProductDialog(self, self.service)
        self.search_customer = SearchCustomerDialog(self, self.service)
        self.register_movement = RegisterMovementDialog(self, self.service)

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

        # Inflows and outflows
        self.bt_register_movement.clicked.connect(self.register_movement.show)

    def setup_title_frame(self) -> None:
        self.bt_search_product = QPushButton("B", maximum_width=50)
        self.bt_register_movement = QPushButton("Movement")

        layout = QHBoxLayout()
        layout.add_widget(self.bt_search_product)
        layout.add_widget(self.bt_register_movement)

        frame = QFrame()
        frame.set_layout(layout)
        return frame        


    

