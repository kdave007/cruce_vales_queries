from src.services.db_service import DBConnection

class Query_Test:
    def __init__(self):
        self.query_name = "query_test"
        self.db = DBConnection()

    def validate_params(self, params):
        return True    
        
    def execute(self,params):
        """
        execute query
        """
        date_range = params['date_range']
        locations = params['locations']

        try:
            with self.db.cursor() as cursor:
                query = """
                SELECT 
                    v.ctienda AS TIENDA, 
                    v.cve_pro_cl AS TIENDA_DESTINO,
                    v.fecha AS FECHA_EMISION,
                    v.folio_ref AS FOLIO_VALE,
                    v.cplaza,
                    v.fecha
                FROM
                    vales v
                JOIN zona 
                    ON v.cplaza = zona.plaza     
                WHERE
                    v.fecha BETWEEN %s AND %s
                    AND zona.rp_plaza IN ({})    
                LIMIT 10
                """.format(','.join(['%s'] * len(locations)))
                
                params = [date_range['start'], date_range['end']] + locations
                cursor.execute(query, params)
                return cursor.fetchall()
                
        except Exception as e:
            print(f"Error executing query: {e}")
            raise

    def fetch_headers(self, data):
        """
        execute query
        """            
        if data is not None:
            
            if len(data) > 0:
                headers = list(data[0].keys())
            return headers
        else:
            print("✗ Error fetching headers")
            return False    
