from PySide6.QtWidgets import QVBoxLayout, QStackedLayout, QLineEdit, QLabel, QPushButton, QWidget, QHBoxLayout
from PySide6.QtCore import Qt, QRegularExpression
from PySide6.QtGui import QRegularExpressionValidator

from __feature__ import snake_case, true_property

from .components.summary_view import SummaryView
from ...shared.content_view import ContentView
from ...shared.components.error_message import ErrorDialog, ErrorMessage

class AssistControl(ContentView):
    inputs_layout = QVBoxLayout()
    stacked_layout = QStackedLayout()

    
    def setup_ui(self):
        self.set_styles(__file__)

        # Input View
        self.title = QLabel("¡Bienvenido/a!", object_name="inputs-title", alignment=Qt.AlignCenter)
        self.sub_title = QLabel("Ingrese su número de cédula para visualizar sus datos y marcar su asistencia.", 
            object_name="inputs-sub-title", alignment=Qt.AlignCenter)

        # Input
        self.inp_ci = QLineEdit( "7478938", placeholder_text="Número de cédula", maximum_width = 600, object_name="input-ci" )
        self.inp_ci.returnPressed.connect( self.show_report )
        input_layout = QHBoxLayout()
        input_layout.add_widget(self.inp_ci)
        
        # Button
        self.bt_continue = QPushButton("Consultá", object_name="bt-continue", maximum_width = 250)
        self.bt_continue.clicked.connect( self.show_report )

        bt_layout = QHBoxLayout()
        bt_layout.add_widget(self.bt_continue)

        # Allow only numbers
        regexp = QRegularExpression("[0-9]*")
        validator = QRegularExpressionValidator(regexp)
        self.inp_ci.set_validator(validator)

        self.inputs_layout.add_spacing(200)
        self.inputs_layout.add_widget(self.title)
        self.inputs_layout.add_widget(self.sub_title)
        self.inputs_layout.add_layout(input_layout)
        self.inputs_layout.add_layout(bt_layout)
        self.inputs_layout.add_stretch()

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
            error_msg = ErrorMessage(
                "Número de cédula no encontrado.",
                f"No encontramos ningún cliente con el número de cédula {self.inp_ci.text} "
            )
            ErrorDialog(self, self.reset_inp_ci).show(error_msg)
            return
        except ValueError:
            error_msg = ErrorMessage(
                "Número de cédula no encontrado.",
                f"No encontramos ningún cliente con el número de cédula {self.inp_ci.text} "
            )
            ErrorDialog(self, self.reset_inp_ci).show(error_msg)
            return
        
        self.set_styles(__file__) 
        self.show_index(1)

    def reset_inp_ci(self):
        self.inp_ci.text = ""
        self.inp_ci.set_focus()

    def show_index(self, index:int ) -> None:
        self.stacked_layout.set_current_index(index)
