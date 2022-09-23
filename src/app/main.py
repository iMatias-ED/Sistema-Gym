from PySide6.QtCore import *
from PySide6.QtWidgets import *
from __feature__ import snake_case, true_property

# Typing
from packages.shared.content_view import ContentView

# Layout
from packages.layout.top_menu import TopMenu 
from packages.layout.content_box import ContentBox 

# Views
from packages.views.assist_control.assist_control import AssistControl
from packages.views.cash_flow.cash_flow import CashFlow
from packages.views.control_panel.control_panel import ControlPanel
from packages.views.customers.customers import Customers
from packages.views.products.products import Products

class Main(QMainWindow):
    root_layout = QVBoxLayout()
    views: dict[str, ContentView] = {}

    def __init__(self):
        super(Main, self).__init__()
        self.setup_ui()
        self.__create_views()
        self.__add_views_to_content_box()

    def stylesheet(self):
        styles = open( "src/app/styles.css", "r" )
        return styles.read()

    def setup_ui(self):
        self.style_sheet = self.stylesheet()

        self.top_menu = TopMenu()
        self.content = ContentBox()
        self.top_menu.view_change.connect( self.show_content )

        self.root_layout.add_widget(self.top_menu, 20)
        self.root_layout.add_widget(self.content, 80)

        widget = QWidget()
        widget.set_layout(self.root_layout)
        self.set_central_widget(widget)

    @Slot(int)
    def show_content(self, index: int):
        self.content.show_index(index)

    def __create_views(self): 
        self.views['assist_control'] = AssistControl()
        self.views['cash_flow']      = CashFlow()
        self.views['control_panel']  = ControlPanel()
        self.views['customers']      = Customers()
        self.views['products']       = Products()

    def __add_views_to_content_box(self):
        self.content.add_content(self.views['cash_flow'], 0)
        self.content.add_content(self.views['customers'], 1)
        self.content.add_content(self.views['products'], 2)
        self.content.add_content(self.views['assist_control'], 3)
        self.content.add_content(self.views['control_panel'], 4)

        # temporal
        self.content.show_index(3)

# Execute
import sys
app = QApplication(sys.argv)

window = Main()
window.show()
# window.show_full_screen()

sys.exit(app.exec())