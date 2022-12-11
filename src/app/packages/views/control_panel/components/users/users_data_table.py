# Service
from ...service import ControlPanelService

# Classes
from .....shared.components.data_table import DataTable, Action
from .....shared.components.confirmation_message import ConfirmationMessage, ConfirmationDialog

class UsersDataTable(DataTable):

    def __init__(self, service: ControlPanelService):
        super(UsersDataTable, self).__init__()
        self.users_service = service
        self.users_service.data_changed.connect( self.refresh )

        self.setup_table(self.users_service.header_labels2)
        self.load_data()
        
    def load_data(self) -> None:
        self.users = self.users_service.get_all()

        actions = [
            Action(0, "X", self.delete_clicked, True, "full_name", "id"),
            Action(1, "E", self.edit_clicked, True, "id"),
        ]
        self.insert_values(self.users, actions)

    def edit_clicked(self, user_id:int) -> None:
        self.edit.emit(user_id)
    
    def delete_clicked(self, user_name:str, user_id:int) -> None:
        ConfirmationDialog(self, lambda: self.delete(user_id)).show(ConfirmationMessage(
            "¿Está seguro?",
            f'''Se eliminará el usuario "{user_name}" y toda la información asociada.''',
            "Esta acción no se puede deshacer."
        ))

    def delete(self, user_id:int) -> None:
        self.delete.emit(user_id)
        self.users_service.delete(user_id)

