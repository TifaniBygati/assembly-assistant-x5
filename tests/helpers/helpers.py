import psycopg
from psycopg.rows import dict_row
from psycopg import sql

from pathlib import Path

import os
import json

TEST_DIR = Path(__file__).resolve().parent.parent

JSON_DATA = TEST_DIR / 'helpers' / 'test_database.json'

INIT_SQL = TEST_DIR.parent / 'scripts' / 'init_postgresql.sql'

def get_test_db_name():
    return os.getenv('DB_NAME', 'assembly_assistant_x5_test')

def load_test_db():
    return psycopg.connect(
            dbname=get_test_db_name(),
            user=os.getenv('DB_USER', 'postgres'),
            password=os.getenv('DB_PASSWORD', 'localbase'),
            host=os.getenv('DB_HOST', '127.0.0.1'),
            port=int(os.getenv('DB_PORT', '5432')),
            row_factory=dict_row
        )

def admin_db():
    return psycopg.connect(
            dbname=os.getenv("DB_ADMIN_NAME", "template1"),
            user=os.getenv("DB_USER", "postgres"),
            password=os.getenv("DB_PASSWORD", "localbase"),
            host=os.getenv("DB_HOST", "127.0.0.1"),
            port=int(os.getenv("DB_PORT", "5432")),
            row_factory=dict_row,
            autocommit=True,
        )

def create_database_if_not_exists():
    db_name = get_test_db_name()

    with admin_db() as db:
        with db.cursor() as cur:
            cur.execute('''
            SELECT 1
            FROM pg_database
            WHERE datname = %s;
            ''', (db_name,))

            database_exists = cur.fetchone()

            if database_exists is None:
                cur.execute(sql.SQL('CREATE DATABASE {};').format(sql.Identifier(db_name)))

def drop_tables_if_exist(cursor):
    cursor.execute('''DROP TABLE IF EXISTS addresses;''')
    cursor.execute('''DROP TABLE IF EXISTS clients;''')

def run_init_sql(cursor):
    init_sql = INIT_SQL.read_text(encoding='utf-8')
    cursor.execute(init_sql)

def load_test_data_json():
    test_data = JSON_DATA.read_text(encoding='utf-8')
    return json.loads(test_data)

def empty_to_none(value):
    if value is None:
        return None

    if value == '':
        return None

    return value

def create_test_client(cursor, item):
    cursor.execute('''
    INSERT INTO clients (name, phone) VALUES (%s, %s)
    RETURNING id;
    ''',(empty_to_none(item.get('name')), item['phone']))

    client_id = cursor.fetchone()
    return client_id['id']

def create_test_address(cursor, client_uuid, item):
    cursor.execute('''
    INSERT INTO addresses(            
        client_id,
        street,
        house,
        floor,
        entrance,
        apartment,
        comment
    ) VALUES (%s, %s, %s, %s, %s, %s, %s)''',
    (client_uuid,
    item['street'],
    item['house'],
    empty_to_none(item.get('floor')),
    empty_to_none(item.get('entrance')),
    empty_to_none(item.get('apartment')),
    empty_to_none(item.get('comment'))))

def migrate_rows_on_test_db(cursor, data):
    client_uuid_map = {}

    for item in data:
        client_uuid_phone = item['phone']

        if client_uuid_phone not in client_uuid_map:
            new_id = create_test_client(cursor, item)
            client_uuid_map[client_uuid_phone] = new_id

        create_test_address(cursor, client_uuid_map[client_uuid_phone], item)
    return {
        "clients_created": len(client_uuid_map),
        "addresses_created": len(data),
    }

def create_test_db():

    data = load_test_data_json()

    create_database_if_not_exists()

    with load_test_db() as db:
        with db.cursor() as cursor:
            drop_tables_if_exist(cursor)
            run_init_sql(cursor)
            result = migrate_rows_on_test_db(cursor, data)

        print(result)

def setup_test_database(monkeypatch):
    monkeypatch.setenv('DB_NAME', 'assembly_assistant_x5_test')
    create_test_db()