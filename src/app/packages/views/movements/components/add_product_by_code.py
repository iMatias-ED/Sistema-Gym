from PySide6.QtCore import Signal, Slot, Qt
from PySide6.QtWidgets import QFrame, QHBoxLayout, QLineEdit, QPushButton, QLabel
from __feature__ import snake_case, true_property

from ..service import MovementsService
from .configure_selected_product import ConfigureSelectedProduct

from ....shared.components.error_message import ErrorDialog, ErrorMessage

from ..classes.sale_item import SaleItem
from ...products.classes.product import Product

class AddProductByCode(QFrame):
    product_selected = Signal(SaleItem)

    def __init__(self, service: MovementsService):
        super(AddProductByCode, self).__init__()
        self.object_name = "code-input-section"
        self.movements_service = service
        self.setup_ui()

    def setup_ui(self):
        self.inp_code = QLineEdit(
            placeholder_text="Ingrese el código del producto",
            object_name="code-input",
            maximum_width=800,
        )
        self.inp_code.returnPressed.connect(self.on_code_inserted)

        self.submit = QPushButton( "Insertar", 
            clicked=self.on_code_inserted,
            object_name="bt-add-product",
            maximum_width=150,
        )

        self.total = QLabel( "Gs. 10.000.000", 
            alignment=Qt.AlignCenter, 
            object_name="total" 
        )

        self.quantity_dialog = ConfigureSelectedProduct(self)
        self.quantity_dialog.selected.connect(self.emit_product_selected)

        layout = QHBoxLayout()
        layout.add_widget(self.inp_code)
        layout.add_widget(self.submit)
        layout.add_spacing(20)
        layout.add_widget(self.total)

        self.set_layout(layout)

    def on_code_inserted(self) -> None:
        try: 
            product = self.movements_service.get_product_by_code(self.inp_code.text)
        except TypeError:
            ErrorDialog(self, self.reset_inp_code).show(ErrorMessage(
                "Producto no encontrado.",
                f'No se encontró ningún producto con el código "{self.inp_code.text}"'
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
