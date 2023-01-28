from typing import List, Union
from datetime import datetime

from ...shared.services.service import DBService, TableHeaderLabel
from .classes.customer import Customer
from .classes.access_time_by_product import AccessTimeByProduct

class CustomersService(DBService):
    TABLE = "customers"

    header_labels = [
        TableHeaderLabel("delete", "Eliminar"),
        TableHeaderLabel("edit", "Editar"),
        TableHeaderLabel("full_name", "Nombre"),
        TableHeaderLabel("ci", "CI"),
        TableHeaderLabel("ruc", "RUC"),
        TableHeaderLabel("invoice_to", "Razón Social"),
        TableHeaderLabel("phone", "Teléfono"),
        TableHeaderLabel("email", "Email"),
        TableHeaderLabel("genre", "Género"),
    ]

    # Create
    def create(self, c:Customer) -> None:
        query = f'''  
            INSERT INTO {self.TABLE} (ci, ruc, full_name, phone, email, genre, invoice_to)
                VALUES (
                    '{c.ci}', '{c.ruc}', '{c.full_name}', '{c.phone}',
                    '{c.email}', '{c.genre}', '{c.invoice_to}'
                )
                RETURNING id;
        '''
        print(query)
        customer_id = self._changes_query(query)
        self.update_customer_access_time( customer_id, c )

        self.data_changed.emit()

    def update_customer_access_time( self, id: int, c: Customer ):
        # Remove old access time data
        self._changes_query("DELETE FROM customers_products_access_time;")

        # Insert new values
        query = f'''            
            INSERT INTO customers_products_access_time 
                ( id_customer, id_product, access_until_date )
            VALUES 
        '''
        # Stringify values
        for access_time in c.access_time:
            query += f"( {id}, {access_time.id_product}, '{access_time.access_until_date}' )"
            query += self.values_separator( c.access_time, access_time)


        self._changes_query(query)

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
            invoice_to
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
            invoice_to
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
            invoice_to
        FROM {self.TABLE} WHERE ci={ci}; '''

        return self._format_customers(self._read_query_fetchone(query))

    def _get_access_time( self, id: int ):
        query = f'''
            SELECT 
                id_product,
                access_until_date
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
                invoice_to          = '{c.invoice_to}'
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
    def _format_customers(self, data: Union[dict, List[dict]]) -> List[Customer]:
        formatted = []

        if isinstance(data, dict):
            new_customer = Customer( dict(data) )
            access_time = self._get_access_time(new_customer.id)
            for time in access_time:
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
