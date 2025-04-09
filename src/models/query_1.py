from src.services.db_service import DBConnection

class Query1:
    def __init__(self):
        self.query_name = "Query 1"
        self.db = DBConnection()

    def validate_params(self, dateRange, locations, limit):
        """
        Validate the parameters before executing the query
        """
        # Add your validation logic here
        return True
        
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
                    v.ctienda AS TIENDA, 
                    v.cve_pro_cl AS TIENDA_DESTINO,
                    v.fecha AS FECHA_EMISION,
                    v.folio_ref AS FOLIO_VALE,
                    CASE 
                        WHEN v.estado = 'X' THEN 'C' 
                        ELSE 'A' 
                    END AS ESTADO,
                    v.tipo_movim AS TIPO,
                    COALESCE(v.desc_mov, ' ') AS DESCRIPCION,
                    pv.clave_art AS ARTICULO,
                    gr.descripcio AS PROD_DESC,
                    SUM(pv.cantidad) AS CANTIDAD,
                    SUM(pv.precio) AS PRECIO,
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
                LEFT JOIN (
                    SELECT clave, descripcio 
                    FROM grupos
                ) AS gr 
                    ON pv.clave_art = gr.clave
                WHERE 
                    v.fecha BETWEEN %s AND %s 
                    AND v.tipo_movim = 'V-' 
                    AND v.cborrado <> '1'
                    AND zona.rp_plaza IN ({})
                GROUP BY 
                    zona.rp_plaza, v.ctienda, tienda_destino, fecha_emision, folio_vale, 
                    v.estado, tipo, descripcion, articulo, prod_desc, folio_alta, fechacort;
                """.format(','.join(['%s'] * len(locations)))
                
                params = [dateRange['start'], dateRange['end']] + locations
                cursor.execute(query, params)
                return cursor.fetchall()
                
        except Exception as e:
            print(f"Error executing query: {e}")
            raise
