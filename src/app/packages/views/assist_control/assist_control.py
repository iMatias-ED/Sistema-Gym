from PySide6.QtWidgets import QVBoxLayout, QStackedLayout, QLineEdit, QPushButton, QWidget
from PySide6.QtCore import Qt, QRegularExpression
from PySide6.QtGui import QRegularExpressionValidator

from __feature__ import snake_case, true_property

from .components.summary_view import SummaryView
from ...shared.content_view import ContentView
from ...shared.components.error_message import ErrorMessageDialog, DialogMessage

class AssistControl(ContentView):
    inputs_layout = QVBoxLayout()
    stacked_layout = QStackedLayout()

    
    def setup_ui(self):
        self.set_styles(__file__)

        # Input View
        self.inp_ci = QLineEdit( placeholder_text="Ingresa tu CI", maximum_width = 400 )
        self.bt_continue = QPushButton("Consultá", maximum_width = 400)
        self.bt_continue.clicked.connect( self.show_report )

        # Allow only numbers
        regexp = QRegularExpression("[0-9]*")
        validator = QRegularExpressionValidator(regexp)
        self.inp_ci.set_validator(validator)

        self.inputs_layout.add_widget(self.inp_ci)
        self.inputs_layout.add_widget(self.bt_continue)
        self.inputs_layout.set_alignment(Qt.AlignCenter)

        inputs_layout_container = QWidget()
        inputs_layout_container.set_layout(self.inputs_layout)

        # Report View
        self.report_view = SummaryView()
        self.report_view.go_back.connect(lambda: self.show_index(0))

        self.stacked_layout.insert_widget(1, self.report_view)
        self.stacked_layout.insert_widget(0, inputs_layout_container)
        self.set_layout(self.stacked_layout)

        self.show_index(0)

    def show_report(self):
        try:
            self.report_view.load_data( int(self.inp_ci.text) )
        except TypeError:
            error_msg = DialogMessage(
                "Número de cédula no encontrado.",
                f"No encontramos ningún cliente con el número de cédula {self.inp_ci.text} "
            )
            ErrorMessageDialog(self, self.reset_inp_ci).show(error_msg)
            return
        
        self.set_styles(__file__) 
        self.show_index(1)

    def reset_inp_ci(self):
        self.inp_ci.text = ""
        self.inp_ci.set_focus()

    def show_index(self, index:int ) -> None:
        self.stacked_layout.set_current_index(index)
