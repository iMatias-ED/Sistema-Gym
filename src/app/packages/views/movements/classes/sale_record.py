from datetime import datetime
from .product_sold import ProductSold

class SaleRecord:
    id: int
    date: int
    id_customer: int
    items: list[ProductSold]

    def __init__(self, data: dict):
        self.items = []

        self.date = data["date"]
        self.id_customer = data["id_customer"]

        if "id" in data: self.id = data["id"]

    def save_product(self, product: ProductSold):
        self.items.append(product)

    def total(self) -> str:
        total = 0
        for product in self.items:
            total += product.total
        return str(total)

    def formatted_date(self) -> str:
        return datetime.fromtimestamp(self.date).strftime("%d/%m/%Y")