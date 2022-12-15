from typing import Union

from PySide6.QtGui import QRegularExpressionValidator, QIcon, QColor
from PySide6.QtCore import Signal, QRegularExpression, Qt, QSize
from PySide6.QtWidgets import QDialog, QLineEdit, QLabel, QComboBox, QPushButton, QVBoxLayout, QHBoxLayout
from __feature__ import snake_case, true_property

# Classes
from ..classes.sale_item import SaleItem
from ...products.classes.price import Price
from ...products.classes.product import Product

class ConfigureSelectedProduct(QDialog):
    price: Price
    product: Product
    selected = Signal(SaleItem)

    ONLY_NUMBERS_VALIDATOR = QRegularExpressionValidator(QRegularExpression("[0-9]*"))

    def __init__(self, parent):
        super(ConfigureSelectedProduct, self).__init__(parent)
        self.object_name = "configure-selected-product"
        self.setup_ui()

    def setup_ui(self):
        self.minimum_width = 350

        self.title = QLabel(object_name="title", alignment=Qt.AlignCenter)
        self.amount = QLabel(object_name="amount", alignment=Qt.AlignCenter)

        self.periods = QComboBox()
        self.periods.currentTextChanged.connect(self.calculate_amount)

        self.bt_plus = QPushButton( minimum_width=45, clicked=self.plus_1, icon=QIcon("src/assets/plus.png"))
        self.bt_minus = QPushButton( minimum_width=45, clicked=self.minus_1, icon=QIcon("src/assets/minus.png"))
        self.quantity = QLineEdit( validator=self.ONLY_NUMBERS_VALIDATOR, maximum_width=150, object_name="quantity" )
        self.quantity.textChanged.connect(self.calculate_amount)

        # icons
        self.bt_plus.set_icon_size(QSize(35, 35))
        self.bt_minus.set_icon_size(QSize(35, 35))

        self.submit = QPushButton("Seleccionar", clicked=self.on_submit, object_name="bt-add-product")

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

    def show(self, product: Product, quantity: Union[int, None] = None, period: Union[str, None] = None):
        self.clear()
        self.product = product
        self.title.text = product.name
        if quantity: self.quantity.text = str(quantity)

        self.add_period_items(product)
        if period: self.periods.set_current_index(self.periods.find_text(period))
        
        super().show()

    def add_period_items(self, product: Product):
        periods = [ p.name for p in product.prices ]
        model = self.periods.model()

        for index, period in enumerate(periods):
            self.periods.add_item(period)
            model.set_data(model.index(index, 0), QColor("white"), Qt.BackgroundRole)

    def calculate_amount(self):
        selected = self.periods.current_text
        
        if selected:
            self.price = self.product.get_price_by_name(selected)

            if self.quantity.text == "": self.quantity.text = "1"
            
            self.total = int(self.quantity.text) * self.price.price
            self.amount.text = f"Gs. {self.total}"

    def on_submit(self):
        selected = SaleItem(
            self.product, self.price, int(self.quantity.text), self.total)

        self.selected.emit(selected)
        self.close()

    # Utils

    def clear(self):
        self.quantity.text = "1"
        self.periods.clear()

    def plus_1(self):
        self.quantity.text = str(int(self.quantity.text) + 1)
    
    def minus_1(self):
        if int(self.quantity.text) <= 1:
            self.quantity.text = "1"
            return
        self.quantity.text = str(int(self.quantity.text) - 1)