import sqlite3

class ProductsService:
    header_labels = ["Eliminar", "Editar", "Código", "Nombre", "Descripción"]

    def _execute_query(self, query):
        conn = sqlite3.connect("src/app/db/test.db")
        
        cursor = conn.cursor()
        cursor.execute(query)

        conn.commit()
        conn.close()

    def create(self, code, name):
        query = f'''
            INSERT INTO products (code, name)
                VALUES ('{code}', '{name}');
        '''
        self._execute_query(query)
