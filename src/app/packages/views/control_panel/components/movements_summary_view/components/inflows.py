from PySide6.QtWidgets import QFrame, QVBoxLayout, QLabel, QPushButton
from PySide6.QtCore import QSize, Qt
from PySide6.QtGui import QIcon
from __feature__ import snake_case, true_property

from ..cash_flow_dialog import CashFlowDialog
from ....service import ControlPanelService

class InflowsSummary(QFrame):
    root_layout = QVBoxLayout()

    def __init__(self):
        super(InflowsSummary, self).__init__()
        self.current_date = ""
        self.object_name = "movements-summary"
        self.root_layout.alignment = Qt.AlignCenter

        self.service = ControlPanelService()

        self.title = QLabel("Entradas de dinero", alignment=Qt.AlignCenter, object_name="title")
        self.amount = QLabel("Gs Total", alignment=Qt.AlignCenter, object_name="total")
        self.summary_bt = QPushButton(icon=QIcon("src/assets/plus.png"), clicked=self.open_summary)
        self.summary_bt.icon_size = QSize(40, 40)

        self.root_layout.add_stretch()
        self.root_layout.add_widget(self.title)
        self.root_layout.add_widget(self.amount)
        self.root_layout.add_widget(self.summary_bt)
        self.root_layout.add_stretch()

        self.set_layout(self.root_layout)

    def open_summary(self):
        data = self.service.get_all_inflows(self.current_date)
        CashFlowDialog(self).show("Entradas de dinero", data)

    def refresh(self, data: dict, date: str):
        self.current_date = date
        self.amount.text = f'Gs. {data["total"]}'