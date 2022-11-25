from ...customers.service import CustomersService
from ...customers.classes.customer import Customer

from ...products.service import Service
from ...products.classes.product import Product

from datetime import datetime
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

    def total(self) -> str:
        total = 0
        for product in self.products:
            total += product.total
        return str(total)

    def formatted_date(self) -> str:
        return datetime.fromtimestamp(self.date).strftime("%d/%m/%Y")