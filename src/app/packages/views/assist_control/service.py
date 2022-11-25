
# Services
from ...shared.service import Service
from ..products.service import ProductsService
from ..customers.service import CustomersService
from ..movements.service import MovementsService

# Classes
from .classes.customer_summary import CustomerSummary
from ..products.classes.product import Product
from ..movements.classes.product_selection import ProductSelection

class AssistControlService(Service):
    products_service = ProductsService()
    customers_service = CustomersService()
    movements_service = MovementsService()

    def get_info(self, ci: int) -> CustomerSummary:
        customer = self.customers_service.get_by_ci_number(ci)
        purchases = self.movements_service.get_purchases_by_customer_id(customer.id)

        return CustomerSummary(customer, purchases)

    def get_product_by_id(self, id: int) -> Product:
        return self.products_service.get_by_id(id)

