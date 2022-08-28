import sqlite3
from .classes.product import Product

from typing import Dict, List, Tuple

class ProductsService:
    header_labels = ["Eliminar", "Editar", "Código", "Nombre"]

    def __init__(self):
        for period in self.get_periods():
            self.header_labels.append( period[1] ) #[1] -> name

    # Create
    def create(self, code:str, name:str, prices_info: List[Tuple[int, str]]):
        query = f''' 
            INSERT INTO products (code, name)
                VALUES ('{code}', '{name}'); 
        '''
        self._changes_query(query)

        # Save product prices by period
        product_id = self.get_id_by_code(code)
        for data in prices_info:
            #[0]->period_id, [1]->price
            #(price should be already type int. Temporary parsing)
            self.create_prices( product_id, data[0], int(data[1]) )
        
    def create_prices(self, id_product:int, id_period:int, price:int):
        query = f'''
            INSERT INTO prices (id_product, id_period, price)
            VALUES ({id_product}, {id_period}, {price});
        '''
        self._changes_query(query)

    # Read
    def get_all_products(self) -> List[Product] : 
        query = f''' SELECT * FROM products; '''
        return self.format_data(self._read_query_fetchall(query))

    def get_product_prices(self, product_id: int):
        query = f'''
            SELECT 
                periods.name,
                prices.price
            FROM prices
                LEFT JOIN periods ON prices.id_period = periods.id
            WHERE prices.id_product = {product_id};
        '''

        return self._read_query_fetchall( query )

    def get_id_by_code(self, code: str):
        query = f''' SELECT id FROM products WHERE code='{code}'; '''
        return self._read_query_fetchone(query)

    def get_periods(self):
        query = f''' SELECT * FROM periods; '''
        return self._read_query_fetchall(query)

    # Delete
    def delete(self, product_id: int):
        query = f'''DELETE FROM products WHERE id={product_id};'''
        print(query)
        self._changes_query(query)


    # Formatting
    def format_data(self, data ):
        formatted = []

        for product in data:
            formatted.append( Product( product ) ) 

        return formatted

    # Execute Queries
    def _changes_query(self, query: str):
        conn = sqlite3.connect("src/app/db/test.db")
        
        cursor = conn.cursor()
        cursor.execute(query)

        conn.commit()
        conn.close()

    def _read_query_fetchall(self, query: str):
        conn = sqlite3.connect("src/app/db/test.db")
        
        cursor = conn.cursor()
        data = cursor.execute(query)
        result = data.fetchall()

        conn.close()
        return result 

    def _read_query_fetchone(self, query: str):
        conn = sqlite3.connect("src/app/db/test.db")
        
        cursor = conn.cursor()
        data = cursor.execute(query)
        result = data.fetchone()

        conn.close()
        return result[0]
