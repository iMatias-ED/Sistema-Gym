from PySide6.QtWidgets import QDialog, QLabel, QWidget, QVBoxLayout
from __feature__ import snake_case, true_property

import time

class SuccessMessage(QDialog):

    def __init__(self, parent: QWidget):
        super().__init__(parent)
        self.object_name = "success-message"
        
        layout = QVBoxLayout()

        self.message = QLabel("¡Operación Exitosa!")
        
        layout.add_widget(self.message)
        self.set_layout(layout)


    def show(self, message: str):
        self.message.text = message
        super().show()

