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
        self.SIDEBAR = Sidebar()
        self.SIDEBAR.example()        
        self.table = Table()
        self.table.example()
        self.dialog = Dialog()

        self.root_layout.add_layout(self.second_layout, 80)
        self.root_layout.add_widget(self.SIDEBAR, 20)

        self.second_layout.add_widget( self.setup_title_frame(), 10 )
        self.second_layout.add_widget( self.table, 90 )

        self.set_layout(self.root_layout)

    def setup_title_frame(self):
        self.title = QLabel("Clientes", alignment=Qt.AlignCenter)
        self.button = QPushButton("+", maximum_width=50)
        self.button.clicked.connect(lambda: self.dialog.example('create'))

        layout = QHBoxLayout()
        layout.add_widget(self.button, 10)
        layout.add_widget(self.title,  90)

        frame = QFrame()
        frame.set_layout(layout)
        return frame        
    

