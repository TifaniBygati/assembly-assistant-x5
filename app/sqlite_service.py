import sqlite3
from pathlib import Path

SRC_MAIN_DIR = Path(__file__).resolve().parent.parent

DB_PATH = SRC_MAIN_DIR / 'data' / 'clients.db'

def load_database():
    db = sqlite3.connect(DB_PATH)
    db.row_factory = sqlite3.Row
    cursor = db.cursor()
    cursor.execute('PRAGMA foreign_keys = ON;')
    return db

def get_all_clients_from_db():

    db = load_database()

    cursor = db.cursor()

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
                   LEFT JOIN addresses AS a ON c.id = a.client_id''')

    rows = cursor.fetchall()

    db.close()

    return [dict(row) for row in rows]

def get_client_by_id_from_db(client_id):

    db = load_database()

    cursor = db.cursor()

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
                   WHERE c.id = ?''', (client_id,))

    rows = cursor.fetchall()

    db.close()

    if not rows:
        return None

    return [dict(row) for row in rows]

def find_clients_by_address_from_db(street=None, house=None, apartment=None):

    check = {
        'street': street,
        'house': house,
        'apartment': apartment
    }

    info = []
    params = []

    for key, value in check.items():
        if value is not None:
            params.append(value)
            info.append(f'a.{key} = ?')

    if not info:
        return []

    db = load_database()

    cursor = db.cursor()

    sql = '''
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
                    JOIN addresses AS a ON c.id = a.client_id
                    WHERE ''' + ' AND '.join(info)


    cursor.execute(sql, params)

    rows = cursor.fetchall()

    db.close()

    return [dict(row) for row in rows]

def create_new_client_from_db(client_data):

    db = load_database()

    cursor = db.cursor()

    sql = 'INSERT INTO clients (order_id, street, house, apartment, phone, comment) VALUES (?, ?, ?, ?, ?, ?);'

    cursor.execute(sql, (
        client_data.order_id,
        client_data.street,
        client_data.house,
        client_data.apartment,
        client_data.phone,
        client_data.comment
    ))

    db.commit()

    last_id = cursor.lastrowid

    cursor.execute('SELECT * FROM clients WHERE id = ?;', (last_id,))

    row = cursor.fetchone()

    db.close()

    return dict(row)

def delete_client_by_client_id_from_db(client_id):

    db = load_database()

    cursor = db.cursor()

    sql = 'DELETE FROM clients WHERE id = ?;'

    cursor.execute(sql, (client_id,))

    db.commit()

    row = cursor.rowcount

    db.close()

    return row > 0

def patch_and_put_client_by_client_id_from_db(client_id, client_data):
    info = []
    params = []

    new_data = client_data.model_dump(exclude_none=True)

    for z, x in new_data.items():
        info.append(f'{z} = ?')
        params.append(x)

    params.append(client_id)

    sql = 'UPDATE clients SET ' + ', '.join(info) + ' WHERE id = ?;'

    db = load_database()
    cursor = db.cursor()

    cursor.execute(sql, params)

    db.commit()

    if cursor.rowcount == 0:
        db.close()
        return None

    cursor.execute('SELECT * FROM clients WHERE id = ?;', (client_id,))

    row = cursor.fetchone()

    db.close()

    return dict(row)