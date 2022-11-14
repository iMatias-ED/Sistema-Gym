from typing import Callable, Dict, Tuple, List
from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import QColor
from __feature__ import snake_case, true_property

# Services 
from ..service import MovementsService

# Classes
from ...customers.classes.customer import Customer

class SearchCustomerDialog(QDialog):
    customer_changed = Signal(Customer)

    root_layout = QGridLayout()
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
        self.title    = self._create_title("Seleccione un cliente", self.last_row())
        self.inp_name = self._create_input("Ingrese un nombre para buscar", self.last_row(), "search-input")
        self.table    = self._create_table( self.last_row(), "customers-datatable")

        # Initial data
        self.update_table_data("")

        # Button
        self.submit = QPushButton("Seleccionar", clicked=self.on_select)
        self.root_layout.add_widget(self.submit, self.last_row(), 1, self.last_row(), 2)

        self.set_layout(self.root_layout)

    def last_row(self) -> int:
        return self.root_layout.row_count()

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
        self.table.row_count = len(self.data)

        for row, customer in enumerate(self.data):
            self.table.set_item(row, 0, QTableWidgetItem(customer.full_name))
            self.table.set_item(row, 1, QTableWidgetItem(str(customer.ci)))

    # Widgets Creations
    def _create_title(self, text:str, row:int, obj_name:str = "") -> QLabel:
        title = QLabel(text, alignment=Qt.AlignCenter, object_name=obj_name)
        self.root_layout.add_widget(title, row, 1, row, 2)
        return title

    def _create_input(self, placeholder:str, row:int, obj_name:str = "") -> QLineEdit:
        line_edit = QLineEdit( placeholder_text=placeholder, object_name=obj_name)
        line_edit.textChanged.connect(self.update_table_data)

        self.inputs_collection.append(line_edit)
        self.root_layout.add_widget(line_edit, row, 1, row, 2)

        return line_edit

    def _create_table(self, row:int, obj_name:str = "") -> QTableWidget:
        header_labels: List[str] = ["Nombre y Apellido", "Número de cédula"]
        table = QTableWidget( 
            object_name=obj_name,
            column_count=len(header_labels), 
            horizontal_header_labels=header_labels )
        table.horizontal_header().stretch_last_section = True
        table.horizontal_header().set_section_resize_mode(QHeaderView.Stretch)

        self.root_layout.add_widget(table, row, 1, row, 2)
        return table

    # Utils
    def clear(self) -> None:
        for inp in self.inputs_collection: inp.clear()

    def _collect_data(self, id: int=None) -> Dict:
        data = {}
        for inp in self.inputs_collection:
            data[inp.object_name] = inp.text;

        # Bug when comboBox is added to a list. Loses its value
        # So we can't add it to self.inputs_collection
        data[self.inp_genre.object_name] = self.inp_genre.current_text;

        if id: data["id"] = id
        return data
