from PySide6.QtWidgets import QWidget 
from __feature__ import snake_case, true_property

# Components
from ....shared.components.summary_dialog import SummaryDialog
# Classes
from ...movements.classes.sale_record import SaleRecord
from ....shared.components.data_table import SubValue 
from ....shared.classes.summary_content import SummaryContent
from ....shared.classes.table_header_label import TableHeaderLabel

class PurchaseDetailDialog(SummaryDialog):
    def __init__(self, parent: QWidget):
        super(PurchaseDetailDialog, self).__init__(parent)

        self.setup_ui( SummaryContent(
            "Fecha de compra",
            "xx/xx/xxxx",
            [   
                TableHeaderLabel("name", "Producto"),
                TableHeaderLabel("quantity", "Cantidad"),
                TableHeaderLabel("period", "Periodo"),
                TableHeaderLabel("price", "Precio Unitario"),
                TableHeaderLabel("total", "Total"),
            ],
            "X Registros encontrados"
        ))

    def show(self, data: SaleRecord):
        self.second_title.text = data.formatted_date
        self.bottom_label.text = f"Gs. {data.total}"
        self.load_data(data)
        
        super().show()

    def load_data(self, data:SaleRecord):        
        sub_values = { "product": [SubValue("name", "name", False)] }
        self.table.test_insert(
            data=data.items,
            sub_values=sub_values    
        )

