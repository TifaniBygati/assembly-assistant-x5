from fastapi.testclient import TestClient
from app.main import app
from tests.helpers.helpers import create_test_database

client = TestClient(app)


def test_get_clients():
    response = client.get('/clients')

    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_client_by_id():
    response = client.get('/clients')

    assert response.status_code == 200

    clients = response.json()

    assert clients != []

    client_id = clients[0]['client_id']

    response = client.get(f'/clients/{client_id}')

    body = response.json()

    assert response.status_code == 200
    assert isinstance(body, list)
    assert body[0]['client_id'] == client_id

def test_get_client_by_address():

    response = client.get('/clients')

    assert response.status_code == 200

    clients = response.json()

    assert clients != []

    client_id = clients[0]['client_id']

    response = client.get(f'/clients/{client_id}')

    assert response.status_code == 200

    body = response.json()

    assert isinstance(body, list)
    assert body != []
    assert body[0]['client_id'] == client_id

    street = body[0]['street']
    house = body[0]['house']

    response = client.get('/clients/search', params={'street': street, 'house': house})

    assert response.status_code == 200

    body = response.json()

    assert isinstance(body, list)
    assert body != []
    assert body[0]['street'] == street
    assert body[0]['house'] == house

def test_clients_from_test_database(monkeypatch):
    test_database_path = create_test_database()

    monkeypatch.setenv('APP_DB_PATH', str(test_database_path))

    response = client.get('/clients')

    assert response.status_code == 200

    body = response.json()
    assert isinstance(body, list)
    assert len(body) == 2

    phones = {client['phone'] for client in body}

    assert phones == {'+79990000001', '+79990000002'}

def test_create_client_in_test_database(monkeypatch):
    test_database_path = create_test_database()

    monkeypatch.setenv('APP_DB_PATH', str(test_database_path))

    payload = {
        'name': 'Петя',
        'phone': '+79990000003',
        'street': 'Ленина',
        'house': '5',
        'floor': '2',
        'entrance': '1',
        'apartment': '10',
        'comment': 'тестовый клиент'
    }

    response = client.post('/clients', json=payload)

    assert response.status_code == 200

    body = response.json()

    assert isinstance(body, dict)
    assert 'client_id' in body

    client_id = body['client_id']

    response = client.get(f'/clients/{client_id}')

    assert response.status_code == 200

    body = response.json()

    assert isinstance(body, list)
    assert len(body) == 1
    assert body[0]['phone'] == payload['phone']
    assert body[0]['name'] == payload['name']

    response = client.get('/clients')

    assert response.status_code == 200

    body = response.json()

    assert isinstance(body, list)
    assert len(body) == 3

    phones = {client_data['phone'] for client_data in body}

    assert payload['phone'] in phones

def test_patch_client_in_test_database(monkeypatch):

    payload = {
        'name': 'test_patch_name',
        'phone': 'test_patch_phone',
    }

    test_database_path = create_test_database()

    monkeypatch.setenv('APP_DB_PATH', str(test_database_path))

    response = client.get('/clients')

    assert response.status_code == 200

    body = response.json()

    assert isinstance(body, list)
    assert body != []

    client_id = body[0]['client_id']

    response = client.get(f'/clients/{client_id}')

    assert response.status_code == 200

    body = response.json()

    assert isinstance(body, list)
    assert len(body) == 1

    client_id = body[0]['client_id']

    old_name = body[0]['name']
    old_phone = body[0]['phone']

    response = client.patch(f'/clients/{client_id}', json=payload)

    assert response.status_code == 200

    body = response.json()

    assert isinstance(body, dict)

    assert body['id'] == client_id

    assert body['name'] != old_name
    assert body['phone'] != old_phone

    assert body['name'] == payload['name']
    assert body['phone'] == payload['phone']

    response = client.get(f'/clients/{client_id}')

    assert response.status_code == 200

    body = response.json()

    assert isinstance(body, list)

    assert len(body) == 1

    assert body[0]['name'] == payload['name']
    assert body[0]['phone'] == payload['phone']

