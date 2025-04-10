from src.services.db_service import DBConnection

class Query3:
    def __init__(self):
        self.query_name = "query_3"
        self.db = DBConnection()

    def validate_params(self, dateRange, locations, limit):
        """
        Validate the parameters before executing the query
        Args:
            dateRange (dict): Dictionary with 'start' and 'end' dates in YYYYMMDD format
            locations (list): List of location codes
            limit (int): Query limit (optional)
        Returns:
            bool: True if parameters are valid
        """
        try:
            # Check if dateRange is a dictionary and has required keys
            if not isinstance(dateRange, dict) or 'start' not in dateRange or 'end' not in dateRange:
                print("Error: dateRange debe ser un diccionario con claves 'start' y 'end'")
                return False

            # Check if dates are not empty and in correct format
            start_date = str(dateRange['start'])
            end_date = str(dateRange['end'])
            
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
        
    def execute(self, dateRange, locations, limit):
        """
        execute query
        """
        try:
            with self.db.cursor() as cursor:
                # Your SQL query here with parameters
                query = """
                    SELECT
                        CASE 
                            WHEN zona.rp_plaza = 'GCHAP' THEN 'GUADA' 
                            ELSE zona.rp_plaza 
                        END AS PLAZA,
                        e.fecha,
                        e.ctienda,
                        SUBSTRING(e.desc_mov, 7, 6) AS vale_cedis,
                        e.no_consec,
                        COALESCE(TO_CHAR(e.fechacort::DATE, 'DD/MM/YYYY'), ' ') AS FECHA_CORTA
                    FROM
                        eysienc e
                    JOIN zona 
                        ON e.cplaza = zona.plaza 
                        AND e.ctienda = zona.tienda
                    WHERE
                        e.fecha BETWEEN '20250301' AND '20250331'
                        AND e.cve_pro_cl IN ('GCEDI', 'ALMAC', 'ALMAR', 'B0001', 'VCEDV', 'PCEDI', 'MCEDI')
                        AND e.cborrado <> '1'
                        AND zona.rp_plaza IN ('BAJAC', 'GUADA', 'GUATE', 'HERMO', 'VALLA', 'NICAR', 'PENLA', 'REYES', 'MANZA', 'XALAP', 'TAPAC', 'CHETU')
                    GROUP BY
                        zona.rp_plaza, e.fecha, e.ctienda, vale_cedis, e.no_consec, fechacort
                    ORDER BY 
                        zona.rp_plaza, e.ctienda, vale_cedis;
                """.format(','.join(['%s'] * len(locations)))
                
                params = [dateRange['start'], dateRange['end']] + locations
                cursor.execute(query, params)
                return cursor.fetchall()
                
        except Exception as e:
            print(f"Error executing query: {e}")
            raise
