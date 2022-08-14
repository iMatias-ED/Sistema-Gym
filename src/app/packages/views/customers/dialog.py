from PySide6.QtWidgets import *
from PySide6.QtCore import *
from __feature__ import snake_case, true_property

from .service import CustomersService

class Dialog(QDialog):
    service = CustomersService()

    def __init__(self):
        super(Dialog, self).__init__()
        self.size = QSize(300, 300)

    def example(self, mode:str):
        print(f"dialog in mode {mode}")
        self.show()

    def create(self):
        print("create mode")
        self.show()

    @Slot(int)
    def edit(self, row):
        print(f"Editing row {row}")
        self.show()