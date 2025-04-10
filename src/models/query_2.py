from src.services.db_service import DBConnection

class Query2:
    def __init__(self):
        self.query_name = "query_2"
        self.db = DBConnection()
    
    def get_required_params(self):
        """Return the parameters required for this query"""
        return {
            'date_range': 'Dictionary with start and end dates in YYYYMMDD format',
            'locations': 'List of location codes'
        }

    def validate_params(self, params):
        """
        Validate the parameters before executing the query
        Args:
            params (dict): Dictionary containing:
                - date_range (dict): with 'start' and 'end' dates
                - locations (list): list of location codes
        Returns:
            bool: True if parameters are valid
        """
        try:
            # Check required parameters
            if 'date_range' not in params or 'locations' not in params:
                print("Error: Se requieren los parámetros 'date_range' y 'locations'")
                return False

            date_range = params['date_range']
            locations = params['locations']

            # Check if date_range is a dictionary and has required keys
            if not isinstance(date_range, dict) or 'start' not in date_range or 'end' not in date_range:
                print("Error: dateRange debe ser un diccionario con claves 'start' y 'end'")
                return False

            # Check if dates are not empty and in correct format
            start_date = str(date_range['start'])
            end_date = str(date_range['end'])
            
            if not (start_date.isdigit() and end_date.isdigit() and len(start_date) == 8 and len(end_date) == 8):
                print("Error: las fechas deben estar en formato YYYYMMDD")
                return False

            # Validate date range
            if int(start_date) > int(end_date):
                print("Error: la fecha de inicio no puede ser posterior a la fecha de fin")
                return False

            # Check if locations is a non-empty list
            if not isinstance(locations, list) or not locations:
                print("Error: locations debe ser una lista no vacia")
                return False

            return True

        except Exception as e:
            print(f"Error validating parameters: {e}")
            return False
        
    def execute(self, params, limit):
        """
        execute query
        """
        date_range = params['date_range']
        locations = params['locations']

        try:
            with self.db.cursor() as cursor:
                query = """
                    SELECT 
                        CASE 
                            WHEN zona.rp_plaza = 'GCHAP' THEN 'GUADA' 
                            ELSE zona.rp_plaza 
                        END AS PLAZA,
                        v.ctienda AS TIENDA, 
                        v.cve_pro_cl AS TIENDA_DESTINO,
                        v.fecha AS FECHA_EMISION,
                        v.folio_ref AS FOLIO_VALE,
                        CASE 
                            WHEN v.estado = 'X' THEN 'C' 
                            ELSE 'A' 
                        END AS ESTADO,
                        COALESCE(v.desc_mov, ' ') AS DESCRIPCION,
                        SUM(pv.cantidad * pv.precio) AS MONTO_TOTAL,
                        COALESCE(ey.folio_alta, ' ') AS FOLIO_ALTA,
                        COALESCE(TO_CHAR(ey.fechacort::DATE, 'DD/MM/YYYY'), ' ') AS FECHA_CORTA
                    FROM 
                        vales v
                    JOIN zona 
                        ON v.cplaza = zona.plaza 
                        AND v.ctienda = zona.tienda
                    INNER JOIN parvales pv 
                        ON v.no_consec = pv.no_consec 
                        AND v.cplaza = pv.cplaza 
                        AND v.ctienda = pv.ctienda
                    LEFT JOIN (
                        SELECT ctienda, cve_pro_cl, SUBSTRING(desc_mov, 7, 6) AS NO_CONSEC, 
                            no_consec AS FOLIO_ALTA, afectado, estado, fechacort 
                        FROM eysienc
                    ) AS ey 
                        ON v.tienda = ey.cve_pro_cl 
                        AND v.folio_ref = ey.no_consec
                    WHERE 
                        v.fecha BETWEEN %s AND %s
                        AND v.tipo_movim = 'V-' 
                        AND v.cborrado <> '1' 
                        AND zona.rp_plaza IN ({})
                    GROUP BY 
                        zona.rp_plaza, v.ctienda, tienda_destino, fecha_emision, folio_vale, 
                        v.estado, descripcion, folio_alta, fechacort;
                """.format(','.join(['%s'] * len(locations)))
                
                params = [date_range['start'], date_range['end']] + locations
                cursor.execute(query, params)
                return cursor.fetchall()
                
        except Exception as e:
            print(f"Error executing query: {e}")
            raise
