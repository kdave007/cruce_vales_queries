import sys
import os

# Add the project root to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.controllers.query_controller import QueryController
from src.services.excel_service import ExcelService
from src.services.db_service import DBConnection

def test_db_connection():
    """Test database connection"""
    try:
        db = DBConnection()
        with db.cursor() as cursor:
            cursor.execute("SELECT 1")
            print("✓ Conexión a base de datos exitosa")
            return True
    except Exception as e:
        print(f"✗ Error de conexión a base de datos: {e}")
        return False

def test_excel_generation():
    # First test DB connection
    if not test_db_connection():
        print("✗ No se puede continuar sin conexión a base de datos")
        return False

    # Initialize controller
    qc = QueryController()
    
    # Test parameters for Query
    test_params = {
        'date_range': {
            'start': '20250301',
            'end': '20250331'
        },
        'locations': ['BAJAC', 'GUADA']
    }
    
    print("\nEjecutando query...")
    # Execute query
    results = qc.execute_query("query_test", test_params)

    if results is not None and len(results) > 0:
        print(f"✓ Query ejecutada exitosamente, generando Excel...")
        print(f"  Registros encontrados: {len(results)}")
        
        # Create Excel service
        excel = ExcelService("query_results.xlsx")

        # Create a new sheet
        sheet = excel.create_sheet("Query Test")

        # Get headers from results
        headers = list(results[0].keys())

        # Write headers and data
        excel.write_headers(sheet, headers)
        excel.write_data(sheet, results)

        # Save the file
        excel.save()
        print("✓ Archivo Excel generado exitosamente: query_results.xlsx")
        return True
    else:
        print("✗ La query no retornó resultados")
        return False

if __name__ == "__main__":
    test_excel_generation()