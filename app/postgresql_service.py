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

def get_client_by_id_from_postgre(client_id):
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
            WHERE c.id = %s
            ORDER BY c.id, a.id 
            ''', (client_id,))

            return cursor.fetchall()

def search_clients_from_postgres(street=None, house=None, apartment=None):

    input_params = {
        'street': street,
        'house': house,
        'apartment': apartment,
    }

    conditions = []
    params = []

    for param_name, param_value in input_params.items():
        if param_value is not None:
            conditions.append(f'a.{param_name} = %s')
            params.append(param_value)

    if not conditions:
        return None

    sql_req = '''
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
            WHERE ''' + ' AND '.join(conditions) + ' ORDER BY c.id, a.id '

    with load_database() as db:
        with db.cursor() as cursor:
            cursor.execute(sql_req, params)

            return cursor.fetchall()

def delete_client_from_postgres(client_id):

    with load_database() as db:
        with db.cursor() as cursor:
            cursor.execute('''
            DELETE FROM clients WHERE id = %s
            RETURNING id
            ''', (client_id,))

            row = cursor.fetchone()

            if row is None:
                return None

            return row['id']



















