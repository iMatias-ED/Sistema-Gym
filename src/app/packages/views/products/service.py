# Services
from ...shared.service import Service

# Classes
from .classes.price import Price
from .classes.period import Period
from .classes.product import Product

from typing import List

class ProductsService(Service):
    header_labels = ["Eliminar", "Editar", "Código", "Nombre"]

    def __init__(self):
        super(ProductsService, self).__init__()

        # Add price periods to header labels
        for period in self.get_periods():
            if period.name not in self.header_labels:
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

    # Search
    def search(self, name: str):
        query = f''' 
            SELECT * FROM products
            WHERE name LIKE '%{name}%'
        '''
        return self._format_products(self._read_query_fetchall(query))

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

    def _format_prices(self, data) -> List[Price]:
        formatted = []

        for price in data:
            formatted.append( Price( dict(price) ) ) 
        return formatted

