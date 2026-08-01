from postgresql_utils import (
    create_database_if_not_exists,
    db_connect,
    run_init_sql
    )
def init_postgresql():
    create_database_if_not_exists()

    with db_connect() as connection:
        with connection.cursor() as cursor:
            run_init_sql(cursor)

    print("PostgreSQL database initialized")
if __name__ == "__main__":
    init_postgresql()