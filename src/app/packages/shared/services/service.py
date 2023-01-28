import sqlite3
from PySide6.QtCore import QObject, Signal
from typing import Union, List
from ..classes.table_header_label import TableHeaderLabel

# Inherits from QObject to use Signals
class DBService(QObject):
    data_changed = Signal()
    DB_PATH = "src/app/db/test.db"

    connection: sqlite3.Connection

    def __init__(self):
        super(DBService, self).__init__()

    def _open_connection(self) -> sqlite3.Cursor:
        self.connection = sqlite3.connect(self.DB_PATH)
        self.connection.row_factory = sqlite3.Row
        
        return self.connection.cursor()

    # Execute Queries
    def _changes_query(self, query: str) -> Union[int, None]:
        conn = sqlite3.connect(self.DB_PATH)
        cursor = conn.cursor()
        
        try:
            cursor.execute(query)
            row_id = cursor.fetchone()
            conn.commit()
        finally:
            conn.close()
        if row_id: return row_id[0]

    def _read_query_fetchall(self, query: str):
        cursor = self._open_connection()
        cursor.execute(query)
        result = cursor.fetchall()
        
        self.connection.close()
        return result

    def _read_query_fetchone(self, query: str):
        cursor = self._open_connection()
        
        data = cursor.execute(query)
        result = data.fetchone()

        self.connection.close()
        return dict(result)

    def values_separator(self, arr: List, element):
            if arr.index(element) == len(arr)-1: return ";" 
            else: return ",\n" 
