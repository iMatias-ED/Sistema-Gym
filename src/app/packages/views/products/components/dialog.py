from typing import Callable, Tuple, List
from PySide6.QtWidgets import *
from PySide6.QtCore import *
from __feature__ import snake_case, true_property

from ..service import ProductsService

class Dialog(QDialog):
    root_layout = QGridLayout()
    price_inputs_collection: List[ Tuple[int, int] ] = []

    def __init__(self, service: ProductsService):
        super(Dialog, self).__init__()
        self.minimum_width = 350 
        self.minimum_height = 250 

        self.service = service
        self.service.data_changed.connect(self.on_data_changed)

        self.setup_ui()

    def setup_ui(self):
        # Products data
        self.title = self._create_title("Productos", self.last_row())
        self.inp_code = self._create_input("Código", "Código del producto", self.last_row())
        self.inp_name = self._create_input("Nombre", "Nombre del producto", self.last_row())
        
        # Prices
        self._create_title("Precios por periodos", self.last_row())
        self.setup_price_inputs()

        # Button
        self.submit = QPushButton("Submit")
        self.root_layout.add_widget(self.submit, self.last_row(), 1, self.last_row(), 2)

        self.set_layout(self.root_layout)

    def setup_price_inputs(self):
        periods = self.service.get_periods()
        for period in periods:
            # id, name, valid_for_days -> Period format
            input = self._create_input( period[1], "Precio en Gs.", self.last_row() )

            # save the period id and the input reference
            self.price_inputs_collection.append( (period[0], input) )

    def last_row(self):
        return self.root_layout.row_count()

    # 
    def create(self):
        self.reconnect_submit(self.on_create_submit)
        self.clear()
        self.show()

    def clear(self):
        for inp in self.price_inputs_collection: inp[1].clear()
        self.inp_code.clear()
        self.inp_name.clear()

    def reconnect_submit(self, connect_to: Callable, parameter=None):
        try:     self.submit.clicked.disconnect()
        except   RuntimeError: pass
        finally: 
            if parameter:
                self.submit.clicked.connect( lambda: connect_to(parameter) )
            else: self.submit.clicked.connect(connect_to)
            
    # Signal Slots
    @Slot()
    def on_create_submit(self):
        prices = []
        for inp in self.price_inputs_collection:
            prices.append( (inp[0], inp[1].text) )
        self.service.create( self.inp_code.text, self.inp_name.text, prices )
    
    @Slot()
    def on_edit_submit(self, product_id):
        prices = []
        for inp in self.price_inputs_collection:
            prices.append( (inp[0], inp[1].text) )
        self.service.update( product_id, self.inp_code.text, self.inp_name.text, prices )

    @Slot(int)
    def edit(self, product_id:int):
        

        product = self.service.get_product_by_id(product_id)
        self.inp_code.text = product.code
        self.inp_name.text = product.name

        prices = self.service.get_product_prices(product_id)
        for index, price in enumerate(prices):
            # price[1] -> value
            # price_inputs_collection[index][1] -> input reference
            self.price_inputs_collection[index][1].text = str(price[1])
        
        self.reconnect_submit(self.on_edit_submit, product.id)
        self.show()

    @Slot()
    def on_data_changed(self):
        self.hide()

    # Widgets Creations
    def _create_title(self, text:str, row:int):
        title = QLabel(text, alignment=Qt.AlignCenter, object_name="dialog-title")
        self.root_layout.add_widget(title, row, 1, row, 2)
        return title

    def _create_input(self, title:str, placeholder:str, row:int):
        label = QLabel(title)
        line_edit = QLineEdit(placeholder_text=placeholder)

        self.root_layout.add_widget(label, row, 1)
        self.root_layout.add_widget(line_edit, row, 2)

        return line_edit