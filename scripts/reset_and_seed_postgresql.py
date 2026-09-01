import os

from postgresql_utils import (
    db_connect,
    seed_rows,
    load_seed_data
)


def db_reset_is_allowed():
    return os.getenv(
        'ALLOW_DB_RESET',
        ''
    ).strip().lower() == 'true'


def clear_tables(cursor):
    cursor.execute(
        'TRUNCATE TABLE clients RESTART IDENTITY CASCADE;'
    )


def reset_and_seed():
    if not db_reset_is_allowed():
        print(
            'Database reset blocked. '
            'Set ALLOW_DB_RESET=true to continue.'
        )
        return

    data = load_seed_data()

    with db_connect() as db:
        with db.cursor() as cursor:
            clear_tables(cursor)

            result = seed_rows(cursor, data)

        print(result)


if __name__ == '__main__':
    reset_and_seed()
