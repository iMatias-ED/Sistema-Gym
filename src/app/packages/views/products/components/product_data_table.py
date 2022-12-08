from typing import List

from ..service import ProductsService
from ....shared.components.data_table import SubValue, DevAction, DataTable, TableItem, Action



class ProductDataTable(DataTable):

    def __init__(self, service: ProductsService):
        super(ProductDataTable, self).__init__()
        self.products_service = service
        self.products_service.data_changed.connect( self.refresh )

        # self.setup_table(self.products_service.header_labels)
        self.setup_dev(self.products_service.header_labels_2)
        self.load_data()
        
    def load_data(self) -> None:
        self.products = self.products_service.get_all()
        sub_values = { "prices": [SubValue("name", "price", True)] }
        actions = [
            DevAction(0, "X", self.delete_clicked, True, "id"),
            DevAction(1, "E", self.edit_clicked, True, "id"),
        ]

        self.test_insert(self.products, actions, sub_values)

    def edit_clicked(self, product_id:int) -> None:
        self.edit.emit(product_id)
    
    def delete_clicked(self, product_id:int) -> None:
        self.delete.emit(product_id)
        self.products_service.delete(product_id)