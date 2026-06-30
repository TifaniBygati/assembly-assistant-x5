import os
import psycopg
from psycopg.rows import dict_row

def load_database():
    return psycopg.connect(
        host = os.getenv('DB_HOST', '127.0.0.1'),
        port = os.getenv('DB_PORT', '5432'),
        user = os.getenv('DB_USER', 'postgres'),
        password = os.getenv('DB_PASSWORD', 'localbase'),
        dbname = os.getenv('DB_NAME', 'postgres'),
        row_factory = dict_row
    )

