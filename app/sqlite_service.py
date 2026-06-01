import sqlite3
from pathlib import Path

SRC_MAIN_DIR = Path(__file__).resolve().parent.parent

DB_PATH = SRC_MAIN_DIR / 'data' / 'clients.db'

def load_database():
    db = sqlite3.connect(DB_PATH)
    db.row_factory = sqlite3.Row
    return db

def get_all_clients_from_db():

    db = load_database()

    cursor = db.cursor()

    cursor.execute('SELECT * FROM clients;')

    rows = cursor.fetchall()

    db.close()

    return [dict(row) for row in rows]