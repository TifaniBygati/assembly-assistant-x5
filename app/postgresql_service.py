import os

import psycopg
from psycopg.rows import dict_row

def load_database():
    return psycopg.connect(
        host = os.getenv('DB_HOST', '127.0.0.1'),
        port = int(os.getenv('DB_PORT', '5433')),
        user = os.getenv('DB_USER', 'postgres'),
        password = os.getenv('DB_PASSWORD', 'localbase'),
        dbname = os.getenv('DB_NAME', 'assembly_assistant_x5_dev'),
        row_factory = dict_row
    )

def empty_to_none(value):
    if value is None:
        return None

    if value == '':
        return None

    return value

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

def create_client_from_postgres(client_data):
    with load_database() as db:
        with db.cursor() as cursor:

            cursor.execute('''
                        SELECT id, name, phone
                        FROM clients
                        WHERE phone = %s
                        ''', (client_data.phone,))

            result = cursor.fetchone()

            if result is None:
                cursor.execute('''
                INSERT INTO clients (name, phone) VALUES (%s, %s)
                    RETURNING id
                ''', (empty_to_none(client_data.name), client_data.phone))

                result = cursor.fetchone()
                client_id = result['id']
            else:
                client_id = result['id']

            cursor.execute('''
            INSERT INTO addresses (client_id, street, house, floor, entrance, apartment, comment)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            ''',
            (client_id, client_data.street, client_data.house, empty_to_none(client_data.floor), empty_to_none(client_data.entrance), empty_to_none(client_data.apartment), empty_to_none(client_data.comment))
            )

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

def client_update_patch_from_postgres(client_id, client_data):
    with load_database() as db:
        with db.cursor() as cursor:

            cursor.execute('''
            SELECT * FROM clients WHERE id = %s
            ''',(client_id,))

            result = cursor.fetchone()

            if result is None:
                return None

            new_data = client_data.model_dump(exclude_none=True)

            set_parts = []
            params = []

            for name, value in new_data.items():
                if name == 'name':
                    value = empty_to_none(value)

                set_parts.append(f'{name} = %s')
                params.append(value)

            sql_req = ' UPDATE clients SET ' + ', '.join(set_parts) + ' WHERE id = %s'

            params.append(client_id)

            cursor.execute(sql_req, params)

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
            ''',
            (client_id,)
            )

            return cursor.fetchall()

def addresses_update_patch_from_postgres(address_id, address_data):
    with load_database() as db:
        with db.cursor() as cursor:

            cursor.execute('''
            SELECT client_id FROM addresses WHERE id = %s
            ''', (address_id,))

            result = cursor.fetchone()

            if result is None:
                return None

            client_id = result['client_id']

            new_data = address_data.model_dump(exclude_none=True)

            set_parts = []
            params = []

            for name, value in new_data.items():
                if name in ['floor', 'entrance', 'apartment', 'comment']:
                    value = empty_to_none(value)

                set_parts.append(f'{name} = %s')
                params.append(value)

            sql_req = ' UPDATE addresses SET ' + ', '.join(set_parts) + ' WHERE id = %s'

            params.append(address_id)

            cursor.execute(sql_req, params)

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
            FROM addresses AS a
            JOIN clients AS c ON a.client_id = c.id
            WHERE c.id = %s
            ORDER BY c.id, a.id
            ''',
            (client_id,)
            )

            return cursor.fetchall()

def client_update_put_from_postgres(client_id, client_data):

    with load_database() as db:

        with db.cursor() as cursor:

            cursor.execute('''
            SELECT id FROM clients WHERE id = %s
            ''', (client_id,))

            result = cursor.fetchone()

            if result is None:
                return None

            new_data = client_data.model_dump()

            set_parts = []
            params = []

            for name, value in new_data.items():

                set_parts.append(f'{name} = %s')
                params.append(value)

            sql_req = ' UPDATE clients SET ' + ', '.join(set_parts) + ' WHERE id = %s'

            params.append(client_id)

            cursor.execute(sql_req, params)

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

def addresses_update_put_from_postgres(address_id, address_data):

    with load_database() as db:
        with db.cursor() as cursor:

            cursor.execute('''
            SELECT client_id
            FROM addresses
            WHERE id = %s
            ''', (address_id,))

            result = cursor.fetchone()

            if result is None:
                return None

            client_id = result['client_id']

            new_data = address_data.model_dump()

            set_parts = []
            params = []

            for name, value in new_data.items():
                if name in ['floor', 'entrance', 'apartment', 'comment']:
                    value = empty_to_none(value)

                set_parts.append(f'{name} = %s')
                params.append(value)

            sql_req = ' UPDATE addresses SET ' + ', '.join(set_parts) + ' WHERE id = %s'

            params.append(address_id)

            cursor.execute(sql_req, params)

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
            FROM addresses AS a
            JOIN clients AS c ON a.client_id = c.id
            WHERE c.id = %s
            ORDER BY c.id, a.id
            ''', (client_id,))

            return cursor.fetchall()