from PySide6.QtWidgets import *
from PySide6.QtCore import *
from __feature__ import snake_case, true_property

from ...shared.content_view import ContentView
from .table import Table
from .sidebar import Sidebar
from .dialog import Dialog

class Customers(ContentView):
    root_layout = QHBoxLayout()
    second_layout = QVBoxLayout()

    def setup_ui(self):
        self.sidebar = Sidebar()
        self.table = Table()
        self.dialog = Dialog()

        self.root_layout.add_layout(self.second_layout, 80)
        self.root_layout.add_widget(self.sidebar, 20)

        self.second_layout.add_widget( self.setup_title_frame(), 10 )
        self.second_layout.add_widget( self.table, 90 )

        self.set_layout(self.root_layout)
        self.__events_manager()

    def __events_manager(self):
        self.bt_create.clicked.connect( self.dialog.create )
        
        # Views Events
        self.table.edit.connect( self.dialog.edit )
        self.table.delete.connect( self.__on_delete )
        self.sidebar.filter_event.connect( self.table.on_filter )

    def setup_title_frame(self):
        self.title = QLabel("Clientes", alignment=Qt.AlignCenter)
        self.bt_create = QPushButton("+", maximum_width=50)

        layout = QHBoxLayout()
        layout.add_widget(self.bt_create, 10)
        layout.add_widget(self.title,  90)

        frame = QFrame()
        frame.set_layout(layout)
        return frame        

    @Slot(int)
    def __on_delete(self, row):
        print(f"On delete. Row {row}")
    

