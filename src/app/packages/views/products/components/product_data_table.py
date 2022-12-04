from typing import List

from ..service import ProductsService
from ....shared.components.data_table import DataTable, TableItem, Action

class ProductDataTable(DataTable):

    def __init__(self, service: ProductsService):
        super(ProductDataTable, self).__init__()
        self.products_service = service
        self.products_service.data_changed.connect( self.refresh )

        self.setup_table(self.products_service.header_labels)
        self.load_data()
        
    def load_data(self) -> None:
        self.products = self.products_service.get_all()
        items: list[ list[TableItem] ] = []

        for product in self.products:
            actions: List[Action] = [
                Action(column=0, label="X", slot=self.delete_clicked, params=product.id),
                Action(column=1, label="E", slot=self.edit_clicked, params=product.id)
            ]            

            row: list[TableItem] = [
                TableItem( column=2, value=product.code ),
                TableItem( column=3, value=product.name ),
                TableItem( column=4, value=product.get_price_by_name("Pago Diario").price ),
                TableItem( column=5, value=product.get_price_by_name("Pago Semanal").price ),
                TableItem( column=6, value=product.get_price_by_name("Pago Mensual").price ),
                TableItem( column=7, value=product.get_price_by_name("Pago Trimestral").price ),
                TableItem( column=8, value=product.get_price_by_name("Pago Semestral").price ),
            ]
            items.append( row + actions )  

        self.insert_items( items )

    def edit_clicked(self, product_id:int) -> None:
        self.edit.emit(product_id)
    
    def delete_clicked(self, product_id:int) -> None:
        self.delete.emit(product_id)
        self.products_service.delete(product_id)