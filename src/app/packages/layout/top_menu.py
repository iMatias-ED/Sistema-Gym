from PySide6.QtCore import Signal
from PySide6.QtWidgets import QFrame, QHBoxLayout, QPushButton, QSizePolicy
from __feature__ import snake_case, true_property

class TopMenu(QFrame):
    view_change = Signal(int)
    
    def __init__(self):
        super(TopMenu, self).__init__()
        self.object_name = "top-menu"
        self.setup_ui()

    def setup_ui(self):
        size_policy = QSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding)

        # Create buttons 
        self.__bt_logo = QPushButton("Logo / Panel de control", size_policy=size_policy)
        self.__bt_movements = QPushButton("Movimientos", size_policy=size_policy)
        self.__bt_customers = QPushButton("Clientes", size_policy=size_policy)
        self.__bt_products = QPushButton("Productos", size_policy=size_policy)
        self.__bt_assistance = QPushButton("Marcar asistencia", size_policy=size_policy)

        self.__bind_buttons()

        # Create Layout
        buttons_layout = QHBoxLayout()

        # Add Buttons to Layout
        buttons_layout.add_widget(self.__bt_logo)
        buttons_layout.add_widget(self.__bt_movements)
        buttons_layout.add_widget(self.__bt_customers)
        buttons_layout.add_widget(self.__bt_products)
        buttons_layout.add_widget(self.__bt_assistance)

        # Add layout to frame
        self.set_layout(buttons_layout)

    def button_clicked(self, value: int):
        self.view_change.emit( value )

    def __bind_buttons(self):
        self.__bt_movements.clicked.connect(lambda: self.button_clicked(0) ) 
        self.__bt_customers.clicked.connect(lambda: self.button_clicked(1) ) 
        self.__bt_products.clicked.connect(lambda: self.button_clicked(2) ) 
        self.__bt_assistance.clicked.connect(lambda: self.button_clicked(3) ) 
        self.__bt_logo.clicked.connect(lambda: self.button_clicked(4) ) 

