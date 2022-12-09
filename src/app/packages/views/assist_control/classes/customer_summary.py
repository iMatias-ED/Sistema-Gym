from ...movements.classes.sale_record import SaleRecord
from ...customers.classes.customer import Customer

from typing import List

class CustomerSummary:
    customer: Customer
    purchases: List[SaleRecord]

    def __init__(self, customer: Customer, purchases: List[SaleRecord]):
        self.customer = customer
        self.purchases = purchases