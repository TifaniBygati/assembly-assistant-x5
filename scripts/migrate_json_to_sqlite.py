import sqlite3

from data.json_storage import load_data

from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent

DB_PATH = PROJECT_ROOT / 'data' / 'clients.db'

data = load_data()

db = sqlite3.connect(DB_PATH)
cursor = db.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS clients (
        id INTEGER PRIMARY KEY,
        order_id TEXT,
        street TEXT,
        house TEXT,
        apartment TEXT,
        phone TEXT,
        comment TEXT
    )
    """)
cursor.execute('DELETE FROM clients')

for client in data:
    cursor.execute("INSERT INTO clients(id, order_id, street, house, apartment, phone, comment) VALUES (?,?,?,?,?,?,?)",
                   (client['id'],
                    client['order_id'],
                    client['street'],
                    client['house'],
                    client['apartment'],
                    client['phone'],
                    client['comment']
                    ))
db.commit()
db.close()