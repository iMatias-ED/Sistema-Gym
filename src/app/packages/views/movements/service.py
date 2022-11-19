from typing import List

# Services
from ...shared.service import Service
from ..products.service import ProductsService
from ..customers.service import CustomersService

# Classes
from ..products.classes.product import Product
from ..customers.classes.customer import Customer
from .classes.product_selection import ProductSelection
from .classes.selected_product_info import SelectedProductInfo

class MovementsService(Service):
    DAY_IN_SECONDS = 86400

    products_service = ProductsService()
    customers_service = CustomersService()

    header_labels = ["Eliminar", "Editar", "Producto", "Cantidad", "Periodo", "Precio Unitario", "Total"]

    def search_users(self, name: str) -> List[Customer]:
        return self.customers_service.search(name)
    
    def search_products(self, name: str) -> List[Product]:
        return self.products_service.search(name)

    def get_product_by_code(self, code: str) -> Product:
        return self.products_service.get_by_code(code)

    def save_sales(self, products_data: list[SelectedProductInfo], customer: Customer):
        total_days = 0
        
        for selection in products_data:
            product = selection.data.product
            total_days += selection.data.price.valid_for_days

            query = f'''
                INSERT INTO sales(id_customer, id_product)
                VALUES ({customer.id}, {product.id})
                RETURNING id;
            '''

            sales_id = self._changes_query(query)
            self._insert_product_sales(sales_id, selection.data)

        self._update_customer_access_time(total_days, customer)

    def _insert_product_sales(self, id_sales: int, data: ProductSelection):
        query = f'''
            INSERT INTO products_sales(
                id_sales,
                quantity, 
                price,
                period,
                days_purchased,
                total
            ) VALUES (
                {id_sales},
                {data.quantity},
                {data.price.price},
                '{data.price.name}',
                {data.price.valid_for_days * data.quantity},
                {data.total}
            );
        '''
        self._changes_query(query)

    def _update_customer_access_time(self, days: int, customer: Customer):        
        new_expire_date = customer.access_until_date + ( days * self.DAY_IN_SECONDS )
        customer.access_until_date = new_expire_date

        query = f'''
            UPDATE customers SET
                access_until_date = {new_expire_date}
            WHERE id = {customer.id};
        '''
        self._changes_query(query)
    
