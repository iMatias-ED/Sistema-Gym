import sqlite3

from PySide6.QtCore import QObject, Signal

from .classes.price import Price

from .classes.period import Period
from .classes.product import Product

from typing import List, Tuple

# Inherits from QObject only to use Signals
class ProductsService(QObject):
    data_changed = Signal()
    header_labels = ["Eliminar", "Editar", "Código", "Nombre"]

    def __init__(self):
        super(ProductsService, self).__init__()
        # Add price periods to header
        for period in self.get_periods():
            self.header_labels.append( period.name )

    # Create
    def create(self, data: Product) -> None:
        query = f''' 
            INSERT INTO products (code, name)
                VALUES ('{data.code}', '{data.name}'); 
        '''
        self._changes_query(query)

        # Save product prices by period
        product_id = self._get_id_by_code(data.code)
        for price in data.prices:
            self._create_prices( product_id, price.name, price.price )
        self.data_changed.emit()
        
    def _create_prices(self, id_product:int, period_name:str, price:int) -> None:
        period_id = self._get_period_id_by_name(period_name)
        query = f'''
            INSERT INTO prices (id_product, id_period, price)
            VALUES ({id_product}, {period_id}, {price});
        '''
        self._changes_query(query)

    # Read
    def get_all(self) -> List[Product] : 
        query = f'''SELECT * FROM products;'''

        return self._format_products(self._read_query_fetchall(query))

    def get_by_id( self, id:int ) -> Product:
        query = f''' SELECT * FROM products WHERE id={id}; '''
        return Product(self._read_query_fetchone(query))

    def get_prices(self, product_id: int) -> List[ Price ]:
        query = f'''
            SELECT
                periods.id,
                periods.name,
                prices.price
            FROM prices
                LEFT JOIN periods ON prices.id_period = periods.id
            WHERE prices.id_product = {product_id};
        '''
        return self._format_prices(self._read_query_fetchall( query ))

    def _get_id_by_code(self, code: str) -> int:
        query = f''' SELECT id FROM products WHERE code='{code}'; '''
        return self._read_query_fetchone(query)["id"]

    def get_periods(self) -> List[ Period ]:
        query = f''' SELECT * FROM periods; '''
        return self._format_periods(self._read_query_fetchall(query))

    def _get_period_id_by_name(self, name:str) -> int:
        query = f'''SELECT id FROM periods WHERE name="{name}"'''
        return self._read_query_fetchone(query)["id"]


    # Update
    def update(self, data: Product) -> None:
        query = f''' 
            UPDATE products SET
                code = '{data.code}',
                name = '{data.name}'
            WHERE id = {data.id}
        '''
        self._changes_query(query)

        # Update product prices by period
        for price in data.prices:
            self._update_prices( data.id, price.name, price.price )
        self.data_changed.emit()
        
    def _update_prices(self, id_product:int, period_name:str, price:int) -> None:
        period_id = self._get_period_id_by_name(period_name)
        query = f'''
            UPDATE prices SET
                price = {price}
            WHERE 
                id_period={period_id} AND
                id_product={id_product};
        '''
        self._changes_query(query)

    # Delete
    def delete(self, product_id: int) -> None:
        query = f'''DELETE FROM products WHERE id={product_id};'''
        self._changes_query(query)
        self.data_changed.emit()

    # Formatting
    # TODO: Use list comprehensions 
    def _format_products(self, data) -> List[Product]:
        formatted = []

        for product in data:
            new_product = Product( dict(product) )
            for price in self.get_prices(new_product.id):
                new_product.save_price(price) 
            
            formatted.append( new_product ) 
        return formatted
    
    def _format_periods(self, data) -> List[Period]:
        formatted = []

        for period in data:
            formatted.append( Period( dict(period) ) ) 
        return formatted

    def _format_prices(self, data) -> List[Period]:
        formatted = []

        for price in data:
            formatted.append( Price( dict(price) ) ) 
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
        conn.row_factory = sqlite3.Row
        
        cursor = conn.cursor()
        data = cursor.execute(query)
        result = data.fetchall()

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

