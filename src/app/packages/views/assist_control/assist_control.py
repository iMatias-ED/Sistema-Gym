from PySide6.QtWidgets import *
from PySide6.QtCore import *
from __feature__ import snake_case, true_property

from .report_view import *
from ...shared.content_view import *

class AssistControl(ContentView):
    inputs_layout = QVBoxLayout()
    stacked_layout = QStackedLayout()
    
    def setup_ui(self):
        self.set_styles(__file__)

        # Input View
        self.inp_ci = QLineEdit( placeholder_text="Ingresa tu CI", maximum_width = 400 )
        self.bt_continue = QPushButton("Consultá", maximum_width = 400)

        self.inputs_layout.add_widget(self.inp_ci)
        self.inputs_layout.add_widget(self.bt_continue)
        self.inputs_layout.set_alignment(Qt.AlignCenter)

        inputs_layout_container = QWidget()
        inputs_layout_container.set_layout(self.inputs_layout)

        # Report View
        self.report_view = ReportView()

        self.stacked_layout.add_widget(self.report_view)
        self.set_layout(self.stacked_layout)