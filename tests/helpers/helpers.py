import json
import sqlite3
from pathlib import Path

TEST_DIR = Path(__file__).resolve().parent

TEST_DATABASE_PATH = TEST_DIR / 'test_database.db'

JSON_PATH = TEST_DIR / 'test_database.json'

def create_test_database():

    with open(JSON_PATH, 'r', encoding='utf-8') as file:

        data = json.load(file)


    db = sqlite3.connect(TEST_DATABASE_PATH)
    cursor = db.cursor()

    cursor.execute('PRAGMA foreign_keys = ON;')

    cursor.execute('DROP TABLE IF EXISTS addresses')
    cursor.execute('DROP TABLE IF EXISTS clients')

    cursor.execute('''
        CREATE TABLE clients (
        id INTEGER PRIMARY KEY,
        name TEXT CHECK (name != '' OR name IS NULL),
        phone TEXT UNIQUE NOT NULL CHECK (phone != ''));
    ''')

    cursor.execute('''
    CREATE TABLE addresses (
        id INTEGER PRIMARY KEY, 
        client_id INTEGER NOT NULL,
        street TEXT NOT NULL CHECK (street != ''), 
        house TEXT NOT NULL CHECK (house != ''),
        floor TEXT CHECK (floor != '' OR floor IS NULL),
        entrance TEXT CHECK (entrance != '' OR entrance IS NULL),
        apartment TEXT CHECK (apartment != '' OR apartment IS NULL),
        comment TEXT NOT NULL DEFAULT '',
        FOREIGN KEY (client_id) REFERENCES clients(id));
    ''')


    cursor.execute('CREATE INDEX IF NOT EXISTS idx_addresses_client_id  ON addresses(client_id);')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_addresses_street_house ON addresses(street, house);')

    db.commit()

    try:
        cursor.execute('BEGIN')

        for x in data:
            name = x.get('name')
            phone = x['phone']
            street = x['street']
            house = x['house']
            floor = x.get('floor')
            entrance = x.get('entrance')
            apartment = x.get('apartment')
            comment = x.get('comment', '')

            cursor.execute('SELECT id FROM clients WHERE phone = ?', (phone,))

            result = cursor.fetchone()

            if result is None:
                cursor.execute('INSERT INTO clients (name, phone) VALUES (?, ?)', (name, phone))

                client_id = cursor.lastrowid

            else:
                client_id = result[0]

            cursor.execute('''INSERT INTO addresses(client_id,street, house, floor, entrance, apartment, comment) VALUES (?,?,?,?,?,?,?)''',
                           (client_id,street, house, floor, entrance, apartment, comment) )
        db.commit()
        
        return TEST_DATABASE_PATH

    except Exception:
        db.rollback()
        raise

    finally:
        db.close()

def setup_test_database(monkeypatch):
    test_database_path = create_test_database()

    monkeypatch.setenv('APP_DB_PATH', str(test_database_path))