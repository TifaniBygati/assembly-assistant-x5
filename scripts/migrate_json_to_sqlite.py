from data.json_storage import load_data
import sqlite3
from pathlib import Path

DIR = Path(__file__).resolve().parent.parent

DATABASE = DIR / 'data' / 'clients.db'

data = load_data()

db = sqlite3.connect(DATABASE)
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

    for row in data:

        name = row.get('name')
        street = row['street']
        house = row['house']
        floor = row.get('floor')
        entrance = row.get('entrance')
        apartment = row.get('apartment')
        phone = row['phone']
        comment = row.get('comment','')

        cursor.execute('SELECT id FROM clients WHERE phone = ?', (phone,))

        result = cursor.fetchone()

        if result is None:
            cursor.execute('INSERT INTO clients (name, phone) VALUES (?, ?)', (name, phone))

            client_id = cursor.lastrowid
        else:
            client_id = result[0]

        cursor.execute('''INSERT INTO addresses(client_id, street, house, floor, entrance, apartment, comment) 
                          VALUES (?,?,?,?,?,?,?)''', (client_id, street, house, floor, entrance, apartment, comment))

    db.commit()

except Exception:
    db.rollback()
    raise
finally:
    db.close()