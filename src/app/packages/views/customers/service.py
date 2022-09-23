import sqlite3
from datetime import datetime
from typing import List, Tuple

from PySide6.QtCore import QObject, Signal
from .classes.customer import Customer

# Inherits from QObject to use Signals
class CustomersService(QObject):
    TABLE = "customers"

    data_changed = Signal()
    header_labels = ["Eliminar", "Editar", "Nombre", "CI", "RUC", "Razón Social", "Teléfono", "Email", "Género", "Fin de membresía"]

    # Create
    def create(self, c:Customer) -> None:
        query = f'''  
            INSERT INTO {self.TABLE} (ci, ruc, full_name, phone, email, genre, invoice_to, access_until_date)
                VALUES (
                    '{c.ci}', '{c.ruc}', '{c.full_name}', '{c.phone}',
                    '{c.email}', '{c.genre}', '{c.invoice_to}',
                    {self._to_timestamp(c.access_until_date)}
                ); 
        '''
        self._changes_query(query)
        self.data_changed.emit()

    # Read
    def get_all(self) -> List[Customer] : 
        query = f''' SELECT 
            id,
            ci,
            ruc,
            full_name,
            phone,
            email,
            genre,
            invoice_to,
            strftime('%d/%m/%Y', datetime(access_until_date, 'unixepoch')) as access_until_date
        FROM {self.TABLE} '''
            # DATETIME(access_until_date, 'unixepoch', 'localtime') as access_until_date
        return self._format_data(self._read_query_fetchall(query))

    def get_by_id( self, id:int ) -> Customer:
        query = f''' SELECT 
            id,
            ci,
            ruc,
            full_name,
            phone,
            email,
            genre,
            invoice_to,
            DATETIME(access_until_date, 'unixepoch', 'localtime') as access_until_date
        FROM {self.TABLE} WHERE id={id}; '''
        return Customer(self._read_query_fetchone(query))

    # Update
    def update(self, id_product:int, code:str, name:str, prices_info: List[Tuple[int, int]]) -> None:
        query = f''' 
            UPDATE {self.TABLE} SET
                code = '{code}',
                name = '{name}'
            WHERE id = {id_product}
        '''
        # self._changes_query(query)
        print(query)
        self.data_changed.emit()

    # Delete
    def delete(self, product_id: int) -> None:
        query = f'''DELETE FROM {self.TABLE} WHERE id={product_id};'''
        # self._changes_query(query)
        print(query)
        self.data_changed.emit()

    # Formatting
    def _format_data(self, data: List) -> List[Customer]:
        formatted = []

        for customer in data:
            formatted.append( Customer( dict(customer) ) ) 

        return formatted

    def _to_timestamp(self, date:str):
        # Access until 11:59 p.m
        print('date', type(date) == int)
        return datetime.strptime(date, "%d/%m/%Y").timestamp() + 86400 - 1

    # Execute Queries
    def _changes_query(self, query: str):
        conn = sqlite3.connect("src/app/db/test.db")
        
        cursor = conn.cursor()
        cursor.execute(query)

        conn.commit()
        conn.close()

    def _read_query_fetchall(self, query: str):
        conn = sqlite3.connect("src/app/db/test.db")
        conn.row_factory = sqlite3.Row

        cursor = conn.cursor()
        cursor.execute(query)
        result = cursor.fetchall()
        
        conn.close()
        return result

    def _read_query_fetchone(self, query: str):
        conn = sqlite3.connect("src/app/db/test.db")
        conn.row_factory = sqlite3.Row
        
        cursor = conn.cursor()
        data = cursor.execute(query)
        result = data.fetchone()

        conn.close()
        return dict(result)

