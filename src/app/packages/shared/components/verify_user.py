from PySide6.QtWidgets import QMainWindow, QWidget, QDialog, QLabel, QLineEdit, QPushButton, QVBoxLayout
from PySide6.QtCore import Signal, QRegularExpression, QSize, Qt
from PySide6.QtGui import QRegularExpressionValidator, QPixmap

from __feature__ import snake_case, true_property

from ..services.security_service import SecurityService
from ..components.error_message import ErrorDialog, ErrorMessage

class VerifyUserIdentityDialog(QDialog):
    user_verified = Signal(None)
    security_service = SecurityService()

    ONLY_NUMBERS_VALIDATOR = QRegularExpressionValidator(QRegularExpression("[0-9]*"))

    def __init__(self, parent: QWidget):
        super(VerifyUserIdentityDialog, self).__init__(parent)
        self.object_name = "login-dialog"
        
        self.setup_ui()
        self.show()

    def setup_ui(self):
        self.logo_pixmap = QPixmap("src/assets/logo-cropped.jpeg")
        self.logo = QLabel(object_name="login-logo")
        self.logo.set_pixmap(self.logo_pixmap.scaled(QSize(500, 700), Qt.KeepAspectRatio))

        self.title = QLabel("Ingrese sus credenciales para continuar", object_name="login-title", alignment=Qt.AlignCenter)
        self.inp_ci = QLineEdit("7478938", placeholder_text="Ingrese su número de cédula", validator=self.ONLY_NUMBERS_VALIDATOR)
        self.inp_pwd = QLineEdit("12345", placeholder_text="Ingrese su contraseña")

        self.bt_verifica = QPushButton("Inicie sesión", clicked=self.verify_user)

        layout = QVBoxLayout()
        layout.add_widget(self.logo)
        layout.add_widget(self.title)
        layout.add_widget(self.inp_ci)
        layout.add_widget(self.inp_pwd)
        layout.add_widget(self.bt_verifica)

        self.set_layout(layout)

    def show(self):
        self.reset_inp_pwd()
        self.reset_inp_ci()
        super().show()

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
