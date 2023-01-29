from datetime import datetime
from typing import Callable, Dict, List
from PySide6.QtWidgets import QGridLayout, QWidgetItem, QLineEdit, QVBoxLayout, QFrame, QWidget, QLabel, QPushButton, QComboBox, QDateTimeEdit, QHBoxLayout
from PySide6.QtCore import Slot, Qt, QLocale, QDate, QSize
from PySide6.QtGui import QColor, QPixmap

from __feature__ import snake_case, true_property

from ...movements.service import MovementsService
from ...movements.components.search_product import SearchProductDialog

from ..service import CustomersService
from ...products.service import ProductsService
from ..classes.customer import Customer
from ...products.classes.product import Product
from ....shared.components.error_message import ErrorDialog, ErrorMessage

class AccessTimeData(QFrame):
    root_layout = QVBoxLayout()

    def __init__(self):
        super(AccessTimeData, self).__init__()

        self.products_service = ProductsService()
        self.products: Dict[int, QDateTimeEdit] = {}
        self.setup_ui()

    def setup_ui(self):
        self.minimum_height = 400

        self.title = QLabel("Productos Vinculados", alignment=Qt.AlignCenter, object_name="config-dialog-title")
        self.search_button = QPushButton(icon=QPixmap("src/assets/plus.png"))
        self.search_button.icon_size = QSize(25, 25)

        title_layout = QHBoxLayout()
        title_layout.add_widget(self.title, 95)
        title_layout.add_widget(self.search_button, 5)

        self.search_dialog = SearchProductDialog(self, MovementsService())
        self.search_dialog.product_selected.connect(self.generate_new_input)

        # Open search dialog
        self.search_button.clicked.connect(lambda: self.search_dialog.search(True))

        self.root_layout.add_layout(title_layout)
        self.root_layout.set_alignment(Qt.AlignTop) 
        self.root_layout.add_spacing(15)
        self.set_layout(self.root_layout)

    def reset_content(self):
        self.products.clear()
        self.clearvbox()
        self.setup_ui()

    def load_customers_data(self, customer: Customer):
        data = customer.access_time
        for access_time in data:
            product = self.products_service.get_by_id(access_time.id_product)
            self.generate_new_input( product, access_time.expiration_as_date() )

    def clearvbox(self, L = False):
        if not L: L = self.root_layout
        if L is not None:
            while L.count():
                item = L.take_at(0)
                widget = item.widget()
                
                if widget is not None:
                    widget.delete_later()
                else:
                    self.clearvbox(item.layout())

    @Slot(Product)
    def generate_new_input(self, product: Product, d:datetime = None):
        # Product already selected before?
        if product.id in self.products:
            self.products[product.id].set_focus()
            return
        
        # Create widgets
        label = QLabel(product.name, minimum_width=200, alignment=Qt.AlignCenter, object_name="input-label")
        date_input = self._create_date_picker()
        bt_remove = QPushButton(icon=QPixmap("src/assets/remove.png"), icon_size = QSize(25, 25), maximum_width=30 )

        # Default date
        if d:
            date_input.set_date( QDate(d.year, d.month, d.day) )

        # Save new input to read values later
        self.products[product.id] = date_input

        # Add widgets to a QHBoxLayout
        row_layout = QHBoxLayout()
        row_layout.add_widget(bt_remove)
        row_layout.add_widget(label)
        row_layout.add_widget(date_input)

        # Add QHBoxLayout to root_layout
        self.root_layout.add_layout(row_layout)

        # Event to remove inputs
        bt_remove.clicked.connect(lambda: self.remove_item( self.root_layout.index_of(row_layout), product ))

    def remove_item(self, layout_index: int, product: Product):    
        # Remove record
        del self.products[product.id]

        # Get the child layout reference
        child_layout: QHBoxLayout = self.root_layout.take_at(layout_index)

        while child_layout.item_at(0):
            item: QWidgetItem = child_layout.item_at(0)

            # The item as widget (QLabel, QPushButton, QLineEdit)
            widget: QWidget = item.widget()

            # Hide the widget
            widget.close()

            # remove widget from layout
            child_layout.remove_widget(widget)
            
            # remove widget from memory
            del widget

        # remove the row_layout from the root layout and memory
        self.root_layout.remove_item(child_layout)
        del child_layout

    def _create_date_picker(self, obj_name:str = "") -> QDateTimeEdit:
        dateEdit = QDateTimeEdit( QDate.current_date(), locale = QLocale.Spanish, display_format = "dd/MM/yyyy", minimum_width=200, object_name=obj_name)
        dateEdit.calendar_popup = True
        return dateEdit
