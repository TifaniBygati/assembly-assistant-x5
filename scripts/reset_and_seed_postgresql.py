import json
import os
from pathlib import Path

import psycopg
from psycopg.rows import dict_row
from psycopg import sql


BASE_DIR = Path(__file__).resolve().parent.parent
JSON_PATH = BASE_DIR / 'data' / 'database.json'
INIT_SQL_PATH = BASE_DIR / 'scripts' / 'init_postgresql.sql'

def get_target_db_name():
    return os.getenv('DB_NAME', 'assembly_assistant_x5_dev')


def load_db():
    return psycopg.connect(
        dbname=get_target_db_name(),
        user=os.getenv('DB_USER', 'postgres'),
        password=os.getenv('DB_PASSWORD', 'localbase'),
        host=os.getenv('DB_HOST', '127.0.0.1'),
        port=int(os.getenv('DB_PORT', '5432')),
        row_factory=dict_row
    )

def load_admin_db():
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
    db_name = get_target_db_name()

    with load_admin_db() as con:
        with con.cursor() as cursor:
            cursor.execute('''
            SELECT 1 
            FROM pg_database
            WHERE datname = %s
            ''',
            (db_name,)
            )

            database_exists = cursor.fetchone()

            if database_exists is None:
                cursor.execute(sql.SQL('CREATE DATABASE {};').format(sql.Identifier(db_name)))

def run_init_sql(cursor):
    init_sql = INIT_SQL_PATH.read_text(encoding='utf-8')
    cursor.execute(init_sql)

def load_json_data():
    return json.loads(JSON_PATH.read_text(encoding='utf-8'))

def drop_tables(cursor):
    cursor.execute('DROP TABLE IF EXISTS addresses;')
    cursor.execute('DROP TABLE IF EXISTS clients;')

def empty_to_none(value):
    if value is None:
        return None

    if value == '':
        return None

    return value

def create_client(cursor, item):

    cursor.execute('''
    INSERT INTO clients (name, phone)
    VALUES (%s, %s)
    RETURNING id;
    ''',
    (empty_to_none(item.get('name')), item['phone'])
    )

    row = cursor.fetchone()
    return row['id']

def create_address(cursor, client_id, item):
    cursor.execute('''
    INSERT INTO addresses (
            client_id,
            street,
            house,
            floor,
            entrance,
            apartment,
            comment
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    ''',
    (
    client_id,
    item['street'],
    item['house'],
    empty_to_none(item.get('floor')),
    empty_to_none(item.get('entrance')),
    empty_to_none(item.get('apartment')),
    empty_to_none(item.get('comment'))
    ),)

def seed_rows(cursor, data):
    client_id_map = {}

    for item in data:
        old_client_id = item['id']

        if old_client_id not in client_id_map:
            new_client_id = create_client(cursor, item)
            client_id_map[old_client_id] = new_client_id

        create_address(cursor, client_id_map[old_client_id], item)
    return {
        "clients_created": len(client_id_map),
        "addresses_created": len(data),
    }


def reset_and_seed():

    data = load_json_data()

    create_database_if_not_exists()

    with load_db() as db:
        with db.cursor() as cursor:
            drop_tables(cursor)
            run_init_sql(cursor)

            result = seed_rows(cursor, data)

        print(result)


if __name__ == '__main__':
    reset_and_seed()
