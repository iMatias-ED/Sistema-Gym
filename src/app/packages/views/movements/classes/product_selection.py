from ...products.classes.price import Price
from ...products.classes.product import Product

class ProductSelection:
    total: int
    price: Price
    quantity: int
    product: Product

    def __init__(self, product: Product, price: Price, quantity: int, total: int):
        self.price = price
        self.total = total
        self.product = product
        self.quantity = quantity

    def add(self, quantity: int) -> None:
        self.quantity += quantity
        self.total = self.price.price * self.quantity

    def __str__(self):
        return f'''{self.product.name}:{self.price.name} - {self.quantity} -> {self.total}'''
    