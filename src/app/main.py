from PySide6.QtCore import *
from PySide6.QtWidgets import *
from __feature__ import snake_case, true_property

# Typing
from packages.shared.content_view import ContentView

# Verify User
from packages.shared.components.verify_user import VerifyUserIdentityDialog

# Layout
from packages.layout.top_menu import TopMenu 
from packages.layout.content_box import ContentBox 

# Views
from packages.views.assist_control.assist_control import AssistControl
from packages.views.movements.movements import Movements
from packages.views.control_panel.control_panel import ControlPanel
from packages.views.customers.customers import Customers
from packages.views.products.products import Products

class Main(QMainWindow):
    root_layout = QVBoxLayout()
    views: dict[str, ContentView] = {}
    user_verified = False
    last_shown_index: int = None;

    def __init__(self):
        super(Main, self).__init__()
        self.size = QSize(1366, 720)
        self.style_sheet = self.stylesheet()

        self.verify_user_dialog = VerifyUserIdentityDialog(self)
        self.verify_user_dialog.finished.connect(self.on_login_closed)
        self.verify_user_dialog.user_verified.connect(self.on_user_verified)

    def on_login_closed(self):
        if not self.user_verified:
            sys.exit()

    def on_user_verified(self):
        self.user_verified = True
        self.verify_user_dialog.user_verified.disconnect(self.on_user_verified)

        self.setup_ui()
        self.__create_views()
        self.__add_views_to_content_box()
        self.show()
        # self.show_full_screen()

    def stylesheet(self) -> str:
        styles = open( "src/app/styles.css", "r" )
        return styles.read()

    def setup_ui(self):
        self.top_menu = TopMenu()
        self.content = ContentBox()
        self.top_menu.view_change.connect( self.show_content )

        self.root_layout.add_widget(self.top_menu, 20)
        self.root_layout.add_widget(self.content, 80)

        widget = QWidget()
        widget.set_layout(self.root_layout)
        self.set_central_widget(widget)

    @Slot(int)
    def show_content(self, index: int, ):
        if self.last_shown_index == 3:
            self.verify_user_dialog.show()
            self.verify_user_dialog.bt_verify.text = "Continuar"

            def after_verification():
                self.content.show_index(index)
                self.top_menu.active_button(index)
                self.last_shown_index = index

                # Delete the slot after using it. Avoid multiple calls.
                self.verify_user_dialog.user_verified.disconnect(after_verification)

            self.verify_user_dialog.user_verified.connect(after_verification)
            return
            

        self.last_shown_index = index
        self.content.show_index(index)
        self.top_menu.active_button(index)

    def __create_views(self): 
        self.views['assist_control'] = AssistControl()
        self.views['movements']      = Movements()
        self.views['control_panel']  = ControlPanel()
        self.views['customers']      = Customers()
        self.views['products']       = Products()

    def __add_views_to_content_box(self):
        self.content.add_content(self.views['movements'], 0)
        self.content.add_content(self.views['customers'], 1)
        self.content.add_content(self.views['products'], 2)
        self.content.add_content(self.views['assist_control'], 3)
        self.content.add_content(self.views['control_panel'], 4)

        # temporal
        self.show_content(1)

# Execute
import sys
app = QApplication(sys.argv)

window = Main()
# window.show_full_screen()

sys.exit(app.exec())