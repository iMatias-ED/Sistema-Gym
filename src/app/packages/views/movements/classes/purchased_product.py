from ...products.classes.product import Product

class PurchasedProduct:
    id_sales: int
    quantity: int
    price: int
    period: str
    days_purchased: int
    total: int
    product: Product

    def __init__(self, data: dict):
        self.id_sales = data["id_sales"]
        self.quantity = data["quantity"]
        self.price = data["price"]
        self.period = data["period"]
        self.days_purchased = data["days_purchased"]
        self.total = data["total"]
        self.product = data["product"]
