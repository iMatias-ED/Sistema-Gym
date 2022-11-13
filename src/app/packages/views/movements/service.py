from typing import List

# Services
from ...shared.service import Service
from ..products.service import ProductsService
from ..customers.service import CustomersService

# Classes
from ..products.classes.product import Product
from ..customers.classes.customer import Customer

class MovementsService(Service):
    products_service = ProductsService()
    customers_service = CustomersService()

    header_labels = ["Eliminar", "Producto", "Cantidad", "Periodo", "Precio", "Total"]

    def search_users(self, name: str) -> List[Customer]:
        return self.customers_service.search(name)
    
    def search_products(self, name: str) -> List[Product]:
        return self.products_service.search(name)
    
