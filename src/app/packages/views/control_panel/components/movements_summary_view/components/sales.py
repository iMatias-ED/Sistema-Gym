from PySide6.QtWidgets import *
from PySide6.QtCore import *
from __feature__ import snake_case, true_property

class SalesSummary(QFrame):
    root_layout = QVBoxLayout()

    def __init__(self):
        super(SalesSummary, self).__init__()

        self.title = QLabel("Ventas")
        self.amount = QLabel("Gs Total")

        self.root_layout.add_widget(self.title)
        self.root_layout.add_widget(self.amount)

        self.set_layout(self.root_layout)

        # self.style_sheet = "background: gray; border: 1px solid blue;"

    def refresh(self, data: dict):
        self.amount.text = f'Gs. {data["total"]}'