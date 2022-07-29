from PySide6.QtCore import *
from PySide6.QtWidgets import *
from __feature__ import snake_case, true_property

class Main(QMainWindow):
    def setup_ui(self):
        self.root_layout = QVBoxLayout()

        buttons_frame = QFrame()
        self.bt_logo = QPushButton("Logo / Panel de control")
        self.bt_movements = QPushButton("Movimientos")
        self.bt_customers = QPushButton("Clientes")
        self.bt_products = QPushButton("Productos")
        self.bt_control_panel = QPushButton("Marcar asistencia")

        buttons_layout = QHBoxLayout()
        buttons_layout.add_widget(self.bt_logo)
        buttons_layout.add_widget(self.bt_movements)
        buttons_layout.add_widget(self.bt_customers)
        buttons_layout.add_widget(self.bt_products)
        buttons_layout.add_widget(self.bt_control_panel)
        buttons_frame.set_layout(buttons_layout)
        buttons_frame.style_sheet = "background: gray;"


        content_frame = QFrame()
        content_frame.style_sheet = "background: gray;"

        self.root_layout.add_widget(buttons_frame, 20)
        self.root_layout.add_widget(content_frame, 80)

        widget = QWidget()
        widget.set_layout(self.root_layout)
        self.set_central_widget(widget)

# Execute
import sys
app = QApplication(sys.argv)

window = Main()
window.setup_ui()
window.show_full_screen()

sys.exit(app.exec())