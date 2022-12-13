from PySide6.QtWidgets import QPushButton, QDialog, QVBoxLayout, QLabel, QWidget
from PySide6.QtCore import Qt
from __feature__ import snake_case, true_property

from typing import Callable

from ..classes.error_message import ErrorMessage

class ErrorDialog(QDialog):
    def __init__(self, parent: QWidget, on_finished: Callable = None):
        super(ErrorDialog, self).__init__(parent)
        if on_finished: self.finished.connect(on_finished)

        self.object_name = "error-message"
        self.setup_ui()
    
    def setup_ui(self):
        self.minimum_width = 400
        self.minimum_height = 300

        self.title = QLabel("Error", object_name="title", alignment=Qt.AlignCenter)
        self.message = QLabel("Mensaje", object_name="message", alignment=Qt.AlignJustify)
        self.bt_accept = QPushButton("Ok", clicked=self.accept)
        self.message.word_wrap = True

        layout = QVBoxLayout()
        layout.add_widget(self.title, 20)
        layout.add_widget(self.message, 65)
        layout.add_widget(self.bt_accept, 15)

        self.set_layout(layout)

    def show(self, value: ErrorMessage):
        self.title.text = value.title
        self.message.text = value.message
        
        super().show()