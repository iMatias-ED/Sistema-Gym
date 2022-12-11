from PySide6.QtCore import Signal, Slot
from PySide6.QtWidgets import QFrame, QHBoxLayout, QLineEdit, QPushButton
from __feature__ import snake_case, true_property

from ..service import MovementsService
from .configure_selected_product import ConfigureSelectedProduct

from ....shared.components.error_message import ErrorMessageDialog, DialogMessage

from ..classes.sale_item import SaleItem
from ...products.classes.product import Product

class AddProductByCode(QFrame):
    product_selected = Signal(SaleItem)

    def __init__(self, service: MovementsService):
        super(AddProductByCode, self).__init__()

        self.movements_service = service
        self.setup_ui()

    def setup_ui(self):
        self.inp_code = QLineEdit(
            minimum_height=45,
            placeholder_text="Ingrese el código del producto")
        self.submit = QPushButton("Insertar", clicked=self.on_code_inserted)

        self.quantity_dialog = ConfigureSelectedProduct(self)
        self.quantity_dialog.selected.connect(self.emit_product_selected)

        layout = QHBoxLayout()
        layout.add_widget(self.inp_code, 70)
        layout.add_widget(self.submit, 30)

        self.set_layout(layout)

    def on_code_inserted(self) -> None:
        try: 
            product = self.movements_service.get_product_by_code(self.inp_code.text)
        except TypeError:
            ErrorMessageDialog(self, self.reset_inp_code).show(DialogMessage(
                "Producto no encontrado.",
                f"No se encontró ningún producto con el código {self.inp_code.text}"
            ))
            return

        self.quantity_dialog.show(product)

    @Slot(SaleItem)
    def emit_product_selected(self, selection: Product) -> None:
        self.inp_code.text = ""
        self.product_selected.emit(selection)

    def reset_inp_code(self):
        self.inp_code.text = ""
        self.inp_code.set_focus()
