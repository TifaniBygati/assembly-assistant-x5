import json
from pathlib import Path

from postgresql_utils import (
    create_database_if_not_exists,
    run_init_sql,
    db_connect,
    seed_rows
)

BASE_DIR = Path(__file__).resolve().parent.parent
JSON_PATH = BASE_DIR / 'data' / 'database.json'

def load_json_data():
    return json.loads(JSON_PATH.read_text(encoding='utf-8'))

def drop_tables(cursor):
    cursor.execute('DROP TABLE IF EXISTS addresses;')
    cursor.execute('DROP TABLE IF EXISTS clients;')

def reset_and_seed():

    data = load_json_data()

    create_database_if_not_exists()

    with db_connect() as db:
        with db.cursor() as cursor:

            drop_tables(cursor)

            run_init_sql(cursor)

            result = seed_rows(cursor, data)

        print(result)


if __name__ == '__main__':
    reset_and_seed()
