from PySide6.QtWidgets import QHBoxLayout, QVBoxLayout, QFrame, QLabel, QPushButton, QSizePolicy
from PySide6.QtCore import Qt
from __feature__ import snake_case, true_property

from ...shared.content_view import ContentView

# Service
from .service import CustomersService

# Componentes
from .components.customers_data_table import CustomersDataTable
from .components.configure_customer_data import ConfigureCustomerDialog
from ...shared.components.table_columns_filter import TableColumnsFilter

class Customers(ContentView):
    service = CustomersService()
    root_layout = QHBoxLayout()
    second_layout = QVBoxLayout()

    def setup_ui(self) -> None:
        self.set_styles(__file__)

        self.table = CustomersDataTable(self.service)
        self.dialog = ConfigureCustomerDialog(self, self.service)
        self.sidebar = TableColumnsFilter([ h.label for h in self.service.header_labels ])

        self.root_layout.add_layout(self.second_layout, 85)
        self.root_layout.add_widget(self.sidebar, 15)
        self.root_layout.add_child_widget(self.dialog)

        self.second_layout.add_widget( self.setup_title_frame(), 10 )
        self.second_layout.add_widget( self.table, 90 )

        self.set_layout(self.root_layout)
        self.__events_manager()

    def __events_manager(self) -> None:
        self.bt_create.clicked.connect( self.dialog.create )
        
        self.table.edit.connect( self.dialog.edit )
        self.sidebar.filter_event.connect( self.table.on_filter )

    def setup_title_frame(self) -> None:
        self.bt_create = QPushButton("Nuevo cliente", object_name="bt-title-section")

        layout = QHBoxLayout()
        layout.add_widget(self.bt_create, 10, Qt.AlignLeft)

        frame = QFrame()
        frame.set_layout(layout)
        return frame        


    

