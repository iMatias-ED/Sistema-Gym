from ...products.classes.price import Price
from ...products.classes.product import Product

class Selection:
    total: str
    price: Price
    quantity: str
    product: Product

    def __init__(self, product: Product, price: Price, quantity: str, total: int):
        self.price = price
        self.total = total
        self.product = product
        self.quantity = quantity