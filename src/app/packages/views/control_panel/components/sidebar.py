from PySide6.QtWidgets import *
from PySide6.QtCore import *
from __feature__ import snake_case, true_property

class Sidebar(QFrame):
    view_change_event = Signal(int, bool)
    root_layout = QVBoxLayout()

    def __init__(self, service):
        super(Sidebar, self).__init__(object_name="sidebar")
        self.users_service = service
        self.setup_ui()

    def setup_ui(self) -> None:
        self.bt_users = QPushButton("Usuarios")
        self.root_layout.add_widget(self.bt_users)
        
        self.set_layout(self.root_layout)
        
    def __on_view_change(self) -> None:
        self.view_change_event.emit()
