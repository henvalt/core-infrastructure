import psycopg2
from psycopg2 import pool

def connect_to_database(host, database, user, password):
    try:
        connection_pool = pool.ThreadedConnectionPool(
            1, 10, 
            host=host, 
            database=database, 
            user=user, 
            password=password
        )
        connection = connection_pool.getconn()
        cursor = connection.cursor()
        cursor.execute("SELECT version()")
        version = cursor.fetchone()
        print(f"Postgres Server Version: {version[0]}")
        connection_pool.putconn(connection)
    except psycopg2.Error as e:
        print(f"Error connecting to database: {e}")

connect_to_database("localhost", "mydatabase", "myuser", "mypassword")