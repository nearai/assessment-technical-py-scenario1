# Database connection and queries
import os
import time
import psycopg2
from psycopg2.pool import SimpleConnectionPool
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Create a connection pool
# First check if DATABASE_URL is provided
database_url = os.getenv('DATABASE_URL')
if database_url:
    # Use the connection string directly
    pool = SimpleConnectionPool(
        minconn=1,
        maxconn=10,
        dsn=database_url
    )
else:
    # Fall back to individual parameters
    pool = SimpleConnectionPool(
        minconn=1,
        maxconn=10,
        user=os.getenv('DB_USER', 'postgres'),
        host=os.getenv('DB_HOST', 'localhost'),
        database=os.getenv('DB_NAME', 'postgres'),
        password=os.getenv('DB_PASSWORD', 'postgres'),
        port=int(os.getenv('DB_PORT', '5432'))
    )

# Test the connection
try:
    conn = pool.getconn()
    cursor = conn.cursor()
    cursor.execute('SELECT NOW()')
    cursor.close()
    pool.putconn(conn)
    print("Database connected successfully")
except Exception as e:
    print(f"Database connection error: {e}")

def query(text, params=None):
    """
    Executes a database query with parameters

    Args:
        text: The SQL query text
        params: The query parameters

    Returns:
        The query result
    """
    try:
        start = time.time()
        conn = pool.getconn()
        cursor = conn.cursor()
        cursor.execute(text, params)

        # Check if the query returns results
        if cursor.description:
            result = cursor.fetchall()
            column_names = [desc[0] for desc in cursor.description]
        else:
            result = []
            column_names = []

        conn.commit()
        cursor.close()
        pool.putconn(conn)

        duration = (time.time() - start) * 1000  # Convert to milliseconds
        print(f"Executed query {text}, duration: {duration}ms, rows: {len(result)}")

        # Create a result object similar to the TypeScript version
        class QueryResult:
            def __init__(self, rows, column_names):
                self.rows = rows
                self.column_names = column_names
                self.rowCount = len(rows)

        # Convert result to a list of dictionaries
        rows = []
        for row in result:
            row_dict = {}
            for i, col_name in enumerate(column_names):
                row_dict[col_name] = row[i]
            rows.append(row_dict)

        return QueryResult(rows, column_names)
    except Exception as e:
        print(f"Error executing query: {e}")
        raise e

def get_client():
    """
    Gets a client from the pool for transactions

    Returns:
        A client from the pool
    """
    class PoolClient:
        def __init__(self, conn):
            self.conn = conn
            self.cursor = conn.cursor()
            self.last_query = None

        def query(self, *args):
            self.last_query = args[0]
            self.cursor.execute(*args)
            if self.cursor.description:
                result = self.cursor.fetchall()
                column_names = [desc[0] for desc in self.cursor.description]
            else:
                result = []
                column_names = []

            # Create a result object similar to the TypeScript version
            class QueryResult:
                def __init__(self, rows, column_names):
                    self.rows = rows
                    self.column_names = column_names
                    self.rowCount = len(rows)

            # Convert result to a list of dictionaries
            rows = []
            for row in result:
                row_dict = {}
                for i, col_name in enumerate(column_names):
                    row_dict[col_name] = row[i]
                rows.append(row_dict)

            return QueryResult(rows, column_names)

        def release(self):
            self.conn.commit()
            self.cursor.close()
            pool.putconn(self.conn)

    conn = pool.getconn()
    return PoolClient(conn)
