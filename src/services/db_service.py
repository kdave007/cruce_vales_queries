# src/services/db_service.py
import psycopg2
from psycopg2.extras import RealDictCursor
from psycopg2.pool import SimpleConnectionPool
from os import getenv
from dotenv import load_dotenv

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
        
        self._pool = SimpleConnectionPool(
            minconn=1,
            maxconn=10,  # Adjust this based on your needs
            host=getenv('DB_HOST'),
            user=getenv('DB_USER'),
            password=getenv('DB_PASSWORD'),
            port=getenv('DB_PORT'),
            dbname=getenv('DB_NAME')
        )

    def get_connection(self):
        """Get a connection from the pool"""
        if not self._pool:
            self._create_pool()
        return self._pool.getconn()

    def return_connection(self, conn):
        """Return a connection to the pool"""
        self._pool.putconn(conn)

    def cursor(self):
        """Get a cursor with connection context management"""
        return PoolCursor(self)

class PoolCursor:
    def __init__(self, db):
        self.db = db
        self.conn = None
        self.cur = None

    def __enter__(self):
        self.conn = self.db.get_connection()
        self.cur = self.conn.cursor(cursor_factory=RealDictCursor)
        return self.cur

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            self.conn.rollback()
        else:
            self.conn.commit()
        
        self.cur.close()
        self.db.return_connection(self.conn)