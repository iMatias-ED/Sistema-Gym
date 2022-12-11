from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QWidget, QPushButton, QHBoxLayout
from __feature__ import snake_case, true_property

from typing import Callable

from ..classes.confirmation_message import ConfirmationMessage

class ConfirmationDialog(QDialog):
    def __init__(self, parent: QWidget, on_accepted: Callable = None, on_rejected: Callable = None, on_finished: Callable = None):
        super(ConfirmationDialog, self).__init__(parent)

        if on_accepted: self.accepted.connect(on_accepted)
        if on_rejected: self.rejected.connect(on_rejected)
        if on_finished: self.finished.connect(on_finished)

        self.setup_ui()
    
    def setup_ui(self):
        self.title = QLabel("Confirmación")
        self.message = QLabel("Mensaje")
        self.highlight = QLabel("Atencion")
        self.message.word_wrap = True

        buttons_layout = QHBoxLayout()
        self.bt_accept = QPushButton("Continuar", clicked=self.accept)
        self.bt_reject = QPushButton("Cancelar", clicked=self.reject)
        buttons_layout.add_widget(self.bt_reject)
        buttons_layout.add_widget(self.bt_accept)

        layout = QVBoxLayout()
        layout.add_widget(self.title)
        layout.add_widget(self.message)
        layout.add_widget(self.highlight)
        layout.add_layout(buttons_layout)

        self.set_layout(layout)

    def show(self, value: ConfirmationMessage):
        self.title.text = value.title
        self.message.text = value.message
        self.highlight.text = value.highlight

        super().show()