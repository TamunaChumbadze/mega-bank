import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()  

DATABASE_URL = os.getenv("DATABASE_URL")

connection_str = os.getenv("DATABASE_URL")
print(connection_str)