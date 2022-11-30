import sqlite3
from PySide6.QtCore import QObject, Signal

# Inherits from QObject to use Signals
class Service(QObject):
    data_changed = Signal()
    current_user_id: int = -1
    DB_PATH = "src/app/db/test.db"

    # Execute Queries
    def _changes_query(self, query: str) -> int:
        conn = sqlite3.connect(self.DB_PATH)
        
        cursor = conn.cursor()
        cursor.execute(query)
        row_id = cursor.fetchone()
        # print("row_id", row_id)

        conn.commit()
        conn.close()

        if row_id: return row_id[0]
        else: return -1

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
