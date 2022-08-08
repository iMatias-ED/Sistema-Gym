from PySide6.QtWidgets import *
from PySide6.QtCore import *
from __feature__ import snake_case, true_property

class Dialog(QDialog):
    def example(self, mode:str):
        self.size = QSize(300, 300)
        self.show()