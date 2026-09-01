import os
import json

import psycopg
from psycopg.rows import dict_row
from psycopg import sql

from alembic import command
from alembic.config import Config

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from pathlib import Path

from app.main import app
from app.database import get_session


TEST_DIR = Path(__file__).resolve().parent.parent
PROJECT_ROOT = TEST_DIR.parent

JSON_DATA = TEST_DIR / 'helpers' / 'test_database.json'


def get_test_db_name():
    return os.getenv('DB_NAME', 'assembly_assistant_x5_test')


def load_test_db():
    return psycopg.connect(
        dbname=get_test_db_name(),
        user=os.getenv('DB_USER', 'postgres'),
        password=os.getenv('DB_PASSWORD', 'localbase'),
        host=os.getenv('DB_HOST', '127.0.0.1'),
        port=int(os.getenv('DB_PORT', '5433')),
        row_factory=dict_row
    )


def admin_db():
    return psycopg.connect(
        dbname=os.getenv('DB_ADMIN_NAME', 'template1'),
        user=os.getenv('DB_USER', 'postgres'),
        password=os.getenv('DB_PASSWORD', 'localbase'),
        host=os.getenv('DB_HOST', '127.0.0.1'),
        port=int(os.getenv('DB_PORT', '5433')),
        row_factory=dict_row,
        autocommit=True,
    )


def create_database_if_not_exists():
    db_name = get_test_db_name()

    with admin_db() as db:
        with db.cursor() as cur:
            cur.execute(
                '''
                SELECT 1
                FROM pg_database
                WHERE datname = %s;
                ''',
                (db_name,)
            )

            database_exists = cur.fetchone()

            if database_exists is None:
                cur.execute(
                    sql.SQL('CREATE DATABASE {};').format(
                        sql.Identifier(db_name)
                    )
                )


def run_migrations():
    alembic_config = Config(
        str(PROJECT_ROOT / 'alembic.ini')
    )

    command.upgrade(alembic_config, 'head')


def clear_test_data(cursor):
    cursor.execute(
        'TRUNCATE TABLE clients RESTART IDENTITY CASCADE;'
    )


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
    cursor.execute(
        '''
        INSERT INTO clients (name, phone)
        VALUES (%s, %s)
        RETURNING id;
        ''',
        (
            empty_to_none(item.get('name')),
            item['phone']
        )
    )

    client_id = cursor.fetchone()
    return client_id['id']


def create_test_address(cursor, client_uuid, item):
    cursor.execute(
        '''
        INSERT INTO addresses(
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
            client_uuid,
            item['street'],
            item['house'],
            empty_to_none(item.get('floor')),
            empty_to_none(item.get('entrance')),
            empty_to_none(item.get('apartment')),
            empty_to_none(item.get('comment'))
        )
    )


def migrate_rows_on_test_db(cursor, data):
    client_key = {}

    for item in data:
        client_id = item['phone']

        if client_id not in client_key:
            new_id = create_test_client(cursor, item)
            client_key[client_id] = new_id

        create_test_address(
            cursor,
            client_key[client_id],
            item
        )

    return {
        'clients_created': len(client_key),
        'addresses_created': len(data),
    }


def create_test_db():
    data = load_test_data_json()

    create_database_if_not_exists()

    run_migrations()

    with load_test_db() as db:
        with db.cursor() as cursor:
            clear_test_data(cursor)
            migrate_rows_on_test_db(cursor, data)


def setup_test_database(monkeypatch):
    monkeypatch.setenv(
        'DB_NAME',
        'assembly_assistant_x5_test'
    )

    create_test_db()

    DB_HOST = os.getenv('DB_HOST', '127.0.0.1')
    DB_PORT = int(os.getenv('DB_PORT', '5433'))
    DB_USER = os.getenv('DB_USER', 'postgres')
    DB_PASSWORD = os.getenv('DB_PASSWORD', 'localbase')
    DB_NAME = os.getenv(
        'DB_NAME',
        'assembly_assistant_x5_test'
    )

    test_engine = create_engine(
        f'postgresql+psycopg://'
        f'{DB_USER}:{DB_PASSWORD}@'
        f'{DB_HOST}:{DB_PORT}/{DB_NAME}'
    )

    TestSessionLocal = sessionmaker(bind=test_engine)

    def get_test_session():
        with TestSessionLocal() as session:
            yield session

    monkeypatch.setitem(
        app.dependency_overrides,
        get_session,
        get_test_session
    )