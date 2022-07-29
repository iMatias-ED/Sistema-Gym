from PySide6.QtCore import *
from PySide6.QtWidgets import *
from __feature__ import snake_case, true_property

from shared.top_menu import TopMenu 
from shared.content_box import ContentBox 

class Main(QMainWindow):
    def setup_ui(self):
        self.root_layout = QVBoxLayout()

        self.top_menu = TopMenu()
        self.content = ContentBox()

        self.top_menu.view_change.connect( self.show_content )

        self.root_layout.add_widget(self.top_menu, 20)
        self.root_layout.add_widget(self.content, 80)

        widget = QWidget()
        widget.set_layout(self.root_layout)
        self.set_central_widget(widget)

    @Slot(int)
    def show_content(self, index):
        self.content.show_index(index)

# Execute
import sys
app = QApplication(sys.argv)

window = Main()
window.setup_ui()
window.show()
# window.show_full_screen()

sys.exit(app.exec())