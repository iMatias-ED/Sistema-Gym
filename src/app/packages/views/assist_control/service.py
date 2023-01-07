
# Services
from ...shared.services.service import DBService
from ..products.service import ProductsService
from ..customers.service import CustomersService
from ..movements.service import MovementsService

# Classes

from ..customers.classes.customer import Customer
from ..products.classes.product import Product
from .classes.customer_summary import CustomerSummary

class AssistControlService(DBService):
    products_service = ProductsService()
    customers_service = CustomersService()
    movements_service = MovementsService()

    def get_info(self, ci: int) -> CustomerSummary:
        customer = self.customers_service.get_by_ci_number(ci)
        purchases = self.movements_service.get_purchases_by_customer_id(customer.id)

        return CustomerSummary(customer, purchases)

    def get_product_by_id(self, id: int) -> Product:
        return self.products_service.get_by_id(id)

    def get_purchases(self, customer_id, limit_date: str):
        return self.movements_service.get_customers_purchases_until(customer_id, limit_date)

    def register_assistance(self, customer: Customer):
        query = f'''
            INSERT INTO assistance_record(id_customer)
            VALUES ({customer.id});
        '''
        self._changes_query(query)