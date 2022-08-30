import sqlite3

from PySide6.QtCore import QObject, Signal
from .classes.product import Product

from typing import List, Tuple

# Inherits from QObject to use Signals
class ProductsService(QObject):
    data_changed = Signal()
    header_labels = ["Eliminar", "Editar", "Código", "Nombre"]

    def __init__(self):
        super(ProductsService, self).__init__()

        # Add price periods to header
        for period in self.get_periods():
            self.header_labels.append( period[1] ) #[1] -> name

    # Create
    def create(self, code:str, name:str, prices_info: List[Tuple[int, int]]) -> None:
        query = f''' 
            INSERT INTO products (code, name)
                VALUES ('{code}', '{name}'); 
        '''
        self._changes_query(query)

        # Save product prices by period
        product_id = self._get_id_by_code(code)
        for data in prices_info:
            #[0]->period_id, [1]->price
            self.create_prices( product_id, data[0], data[1] )
        self.data_changed.emit()
        
    def create_prices(self, id_product:int, id_period:int, price:int) -> None:
        query = f'''
            INSERT INTO prices (id_product, id_period, price)
            VALUES ({id_product}, {id_period}, {price});
        '''
        self._changes_query(query)

    # Read
    def get_all(self) -> List[Product] : 
        query = f''' SELECT * FROM products; '''
        return self._format_data(self._read_query_fetchall(query))

    def get_by_id( self, id:int ) -> Product:
        query = f''' SELECT * FROM products WHERE id={id}; '''
        return Product(self._read_query_fetchone(query))

    def get_prices(self, product_id: int) -> List[ Tuple[str, int] ]:
        query = f'''
            SELECT 
                periods.name,
                prices.price
            FROM prices
                LEFT JOIN periods ON prices.id_period = periods.id
            WHERE prices.id_product = {product_id};
        '''
        return self._read_query_fetchall( query )

    def _get_id_by_code(self, code: str) -> int:
        query = f''' SELECT id FROM products WHERE code='{code}'; '''
        return self._read_query_fetchone(query)

    def get_periods(self) -> List[ Tuple[int, str, int] ]:
        query = f''' SELECT * FROM periods; '''
        return self._read_query_fetchall(query)

    # Update
    def update(self, id_product:int, code:str, name:str, prices_info: List[Tuple[int, int]]) -> None:
        query = f''' 
            UPDATE products SET
                code = '{code}',
                name = '{name}'
            WHERE id = {id_product}
        '''
        self._changes_query(query)

        # Update product prices by period
        for data in prices_info:
            # [0]->period_id, [1]->price
            # (price should be already type int. Temporary parsing)
            self.__update_prices( id_product, data[0], int(data[1]) )

        self.data_changed.emit()
        
    def _update_prices(self, id_product:int, id_period:int, price:int) -> None:
        query = f'''
            UPDATE prices SET
                price = {price}
            WHERE 
                id_period={id_period} AND
                id_product={id_product};
        '''
        self._changes_query(query)

    # Delete
    def delete(self, product_id: int) -> None:
        query = f'''DELETE FROM products WHERE id={product_id};'''
        self._changes_query(query)
        self.data_changed.emit()

    # Formatting
    def _format_data(self, data) -> List[Product]:
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

        if len(result) > 1: return result
        return result[0]

