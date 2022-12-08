from typing import List, Union

# Service
from ...service import ControlPanelService

# Classes
from .....shared.components.data_table import DataTable, DevAction, TableItem, Action

class UsersDataTable(DataTable):

    def __init__(self, service: ControlPanelService):
        super(UsersDataTable, self).__init__()
        self.users_service = service
        self.users_service.data_changed.connect( self.refresh )

        self.setup_dev(self.users_service.header_labels2)
        self.load_data()
        
    def load_data(self) -> None:
        self.users = self.users_service.get_all()

        actions = [
            DevAction(0, "X", self.delete_clicked, True, "id"),
            DevAction(1, "E", self.edit_clicked, True, "id"),
        ]
        self.test_insert(self.users, actions)

    def edit_clicked(self, user_id:int) -> None:
        self.edit.emit(user_id)
    
    def delete_clicked(self, user_id:int) -> None:
        self.delete.emit(user_id)
        self.users_service.delete(user_id)

