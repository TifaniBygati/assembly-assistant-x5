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