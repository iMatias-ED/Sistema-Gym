from typing import Callable, Dict, List, Tuple
from PySide6.QtWidgets import *
from PySide6.QtCore import *
from __feature__ import snake_case, true_property

from ...service import ControlPanelService

class UsersDataTable(QTableWidget):
    #Both emits the user_id
    edit = Signal(int)
    delete = Signal(int)

    def __init__(self, service: ControlPanelService):
        super(UsersDataTable, self).__init__()
        self.users_service = service
        self.users_service.data_changed.connect( self.refresh )

        self.config_table()

    def config_table(self) -> None:
        self.vertical_header().visible = False
        self.column_count = len(self.users_service.header_labels)
        self.set_horizontal_header_labels(self.users_service.header_labels)

        self.horizontal_header().stretch_last_section = True
        self.horizontal_header().set_section_resize_mode(QHeaderView.Stretch)

        self.load_data()
        
    def load_data(self) -> None:
        self.users = self.users_service.get_all()
        self.row_count = len(self.users)

        def create_button(text:str, user_id: int, on_clicked: Callable)  -> QPushButton:
            button = QPushButton(text)
            button.clicked.connect( lambda: on_clicked(user_id) )
            return button

        for row, user in enumerate(self.users):
            self.set_cell_widget(row, 0, create_button( "X", user.id, self.delete_clicked ))
            self.set_cell_widget(row, 1, create_button( "E", user.id, self.edit_clicked))

            self.set_item(row, 2, QTableWidgetItem(user.full_name))
            self.set_item(row, 3, QTableWidgetItem(str(user.ci)))
            self.set_item(row, 4, QTableWidgetItem(user.phone))
            self.set_item(row, 5, QTableWidgetItem(user.email))
            self.set_item(row, 6, QTableWidgetItem(user.genre))

    def refresh(self)  -> None:
        self.clear_contents()
        self.load_data()

    def edit_clicked(self, user_id:int) -> None:
        self.edit.emit(user_id)
    
    def delete_clicked(self, user_id:int) -> None:
        self.delete.emit(user_id)
        self.users_service.delete(user_id)

    @Slot()
    def _on_data_changed(self) -> None:
        self.refresh()
