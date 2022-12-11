from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QWidget
from __feature__ import snake_case, true_property

from typing import Callable

from ..classes.dialog_message import DialogMessage

class ErrorMessageDialog(QDialog):
    def __init__(self, parent: QWidget, on_finished: Callable = None):
        super(ErrorMessageDialog, self).__init__(parent)
        if on_finished: self.finished.connect(on_finished)

        self.setup_ui()
    
    def setup_ui(self):
        self.title = QLabel("Error")
        self.message = QLabel("Mensaje")
        self.message.word_wrap = True

        layout = QVBoxLayout()
        layout.add_widget(self.title)
        layout.add_widget(self.message)

        self.set_layout(layout)

    def show(self, value: DialogMessage):
        self.title.text = value.title
        self.message.text = value.message
        
        super().show()