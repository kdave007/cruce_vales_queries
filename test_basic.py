from src.controllers.query_controller import QueryController
from src.services.db_service import DBConnection


def testDBconnection():
    try:
        db = DBConnection()
        with db.cursor() as cursor:  # Fix: cursor is a method, not a property
            cursor.execute("SELECT 1")
            result = cursor.fetchone()
            print("✓ Conexión a base de datos exitosa")
            return True
    except Exception as e:
        print(f"✗ Error de conexión a base de datos: {e}")
        return False

def test():
    testDBconnection()
    qc = QueryController()
    # qc.execute_query("query_2",None)

if __name__ == "__main__":
    print("\n1. Probando conexión a base de datos:")
    testDBconnection()