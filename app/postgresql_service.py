import os
import psycopg
from psycopg.rows import dict_row

def load_database():
    return psycopg.connect(
        host = os.getenv('DB_HOST', '127.0.0.1'),
        port = int(os.getenv('DB_PORT', '5432')),
        user = os.getenv('DB_USER', 'postgres'),
        password = os.getenv('DB_PASSWORD', 'localbase'),
        dbname = os.getenv('DB_NAME', 'assembly_assistant_x5_dev'),
        row_factory = dict_row
    )

def get_clients_from_postgres():
    with load_database() as db:
        with db.cursor() as cursor:
            cursor.execute('''
            SELECT 
                c.id AS client_id,
                c.name,
                c.phone,
                a.id AS address_id,
                a.street,
                a.house,
                a.floor,
                a.entrance,
                a.apartment,
                a.comment
            FROM clients AS c
            LEFT JOIN addresses AS a ON c.id = a.client_id
            ORDER BY c.id, a.id 
            ''')

            return cursor.fetchall()