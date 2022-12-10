from PySide6.QtWidgets import QDialog, QLabel, QVBoxLayout, QHBoxLayout, QWidget
from __feature__ import snake_case, true_property

from typing import List

from ...shared.classes.table_header_label import TableHeaderLabel
from ..classes.summary_content import SummaryContent
from .data_table import DataTable
class SummaryDialog(QDialog):

    def setup_ui(self, content: SummaryContent):
        # Title section
        self.title = QLabel(content.title)
        self.second_title = QLabel(content.second_title)

        title_layout = QHBoxLayout()
        title_layout.add_widget(self.title)
        title_layout.add_widget(self.second_title)

        # Table section
        self.table = self.create_table(content.table_headers)

        # Total section
        self.bottom_label = QLabel(content.bottom_label)

        # Add widgets to layout
        layout = QVBoxLayout()
        layout.add_layout(title_layout)
        layout.add_widget(self.table)
        layout.add_widget(self.bottom_label)

        self.set_layout(layout)

    def create_table(self, header_labels: List[TableHeaderLabel]):
        table = DataTable()
        table.setup_table(header_labels)
        return table