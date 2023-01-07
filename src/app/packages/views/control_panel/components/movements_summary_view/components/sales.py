from PySide6.QtWidgets import QVBoxLayout, QFrame, QLabel, QDateTimeEdit
from PySide6.QtCore import QDate, QLocale, Signal
from __feature__ import snake_case, true_property

class SalesSummary(QFrame):
    date_changed = Signal(None)
    root_layout = QVBoxLayout()

    def __init__(self):
        super(SalesSummary, self).__init__()
        self.date_picker = self._create_date_picker()
        self.date_picker.maximum_date = QDate.current_date()
        self.date_picker.maximum_width = 350;

        self.date_picker.dateChanged.connect(self.on_date_changed)        

        self.title = QLabel("Ventas")
        self.amount = QLabel("Gs Total")

        self.root_layout.add_widget(self.date_picker)
        self.root_layout.add_stretch()
        self.root_layout.add_widget(self.title)
        self.root_layout.add_stretch()
        self.root_layout.add_widget(self.amount)
        self.root_layout.add_spacing(50)

        self.set_layout(self.root_layout)

    def on_date_changed(self):
        self.date_changed.emit()

    def _create_date_picker(self, obj_name:str = "") -> QDateTimeEdit:
        dateEdit = QDateTimeEdit( QDate.current_date(), locale = QLocale.Spanish, display_format = "dd/MM/yyyy", object_name=obj_name)
        dateEdit.calendar_popup = True
        return dateEdit

    def refresh(self, data: dict):
        self.amount.text = f'Gs. {data["total"]}'