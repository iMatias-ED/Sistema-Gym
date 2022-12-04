from ...movements.classes.sale_record import SaleRecord
from ...customers.classes.customer import Customer

class CustomerSummary:
    customer: Customer
    purchases: list[SaleRecord]

    def __init__(self, customer: Customer, purchases: list[SaleRecord]):
        self.customer = customer
        self.purchases = purchases