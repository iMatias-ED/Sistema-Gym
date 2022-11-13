import sqlite3
from PySide6.QtCore import QObject, Signal

# Inherits from QObject to use Signals
class Service(QObject):
    data_changed = Signal()
    DB_PATH = "src/app/db/test.db"

    # Execute Queries
    def _changes_query(self, query: str):
        conn = sqlite3.connect(self.DB_PATH)
        
        cursor = conn.cursor()
        cursor.execute(query)

        conn.commit()
        conn.close()

    def _read_query_fetchall(self, query: str):
        conn = sqlite3.connect(self.DB_PATH)
        conn.row_factory = sqlite3.Row

        cursor = conn.cursor()
        cursor.execute(query)
        result = cursor.fetchall()
        
        conn.close()
        return result

    def _read_query_fetchone(self, query: str):
        conn = sqlite3.connect(self.DB_PATH)
        conn.row_factory = sqlite3.Row
        
        cursor = conn.cursor()
        data = cursor.execute(query)
        result = data.fetchone()

        conn.close()
        return dict(result)
