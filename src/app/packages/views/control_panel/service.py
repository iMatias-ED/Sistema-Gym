from typing import List, Union
from datetime import datetime

from ...shared.services.service import DBService
from ...shared.services.security_service import SecurityService
from .classes.user import User


class ControlPanelService(DBService):
    TABLE = "users"
    security_service = SecurityService()

    header_labels = ["Eliminar", "Editar", "Nombre", "CI", "Teléfono", "Email", "Género"]

    # Create
    def create(self, c:User) -> None:

        query = f'''  
            INSERT INTO users (
                full_name,
                ci,
                phone,
                email,
                genre,
                password
            ) VALUES (
                '{c.full_name}',
                {c.ci},
                '{c.phone}',
                '{c.email}',
                '{c.genre}',
                '{self.security_service.encrypt(c.password)}'
            );
        '''
        print(query)
        self._changes_query(query)
        self.data_changed.emit()

    # Read
    def get_all(self) -> List[User] : 
        query = f''' SELECT * FROM {self.TABLE} '''
        return self._format_users(self._read_query_fetchall(query))

    def get_by_id( self, id:int ) -> User:
        query = f''' SELECT * FROM {self.TABLE} WHERE id={id}; '''
        return self._format_users(self._read_query_fetchone(query))

    def get_by_ci_number( self, ci:int ) -> User:
        query = f''' SELECT * FROM {self.TABLE} WHERE ci={ci}; '''
        return self._format_users(self._read_query_fetchone(query))

    # Update
    def update(self, c:User ) -> None:
        query = f''' 
            UPDATE users SET
                full_name = '{c.full_name}',
                ci = {c.ci},
                phone = '{c.phone}',
                email = '{c.email}',
                genre = '{c.genre}',
                password = '{self.security_service.encrypt(c.password)}'
            WHERE id = {c.id}
            RETURNING id
            ;
        '''
        self._changes_query(query)
        self.data_changed.emit()

    # Delete
    def delete(self, id: int) -> None:
        query = f'''DELETE FROM {self.TABLE} WHERE id={id};'''
        self._changes_query(query)
        self.data_changed.emit()


    # Formatting
    def _format_users(self, data: Union[dict, list[dict]]) -> List[User]:

        if isinstance(data, dict):
            return User(dict(data))

        formatted = []
        for user in data:
            formatted.append( User( dict(user) ) ) 
        return formatted

    def get_total_inflows(self):
        query = f'''
            SELECT SUM(amount) as total FROM cash_flow 
            WHERE id_movement_type = 2;
        '''
        return self._read_query_fetchone(query)

    def get_total_outflows(self):
        query = f'''
            SELECT SUM(amount) as total FROM cash_flow 
            WHERE id_movement_type = 1;
        '''
        return self._read_query_fetchone(query)

    def get_total_sales(self):
        query = f'''
            SELECT sum(total) as total FROM products_sales;
        '''
        return self._read_query_fetchone(query)