def test_patch_address_in_test_database(monkeypatch):

    payload = {
        'street':'Мира',
        'house':'5',
        'floor':'2',
        'entrance':'1',
        'apartment':'10'
    }

    test_database_path = create_test_database()

    monkeypatch.setenv('APP_DB_PATH', str(test_database_path))

    response = client.get('/clients')

    assert response.status_code == 200

    body = response.json()

    assert isinstance(body, list)
    assert body != []

    client_id = body[0]['client_id']

    response = client.get(f'/clients/{client_id}')

    assert response.status_code == 200

    body = response.json()

    assert isinstance(body, list)
    assert len(body) == 1

    address_id = body[0]['address_id']

    response = client.patch(f'/clients/addresses/{address_id}', json=payload)

    assert response.status_code == 200

    body = response.json()

    assert isinstance(body, dict)
    assert body['address_id'] == address_id

    assert body['street'] == payload['street']
    assert body['house'] == payload['house']
    assert body['floor'] == payload['floor']
    assert body['entrance'] == payload['entrance']
    assert body['apartment'] == payload['apartment']

    response = client.get(f'/clients/{client_id}')

    assert response.status_code == 200

    body = response.json()

    assert isinstance(body, list)
    assert len(body) == 1
    assert body[0]['address_id'] == address_id

    assert body[0]['street'] == payload['street']
    assert body[0]['house'] == payload['house']
    assert body[0]['floor'] == payload['floor']
    assert body[0]['entrance'] == payload['entrance']
    assert body[0]['apartment'] == payload['apartment']

def test_put_client_in_test_database(monkeypatch):

    payload = {
        'name': 'test_put_name',
        'phone': 'test_put_phone'
    }

    test_database_path = create_test_database()

    monkeypatch.setenv('APP_DB_PATH', str(test_database_path))

    response = client.get('/clients')

    assert response.status_code == 200

    body = response.json()

    assert isinstance(body, list)
    assert body != []

    client_id = body[0]['client_id']

    response = client.put(f'/clients/{client_id}', json=payload)

    assert response.status_code == 200

    body = response.json()

    assert isinstance(body, dict)

    assert body['client_id'] == client_id
    assert body['name'] == payload['name']
    assert body['phone'] == payload['phone']

    response = client.get(f'/clients/{client_id}')

    assert response.status_code == 200

    body = response.json()

    assert isinstance(body, list)
    assert len(body) == 1

    assert body[0]['name'] == payload['name']
    assert body[0]['phone'] == payload['phone']

def test_put_address_in_test_database(monkeypatch):

    payload = {
        'street': 'Мира',
        'house': '77',
        'floor': None,
        'entrance': None,
        'apartment': None,
        'comment': 'частный дом'
    }

    test_database_path = create_test_database()

    monkeypatch.setenv('APP_DB_PATH', str(test_database_path))

    response = client.get('/clients')

    assert response.status_code == 200

    body = response.json()

    assert isinstance(body, list)
    assert body != []

    client_id = body[0]['client_id']

    response = client.get(f'/clients/{client_id}')

    assert response.status_code == 200

    body = response.json()

    assert isinstance(body, list)
    assert len(body) == 1

    address_id = body[0]['address_id']

    response = client.put(f'/clients/addresses/{address_id}', json=payload)

    assert response.status_code == 200

    body = response.json()

    assert isinstance(body, dict)

    assert body['street'] == payload['street']
    assert body['house'] == payload['house']
    assert body['comment'] == payload['comment']
    assert body['floor'] == payload['floor']
    assert body['entrance'] == payload['entrance']
    assert body['apartment'] == payload['apartment']

    response = client.get(f'/clients/{client_id}')

    assert response.status_code == 200

    body = response.json()

    assert isinstance(body, list)
    assert len(body) == 1

    assert body[0]['street'] == payload['street']
    assert body[0]['house'] == payload['house']
    assert body[0]['floor'] == payload['floor']
    assert body[0]['entrance'] == payload['entrance']
    assert body[0]['apartment'] == payload['apartment']
    assert body[0]['comment'] == payload['comment']