from PySide6.QtWidgets import *
from PySide6.QtCore import *
from __feature__ import snake_case, true_property

from .users_data_table import UsersDataTable
from .configure_user_data import ConfigureUserDataDialog
from ...service import ControlPanelService

class UsersView(QFrame):
    layout = QVBoxLayout()
    service = ControlPanelService()

    def __init__(self):
        super(UsersView, self).__init__()
        self.setup_ui()

    def setup_ui(self) -> None:
        self.table = UsersDataTable(self.service)
        self.dialog = ConfigureUserDataDialog(self, self.service)

        self.layout.add_widget( self.setup_title_frame(), 10 )
        self.layout.add_widget( self.table, 90 )

        self.set_layout(self.layout)
        self.__events_manager()

    def __events_manager(self) -> None:
        self.bt_create.clicked.connect( self.dialog.create )
        self.table.edit.connect( self.dialog.edit )

    def setup_title_frame(self) -> None:
        self.title = QLabel("Usuarios", alignment=Qt.AlignCenter, object_name="view-title")
        self.bt_create = QPushButton("+", maximum_width=50)

        layout = QHBoxLayout()
        layout.add_widget(self.bt_create, 10)
        layout.add_widget(self.title,  90)

        frame = QFrame()
        frame.set_layout(layout)
        return frame     