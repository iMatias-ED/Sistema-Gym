from datetime import datetime
from typing import List
from .product_sold import ProductSold

class SaleRecord:
    id: int
    date: str
    total: int
    id_customer: int
    items: List[ProductSold]

    def __init__(self, data: dict):
        self.items = []

        self.date = data["date"]
        self.id_customer = data["id_customer"]

        if "id" in data: self.id = data["id"]

    def save_product(self, product: ProductSold):
        self.items.append(product)
        self.update_total()

    def update_total(self) -> None:
        total = 0
        for product in self.items:
            total += product.total
        self.total = total