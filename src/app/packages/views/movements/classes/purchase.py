from ...customers.service import CustomersService
from ...customers.classes.customer import Customer

from ...products.service import Service
from ...products.classes.product import Product

from .purchased_product import PurchasedProduct

class Purchase:
    id: int
    date: int
    id_customer: int
    products: list[PurchasedProduct]

    def __init__(self, data: dict):
        self.products = []

        self.date = data["date"]
        self.id_customer = data["id_customer"]

        if "id" in data: self.id = data["id"]

    def save_product(self, product: PurchasedProduct):
        self.products.append(product)