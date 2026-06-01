import json
from pathlib import Path

DATA_DIR  = Path(__file__).resolve().parent

DATABASE_JSON_PATH = DATA_DIR / 'database.json'

def load_data():
    with open(DATABASE_JSON_PATH, 'r', encoding='utf-8') as file:
        data = json.load(file)
        return data

def save_data(data):
    with open(DATABASE_JSON_PATH, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)
