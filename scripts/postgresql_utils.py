import os
import json

import psycopg
from psycopg.rows import dict_row

from pathlib import Path

SCRIPTS_DIR = Path(__file__).resolve().parent
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
