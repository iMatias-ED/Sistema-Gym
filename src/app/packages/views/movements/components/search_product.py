from typing import List
from PySide6.QtWidgets import *
from PySide6.QtCore import *
from __feature__ import snake_case, true_property

# Services
from ..service import MovementsService

# Classes
from ..classes.product_selection import ProductSelection
from ...products.classes.product import Product

# Components
from .select_product_quantity import SelectProductQuantityDialog

class SearchProductDialog (QDialog):
    product_selected = Signal(ProductSelection)

    root_layout = QGridLayout()
    inputs_collection: List[ QLineEdit ] = []

    def __init__(self, parent, service:MovementsService):
        super(SearchProductDialog, self).__init__(parent)

        self.movements_service = service
        self.setup_ui()

    def setup_ui(self) -> None:
        self.minimum_width = 450 

        # Products data
        self.title    = self._create_title("Seleccione un Producto", self.last_row())
        self.inp_name = self._create_input("Ingrese un nombre para buscar", self.last_row(), "search-input")
        self.table    = self._create_table( self.last_row(), "products-datatable")

        # Initial data
        self.update_table_data("")

        # Button
        self.submit = QPushButton("Seleccionar", clicked=self.on_product_selected)
        self.root_layout.add_widget(self.submit, self.last_row(), 1, self.last_row(), 2)        

        # Select Quantity Dialog
        self.quantity_dialog = SelectProductQuantityDialog(self)
        self.quantity_dialog.selected.connect(self.on_selection_finished)

        self.set_layout(self.root_layout)

    def last_row(self) -> int:
        return self.root_layout.row_count()

    def search(self): 
        self.show()

    # Signal Slots
    @Slot()
    def on_product_selected(self) -> None:
        self.quantity_dialog.show(self.data[self.table.current_row()])
        
    @Slot(str)
    def update_table_data(self, text:str):
        self.data = self.movements_service.search_products(text)
        self.table.row_count = len(self.data)

        for row, product in enumerate(self.data):
            self.table.set_item(row, 0, QTableWidgetItem(product.name))

    @Slot(ProductSelection)
    def on_selection_finished(self, data: ProductSelection):
        self.product_selected.emit(data)
        self.close()

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
        header_labels: List[str] = ["Nombre del producto"]

        table = QTableWidget( 
            object_name=obj_name,
            column_count=len(header_labels), 
            horizontal_header_labels=header_labels )

        table.vertical_header().visible = False
        table.horizontal_header().stretch_last_section = True
        table.horizontal_header().set_section_resize_mode(QHeaderView.Stretch)

        self.root_layout.add_widget(table, row, 1, row, 2)
        return table
