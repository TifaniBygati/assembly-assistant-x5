import os

from postgresql_utils import (
    create_database_if_not_exists,
    run_init_sql,
    db_connect,
    seed_rows,
    load_seed_data
)

def db_reset_is_allowed():
    return os.getenv('ALLOW_DB_RESET', '').strip().lower() == 'true'

def drop_tables(cursor):
    cursor.execute('DROP TABLE IF EXISTS addresses;')
    cursor.execute('DROP TABLE IF EXISTS clients;')

def reset_and_seed():
    if not db_reset_is_allowed():
        print(
            "Database reset blocked. "
            "Set ALLOW_DB_RESET=true to continue."
        )
        return


    data = load_seed_data()

    create_database_if_not_exists()

    with db_connect() as db:
        with db.cursor() as cursor:

            drop_tables(cursor)

            run_init_sql(cursor)

            result = seed_rows(cursor, data)

        print(result)


if __name__ == '__main__':
    reset_and_seed()
