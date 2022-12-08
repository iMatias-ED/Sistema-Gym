from datetime import datetime
from .product_sold import ProductSold

class SaleRecord:
    id: int
    date: int
    total: int
    id_customer: int
    formatted_date: str
    items: list[ProductSold]

    def __init__(self, data: dict):
        self.items = []

        self.date = data["date"]
        self.id_customer = data["id_customer"]

        if "id" in data: self.id = data["id"]
        self.formatted_date = datetime.fromtimestamp(self.date).strftime("%d/%m/%Y")

    def save_product(self, product: ProductSold):
        self.items.append(product)
        self.update_total()

    def update_total(self) -> None:
        total = 0
        for product in self.items:
            total += product.total
        self.total = total