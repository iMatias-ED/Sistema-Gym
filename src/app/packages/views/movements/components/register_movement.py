from typing import Dict
from PySide6.QtWidgets import QDialog, QWidget, QLabel, QComboBox, QLineEdit, QPushButton, QPlainTextEdit, QVBoxLayout
from PySide6.QtCore import Qt
from PySide6.QtGui import QColor
from __feature__ import snake_case, true_property

from ..classes.cash_flow_item import CashFlowItem
from ..classes.movement_type import MovementType

# Services 
from ..service import MovementsService

class RegisterMovementDialog(QDialog):
    id_movement_type: int
    cash_flow_data: Dict[str, MovementType]

    def __init__(self, parent: QWidget, service: MovementsService):
        super(RegisterMovementDialog, self).__init__(parent)
        self.object_name = "register-movement"
        
        self.movements_service = service
        self.setup_ui()

    def setup_ui(self):
        self.minimum_width = 400
        self.title = QLabel("Movimiento de dinero", object_name = "title", alignment=Qt.AlignCenter)

        self.select_flow_type = QComboBox(object_name="select-flow-type")
        self.add_flow_type_items()

        self.amount = QLineEdit( placeholder_text="Ingrese el monto en Gs." )
        self.description = QPlainTextEdit(placeholder_text="Ingrese una descripción")
        self.submit = QPushButton("Guardar", clicked=self._on_submit)

        layout = QVBoxLayout()
        layout.add_widget(self.title)
        layout.add_widget(self.select_flow_type)
        layout.add_widget(self.amount)
        layout.add_widget(self.description)
        layout.add_widget(self.submit)

        self.set_layout(layout)

    def add_flow_type_items(self):
        self.cash_flow_data = { cf.name: cf for cf in self.movements_service.get_cash_flow_types() }

        model = self.select_flow_type.model()
        for index, movement_type in enumerate(self.cash_flow_data.keys()):
            self.select_flow_type.add_item(movement_type)
            model.set_data(model.index(index, 0), QColor("white"), Qt.BackgroundRole)


    def _on_submit(self):
        from ....shared.services.security_service import current_user_id
        cash_flow = self.cash_flow_data[self.select_flow_type.current_text]
        
        data = {
            "id_user": current_user_id,
            "id_movement_type": cash_flow.id,
            "amount": self.amount.text,
            "description": self.description.plain_text
        }

        self.hide()
        self.movements_service.register_cash_flow( CashFlowItem(data) )


