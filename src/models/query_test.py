from src.services.db_service import DBConnection

class Query_Test:
    def __init__(self):
        self.query_name = "query_test"
        self.db = DBConnection()
        
    def execute(self,params):
        """
        execute query
        """
        try:
            with self.db.cursor() as cursor:
                query = """
                SELECT 
                    v.ctienda AS TIENDA, 
                    v.cve_pro_cl AS TIENDA_DESTINO,
                    v.fecha AS FECHA_EMISION,
                    v.folio_ref AS FOLIO_VALE
                FROM
                    vales v
                LIMIT 10
                """
                cursor.execute(query)
                return cursor.fetchall()
                
        except Exception as e:
            print(f"Error executing query: {e}")
            raise
