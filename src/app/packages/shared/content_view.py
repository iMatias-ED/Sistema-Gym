from PySide6.QtWidgets import QFrame
from __feature__ import snake_case, true_property
import pathlib

class ContentView(QFrame):
    def __init__(self):
        super(ContentView, self).__init__()
        self.setup_ui()

    def set_styles(self, path: str):
        parent_directory = pathlib.Path(path).parent.resolve()
        file = open( f"{parent_directory}/styles.css", "r" )
        self.style_sheet = file.read()
        file.close()

    def setup_ui(self):
        # code should go here
        pass
