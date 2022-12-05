from typing import List
from PySide6.QtWidgets import QDialog, QLineEdit, QPushButton, QVBoxLayout, QLabel
from PySide6.QtCore import Signal, Slot, Qt
from __feature__ import snake_case, true_property

# Services 
from ..service import MovementsService

# Classes
from ....shared.components.data_table import DataTable, TableItem
from ...customers.classes.customer import Customer

class SearchCustomerDialog(QDialog):
    customer_changed = Signal(Customer)

    root_layout = QVBoxLayout()
    inputs_collection: List[ QLineEdit ] = []

    def __init__(self, parent, service:MovementsService):
        super(SearchCustomerDialog, self).__init__(parent)

        self.movements_service = service
        self.movements_service.data_changed.connect(self.on_data_changed) 

        self.setup_ui()
        # self.set_window_flags(Qt.FramelessWindowHint)

    def setup_ui(self) -> None:
        self.minimum_width = 450 

        # Products data
        self.title    = self._create_title("Seleccione un cliente", "dialog-title") 
        self.inp_name = self._create_input("Ingrese un nombre para buscar", "search-input")
        self.table    = self._create_table()

        # Add to layout
        self.root_layout.add_widget(self.title)
        self.root_layout.add_widget(self.inp_name)
        self.root_layout.add_widget(self.table)

        # Initial data
        self.update_table_data("")

        # Button
        self.submit = QPushButton("Seleccionar", clicked=self.on_select)
        self.root_layout.add_widget(self.submit)

        self.set_layout(self.root_layout)

    def search(self): 
        self.show()

    # Signal Slots
    @Slot()
    def on_select(self) -> None:
        self.hide()
        self.customer_changed.emit( self.data[self.table.current_row()] )

    @Slot()
    def on_data_changed(self) -> None:
        self.hide()

    @Slot(str)
    def update_table_data(self, text:str):
        self.data = self.movements_service.search_users(text)
        table_items: List[ List[TableItem] ] = []

        for customer in self.data:
            table_items.append([
                TableItem(column=0, value=customer.full_name),
                TableItem(column=1, value=customer.ci)
            ])
        self.table.insert_items(table_items)

    # Widgets Creations
    def _create_title(self, text:str, obj_name:str = "") -> QLabel:
        title = QLabel(text, alignment=Qt.AlignCenter, object_name=obj_name)
        return title

    def _create_input(self, placeholder:str, obj_name:str = "") -> QLineEdit:
        line_edit = QLineEdit( placeholder_text=placeholder, object_name=obj_name)
        line_edit.textChanged.connect(self.update_table_data)

        return line_edit

    def _create_table(self) -> DataTable:
        table = DataTable()
        table.setup_table(["Nombre y Apellido", "Número de cédula"])
        return table
