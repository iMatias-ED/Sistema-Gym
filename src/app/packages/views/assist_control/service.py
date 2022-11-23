
# Services
from ...shared.service import Service
from ..products.service import ProductsService
from ..customers.service import CustomersService
from ..movements.service import MovementsService

# Classes
from .classes.customer_summary import CustomerSummary
from ..movements.classes.product_selection import ProductSelection

class AssistControlService(Service):
    products_service = ProductsService()
    customers_service = CustomersService()
    movements_service = MovementsService()

    summary: CustomerSummary

    def get_info(self, ci: int):
        customer = self.customers_service.get_by_ci_number(ci)
        purchases = self.movements_service.get_purchases_by_customer_id(customer.id)

        print()
        for purchase in purchases: 
            print("- fecha", purchase.date)
            print("- products", purchase.products)
            print("\n#############\n")

