import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()  

def get_connection():
    """Creat and return a database connection using environment variables."""
    try:
        conn = psycopg2.connect(os.getenv("DATABASE_URL"))
        return conn
    except Exception as e:
        print(f"Error connecting to the database: {e}")
        return None
    
def init_database():
    """initialize the database with required tables."""
    conn = get_connection()
    if conn is None:
        return False
    
    try:
        cursor = conn.cursor()
        with open('schema.sql', 'r') as f:
            schema = f.read()
        
        cursor.execute(schema)
        conn.commit()
        cursor.close()
        conn.close()
        print("Database initialized successfully.")
        return True

    except Exception as e:
        print(f"Error initializing database: {e}")
        return False
    
init_database()