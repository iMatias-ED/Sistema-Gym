from typing import List, Union
from datetime import datetime

from ...shared.service import Service
from .classes.customer import Customer
from .classes.access_time_by_product import AccessTimeByProduct

class CustomersService(Service):
    TABLE = "customers"

    header_labels = ["Eliminar", "Editar", "Nombre", "CI", "RUC", "Razón Social", "Teléfono", "Email", "Género", "Fin de membresía"]

    # Create
    def create(self, c:Customer) -> None:
        query = f'''  
            INSERT INTO {self.TABLE} (ci, ruc, full_name, phone, email, genre, invoice_to, access_until_date)
                VALUES (
                    '{c.ci}', '{c.ruc}', '{c.full_name}', '{c.phone}',
                    '{c.email}', '{c.genre}', '{c.invoice_to}',
                    {self._to_timestamp(c.access_until_date)}
                )
                RETURNING id;
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
            strftime('%d/%m/%Y', datetime(access_until_date, 'unixepoch', 'localtime')) as access_until_date
        FROM {self.TABLE} '''
        return self._format_customers(self._read_query_fetchall(query))

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
            strftime('%d/%m/%Y', datetime(access_until_date, 'unixepoch', 'localtime')) as access_until_date
        FROM {self.TABLE} WHERE id={id}; '''
        return self._format_customers(self._read_query_fetchone(query))

    def get_by_ci_number( self, ci:int ) -> Customer:
        query = f''' SELECT 
            id,
            ci,
            ruc,
            full_name,
            phone,
            email,
            genre,
            invoice_to,
            strftime('%d/%m/%Y', datetime(access_until_date, 'unixepoch', 'localtime')) as access_until_date
        FROM {self.TABLE} WHERE ci={ci}; '''
        return self._format_customers(self._read_query_fetchone(query))

    def _get_access_time( self, id: int ):
        query = f'''
            SELECT 
                id_product,
                access_until_date as unix_time,
                strftime('%d/%m/%Y', datetime(access_until_date, 'unixepoch', 'localtime')) as time
            FROM customers_products_access_time
            WHERE id_customer = {id};
        '''
        return self._read_query_fetchall(query)

    # Update
    def update(self, c:Customer ) -> None:
        query = f''' 
            UPDATE {self.TABLE} SET
                ci                  =  {c.ci},
                ruc                 = '{c.ruc}',
                phone               = '{c.phone}',
                email               = '{c.email}',
                genre               = '{c.genre}',
                full_name           = '{c.full_name}',
                invoice_to          = '{c.invoice_to}',
                access_until_date   =  {self._to_timestamp(c.access_until_date)}
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

    # Search
    def search(self, name: str):
        query = f''' 
            SELECT * FROM customers
            WHERE full_name LIKE '%{name}%'
        '''
        return self._format_customers(self._read_query_fetchall(query))

    # Formatting
    def _format_customers(self, data: Union[dict, list[dict]]) -> List[Customer]:
        formatted = []

        if isinstance(data, dict):
            new_customer = Customer( dict(data) )
            for time in self._get_access_time(new_customer.id):
                new_customer.add_access_time( AccessTimeByProduct(dict( time )) )
            return new_customer

        for customer in data:
            new_customer = Customer( dict(customer) )
            for time in self._get_access_time(new_customer.id):
                new_customer.add_access_time( AccessTimeByProduct(dict( time )) )

            formatted.append( new_customer ) 
        return formatted

    def _to_timestamp(self, date:str):
        # Access until 11:59 p.m
        return datetime.strptime(date, "%d/%m/%Y").timestamp() + 86400 - 1
