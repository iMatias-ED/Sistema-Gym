from PySide6.QtWidgets import QFrame
from __feature__ import snake_case, true_property

class ContentView(QFrame):
    def __init__(self, bgcolor):
        super(ContentView, self).__init__()
        self.style_sheet = f"background: {bgcolor}"
