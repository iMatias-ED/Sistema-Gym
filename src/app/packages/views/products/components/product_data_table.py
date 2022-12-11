from ..service import ProductsService
from ....shared.components.data_table import SubValue, Action, DataTable
from ....shared.components.confirmation_message import ConfirmationMessage, ConfirmationDialog
class ProductDataTable(DataTable):

    def __init__(self, service: ProductsService):
        super(ProductDataTable, self).__init__()
        self.products_service = service
        self.products_service.data_changed.connect( self.refresh )

        self.setup_table(self.products_service.header_labels)
        self.load_data()
        
    def load_data(self) -> None:
        self.products = self.products_service.get_all()
        sub_values = { "prices": [SubValue("name", "price", True)] }
        actions = [
            Action(0, "X", self.delete_clicked, True, "name", "id"),
            Action(1, "E", self.edit_clicked, True, "id"),
        ]

        self.insert_values(self.products, actions, sub_values)

    def edit_clicked(self, product_id:int) -> None:
        self.edit.emit(product_id)
    
    def delete_clicked(self, product_name:str, product_id:int) -> None:
        ConfirmationDialog(self, lambda: self.delete(product_id)).show(ConfirmationMessage(
            "¿Está seguro?",
            f'''Se eliminará el producto "{product_name}" y toda la información asociada (registros de ventas y tiempo de acceso de los clientes )''',
            "Esta acción no se puede deshacer."
        ))

    def delete(self, product_id: int):
        self.delete.emit(product_id)
        self.products_service.delete(product_id)