from typing import List

# Service
from ..service import CustomersService

# Components | Classes
from ....shared.components.data_table import DataTable, TableItem, Action

class CustomersDataTable(DataTable):
    def __init__(self, service: CustomersService):
        super(CustomersDataTable, self).__init__()
        self.customers_service = service
        self.customers_service.data_changed.connect( self.refresh )

        self.setup_table( self.customers_service.header_labels )
        self.load_data()
        
    def load_data(self) -> None:
        self.customers = self.customers_service.get_all()
        items: list[ list[TableItem] ] = []

        for customer in self.customers:
            actions: List[Action] = [
                Action(column=0, label="X", slot=self.delete_clicked, params=customer.id),
                Action(column=1, label="E", slot=self.edit_clicked, params=customer.id)
            ]            

            row: list[TableItem] = [
                TableItem( column=2, value=customer.full_name ),
                TableItem( column=3, value=customer.ci ),
                TableItem( column=4, value=customer.ruc ),
                TableItem( column=5, value=customer.invoice_to ),
                TableItem( column=6, value=customer.phone ),
                TableItem( column=7, value=customer.email ),
                TableItem( column=8, value=customer.genre ),
            ]
            items.append( row + actions )  

        self.insert_items( items )

    def edit_clicked(self, customer_id:int) -> None:
        self.edit.emit(customer_id)
    
    def delete_clicked(self, customer_id:int) -> None:
        self.delete.emit(customer_id)
        self.customers_service.delete(customer_id)