from typing import List

from PySide6.QtWidgets import QFrame, QVBoxLayout, QPushButton
from PySide6.QtCore import Signal
from __feature__ import snake_case, true_property

class sidebar_menu(QFrame):
    view_change_event = Signal(int)
    root_layout = QVBoxLayout()
    collection: List[QPushButton]

    def __init__(self, service):
        super(sidebar_menu, self).__init__(object_name="left-menu")
        self.users_service = service
        self.setup_ui()

    def setup_ui(self) -> None:
        self.bt_users = QPushButton("Usuarios", clicked=lambda: self.__on_view_change(0))
        self.bt_summary = QPushButton("Resumen General", clicked=lambda: self.__on_view_change(1))

        self.collection = [ self.bt_users, self.bt_summary ]

        self.root_layout.add_spacing(85)
        self.root_layout.add_widget(self.bt_users)
        self.root_layout.add_widget(self.bt_summary)
        self.root_layout.add_stretch()
        
        self.set_layout(self.root_layout)
        
    def __on_view_change(self, view_index: int) -> None:
        for bt in self.collection: bt.style_sheet = "background: transparent;"
        self.collection[view_index].style_sheet = "background: #249AF2;"

        self.view_change_event.emit(view_index)
