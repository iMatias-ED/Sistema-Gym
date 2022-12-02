from PySide6.QtWidgets import *
from PySide6.QtCore import *
from __feature__ import snake_case, true_property

from ...shared.content_view import ContentView

# Service
from .service import ControlPanelService

# Componentes
from .components.sidebar import Sidebar
from .components.users_view import UsersView
from .components.summary_view.summary_view import SummaryView

class ControlPanel(ContentView):
    service = ControlPanelService()
    root_layout = QHBoxLayout()
    content_layout = QStackedLayout()

    def setup_ui(self) -> None:
        self.set_styles(__file__)
        self.sidebar = Sidebar(self.service)
        
        self.users_view = UsersView() 
        self.summary_view = SummaryView()

        scrollArea = QScrollArea(self, widget_resizable=True)
        scrollArea.set_widget(self.summary_view)

        self.root_layout.add_widget(self.sidebar, 20)
        self.root_layout.add_layout(self.content_layout, 80)

        self.content_layout.insert_widget(0, self.users_view)
        self.content_layout.insert_widget(1, scrollArea)

        self.set_layout(self.root_layout)
        self.__events_manager()

    def __events_manager(self) -> None:
        self.sidebar.view_change_event.connect(self.on_view_change)
        self.sidebar.view_change_event.connect(self.summary_view.on_show)

    @Slot(int)
    def on_view_change(self, index: int):
        self.content_layout.set_current_index(index)
    


    

