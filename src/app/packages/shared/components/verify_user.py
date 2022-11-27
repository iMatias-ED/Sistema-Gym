from PySide6.QtWidgets import QWidget, QDialog, QLabel, QLineEdit, QPushButton, QVBoxLayout
from PySide6.QtCore import Signal
from __feature__ import snake_case, true_property

from ..services.security_service import SecurityService

class VerifyUserIdentityDialog(QDialog):
    user_verified = Signal(None)
    security_service = SecurityService()

    def __init__(self, parent: QWidget):
        super(VerifyUserIdentityDialog, self).__init__(parent)
        
        self.setup_ui()
        self.show()

    def setup_ui(self):
        self.title = QLabel("Verificación")
        self.inp_ci = QLineEdit(placeholder_text="Ingrese su Número de cédula")
        self.inp_pwd = QLineEdit(placeholder_text="Ingrese su Número de contraseña")

        self.bt_verifica = QPushButton("Verificá", clicked=self.verify_user)

        layout = QVBoxLayout()
        layout.add_widget(self.title)
        layout.add_widget(self.inp_ci)
        layout.add_widget(self.inp_pwd)
        layout.add_widget(self.bt_verifica)

        self.set_layout(layout)

    def verify_user(self):
        verified = self.security_service.check_password(self.inp_ci.text, self.inp_pwd.text)

        if (verified): 
            self.user_verified.emit()
            self.close()
        else: self.inp_pwd.text = ""
