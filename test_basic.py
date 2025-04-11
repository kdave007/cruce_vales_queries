import sys
from pathlib import Path

# Add the project root directory to Python path
project_root = str(Path(__file__).parent)
if project_root not in sys.path:
    sys.path.append(project_root)

from src.controllers.query_controller import QueryController
from src.services.db_service import DBConnection


def testDBconnection():
    try:
        db = DBConnection()
        with db.cursor() as cursor:
            cursor.execute("SELECT 1")
            result = cursor.fetchone()
            print("✓ Conexión a base de datos exitosa")
            return True
    except Exception as e:
        print(f"✗ Error de conexión a base de datos: {e}")
        return False

def test():
    qc = QueryController()
    
    # Test parameters for Query1
    test_params = {
        'date_range': {
            'start': '20250301',
            'end': '20250331'
        },
        'locations': ['BAJAC', 'GUADA']
    }
    
    results = qc.execute_query("query_test", test_params)

    if results is not None:
        print(f"✓ Query1 ejecutada exitosamente")
        print(f"  Registros encontrados: {len(results['data'])}")
        if len(results['data']) > 0:
          
            for element in results['data']:
                print(" ---------------------")
                for key, value in element.items():
                    print(f"  --  {key}: {value}")
                    
            # Print headers too
            print("\nHeaders:")
            for header in results['headers']:
                print(f"  - {header}")
                
        return True
    else:
        print("✗ Query1 no retornó resultados")
        return False


if __name__ == "__main__":
    print("\n1. Probando conexión a base de datos:")
    testDBconnection()
    test()