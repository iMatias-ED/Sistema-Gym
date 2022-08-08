from PySide6.QtWidgets import QFrame, QStackedLayout
from __feature__ import snake_case, true_property

class ContentBox(QFrame):
    __content_layout = QStackedLayout()
    
    def __init__(self):
        super(ContentBox, self).__init__()
        self.set_layout(self.__content_layout)
        self.style_sheet = "background: gray"

    def add_content(self, widget: QFrame, index: int) -> int:
        return self.__content_layout.insert_widget(index, widget)

    def show_index(self, index:int ) -> None:
        self.__content_layout.current_index = index