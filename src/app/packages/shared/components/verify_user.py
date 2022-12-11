from PySide6.QtWidgets import QWidget, QDialog, QLabel, QLineEdit, QPushButton, QVBoxLayout
from PySide6.QtCore import Signal, QRegularExpression
from PySide6.QtGui import QRegularExpressionValidator

from __feature__ import snake_case, true_property

from ..services.security_service import SecurityService
from ..components.error_message import ErrorDialog, ErrorMessage

class VerifyUserIdentityDialog(QDialog):
    user_verified = Signal(None)
    security_service = SecurityService()

    ONLY_NUMBERS_VALIDATOR = QRegularExpressionValidator(QRegularExpression("[0-9]*"))

    def __init__(self, parent: QWidget):
        super(VerifyUserIdentityDialog, self).__init__(parent)
        
        self.setup_ui()
        self.show()

    def setup_ui(self):
        self.title = QLabel("Verificación")
        self.inp_ci = QLineEdit(placeholder_text="Ingrese su Número de cédula", validator=self.ONLY_NUMBERS_VALIDATOR)
        self.inp_pwd = QLineEdit(placeholder_text="Ingrese su Número de contraseña")

        self.bt_verifica = QPushButton("Verificá", clicked=self.verify_user)

        layout = QVBoxLayout()
        layout.add_widget(self.title)
        layout.add_widget(self.inp_ci)
        layout.add_widget(self.inp_pwd)
        layout.add_widget(self.bt_verifica)

        self.set_layout(layout)

    def verify_user(self):
        try: 
            verified = self.security_service.check_password(self.inp_ci.text, self.inp_pwd.text)
        except TypeError:
            message = ErrorMessage(
                "Usuario no encontrado.",
                f"No se encontró ningún usuario con el número de cédula {self.inp_ci.text}"
            )
            ErrorDialog(self, self.reset_inp_ci).show(message)
            return

        if (verified): 
            self.user_verified.emit()
            self.close()
        else: 
            message = ErrorMessage(
                "Contraseña incorrecta.",
                "La contraseña ingresada es incorrecta."
            )
            ErrorDialog(self, self.reset_inp_pwd).show(message)

    def reset_inp_ci(self):
        self.inp_ci.text = ""
        self.inp_ci.set_focus()

    def reset_inp_pwd(self):
        self.inp_pwd.text = ""
        self.inp_pwd.set_focus()
