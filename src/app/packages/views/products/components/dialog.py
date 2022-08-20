from PySide6.QtWidgets import *
from PySide6.QtCore import *
from __feature__ import snake_case, true_property

class Dialog(QDialog):
    root_layout = QGridLayout()

    def __init__(self, service):
        super(Dialog, self).__init__()
        self.minimum_width = 350 
        self.minimum_height = 250 

        self.service = service
        self.setup_ui()

    def setup_ui(self):
        self.title = QLabel("Creá un producto", alignment=Qt.AlignCenter, object_name="dialog-title")
        self.title.style_sheet = "background: blue;"
        self.root_layout.add_widget(self.title, 1, 1, 1, 2)

        self.inp_code = self._create_input("Código", "Código del producto", self.row())
        self.inp_name = self._create_input("Nombre", "Nombre del producto", self.row())
        
        self.submit = QPushButton("Submit")
        self.submit.clicked.connect(self.on_create_submit)
        self.root_layout.add_widget(self.submit, self.row(), 1, self.row(), 2)

        self.set_layout(self.root_layout)

    def row(self):
        return self.root_layout.row_count()

    def _create_input(self, title:str, placeholder:str, row:int):
        label = QLabel(title)
        line_edit = QLineEdit(placeholder_text=placeholder)

        self.root_layout.add_widget(label, row, 1)
        self.root_layout.add_widget(line_edit, row, 2)

        return line_edit

    def example(self, mode:str):
        print(f"dialog in mode {mode}")
        self.show()

    def create(self):
        print("create mode")
        self.show()

    def on_create_submit(self):
        self.service.create( self.inp_code.text, self.inp_name.text )

    @Slot(int)
    def edit(self, row:int):
        print(f"Editing row {row}")
        self.show()