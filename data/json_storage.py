import json

def load_data():
    with open('./data/database.json', 'r', encoding='utf-8') as file:
        data = json.load(file)
        return data

def save_data(data):
    with open('./data/database.json', 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

def load_data_for_migrate():
    with open('../data/database.json', 'r', encoding='utf-8') as file:
        data = json.load(file)
        return data