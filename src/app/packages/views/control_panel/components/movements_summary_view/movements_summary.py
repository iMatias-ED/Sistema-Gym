from PySide6.QtWidgets import QFrame, QVBoxLayout,QHBoxLayout
from PySide6.QtCore import Slot
from __feature__ import snake_case, true_property

from ...service import ControlPanelService
from .components.inflows import InflowsSummary
from .components.outflows import OutflowsSummary
from .components.sales import SalesSummary

class MovementsSummaryView(QFrame):
    VIEW_INDEX = 1
    service = ControlPanelService()
    content_layout = QHBoxLayout()

    def __init__(self):
        super(MovementsSummaryView, self).__init__()
        self.setup_ui()

    def setup_ui(self):
        self.inflows = InflowsSummary()
        self.outflows = OutflowsSummary()
        self.sales = SalesSummary()

        h_layout = QVBoxLayout()
        h_layout.add_widget(self.inflows)
        h_layout.add_widget(self.outflows)

        self.content_layout.add_widget(self.sales, 70)
        self.content_layout.add_layout(h_layout, 30)

        self.set_layout(self.content_layout)

    @Slot(int)
    def on_show(self, index: int):
        if index == self.VIEW_INDEX:
            self.sales.refresh(self.service.get_total_sales())
            self.inflows.refresh(self.service.get_total_inflows())
            self.outflows.refresh(self.service.get_total_outflows())
