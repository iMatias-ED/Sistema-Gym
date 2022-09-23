from PySide6.QtWidgets import *
from PySide6.QtCore import *
from __feature__ import snake_case, true_property

class Sidebar(QFrame):
    filter_event = Signal(int, bool)
    root_layout = QVBoxLayout()
    checkbox_layout = QVBoxLayout()

    def __init__(self, service):
        super(Sidebar, self).__init__(object_name="sidebar")
        self.service = service
        self.setup_ui()

    def setup_ui(self) -> None:
        for index, label in enumerate(self.service.header_labels):
            self.create_checkbox(label, index)
        self.checkbox_layout.add_stretch()

        self.title = QLabel('Ocultar Columnas', object_name="view-title", alignment=Qt.AlignCenter)
        self.root_layout.add_widget(self.title, 10)
        self.root_layout.add_layout(self.checkbox_layout, 90)
        
        self.set_layout(self.root_layout)

    def create_checkbox(self, label:str, index: int) -> None:
        checkbox = QCheckBox(label)
        checkbox.stateChanged.connect( lambda: self.__on_filter(index, checkbox.checked) )
        self.checkbox_layout.add_widget(checkbox)
        
    def __on_filter(self, index: int, state: bool) -> None:
        self.filter_event.emit(index, state)
