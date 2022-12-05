from PySide6.QtWidgets import QVBoxLayout, QLineEdit, QPushButton, QDialog, QLabel
from PySide6.QtCore import Signal, Slot, Qt
from __feature__ import snake_case, true_property

# Services
from ..service import MovementsService

# Classes
from ..classes.sale_item import SaleItem
from ....shared.components.data_table import DataTable, TableItem

# Components
from .configure_selected_product import ConfigureSelectedProduct

class SearchProductDialog (QDialog):
    product_selected = Signal(SaleItem)
    root_layout = QVBoxLayout()

    def __init__(self, parent, service:MovementsService):
        super(SearchProductDialog, self).__init__(parent)

        self.movements_service = service
        self.setup_ui()

    def setup_ui(self) -> None:
        self.minimum_width = 450 

        # Products data
        self.title    = self._create_title("Seleccione un Producto", "dialog-title" )
        self.inp_name = self._create_input("Ingrese un nombre para buscar", "search-input")
        self.table    = self._create_table()

        # Add widgets to layout
        self.root_layout.add_widget(self.title)
        self.root_layout.add_widget(self.inp_name)
        self.root_layout.add_widget(self.table)          

        # Initial data
        self.update_table_data("")

        # Button
        self.submit = QPushButton("Seleccionar", clicked=self.on_product_selected)
        self.root_layout.add_widget(self.submit)        

        # Select Quantity Dialog
        self.quantity_dialog = ConfigureSelectedProduct(self)
        self.quantity_dialog.selected.connect(self.on_selection_finished)

        self.set_layout(self.root_layout)

    def search(self): 
        self.show()

    # Signal Slots
    @Slot()
    def on_product_selected(self) -> None:
        self.quantity_dialog.show(self.data[self.table.current_row()])
        
    @Slot(str)
    def update_table_data(self, text:str):
        self.data = self.movements_service.search_products(text)
        self.table.insert_items(
            [ [TableItem(column=0, value=p.name)] for p in self.data ])

    @Slot(SaleItem)
    def on_selection_finished(self, data: SaleItem):
        self.product_selected.emit(data)
        self.close()

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
        table.setup_table(["Nombre del producto"])
        return table
