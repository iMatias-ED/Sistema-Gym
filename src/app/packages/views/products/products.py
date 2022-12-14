from PySide6.QtWidgets import *
from PySide6.QtCore import *
from __feature__ import snake_case, true_property

from ...shared.content_view import ContentView

# Service
from .service import ProductsService

# Componentes
from .components.product_data_table import ProductDataTable
from .components.configure_product_data import ConfigureProductData
from ...shared.components.table_columns_filter import TableColumnsFilter

class Products(ContentView):
    service = ProductsService()
    root_layout = QHBoxLayout()
    second_layout = QVBoxLayout()

    def setup_ui(self) -> None:
        self.set_styles(__file__)

        self.table = ProductDataTable(self.service)
        self.dialog = ConfigureProductData(self, self.service)
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
        self.bt_create = QPushButton("Nuevo producto", object_name="bt-title-section")

        layout = QHBoxLayout()
        layout.add_widget(self.bt_create, 10, Qt.AlignLeft)

        frame = QFrame()
        frame.set_layout(layout)
        return frame        


    

