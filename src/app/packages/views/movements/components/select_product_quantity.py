from PySide6.QtCore import Signal
from PySide6.QtWidgets import QDialog, QLineEdit, QLabel, QComboBox, QPushButton, QVBoxLayout, QHBoxLayout
from __feature__ import snake_case, true_property

from ..classes.selection import Selection
from ...products.classes.price import Price
from ...products.classes.product import Product

class SelectProductQuantityDialog(QDialog):
    price: Price
    product: Product
    selected = Signal(Selection)

    def __init__(self, parent):
        super(SelectProductQuantityDialog, self).__init__(parent)
        self.setup_ui()

    def setup_ui(self):
        self.title = QLabel()
        self.amount = QLabel()

        self.periods = QComboBox()
        self.periods.currentTextChanged.connect(self.calculate_amount)

        self.bt_plus = QPushButton("+", minimum_width=45, clicked=self.plus_1)
        self.bt_minus = QPushButton("-", minimum_width=45, clicked=self.minus_1)
        self.quantity = QLineEdit(text="1" )
        self.quantity.textChanged.connect(self.calculate_amount)

        self.submit = QPushButton("Seleccionar", clicked=self.on_submit)

        layout = QVBoxLayout()
        quantity_layout = QHBoxLayout()

        quantity_layout.add_widget(self.bt_minus)
        quantity_layout.add_widget(self.quantity)
        quantity_layout.add_widget(self.bt_plus)

        layout.add_widget(self.title)
        layout.add_widget(self.amount)
        layout.add_widget(self.periods)
        layout.add_layout(quantity_layout)
        layout.add_widget(self.submit)
        
        self.set_layout(layout)

    def show(self, product: Product):
        self.clear()
        self.product = product
        self.title.text = product.name

        self.periods.add_items([ p.name for p in product.prices ])
        
        super().show()

    def calculate_amount(self):
        selected = self.periods.current_text
        
        if selected:
            self.price = self.product.get_price_by_name(selected)
            
            self.total = int(self.quantity.text) * self.price.price
            self.amount.text = f"Gs. {self.total}"

    def on_submit(self):
        selected = Selection(self.product, self.price, self.quantity.text, self.total)

        self.selected.emit(selected)
        self.close()

    # Utils

    def clear(self):
        self.quantity.text = "1"
        self.periods.clear()

    def plus_1(self):
        self.quantity.text = str(int(self.quantity.text) + 1)
    
    def minus_1(self):
        self.quantity.text = str(int(self.quantity.text) - 1)