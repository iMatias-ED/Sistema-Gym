from typing import Callable, List
import sqlite3

from PySide6.QtWidgets import *
from PySide6.QtCore import *
from __feature__ import snake_case, true_property

from ..service import ProductsService
from ..classes.product import Product
from ..classes.price import Price
from ....shared.components.error_message import ErrorMessageDialog, DialogMessage

class ConfigureProductData(QDialog):
    root_layout = QGridLayout()
    inputs_collection: List[ QLineEdit ] = []
    price_inputs_collection: List[ QLineEdit ] = []

    def __init__(self, parent, service:ProductsService):
        super(ConfigureProductData, self).__init__(parent)

        self.products_service = service
        self.products_service.data_changed.connect(self.on_data_changed) 

        self.setup_ui()
        # self.set_window_flags(Qt.FramelessWindowHint)

    def setup_ui(self) -> None:
        self.minimum_width = 450 
        self.minimum_height = 300

        # Products data
        self.title = self._create_title("Productos", self.last_row())
        self.inp_code = self._create_input("Código", "Código del producto", self.last_row(), "code")
        self.inp_name = self._create_input("Nombre", "Nombre del producto", self.last_row(), "name")
        
        # Prices
        self._create_title("Precios por periodos", self.last_row())
        self.setup_price_inputs()

        # Button
        self.submit = QPushButton("Guardar")
        self.root_layout.add_widget(self.submit, self.last_row(), 1, self.last_row(), 2)

        self.set_layout(self.root_layout)

    def setup_price_inputs(self) -> None:
        for period in self.products_service.get_periods():
            line_edit = self._create_input( period.name, "Precio en Gs.", self.last_row(), period.name )
            self.price_inputs_collection.append(line_edit)

    def last_row(self) -> int:
        return self.root_layout.row_count()

    # Open mode

    def create(self) -> None:
        self._reconnect_submit(self.on_create_submit)
        self.clear()
        self.show()

    @Slot(int)
    def edit(self, product_id:int) -> None:
        product = self.products_service.get_by_id(product_id)
        self.inp_code.text = product.code
        self.inp_name.text = product.name

        prices = self.products_service.get_prices(product_id)
        for index, price in enumerate(prices):
            self.price_inputs_collection[index].text = str(price.price)
        
        self._reconnect_submit(self.on_edit_submit, product.id)
        self.show()
            
    # Signal Slots
    @Slot()
    def on_create_submit(self) -> None:
        try:         
            self.products_service.create( self._collect_data() )
        except sqlite3.IntegrityError as e:
            self.manage_error(e.args[0])
    
    @Slot()
    def on_edit_submit(self, product_id) -> None:
        try:
            self.products_service.update( self._collect_data(product_id) )
        except sqlite3.IntegrityError as e:
            self.manage_error(e.args[0])

    def manage_error(self, error: str):
        if "code" in error:
            ErrorMessageDialog(self, self.reset_inp_code).show(DialogMessage(
                "Código duplicado",
                f'Ya existe un producto con el código "{self.inp_code.text}"'
            ))
        if "name" in error:
            ErrorMessageDialog(self, self.reset_inp_name).show(DialogMessage(
                "Nombre duplicado",
                f'Ya existe un producto con el nombre "{self.inp_name.text}"'
            ))

    def reset_inp_code(self):
        self.inp_code.text = ""
        self.inp_code.set_focus()

    def reset_inp_name(self):
        self.inp_name.text = ""
        self.inp_name.set_focus()

    @Slot()
    def on_data_changed(self) -> None:
        self.hide()

    # Utils
    def _collect_data(self, id: int=None) -> Product:
        data: dict[str, str] = {}
        for inp in self.inputs_collection:
            data[inp.object_name] = inp.text;
        
        if id: data["id"] = id
        product = Product(data)

        for inp in self.price_inputs_collection:
            price_data = {
                "name": inp.object_name,
                "price": inp.text
            }
            product.save_price(Price(price_data))
        return product

    def clear(self) -> None:
        for inp in self.inputs_collection: inp.clear()
        self.inp_code.clear()
        self.inp_name.clear()

    def _reconnect_submit(self, connect_to: Callable, parameter=None) -> None:
        try:     self.submit.clicked.disconnect()
        except   RuntimeError: pass
        finally: 
            if parameter:
                self.submit.clicked.connect( lambda: connect_to(parameter) )
            else: self.submit.clicked.connect(connect_to)

    # Widgets Creations
    def _create_title(self, text:str, row:int) -> QLabel:
        title = QLabel(text, alignment=Qt.AlignCenter, object_name="dialog-title")
        self.root_layout.add_widget(title, row, 1, row, 2)
        return title

    def _create_input(self, title:str, placeholder:str, row:int, object_name: str = "") -> QLineEdit:
        label = QLabel(title)
        line_edit = QLineEdit( placeholder_text=placeholder, object_name=str(object_name))

        self.inputs_collection.append(line_edit)

        self.root_layout.add_widget(label, row, 1)
        self.root_layout.add_widget(line_edit, row, 2)

        return line_edit