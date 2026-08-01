import os
import json

import psycopg
from psycopg import sql
from psycopg.rows import dict_row

from pathlib import Path



SCRIPTS_DIR = Path(__file__).resolve().parent
INIT_SQL = SCRIPTS_DIR / "init_postgresql.sql"
SEED_PATH = SCRIPTS_DIR.resolve().parent / "seed" / "initial_clients.json"

def get_db_name():
    return os.getenv("DB_NAME", "assembly_assistant_x5_dev")

def db_connect():
    return psycopg.connect(
        dbname=get_db_name(),
        user=os.getenv('DB_USER', 'postgres'),
        password=os.getenv('DB_PASSWORD', 'localbase'),
        host=os.getenv('DB_HOST', '127.0.0.1'),
        port=int(os.getenv('DB_PORT', '5433')),
        row_factory=dict_row
    )

def admin_db_connect():
    return psycopg.connect(
        dbname=os.getenv('DB_ADMIN_NAME', 'template1'),
        user=os.getenv('DB_USER', 'postgres'),
        password=os.getenv('DB_PASSWORD', 'localbase'),
        host=os.getenv('DB_HOST', '127.0.0.1'),
        port=int(os.getenv('DB_PORT', '5433')),
        row_factory=dict_row,
        autocommit=True
    )

def create_database_if_not_exists():
    database = get_db_name()
    with admin_db_connect() as conn:
        with conn.cursor() as cursor:

            cursor.execute('''
            SELECT 1 
            FROM pg_database
            WHERE datname = %s;
            ''',
            (
            database,
            )
            )

            result = cursor.fetchone()

            if result is None:
                cursor.execute(sql.SQL('CREATE DATABASE {};').format(sql.Identifier(database)))

def run_init_sql(cursor):
    init_sql = INIT_SQL.read_text(encoding='utf-8')
    cursor.execute(init_sql)

def empty_to_none(value):
    if value is None:
        return None

    if value == '':
        return None

    return value

def create_client(cursor, item):
    cursor.execute("""
    INSERT INTO clients (name, phone) 
    VALUES (%s, %s)
    RETURNING id;
    """,
    (empty_to_none(item.get('name')),
    item['phone']))

    row = cursor.fetchone()
    return row['id']

def create_address(cursor, new_client_id, item):
    cursor.execute("""
    INSERT INTO addresses (client_id, street, house, floor, entrance, apartment, comment)
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    """,
    (new_client_id,
     item['street'],
     item['house'],
     empty_to_none(item.get('floor')),
     empty_to_none(item.get('entrance')),
     empty_to_none(item.get('apartment')),
     empty_to_none(item.get('comment')),),
    )

def seed_rows(cursor, data):
    client_id_map = {}

    for item in data:
        old_client_id = item['id']

        if old_client_id not in client_id_map:
            new_client_id = create_client(cursor, item)
            client_id_map[old_client_id] = new_client_id
        create_address(
            cursor,
            client_id_map[old_client_id],
            item
        )

    return {
        "clients_created": len(client_id_map),
        "addresses_created": len(data),
    }

def load_seed_data():
    return json.loads(SEED_PATH.read_text(encoding='utf-8'))
