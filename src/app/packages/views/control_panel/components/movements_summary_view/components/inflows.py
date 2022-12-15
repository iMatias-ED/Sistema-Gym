from PySide6.QtWidgets import *
from PySide6.QtCore import *
from __feature__ import snake_case, true_property

class InflowsSummary(QFrame):
    root_layout = QVBoxLayout()

    def __init__(self):
        super(InflowsSummary, self).__init__()

        self.title = QLabel("Entradas de dinero")
        self.amount = QLabel("Gs Total")

        self.root_layout.add_widget(self.title)
        self.root_layout.add_widget(self.amount)

        self.set_layout(self.root_layout)

    def refresh(self, data: dict):
        self.amount.text = f'Gs. {data["total"]}'