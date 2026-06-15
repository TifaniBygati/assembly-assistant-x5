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

    try:
        cursor.execute('BEGIN')

        cursor.execute('SELECT id FROM clients WHERE phone = ?', (client_data.phone, ))

        result = cursor.fetchone()

        if result is None:
            cursor.execute('INSERT INTO clients (name, phone) VALUES (?, ?)',(client_data.name, client_data.phone))

            client_id = cursor.lastrowid
        else:
            client_id = result['id']

        comment = client_data.comment or ''

        cursor.execute('INSERT INTO addresses (client_id, street, house, floor, entrance, apartment, comment)'
                       'VALUES (?,?,?,?,?,?,?)',(
            client_id,
            client_data.street,
            client_data.house,
            client_data.floor,
            client_data.entrance,
            client_data.apartment,
            comment
            ))

        address_id_last = cursor.lastrowid

        db.commit()
        cursor.execute('''
                       SELECT c.id AS client_id,
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
                       WHERE a.id = ?
                       ''', (address_id_last,))

        row = cursor.fetchone()

        return dict(row)

    except Exception:

        db.rollback()
        raise

    finally:
        db.close()

def delete_client_from_db(client_id):
    db = load_database()

    cursor = db.cursor()

    try:
        cursor.execute('BEGIN')

        cursor.execute('SELECT id FROM clients WHERE id = ?', (client_id,))

        result = cursor.fetchone()

        if result is None:
            db.rollback()#
            return None

        cursor.execute('DELETE FROM addresses WHERE client_id = ?', (client_id,))

        cursor.execute('DELETE FROM clients WHERE id = ?', (client_id,))

        db.commit()

        return {'deleted': True, 'client_id': client_id}

    except Exception:
        db.rollback()
        raise

    finally:
        db.close()

def client_address_update(address_id,client_data):

    db = load_database()

    cursor = db.cursor()

    try:

        cursor.execute("BEGIN")

        cursor.execute('SELECT id FROM addresses WHERE id = ?', (address_id,))

        result = cursor.fetchone()

        if result is None:
            db.rollback()
            return None

        new_params = client_data.model_dump(exclude_none=True)

        params = []
        info = []

        for z, x in new_params.items():
            params.append(f'{z} = ?')
            info.append(x)

        if not info:
            db.rollback()
            return None

        sql = 'UPDATE addresses SET ' + ', ' .join(params) + ' WHERE id = ?'

        info.append(address_id)

        cursor.execute(sql, info)

        db.commit()

        cursor.execute('''SELECT 
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
            LEFT JOIN clients AS c ON a.client_id = c.id
            WHERE a.id = ?
                       ''', (address_id,))

        result = cursor.fetchone()

        return dict(result)

    except Exception:
        db.rollback()
        raise

    finally:
        db.close()

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