from ...movements.classes.purchase import Purchase
from ...customers.classes.customer import Customer

class CustomerSummary:
    customer: Customer
    purchases: list[Purchase]

    def __init__(self, customer: Customer, purchases: list[Purchase]):
        self.customer = customer
        self.purchases = purchases