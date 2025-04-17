# src/services/db_service.py
import psycopg2
from psycopg2.extras import RealDictCursor
from psycopg2.pool import SimpleConnectionPool
from os import getenv
from dotenv import load_dotenv
import threading
from contextlib import contextmanager

class TimeoutError(Exception):
    pass

@contextmanager
def timeout(seconds):
    timer = threading.Timer(seconds, lambda: (_ for _ in ()).throw(TimeoutError("La conexión a la base de datos tardó demasiado tiempo")))
    timer.start()
    try:
        yield
    finally:
        timer.cancel()

class DBConnection:
    _instance = None
    _pool = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DBConnection, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if self._pool is None:
            self._create_pool()

    def _create_pool(self):
        """Initialize connection pool"""
        load_dotenv('config/credentials.secure.env')
        
        try:
            with timeout(10):  # 10 second timeout for connection
                self._pool = SimpleConnectionPool(
                    minconn=1,
                    maxconn=10,  # Adjust this based on your needs
                    host=getenv('DB_HOST'),
                    user=getenv('DB_USER'),
                    password=getenv('DB_PASSWORD'),
                    port=int(getenv('DB_PORT')),  # Convert port to integer
                    dbname=getenv('DB_NAME'),  # Match the correct env variable name
                    # Add connection timeouts
                    connect_timeout=5,
                    options='-c statement_timeout=30000'  # 30 second query timeout
                )
        except TimeoutError as e:
            print("✗ Error: Tiempo de espera agotado al conectar a la base de datos")
            print("  Por favor, verifique su conexión y las credenciales")
            raise
        except Exception as e:
            print(f"✗ Error al conectar a la base de datos: {str(e)}")
            print("  Por favor, verifique su conexión y las credenciales")
            raise

    def get_connection(self):
        """Get a connection from the pool"""
        if not self._pool:
            self._create_pool()
        try:
            with timeout(5):  # 5 second timeout for getting connection
                return self._pool.getconn()
        except TimeoutError:
            print("✗ Error: Tiempo de espera agotado al obtener conexión del pool")
            print("  La base de datos está sobrecargada o no responde")
            raise
        except Exception as e:
            print(f"✗ Error al obtener conexión: {str(e)}")
            raise

    def return_connection(self, conn):
        """Return a connection to the pool"""
        try:
            self._pool.putconn(conn)
        except Exception as e:
            print(f"✗ Error al devolver conexión al pool: {str(e)}")
            raise

    def cursor(self):
        """Get a cursor with connection context management"""
        return PoolCursor(self)

class PoolCursor:
    def __init__(self, db):
        self.db = db
        self.conn = None
        self.cur = None

    def __enter__(self):
        try:
            self.conn = self.db.get_connection()
            self.cur = self.conn.cursor(cursor_factory=RealDictCursor)
            return self.cur
        except Exception as e:
            if self.conn:
                self.db.return_connection(self.conn)
            raise

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            if isinstance(exc_val, psycopg2.Error):
                print(f"✗ Error en la base de datos: {str(exc_val)}")
            self.conn.rollback()
        else:
            self.conn.commit()
        
        if self.cur:
            self.cur.close()
        if self.conn:
            self.db.return_connection(self.conn)