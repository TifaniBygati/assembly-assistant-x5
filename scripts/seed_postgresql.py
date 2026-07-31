import json
from pathlib import Path

from postgresql_utils import (
    create_database_if_not_exists,
    db_connect,
    run_init_sql,
    seed_rows
    )
BASE_DIR = Path(__file__).resolve().parent.parent
SEED_PATH  = BASE_DIR / "seed" / "initial_clients.json"

def load_seed_data():
    return json.loads(SEED_PATH.read_text(encoding="utf-8"))

def database_is_empty(cursor):
    cursor.execute("""
    SELECT 
        EXISTS (SELECT 1 FROM clients) AS client_exists,
        EXISTS (SELECT 1 FROM addresses) AS addresses_exists;
    """)

    row = cursor.fetchone()

    return not any((row['client_exists'],
                    row['addresses_exists']))

def seed_postgresql():
    create_database_if_not_exists()
    with db_connect() as db:
        with db.cursor() as cursor:

            run_init_sql(cursor)

            if not database_is_empty(cursor):
                print("Database is not empty. Seeding skipped")
                return
            data = load_seed_data()
            print(f"Seed rows loaded: {len(data)}")
            result = seed_rows(cursor, data)

    print(result)



if __name__ == '__main__':
    seed_postgresql()
