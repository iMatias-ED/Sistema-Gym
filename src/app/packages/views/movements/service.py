import time
from typing import List, Union

# Services
from ...shared.services.service import DBService
from ..products.service import ProductsService
from ..customers.service import CustomersService

# Classes
from ..products.classes.product import Product
from ..customers.classes.customer import Customer
from .classes.sale_record import SaleRecord
from .classes.cash_flow_item import CashFlowItem
from .classes.movement_type import MovementType
from .classes.product_sold import ProductSold
from .classes.sale_item import SaleItem
from ...shared.classes.table_header_label import TableHeaderLabel

class MovementsService(DBService):
    DAY_IN_SECONDS = 86400

    products_service = ProductsService()
    customers_service = CustomersService()

    header_labels = ["Eliminar", "Editar", "Producto", "Cantidad", "Periodo", "Precio Unitario", "Total"]
    header_labels_2 = [
        TableHeaderLabel("action", "Eliminar"),
        TableHeaderLabel("action", "Editar"),
        TableHeaderLabel("product_name", "Producto"),
        TableHeaderLabel("quantity", "Cantidad"),
        TableHeaderLabel("period", "Periodo"),
        TableHeaderLabel("price", "Precio Unitario"),
        TableHeaderLabel("total", "Total"),
    ]


    def search_users(self, name: str) -> List[Customer]:
        return self.customers_service.search(name)
    
    def search_products(self, name: str) -> List[Product]:
        return self.products_service.search(name)

    def get_product_by_code(self, code: str) -> Product:
        return self.products_service.get_by_code(code)

    def save_sales(self, products_data: list[SaleItem], customer: Customer):
        total_days = 0

        query = f'''
            INSERT INTO sales(id_customer)
            VALUES ({customer.id})
            RETURNING id;
        '''
        sales_id = self._changes_query(query)

        for item in products_data:
            product = item.product
            total_days += item.price.valid_for_days

            self._insert_product_sales(sales_id, item)

        self._update_customer_access_time(total_days, customer, product)

    def _insert_product_sales(self, id_sales: int, data: SaleItem):
        query = f'''
            INSERT INTO products_sales(
                id_sales,
                id_product,
                quantity, 
                price,
                period,
                days_purchased,
                total
            ) VALUES (
                {id_sales},
                {data.product.id},
                {data.quantity},
                {data.price.price},
                '{data.price.name}',
                {data.price.valid_for_days * data.quantity},
                {data.total}
            );
        '''
        self._changes_query(query)

    def _update_customer_access_time(self, days: int, customer: Customer, product: Product):        
        access_time = customer.access_time_by_product_id(product.id)
        
        if access_time:
            new_expire_date = access_time.unix_time + ( days * self.DAY_IN_SECONDS )
            query = f'''
                UPDATE customers_products_access_time SET
                    access_until_date = {new_expire_date}
                WHERE  
                    id_customer = {customer.id} AND
                    id_product = {product.id};
            '''
        else:
            new_expire_date = time.time() + ( days * self.DAY_IN_SECONDS )
            query = f'''
                INSERT INTO customers_products_access_time
                    (id_customer, id_product, access_until_date)
                VALUES (
                    {customer.id},
                    {product.id},
                    {new_expire_date}
                );
            '''
        
        self._changes_query(query)
    
    def get_purchases_by_customer_id(self, id_customer: int) -> list[SaleRecord]:
        query = f'''
            SELECT * FROM sales WHERE id_customer={id_customer};
        '''

        return self._format_purchases (self._read_query_fetchall(query))

    def _get_products_purchased(self, id_sales: int):
        query = f'''
            SELECT * FROM products_sales 
            WHERE id_sales = {id_sales};
        '''
        return self._read_query_fetchall(query)

    def _format_purchased_products(self, data: dict):
        data["product"] = self.products_service.get_by_id(data["id_product"])
        return ProductSold(data)

    def _format_purchases(self, data: list) -> list[SaleRecord]:
        def create(data: dict) -> SaleRecord:
            purchase = SaleRecord(data)

            for product in self._get_products_purchased(purchase.id):
                purchase.save_product(self._format_purchased_products(dict(product)))
            return purchase

        return [ create(dict(purchase)) for purchase in data ]

    def _format_cash_flow_types(self, data: list[dict]) -> list[MovementType]:
        formatted = [ MovementType(flow_type) for flow_type in data ]
        return formatted
        

    def get_cash_flow_types(self):
        query = "SELECT * FROM cash_movement_types;"
        return self._format_cash_flow_types(self._read_query_fetchall(query))

    def register_cash_flow(self, data: CashFlowItem):
        query = f'''
            INSERT INTO cash_flow (
                id_user,
                id_movement_type,
                amount,
                description
            ) VALUES (
                {data.id_user},
                {data.id_movement_type},
                {data.amount},
                '{data.description}'
            );
        '''
        self._changes_query(query)