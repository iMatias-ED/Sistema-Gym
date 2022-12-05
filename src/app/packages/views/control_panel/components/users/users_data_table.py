from typing import List, Union

# Service
from ...service import ControlPanelService

# Classes
from .....shared.components.data_table import DataTable, TableItem, Action

class UsersDataTable(DataTable):

    def __init__(self, service: ControlPanelService):
        super(UsersDataTable, self).__init__()
        self.users_service = service
        self.users_service.data_changed.connect( self.refresh )

        self.setup_table(self.users_service.header_labels)
        self.load_data()
        
    def load_data(self) -> None:
        self.users = self.users_service.get_all()
        table_items: List[ List[ Union[ Action, TableItem ] ]] = []

        for user in self.users:
            table_items.append([
                Action( column=0, label="X", slot=self.delete_clicked , params=user.id ),
                Action( column=1, label="E", slot=self.edit_clicked , params=user.id ),
                TableItem( column=2, value=user.full_name),
                TableItem( column=3, value=user.ci),
                TableItem( column=4, value=user.phone),
                TableItem( column=5, value=user.email),
                TableItem( column=6, value=user.genre),
            ])
        self.insert_items(table_items)

    def edit_clicked(self, user_id:int) -> None:
        self.edit.emit(user_id)
    
    def delete_clicked(self, user_id:int) -> None:
        self.delete.emit(user_id)
        self.users_service.delete(user_id)

