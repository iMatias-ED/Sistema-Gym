from PySide6.QtWidgets import *
from PySide6.QtCore import *
from __feature__ import snake_case, true_property

from .service import *

class Sidebar(QFrame):
    filter_event = Signal(int, bool)
    service = CustomersService()
    layout = QVBoxLayout()
    
    def __init__(self):
        super(Sidebar, self).__init__()
        self.setup_ui()

    def setup_ui(self):
        self.style_sheet = "background: darkgreen;"

        for index, label in enumerate(self.service.header_labels):
            self.create_checkbox(label, index)
        
        self.layout.add_stretch()
        self.set_layout(self.layout)

    def create_checkbox(self, label:str, index: int):
        checkbox = QCheckBox(label)
        checkbox.stateChanged.connect( lambda: self.__on_filter(index, checkbox.checked) )
        self.layout.add_widget(checkbox)
        
    def __on_filter(self, index: int, state: bool):
        self.filter_event.emit(index, state)
